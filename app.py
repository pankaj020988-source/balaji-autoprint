import streamlit as st
from PIL import Image, ImageOps
import io
import fitz  # PyMuPDF

# ==========================================
# 🌐 १. लेआउट कॉन्फिगरेशन
# ==========================================
st.set_page_config(
    page_title="बालाजी सायबर पॉइंट - डिजिटल टूलकिट", 
    page_icon="🖥️", 
    layout="wide"
)

# ==========================================
# 🎨 २. कॉर्पोरेट UI डिझाईन (CSS)
# ==========================================
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    .main-header {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        text-align: center;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# मुख्य शीर्षक
st.markdown("<div class='main-header'>श्री बालाजी सायबर पॉईंट - आयुष्मान भारत 4x6 प्रिंट प्रोसेसिंग</div>", unsafe_allow_html=True)

# ==========================================
# 🛠️ ३. मुख्य कार्यप्रणाली (Ayushman 4x6 Layout)
# ==========================================
col_a1, col_a2 = st.columns([2, 1])
with col_a1:
    pdf_file = st.file_uploader("आयुष्मान भारत PDF फाईल अपलोड करा:", type=["pdf"], key="ayushman_pdf_uploader")
with col_a2:
    pdf_password = st.text_input("PDF पासवर्ड (असेल तर):", type="password", key="ayushman_pass_input")

if pdf_file is not None:
    if st.button("4x6 प्रिंटींग लेआउट जनरेट करा", type="primary", use_container_width=True, key="btn_ayushman_gen"):
        with st.spinner("प्रक्रिया सुरू आहे..."):
            try:
                pdf_bytes = pdf_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                
                if doc.is_encrypted:
                    if pdf_password:
                        auth_success = doc.authenticate(pdf_password)
                        if not auth_success:
                            st.error("चुकीचा पासवर्ड प्रविष्ट केला आहे.")
                            st.stop()
                    else:
                        st.warning("कृपया PDF पासवर्ड टाका.")
                        st.stop()

                page = doc[0]
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                full_img = Image.open(io.BytesIO(img_data)).convert("RGB")
                
                w, h = full_img.size
                
                # आयुष्मान भारत कार्ड क्रॉप कॉर्डिनेट्स
                crop_front = full_img.crop((int(w * 0.05), int(h * 0.55), int(w * 0.49), int(h * 0.88)))
                crop_back = full_img.crop((int(w * 0.51), int(h * 0.55), int(w * 0.95), int(h * 0.88)))
                
                PAPER_W, PAPER_HEIGHT = 1200, 1800
                final_canvas = Image.new("RGB", (PAPER_W, PAPER_HEIGHT), "white")

                card_w, card_h = 1050, 650
                front_resized = crop_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                back_resized = crop_back.resize((card_w, card_h), Image.Resampling.LANCZOS)

                front_bordered = ImageOps.expand(front_resized, border=4, fill='black')
                back_bordered = ImageOps.expand(back_resized, border=4, fill='black')

                paste_x = (PAPER_W - front_bordered.width) // 2
                
                final_canvas.paste(front_bordered, (paste_x, 150))
                final_canvas.paste(back_bordered, (paste_x, 920))

                st.image(final_canvas, caption="4x6 Print Preview", use_container_width=True)
                
                id_buffer = io.BytesIO()
                final_canvas.save(id_buffer, format="PNG", dpi=(300, 300))
                
                st.download_button(
                    label="4x6 PNG डाऊनलोड करा", 
                    data=id_buffer.getvalue(), 
                    file_name="Ayushman_4x6_Layout.png", 
                    mime="image/png", 
                    use_container_width=True,
                    key="dl_ayushman_btn"
                )
            except Exception as e:
                st.error(f"त्रुटी: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #94A3B8;'>श्री बालाजी सायबर पॉईंट, माणगाव, रायगड</p>", unsafe_allow_html=True)
