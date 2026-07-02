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
# 🚀 ४०० DPI हाय-क्वालिटी नो-मार्जिन कडक कोड
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0056b3;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #28a745;'>आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ क्वालिटी वाढवून काठोकाठ बॉक्स फिक्स केला जात आहे..."):
            try:
                # सर्व्हरची जुनी मेमरी क्लिअर करण्यासाठी फाईल वाचन
                st.cache_data.clear()
                
                pdf_bytes = uploaded_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                
                if len(doc) < 1:
                    st.error("मजकूर सापडला नाही! कृपया खरी पीडीएफ अपलोड करा.")
                else:
                    page = doc[0]
                    # क्वालिटी एकदम कडक आणि अक्षरे स्पष्ट ठेवण्यासाठी ४०० DPI वर रेंडरिंग
                    pix = page.get_pixmap(dpi=400)
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    width, height = img.size
                    
                    # 🎯 चारी बाजूंनी नको असलेली पांढरी जागा छाटण्यासाठी अचूक क्रॉपिंग
                    front_box = (int(width * 0.035), int(height * 0.13), int(width * 0.495), int(height * 0.86))
                    back_box = (int(width * 0.505), int(height * 0.13), int(width * 0.965), int(height * 0.86))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 ४x६ कॅनव्हास आणि कार्डची रुंदी एकाच पिक्सेलवर लॉक (० मार्जिन!)
                    # यामुळे बाहेर कोणतीही अतिरिक्त पांढरी जागा शिल्लक राहूच शकत नाही
                    card_w = 1200
                    card_h = 790
                    
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    # मुख्य ४x६ मास्टर कॅनव्हास (Exact Paper Ratio)
                    PAPER_WIDTH = 1200
                    PAPER_HEIGHT = 1800
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # डाव्या-उजव्या बाजूला थेट ० पिक्सेलवर चिकटवून पेस्ट (No Left/Right Margins)
                    final_canvas.paste(img_front, (0, 60))
                    final_canvas.paste(img_back, (0, 950))
                    
                    # 🔲 काठोकाठ कडक ५ पिक्सेलची काळी बॉर्डर - थेट कार्डच्या कडांवर फिक्स!
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([0, 60, PAPER_WIDTH - 1, 60 + card_h], outline="black", width=5)
                    draw.rectangle([0, 950, PAPER_WIDTH - 1, 950 + card_h], outline="black", width=5)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(400, 400))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान कार्ड आता काठोकाठ फिट झाले असून क्वालिटी कडक झाली आहे! (User: {st.session_state.user_role})")
                    
                    # स्क्रीनवर कडक प्रिव्ह्यू
                    st.image(final_canvas, caption="४x६ कडक प्रिंट प्रिव्ह्यू (हाय-क्वालिटी)", width=650)
                    st.write("")
                    
                    unique_time = int(time.time())
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_HD_BoxFit_{unique_time}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
