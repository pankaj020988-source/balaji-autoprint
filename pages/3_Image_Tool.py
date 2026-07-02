import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import io
import cv2
import numpy as np

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - इमेज टूल्स", page_icon="📸", layout="centered")

st.markdown("<h2 style='text-align: center; color: #0078D7;'>📸 श्री बालाजी सायबर पॉईंट - इमेज पोर्टल्स</h2>", unsafe_allow_html=True)
st.write("---")

# मुख्य चार टॅब्स
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 पासपोर्ट फोटो शीट मेकर", 
    "📝 सरकारी फॉर्म फोटो-सही रीसायझर", 
    "🖨️ स्मार्ट आयडी कार्ड प्रिंटर (Aadhaar/PAN)",
    "📸 कॅम-स्कॅनर (CamScanner)"
])

# ==========================================
# 📸 टॅब १: पासपोर्ट साईझ फोटो शीट मेकर
# ==========================================
with tab1:
    st.markdown("<h4 style='color: #0078D7;'>पासपोर्ट साईझ फोटो批次 जनरेटर (३.५ x ४.५ सेमी)</h4>", unsafe_allow_html=True)
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
                    
                    st.success(f"✅ {label} यशस्वीरित्या रीसाईझ झाला आहे! (फायनल साईझ: {final_size_kb} KB)")
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
# 🖨️ टॅब ३: स्मार्ट आयडी कार्ड प्रिंटर (Aadhaar/PAN/Voter)
# ==========================================
with tab3:
    st.markdown("<h4 style='color: #0056b3;'>स्मार्ट आयडी कार्ड प्रिंटर (Aadhaar/PAN/Voter)</h4>", unsafe_allow_html=True)
    
    col_id1, col_id2 = st.columns(2)
    with col_id1:
        front_file = st.file_uploader("१. फ्रंट बाजूचा (Front Side) फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="id_front")
    with col_id2:
        back_file = st.file_uploader("२. बॅक बाजूचा (Back Side) फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="id_back")

    if front_file is not None and back_file is not None:
        if st.button("⚙️ ४x६ कडक प्रिंट लेआउट तयार करा", type="primary", use_container_width=True, key="btn_id_generate"):
            with st.spinner("⏳ दोन्ही बाजूंची साईझ एकसमान करून बॉर्डर सेट होत आहे..."):
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
                    st.image(id_canvas, caption="४x६ प्रिंट प्रिव्ह्यू (फ्रंट वर, बॅक खाली)", use_container_width=True)
                    
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
# 📸 टॅब ४: प्रगत कॅम-स्कॅनर टूल (ऑटो-सरळ आणि कडक कलर)
# ==========================================
with tab4:
    st.markdown("<h4 style='color: #E65100;'>📸 प्रगत डिजिटल कॅम-स्कॅनर (CamScanner Master)</h4>", unsafe_allow_html=True)
    st.write("हे टूल तिरपा आलेला फोटो स्वयंचलितपणे शोधून सरळ करेल आणि मूळ फोटोमधील चेहरा व रंग सुरक्षित ठेवून मागचा अंधार साफ करेल.")
    st.write("---")
    
    def scan_and_straighten_image(pil_image, mode):
        # PIL चे OpenCV मध्ये रूपांतर करणे
        img = np.array(pil_image.convert('RGB'))
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        orig = img_bgr.copy()
        
        # 🎯 १. कडा शोधून फोटो सरळ करणे (Perspective Auto-Crop)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 30, 120)
        
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        warped = orig
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            
            # ४ कडा सापडल्यास आणि तो एरिया पुरेसा मोठा असल्यास सरळ करणे
            if len(approx) == 4 and cv2.contourArea(c) > (img_bgr.shape[0] * img_bgr.shape[1] * 0.15):
                pts = approx.reshape(4, 2)
                rect = np.zeros((4, 2), dtype="float32")
                
                s = pts.sum(axis=1)
                rect[0] = pts[np.argmin(s)]
                rect[2] = pts[np.argmax(s)]
                
                diff = np.diff(pts, axis=1)
                rect[1] = pts[np.argmin(diff)]
                rect[3] = pts[np.argmax(diff)]
                
                (tl, tr, br, bl) = rect
                widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
                widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
                maxWidth = max(int(widthA), int(widthB))
                
                heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
                heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                maxHeight = max(int(heightA), int(heightB))
                
                dst = np.array([
                    [0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]], dtype="float32")
                
                M = cv2.getPerspectiveTransform(rect, dst)
                warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
                break
        
        # 🎯 २. फिल्टर आणि एन्हान्समेंट लॉजिक (चेहरा न उडवता कडक स्कॅनिंग)
        if mode == "कडक ब्लॅक & व्हाईट (B&W)":
            gray_w = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
            scanned = cv2.adaptiveThreshold(gray_w, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 12)
            return Image.fromarray(scanned)
            
        elif mode == "मॅजिक कलर (Magic Color)":
            # सौम्य बॅकग्राउंड इल्युमिनेशन कॉम्पेन्सेशन (सावली धुवून काढणे)
            dilated = cv2.dilate(warped, np.ones((11,11), np.uint8))
            bg = cv2.GaussianBlur(dilated, (51, 51), 0)
            diff = cv2.absdiff(warped, bg)
            clean_bg = 255 - diff
            
            # मूळ फोटोचे टोन टिकवून ठेवण्यासाठी ओरिजिनल आणि क्लीन प्रतिमेचे कडक मिश्रण (Soft Blend)
            blended = cv2.addWeighted(warped, 0.45, clean_bg, 0.55, 0)
            
            enhanced_pil = Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
            
            # अक्षरे ठळक करण्यासाठी हलका कॉन्ट्रास्ट आणि शार्पनेस वाढवणे
            enhancer = ImageEnhance.Contrast(enhanced_pil)
            enhanced_pil = enhancer.enhance(1.25)
            sharp = ImageEnhance.Sharpness(enhanced_pil)
            return sharp.enhance(1.2)
            
        return Image.fromarray(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))

    scan_file = st.file_uploader("स्कॅन करण्यासाठी प्रतिमेचा फोटो अपलोड करा (JPG/PNG):", type=["jpg", "jpeg", "png"], key="scanner_upload")

    if scan_file is not None:
        original_image = Image.open(scan_file)
        
        col_scan1, col_scan2 = st.columns(2)
        
        with col_scan1:
            st.markdown("**📱 मूळ फोटो:**")
            st.image(original_image, use_container_width=True)
            
        scan_mode = st.selectbox(
            "स्कॅनर मोड निवडा:", 
            ["मॅजिक कलर (Magic Color)", "कडक ब्लॅक & व्हाईट (B&W)", "मूळ कलर"],
            key="scanner_mode_select"
        )
        
        if st.button("🚀 मॅजिक स्कॅनिंग सुरू करा", type="primary", use_container_width=True, key="scan_btn"):
            with st.spinner("⏳ सिस्टीम फोटो सरळ करून सावली साफ करत आहे..."):
                try:
                    scanned_result = scan_and_straighten_image(original_image, mode=scan_mode)
                    
                    with col_scan2:
                        st.markdown("**🖨️ स्कॅन झालेला रिझल्ट:**")
                        st.image(scanned_result, use_container_width=True)
                        
                    img_byte_arr = io.BytesIO()
                    scanned_result.save(img_byte_arr, format='JPEG', quality=95)
                    
                    st.write("")
                    st.download_button(
                        label="📥 स्कॅन झालेली कडक इमेज डाऊनलोड करा",
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
