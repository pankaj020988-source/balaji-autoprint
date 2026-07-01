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
    "Color Printout /カラー प्रिंट", 
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
    
    # 🎯 दुरुस्त केलेला भाग (बटण रीसेट करण्यासाठी)
    if st.button("❌ Clear List (यादी साफ करा)", use_container_width=True):
        st.session_state.items_list = []
        st.rerun()

    st.write("---")

    # 🖨️ फायनल बिल जनरेशन बटण
    if st.button("🖨️ Generate Bill & WhatsApp Preview", use_container_width=True):
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
                    <td style="text-align: right; border-bottom: 1px solid #ddd; padding: 10px; font-weight: bold;">₹ {item[1]:.2f}/-</td>
                </tr>
                """
            
            # मूळ कडक HTML बिल टेम्पलेट
            html_bill = f"""<!DOCTYPE html>
            <html>
            <head><meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; color: #333; }}
                .bill-box {{ border: 2px solid #0056b3; padding: 15px; border-radius: 8px; max-width: 500px; margin: auto; }}
                .shop-name {{ color: #0056b3; font-size: 24px; font-weight: bold; text-align: center; }}
                .items-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                .items-table th {{ background-color: #0056b3; color: white; padding: 8px; }}
                .stamp-box {{ border: 3px dashed #cc0000; color: #cc0000; font-size: 14px; font-weight: bold; text-align: center; padding: 5px; width: 120px; margin-left: auto; transform: rotate(-4deg); }}
            </style>
            </head>
            <body>
            <div class="bill-box">
                <div class="shop-name">BALAJI CYBER POINT</div>
                <p style="text-align:center; font-size:12px;">माणगाव, रायगड | 📞 8007365051</p>
                <hr>
                <p><b>बिल नंबर:</b> {bill_no} <br> <b>तारीख:</b> {current_date}<br><b>ग्राहक:</b> {cust_name}</p>
                <table class="items-table">
                    <thead><tr><th>क्र.</th><th>सेवा प्रकार</th><th>रक्कम</th></tr></thead>
                    <tbody>{table_rows_html}</tbody>
                </table>
                <h3 style="color:#0056b3;">एकूण: ₹ {total_bill:.2f}/-</h3>
                <div class="stamp-box">PAID<br><span style="font-size:8px;">BALAJI CYBER POINT</span></div>
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
            
            # प्रिंटसाठी HTML फाईल डाऊनलोड करण्याचे बटण
            st.download_button(
                label="📥 बिलाची HTML प्रिंट फाईल डाऊनलोड करा",
                data=html_bill,
                file_name=f"Bill_{bill_no}.html",
                mime="text/html"
            )
            
            if sheet_success:
                st.success("✅ गुगल शीटमध्ये हिशोब सुरक्षित सेव्ह झाला आहे!")
