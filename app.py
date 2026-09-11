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
# 📐 बॉर्डरपेक्षा सुरक्षित अंतरावर कटिंग लाईन काढणारे फंक्शन
# ==========================================
def draw_safe_cutting_guides(draw_obj, box, offset=12, line_len=35, color="#666666", width=2):
    """
    कार्डच्या मुख्य बॉर्डरपेक्षा offset पिक्सेल बाहेर सेफ कटिंग गाईड्स आणि कॉर्नर मार्क्स काढते.
    """
    x0, y0, x1, y1 = box
    
    # बॉर्डरच्या बाहेर सेफ बॉक्स कॉर्डिनेट्स
    cx0 = x0 - offset
    cy0 = y0 - offset
    cx1 = x1 + offset
    cy1 = y1 + offset
    
    # कोपऱ्यांवर सुलभ कटिंगसाठी कॉर्नर कट्स (Corner Crop Lines)
    # Top-Left
    draw_obj.line([(cx0 - line_len, cy0), (cx0, cy0)], fill=color, width=width)
    draw_obj.line([(cx0, cy0 - line_len), (cx0, cy0)], fill=color, width=width)
    
    # Top-Right
    draw_obj.line([(cx1, cy0), (cx1 + line_len, cy0)], fill=color, width=width)
    draw_obj.line([(cx1, cy0 - line_len), (cx1, cy0)], fill=color, width=width)
    
    # Bottom-Left
    draw_obj.line([(cx0 - line_len, cy1), (cx0, cy1)], fill=color, width=width)
    draw_obj.line([(cx0, cy1), (cx0, cy1 + line_len)], fill=color, width=width)
    
    # Bottom-Right
    draw_obj.line([(cx1, cy1), (cx1 + line_len, cy1)], fill=color, width=width)
    draw_obj.line([(cx1, cy1), (cx1, cy1 + line_len)], fill=color, width=width)
    
    # कार्डभोवती हलकी तुटक (Dotted) सुरक्षित कटिंग लाईन
    dash_len = 15
    space_len = 10
    
    # वरची आणि खालची तुटक रेषा
    for x in range(int(cx0), int(cx1), dash_len + space_len):
        draw_obj.line([(x, cy0), (min(x + dash_len, cx1), cy0)], fill="#888888", width=1)
        draw_obj.line([(x, cy1), (min(x + dash_len, cx1), cy1)], fill="#888888", width=1)
        
    # डावी आणि उजवी तुटक रेषा
    for y in range(int(cy0), int(cy1), dash_len + space_len):
        draw_obj.line([(cx0, y), (cx0, min(y + dash_len, cy1))], fill="#888888", width=1)
        draw_obj.line([(cx1, y), (cx1, min(y + dash_len, cy1))], fill="#888888", width=1)

# ==========================================
# 🖥️ मुख्य इंटरफेस
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0F172A; font-weight: 800;'>बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #2563EB; font-weight: 600;'>आयुष्मान भारत - 4x6 पॉकेट कार्ड कंव्हर्टर (Safe Cutting Line)</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("आयुष्मान भारत PDF फाईल अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("4x6 कटिंग लाईन लेआउट जनरेट करा", type="primary", use_container_width=True):
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
                    
                    # 🎯 ३. मानक पॉकेट लॅमिनेशन साईझ (1020 x 640 px)
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    card_w, card_h = 1020, 640
                    
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    # कडक काळी ४ पिक्सेल मुख्य बॉर्डर
                    front_bordered = ImageOps.expand(img_front, border=4, fill='black')
                    back_bordered = ImageOps.expand(img_back, border=4, fill='black')
                    
                    bw, bh = front_bordered.size
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # दोन्ही बाजूने समान पांढरी मार्जिन ठेवून सेंटर पेस्टिंग
                    paste_x = (PAPER_WIDTH - bw) // 2
                    y_front = 180
                    y_back = 950
                    
                    final_canvas.paste(front_bordered, (paste_x, y_front))
                    final_canvas.paste(back_bordered, (paste_x, y_back))
                    
                    # 🎯 मुख्य बॉर्डरच्या १२ px बाहेर सेफ कटिंग लाईन्स आणि गाईड मार्क्स
                    draw = ImageDraw.Draw(final_canvas)
                    draw_safe_cutting_guides(draw, (paste_x, y_front, paste_x + bw, y_front + bh), offset=12)
                    draw_safe_cutting_guides(draw, (paste_x, y_back, paste_x + bw, y_back + bh), offset=12)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(400, 400))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    # प्रिव्ह्यू आणि डाऊनलोड
                    st.image(final_canvas, caption="4x6 Print Preview (Safe Margin Cutting Lines)", width=500)
                    st.write("")
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="4x6 सेफ कटिंग लाईन PNG डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_Safe_Cutting_4x6_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"त्रुटी: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #94A3B8;'>बालाजी सायबर पॉईंट, माणगाव, रायगड</p>", unsafe_allow_html=True)
