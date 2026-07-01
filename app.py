import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageOps
import io

# पेज सेटिंग
st.set_page_config(page_title="बालाजी सायबर पॉईंट - लॉगिन", page_icon="🔐", layout="centered")

# ==========================================
# 🔐 मजबूत लॉगिन सिस्टीम (Robust Login)
# ==========================================
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# लॉगिन फॉर्म
if st.session_state.user_role is None:
    st.markdown("<h2 style='text-align: center; color: #0056b3;'>🔐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: gray;'>सिस्टीम वापरण्यासाठी लॉगिन करा</h5>", unsafe_allow_html=True)
    st.write("---")
    
    u_input = st.text_input("युझरनेम (Username):")
    p_input = st.text_input("पासवर्ड (Password):", type="password")
    
    if st.button("🔓 लॉगिन करा", type="primary", use_container_width=True):
        # .strip() मुळे चुकून झालेली स्पेस (Space) आपोआप निघून जाईल
        user_clean = u_input.strip().lower()
        pass_clean = p_input.strip()
        
        if user_clean == "balaji" and pass_clean == "pankaj1965":
            st.session_state.user_role = "Manager (Pankajji)"
            st.success("जी हुजूर! पंकजजी आपले स्वागत आहे.")
            st.rerun()
        elif user_clean == "staff" and pass_clean == "balaji77":
            st.session_state.user_role = "Staff / Partner"
            st.success("लॉगिन यशस्वी! स्टाफ मोड सक्रिय.")
            st.rerun()
        else:
            st.error("❌ चुकीचा युझरनेम किंवा पासवर्ड! कृपया पुन्हा तपासा.")
            
    st.stop() # लॉगिन होईपर्यंत पुढचा कोड पूर्णपणे लॉक राहील

# ==========================================
# 🚀 लॉगिन झाल्यावर मूळ आयुष्मान भारत कोड सुरू
# ==========================================
st.sidebar.markdown(f"👤 **चालू युझर:** `{st.session_state.user_role}`")
if st.sidebar.button("🔒 लॉग आऊट (Logout)"):
    st.session_state.user_role = None
    st.rerun()

st.markdown("<h2 style='text-align: center; color: #0056b3;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #28a745;'>आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कंव्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 कडक ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ पीडीएफ मधून कडक कार्ड लेआउट तयार होत आहे..."):
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
                    
                    crop_left = int(width * 0.05)
                    crop_top = int(height * 0.45)
                    crop_right = int(width * 0.95)
                    crop_bottom = int(height * 0.88)
                    
                    cropped_id = img.crop((crop_left, crop_top, crop_right, crop_bottom))
                    
                    target_w, target_h = 1200, 1800
                    cropped_id = cropped_id.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    cropped_id = ImageOps.expand(cropped_id, border=6, fill='black')
                    
                    img_byte_arr = io.BytesIO()
                    cropped_id.save(img_byte_arr, format='PNG', dpi=(300, 300))
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    st.success(f"✅ आयुष्मान कार्ड लेआउट एकदम कडक तयार झाले आहे! (User: {st.session_state.user_role})")
                    st.image(cropped_id, caption="४x६ प्रिंट प्रिव्ह्यू", use_container_width=True)
                    
                    st.download_button(
                        label="📥 कडक ४x६ प्रिंट इमेज (PNG) डाऊनलोड करा",
                        data=img_byte_arr,
                        file_name="Ayushman_Bharat_4x6_Print.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
