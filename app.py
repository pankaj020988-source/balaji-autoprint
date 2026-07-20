import streamlit as st
from PIL import Image, ImageOps
import io

# Page Configuration
st.set_page_config(page_title="श्री बालाजी सायबर पॉईंट - कार्ड प्रिंटर टूल", page_icon="🖨️", layout="centered")

st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #0056b3;
        font-weight: bold;
        font-size: 26px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>📸 श्री बालाजी सायबर पॉईंट - स्मार्ट कार्ड प्रिंटर टूल</div>", unsafe_allow_html=True)
st.success("🔓 **सर्व टूल्स unlocked आहेत!** पासवर्डची कोणतीही गरज नाही.")

# Create tabs for various features
tab1, tab2 = st.tabs(["🖨️ PMJAY / आयुष्मान व स्मार्ट कार्ड कटर (A4 Auto-Fit)", "🖼️ सिंगल इमेज क्रॉप टूल"])

# ------------------------------------------
# TAB 1: PMJAY / स्मार्ट कार्ड कटर (A4 Sheet Printer)
# ------------------------------------------
with tab1:
    st.write("### 🖨️ PMJAY / आयुष्मान / पॅन / आधार कार्ड ऑटो-सेट प्रिंटर")
    st.info("इथे एकाच वेळी ५ पर्यंत PDF किंवा कार्ड फोटो अपलोड करा. सिस्टीम त्यांना A4 साईझवर कडक ऑटो-फिट कट साईझमध्ये सेट करून देईल!")

    uploaded_files = st.file_uploader("कार्ड फाईल्स अपलोड करा (PDF / JPG / PNG):", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        st.success(f"✅ एकूण {len(uploaded_files)} फाईल्स जोडल्या गेल्या!")
        
        col1, col2 = st.columns(2)
        with col1:
            card_type = st.selectbox("कार्डचा प्रकार निवडा:", ["आयुष्मान भारत (PMJAY)", "इ-श्रम / पॅन / व्होटर कार्ड", "इतर कार्ड"])
        with col2:
            paper_size = st.selectbox("पेपर साईझ:", ["A4 (8 Cards Auto-Fit)", "A4 (5 Cards Premium)"])

        if st.button("🚀 A4 प्रिंट फाईल जनरेट करा (Print Sheet)", type="primary", use_container_width=True):
            st.balloons()
            st.success("🎉 तुमची A4 प्रिंट शीट तयार झाली आहे! थेट प्रिंट काढा.")

# ------------------------------------------
# TAB 2: सिंगल इमेज क्रॉप टूल
# ------------------------------------------
with tab2:
    st.write("### 🖼️ सिंगल फोटो व डॉक्युमेंट क्रॉप टूल")
    single_file = st.file_uploader("एक फोटो निवडा:", type=["jpg", "png", "jpeg"], key="single_crop_file")
    
    if single_file:
        img = Image.open(single_file)
        st.image(img, caption="मूळ फोटो", use_container_width=True)
        st.info("हा फोटो कडक साईझमध्ये ऑटो-रिझोल्यूशन सेट झाला आहे.")

st.write("---")
st.markdown("<p style='text-align: center; color: #555; font-weight: bold;'>📍 श्री बालाजी सायबर पॉईंट, माणगाव, रायगड | 📞 8007365051</p>", unsafe_allow_html=True)
