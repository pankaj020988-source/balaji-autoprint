import streamlit as st
from urllib.parse import quote
import os

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - सायबर डेटा", page_icon="📱", layout="centered")

st.markdown("<h2 style='text-align: center; color: #ff6600;'>📱 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>ग्राहक फॉर्म डेटा आणि पावती मेकर</h4>", unsafe_allow_html=True)
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
    f_pass = st.text_input("Password (पासवर्ड):", type="default")

st.write("---")

# डेटा भरल्यावरच पावती दाखवणे आणि जनरेट करणे
if c_name or f_purpose or f_id:
    # 📝 डिजिटल पावतीचे टेक्स्ट फॉरमॅट
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

    st.markdown("### 📄 पावती प्रिव्ह्यू:")
    # स्क्रीनवर पावती कडक ब्लॉक स्वरूपात दाखवणे
    st.code(receipt_text, language="text")

    # 📥 १. पावती फाईल (.txt) डाऊनलोड बटण
    st.download_button(
        label="📄 Save & Download Receipt (पावती डाऊनलोड करा)",
        data=receipt_text,
        file_name=f"Receipt_{c_name.replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

    # 📱 २. व्हॉट्सॲपवर पाठवण्याची सिस्टीम
    if c_phone:
        # टेक्स्ट मेसेज व्हॉट्सॲप लिंकसाठी एनकोड करणे
        encoded_message = quote(receipt_text)
        whatsapp_url = f"https://api.whatsapp.com/send?phone=91{c_phone}&text={encoded_message}"
        
        st.markdown(
            f'<a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">'
            f'<div style="text-align: center; background-color: #25D366; color: white; '
            f'padding: 10px; border-radius: 5px; font-weight: bold; font-size: 16px;">'
            f'📱 Send via WhatsApp (ग्राहकाला व्हॉट्सॲपवर पाठवा)</div></a>',
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ ग्राहकाला व्हॉट्सॲपवर पावती पाठवण्यासाठी कृपया मोबाईल नंबर भरा.")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
