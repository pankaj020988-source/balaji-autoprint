import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time
import base64

# पेज सेटिंग (Full Wide Layout)
st.set_page_config(page_title="बालाजी सायबर पॉईंट - होम", page_icon="🌐", layout="wide")

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
# 🚀 डेस्कटॉप मास्टर पिक्सेल मॅपिंग कोड (१००% कडक फिट)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0056b3;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #28a745;'>आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ डेस्कटॉप मास्टर लॉजिकनुसार काठोकाठ कटिंग सुरू आहे..."):
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
                    
                    # 🎯 कडक आणि टाईट क्रॉपिंग - नको असलेला सर्व पांढरा भाग काढून टाकणे
                    front_box = (int(width * 0.042), int(height * 0.27), int(width * 0.485), int(height * 0.735))
                    back_box = (int(width * 0.515), int(height * 0.27), int(width * 0.958), int(height * 0.735))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 ४x६ पेपरच्या कडांना चिकटवण्यासाठी पूर्ण १२०० पिक्सेल रुंदी वापरणे (० मार्जिन)
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    card_w, card_h = 1200, 765
                    
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # 🎯 डाव्या-उजव्या कडेला ० पिक्सेल (Edge-to-Edge पेस्ट)
                    final_canvas.paste(img_front, (0, 60))
                    final_canvas.paste(img_back, (0, 930))
                    
                    # 🔲 कटिंगसाठी काठोकाठ ४ पिक्सेलची कडक काळी बॉर्डर
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([0, 60, PAPER_WIDTH - 1, 60 + card_h], outline="black", width=4)
                    draw.rectangle([0, 930, PAPER_WIDTH - 1, 930 + card_h], outline="black", width=4)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान कार्ड शंभर टक्के काठोकाठ फिट झाले आहे! (User: {st.session_state.user_role})")
                    
                    # 🎯 स्क्रीनवर प्रिव्ह्यू मोठ्या रुंदीत दाखवणे
                    encoded = base64.b64encode(img_byte_arr_raw).decode()
                    st.markdown(
                        f'<div style="text-align: center;"><img src="data:image/png;base64,{encoded}" style="width: 100%; max-width: 650px; border: 1px solid #000; border-radius: 2px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/></div>',
                        unsafe_allow_html=True
                    )
                    st.write("")
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_PerfectFit_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
