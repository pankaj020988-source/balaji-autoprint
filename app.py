import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time

# पेज सेटिंग
st.set_page_config(page_title="बालाजी सायबर पॉईंट - होम", page_icon="🌐", layout="centered")

# ==========================================
# 👤 साईडबार युझर सिलेक्शन सिस्टीम
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
# 🚀 १००% परफेक्ट कट-टू-कट फुल विड्थ कन्व्हर्टर
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0056b3;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #28a745;'>आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ परफेक्ट काठोकाठ कटिंग आणि कॉम्प्रेशन सुरू आहे..."):
            try:
                pdf_bytes = uploaded_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                
                if len(doc) < 1:
                    st.error("मजकूर सापडला नाही! कृपया खरी पीडीएफ अपलोड करा.")
                else:
                    page = doc[0]
                    # हाय रिझोल्यूशन रेंडरिंग (300 DPI)
                    pix = page.get_pixmap(dpi=300)
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    width, height = img.size
                    
                    # 🎯 परफेक्ट कडक क्रॉपिंग - फक्त कार्डचा मुख्य भाग निवडणे (No Margins)
                    # १. फ्रंट बाजू (परफेक्ट डावा भाग)
                    front_box = (int(width * 0.05), int(height * 0.28), int(width * 0.485), int(height * 0.74))
                    # २. बॅक बाजू (परफेक्ट उजवा भाग)
                    back_box = (int(width * 0.515), int(height * 0.28), int(width * 0.95), int(height * 0.74))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 ४x६ पेपरच्या रुंदीएवढी पूर्ण फिट साईझ (११९० x ७६०)
                    card_w, card_h = 1190, 760
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    # ४x६ मुख्य कॅनव्हास (१२०० x १८०० उभा पेपर)
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # डाव्या-उजव्या बाजूने परफेक्ट सेंटर (काठोकाठ भरण्यासाठी)
                    paste_x = (PAPER_WIDTH - card_w) // 2
                    
                    # फ्रंट वर आणि बॅक खाली पेस्ट करणे
                    final_canvas.paste(img_front, (paste_x, 60))
                    final_canvas.paste(img_back, (paste_x, 900))
                    
                    # 🔲 कटिंग करण्यासाठी कडक ४ पिक्सेलची काळी बॉर्डर
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([paste_x, 60, paste_x + card_w, 60 + card_h], outline="black", width=4)
                    draw.rectangle([paste_x, 900, paste_x + card_w, 900 + card_h], outline="black", width=4)
                    
                    # मेमरी सेव्हिंग
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान कार्ड लेआउट एकदम काठोकाठ सरळ फिट झाले आहे! (User: {st.session_state.user_role})")
                    
                    # कॅश अडथळा रोखण्यासाठी प्रिव्ह्यू
                    st.image(final_canvas, caption="४x६ कडक प्रिंट प्रिव्ह्यू (Full Width)", use_container_width=True)
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr,
                        file_name=f"Ayushman_FullFit_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
