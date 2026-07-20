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
# 👥 साईडबार युझर सिस्टीम
# ==========================================
if "user_role" not in st.session_state:
    st.session_state.user_role = "Manager (Pankajji)"

st.sidebar.markdown("### सिस्टीम युझर")
current_user = st.sidebar.radio(
    "युझर निवडा:",
    ("Manager (Pankajji)", "Staff / Partner"),
    index=0 if st.session_state.user_role == "Manager (Pankajji)" else 1
)
st.session_state.user_role = current_user

st.sidebar.write("---")
st.sidebar.markdown(f"**सध्याचे युझर:** `{st.session_state.user_role}`")

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
# 🖥️ मुख्य इंटरफेस
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0F172A; font-weight: 800;'>श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #2563EB; font-weight: 600;'>आयुष्मान भारत - 4x6 लेआउट ऑटो ट्रिम कंव्हर्टर</h4>", unsafe_allow_html=True)
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
                    # ४०० DPI हाय-डेफिनिशन रेंडरिंग
                    pix = page.get_pixmap(dpi=400)
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    width, height = img.size
                    
                    # १. मूळ पीडीएफ मधून रफ क्रॉप
                    rough_front = img.crop((int(width * 0.03), int(height * 0.12), int(width * 0.50), int(height * 0.88)))
                    rough_back = img.crop((int(width * 0.50), int(height * 0.12), int(width * 0.97), int(height * 0.88)))
                    
                    # २. ऑटो-ट्रिमिंग
                    img_front = auto_crop_card(rough_front)
                    img_back = auto_crop_card(rough_back)
                    
                    # ३. मूळ परफेक्ट साईझ लॉक (1200 x 765 px)
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    card_w, card_h = 1200, 765
                    
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # डाव्या-उजव्या कडेला ० मार्जिनवर तंतोतंत पेस्ट (Edge-to-Edge)
                    final_canvas.paste(img_front, (0, 80))
                    final_canvas.paste(img_back, (0, 950))
                    
                    # काठोकाठ ५ पिक्सेलची काळी बॉर्डर
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([0, 80, PAPER_WIDTH - 1, 80 + card_h], outline="black", width=5)
                    draw.rectangle([0, 950, PAPER_WIDTH - 1, 950 + card_h], outline="black", width=5)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(400, 400))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    # प्रिव्ह्यू आणि डाऊनलोड
                    st.image(final_canvas, caption="4x6 Print Preview", width=650)
                    st.write("")
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="4x6 PNG इमेज डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_4x6_Layout_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"त्रुटी: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #94A3B8;'>श्री बालाजी सायबर पॉईंट, माणगाव, रायगड</p>", unsafe_allow_html=True)
