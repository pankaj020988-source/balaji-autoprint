# ==========================================
# 🖨️ टॅब ३: स्मार्ट आयडी कार्ड प्रिंटर (Aadhaar/PAN/Voter)
# ==========================================
with st.container():
    st.write("---")
    st.markdown("<h3 style='text-align: center; color: #0056b3;'>🖨️ स्मार्ट आयडी कार्ड प्रिंटर (Aadhaar/PAN/Voter)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>दोन्ही बाजूंचे फोटो अपलोड करा, ६ पिक्सेल काळी बॉर्डर आणि एकसमान साईझ ऑटोमॅटिक सेट होईल!</p>", unsafe_allow_html=True)
    
    col_id1, col_id2 = st.columns(2)
    with col_id1:
        front_file = st.file_uploader("१. फ्रंट बाजूचा (Front Side) फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="id_front")
    with col_id2:
        back_file = st.file_uploader("२. बॅक बाजूचा (Back Side) फोटो अपलोड करा:", type=["jpg", "jpeg", "png"], key="id_back")

    if front_file is not None and back_file is not None:
        if st.button("⚙️ ४x६ कडक प्रिंट लेआउट तयार करा", type="primary", use_container_width=True, key="btn_id_generate"):
            with st.spinner("⏳ दोन्ही बाजूंची साईझ एकसमान करून बॉर्डर सेट होत आहे..."):
                try:
                    # १. फोटो मेमरीमध्ये लोड करणे
                    img_f = Image.open(front_file).convert("RGB")
                    img_b = Image.open(back_file).convert("RGB")
                    
                    # 🎯 २. दोन्ही बाजूंची साईझ शंभर टक्के एकसमान आणि कडक फिट (११३० x ७१० पिक्सेल)
                    final_w, final_h = 1130, 710
                    img_f = img_f.resize((final_w, final_h), Image.Resampling.LANCZOS)
                    img_b = img_b.resize((final_w, final_h), Image.Resampling.LANCZOS)
                    
                    # 🔲 ३. दोन्ही फोटोंना एकदम परफेक्ट कट-टू-कट ६ पिक्सेलची काळी बॉर्डर लावणे
                    img_f = ImageOps.expand(img_f, border=6, fill='black')
                    img_b = ImageOps.expand(img_b, border=6, fill='black')
                    
                    # 🖼️ ४. ४x६ मुख्य कॅनव्हास (१२०० x १८०० उभा फोटो पेपर)
                    target_w, target_h = 1200, 1800
                    id_canvas = Image.new("RGB", (target_w, target_h), "white")
                    
                    # सेंटर अलाइनमेंट कॅल्क्युलेशन
                    paste_x = (target_w - img_f.width) // 2
                    
                    # ५. वरती फ्रंट आणि खाली बॅक परफेक्ट पेस्ट केले
                    id_canvas.paste(img_f, (paste_x, 150)) # वरून १५० पिक्सेल सोडले
                    id_canvas.paste(img_b, (paste_x, 950)) # दोन्हीमध्ये कडक अंतर
                    
                    # ६. हाय-क्वालिटी पीएनजी (PNG) मेमरी सेव्हिंग
                    id_buffer = io.BytesIO()
                    id_canvas.save(id_buffer, format="PNG", dpi=(300, 300))
                    id_buffer.seek(0)
                    
                    st.success("✅ आयडी कार्ड प्रिंट शीट एकदम रेडी आहे!")
                    st.image(id_canvas, caption="४x६ प्रिंट प्रिव्ह्यू (फ्रंट वर, बॅक खाली)", use_container_width=True)
                    
                    # 📥 ७. डाऊनलोड बटण
                    st.download_button(
                        label="📥 ४x६ कडक आयडी कार्ड प्रिंट (PNG) डाऊनलोड करा",
                        data=id_buffer,
                        file_name="Balaji_Smart_ID_Print.png",
                        mime="image/png",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ चूक झाली: {e}")
