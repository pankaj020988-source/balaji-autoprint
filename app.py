import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time

# पेज सेटिंग (बालाजी सायबर पॉईंट थीम)
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
# 🚀 दुरुस्त केलेला कडक ओरीजनल मास्टर कोड (१००% अचूक)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0056b3;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #28a745;'>आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ कार्ड न कट होता परफेक्ट लेआउट तयार होत आहे..."):
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
                    
                    # 🎯 🎯 कडक बदल: वरचा आणि खालचा भाग अजिबात कट न होण्यासाठी उंचीचे कोऑर्डिनेट्स वाढवले (Perfect Safe Zone)
                    front_box = (int(width * 0.04), int(height * 0.14), int(width * 0.49), int(height * 0.85))
                    back_box = (int(width * 0.51), int(height * 0.14), int(width * 0.96), int(height * 0.85))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 ४x६ पेपरची मुख्य स्टँडर्ड साईझ (१२०० x १८०० pixels)
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    
                    # उंची थोडी वाढवली जेणेकरून अक्षर किंवा पट्टी दाबलेली दिसणार नाही (१२०० x ७९५)
                    card_w, card_h = 1200, 795
                    
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # 🎯 डाव्या आणि उजव्या कडेला ० मार्जिन (Edge-to-Edge परफेक्ट कडांना चिकटून पेस्ट)
                    final_canvas.paste(img_front, (0, 60))
                    final_canvas.paste(img_back, (0, 930))
                    
                    # 🔲 कात्रीने व्यवस्थित कापण्यासाठी कडक ४ पिक्सेलची काठोकाठ बॉर्डर
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([0, 60, PAPER_WIDTH - 1, 60 + card_h], outline="black", width=4)
                    draw.rectangle([0, 930, PAPER_WIDTH - 1, 930 + card_h], outline="black", width=4)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान भारत कार्ड आता न कट होता १००% परफेक्ट फिट झाले आहे! (User: {st.session_state.user_role})")
                    
                    # स्क्रीन प्रिव्ह्यू
                    st.image(final_canvas, caption="४x६ प्रिंट प्रिव्ह्यू (दुरुस्त केलेला परफेक्ट कोड)", width=650)
                    st.write("")
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_Master_Fix_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
