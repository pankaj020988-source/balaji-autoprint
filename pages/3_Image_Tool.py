import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import io
import fitz  # PyMuPDF
import cv2
import numpy as np

# ==========================================
# 🌐 १. वाईड लेआउट कॉन्फिगरेशन
# ==========================================
st.set_page_config(
    page_title="बालाजी सायबर पॉइंट - डिजिटल टूलकिट", 
    page_icon="🖥️", 
    layout="wide"
)

# ==========================================
# 🎨 २. कॉर्पोरेट व्यावसायिक UI डिझाईन (CSS Fix)
# ==========================================
st.markdown("""
    <style>
    /* वरच्या बाजूला पुरेशी जागा ठेवल्याने हेडिंग कट होणार नाही */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* मुख्य हेडिंग स्टायलिंग */
    .main-header {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        text-align: center;
        margin-bottom: 25px !important;
        margin-top: 10px !important;
        letter-spacing: 0.5px;
        line-height: 1.4 !important;
    }
    
    /* टॅब लेआउट अचूक आणि समान बसवणे */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    
    /* व्यावसायिक बटण स्वरूप */
    button[data-baseweb="tab"] {
        flex: 1 !important;
        text-align: center !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        padding: 12px 6px !important;
        background-color: #F8FAFC !important;
        color: #334155 !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease-in-out;
        white-space: nowrap !important;
    }
    
    button[data-baseweb="tab"]:hover {
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
        box-shadow: 0px 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# मुख्य व्यावसायिक शीर्षक
st.markdown("<div class='main-header'>बालाजी सायबर पॉईंट - इमेज प्रोसेसिंग टूलकिट</div>", unsafe_allow_html=True)

# ==========================================
# 🛠️ ३. मुख्य टूल्स (टॅब्स)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "आधार कटर (4x6 Layout)", 
    "पासपोर्ट फोटो मेकर (9 Photos)", 
    "फॉर्म फोटो व सही रीसायझर", 
    "डॉक्युमेंट स्कॅनर (Doc/PDF)"
])

# ------------------------------------------
# 🖨️ टॅब १: आधार कार्ड कटर
# ------------------------------------------
with tab1:
    col_a1, col_a2 = st.columns([2, 1])
    with col_a1:
        pdf_file = st.file_uploader("आधार PDF अपलोड करा:", type=["pdf"], key="aadhaar_pdf_uploader")
    with col_a2:
        pdf_password = st.text_input("PDF पासवर्ड (असेल तर):", type="password", key="pdf_pass_input")

    if pdf_file is not None:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            top_trim = st.slider("वरचा भाग ट्रीम (%)", 65.0, 78.0, 72.2, step=0.2, key="top_trim_slider")
        with col_c2:
            bottom_trim = st.slider("खालचा भाग ट्रीम (%)", 88.0, 98.0, 92.5, step=0.2, key="bot_trim_slider")

        if st.button("4x6 लेआउट जनरेट करा", type="primary", use_container_width=True, key="btn_aadhaar_gen"):
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

                    st.image(final_canvas, caption="4x6 Print Preview", use_container_width=True)
                    
                    id_buffer = io.BytesIO()
                    final_canvas.save(id_buffer, format="PNG", dpi=(300, 300))
                    
                    st.download_button(
                        label="4x6 PNG डाऊनलोड करा", 
                        data=id_buffer.getvalue(), 
                        file_name="Aadhaar_4x6_Layout.png", 
                        mime="image/png", 
                        use_container_width=True,
                        key="dl_aadhaar_btn"
                    )
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# ------------------------------------------
# 📸 टॅब २: पासपोर्ट फोटो जनरेटर
# ------------------------------------------
with tab2:
    uploaded_image = st.file_uploader("मूळ फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="pp_uploader")

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="अपलोड फाईल", width=120)
        
        DPI = 300
        paper_option = st.radio(
            "पेपर साईझ निवडा:",
            ("4x6 Paper - 9 Photos", "Full A4 Sheet"),
            key="paper_opt",
            horizontal=True
        )
        
        if st.button("पासपोर्ट सीट जनरेट करा", type="primary", use_container_width=True, key="btn_pp"):
            with st.spinner("प्रक्रिया सुरू आहे..."):
                try:
                    if "4x6" in paper_option:
                        canvas_w, canvas_h = int(4 * DPI), int(6 * DPI)
                        cols, rows = 3, 3
                        file_suffix = "4x6_9Photos"
                        
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
                    
                    st.image(sheet, caption="Print Preview", use_container_width=True)
                    
                    st.download_button(
                        label="फोटो शीट डाऊनलोड करा (PNG)",
                        data=buffer,
                        file_name=f"Passport_Sheet_{file_suffix}.png",
                        mime="image/png",
                        use_container_width=True,
                        key="dl_pp_btn"
                    )
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# ------------------------------------------
# 📝 टॅब ३: फोटो व सही रीसायझर
# ------------------------------------------
with tab3:
    tool_mode = st.radio("प्रकार निवडा:", ("फोटो (Max 20KB)", "सही (Max 10KB)"), key="mode_form", horizontal=True)
    uploaded_file = st.file_uploader("इमेज अपलोड करा:", type=["jpg", "jpeg", "png"], key="form_uploader")

    if uploaded_file is not None:
        raw_img = Image.open(uploaded_file).convert("RGB")
        st.image(raw_img, caption="अपलोड फाईल", width=120)
        
        t_width, t_height, max_kb, label = (160, 200, 20, "Photo") if "फोटो" in tool_mode else (256, 64, 10, "Signature")
            
        if st.button("कॉम्प्रेश करा", type="primary", use_container_width=True, key="btn_resize_gen"):
            with st.spinner("प्रक्रिया सुरू आहे..."):
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
                    
                    st.success(f"अंतिम साईझ: {final_size_kb} KB")
                    st.image(final_bytes, caption=f"रीसाईझ {label}")
                    
                    st.download_button(
                        label="डाऊनलोड करा (JPG)",
                        data=final_bytes,
                        file_name=f"Resized_{label.lower()}.jpg",
                        mime="image/jpeg",
                        use_container_width=True,
                        key="dl_form_btn"
                    )
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# ------------------------------------------
# 📸 टॅब ४: डॉक्युमेंट स्कॅनर
# ------------------------------------------
with tab4:
    if "c_left" not in st.session_state: st.session_state.c_left = 0
    if "c_right" not in st.session_state: st.session_state.c_right = 0
    if "c_top" not in st.session_state: st.session_state.c_top = 0
    if "c_bottom" not in st.session_state: st.session_state.c_bottom = 0
    if "r_angle" not in st.session_state: st.session_state.r_angle = 0

    scan_file = st.file_uploader("इमेज किंवा PDF अपलोड करा:", type=["jpg", "jpeg", "png", "pdf"], key="scanner_upload")

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
                
            col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
            with col_b1:
                if st.button("डावीकडून कापा", use_container_width=True): st.session_state.c_left += 5
            with col_b2:
                if st.button("उजवीकडून कापा", use_container_width=True): st.session_state.c_right += 5
            with col_b3:
                if st.button("वरून कापा", use_container_width=True): st.session_state.c_top += 5
            with col_b4:
                if st.button("खालून कापा", use_container_width=True): st.session_state.c_bottom += 5
            with col_b5:
                if st.button("90° फिरवा", use_container_width=True): st.session_state.r_angle = (st.session_state.r_angle + 90) % 360

            if st.button("रिसेट करा", type="secondary", use_container_width=True):
                st.session_state.c_left = 0
                st.session_state.c_right = 0
                st.session_state.c_top = 0
                st.session_state.c_bottom = 0
                st.session_state.r_angle = 0

            scan_mode = st.selectbox(
                "कलर मोड:", 
                ["Magic Color", "B&W", "Original"],
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

            st.image(working_img, caption="Preview", use_container_width=True)
            
            if st.button("स्कॅनिंग पूर्ण करा", type="primary", use_container_width=True, key="scan_btn"):
                with st.spinner("प्रक्रिया सुरू आहे..."):
                    try:
                        img_np = np.array(working_img.convert('RGB'))
                        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                        
                        if scan_mode == "B&W":
                            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                            scanned = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 12)
                            final_res = Image.fromarray(scanned)
                        elif scan_mode == "Magic Color":
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
                        
                        st.image(final_res, caption="Scanned Result", use_container_width=True)
                        
                        img_byte_arr = io.BytesIO()
                        final_res.save(img_byte_arr, format='JPEG', quality=95)
                        
                        st.download_button(
                            label="इमेज डाऊनलोड करा",
                            data=img_byte_arr.getvalue(),
                            file_name="Scanned_Document.jpg",
                            mime="image/jpeg",
                            use_container_width=True,
                            key="scan_dl_btn"
                        )
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")
        except Exception as e:
            st.error(f"त्रुटी: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #94A3B8;'>श्री बालाजी सायबर पॉईंट, माणगाव, रायगड</p>", unsafe_allow_html=True)
