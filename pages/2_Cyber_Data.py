import streamlit as st
from urllib.parse import quote
import os
from datetime import datetime

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - सायबर डेटा", page_icon="📱", layout="centered")

st.markdown("<h2 style='text-align: center; color: #ff6600;'>📱 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>ग्राहक फॉर्म डेटा आणि कडक पावती मेकर</h4>", unsafe_allow_html=True)
st.write("---")

# 👤 ग्राहक आणि फॉर्मची माहिती इनपुट बॉक्स
col1, col2 = st.columns(2)
with col1:
    c_name = st.text_input("Customer Name (ग्राहकाचे नाव):")
    f_purpose = st.text_input("Form Name / Purpose (कामाचा प्रकार):")
    f_id = st.text_input("Login / User ID (युझर आयडी):")
with col2:
    c_phone = st.text_input("Phone Number (१० अंकी मोबाईल):")
    f_site = st.text_input("Website Used (वापरलेली वेबसाईट):")
    f_pass = st.text_input("Password (पासवर्ड):")

st.write("---")

# डेटा भरल्यावरच पावती दाखवणे आणि जनरेट करणे
if c_name or f_purpose or f_id:
    
    # 🎯 अचूक चालू तारीख आणि वेळ सिस्टीम
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 📝 १. व्हॉट्सॲप आणि साध्या टेक्स्टसाठी फॉरमॅट
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

    # 🔥 २. स्क्रीनशॉटसारखे कडक पिवळे HTML बिल डिझाईन
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

    # 📥 सुधारलेले डाऊनलोड बटण (HTML फाईल डाऊनलोड होईल)
    st.download_button(
        label="📄 Save & Download Color Receipt (कलर पावती डाऊनलोड करा)",
        data=html_receipt,
        file_name=f"Color_Receipt_{c_name.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True
    )

    # 📱 व्हॉट्सॲपवर पाठवण्याची सिस्टीम
    if c_phone:
        encoded_message = quote(receipt_text)
        whatsapp_url = f"https://api.whatsapp.com/send?phone=91{c_phone}&text={encoded_message}"
        
        st.markdown(
            f'<a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">'
            f'<div style="text-align: center; background-color: #25D366; color: white; '
            f'padding: 10px; border-radius: 5px; font-weight: bold; font-size: 16px;">'
            f'📱 Send via WhatsApp (ग्राहकाला व्हॉट्सॲपवर पाठवा)</div></a>',
            unsafe_allow_html=True
        )

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
