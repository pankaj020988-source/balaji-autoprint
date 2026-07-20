# ------------------------------------------
# 📸 टॅब ४: कॅम-स्कॅनर (JPG, PNG आणि PDF सपोर्टसह)
# ------------------------------------------
with tab4:
    st.markdown("<h4 style='color: #E65100;'>📸 बालाजी सुपर-फास्ट कॅम-स्कॅनर</h4>", unsafe_allow_html=True)
    st.write("झटपट क्रॉप आणि सरळ करण्यासाठी खालील बटनांचा वापर करा.")
    
    if "c_left" not in st.session_state: st.session_state.c_left = 0
    if "c_right" not in st.session_state: st.session_state.c_right = 0
    if "c_top" not in st.session_state: st.session_state.c_top = 0
    if "c_bottom" not in st.session_state: st.session_state.c_bottom = 0
    if "r_angle" not in st.session_state: st.session_state.r_angle = 0

    # 🎯 इथे "pdf" पर्याय जोडला आहे
    scan_file = st.file_uploader("स्कॅन करण्यासाठी डॉक्युमेंटचा फोटो किंवा PDF फाईल अपलोड करा (JPG/PNG/PDF):", type=["jpg", "jpeg", "png", "pdf"], key="scanner_upload")

    if scan_file is not None:
        try:
            # 📄 जर फाईल PDF असेल तर त्याचे इमेजमध्ये रूपांतर करणे
            if scan_file.name.lower().endswith(".pdf"):
                pdf_bytes = scan_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                page = doc[0] # पहिली पान रेंडर करणे
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
