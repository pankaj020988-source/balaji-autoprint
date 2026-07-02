import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time

# पेज सेटिंग (Full Wide Layout)
st.set_page_config(page_title="बालाजी सायबर पॉईंट - होम", page_icon="🌐", layout="wide")

# ==========================================
# 👤 साईडबार युझर सेलेक्शन सिस्टीम
# ==========================================
if "user_role" not in st.session_state:
    st.session_state.user_role = "Manager (Pankajji)"

st.sidebar.markdown("### 👥 सिस्टीम युझर")
current_user = st.sidebar.radio(
    "कॉम्प्युटर कोण वापरत आहे?",
    ("Manager (Pankajji)", "Staff / Partner"),
    index=0 if st.session_state.user_role == "Manager (Pankajji)" else 1
)
st.session_state.user_role = current_user

st.sidebar.write("---")
st.sidebar.markdown(f"👤 **चालू युझर:** `{st.session_state.user_role}`")

# ==========================================
# 🚀 कडांना तंतोतंत लॉक करणारा कडक लेआउट कोड
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0056b3;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #28a745;'>आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ कडांना तंतोतंत मॅच करणारा कडक बॉक्स तयार होत आहे..."):
            try:
                pdf_bytes = uploaded_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                
                if len(doc) < 1:
                    st.error("मजकूर सापडला नाही! कृपया खरी पीडीएफ अपलोड करा.")
                else:
                    page = doc[0]
                    pix = page.get_pixmap(dpi=300)
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    width, height = img.size
                    
                    # 🎯 न कट होणारे कडक क्रॉपिंग कोऑर्डिनेट्स
                    front_box = (int(width * 0.038), int(height * 0.15), int(width * 0.492), int(height * 0.85))
                    back_box = (int(width * 0.508), int(height * 0.15), int(width * 0.962), int(height * 0.85))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 बाहेरचा मोठा पांढरा भाग घालवण्यासाठी रुंदी थेट १०८० पिक्सेलवर लॉक केली!
                    PAPER_WIDTH, PAPER_HEIGHT = 1080, 1620
                    card_w, card_h = 1080, 680  # कार्ड आणि कॅनव्हासची रुंदी एकसमान (० मार्जिन!)
                    
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # 🎯 डाव्या-उजव्या कडेला शंभर टक्के चिकटवून पेस्ट (० पिक्सेल अंतर)
                    final_canvas.paste(img_front, (0, 70))
                    final_canvas.paste(img_back, (0, 870))
                    
                    # 🔲 काठोकाठ कडक ४ पिक्सेलची काळी बॉर्डर (थेट कडांवर लॉक)
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([0, 70, PAPER_WIDTH - 1, 70 + card_h], outline="black", width=4)
                    draw.rectangle([0, 870, PAPER_WIDTH - 1, 870 + card_h], outline="black", width=4)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान कार्ड आता बॉक्समध्ये परफेक्ट फिट झाले आहे! (User: {st.session_state.user_role})")
                    
                    # स्क्रीनवर कडक प्रिव्ह्यू
                    st.image(final_canvas, caption="४x६ कडक प्रिंट प्रिव्ह्यू (No Margins)", width=600)
                    st.write("")
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_ExactFit_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
