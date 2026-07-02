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
# 🚀 १००% काठोकाठ कडक क्रॉप लेआउट (No Margins)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0056b3;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #28a745;'>आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ फालतू पांढरा भाग काढून तंतोतंत बॉर्डर मॅच होत आहे..."):
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
                    
                    # 🎯 अत्यंत कडक क्रॉपिंग (Extreme Tight Crop) - पांढऱ्या कडा पूर्णपणे गाळल्या आहेत!
                    front_box = (int(width * 0.052), int(height * 0.282), int(width * 0.478), int(height * 0.722))
                    back_box = (int(width * 0.522), int(height * 0.282), int(width * 0.948), int(height * 0.722))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 ४x६ पेपरच्या रुंदीनुसार (१२०0 पिक्सेल) पूर्ण भरून येण्यासाठी कडक साईझ
                    card_w, card_h = 1200, 755
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    # ४x६ मुख्य कॅनव्हास (१२०० x १८०० pixels - उभा फोटो पेपर)
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # 🎯 डाव्या आणि उजव्या कडेला शंभर टक्के चिकटवून पेस्ट (० मार्जिन!)
                    final_canvas.paste(img_front, (0, 70))
                    final_canvas.paste(img_back, (0, 930))
                    
                    # 🔲 काठोकाठ कडक ४ पिक्सेलची काळी बॉर्डर - थेट कार्डच्या कडांना तंतोतंत चिकटून!
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([0, 70, PAPER_WIDTH - 1, 70 + card_h], outline="black", width=4)
                    draw.rectangle([0, 930, PAPER_WIDTH - 1, 930 + card_h], outline="black", width=4)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान भारत कार्ड आता काठोकाठ कडांना चिकटून बॉक्समध्ये फिट झाले आहे! (User: {st.session_state.user_role})")
                    
                    # स्क्रीनवर कडक सुरक्षित प्रिव्ह्यू
                    st.image(final_canvas, caption="४x६ कडक प्रिंट प्रिव्ह्यू (No Margins - Tight Fit)", width=620)
                    st.write("")
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_TightFit_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
