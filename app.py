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
# 🚀 अजिबात कट न होणारा आणि कडांना बॉर्डर लॉक करणारा कोड
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0056b3;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #28a745;'>आयुष्मान भारत PDF ते 4X6 कडक PRINT कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ कार्ड सुरक्षित ठेवून काठोकाठ बॉर्डर सेट होत आहे..."):
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
                    
                    # 🎯 सुरक्षित क्रॉपिंग - कार्ड अजिबात कट होणार नाही याची पूर्ण खात्री (उंची भरपूर ठेवली आहे)
                    front_box = (int(width * 0.040), int(height * 0.14), int(width * 0.492), int(height * 0.86))
                    back_box = (int(width * 0.508), int(height * 0.14), int(width * 0.960), int(height * 0.86))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 ४x६ पेपरची मुख्य स्टँडर्ड साईझ (१२०० x १८००)
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    
                    # कार्डचा आकार एकदम प्रमाणबद्ध (चपटं किंवा कट न दिसण्यासाठी)
                    card_w, card_h = 1120, 715
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # 🎯 कॅनव्हासवर कार्ड्स एकदम मध्यभागी पेस्ट करणे
                    paste_x = (PAPER_WIDTH - card_w) // 2
                    
                    final_canvas.paste(img_front, (paste_x, 100))
                    final_canvas.paste(img_back, (paste_x, 950))
                    
                    # 🔲 🎯 कडक बदल: काळी बॉर्डर बाहेरच्या मोठ्या पांढऱ्या भागाला न मारता थेट कार्डच्या कडांना चिकटून मारणे!
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    
                    # यामुळे कात्रीने कापताना काळी रेघ थेट कार्डच्या काठावर मिळेल, पांढरा भाग कापायचा टेन्शन मिटेल!
                    draw.rectangle([paste_x, 100, paste_x + card_w, 100 + card_h], outline="black", width=5)
                    draw.rectangle([paste_x, 950, paste_x + card_w, 950 + card_h], outline="black", width=5)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान भारत कार्ड आता न कट होता बॉक्समध्ये परफेक्ट फिट झाले आहे! (User: {st.session_state.user_role})")
                    
                    # सुरक्षित स्क्रीन प्रिव्ह्यू
                    st.image(final_canvas, caption="४x६ कडक प्रिंट प्रिव्ह्यू (परफेक्ट फिट बॉर्डर)", width=620)
                    st.write("")
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_Perfect_NoCut_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
