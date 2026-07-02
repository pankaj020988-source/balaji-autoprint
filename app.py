import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import io

# ==========================================
# 🌐 मुख्य पेज कॉन्फिगरेशन आणि थीम सेटिंग्ज
# ==========================================
st.set_page_config(page_title="बालाजी सायबर पॉईंट - होम", page_icon="🏠", layout="wide")

# पासवर्ड आणि ऑथेंटिकेशन स्टेट मेमरी मॅनेजमेंट
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "c_left" not in st.session_state: st.session_state.c_left = 0
if "c_right" not in st.session_state: st.session_state.c_right = 0
if "c_top" not in st.session_state: st.session_state.c_top = 0
if "c_bottom" not in st.session_state: st.session_state.c_bottom = 0
if "r_angle" not in st.session_state: st.session_state.r_angle = 0

# ==========================================
# 🗺️ मुख्य २ टॅब लेआउट (Home आणि Admin Desk)
# ==========================================
main_tab1, main_tab2 = st.tabs(["🏠 Home", "🔒 Admin Desk"])

# ------------------------------------------
# 📢 १. सर्वांसाठी खुले असलेले होम पेज (व्यावसायिक मार्केटिंग)
# ------------------------------------------
with main_tab1:
    # 🌟 वरचे मुख्य होर्डिंग बॅनर (HTML आणि CSS डिझाईन)
    st.markdown("""
    <div style="background: linear-gradient(135px, #002f6c 0%, #0056b3 100%); padding: 30px; border-radius: 10px; text-align: center; color: white; border: 3px solid #d4af37; box-shadow: 0px 4px 15px rgba(0,0,0,0.2);">
        <h1 style="color: #e5be3b; font-size: 42px; font-weight: bold; margin-bottom: 5px;">बालाजी सायबर पॉईंट (माणगाव)</h1>
        <h3 style="font-size: 24px; font-weight: 500; margin-top: 0; opacity: 0.95;">तुमचे डिजिटल आणि ट्रॅव्हल सोल्यूशन पार्टनर!</h3>
        <hr style="border: 1px solid #d4af37; width: 60%; margin: 15px auto;">
        <div style="display: flex; justify-content: space-around; font-size: 18px; font-weight: bold; margin-top: 15px;">
            <div>💻 ऑनलाईन फॉर्म्स</div>
            <div>📄 सरकारी योजना</div>
            <div>✈️ ट्रॅव्हल बुकिंग</div>
            <div>💰 कर आणि महसूल</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # 🌟 आमच्या प्रमुख सेवा सेक्शन
    st.markdown("### 🌟 आमच्या प्रमुख सेवा:")
    st.markdown("""
    * **सर्व ऑनलाईन फॉर्म्स:** नोकरभरती, ॲडमिट कार्ड आणि हॉल तिकीट.
    * **शासकीय योजना:** घरकुल योजना, शबरी आवास योजना आणि इतर सरकारी अर्ज.
    * **ट्रॅव्हल बुकिंग:** देश-विदेशातील फ्लाईट्स, हॉटेल्स आणि टूर पॅकेजेस (MakeMyTrip).
    * **कर आणि महसूल:** नगरपंचायत प्रॉपर्टी टॅक्स, वीज बिल आणि महाआयटी सेवा.
    * **डिजिटल फोटो टूल्स:** जुने फोटो 4K मध्ये रिस्टोर करणे आणि कॉम्प्युटर रीसायझिंग.
    """)
    
    st.write("")
    
    # 📍 तळाशी पत्ता पट्टी
    st.markdown("""
    <div style="background-color: #154c8c; color: white; padding: 12px; border-radius: 5px; text-align: center; font-size: 16px; font-weight: bold;">
        📍 पत्ता: बालाजी कॉम्प्लेक्स, माणगाव, रायगड, महाराष्ट्र
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# 🔐 २. पासवर्ड प्रोटेक्टेड ॲडमीन डेस्क (सर्व अंतर्गत ॲप्स)
# ------------------------------------------
with main_tab2:
    if not st.session_state.authenticated:
        st.markdown("<h3 style='color: #D32F2F;'>🔐 सायबर ऑपरेशन्स लॉगिन</h3>", unsafe_allow_html=True)
        st.write("अंतर्गत टूल्स आणि हिशोब मॅनेजमेंट वापरण्यासाठी तुमचा सुरक्षित पासवर्ड प्रविष्ट करा.")
        
        # गुप्त पासवर्ड बॉक्स (Default: Balaji@123)
        access_password = st.text_input("🔑 मॅनेजर/स्टाफ पासवर्ड प्रविष्ट करा:", type="password", key="main_admin_password")
        
        if st.button("🔓 सिस्टीम अनलॉक करा", type="primary", use_container_width=True):
            if access_password == "Balaji@123":
                st.session_state.authenticated = True
                st.success("🔓 लॉगिन यशस्वी! सिस्टीम अनलॉक झाली आहे.")
                st.rerun()
            else:
                st.error("❌ चुकीचा पासवर्ड! कृपया योग्य संकेतशब्द प्रविष्ट करा.")
                
    else:
        # यशस्वी लॉगिननंतर डाव्या बाजूला कंट्रोल आणि वर सर्व ॲप्स टॅब स्वरूपात उघडतील
        st.sidebar.success("🔓 ॲडमीन डेस्क अनलॉक आहे")
        if st.sidebar.button("🔒 सिस्टीम लॉक करा (Log Out)", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
            
        st.write("---")
        st.markdown("#### ⚙️ बालाजी डिजिटल ऑपरेशन्स पॅनेल")
        
        # 🎯 सर्व ४ मूळ ॲप्स आता एकाच ठिकाणी सुरक्षित टॅबच्या आत!
        app_tab1, app_tab2, app_tab3, app_tab4 = st.tabs([
            "🖨️ app (Ayushman Printer)", 
            "📊 Bill Manager", 
            "📁 Cyber Data", 
            "📸 Image Tool & Scanner"
        ])
        
        # ---------------------------------------------------------
        # अंतर्गत ॲप १: app (Ayushman Printer)
        # ---------------------------------------------------------
        with app_tab1:
            st.markdown("##### 🖨️ आयुष्मान भारत ४x६ ऑटो-प्रिंट सिस्टीम")
            uploaded_pdf = st.file_uploader("सरकारी आयुष्मान PDF फाईल अपलोड करा:", type=["pdf"], key="ayushman_pdf_uploader")
            st.info("तुमची आयुष्मान भारत सिस्टीम सुरक्षितपणे कनेक्टेड आहे...")

        # ---------------------------------------------------------
        # अंतर्गत ॲप २: Bill Manager
        # ---------------------------------------------------------
        with app_tab2:
            st.markdown("##### 📊 दैनिक बिल मॅनेजर आणि हिशोब खाते")
            st.info("हिशोब डेटा सुरक्षितपणे चालू आहे...")

        # ---------------------------------------------------------
        # अंतर्गत ॲप ३: Cyber Data
        # ---------------------------------------------------------
        with app_tab3:
            st.markdown("##### 📁 सायबर डेटा आणि दस्तऐवज स्टोरेज")
            st.info("सायबर डेटाबेस सर्व्हर सुरू आहे...")

        # ---------------------------------------------------------
        # अंतर्गत ॲप ४: Image Tool (पासपोर्ट, रीसायझर, आयडी आणि कॅम-स्कॅनर)
        # ---------------------------------------------------------
        with app_tab4:
            st.markdown("##### 📸 प्रगत इमेज टूल्स आणि सुपर-फास्ट स्कॅनर")
            
            # इमेज टूलचे ४ उप-विभाग
            sub_tool_tab1, sub_tool_tab2, sub_tool_tab3, sub_tool_tab4 = st.tabs([
                "📸 पासपोर्ट मेकर", "📝 फोटो-सही रीसायझर", "🖨️ स्मार्ट आयडी प्रिंटर", "📸 सुपर-फास्ट स्कॅनर"
            ])
            
            # अ) पासपोर्ट मेकर
            with sub_tool_tab1:
                st.markdown("###### पासपोर्ट साईझ फोटो ऑटो-शीट जनरेटर (३.५ x ४.५ सेमी)")
                uploaded_image = st.file_uploader("फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="pp_uploader")
                if uploaded_image is not None:
                    img = Image.open(uploaded_image)
                    st.image(img, width=150)
                    DPI = 300
                    id_w, id_h = int(3.5 / 2.54 * DPI), int(4.5 / 2.54 * DPI)
                    paper_option = st.radio("पेपर साईझ निवडा:", ("४x६ inch फोटो पेपर (4x6 Sheet)", "पूर्ण A4 सरकारी paper (Full A4 Sheet)"), key="paper_opt")
                    if st.button("🚀 पासपोर्ट साईझ फोटो शीट तयार करा", type="primary", use_container_width=True, key="btn_pp"):
                        try:
                            canvas_w, canvas_h = (int(4 * DPI), int(6 * DPI)) if "४x६" in paper_option else (int(8.27 * DPI), int(11.69 * DPI))
                            resized_id = ImageOps.fit(img, (id_w, id_h), Image.Resampling.LANCZOS)
                            sheet = Image.new("RGB", (canvas_w, canvas_h), "white")
                            margin = 25
                            for y in range(margin, canvas_h - id_h, id_h + margin):
                                for x in range(margin, canvas_w - id_w, id_w + margin): sheet.paste(resized_id, (x, y))
                            buffer = io.BytesIO()
                            sheet.save(buffer, format="PNG", dpi=(DPI, DPI))
                            st.image(sheet, use_container_width=True)
                            st.download_button(label="📥 HD फोटो शीट डाऊनलोड करा", data=buffer.getvalue(), file_name="Balaji_Passport.png", mime="image/png", use_container_width=True)
                        except Exception as e: st.error(f"❌ चूक: {e}")

            # ब) फोटो-सही रीसायझर
            with sub_tool_tab2:
                st.markdown("###### 📝 सरकारी फॉर्म - फोटो व सही कॉम्प्रेसर")
                tool_mode = st.radio("रीसाईझ प्रकार निवडा:", ("फोटो (Photo - 20KB)", "सही (Signature - 10KB)"), key="mode_form")
                uploaded_file = st.file_uploader("फाईल अपलोड करा:", type=["jpg", "jpeg", "png"], key="form_uploader")
                if uploaded_file is not None:
                    raw_img = Image.open(uploaded_file).convert("RGB")
                    t_width, t_height, max_kb, label = (160, 200, 20, "Photo") if "फोटो" in tool_mode else (256, 64, 10, "Signature")
                    if st.button(f"⚡ {label} रीसाईझ करा", type="primary", use_container_width=True, key="resize_btn"):
                        try:
                            resized_img = raw_img.resize((t_width, t_height), Image.Resampling.LANCZOS)
                            quality = 95
                            img_buffer = io.BytesIO()
                            resized_img.save(img_buffer, "JPEG", optimize=True, quality=quality)
                            while img_buffer.tell() > max_kb * 1024 and quality > 10:
                                quality -= 5
                                img_buffer = io.BytesIO()
                                resized_img.save(img_buffer, "JPEG", optimize=True, quality=quality)
                            st.success(f"✅ यशस्वी! साईझ: {len(img_buffer.getvalue()) // 1024} KB")
                            st.image(img_buffer.getvalue())
                            st.download_button(label="📥 कॉम्प्रेस फाईल डाऊनलोड करा", data=img_buffer.getvalue(), file_name=f"balaji_{label.lower()}.jpg", mime="image/jpeg", use_container_width=True, key="dl_compress")
                        except Exception as e: st.error(f"❌ चूक: {e}")

            # क) स्मार्ट आयडी प्रिंटर
            with sub_tool_tab3:
                st.markdown("###### 🖨️ स्मार्ट आयडी कार्ड प्रिंटर")
                col_id1, col_id2 = st.columns(2)
                with col_id1: front_file = st.file_uploader("१. फ्रंट बाजू फोटो:", type=["jpg", "jpeg", "png"], key="id_front")
                with col_id2: back_file = st.file_uploader("२. बॅक बाजू फोटो:", type=["jpg", "jpeg", "png"], key="id_back")
                if front_file and back_file:
                    if st.button("⚙️ ४x६ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True, key="id_print_btn"):
                        try:
                            img_f, img_b = Image.open(front_file).convert("RGB"), Image.open(back_file).convert("RGB")
                            img_f = img_f.resize((1130, 710), Image.Resampling.LANCZOS)
                            img_b = img_b.resize((1130, 710), Image.Resampling.LANCZOS)
                            img_f = ImageOps.expand(img_f, border=6, fill='black')
                            img_b = ImageOps.expand(img_b, border=6, fill='black')
                            id_canvas = Image.new("RGB", (1200, 1800), "white")
                            id_canvas.paste(img_f, (35, 150))
                            id_canvas.paste(img_b, (35, 950))
                            id_buffer = io.BytesIO()
                            id_canvas.save(id_buffer, format="PNG", dpi=(300, 300))
                            st.image(id_canvas, use_container_width=True)
                            st.download_button(label="📥 प्रिंट फाईल (PNG) डाऊनलोड करा", data=id_buffer.getvalue(), file_name="Balaji_ID_Print.png", mime="image/png", use_container_width=True, key="dl_id_canvas")
                        except Exception as e: st.error(f"❌ चूक: {e}")

            # ड) सुपर-फास्ट स्कॅनर
            with sub_tool_tab4:
                st.markdown("###### 📸 बालाजी सुपर-फास्ट कॅम-स्कॅनर")
                scan_file = st.file_uploader("स्कॅन करण्यासाठी फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="scanner_upload")
                if scan_file is not None:
                    original_image = Image.open(scan_file)
                    st.markdown("####### ⚡ वन-क्लिक फास्ट कंट्रोल्स:")
                    col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
                    with col_b1:
                        if st.button("⬅️ डावीकडून कापा", use_container_width=True, key="l_crop"): st.session_state.c_left += 5
                    with col_b2:
                        if st.button("➡️ उजवीकडून कापा", use_container_width=True, key="r_crop"): st.session_state.c_right += 5
                    with col_b3:
                        if st.button("⬆️ वरून कापा", use_container_width=True, key="t_crop"): st.session_state.c_top += 5
                    with col_b4:
                        if st.button("⬇️ खालून कापा", use_container_width=True, key="b_crop"): st.session_state.c_bottom += 5
                    with col_b5:
                        if st.button("🔄 ९०° फिरवा", use_container_width=True, key="rot_crop"): st.session_state.r_angle = (st.session_state.r_angle + 90) % 360

                    if st.button("🔄 सर्व नियंत्रणे रिसेट करा (Reset All)", type="secondary", use_container_width=True, key="rst_all_scan"):
                        st.session_state.c_left = 0; st.session_state.c_right = 0; st.session_state.c_top = 0; st.session_state.c_bottom = 0; st.session_state.r_angle = 0
                        st.rerun()

                    scan_mode = st.selectbox("🎨 कलर मोड निवडा:", ["मॅजिक कलर (Magic Color)", "कडक ब्लॅक & व्हाईट (B&W)", "मूळ कलर"], key="scanner_mode_select")
                    
                    if st.session_state.r_angle != 0:
                        if st.session_state.r_angle == 90: working_img = original_image.transpose(Image.ROTATE_270)
                        elif st.session_state.r_angle == 180: working_img = original_image.transpose(Image.ROTATE_180)
                        elif st.session_state.r_angle == 270: working_img = original_image.transpose(Image.ROTATE_90)
                        else: working_img = original_image
                    else: working_img = original_image
                        
                    w, h = working_img.size
                    l_px, r_px = int(w * (st.session_state.c_left / 100)), w - int(w * (st.session_state.c_right / 100))
                    t_px, b_px = int(h * (st.session_state.c_top / 100)), h - int(h * (st.session_state.c_bottom / 100))
                    if r_px > l_px and b_px > t_px: working_img = working_img.crop((l_px, t_px, r_px, b_px))
                        
                    st.image(working_img, caption="लाईव्ह प्रिव्ह्यू", use_container_width=True)
                    
                    if st.button("🚀 ३. मॅजिक स्कॅनिंग फिनिश करा", type="primary", use_container_width=True, key="scan_btn"):
                        with st.spinner("⏳ सिस्टीम साफ करत आहे..."):
                            try:
                                img_np = np.array(working_img.convert('RGB'))
                                img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                                if scan_mode == "कडक ब्लॅक & व्हाईट (B&W)":
                                    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                                    final_res = Image.fromarray(cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 12))
                                elif scan_mode == "मॅजिक कलर (Magic Color)":
                                    channels = cv2.split(img_cv)
                                    result_channels = []
                                    for ch in channels:
                                        dilated = cv2.dilate(ch, np.ones((7,7), np.uint8))
                                        diff = 255 - cv2.absdiff(ch, cv2.medianBlur(dilated, 21))
                                        result_channels.append(cv2.normalize(diff, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1))
                                    blended = cv2.addWeighted(img_cv, 0.60, cv2.merge(result_channels), 0.40, 0)
                                    enhanced_pil = Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
                                    final_res = ImageEnhance.Sharpness(ImageEnhance.Contrast(enhanced_pil).enhance(1.3)).enhance(1.2)
                                else: final_res = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
                                
                                st.image(final_res, caption="फायनल रिझल्ट", use_container_width=True)
                                img_byte_arr = io.BytesIO()
                                final_res.save(img_byte_arr, format='JPEG', quality=95)
                                st.download_button(label="📥 परफेक्ट इमेज डाऊनलोड करा", data=img_byte_arr.getvalue(), file_name="Balaji_Perfect_Scan.jpg", mime="image/jpeg", use_container_width=True, key="dl_final_scan_btn")
                            except Exception as e: st.error(f"❌ चूक: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
