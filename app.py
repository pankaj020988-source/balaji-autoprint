import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time

# पेज सेटिंग
st.set_page_config(page_title="बालाजी सायबर पॉईंट - होम", page_icon="🌐", layout="centered")

# ==========================================
# 👤 साईडबार युझर सिलेक्शन सिस्टीम (पासवर्ड फ्री)
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
# 🚀 डेस्कटॉप ॲपप्रमाणे १००% कडक एज-टू-एज (Full Width)
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
                    # ३०० DPI वर हाय-क्वालिटी कडक रेंडरिंग
                    pix = page.get_pixmap(dpi=300)
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    width, height = img.size
                    
                    # 🎯 डेस्कटॉप ओरिजिनल पिक्सेल कॅल्क्युलेशननुसार परफेक्ट क्रॉप (No Side Margins)
                    front_box = (int(width * 0.04), int(height * 0.26), int(width * 0.49), int(height * 0.75))
                    back_box = (int(width * 0.51), int(height * 0.26), int(width * 0.96), int(height * 0.75))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 ४x६ पेपरच्या पूर्ण रुंदीला (१२०० पिक्सेल) लॉक करणे
                    card_w, card_h = 1200, 765
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    # ४x६ मुख्य कॅनव्हास (१२०० x १८०० उभा फोटो पेपर)
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # 🎯 डाव्या आणि उजव्या कडेला शंभर टक्के चिकटवून पेस्ट (० मार्जिन)
                    final_canvas.paste(img_front, (0, 60))
                    final_canvas.paste(img_back, (0, 920))
                    
                    # 🔲 कात्रीने व्यवस्थित कापण्यासाठी कडक ४ पिक्सेलची काळी काठोकाठ बॉर्डर
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([0, 60, card_w - 1, 60 + card_h], outline="black", width=4)
                    draw.rectangle([0, 920, card_w - 1, 920 + card_h], outline="black", width=4)
                    
                    # हाय-क्वालिटी पीएनजी मेमरी सेव्हिंग
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान कार्ड शंभर टक्के काठोकाठ फिट झाले आहे! (User: {st.session_state.user_role})")
                    st.image(final_canvas, caption="४x६ प्रिंट प्रिव्ह्यू (Edge-to-Edge)", use_container_width=True)
                    
                    # कॅश मेमरीचा घोळ टाळण्यासाठी युनिक आयडी
                    unique_time = int(time.time())
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr,
                        file_name=f"Ayushman_Desktop_Style_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
