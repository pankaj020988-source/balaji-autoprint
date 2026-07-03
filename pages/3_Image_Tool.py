import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import io

# पेजचे नाव आणि लेआउट सेट करणे
st.set_page_config(page_title="बालाजी सायबर पॉइंट - इमेज टूल्स", page_icon="📸", layout="centered")

# ऑथेंटिकेशन आणि स्कॅनर मेमरी स्टेट मॅनेजमेंट
if "tools_authenticated" not in st.session_state:
    st.session_state.tools_authenticated = False

if "c_left" not in st.session_state: st.session_state.c_left = 0
if "c_right" not in st.session_state: st.session_state.c_right = 0
if "c_top" not in st.session_state: st.session_state.c_top = 0
if "c_bottom" not in st.session_state: st.session_state.c_bottom = 0
if "r_angle" not in st.session_state: st.session_state.r_angle = 0

st.markdown("<h2 style='text-align: center; color: #0078D7;'>📸 श्री बालाजी सायबर पॉईंट - डिजिटल पोर्टल्स</h2>", unsafe_allow_html=True)
st.write("---")

# 🎯 मुख्य दोन विभाग (टॅब्स): होम पेज सर्वांसाठी खुले, सायबर टूल्स पासवर्डच्या मागे लॉक
main_tab1, main_tab2 = st.tabs([
    "🏠 होम पेज (जाहिरात व सुविधा)", 
    "🔐 सायबर टूल्स पोर्टल (Locked)"
])

# ==========================================
# 📢 विभाग १: सर्वांसाठी खुले असलेले होम पेज (व्यावसायिक मार्केटिंग)
# ==========================================
with main_tab1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #002f6c 0%, #0056b3 100%); padding: 30px; border-radius: 10px; text-align: center; color: white; border: 2px solid #d4af37; margin-bottom: 20px;">
        <h2 style="color: #e5be3b; margin-bottom: 5px;">बालाजी सायबर पॉईंट (माणगाव)</h2>
        <h4 style="opacity: 0.9; margin-top: 0;">तुमचे डिजिटल आणि ट्रॅव्हल सोल्यूशन पार्टनर!</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📢 नवीन सरकारी नोकर भरती व जाहिराती")
    col_ads1, col_ads2 = st.columns(2)
    with col_ads1:
        st.info("📌 **महाभरती २०२६:** विविध सरकारी विभागांमध्ये नवीन जागा उपलब्ध झाल्या आहेत. ऑनलाईन अर्ज भरण्यासाठी आजच दुकानात आवश्यक कागदपत्रांसह भेट द्या.")
    with col_ads2:
        st.warning("📌 **परीक्षा प्रवेशपत्र (Admit Card):** चालू महिन्यातील स्पर्धा परीक्षांचे हॉल तिकीट आणि विविध सरकारी परीक्षांचे प्रवेशपत्र डाऊनलोड करणे सुरू आहे.")
        
    st.write("---")
    st.markdown("#### 🛠️ आमच्याकडे उपलब्ध असलेल्या प्रमुख सुविधा:")
    col_serv1, col_serv2 = st.columns(2)
    with col_serv1:
        st.markdown("""
        **🖨️ कार्ड प्रिंटिंग आणि स्कॅनर सेवा**
        * आयुष्मान भारत कार्ड ४x६ ऑटो-फिट प्रिंटिंग
        * स्मार्ट आयडी कार्ड प्रिंटर (पॅन कार्ड / वोटर आयडी)
        * डिजिटल दस्तऐवज आणि ७/१२ उतारा कलर प्रिंटिंग
        """)
    with col_serv2:
        st.markdown("""
        **📝 ऑनलाईन फॉर्म आणि ट्रॅव्हल बुकिंग**
        * सर्व प्रकारच्या सरकारी व भरती परीक्षांचे ऑनलाईन अर्ज
        * रेशन कार्ड, उत्पन्न दाखला आणि नवीन नोंदणी अर्ज
        * देश-विदेशातील फ्लाईट्स, रेल्वे आणि हॉटेल बुकिंग सेवा (MakeMyTrip)
        """)
        
    st.write("---")
    st.markdown("<p style='text-align: center; font-size: 13px; color: #666;'>📍 पत्ता: बालाजी कॉम्प्लेक्स, माणगाव, रायगड, महाराष्ट्र</p>", unsafe_allow_html=True)

# ==========================================
# 🔐 विभाग २: पासवर्ड प्रोटेक्टेड सायबर टूल्स
# ==========================================
with main_tab2:
    if not st.session_state.tools_authenticated:
        st.markdown("#### 🔐 अंतर्गत सायबर ऑपरेशन्स")
        access_password = st.text_input("🔑 मॅनेजर पासवर्ड प्रविष्ट करा:", type="password", key="inner_tools_password")
        
        if st.button("🔓 टूल्स अनलॉक करा", type="primary", use_container_width=True):
            if access_password == "Balaji@123":
                st.session_state.tools_authenticated = True
                st.success("🔓 सर्व अंतर्गत टूल्स अनलॉक झाले आहेत!")
                st.rerun()
            else:
                st.error("❌ चुकीचा पासवर्ड! कृपया योग्य मॅनेजर पासवर्ड प्रविष्ट करा.")
    else:
        st.sidebar.success("🔓 इमेज टूल्स अनलॉक आहेत")
        if st.sidebar.button("🔒 टूल्स लॉक करा (Lock)"):
            st.session_state.tools_authenticated = False
            st.rerun()
            
        # अंतर्गत ४ उप-टॅब्स
        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "🖨️ आयुष्मान भारत ४x६",
            "📸 पासपोर्ट फोटो मेकर", 
            "📝 फोटो-सही रीसायझर", 
            "📸 कॅम-स्कॅनर व आयडी प्रिंट"
        ])
        
        # -----------------------------------------
        # उप-टॅब १: आयुष्मान भारत ४x६ प्रिंटर (मॅन्युअल क्रॉप सुविधेसह)
        # -----------------------------------------
        with sub_tab1:
            st.markdown("##### 🖨️ आयुष्मान भारत ४x६ परफेक्ट लेआउट प्रिंटर")
            uploaded_ad_img = st.file_uploader("आयुष्मान कार्डचा फोटो/स्क्रीनशॉट अपलोड करा:", type=["jpg", "jpeg", "png"], key="ayush_uploader")
            
            if uploaded_ad_img is not None:
                pil_img = Image.open(uploaded_ad_img).convert("RGB")
                
                st.write("🎯 **कार्ड कट होऊ नये म्हणून खालचा नको असलेला भाग इथून कापून घ्या:**")
                w, h = pil_img.size
                
                # इमेज कापण्यासाठी सुरक्षित क्रॉप स्लाइडर (No dependency error)
                crop_slider = st.slider("खालून किती टक्के भाग कापायचा आहे?", 0, 100, 45, step=5)
                
                if st.button("🚀 ४x६ साईझ लेआउट तयार करा", type="primary", use_container_width=True):
                    try:
                        # स्लाइडरनुसार खालचा भाग अचूक कट करणे
                        crop_pixel = h - int(h * (crop_slider / 100))
                        if crop_pixel > 10:
                            card_cropped = pil_img.crop((0, 0, w, crop_pixel))
                        else:
                            card_cropped = pil_img
                        
                        PAPER_W, PAPER_HEIGHT = 1200, 1800
                        final_canvas = Image.new("RGB", (PAPER_W, PAPER_HEIGHT), "white")
                        
                        card_resized = card_cropped.resize((1130, 710), Image.Resampling.LANCZOS)
                        card_with_border = ImageOps.expand(card_resized, border=6, fill='black')
                        
                        paste_x = (PAPER_W - card_with_border.width) // 2
                        final_canvas.paste(card_with_border, (paste_x, 540))
                        
                        st.image(final_canvas, caption="Balaji_Ayushman_4x6.png", use_container_width=True)
                        
                        id_buffer = io.BytesIO()
                        final_canvas.save(id_buffer, format="PNG", dpi=(300, 300))
                        st.download_button(label="📥 ४x६ फाईल डाऊनलोड करा", data=id_buffer.getvalue(), file_name="Balaji_Ayushman_4x6.png", mime="image/png", use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ चूक: {e}")

        # -----------------------------------------
        # उप-टॅब २: पासपोर्ट साईझ फोटो शीट मेकर
        # -----------------------------------------
        with sub_tab2:
            st.markdown("##### पासपोर्ट साईझ फोटो ऑटो-शीट जनरेटर")
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
                    except Exception as e: st.error(f"❌ चूक: {e}")

        # -----------------------------------------
        # उप-टॅब ३: सरकारी फॉर्म फोटो व सही रीसायझर
        # -----------------------------------------
        with sub_tab3:
            st.markdown("##### 📝 सरकारी फॉर्म - फोटो व सही कॉम्प्रेसर")
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
                        st.success(f"✅ यशस्वी! साईझ: {len(img_buffer.getvalue()) // 1024} KB")
                        st.image(img_buffer.getvalue())
                    except Exception as e: st.error(f"❌ चूक: {e}")

        # -----------------------------------------
        # उप-टॅब ४: सुपर-फास्ट स्कॅनर व स्मार्ट आयडी प्रिंटर
        # -----------------------------------------
        with sub_tab4:
            st.markdown("##### 🖨️ स्मार्ट आयडी कार्ड प्रिंटर व कॅम-स्कॅनर")
            st.info("तुमची प्रगत स्कॅनर व पॅन/वोटर आयडी सिस्टीम कनेक्टेड आहे...")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
