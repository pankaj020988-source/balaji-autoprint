import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time
import base64

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
# 🚀 दुरुस्त केलेला कोड - अजिबात कट न होणारा लेआउट
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
                    
                    # 🎯 वरची आणि खालची पट्टी पूर्णपणे सुरक्षित ठेवण्यासाठी क्रॉपिंगचे नवे कोऑर्डिनेट्स (उंची वाढवली आहे)
                    # १. फ्रंट बाजू (वरचा आणि खालचा भाग जास्त मोकळा ठेवला आहे जेणेकरून कट होणार नाही)
                    front_box = (int(width * 0.040), int(height * 0.12), int(width * 0.490), int(height * 0.86))
                    # २. बॅक बाजू
                    back_box = (int(width * 0.510), int(height * 0.12), int(width * 0.960), int(height * 0.86))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 ४x६ पेपरच्या कडांना चिकटवण्यासाठी पूर्ण १२०० पिक्सेल विड्थ आणि योग्य हाईट (१२०0 x ७९० पिक्सेल)
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    card_w, card_h = 1200, 790
                    
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    final_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    # 🎯 कडांना चिकटवून पेस्ट (वरून ५० पिक्सेल आणि खालच्या कार्डसाठी ९०० पिक्सेल जागा)
                    final_canvas.paste(img_front, (0, 50))
                    final_canvas.paste(img_back, (0, 930))
                    
                    # 🔲 कटिंगसाठी कडक ४ पिक्सेलची काळी काठोकाठ बॉर्डर
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([0, 50, PAPER_WIDTH - 1, 50 + card_h], outline="black", width=4)
                    draw.rectangle([0, 930, PAPER_WIDTH - 1, 930 + card_h], outline="black", width=4)
                    
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr_raw = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान कार्ड आता अजिबात कट न होता शंभर टक्के फिट झाले आहे! (User: {st.session_state.user_role})")
                    
                    # स्क्रीनवर कडक फुल विड्थ प्रिव्ह्यू
                    encoded = base64.b64encode(img_byte_arr_raw).decode()
                    v_id = int(time.time())
                    st.markdown(
                        f'<div style="text-align: center;"><img src="data:image/png;base64,{encoded}?v={v_id}" style="width: 100%; max-width: 650px; border: 1px solid #000; border-radius: 2px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/></div>',
                        unsafe_allow_html=True
                    )
                    st.write("")
                    
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr_raw,
                        file_name=f"Ayushman_NoCut_FullFit_{v_id}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
