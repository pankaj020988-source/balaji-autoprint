import streamlit as st
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - बिल मॅनेजर", page_icon="🧾", layout="centered")

# ==========================================
# गुगल SHEET जोडणी (Google Sheet Connection)
# ==========================================
def get_next_bill_number_and_save(row_data_without_no):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        if "gcp_service_account" in st.secrets:
            creds_dict = json.loads(st.secrets["gcp_service_account"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        elif os.path.exists("credentials.json"):
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        else:
            return False, f"BCP-{datetime.now().strftime('%H%M%S')}"
            
        client = gspread.authorize(creds)
        spreadsheet = client.open("बालाजी सायबर पॉइंट हिशोब")
        
        try:
            sheet = spreadsheet.worksheet("बिल डेटा")
        except gspread.exceptions.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title="बिल डेटा", rows="1000", cols="10")
            sheet.append_row(["तारीख/वेळ", "बिल नंबर", "ग्राहक नाव", "मोबाईल नंबर", "कामाचा प्रकार", "एकूण रक्कम"])
        
        all_records = sheet.get_all_values()
        next_serial = 101
        if len(all_records) > 1:
            last_row = all_records[-1]
            last_bill_no = last_row[1]
            try:
                last_num = int(last_bill_no.split('-')[1])
                next_serial = last_num + 1
            except:
                next_serial = 101 + (len(all_records) - 1)

        final_bill_no = f"BCP-{next_serial}"
        full_row_data = [row_data_without_no[0], final_bill_no, row_data_without_no[1], row_data_without_no[2], row_data_without_no[3], row_data_without_no[4]]
        sheet.append_row(full_row_data)
        return True, final_bill_no
    except Exception as e:
        st.sidebar.error(f"Google Sheet Error: {e}")
        return False, f"BCP-{datetime.now().strftime('%H%M%S')}"

# ==========================================
# स्टेट मॅनेजमेंट (मागील डेटा साठवण्यासाठी)
# ==========================================
if "items_list" not in st.session_state:
    st.session_state.items_list = []

st.markdown("<h2 style='text-align: center; color: #0056b3;'>🧾 बालाजी सायबर पॉइंट - स्मार्ट बिल मेकर </h2>", unsafe_allow_html=True)
st.write("---")

# 👤 ग्राहक माहिती इनपुट
col1, col2 = st.columns(2)
with col1:
    cust_name = st.text_input("ग्राहक नाव (Customer Name):", key="c_name")
with col2:
    cust_phone = st.text_input("मोबाईल नंबर (Optional):", key="c_phone")

st.markdown("<h5 style='color: #0056b3;'>──────── काम आणि कॅल्क्युलेटर ────────</h5>", unsafe_allow_html=True)

# 🛠️ सेवा निवडणे
services = [
    "निवडा...",
    "Xerox / झेरॉक्स", 
    "Color Printout / कलर प्रिंट", 
    "Lamination / लॅमिनेशन", 
    "Passport Photo / पासपोर्ट फोटो",
    "Online Form / ऑनलाईन फॉर्म फी",
    "Other / इतर सेवा (मॅन्युअली रक्कम टाका)"
]
selected_service = st.selectbox("सेवा निवडा (Select Service):", services)

calculated_amount = 0.0
final_service_name = selected_service

# 📊 सेवेनुसार ऑटो-कॅल्क्युलेटर
if "Xerox" in selected_service or "Color Printout" in selected_service or "Lamination" in selected_service:
    default_rate = 5.0 if "Xerox" in selected_service else (10.0 if "Color" in selected_service else 50.0)
    
    c_col1, c_col2, c_col3 = st.columns(3)
    with c_col1:
        pages = st.number_input("पेजेस (Pages):", min_value=1, value=1, step=1)
    with c_col2:
        copies = st.number_input("कॉपी (Copies):", min_value=1, value=1, step=1)
    with c_col3:
        rate = st.number_input("दर (Rate ₹):", min_value=0.0, value=default_rate, step=0.5)
        
    calculated_amount = float(pages * copies * rate)
    final_service_name = f"{selected_service} ({pages} Pg x {copies} Copy)"

elif "Passport Photo" in selected_service:
    photo_pack = st.selectbox("फोटो पॅक निवडा:", ["4X6 - 9 Photo (₹ 60)", "A4 - 36 Photo (₹ 150)"])
    calculated_amount = 60.0 if "60" in photo_pack else 150.0
    final_service_name = f"Passport Photo ({photo_pack.split(' (')[0]})"

elif "Other" in selected_service:
    custom_name = st.text_input("कामाचे नाव लिहा:")
    final_service_name = custom_name

# 💰 एकूण रक्कम इनपुट (बदलण्याची मुभा)
final_amount = st.number_input("एकूण रक्कम (₹) [येथे बदलू शकता]:", min_value=0.0, value=float(calculated_amount), step=1.0)

# ➕ यादीत काम जोडण्याचे बटण
if st.button("➕ Add Item (यादीत काम जोडा)", type="primary", use_container_width=True):
    if selected_service == "निवडा..." or final_amount <= 0:
        st.error("कृपया सेवा निवडा आणि योग्य रक्कम भरा!")
    elif "Other" in selected_service and not final_service_name.strip():
        st.error("कृपया कामाचे नाव टाईप करा!")
    else:
        st.session_state.items_list.append((final_service_name, final_amount))
        st.success(f"जोडले: {final_service_name} -> ₹ {final_amount}/-")

# 📋 सध्या जोडलेल्या कामांची समरी
if st.session_state.items_list:
    st.write("### 📋 बिलात जोडलेली कामे:")
    total_bill = 0.0
    for idx, item in enumerate(st.session_state.items_list, start=1):
        st.write(f"**{idx}. {item[0]}** -> ₹ {item[1]:.2f}/-")
        total_bill += item[1]
        
    st.markdown(f"#### 💰 एकूण देय रक्कम: **₹ {total_bill}/-**")
    
    if st.button("❌ Clear List (यादी साफ करा)", use_container_width=True):
        st.session_state.items_list = []
        st.rerun()

    st.write("---")

    # 🖨️ फायनल बिल जनरेशन बटण
    if st.button("🖨️ Generate Full Bill & WhatsApp Preview", use_container_width=True):
        if not cust_name.strip():
            st.error("कृपया ग्राहकाचे नाव आधी भरा!")
        else:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            wa_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            all_services_text = ", ".join(item[0] for item in st.session_state.items_list)
            
            # गुगल शीटला सेव्ह करणे
            sheet_success, bill_no = get_next_bill_number_and_save([current_date, cust_name, cust_phone, all_services_text, total_bill])
            
            # HTML टेबल रोज तयार करणे
            table_rows_html = ""
            for idx, item in enumerate(st.session_state.items_list, start=1):
                table_rows_html += f"""
                <tr>
                    <td style="text-align: center; border-bottom: 1px solid #ddd; padding: 10px;">{idx}</td>
                    <td style="text-align: left; border-bottom: 1px solid #ddd; padding: 10px;"><b>{item[0]}</b></td>
                    <td style="text-align: right; border-bottom: 1px solid #ddd; padding: 10px; font-weight: bold; white-space: nowrap;">₹ {item[1]:.2f}/-</td>
                </tr>
                """
            
            # 🔥 मूळ कडक A5 डबल-पेज HTML बिल टेम्पलेट (जाहिरातीसह)
            html_bill = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; color: #333; background-color: #f0f2f5; }}
        .page-front {{ width: 148mm; min-height: 210mm; padding: 10mm; box-sizing: border-box; background-color: #ffffff; margin: 10px auto; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .page-back {{ width: 148mm; min-height: 210mm; padding: 10mm; box-sizing: border-box; background-color: #ffffff; margin: 20px auto; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); page-break-before: always; }}
        
        .bill-box {{ border: 2.5px solid #0056b3; padding: 15px; border-radius: 8px; background-color: #ffffff; height: 100%; box-sizing: border-box; }}
        .header-table {{ width: 100%; border-bottom: 3.5px solid #0056b3; padding-bottom: 6px; }}
        .shop-name {{ color: #0056b3; font-size: 24px; font-weight: bold; margin: 0; }}
        .address {{ font-size: 11px; color: #555; margin: 2px 0; }}
        .contacts {{ font-size: 11px; font-weight: bold; color: #111; }}
        .bill-details {{ width: 100%; margin-top: 10px; font-size: 13px; border-collapse: collapse; }}
        .items-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; table-layout: fixed; }}
        .items-table th {{ background-color: #0056b3; color: white; padding: 8px; font-weight: bold; }}
        .bottom-container {{ width: 100%; margin-top: 15px; border-collapse: collapse; }}
        .total-section {{ font-size: 16px; font-weight: bold; color: #0056b3; text-align: left; }}
        .stamp-box {{ border: 3px dashed #cc0000; color: #cc0000; font-size: 14px; font-weight: bold; text-align: center; padding: 4px 10px; width: 130px; border-radius: 5px; transform: rotate(-4deg); background-color: #fff5f5; font-weight: 900; line-height: 1.2; margin-left: auto; }}
        .services-box {{ border: 1.5px solid #0056b3; border-radius: 6px; background-color: #f4f8ff; padding: 10px; margin-top: 15px; }}
        .services-title {{ font-size: 12px; font-weight: bold; color: #0056b3; margin: 0 0 6px 0; border-bottom: 1.5px solid #0056b3; padding-bottom: 3px; text-align: center; }}
        .services-list {{ width: 100%; font-size: 11px; color: #111; font-weight: bold; border-collapse: collapse; }}
        .services-list td {{ padding: 3px 5px; width: 50%; }}
        .footer {{ text-align: center; font-size: 11px; color: #555; border-top: 1px dashed #ccc; padding-top: 6px; font-weight: bold; margin-top: 15px; }}
        
        .adv-box {{ border: 4px double #ff6600; padding: 15px; border-radius: 12px; text-align: center; height: 100%; box-sizing: border-box; }}
        .adv-title {{ font-size: 28px; font-weight: bold; color: #ff6600; margin: 0; }}
        .adv-subtitle {{ font-size: 14px; color: #555; margin: 3px 0 15px 0; font-weight: bold; border-bottom: 2.5px solid #ff6600; padding-bottom: 8px; letter-spacing: 0.5px; }}
        .adv-heading {{ font-size: 16px; font-weight: bold; color: #111; margin: 10px 0 6px 0; background: #ffe6d5; padding: 6px; border-radius: 5px; text-align: center; border-left: 5px solid #ff6600; }}
        .adv-table {{ width: 100%; font-size: 13px; text-align: left; border-collapse: collapse; font-weight: bold; margin-bottom: 2px; }}
        .adv-table td {{ padding: 6px 8px; color: #222; width: 50%; }}
        .adv-features {{ display: flex; justify-content: space-around; background: #fdfaf6; padding: 8px; border-radius: 6px; border: 1px dashed #ff6600; margin-top: 8px; }}
        .feature-item {{ font-size: 12px; font-weight: bold; color: #555; }}
        .adv-footer {{ font-size: 14px; font-weight: bold; color: #ff6600; background: #fff0e6; padding: 10px; border-radius: 6px; margin-top: 15px; line-height: 1.5; border: 1px solid #ff6600; }}

        @media print {{
            body {{ background-color: #fff; padding: 0; }}
            .page-front, .page-back {{ margin: 0; box-shadow: none; border-radius: 0; width: 100%; }}
        }}
    </style>
</head>
<body>
    <!-- १. बिलाची पुढची बाजू -->
    <div class="page-front">
        <div class="bill-box">
            <table class="header-table">
                <tr>
                    <td>
                        <div class="shop-name">BALAJI CYBER POINT</div>
                        <div class="address">Mangaon, Raigad, Maharashtra</div>
                        <div class="contacts">📞 Call: 8007365051 | 💬 WA: 8806789013</div>
                    </td>
                    <td style="text-align: right; vertical-align: top;">
                        <h2 style="margin: 0; color: #0056b3; font-size: 18px;">INVOICE</h2>
                    </td>
                </tr>
            </table>
            <table class="bill-details">
                <tr><td><b>बिल क्र:</b> {bill_no}</td><td style="text-align: right;"><b>तारीख/वेळ:</b> {current_date}</td></tr>
                <tr><td><b>ग्राहक नाव:</b> {cust_name}</td><td style="text-align: right;"><b>मोबाईल नं:</b> {cust_phone if cust_phone else '-'}</td></tr>
            </table>
            <table class="items-table">
                <thead>
                    <tr>
                        <th style="width: 12%; text-align: center;">क्र.</th>
                        <th style="width: 63%; text-align: left;">कामाचा तपशील / सेवा प्रकार</th>
                        <th style="width: 25%; text-align: right;">रक्कम</th>
                    </tr>
                </thead>
                <tbody>{table_rows_html}</tbody>
            </table>
            
            <table class="bottom-container">
                <tr>
                    <td class="total-section" style="vertical-align: middle;">एकूण देय रक्कम: ₹ {total_bill:.2f}/-</td>
                    <td style="text-align: right; width: 140px;">
                        <div class="stamp-box">PAID<br><span style="font-size:8px; font-weight:bold;">BALAJI CYBER POINT</span></div>
                    </td>
                </tr>
            </table>
            <div class="services-box">
                <div class="services-title">⚡ आमच्याकडील प्रमुख सेवा Center ⚡</div>
                <table class="services-list">
                    <tr><td>• On-line सर्व सरकारी फॉर्म</td><td>• नवीन पॅन कार्ड / दुरुस्ती</td></tr>
                    <tr><td>• मतदार कार्ड (Voter ID) कामे</td><td>• लाईट बिल भरणे केंद्र</td></tr>
                    <tr><td>• पासपोर्ट व ड्रायव्हिंग लायसन्स</td><td>• गॅझेट गॅरंटी (नाव बदलणे)</td></tr>
                    <tr><td>• डोमासिएल / उत्पन्न दाखला</td><td>• कलर PRINTING व लॅमिनेशन</td></tr>
                </table>
            </div>
            <div class="footer">🙏 धन्यवाद! पुन्हा भेट द्या! 🙏</div>
        </div>
    </div>
    
    <!-- २. बिलाची मागची बाजू (जाहिरात) -->
    <div class="page-back">
        <div class="adv-box">
            <div class="adv-title">BALAJI CYBER POINT</div>
            <div class="adv-subtitle">डिजिटल क्रांती आणि शासकीय सेवा केंद्र</div>
            <div class="adv-heading">🎯 सर्व ऑनलाईन सेवा एकाच छताखाली!</div>
            <table class="adv-table">
                <tr><td>✅ महा-ई-सेवा केंद्र कामे</td><td>✅ नवीन पॅन कार्ड / दुरुस्ती</td></tr>
                <tr><td>✅ मतदार कार्ड आणि आधार लिंक</td><td>✅ लाईट बिल पेमेंट सुविधा Center</td></tr>
                <tr><td>✅ गॅझेट गॅरंटी (नाव/धर्म बदलणे)</td><td>✅ पासपोर्ट आणि लायसन्स अर्ज</td></tr>
                <tr><td>✅ डोमासिएल, उत्पन्न व जातीचे दाखले</td><td>✅ सर्व प्रकारचे ऑनलाईन जॉब फॉर्म</td></tr>
            </table>
            <div class="adv-heading">🖨️ स्पेशल प्रिंटिंग आणि बुकिंग सेवा</div>
            <table class="adv-table">
                <tr><td>🚀 A3 हाय-क्वालिटी प्रिंटिंग</td><td>🔥 A3 आणि A4 कडक लॅमिनेशन</td></tr>
                <tr><td>✈️ फ्लाईट बुकिंग (Flight Tickets)</td><td>📸 पासपोर्ट साईझ फोटो</td></tr>
                <tr><td>🗂️  कलर झेरॉक्स आणि स्कॅनिंग</td><td>👮 पोलीस व्हेरिफिकेशन (Police Verification)</td></tr>
            </table>
            <div class="adv-features">
                <div class="feature-item">⚡ अचूक काम</div>
                <div class="feature-item">🚀 जलद सेवा</div>
                <div class="feature-item">💎 वाजवी दर</div>
            </div>
            <div class="adv-footer">
                📍 पत्ता: बालाजी कॉम्प्लेक्स, माणगाव, रायगड, Maharashtra<br>
                📞 संपर्क: 8007365051 | 💬 व्हॉट्सॲप: 8806789013
            </div>
        </div>
    </div>
</body>
</html>
"""
            
            # स्क्रीनवर व्हॉट्सॲप मेसेज प्रिव्ह्यू दाखवणे
            st.markdown("### 📸 व्हॉट्सॲप प्रिव्ह्यू (स्क्रीनशॉट काढा):")
            wa_bubble = f"""
            <b>🧾 BALAJI CYBER POINT 🧾</b>
            <i>डिजिटल शासकीय सेवा केंद्र, माणगाव</i>
            ───────────────────────
            प्रिय <b>{cust_name}</b>,
            आपले बिल यशस्वीरित्या तयार झाले आहे:
            
            📄 <b>बिल नंबर:</b> `{bill_no}`
            📅 <b>तारीख/वेळ:</b> {wa_date}
            🛠️ <b>कामाचा तपशील:</b> {all_services_text}
            💰 <b>एकूण रक्कम:</b> ₹ <b>{total_bill:.2f}/-</b>
            ───────────────────────
            👍 <b>STATUS: PAID</b>
            🙏 <b>धन्यवाद! पुन्हा भेट द्या!</b>
            """
            st.info(wa_bubble)
            
            # 🔥 संपूर्ण कडक डबल-पेज बिल डाऊनलोड बटण
            st.download_button(
                label="📥 संपूर्ण कडक A5 बिल फाईल डाऊनलोड करा",
                data=html_bill,
                file_name=f"Full_Bill_{bill_no}.html",
                mime="text/html"
            )
            
            if sheet_success:
                st.success("✅ गुगल शीटमध्ये हिशोब सुरक्षित सेव्ह झाला आहे!")
