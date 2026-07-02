import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import io

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - इमेज टूल्स", page_icon="📸", layout="centered")

# पासवर्ड स्टेट मेमरी मॅनेजमेंट
if "tools_authenticated" not in st.session_state:
    st.session_state.tools_authenticated = False

st.markdown("<h2 style='text-align: center; color: #0078D7;'>📸 श्री बालाजी सायबर पॉईंट - इमेज पोर्टल्स</h2>", unsafe_allow_html=True)
st.write("---")

# 🎯 मुख्य दोन विभाग (टॅब्स): होम पेज सर्वांसाठी खुले, सायबर टूल्स पासवर्डच्या मागे लॉक
main_tab1, main_tab2 = st.tabs([
    "🏠 होम पेज (जाहिरात व सुविधा)", 
    "🔐 सायबर टूल्स पोर्टल (Locked)"
])

# ==========================================
# 📢 विभाग १: सर्वांसाठी खुले असलेले होम पेज (मार्केटिंग)
# ==========================================
with main_tab1:
    st.markdown("<h3 style='text-align: center; color: #28a745;'>📍 श्री बालाजी सायबर पॉईंट, माणगाव</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: #6c757d;'>तुमचे डिजिटल काम, आमची जबाबदारी!</h5>", unsafe_allow_html=True)
    st.write("---")
    
    # 📌 नवीन भरती आणि सरकारी जाहिराती सेक्शन
    st.markdown("#### 📢 नवीन सरकारी नोकर भरती व जाहिराती")
    col_ads1, col_ads2 = st.columns(2)
    
    with col_ads1:
        st.info("📌 **महाभरती २०२६:** विविध सरकारी विभागांमध्ये नवीन जागा सुटल्या आहेत. ऑनलाईन फॉर्म भरण्यासाठी आजच दुकानात आवश्यक कागदपत्रे घेऊन या.")
    with col_ads2:
        st.warning("📌 **नवीन परीक्षा प्रवेशपत्र (Admit Card):** चालू महिन्यातील स्पर्धा परीक्षांचे हॉल तिकीट आणि सरकारी परीक्षांचे प्रवेशपत्र डाऊनलोड करणे सुरू आहे.")
        
    st.write("---")
    
    # 🛠️ आमच्याकडे उपलब्ध असलेल्या प्रमुख सुविधा
    st.markdown("#### 🛠️ आमच्याकडे उपलब्ध असलेल्या कडक सुविधा:")
    
    col_serv1, col_serv2 = st.columns(2)
    with col_serv1:
        st.markdown("""
        **🖨️ कडक कार्ड प्रिंटिंग व स्कॅनर सेवा**
        * आयुष्मान भारत कार्ड ४x६ ऑटो-फिट प्रिंट
        * स्मार्ट आयडी कार्ड प्रिंटर (पॅन/वोटर आयडी)
        * डिजिटल दस्तऐवज आणि ७/१२ उतारा कलर प्रिंटिंग
        * मोबाईलच्या फोटोंना कडक साफ करणारे कॅम-स्कॅनर टूल
        """)
    with col_serv2:
        st.markdown("""
        **📝 ऑनलाईन फॉर्म आणि ट्रॅव्हल बुकिंग**
        * सर्व प्रकारच्या सरकारी व भरती परीक्षांचे ऑनलाईन फॉर्म्स
        * रेशन कार्ड, उत्पन्न दाखला व नवीन अर्ज नोंदणी
        * देश-विदेशातील फ्लाईट्स, रेल्वे आणि हॉटेल बुकिंग
        * जुन्या व खराब फोटोंचे कडक डिजिटल पुनरुज्जीवन
        """)
        
    st.write("---")
    st.markdown("<p style='text-align: center; font-size: 13px; color: #666;'>📍 पत्ता: बालाजी कॉम्प्लेक्स, माणगाव, रायगड, महाराष्ट्र</p>", unsafe_allow_html=True)

# ==========================================
# 🔐 विभाग २: पासवर्ड प्रोटेक्टेड सायबर टूल्स
# ==========================================
with main_tab2:
    if not st.session_state.tools_authenticated:
        st.markdown("#### 🔐 अंतर्गत सायबर ऑपरेशन्स")
        st.write("पासपोर्ट मेकर, आयडी प्रिंटर आणि स्कॅनर टूल्स वापरण्यासाठी मॅनेजर पासवर्ड टाका.")
        
        # गुप्त पासवर्ड बॉक्स (Default: Balaji@123)
        access_password = st.text_input("🔑 मॅनेजर पासवर्ड प्रविष्ट करा:", type="password", key="inner_tools_password")
        
        if st.button("🔓 टूल्स अनलॉक करा", type="primary", use_container_width=True):
            if access_password == "Balaji@123":
                st.session_state.tools_authenticated = True
                st.success("🔓 पासवर्ड बरोबर आहे! सर्व अंतर्गत टूल्स अनलॉक झाले आहेत.")
                st.rerun()
            else:
                st.error("❌ चुकीचा पासवर्ड! कृपया योग्य मॅनेजर पासवर्ड प्रविष्ट करा.")
                
    else:
        st.sidebar.success("🔓 इमेज टूल्स अनलॉक आहेत")
        if st.sidebar.button("🔒 टूल्स लॉक करा (Lock)"):
            st.session_state.tools_authenticated = False
            st.rerun()
            
        # पासवर्ड मॅच झाल्यावर अंतर्गत ४ उप-टॅब्स दिसतील
        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "📸 पासपोर्ट फोटो शीट मेकर", 
            "📝 सरकारी फॉर्म फोटो-सही रीसायझर", 
            "🖨️ स्मार्ट आयडी कार्ड प्रिंटर",
            "📸 कॅम-स्कॅनर (Super Fast)"
        ])
        
        # -----------------------------------------
        # उप-टॅब १: पासपोर्ट साईझ फोटो शीट मेकर
        # -----------------------------------------
        with sub_tab1:
            st.markdown("##### पासपोर्ट साईझ फोटो ऑटो-शीट जनरेटर (३.५ x ४.५ सेमी)")
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
                            for x in range(margin, canvas_w - id_w, id_w + margin):
                                sheet.paste(resized_id, (x, y))
                        buffer = io.BytesIO()
                        sheet.save(buffer, format="PNG", dpi=(DPI, DPI))
                        st.image(sheet, use_container_width=True)
                        st.download_button(label="📥 HD फोटो शीट डाऊनलोड करा", data=buffer.getvalue(), file_name="Balaji_Passport.png", mime="image/png", use_container_width=True)
                    except Exception as e: st.error(f"❌ चूक: {e}")

        # -----------------------------------------
        # उप-टॅब २: सरकारी फॉर्म फोटो व सही रीसायझर
        # -----------------------------------------
        with sub_tab2:
            st.markdown("##### 📝 सरकारी फॉर्म - फोटो व सही कॉम्प्रेसर")
            tool_mode = st.radio("रीसाईझ प्रकार निवडा:", ("ग्राहक फोटो (Photo - 20KB)", "ग्राहक सही (Signature - 10KB)"))
            uploaded_file = st.file_uploader("फाईल अपलोड करा:", type=["jpg", "jpeg", "png"], key="form_uploader")
            if uploaded_file is not None:
                raw_img = Image.open(uploaded_file).convert("RGB")
                t_width, t_height, max_kb, label = (160, 200, 20, "Photo") if "Photo" in tool_mode else (256, 64, 10, "Signature")
                if st.button(f"⚡ {label} रीसाईझ करा", type="primary", use_container_width=True):
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
                        st.download_button(label="📥 कॉम्प्रेस फाईल डाऊनलोड करा", data=img_buffer.getvalue(), file_name=f"balaji_{label.lower()}.jpg", mime="image/jpeg", use_container_width=True)
                    except Exception as e: st.error(f"❌ चूक: {e}")

        # -----------------------------------------
        # उप-टॅब ३: स्मार्ट आयडी कार्ड प्रिंटर
        # -----------------------------------------
        with sub_tab3:
            st.markdown("##### 🖨️ स्मार्ट आयडी कार्ड प्रिंटर")
            col_id1, col_id2 = st.columns(2)
            with col_id1: front_file = st.file_uploader("१. फ्रंट बाजू फोटो:", type=["jpg", "jpeg", "png"], key="id_front")
            with col_id2: back_file = st.file_uploader("२. बॅक बाजू फोटो:", type=["jpg", "jpeg", "png"], key="id_back")
            if front_file and back_file:
                if st.button("⚙️ ४x६ कडक प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
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
                        st.download_button(label="📥 प्रिंट फाईल (PNG) डाऊनलोड करा", data=id_buffer.getvalue(), file_name="Balaji_ID_Print.png", mime="image/png", use_container_width=True)
                    except Exception as e: st.error(f"❌ चूक: {e}")

        # -----------------------------------------
        # उप-टॅब ४: सुपर-फास्ट कॅम-स्कॅनर (Super Fast Scanner)
        # -----------------------------------------
        with sub_tab4:
            st.markdown("##### 📸 बालाजी सुपर-फास्ट कॅम-स्कॅनर")
            if "c_left" not in st.session_state: st.session_state.c_left = 0
            if "c_right" not in st.session_state: st.session_state.c_right = 0
            if "c_top" not in st.session_state: st.session_state.c_top = 0
            if "c_bottom" not in st.session_state: st.session_state.c_bottom = 0
            if "r_angle" not in st.session_state: st.session_state.r_angle = 0

            scan_file = st.file_uploader("स्कॅन करण्यासाठी फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="scanner_upload")
            if scan_file is not None:
                original_image = Image.open(scan_file)
                st.markdown("###### ⚡ वन-क्लिक फास्ट कंट्रोल्स:")
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
                    if st.button("🔄 ९0° फिरवा", use_container_width=True): st.session_state.r_angle = (st.session_state.r_angle + 90) % 360

                if st.button("🔄 सर्व नियंत्रणे रिसेट करा (Reset All)", type="secondary", use_container_width=True):
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
                    with st.spinner("⏳ सिस्टीम कडक साफ करत आहे..."):
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
                            st.download_button(label="📥 परफेक्ट इमेज डाऊनलोड करा", data=img_byte_arr.getvalue(), file_name="Balaji_Perfect_Scan.jpg", mime="image/jpeg", use_container_width=True)
                        except Exception as e: st.error(f"❌ चूक: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
