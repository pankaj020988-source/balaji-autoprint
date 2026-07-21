import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageDraw
import io
import time

# ==========================================
# 🌐 लेआउट कॉन्फिगरेशन
# ==========================================
st.set_page_config(page_title="बालाजी सायबर पॉईंट - होम", page_icon="🖥️", layout="wide")

# ==========================================
# ✂️ ऑटो-ट्रिमिंग फंक्शन
# ==========================================
def auto_crop_card(card_img):
    """कार्डच्या आजूबाजूची अतिरिक्त पांढरी जागा स्वयंचलितपणे कापून टाकते"""
    gray = card_img.convert("L")
    inverted = ImageOps.invert(gray)
    bbox = inverted.getbbox()
    if bbox:
        return card_img.crop(bbox)
    return card_img

# ==========================================
# 🖥️ मुख्य इंटरफेस (श्री शब्द काढलेला)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0F172A; font-weight: 800;'>बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #2563EB; font-weight: 600;'>आयुष्मान भारत - 4x6 पॉकेट कार्ड कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("आयुष्मान भारत PDF फाईल अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("4x6 प्रिंटींग लेआउट जनरेट करा", type="primary", use_container_width=True):
        with st.spinner("प्रक्रिया सुरू आहे..."):
            try:
                st.cache_data.clear()
                
                pdf_bytes = uploaded_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                
                if len(doc) < 1:
                    st.error("मजकूर सापडला नाही! कृपया योग्य फाईल अपलोड करा.")
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
                    card_w, card_h = 1020, 640
                    
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    front_bordered = ImageOps.expand(img_front, border=5, fill='black')
                    back_bordered = ImageOps.expand(img_back, border=5, fill='black')
                    
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    paste_x = (PAPER_WIDTH - front_bordered.width) // 2
                    
                    final_canvas.paste(front_bordered, (paste_x, 180))
                    final_canvas.paste(back_bordered, (paste_x, 950))
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(400, 400))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    st.image(final_canvas, caption="4x6 Print Preview (Standard Pocket Size)", width=650)
                    st.write("")
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="4x6 PNG इमेज डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_Pocket_4x6_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"त्रुटी: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #94A3B8;'>बालाजी सायबर पॉईंट, माणगाव, रायगड</p>", unsafe_allow_html=True)
