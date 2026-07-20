import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageDraw
import io
import time

# ==========================================
# 🌐 १. पेज कॉन्फिगरेशन
# ==========================================
st.set_page_config(
    page_title="श्री बालाजी सायबर पॉईंट - इमेज व कार्ड टूल", 
    page_icon="📸", 
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
    </style>
""", unsafe_allow_html=True)

# 📢 मुख्य हेडर
st.markdown("""
<div class="main-header">
    <h2 style="color: #e5be3b; margin: 0;">📸 श्री बालाजी सायबर पॉईंट - मास्टर इमेज टूल</h2>
    <p style="margin-top: 5px; opacity: 0.95; font-size: 15px;">आयुष्मान भारत PDF, ४x६ फोटो आणि स्मार्ट कार्ड प्रिंटर सोल्यूशन्स</p>
</div>
""", unsafe_allow_html=True)

st.success("🔓 **सर्व सायबर टूल्स अनलॉक करण्यात आले आहेत!** कोणताही पासवर्ड न टाकता खालील टूल्स वापरा.")

# ✂️ ऑटो-ट्रिमिंग फंकशन (पांढरा भाग कट करण्यासाठी)
def auto_crop_card(card_img):
    gray = card_img.convert("L")
    inverted = ImageOps.invert(gray)
    bbox = inverted.getbbox()
    if bbox:
        return card_img.crop(bbox)
    return card_img

# ==========================================
# 🛠️ २. अनलॉक केलेले मास्टर टूल्स (जाहिरात टॅब काढला आहे)
# ==========================================
tool_tab1, tool_tab2 = st.tabs([
    "🖨️ आयुष्मान भारत PDF ते 4X6 कडक प्रिंट", 
    "🖼️ सिंगल फोटो / डॉक्युमेंट क्रॉप व प्रिंट"
])

# ------------------------------------------
# टॅब १: आयुष्मान भारत PDF ते 4X6 कन्व्हर्टर
# ------------------------------------------
with tool_tab1:
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

# ------------------------------------------
# टॅब २: सिंगल फोटो क्रॉप टूल
# ------------------------------------------
with tool_tab2:
    st.write("### 🖼️ फोटो / पॅन / व्होटर कार्ड क्रॉप टूल")
    single_file = st.file_uploader("एक फोटो अपलोड करा (JPG/PNG):", type=["jpg", "png", "jpeg"], key="single_img_uploader")
    
    if single_file:
        img = Image.open(single_file)
        st.image(img, caption="मूळ फोटो", use_container_width=True)
        st.success("फोटो रेडी आहे!")

st.write("---")
st.markdown("<p style='text-align: center; color: #555; font-weight: bold;'>📍 श्री बालाजी सायबर पॉईंट, माणगाव | 📞 संपर्क: 8007365051</p>", unsafe_allow_html=True)
