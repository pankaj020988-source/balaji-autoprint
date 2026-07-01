import streamlit as st
from PIL import Image, ImageOps
import io

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - इमेज टूल्स", page_icon="📸", layout="centered")

# मुख्य टॅब्स तयार करणे (पासपोर्ट शीट आणि फॉर्म रीसायझर दोन्ही एकत्र)
tab1, tab2 = st.tabs(["📸 पासपोर्ट साईझ फोटो शीट मेकर", "📝 सरकारी फॉर्म फोटो व सही रीसायझर"])

# ==========================================
# 📸 टॅब १: पासपोर्ट साईझ फोटो शीट मेकर
# ==========================================
with tab1:
    st.markdown("<h3 style='text-align: center; color: #0078D7;'>📸 पासपोर्ट साईझ फोटो शीट जनरेटर (३.५ x ४.५ सेमी)</h3>", unsafe_allow_html=True)
    st.write("---")

    uploaded_image = st.file_uploader("ज्या फोटोचे पासपोर्ट साईझ शेड्स बनवायचे आहेत तो फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="pp_uploader")

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="अपलोड केलेला मूळ फोटो", width=150)
        st.write("---")
        
        DPI = 300
        id_w, id_h = int(3.5 / 2.54 * DPI), int(4.5 / 2.54 * DPI)
        
        paper_option = st.radio(
            "कोणत्या साईझच्या paper वर फोटो सेट करायचे आहेत?",
            ("४x६ inch फोटो पेपर (4x6 Sheet)", "पूर्ण A4 सरकारी पेपर (Full A4 Sheet)"),
            key="paper_opt"
        )
        
        if st.button("🚀 पासपोर्ट साईझ फोटो शीट तयार करा", type="primary", use_container_width=True, key="btn_pp"):
            with st.spinner("⏳ परफेक्ट हाय-क्वालिटी लेआउट तयार होत आहे..."):
                try:
                    if "४x६" in paper_option:
                        canvas_w, canvas_h = int(4 * DPI), int(6 * DPI)
                        file_suffix = "4x6_Sheet"
                    else:
                        canvas_w, canvas_h = int(8.27 * DPI), int(11.69 * DPI)
                        file_suffix = "A4_Sheet"
                    
                    resized_id = ImageOps.fit(img, (id_w, id_h), Image.Resampling.LANCZOS)
                    sheet = Image.new("RGB", (canvas_w, canvas_h), "white")
                    
                    margin = 25
                    for y in range(margin, canvas_h - id_h, id_h + margin):
                        for x in range(margin, canvas_w - id_w, id_w + margin):
                            sheet.paste(resized_id, (x, y))
                    
                    buffer = io.BytesIO()
                    sheet.save(buffer, format="PNG", dpi=(DPI, DPI))
                    buffer.seek(0)
                    
                    st.success("✅ तुमचे पासपोर्ट फोटो शीट एकदम हाय-क्वालिटीमध्ये तयार झाले आहे!")
                    st.image(sheet, caption="⚙️ प्रिंट प्रिव्ह्यू", use_container_width=True)
                    
                    st.download_button(
                        label="📥 तयार झालेली HD फोटो शीट (PNG) डाऊनलोड करा",
                        data=buffer,
                        file_name=f"Balaji_Passport_{file_suffix}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ चूक झाली: {e}")

# ==========================================
# 📝 टॅब २: सरकारी फॉर्म फोटो व सही रीसायझर
# ==========================================
with tab2:
    st.markdown("<h3 style='text-align: center; color: #4CAF50;'>📝 सरकारी फॉर्म - फोटो व सही कॉम्प्रेसर टूल</h3>", unsafe_allow_html=True)
    st.write("---")

    # फॉर्मसाठी फोटो किंवा सही निवडणे
    tool_mode = st.radio("तुम्हाला काय रीसाईझ करायचे आहे?", ("ग्राहक फोटो (Photo - 20KB)", "ग्राहक सही (Signature - 10KB)"))
    
    uploaded_file = st.file_uploader("तुमची फाईल (Photo/Sign) इथे अपलोड करा:", type=["jpg", "jpeg", "png"], key="form_uploader")
    
    if uploaded_file is not None:
        raw_img = Image.open(uploaded_file).convert("RGB")
        st.image(raw_img, caption="अपलोड केलेली मूळ फाईल", width=150)
        
        # मोडनुसार पिक्सेल आणि KB लिमिट सेट करणे
        if "Photo" in tool_mode:
            t_width, t_height, max_kb, label = 160, 200, 20, "Photo"
        else:
            t_width, t_height, max_kb, label = 256, 64, 10, "Signature"
            
        if st.button(f"⚡ {label} रीसाईझ आणि कॉम्प्रेस करा", type="primary", use_container_width=True):
            with st.spinner("⏳ कॉम्प्रेस होत आहे..."):
                try:
                    # १. पिक्सेल रीसाईझ (LANCZOS हाय क्वालिटी)
                    resized_img = raw_img.resize((t_width, t_height), Image.Resampling.LANCZOS)
                    
                    # २. स्मार्ट कॉम्प्रेशन लूप (KB लिमिटमध्ये बसवणे)
                    quality = 95
                    img_buffer = io.BytesIO()
                    resized_img.save(img_buffer, "JPEG", optimize=True, quality=quality)
                    
                    while img_buffer.tell() > max_kb * 1024 and quality > 10:
                        quality -= 5
                        img_buffer = io.BytesIO()
                        resized_img.save(img_buffer, "JPEG", optimize=True, quality=quality)
                        
                    final_bytes = img_buffer.getvalue()
                    final_size_kb = len(final_bytes) // 1024
                    
                    st.success(f"✅ {label} यशस्वीरित्या रीसाईझ झाला आहे! (फायनल साईझ: {final_size_kb} KB)")
                    st.image(final_bytes, caption=f"रीसाईझ केलेला {label} ({t_width}x{t_height})")
                    
                    # डाऊनलोड बटण
                    st.download_button(
                        label=f"📥 कॉम्प्रेस झालेली {label} डाऊनलोड करा",
                        data=final_bytes,
                        file_name=f"balaji_converted_{label.lower()}.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ चूक झाली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
