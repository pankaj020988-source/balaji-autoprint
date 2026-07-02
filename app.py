import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

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
# 🚀 दुरुस्त केलेला कट-टू-कट आयुष्मान भारत कोड
# ==========================================
st.markdown("<h2 style='text-align: center; color: #0056b3;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #28a745;'>आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ पीडीएफ मधून परफेक्ट कट-टू-कट लेआउट तयार होत आहे..."):
            try:
                pdf_bytes = uploaded_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                
                if len(doc) < 1:
                    st.error("मजकूर सापडला नाही! कृपया खरी पीडीएफ अपलोड करा.")
                else:
                    page = doc[0]
                    # ३०० DPI वर स्पष्ट रेंडरिंग
                    pix = page.get_pixmap(dpi=300)
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    width, height = img.size
                    
                    # 🎯 परफेक्ट काठोकाठ क्रॉपिंग (पांढरा भाग काढून टाकणे)
                    # १. फ्रंट बाजू (डावीकडील हिस्सा)
                    front_box = (int(width * 0.03), int(height * 0.25), int(width * 0.49), int(height * 0.77))
                    # २. बॅक बाजू (उजवीकडील हिस्सा)
                    back_box = (int(width * 0.51), int(height * 0.25), int(width * 0.97), int(height * 0.77))
                    
                    img_front = img.crop(front_box)
                    img_back = img.crop(back_box)
                    
                    # 📏 ४x६ पेपरच्या रुंदीनुसार (१२०० पिक्सेल) पूर्ण फिट साईझ (११७० x ७४० पिक्सेल)
                    card_w, card_h = 1170, 740
                    img_front = img_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    img_back = img_back.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    
                    # 🖼️ ४x६ मुख्य कॅनव्हास (१२०० x १८०० उभा पेपर)
                    canvas_w, canvas_h = 1200, 1800
                    final_canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
                    
                    # सेंटर अलाइनमेंट
                    paste_x = (canvas_w - card_w) // 2
                    
                    # फ्रंट आणि बॅक कॅनव्हासवर पेस्ट करणे
                    final_canvas.paste(img_front, (paste_x, 80))   # वरून फक्त ८० पिक्सेल अंतर
                    final_canvas.paste(img_back, (paste_x, 920))  # मध्यभागी योग्य जागा
                    
                    # 🔲 कटिंग गाईडसाठी काठोकाठ ४ पिक्सेलची कडक काळी बॉर्डर
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(final_canvas)
                    draw.rectangle([paste_x, 80, paste_x + card_w, 80 + card_h], outline="black", width=4)
                    draw.rectangle([paste_x, 920, paste_x + card_w, 920 + card_h], outline="black", width=4)
                    
                    # हाय-क्वालिटी पीएनजी मेमरी सेव्हिंग
                    img_byte_arr = io.BytesIO()
                    final_canvas.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान कार्ड लेआउट एकदम काठोकाठ फिट तयार झाले आहे! (User: {st.session_state.user_role})")
                    st.image(final_canvas, caption="४x६ प्रिंट प्रिव्ह्यू (फुल साईझ)", use_container_width=True)
                    
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr,
                        file_name="Ayushman_Bharat_4x6_FullFit.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
