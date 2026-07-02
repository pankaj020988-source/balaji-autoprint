import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import io

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - इमेज टूल्स", page_icon="📸", layout="centered")

st.markdown("<h2 style='text-align: center; color: #0078D7;'>📸 श्री बालाजी सायबर पॉईंट - इमेज पोर्टल्स</h2>", unsafe_allow_html=True)
st.write("---")

# मुख्य चार टॅब्स
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 पासपोर्ट फोटो शीट मेकर", 
    "📝 सरकारी फॉर्म फोटो-सही रीसायझर", 
    "🖨️ स्मार्ट आयडी कार्ड प्रिंटर",
    "📸 कॅम-स्कॅनर (Super Fast)"
])

# ==========================================
# 📸 टॅब १: पासपोर्ट साईझ फोटो शीट मेकर
# ==========================================
with tab1:
    st.markdown("<h4 style='color: #0078D7;'>पासपोर्ट साईझ फोटो ऑटो-शीट जनरेटर (३.५ x ४.५ सेमी)</h4>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("ज्या फोटोचे पासपोर्ट साईझ बनवायचे आहेत तो फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="pp_uploader")

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="अपलोड केलेला मूळ फोटो", width=150)
        st.write("---")
        
        DPI = 300
        id_w, id_h = int(3.5 / 2.54 * DPI), int(4.5 / 2.54 * DPI)
        
        paper_option = st.radio(
            "कोणत्या साईझच्या paper वर फोटो सेट करायचे आहेत?",
            ("४x६ inch फोटो पेपर (4x6 Sheet)", "पूर्ण A4 सरकारी paper (Full A4 Sheet)"),
            key="paper_opt"
        )
        
        if st.button("🚀 पासपोर्ट साईझ फोटो शीट तयार करा", type="primary", use_container_width=True, key="btn_pp"):
            with st.spinner("⏳ कडक हाय-क्वालिटी लेआउट तयार होत आहे..."):
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
                    
                    st.success("✅ तुमचे पासपोर्ट फोटो शीट तयार झाले आहे!")
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
    st.markdown("<h4 style='color: #4CAF50;'>सरकारी फॉर्म - फोटो व सही कॉम्प्रेसर टूल</h4>", unsafe_allow_html=True)
    tool_mode = st.radio("तुम्हाला काय रीसाईझ करायचे आहे?", ("ग्राहक फोटो (Photo - 20KB)", "ग्राहक सही (Signature - 10KB)"))
    uploaded_file = st.file_uploader("तुमची फाईल (Photo/Sign) इथे अपलोड करा:", type=["jpg", "jpeg", "png"], key="form_uploader")
    
    if uploaded_file is not None:
        raw_img = Image.open(uploaded_file).convert("RGB")
        st.image(raw_img, caption="अपलोड केलेली मूळ फाईल", width=150)
        
        if "Photo" in tool_mode:
            t_width, t_height, max_kb, label = 160, 200, 20, "Photo"
        else:
            t_width, t_height, max_kb, label = 256, 64, 10, "Signature"
            
        if st.button(f"⚡ {label} रीसाईझ आणि कॉम्प्रेस करा", type="primary", use_container_width=True):
            with st.spinner("⏳ कॉम्प्रेस होत आहे..."):
                try:
                    resized_img = raw_img.resize((t_width, t_height), Image.Resampling.LANCZOS)
                    quality = 95
                    img_buffer = io.BytesIO()
                    resized_img.save(img_buffer, "JPEG", optimize=True, quality=quality)
                    
                    while img_buffer.tell() > max_kb * 1024 and quality > 10:
                        quality -= 5
                        img_buffer = io.BytesIO()
                        resized_img.save(img_buffer, "JPEG", optimize=True, quality=quality)
                        
                    final_bytes = img_buffer.getvalue()
                    final_size_kb = len(final_bytes) // 1024
                    
                    st.success(f"✅ {label} यशस्वीरित्या रीसाईझ झाला आहे! (साईझ: {final_size_kb} KB)")
                    st.image(final_bytes, caption=f"रीसाईझ केलेला {label}")
                    
                    st.download_button(
                        label=f"📥 कॉम्प्रेस झालेली {label} डाऊनलोड करा",
                        data=final_bytes,
                        file_name=f"balaji_converted_{label.lower()}.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ चूक झाली: {e}")

# ==========================================
# 🖨️ टॅब ३: स्मार्ट आयडी कार्ड प्रिंटर
# ==========================================
with tab3:
    st.markdown("<h4 style='color: #0056b3;'>स्मार्ट आयडी कार्ड प्रिंटर</h4>", unsafe_allow_html=True)
    
    col_id1, col_id2 = st.columns(2)
    with col_id1:
        front_file = st.file_uploader("१. फ्रंट बाजूचा (Front Side) फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="id_front")
    with col_id2:
        back_file = st.file_uploader("२. बॅक बाजूचा (Back Side) फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="id_back")

    if front_file is not None and back_file is not None:
        if st.button("⚙️ ४x६ कडक प्रिंट लेआउट तयार करा", type="primary", use_container_width=True, key="btn_id_generate"):
            with st.spinner("⏳ लेआउट तयार होत आहे..."):
                try:
                    img_f = Image.open(front_file).convert("RGB")
                    img_b = Image.open(back_file).convert("RGB")
                    
                    final_w, final_h = 1130, 710
                    img_f = img_f.resize((final_w, final_h), Image.Resampling.LANCZOS)
                    img_b = img_b.resize((final_w, final_h), Image.Resampling.LANCZOS)
                    
                    img_f = ImageOps.expand(img_f, border=6, fill='black')
                    img_b = ImageOps.expand(img_b, border=6, fill='black')
                    
                    PAPER_WIDTH, PAPER_HEIGHT = 1200, 1800
                    id_canvas = Image.new("RGB", (PAPER_WIDTH, PAPER_HEIGHT), "white")
                    
                    paste_x = (PAPER_WIDTH - img_f.width) // 2
                    
                    id_canvas.paste(img_f, (paste_x, 150))
                    id_canvas.paste(img_b, (paste_x, 950))
                    
                    id_buffer = io.BytesIO()
                    id_canvas.save(id_buffer, format="PNG", dpi=(300, 300))
                    id_buffer.seek(0)
                    
                    st.success("✅ आयडी कार्ड प्रिंट sheet एकदम रेडी आहे!")
                    st.image(id_canvas, caption="४x६ प्रिंट प्रिव्ह्यू", use_container_width=True)
                    
                    st.download_button(
                        label="📥 ४x६ कडक आयडी कार्ड प्रिंट (PNG) डाऊनलोड करा",
                        data=id_buffer,
                        file_name="Balaji_Smart_ID_Print.png",
                        mime="image/png",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ चूक झाली: {e}")

# ==========================================
# 📸 टॅब ४: वेगवान वन-क्लिक कॅम-स्कॅनर (Super Fast Automation)
# ==========================================
with tab4:
    st.markdown("<h4 style='color: #E65100;'>📸 बालाजी सुपर-फास्ट कॅम-स्कॅनर</h4>", unsafe_allow_html=True)
    st.write("झटपट क्रॉप आणि सरळ करण्यासाठी फक्त खालील बटनांवर क्लिक करा. स्लायडर्स सरकवण्याची गरज नाही!")
    st.write("---")
    
    # क्रॉप आणि रोटेशनसाठी मेमरी स्टेट मॅनेजमेंट
    if "c_left" not in st.session_state: st.session_state.c_left = 0
    if "c_right" not in st.session_state: st.session_state.c_right = 0
    if "c_top" not in st.session_state: st.session_state.c_top = 0
    if "c_bottom" not in st.session_state: st.session_state.c_bottom = 0
    if "r_angle" not in st.session_state: st.session_state.r_angle = 0

    scan_file = st.file_uploader("स्कॅन करण्यासाठी डॉक्युमेंटचा फोटो अपलोड करा (JPG/PNG):", type=["jpg", "jpeg", "png"], key="scanner_upload")

    if scan_file is not None:
        original_image = Image.open(scan_file)
        
        # ⚡ वन-क्लिक कंट्रोल बटन्स पॅनेल
        st.markdown("##### ⚡ १. वन-क्लिक फास्ट कंट्रोल्स:")
        
        col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
        with col_b1:
            if st.button("⬅️ डावीकडून कापा", use_container_width=True): st.session_state.c_left += 5
        with col_b2:
            if st.button("➡️ उजवीकडून कापा", use_container_width=True): st.session_state.c_right += 5
        with col_b3:
            if st.button("⬆️ वरून कापा", use_container_width=True): st.session_state.c_top += 5
        with col_b4:
            if st.button("⬇️ खालून कापा", use_container_width=True): st.session_state.c_bottom += 5
        with col_b5:
            if st.button("🔄 ९०° फिरवा", use_container_width=True): st.session_state.r_angle = (st.session_state.r_angle + 90) % 360

        if st.button("🔄 सर्व नियंत्रणे रिसेट करा (Reset All)", type="secondary", use_container_width=True):
            st.session_state.c_left = 0
            st.session_state.c_right = 0
            st.session_state.c_top = 0
            st.session_state.c_bottom = 0
            st.session_state.r_angle = 0
            st.rerun()

        scan_mode = st.selectbox(
            "🎨 कलर मोड निवडा:", 
            ["मॅजिक कलर (Magic Color)", "कडक ब्लॅक & व्हाईट (B&W)", "मूळ कलर"],
            key="scanner_mode_select"
        )
        
        # --- फास्ट इमेज प्रोसेसिंग ---
        # रोटेशन अप्लाय करणे
        if st.session_state.r_angle != 0:
            if st.session_state.r_angle == 90: working_img = original_image.transpose(Image.ROTATE_270)
            elif st.session_state.r_angle == 180: working_img = original_image.transpose(Image.ROTATE_180)
            elif st.session_state.r_angle == 270: working_img = original_image.transpose(Image.ROTATE_90)
            else: working_img = original_image
        else:
            working_img = original_image
            
        # क्रॉपिंग अप्लाय करणे
        w, h = working_img.size
        l_px = int(w * (st.session_state.c_left / 100))
        r_px = w - int(w * (st.session_state.c_right / 100))
        t_px = int(h * (st.session_state.c_top / 100))
        b_px = h - int(h * (st.session_state.c_bottom / 100))
        
        if r_px > l_px and b_px > t_px:
            working_img = working_img.crop((l_px, t_px, r_px, b_px))
            
        st.write("---")
        st.markdown("##### 📐 २. तुमचा लाईव्ह क्रॉप प्रिव्ह्यू (Live Crop Preview):")
        st.image(working_img, caption="सध्याचा दस्तऐवज आकार", use_container_width=True)
        st.write("---")
        
        if st.button("🚀 ३. मॅजिक स्कॅनिंग फिनिश करा", type="primary", use_container_width=True, key="scan_btn"):
            with st.spinner("⏳ सिस्टीम सावली साफ करून रिझल्ट कडक करत आहे..."):
                try:
                    img_np = np.array(working_img.convert('RGB'))
                    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                    
                    if scan_mode == "कडक ब्लॅक & व्हाईट (B&W)":
                        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                        scanned = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 12)
                        final_res = Image.fromarray(scanned)
                        
                    elif scan_mode == "मॅजिक कलर (Magic Color)":
                        channels = cv2.split(img_cv)
                        result_channels = []
                        for ch in channels:
                            dilated = cv2.dilate(ch, np.ones((7,7), np.uint8))
                            bg = cv2.medianBlur(dilated, 21)
                            diff = cv2.absdiff(ch, bg)
                            diff = 255 - diff
                            norm = cv2.normalize(diff, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
                            result_channels.append(norm)
                        
                        merged_bg = cv2.merge(result_channels)
                        blended = cv2.addWeighted(img_cv, 0.60, merged_bg, 0.40, 0)
                        
                        enhanced_pil = Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
                        
                        enhancer = ImageEnhance.Contrast(enhanced_pil)
                        enhanced_pil = enhancer.enhance(1.3)
                        sharp = ImageEnhance.Sharpness(enhanced_pil)
                        final_res = sharp.enhance(1.2)
                    else:
                        final_res = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
                    
                    st.markdown("#### 🖨️ तुमचा फायनल स्कॅन झालेला रिझल्ट:")
                    st.image(final_res, use_container_width=True)
                    
                    img_byte_arr = io.BytesIO()
                    final_res.save(img_byte_arr, format='JPEG', quality=95)
                    
                    st.write("")
                    st.download_button(
                        label="📥 स्कॅन झालेली परफेक्ट इमेज डाऊनलोड करा",
                        data=img_byte_arr.getvalue(),
                        file_name="Balaji_Perfect_Scan.jpg",
                        mime="image/jpeg",
                        use_container_width=True,
                        key="scan_dl_btn"
                    )
                except Exception as e:
                    st.error(f"❌ चूक झाली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
