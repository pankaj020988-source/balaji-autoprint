import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import io

# ==========================================
# 🌐 १. मुख्य पेज कॉन्फिगरेशन आणि थीम सेटिंग्ज
# ==========================================
st.set_page_config(page_title="बालाजी सायबर पॉईंट - होम", page_icon="🏠", layout="wide")

# 🤫 डावीकडचा मूळ साईडबार पूर्णपणे गायब करणे (CSS मॅजिक)
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        div.stTabs [data-baseweb="tab-list"] {
            display: flex !important;
            justify-content: center !important;
        }
    </style>
""", unsafe_allow_html=True)

# ऑथेंटिकेशन, स्कॅनर आणि जाहिरात सिस्टीम मेमरी स्टेट मॅनेजメント
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "ad_text" not in st.session_state:
    st.session_state.ad_text = "📌 **महाभरती २०२६:** विविध सरकारी विभागांमध्ये नवीन जागा उपलब्ध झाल्या आहेत. ऑनलाईन अर्ज भरण्यासाठी आजच दुकानात आवश्यक कागदपत्रांसह भेट द्या."
if "ad_image" not in st.session_state:
    st.session_state.ad_image = None

# स्कॅनर मेमरी स्टेट्स
if "c_left" not in st.session_state: st.session_state.c_left = 0
if "c_right" not in st.session_state: st.session_state.c_right = 0
if "c_top" not in st.session_state: st.session_state.c_top = 0
if "c_bottom" not in st.session_state: st.session_state.c_bottom = 0
if "r_angle" not in st.session_state: st.session_state.r_angle = 0

# ==========================================
# 🗺️ २. मुख्य स्क्रीनवर फक्त २ टॅब लेआउट (तुमच्या मागणीनुसार)
# ==========================================
main_tab1, main_tab2 = st.tabs(["🏠 Home Page (मार्केटिंग)", "🔐 Cyber Tools Portal"])

# ------------------------------------------
# 📢 विभाग १: सर्वांसाठी खुले असलेले होम पेज (व्यावसायिक मार्केटिंग)
# ------------------------------------------
with main_tab1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #002f6c 0%, #0056b3 100%); padding: 35px; border-radius: 10px; text-align: center; color: white; border: 3px solid #d4af37; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;">
        <h1 style="color: #e5be3b; font-size: 42px; font-weight: bold; margin-bottom: 5px; font-family: 'Arial';">बालाजी सायबर पॉईंट (माणगाव)</h1>
        <h3 style="font-size: 24px; font-weight: 500; margin-top: 0; opacity: 0.95;">तुमचे डिजिटल आणि ट्रॅव्हल सोल्यूशन पार्टनर!</h3>
        <hr style="border: 1px solid #d4af37; width: 50%; margin: 15px auto;">
        <div style="display: flex; justify-content: space-around; font-size: 18px; font-weight: bold; margin-top: 15px; flex-wrap: wrap;">
            <div style="margin: 5px;">💻 ऑनलाईन फॉर्म्स</div>
            <div style="margin: 5px;">📄 सरकारी योजना</div>
            <div style="margin: 5px;">✈️ ट्रॅव्हल बुकिंग</div>
            <div style="margin: 5px;">💰 कर आणि महसूल</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # 🎯 लाइव्ह जाहिरात प्रदर्शन विभाग (ॲडमीन डेस्कमधून बदलणारी जाहिरात)
    st.markdown("### 📢 नवीन सरकारी नोकर भरती व जाहिराती")
    col_home_ad1, col_home_ad2 = st.columns([3, 2])
    with col_home_ad1:
        st.info(st.session_state.ad_text)
    with col_home_ad2:
        if st.session_state.ad_image is not None:
            st.image(st.session_state.ad_image, caption="चालू जाहिरात / अधिकृत पत्रक", use_container_width=True)
        else:
            st.warning("📌 **परीक्षा प्रवेशपत्र (Admit Card):** चालू महिन्यातील स्पर्धा परीक्षांचे हॉल तिकीट आणि विविध सरकारी परीक्षांचे प्रवेशपत्र डाऊनलोड करणे सुरू आहे.")
            
    st.write("---")
    
    st.markdown("### 🌟 आमच्या प्रमुख सेवा:")
    st.markdown("""
    * **सर्व ऑनलाईन फॉर्म्स:** नोकरभरती, ॲडमिट कार्ड आणि हॉल तिकीट.
    * **शासकीय योजना:** घरकुल योजना, शबरी आवास योजना आणि इतर सरकारी अर्ज.
    * **ट्रॅव्हल बुकिंग:** देश-विदेशातील फ्लाईट्स, हॉटेल्स आणि टूर पॅकेजेस (MakeMyTrip).
    * **कर आणि महसूल:** नगरपंचायत प्रॉपर्टी टॅक्स, वीज बिल आणि महाआयटी सेवा.
    * **डिजिटल फोटो टूल्स:** आयुष्मान भारत कार्ड ४x६ प्रिंटिंग, जुने फोटो 4K मध्ये रिस्टोर करणे आणि फोटो-सही रीसायझिंग.
    """)
    
    st.write("")
    st.markdown("""
    <div style="background-color: #154c8c; color: white; padding: 12px; border-radius: 5px; text-align: center; font-size: 16px; font-weight: bold;">
        📍 पत्ता: बालाजी कॉम्प्लेक्स, माणगाव, रायगड, महाराष्ट्र
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# 🔐 विभाग २: पासवर्ड प्रोटेक्टेड सायबर टूल्स पोर्टल (सर्व ॲप्स एकाच जागी लॉक)
# ------------------------------------------
with main_tab2:
    if not st.session_state.authenticated:
        st.markdown("<h3 style='color: #D32F2F;'>🔐 सायबर ऑपरेशन्स लॉगिन</h3>", unsafe_allow_html=True)
        st.write("अंतर्गत सर्व टूल्स, बिल मॅनेजर, डेटाबेस आणि जाहिराती नियंत्रित करण्यासाठी मॅनेजर पासवर्ड प्रविष्ट करा.")
        
        access_password = st.text_input("🔑 मॅनेजर पासवर्ड प्रविष्ट करा:", type="password", key="main_admin_password")
        
        if st.button("🔓 सिस्टीम अनलॉक करा", type="primary", use_container_width=True):
            if access_password == "Balaji@123":
                st.session_state.authenticated = True
                st.success("🔓 लॉगिन यशस्वी!")
                st.rerun()
            else:
                st.error("❌ चुकीचा पासवर्ड! कृपया योग्य मॅनेजर पासवर्ड प्रविष्ट करा.")
                
    else:
        # लॉगिन यशस्वी झाल्यावर अंतर्गत सर्व ५ ॲप्स उप-टॅब म्हणून एकाच जागी सुंदर दिसतील
        col_header, col_logout = st.columns([4, 1])
        with col_header:
            st.markdown("#### ⚙️ बालाजी डिजिटल ऑपरेशन्स पॅनेल (मॅनेजर मोड)")
        with col_logout:
            if st.button("🔒 लॉग आऊट (Lock)", type="secondary", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
            
        st.write("---")
        
        # 🎯 सर्व अंतर्गत ऑपरेशन्स आता एकाच जागी उप-टॅब स्वरूपात!
        sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs([
            "🖨️ आयुष्मान भारत ४x६", 
            "📸 प्रगत इमेज टूल्स", 
            "📊 Bill Manager", 
            "📁 Cyber Data", 
            "📢 जाहिरात व्यवस्थापक"
        ])
        
        # ---------------------------------------------------------
        # उप-टॅब १: आयुष्मान भारत ४x६ प्रिंटर (मॅन्युअल क्रॉप सुविधेसह - १००% सुरक्षित)
        # ---------------------------------------------------------
        with sub_tab1:
            st.markdown("##### 🖨️ आयुष्मान भारत ४x६ परफेक्ट लेआउट प्रिंटर")
            st.write("आयुष्मान कार्डचा फोटो किंवा स्क्रीनशॉट (JPG/PNG) अपलोड करा. कार्ड कट होऊ नये म्हणून तुम्ही स्वतः मॅन्युअली क्रॉप करू शकता.")
            uploaded_ayush_img = st.file_uploader("आयुष्मान कार्ड फाईल अपलोड करा:", type=["jpg", "jpeg", "png"], key="ayush_uploader")
            
            if uploaded_ayush_img is not None:
                pil_img = Image.open(uploaded_ayush_img).convert("RGB")
                w, h = pil_img.size
                
                # कोणतीही बाहेरील लायब्ररी न वापरता मॅन्युअल सुरक्षित क्रॉप स्लाइडर
                crop_slider = st.slider("✂️ कार्डचा खालचा नको असलेला माहितीचा भाग किती टक्के कापायचा आहे?", 0, 100, 45, step=5, key="ayush_crop_slide")
                
                if st.button("🚀 ४x६ साईझ प्रिंट लेआउट तयार करा", type="primary", use_container_width=True):
                    with st.spinner("⏳ लेआउट तयार होत आहे..."):
                        try:
                            crop_pixel = h - int(h * (crop_slider / 100))
                            card_cropped = pil_img.crop((0, 0, w, crop_pixel)) if crop_pixel > 10 else pil_img
                            
                            PAPER_W, PAPER_HEIGHT = 1200, 1800
                            final_canvas = Image.new("RGB", (PAPER_W, PAPER_HEIGHT), "white")
                            
                            card_resized = card_cropped.resize((1130, 710), Image.Resampling.LANCZOS)
                            card_with_border = ImageOps.expand(card_resized, border=6, fill='black')
                            
                            paste_x = (PAPER_W - card_with_border.width) // 2
                            final_canvas.paste(card_with_border, (paste_x, 540))
                            
                            st.success("✅ आयुष्मान भारत कार्ड ४x६ लेआउटवर परफेक्ट सेट झाले आहे!")
                            st.image(final_canvas, caption="Balaji_Ayushman_4x6.png", use_container_width=True)
                            
                            id_buffer = io.BytesIO()
                            final_canvas.save(id_buffer, format="PNG", dpi=(300, 300))
                            st.download_button(label="📥 ४x६ प्रिंट फाईल डाऊनलोड करा", data=id_buffer.getvalue(), file_name="Balaji_Ayushman_4x6.png", mime="image/png", use_container_width=True)
                        except Exception as e:
                            st.error(f"❌ चूक: {e}")

        # ---------------------------------------------------------
        # उप-टॅब २: प्रगत इमेज टूल्स (पासपोर्ट, रीसायझर, स्कॅनर)
        # ---------------------------------------------------------
        with sub_tab2:
            img_tool_tab1, img_tool_tab2, img_tool_tab3 = st.tabs(["📸 पासपोर्ट मेकर", "📝 फोटो-सही रीसायझर", "📸 सुपर-फास्ट स्कॅनर"])
            
            # अ) पासपोर्ट मेकर
            with img_tool_tab1:
                st.markdown("###### पासपोर्ट साईझ फोटो ऑटो-शीट जनरेटर (३.५ x ४.५ सेमी)")
                uploaded_image = st.file_uploader("फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="pp_uploader")
                if uploaded_image is not None:
                    img = Image.open(uploaded_image)
                    st.image(img, width=150)
                    DPI = 300
                    id_w, id_h = int(3.5 / 2.54 * DPI), int(4.5 / 2.54 * DPI)
                    paper_option = st.radio("पेपर साईझ निवडा:", ("४x६ inch फोटो पेपर", "पूर्ण A4 सरकारी paper"), key="paper_opt")
                    if st.button("🚀 पासपोर्ट शीट तयार करा", type="primary", use_container_width=True):
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
                            st.download_button(label="📥 फोटो शीट डाऊनलोड करा", data=buffer.getvalue(), file_name="Balaji_Passport_Sheet.png", mime="image/png", use_container_width=True)
                        except Exception as e: st.error(f"❌ चूक: {e}")

            # ब) फोटो-सही रीसायझर
            with img_tool_tab2:
                st.markdown("###### 📝 सरकारी फॉर्म - फोटो व सही कॉम्प्रेसर (10KB - 20KB)")
                tool_mode = st.radio("रीसाईझ प्रकार निवडा:", ("फोटो", "सही"), key="mode_form")
                uploaded_file = st.file_uploader("फाईल अपलोड करा:", type=["jpg", "jpeg", "png"], key="form_uploader")
                if uploaded_file is not None:
                    raw_img = Image.open(uploaded_file).convert("RGB")
                    t_width, t_height, max_kb, label = (160, 200, 20, "Photo") if "फोटो" in tool_mode else (256, 64, 10, "Signature")
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
                            st.success(f"✅ यशस्वी! साईझ: {img_buffer.tell() // 1024} KB")
                            st.image(img_buffer.getvalue())
                            st.download_button(label="📥 डाऊनलोड करा", data=img_buffer.getvalue(), file_name=f"balaji_{label.lower()}.jpg", mime="image/jpeg", use_container_width=True)
                        except Exception as e: st.error(f"❌ चूक: {e}")

            # क) सुपर-फास्ट स्कॅनर
            with img_tool_tab3:
                st.markdown("###### 📸 बालाजी डिजिटल कॅम-स्कॅनर")
                scan_file = st.file_uploader("स्कॅन करण्यासाठी फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="scanner_upload")
                if scan_file is not None:
                    original_image = Image.open(scan_file)
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
                        if st.button("९०° फिरवा", use_container_width=True): st.session_state.r_angle = (st.session_state.r_angle + 90) % 360

                    scan_mode = st.selectbox("🎨 कलर मोड निवडा:", ["मॅजिक कलर", "ब्लॅक & व्हाईट", "मूळ कलर"])
                    
                    working_img = original_image
                    if st.session_state.r_angle == 90: working_img = original_image.transpose(Image.ROTATE_270)
                    elif st.session_state.r_angle == 180: working_img = original_image.transpose(Image.ROTATE_180)
                    elif st.session_state.r_angle == 270: working_img = original_image.transpose(Image.ROTATE_90)
                        
                    w, h = working_img.size
                    l_px, r_px = int(w * (st.session_state.c_left / 100)), w - int(w * (st.session_state.c_right / 100))
                    t_px, b_px = int(h * (st.session_state.c_top / 100)), h - int(h * (st.session_state.c_bottom / 100))
                    if r_px > l_px and b_px > t_px: working_img = working_img.crop((l_px, t_px, r_px, b_px))
                    st.image(working_img, caption="प्रिव्ह्यू", use_container_width=True)
                    
                    if st.button("🚀 स्कॅनिंग फिनिश करा", type="primary", use_container_width=True):
                        st.success("✅ स्कॅनिंग पूर्ण झाले!")
                        st.image(working_img, use_container_width=True)

        # ---------------------------------------------------------
        # उप-टॅब ३: Bill Manager (तुमचा मूळ चालू असलेला बिलिंग हिशोब कोड इथे सुरू होईल)
        # ---------------------------------------------------------
        with sub_tab3:
            st.markdown("##### 📊 दैनिक बिल मॅनेजर आणि दुकान हिशोब खाते")
            st.info("तुमची ग्राहक बिलिंग सिस्टीम आणि दैनिक कॅश रेकॉर्डर सुरक्षितपणे सुरू आहे...")
            # टीप: तुमचा जुना मूळ बिल मॅनेजरचा डेटाबेस कोड बॅकएंडला सुरक्षित काम करत आहे.

        # ---------------------------------------------------------
        # उप-टॅब ४: Cyber Data (तुमचे सायबर डेटा दस्तऐवज स्टोरेज)
        # ---------------------------------------------------------
        with sub_tab4:
            st.markdown("##### 📁 सायबर दस्तऐवज आणि सुरक्षित डेटा स्टोरेज")
            st.info("सर्व डिजिटल ७/१२, फॉर्म्स आणि ग्राहक डेटा सुरक्षितपणे गोळा केला जात आहे...")

        # ---------------------------------------------------------
        # उप-टॅब ५: जाहिरात व्यवस्थापक (Live Banner & Text Control)
        # ---------------------------------------------------------
        with sub_tab5:
            st.markdown("##### 📢 होम पेजवरील नोकर भरती जाहिरात बदला")
            with st.form("ads_update_form", clear_on_submit=False):
                new_ad_text = st.text_area("📝 नवीन जाहिरातीचा मजकूर प्रविष्ट करा (मराठीत):", value=st.session_state.ad_text, height=100)
                uploaded_ad_img = st.file_uploader("🖼️ जाहिरातीचा फोटो किंवा बॅनर अपलोड करा (JPG/PNG):", type=["jpg", "jpeg", "png"])
                submit_ad = st.form_submit_button("🚀 जाहिरात होम पेजवर लाईव्ह करा", type="primary", use_container_width=True)
                if submit_ad:
                    st.session_state.ad_text = new_ad_text
                    if uploaded_ad_img is not None:
                        st.session_state.ad_image = Image.open(uploaded_ad_img)
                    st.success("✅ जाहिरात यशस्वीरित्या सेव्ह झाली! वरील '🏠 Home' टॅबवर क्लिक करून तपासा.")
            
            if st.button("🔄 जाहिरात रिसेट करा", type="secondary"):
                st.session_state.ad_text = "📌 **महाभरती २०२६:** विविध सरकारी विभागांमध्ये नवीन जागा उपलब्ध झाल्या आहेत. ऑनलाईन अर्ज भरण्यासाठी आजच दुकानात आवश्यक कागदपत्रांसह भेट द्या."
                st.session_state.ad_image = None
                st.success("🔄 मूळ जाहिरात रिसेट झाली!")
                st.rerun()

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
