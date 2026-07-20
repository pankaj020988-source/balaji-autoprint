import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageDraw
import io
import time

# ==========================================
# 🌐 पेज सेटिंग (बालाजी सायबर पॉईंट स्पेशल)
# ==========================================
st.set_page_config(page_title="श्री बालाजी सायबर पॉईंट - आयुष्मान 4X6 कंव्हर्टर", page_icon="🖨️", layout="wide")

# ==========================================
# ✂️ ऑटो-ट्रिमिंग (पांढरी जागा गायब करणारी सिस्टीम)
# ==========================================
def auto_crop_card(card_img):
    """कार्डच्या आजूबाजूची सर्व शुद्ध पांढरी जागा स्वयंचलितपणे कापून टाकते"""
    gray = card_img.convert("L")
    inverted = ImageOps.invert(gray)
    bbox = inverted.getbbox()
    if bbox:
        return card_img.crop(bbox)
    return card_img

# ==========================================
# 📢 मुख्य हेडर आणि लेआउट
# ==========================================
st.markdown("""
<div style="background: linear-gradient(135deg, #002f6c 0%, #0056b3 100%); padding: 20px; border-radius: 12px; text-align: center; color: white; border: 2px solid #d4af37; margin-bottom: 20px;">
    <h2 style="color: #e5be3b; margin: 0;">श्री बालाजी सायबर पॉईंट, माणगाव</h2>
    <h4 style="margin-top: 5px; font-size: 18px; opacity: 0.95;">आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कंव्हर्टर</h4>
</div>
""", unsafe_allow_html=True)

st.success("🔓 **सर्व टूल्स unlocked आहेत!** कोणतीही PDF टाका आणि १-क्लिकमध्ये ४x६ प्रिंट शीट डाऊनलोड करा.")
st.write("---")

# 📁 फाईल अपलोडर
uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ स्वयंचलित तंत्रज्ञानाद्वारे पांढरा भाग काढून लेआउट फिक्स होत आहे..."):
            try:
                # कॅशे क्लिअर करणे
                st.cache_data.clear()
                
                pdf_bytes = uploaded_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                
                if len(doc) < 1:
                    st.error("मजकूर सापडला नाही! कृपया खरी पीडीएफ अपलोड करा.")
                else:
                    page = doc[0]
                    # ४०० DPI वर हाय-डेफिनिशन कडक रेंडरिंग
                    pix = page.get_pixmap(dpi=400)
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    width, height = img.size
                    
                    # १. मूळ पीडीएफ मधून दोन्ही बाजूंचा सुरक्षित रफ क्रॉप
                    rough_front = img.crop((int(width * 0.03), int(height * 0.12), int(width * 0.50), int(height * 0.88)))
                    rough_back = img.crop((int(width * 0.50), int(height * 0.12), int(width * 0.97), int(height * 0.88)))
                    
                    # २. जादुई ऑटो-ट्रिम: आजूबाजूची सर्व एक्स्ट्रा पांढरी जागा स्वयंचलितपणे नष्ट!
                    img_front = auto_crop_card(rough_front)
                    img_back = auto_crop_card(rough_back)
                    
                    # ३. ४x६ कॅनव्हास आणि कार्डची साईझ कडांना मॅच करण्यासाठी परफेक्ट लॉक
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    card_w, card_h = 1200, 765
                    
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # डाव्या-उजव्या कडेला ० मार्जिनवर तंतोतंत पेस्ट (Edge-to-Edge)
                    final_canvas.paste(img_front, (0, 80))
                    final_canvas.paste(img_back, (0, 950))
                    
                    # काठोकाठ कडक ५ पिक्सेलची काळी बॉर्डर
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([0, 80, PAPER_WIDTH - 1, 80 + card_h], outline="black", width=5)
                    draw.rectangle([0, 950, PAPER_WIDTH - 1, 950 + card_h], outline="black", width=5)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(400, 400))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    st.success("✅ आयुष्मान कार्ड आता काठोकाठ फिट झाले असून क्वालिटी कडक झाली आहे!")
                    
                    # स्क्रीनवर प्रिव्ह्यू
                    st.image(final_canvas, caption="४x६ कडक प्रिंट प्रिव्ह्यू (ऑटो-फिट मास्टर)", width=650)
                    st.write("")
                    
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
st.markdown("<p style='text-align: center; font-size: 13px; color: #555; font-weight: bold;'>📍 श्री बालाजी सायबर पॉईंट, माणगाव | 📞 संपर्क: 8007365051</p>", unsafe_allow_html=True)
