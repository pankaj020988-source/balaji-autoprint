import streamlit as st
from urllib.parse import quote
import os
from datetime import datetime

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - सायबर डेटा व रिमाइंडर", page_icon="📱", layout="centered")

# मुख्य टॅब्स तयार करणे (डेटा मेकर आणि रिमाइंडर दोन्ही एकत्र)
tab1, tab2 = st.tabs(["🔐 ग्राहक पासवर्ड डेटा पावती", "🚨 ग्राहक रिमाइंडर टूल (Reminder)"])

# ==========================================
# 🔐 टॅब १: ग्राहक फॉर्म डेटा आणि पावती मेकर
# ==========================================
with tab1:
    st.markdown("<h3 style='text-align: center; color: #ff6600;'>🔐 श्री बालाजी सायबर पॉईंट - डेटा पावती मेकर</h3>", unsafe_allow_html=True)
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        c_name = st.text_input("Customer Name (ग्राहकाचे नाव):", key="cyber_name")
        f_purpose = st.text_input("Form Name / Purpose (कामाचा प्रकार):", key="cyber_purpose")
        f_id = st.text_input("Login / User ID (युझर आयडी):", key="cyber_id")
    with col2:
        c_phone = st.text_input("Phone Number (१० अंकी मोबाईल):", key="cyber_phone")
        f_site = st.text_input("Website Used (वापरलेली वेबसाईट):", key="cyber_site")
        f_pass = st.text_input("Password (पासवर्ड):", key="cyber_pass")

    st.write("---")

    if c_name or f_purpose or f_id:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        receipt_text = f"""*************************************
      BALAJI CYBER POINT
*************************************
Customer: {c_name}
Phone: {c_phone if c_phone else '-'}
-------------------------------------
Form Details:
Purpose: {f_purpose}
Website: {f_site}

Login ID: {f_id}
Password: {f_pass}
-------------------------------------
Thank you for visiting!
*************************************"""

        html_receipt = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f2f5; display: flex; justify-content: center; }}
        .receipt-card {{ width: 450px; background: white; border: 3px solid #ffb703; border-radius: 10px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); box-sizing: border-box; }}
        .header {{ text-align: center; border-bottom: 2px solid #ffb703; padding-bottom: 10px; margin-bottom: 15px; }}
        .shop-name {{ color: #fb8500; font-size: 24px; font-weight: bold; margin: 0; letter-spacing: 0.5px; }}
        .info-row {{ display: flex; margin: 8px 0; font-size: 14px; line-height: 1.6; }}
        .info-label {{ width: 110px; font-weight: bold; color: #555; }}
        .info-value {{ flex: 1; color: #111; font-weight: 600; }}
        .secret-box {{ background-color: #fdf0d5; border: 1px dashed #ffb703; border-radius: 6px; padding: 12px; margin-top: 15px; }}
        .secret-row {{ display: flex; margin: 6px 0; font-size: 14px; }}
        .secret-label {{ width: 90px; font-weight: bold; color: #fb8500; }}
        .secret-value {{ flex: 1; color: #000; font-weight: bold; word-break: break-all; }}
        .footer {{ text-align: center; font-size: 13px; font-weight: bold; color: #fb8500; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style>
</head>
<body>
    <div class="receipt-card">
        <div class="header">
            <div class="shop-name">BALAJI CYBER POINT</div>
            <div style="font-size: 11px; color: #667781; margin-top: 2px;">Mangaon, Raigad, Maharashtra</div>
            <div style="font-size: 11px; font-weight: bold; color: #333; margin-top: 2px;">📞 8007365051 | 💬 WA: 8806789013</div>
        </div>
        <div class="info-row"><div class="info-label">तारीख/वेळ:</div><div class="info-value">{current_time}</div></div>
        <div class="info-row"><div class="info-label">ग्राहक नाव:</div><div class="info-value">{c_name}</div></div>
        <div class="info-row"><div class="info-label">मोबाईल नं:</div><div class="info-value">{c_phone if c_phone else '-'}</div></div>
        <div class="info-row"><div class="info-label">काम/फॉर्म:</div><div class="info-value">{f_purpose}</div></div>
        <div class="secret-box">
            <div class="secret-row"><div class="secret-label">🌐 वेबसाईट:</div><div class="secret-value"><a href="{f_site}" target="_blank" style="color: #0078D7;">{f_site if f_site else '-'}</a></div></div>
            <div class="secret-row"><div class="secret-label">👤 User ID:</div><div class="secret-value" style="background:#fff; padding:2px 5px; border-radius:4px; border:1px solid #eee;">{f_id}</div></div>
            <div class="secret-row"><div class="secret-label">🔑 पासवर्ड:</div><div class="secret-value" style="background:#fff; padding:2px 5px; border-radius:4px; border:1px solid #eee;">{f_pass}</div></div>
        </div>
        <div class="footer">Thank You! Visit Again!</div>
    </div>
</body>
</html>
"""
        st.markdown("### 📄 पावती प्रिव्ह्यू:")
        st.code(receipt_text, language="text")

        st.download_button(
            label="📄 Save & Download Color Receipt (कलर पावती डाऊनलोड करा)",
            data=html_receipt,
            file_name=f"Color_Receipt_{c_name.replace(' ', '_')}.html",
            mime="text/html",
            use_container_width=True
        )

        if c_phone:
            encoded_message = quote(receipt_text)
            whatsapp_url = f"https://api.whatsapp.com/send?phone=91{c_phone}&text={encoded_message}"
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><div style="text-align: center; background-color: #25D366; color: white; padding: 10px; border-radius: 5px; font-weight: bold; font-size: 16px;">📱 Send via WhatsApp (ग्राहकाला व्हॉट्सॲपवर पाठवा)</div></a>', unsafe_allow_html=True)

# ==========================================
# 🚨 टॅब २: ग्राहक रिमाइंडर टूल (Reminder)
# ==========================================
with tab2:
    st.markdown("<h3 style='text-align: center; color: #d32f2f;'>🚨 श्री बालाजी सायबर पॉईंट - ग्राहक रिमाइंडर टूल</h3>", unsafe_allow_html=True)
    st.write("---")

    r_name = st.text_input("Customer Name (ग्राहकाचे नाव):", value="Customer", key="rem_name")
    r_phone = st.text_input("Phone Number (१० अंकी मोबाईल नंबर):", key="rem_phone")
    
    reminder_options = [
        "Admit Card Download",
        "Pending Payment",
        "Form Correction Window",
        "Exam Date",
        "Result Declaration",
        "Other..."
    ]
    r_type = st.selectbox("What is the Reminder For? (रिमाइंडर कशासाठी आहे?)", reminder_options)
    
    r_date = st.date_input("Important Date (महत्त्वाची तारीख):")
    formatted_r_date = r_date.strftime('%d-%m-%Y')
    
    r_notes = st.text_area("Extra Details / Form Name (इतर माहिती / फॉर्मचे नाव):", placeholder="उदा. SSC CGL Tier 1 किंवा ५० रुपये देणे बाकी...")

    st.write("---")

    # रिमाइंडर टेक्स्ट तयार करणे
    rem_notes_text = r_notes if r_notes.strip() else "None"
    
    whatsapp_msg = f"""*BALAJI CYBER POINT - REMINDER*

Hello {r_name},
This is a reminder regarding your *{r_type}*.

*Important Date:* {formatted_r_date}
"""
    if rem_notes_text != "None":
        whatsapp_msg += f"*Details:* {rem_notes_text}\n"
        
    whatsapp_msg += f"\nPlease visit us if you need assistance!\nThank you."

    # प्रिंटसाठी कडक स्लिप डिझाईन (HTML)
    html_reminder_slip = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; display: flex; justify-content: center; }}
        .reminder-box {{ width: 400px; padding: 20px; border: 2.5px dashed #333; background: #fff; border-radius: 8px; box-sizing: border-box; }}
        h2, h3 {{ text-align: center; margin: 5px 0; }}
        p {{ font-size: 14px; margin: 10px 0; line-height: 1.5; }}
        hr {{ border: 0; border-top: 1px dashed #ccc; }}
    </style>
</head>
<body>
    <div class="reminder-box">
        <h2>BALAJI CYBER POINT</h2>
        <h3 style="color: #d32f2f;">*** IMPORTANT REMINDER ***</h3>
        <hr>
        <p><strong>Customer:</strong> {r_name}</p>
        <p><strong>Regarding:</strong> {r_type}</p>
        <p><strong>Date to Remember:</strong> {formatted_r_date}</p>
        <hr>
        <p><strong>Details:</strong> {rem_notes_text}</p>
        <hr>
        <p style="text-align: center; font-size: 12px; font-weight: bold;">
            Please keep this slip safe.<br>
            Thank you for choosing Balaji Cyber Point!
        </p>
    </div>
</body>
</html>
"""

    st.markdown("### 📢 रिमाइंडर प्रिव्ह्यू:")
    st.code(whatsapp_msg, language="text")

    # १. व्हॉट्सॲप बटन
    if r_phone:
        encoded_rem = quote(whatsapp_msg)
        rem_wa_url = f"https://api.whatsapp.com/send?phone=91{r_phone}&text={encoded_rem}"
        st.markdown(f'<a href="{rem_wa_url}" target="_blank"><div style="text-align: center; background-color: #25D366; color: white; padding: 12px; border-radius: 5px; font-weight: bold; font-size: 16px; margin-bottom: 10px;">📱 Send WhatsApp Reminder</div></a>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ व्हॉट्सॲप रिमाइंडर पाठवण्यासाठी आधी मोबाईल नंबर भरा.")

    # २. प्रिंट स्लिप बटण
    st.download_button(
        label="🖨️ Download & Print Reminder Slip",
        data=html_reminder_slip,
        file_name=f"Reminder_{r_name.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True
    )

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
