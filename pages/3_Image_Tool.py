import streamlit as st
from PIL import Image, ImageOps
import io

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - इमेज टूल", page_icon="📸", layout="centered")

st.markdown("<h2 style='text-align: center; color: #0078D7;'>📸 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>पासपोर्ट साईझ फोटो ऑटो-शीट जनरेटर (३.५ x ४.५ सेमी)</h4>", unsafe_allow_html=True)
st.write("---")

# 📥 १. फोटो अपलोड करण्यासाठी सुंदर बॉक्स
uploaded_image = st.file_uploader("ज्या फोटोचे पासपोर्ट साईझ शेड्स बनवायचे आहेत तो फोटो अपलोड करा:", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # फोटो मेमरीमध्ये लोड करणे
    img = Image.open(uploaded_image)
    
    st.image(img, caption="अपलोड केलेला मूळ फोटो", width=150)
    st.write("---")
    
    # 📏 २. साईझ आणि पेपर सेटिंग्ज (३०० DPI हाय क्वालिटी)
    DPI = 300
    id_w, id_h = int(3.5 / 2.54 * DPI), int(4.5 / 2.54 * DPI)  # ३.५ x ४.५ सेमी पिक्सेलमध्ये
    
    # ३. पेपर निवडीसाठी ऑप्शन्स
    paper_option = st.radio(
        "कोणत्या साईझच्या पेपरवर फोटो सेट करायचे आहेत?",
        ("४x६ इंच फोटो पेपर (4x6 Sheet)", "पूर्ण A4 सरकारी पेपर (Full A4 Sheet)")
    )
    
    if st.button("🚀 पासपोर्ट साईझ फोटो शीट तयार करा", type="primary", use_container_width=True):
        with st.spinner("⏳ परफेक्ट लेआउट तयार होत आहे..."):
            try:
                # निवडलेल्या पेपरनुसार पिक्सेल साईझ ठरवणे
                if "४x६" in paper_option:
                    canvas_w, canvas_h = int(4 * DPI), int(6 * DPI)
                    file_suffix = "4x6_Sheet"
                else:
                    canvas_w, canvas_h = int(8.27 * DPI), int(11.69 * DPI)
                    file_suffix = "A4_Sheet"
                
                # फोटो कडक ३.५ x ४.५ सेमी मध्ये फिट करणे
                resized_id = ImageOps.fit(img, (id_w, id_h), Image.Resampling.LANCZOS)
                
                # कोऱ्या पांढऱ्या पेपरचा कॅनव्हास तयार करणे
                sheet = Image.new("RGB", (canvas_w, canvas_h), "white")
                
                # फोटोंमधील अंतर (Margin) सेट करून ऑटो-पेस्ट चक्रव्यूह
                margin = 25
                for y in range(margin, canvas_h - id_h, id_h + margin):
                    for x in range(margin, canvas_w - id_w, id_w + margin):
                        sheet.paste(resized_id, (x, y))
                
                # प्रिव्ह्यू दाखवण्यासाठी आणि डाऊनलोड करण्यासाठी मेमरी सेव्हिंग
                buffer = io.BytesIO()
                sheet.save(buffer, format="JPEG", quality=95, dpi=(DPI, DPI))
                buffer.seek(0)
                
                st.success("✅ तुमचे पासपोर्ट फोटो शीट एकदम परफेक्ट तयार झाले आहे!")
                st.image(sheet, caption="⚙️ प्रिंट प्रिव्ह्यू (डाऊनलोड करून डायरेक्ट प्रिंट काढा)", use_container_width=True)
                
                # 📥 ४. कडक डाऊनलोड बटण
                st.download_button(
                    label="📥 तयार झालेली फोटो शीट (JPG) डाऊनलोड करा",
                    data=buffer,
                    file_name=f"Balaji_Passport_{file_suffix}.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ चूक झाली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
