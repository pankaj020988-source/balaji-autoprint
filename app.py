import streamlit as st

# ==========================================
# 🌐 मुख्य पेज कॉन्फिगरेशन
# ==========================================
st.set_page_config(
    page_title="बालाजी सायबर पॉईंट - डिजिटल टूलकिट", 
    page_icon="📸", 
    layout="wide"
)

# 🎨 साईडबार आणि टॅब्सचे डिझाईन
st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
        }
        .tool-card {
            background-color: #f8faff;
            border: 2px solid #0056b3;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        .tool-card:hover {
            transform: translateY(-4px);
            box-shadow: 0px 8px 18px rgba(0,0,0,0.15);
            background-color: #ffffff;
        }
        .tool-title {
            color: #002f6c;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .tool-desc {
            color: #555555;
            font-size: 14px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# 📢 मुख्य header
st.markdown("""
<div style="background: linear-gradient(135deg, #002f6c 0%, #0056b3 100%); padding: 25px; border-radius: 12px; text-align: center; color: white; border: 2px solid #d4af37; margin-bottom: 25px;">
    <h1 style="color: #e5be3b; margin: 0; font-size: 36px;">📸 श्री बालाजी सायबर पॉईंट - मास्टर टूलकिट</h1>
    <p style="font-size: 16px; margin-top: 5px; opacity: 0.95;">सर्व टूल्स पासवर्ड लॉकशिवाय वापरासाठी मोकळे करण्यात आले आहेत.</p>
</div>
""", unsafe_allow_html=True)

st.success("🔓 **सर्व टूल्स अनलॉक आहेत!** डाव्या बाजूच्या मेन्यूमधून किंवा खालील बटनांवर क्लिक करून थेट टूल वापरा.")

st.write("")

# 🛠️ चारही टूल्सचे थेट प्रवेश कार्ड्स
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🧾 1. स्मार्ट बिल मेकर (Bill Manager)</div>
        <div class="tool-desc">ग्राहकांचे बिल तयार करा, A5 प्रिंट काढा आणि जुने हिशोब थेट शोधून री-प्रिंट करा.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/Bill_Manager.py", label="🚀 बिल मेकर उघडा", use_container_width=True)

    st.write("")
    
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">📊 2. सायबर डेटा आणि हिशोब (Cyber Data)</div>
        <div class="tool-desc">गुगल शीटमधील दैनिक जमा-खर्च, ग्राहकांची यादी आणि हिशोब तपासा.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/Cyber_Data.py", label="🚀 सायबर डेटा उघडा", use_container_width=True)

with col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🖼️ 3. इमेज टूल आणि फोटो क्रॉप (Image Tool)</div>
        <div class="tool-desc">आयुष्मान, पॅन कार्ड आणि पासपोर्ट फोटो एका क्लिकवर A4 शीटवर प्रिंट करण्यासाठी क्रॉप करा.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/Image_Tool.py", label="🚀 इमेज टूल उघडा", use_container_width=True)

    st.write("")

    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">⚙️ 4. सिस्टीम कंट्रोल (App / Settings)</div>
        <div class="tool-desc">मेन ॲपच्या इतर अंतर्गत सेटिंग्ज आणि कंट्रोल ऑप्शन्स.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("app.py", label="🚀 मुख्य ॲप रिफ्रेश करा", use_container_width=True)

st.write("---")
st.markdown("<p style='text-align: center; color: #777; font-weight: bold;'>📍 बालाजी सायबर पॉईंट, माणगाव, रायगड | संपर्क: 8007365051</p>", unsafe_allow_html=True)
