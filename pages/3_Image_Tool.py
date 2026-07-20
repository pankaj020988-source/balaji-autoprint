import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import io
import fitz  # PyMuPDF
import cv2
import numpy as np

# ==========================================
# 🌐 १. वाईड लेआउट कॉन्फिगरेशन (Full Page Width)
# ==========================================
st.set_page_config(
    page_title="बालाजी सायबर पॉइंट - इमेज टूल्स", 
    page_icon="📸", 
    layout="wide"  # 🎯 पूर्ण स्क्रीनचा वापर करण्यासाठी wide लेआउट
)

# ==========================================
# 🎨 २. सर्व टॅब्स एकाच वेळी दिसण्यासाठी प्रोफेशनल CSS
# ==========================================
st.markdown("""
    <style>
    /* मुख्य कन्टेनर मार्जिन कमी करणे */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* टॅब यादी पूर्ण स्क्रीनवर बसवणे */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        width: 100%;
        display: flex;
        justify-content: space-between;
    }
    
    /* प्रत्येक टॅबचे सुंदर आणि आकर्षक डिझाईन */
    button[data-baseweb="tab"] {
        flex: 1 !important;
        text-align: center !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        border-radius: 8px 8px 0px 0px !important;
        padding: 12px 8px !important;
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    /* हॉव्हर (माऊस नेल्यावर) इफेक्ट */
    button[data-baseweb="tab"]:hover {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
    }
    
    /* सिलेक्ट केलेल्या (Active) टॅबचा कडक रंग */
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0078D7 0%, #0056b3 100%) !important;
        color: #ffffff !important;
        border: 1px solid #0056b3 !important;
        box-shadow: 0px 4px 8px rgba(0, 120, 215, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #0078D7; font-weight: 800;'>📸 श्री बालाजी सायबर पॉईंट - डिजिटल इमेज पोर्टल्स</h2>", unsafe_allow_html=True)
st.success("🔓 **सर्व टूल्स unlocked आहेत!** कोणताही पासवर्ड न टाकता खालील सर्व टूल्स वापरा.")
st.write("---")

# ==========================================
# 🛠️ ३. चार मुख्य टूल्स (एकाच लाईनमध्ये बसणारे)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🖨️ आधार कटर (Precision Cut)", 
    "📸 पासपोर्ट फोटो मेकर (९ फोटो)", 
    "📝 फोटो-सही रीसायझर", 
    "📸 कॅम-स्कॅनर (Photo & PDF)"
])

# ------------------------------------------
# 🖨️ टॅब १: ओरिजिनल आधार कार्ड कटर
# ------------------------------------------
with tab1:
    st.markdown("<h4 style='color: #0056b3;'>🖨️ ओरिजिनल आधार कार्ड कटर (परफेक्ट काठोकाठ लेआउट)</h4>", unsafe_allow_html=True)
    st.info("💡 वरचा आणि खालचा एक्स्ट्रा भाग १-क्लिकमध्ये कट करा आणि काठोकाठ ४x६ प्रिंट काढा.")

    col_a1, col_a2 = st.columns([2, 1])
    with col_a1:
        pdf_file = st.file_uploader("ओरिजिनल आधार PDF फाईल अपलोड करा:", type=["pdf"], key="aadhaar_pdf_uploader")
    with col_a2:
        pdf_password = st.text_input("🔑 PDF पासवर्ड (असेल तर):", type="password", help="उदा. नाव + जन्मवर्ष", key="pdf_pass_input")

    if pdf_file is not None:
        st.write("📐 **अचूक काठोकाठ कटिंगसाठी सोपे कंट्रोल्स:**")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            top_trim = st.slider("✂️ वरचा एक्स्ट्रा भाग कापा (%)", 65.0, 78.0, 72.2, step=0.2, key="top_trim_slider")
        with col_c2:
            bottom_trim = st.slider("✂️ खालचा एक्स्ट्रा भाग कापा (%)", 88.0, 98.0, 92.5, step=0.2, key="bot_trim_slider")

        if st.button("🚀 ओरिजिनल आधार ४x६ लेआउट तयार करा", type="primary", use_container_width=True, key="btn_aadhaar_gen"):
            with st.spinner("⏳ नको असलेला भाग कट करून आधार कार्ड सेट होत आहे..."):
                try:
                    pdf_bytes = pdf_file.read()
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                    
                    if doc.is_encrypted:
                        if pdf_password:
                            auth_success = doc.authenticate(pdf_password)
                            if not auth_success:
                                st.error("❌ चुकीचा पासवर्ड! कृपया योग्य आधार PDF पासवर्ड प्रविष्ट करा.")
                                st.stop()
                        else:
                            st.warning("⚠️ ही PDF पासवर्ड प्रोटेक्टेड आहे. कृपया वर पासवर्ड टाका!")
                            st.stop()

                    page = doc[0]
                    pix = page.get_pixmap(dpi=400)
                    img_data = pix.tobytes("png")
                    full_img = Image.open(io.BytesIO(img_data)).convert("RGB")
                    
                    w, h = full_img.size
                    
                    t_pct = top_trim / 100.0
                    b_pct = bottom_trim / 100.0
                    
                    crop_front = full_img.crop((int(w * 0.078), int(h * t_pct), int(w * 0.492), int(h * b_pct)))
                    crop_back = full_img.crop((int(w * 0.508), int(h * t_pct), int(w * 0.922), int(h * b_pct)))
                    
                    PAPER_W, PAPER_HEIGHT = 1200, 1800
                    final_canvas = Image.new("RGB", (PAPER_W, PAPER_HEIGHT), "white")

                    card_w, card_h = 1050, 600
                    front_resized = crop_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    back_resized = crop_back.resize((card_w, card_h), Image.Resampling.LANCZOS)

                    front_bordered = ImageOps.expand(front_resized, border=5, fill='black')
                    back_bordered = ImageOps.expand(back_resized, border=5, fill='black')

                    paste_x = (PAPER_W - front_bordered.width) // 2
                    
                    final_canvas.paste(front_bordered, (paste_x, 180))
                    final_canvas.paste(back_bordered, (paste_x, 950))

                    st.success("✅ एक्स्ट्रा भाग पूर्ण कट झाला आहे! कार्ड काठोकाठ रेडी आहे.")
                    st.image(final_canvas, caption="Balaji_Aadhaar_Precision_Fit.png", use_container_width=True)
                    
                    id_buffer = io.BytesIO()
                    final_canvas.save(id_buffer, format="PNG", dpi=(300, 300))
                    
                    st.download_button(
                        label="📥 ४x६ आधार प्रिंट फाईल (PNG) डाऊनलोड करा", 
                        data=id_buffer.getvalue(), 
                        file_name="Balaji_Aadhaar_4x6_Perfect.png", 
                        mime="image/png", 
                        use_container_width=True,
                        key="dl_aadhaar_btn"
                    )
                except Exception as e:
                    st.error(f"❌ आधार कार्ड प्रक्रियेत अडचण आली: {e}")

# ------------------------------------------
# 📸 टॅब २: पासपोर्ट फोटो (९ फोटो)
# ------------------------------------------
with tab2:
    st.markdown("<h4 style='color: #0078D7;'>पासपोर्ट साईझ फोटो ऑटो-शीट जनरेटर (९ फोटो 4x6 / A4)</h4>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("ज्या फोटोचे पासपोर्ट साईझ बनवायचे आहेत तो फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="pp_uploader")

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="अपलोड केलेला मूळ फोटो", width=150)
        st.write("---")
        
        DPI = 300
        paper_option = st.radio(
            "कोणत्या साईझच्या paper वर फोटो सेट करायचे आहेत?",
            ("४x६ inch फोटो पेपर - ९ फोटो (9 Photos on 4x6)", "पूर्ण A4 सरकारी paper (Full A4 Sheet)"),
            key="paper_opt"
        )
        
        if st.button("🚀 पासपोर्ट साईझ फोटो शीट तयार करा", type="primary", use_container_width=True, key="btn_pp"):
            with st.spinner("⏳ कडक ९ फोटोंचे हाय-क्वालिटी लेआउट तयार होत आहे..."):
                try:
                    if "४x६" in paper_option:
                        canvas_w, canvas_h = int(4 * DPI), int(6 * DPI)
                        cols, rows = 3, 3
                        file_suffix = "4x6_9_Photos"
                        
                        id_w, id_h = 350, 450
                        resized_id = ImageOps.fit(img, (id_w, id_h), Image.Resampling.LANCZOS)
                        resized_id = ImageOps.expand(resized_id, border=3, fill='black')
                        
                        sheet = Image.new("RGB", (canvas_w, canvas_h), "white")
                        
                        margin_x = (canvas_w - (cols * resized_id.width)) // (cols + 1)
                        margin_y = (canvas_h - (rows * resized_id.height)) // (rows + 1)
                        
                        for r in range(rows):
                            for c in range(cols):
                                x = margin_x + c * (resized_id.width + margin_x)
                                y = margin_y + r * (resized_id.height + margin_y)
                                sheet.paste(resized_id, (x, y))
                    else:
                        canvas_w, canvas_h = int(8.27 * DPI), int(11.69 * DPI)
                        file_suffix = "A4_Sheet"
                        id_w, id_h = int(3.5 / 2.54 * DPI), int(4.5 / 2.54 * DPI)
                        
                        resized_id = ImageOps.fit(img, (id_w, id_h), Image.Resampling.LANCZOS)
                        resized_id = ImageOps.expand(resized_id, border=3, fill='black')
                        
                        sheet = Image.new("RGB", (canvas_w, canvas_h), "white")
                        margin = 25
                        for y in range(margin, canvas_h - id_h, id_h + margin):
                            for x in range(margin, canvas_w - id_w, id_w + margin):
                                sheet.paste(resized_id, (x, y))
                    
                    buffer = io.BytesIO()
                    sheet.save(buffer, format="PNG", dpi=(DPI, DPI))
                    buffer.seek(0)
                    
                    st.success(f"✅ तुमचे {9 if '४x६' in paper_option else 'A4'} पासपोर्ट फोटो शीट तयार झाले आहे!")
                    st.image(sheet, caption="⚙️ ९ फोटो प्रिंट प्रिव्ह्यू", use_container_width=True)
                    
                    st.download_button(
                        label="📥 तयार झालेली HD फोटो शीट (PNG) डाऊनलोड करा",
                        data=buffer,
                        file_name=f"Balaji_Passport_{file_suffix}.png",
                        mime="image/png",
                        use_container_width=True,
                        key="dl_pp_btn"
                    )
                except Exception as e:
                    st.error(f"❌ चूक झाली: {e}")

# ------------------------------------------
# 📝 टॅब ३: सरकारी फॉर्म रीसायझर
# ------------------------------------------
with tab3:
    st.markdown("<h4 style='color: #4CAF50;'>सरकारी फॉर्म - फोटो व सही कॉम्प्रेसर टूल</h4>", unsafe_allow_html=True)
    tool_mode = st.radio("तुम्हाला काय रीसाईझ करायचे आहे?", ("ग्राहक फोटो (Photo - 20KB)", "ग्राहक सही (Signature - 10KB)"), key="mode_form")
    uploaded_file = st.file_uploader("तुमची फाईल (Photo/Sign) इथे अपलोड करा:", type=["jpg", "jpeg", "png"], key="form_uploader")

    if uploaded_file is not None:
        raw_img = Image.open(uploaded_file).convert("RGB")
        st.image(raw_img, caption="अपलोड केलेली मूळ फाईल", width=150)
        
        t_width, t_height, max_kb, label = (160, 200, 20, "Photo") if "Photo" in tool_mode else (256, 64, 10, "Signature")
            
        if st.button(f"⚡ {label} रीसाईझ आणि कॉम्प्रेस करा", type="primary", use_container_width=True, key="btn_resize_gen"):
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
                        use_container_width=True,
                        key="dl_form_btn"
                    )
                except Exception as e:
                    st.error(f"❌ चूक झाली: {e}")

# ------------------------------------------
# 📸 टॅब ४: कॅम-स्कॅनर (Photo + PDF Support)
# ------------------------------------------
with tab4:
    st.markdown("<h4 style='color: #E65100;'>📸 बालाजी सुपर-फास्ट कॅम-स्कॅनर</h4>", unsafe_allow_html=True)
    st.write("झटपट क्रॉप आणि सरळ करण्यासाठी खालील बटनांचा वापर करा.")
    
    if "c_left" not in st.session_state: st.session_state.c_left = 0
    if "c_right" not in st.session_state: st.session_state.c_right = 0
    if "c_top" not in st.session_state: st.session_state.c_top = 0
    if "c_bottom" not in st.session_state: st.session_state.c_bottom = 0
    if "r_angle" not in st.session_state: st.session_state.r_angle = 0

    scan_file = st.file_uploader("स्कॅन करण्यासाठी डॉक्युमेंटचा फोटो किंवा PDF फाईल अपलोड करा (JPG/PNG/PDF):", type=["jpg", "jpeg", "png", "pdf"], key="scanner_upload")

    if scan_file is not None:
        try:
            if scan_file.name.lower().endswith(".pdf"):
                pdf_bytes = scan_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                page = doc[0]
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                original_image = Image.open(io.BytesIO(img_data)).convert("RGB")
            else:
                original_image = Image.open(scan_file).convert("RGB")
                
            st.markdown("##### ⚡ वन-क्लिक FAST कंट्रोल्स:")
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

            scan_mode = st.selectbox(
                "🎨 कलर मोड निवडा:", 
                ["मॅजिक कलर (Magic Color)", "कडक ब्लॅक & व्हाईट (B&W)", "मूळ कलर"],
                key="scanner_mode_select"
            )
            
            if st.session_state.r_angle != 0:
                if st.session_state.r_angle == 90: working_img = original_image.transpose(Image.ROTATE_270)
                elif st.session_state.r_angle == 180: working_img = original_image.transpose(Image.ROTATE_180)
                elif st.session_state.r_angle == 270: working_img = original_image.transpose(Image.ROTATE_90)
                else: working_img = original_image
            else:
                working_img = original_image

            w, h = working_img.size
            l_px = int(w * (st.session_state.c_left / 100))
            r_px = w - int(w * (st.session_state.c_right / 100))
            t_px = int(h * (st.session_state.c_top / 100))
            b_px = h - int(h * (st.session_state.c_bottom / 100))

            if r_px > l_px and b_px > t_px:
                working_img = working_img.crop((l_px, t_px, r_px, b_px))

            st.write("---")
            st.markdown("##### 📐 लाईव्ह क्रॉप प्रिव्ह्यू:")
            st.image(working_img, caption="सध्याचा डॉक्युमेंट आकार", use_container_width=True)
            st.write("---")
            
            if st.button("🚀 ३. मॅजिक स्कॅनिंग फिनिश करा", type="primary", use_container_width=True, key="scan_btn"):
                with st.spinner("⏳ सिस्टीम सावली साफ करत आहे..."):
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
                        
                        st.download_button(
                            label="📥 स्कॅन झालेली इमेज डाऊनलोड करा",
                            data=img_byte_arr.getvalue(),
                            file_name="Balaji_Perfect_Scan.jpg",
                            mime="image/jpeg",
                            use_container_width=True,
                            key="scan_dl_btn"
                        )
                    except Exception as e:
                        st.error(f"❌ चूक झाली: {e}")
        except Exception as e:
            st.error(f"❌ फाईल ओपन करताना चूक झाली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 13px; color: #666;'>📍 श्री बालाजी सायबर पॉईंट, माणगाव, रायगड | Designed for Fast Cyber Operations</p>", unsafe_allow_html=True)
