import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageDraw
import io
import time

# ==========================================
# 🌐 १. पेज कॉन्फिगरेशन
# ==========================================
st.set_page_config(
    page_title="श्री बालाजी सायबर पॉईंट - डिजिटल पोर्टल्स", 
    page_icon="📷", 
    layout="wide"
)

# CSS डिझाईन
st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
        }
        .main-header {
            background: linear-gradient(135deg, #002f6c 0%, #0056b3 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            border: 2px solid #d4af37;
            margin-bottom: 20px;
        }
        .ad-box {
            background-color: #f8faff;
            border: 2px solid #0056b3;
            border-radius: 10px;
            padding: 20px;
            margin-top: 15px;
        }
        .ad-title {
            color: #002f6c;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 📢 मुख्य हेडर
st.markdown("""
<div class="main-header">
    <h1 style="color: #e5be3b; margin: 0; font-size: 32px;">📷 श्री बालाजी सायबर पॉईंट - डिजिटल पोर्टल्स</h1>
</div>
""", unsafe_allow_html=True)

# ✂️ ऑटो-ट्रिमिंग फंक्शन (पांढरा भाग कट करण्यासाठी)
def auto_crop_card(card_img):
    gray = card_img.convert("L")
    inverted = ImageOps.invert(gray)
    bbox = inverted.getbbox()
    if bbox:
        return card_img.crop(bbox)
    return card_img

# ==========================================
# 🏠 २. मूळ टॅब सिस्टीम (होम पेज + सायबर टूल्स)
# ==========================================
main_tab1, main_tab2 = st.tabs([
    "🏠 होम पेज (जाहिरात व सुविधा)", 
    "🔐 सायबर टूल्स पोर्टल (Locked)"
])

# ------------------------------------------
# टॅब १: होम पेज (जाहिरात व माहिती)
# ------------------------------------------
with main_tab1:
    st.markdown("""
    <div style="background-color: #004085; color: white; padding: 25px; border-radius: 8px; text-align: center; margin-bottom: 20px;">
        <h2 style="color: #ffc107; margin: 0;">बालाजी सायबर पॉईंट (माणगाव)</h2>
        <h4 style="margin-top: 5px; font-weight: 400;">तुमचे डिजिटल आणि ट्रॅव्हल सोल्यूशन पार्टनर!</h4>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 8px; border-left: 5px solid #0056b3;">
            <h4 style="color: #0056b3; margin-top: 0;">📢 नवीन सरकारी नोकर भरती व जाहिराती</h4>
            <p><b>📌 महाभरती २०२६:</b> विविध सरकारी विभागांमध्ये नवीन जागा उपलब्ध झाल्या आहेत. ऑनलाईन अर्ज भरण्यासाठी आजच दुकानात आवश्यक कागदपत्रांसह भेट द्या.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div style="background-color: #fff9e6; padding: 15px; border-radius: 8px; border-left: 5px solid #ffc107;">
            <h4 style="color: #856404; margin-top: 0;">📌 परीक्षा प्रवेशपत्र (Admit Card)</h4>
            <p>चालू महिन्यातील स्पर्धा परीक्षांचे हॉल तिकीट आणि विविध सरकारी परीक्षांचे प्रवेशपत्र डाऊनलोड करणे सुरू आहे.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 🛠️ आमच्याकडे उपलब्ध असलेल्या प्रमुख सुविधा:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("🖨️ **कार्ड प्रिंटिंग आणि स्कॅनर सेवा**")
        st.write("* आयुष्मान भारत कार्ड ४x६ ऑटो-फिट प्रिंटिंग")
        st.write("* स्मार्ट आयडी कार्ड प्रिंटर (पॅन कार्ड / व्होटर आयडी)")
        st.write("* A4 / A3 हाय-क्वालिटी कलर प्रिंटिंग आणि लॅमिनेशन")
    with col2:
        st.write("📝 **ऑनलाईन फॉर्म आणि ट्रॅव्हल बुकिंग**")
        st.write("* सर्व प्रकारच्या सरकारी व भरती परीक्षांचे ऑनलाईन अर्ज")
        st.write("* फ्लाईट, रेल्वे व बस तिकिट बुकिंग")
        st.write("* पासपोर्ट व ड्रायव्हिंग लायसन्स ऑनलाईन अर्ज")

# ------------------------------------------
# टॅब २: सायबर टूल्स पोर्टल (आयुष्मान भारत PDF कन्व्हर्टर)
# ------------------------------------------
with main_tab2:
    st.write("### 🖨️ आयुष्मान भारत सरकारी PDF ऑटो-फिट 4X6 प्रिंटर")
    uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"], key="ayushman_pdf_uploader")

    if uploaded_file is not None:
        if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
            with st.spinner("⏳ स्वयंचलित तंत्रज्ञानाद्वारे पांढरा भाग काढून लेआउट फिक्स होत आहे..."):
                try:
                    st.cache_data.clear()
                    pdf_bytes = uploaded_file.read()
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                    
                    if len(doc) < 1:
                        st.error("मजकूर सापडला नाही! कृपया खरी पीडीएफ अपलोड करा.")
                    else:
                        page = doc[0]
                        pix = page.get_pixmap(dpi=400)
                        img_data = pix.tobytes("png")
                        img = Image.open(io.BytesIO(img_data))
                        
                        width, height = img.size
                        rough_front = img.crop((int(width * 0.03), int(height * 0.12), int(width * 0.50), int(height * 0.88)))
                        rough_back = img.crop((int(width * 0.50), int(height * 0.12), int(width * 0.97), int(height * 0.88)))
                        
                        img_front = auto_crop_card(rough_front)
                        img_back = auto_crop_card(rough_back)
                        
                        PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                        card_w, card_h = 1200, 765
                        
                        img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                        img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                        
                        final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                        final_canvas.paste(img_front, (0, 80))
                        final_canvas.paste(img_back, (0, 950))
                        
                        draw = ImageDraw.Draw(final_canvas)
                        draw.rectangle([0, 80, PAPER_WIDTH - 1, 80 + card_h], outline="black", width=5)
                        draw.rectangle([0, 950, PAPER_WIDTH - 1, 950 + card_h], outline="black", width=5)
                        
                        img_byte_arr = io.BytesIO()
                        final_canvas.save(img_byte_arr, format='PNG', dpi=(400, 400))
                        img_byte_arr_raw = img_byte_arr.getvalue()
                        
                        st.success("✅ आयुष्मान कार्ड आता काठोकाठ ४x६ वर ऑटो-फिट झाले आहे!")
                        st.image(final_canvas, caption="४x६ कडक प्रिंट प्रिव्ह्यू", width=600)
                        
                        unique_time = int(time.time())
                        st.download_button(
                            label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                            data=img_byte_arr_raw,
                            file_name=f"Ayushman_AutoFit_HD_{unique_time}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; color: #555; font-weight: bold;'>📍 श्री बालाजी सायबर पॉईंट, माणगाव | 📞 संपर्क: 8007365051</p>", unsafe_allow_html=True)
