import streamlit as st
import os
from fitz import open as open_pdf, Matrix
from PIL import Image, ImageOps
import io

# 🌐 वेब साईटचे नाव आणि लेआउट (श्री बालाजी सायबर पॉईंट ब्रँडिंग)
st.set_page_config(page_title="श्री बालाजी सायबर पॉईंट - PMJAY 4X6", page_icon="🖨️", layout="centered")

st.markdown("<h2 style='text-align: center; color: #0078D7;'>🌐 श्री बालाजी सायबर पॉईंट, माणगाव</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>आयुष्मान भारत PDF ते 4X6 कडक प्रिंट कन्व्हर्टर</h4>", unsafe_allow_html=True)
st.write("---")

def get_clean_card_boundary(cropped_img):
    """आजूबाजूची नको असलेली पांढरी स्पेस ऑटोमॅटिक कट करण्याची सिस्टीम"""
    gray = cropped_img.convert("L")
    inverted = ImageOps.invert(gray)
    thresh = inverted.point(lambda p: 255 if p > 10 else 0)
    bbox = thresh.getbbox()
    if bbox:
        return cropped_img.crop(bbox)
    return cropped_img

# 📁 फाईल अपलोड करण्याचा सुंदर बॉक्स
uploaded_file = st.file_uploader("तुमची आयुष्मान भारत सरकारी PDF फाईल इथे अपलोड करा:", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("⏳ प्रोसेसिंग सुरू आहे... १ सेकंद थांबा..."):
        try:
            # १. अपलोड केलेली PDF मेमरीमध्ये वाचणे
            pdf_bytes = uploaded_file.read()
            doc = open_pdf(stream=pdf_bytes, filetype="pdf")
            page = doc[0]
            
            # हाय-क्वालिटी रूपांतर (झूम ४)
            zoom = 4
            mat = Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # इमेज PIL फॉर्मॅटमध्ये कन्व्हर्ट करणे
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            width, height = img.size
            doc.close()
            
            # २. अचूक प्राथमिक क्रॉपिंग (फ्रंट आणि बॅक)
            front_crop = img.crop((int(width * 0.03), int(height * 0.32), int(width * 0.495), int(height * 0.89)))
            back_crop = img.crop((int(width * 0.505), int(height * 0.32), int(width * 0.97), int(height * 0.89)))
            
            # ३. ऑटोमॅटिक पांढरी जागा ट्रिम करणे (दोन्ही बाजूंची पांढरी पट्टी गायब)
            clean_front = get_clean_card_boundary(front_crop)
            clean_back = get_clean_card_boundary(back_crop)
            
            # ४. दोन्ही बाजूंची साईझ शंभर टक्के एकसमान आणि कडक फिट (११३० x ७१० पिक्सेल)
            final_w, final_h = 1130, 710
            clean_front = clean_front.resize((final_w, final_h), Image.Resampling.LANCZOS)
            clean_back = clean_back.resize((final_w, final_h), Image.Resampling.LANCZOS)
            
            # 🔲 ५. ४ ही बाजूंना एकदम परफेक्ट कट-टू-कट ६ पिक्सेलची काळी बॉर्डर
            clean_front = ImageOps.expand(clean_front, border=6, fill='black')
            clean_back = ImageOps.expand(clean_back, border=6, fill='black')
            
            # ६. ४x६ मुख्य कॅनव्हास (१२०० x १८०० उभा फोटो पेपर)
            target_w, target_h = 1200, 1800
            final_4x6_canvas = Image.new("RGB", (target_w, target_h), "white")
            
            # सेंटर अलाइनमेंट
            paste_x = (target_w - clean_front.width) // 2
            
            # वरती फ्रंट आणि खाली बॅक परफेक्ट पेस्ट केले
            final_4x6_canvas.paste(clean_front, (paste_x, 110))
            final_4x6_canvas.paste(clean_back, (paste_x, 920))
            
            # ७. फाईल डाऊनलोडसाठी मेमरीमध्ये सेव्ह करणे
            buffer = io.BytesIO()
            final_4x6_canvas.save(buffer, format="JPEG", quality=100, subsampling=0)
            buffer.seek(0)
            
            # 🖥️ स्क्रीनवर नवीन कार्डाचा प्रिव्ह्यू दाखवणे
            st.success("✅ कार्ड एकदम परफेक्ट तयार झाले आहे!")
            st.image(final_4x6_canvas, caption="४x६ प्रिंट प्रिव्ह्यू (फ्रंट वर, बॅक खाली)", use_container_width=True)
            
            # 📥 कडक डाऊनलोड बटण
            original_name = os.path.splitext(uploaded_file.name)[0]
            st.download_button(
                label="📥 ४x६ फोटो प्रिंट (JPG) डाऊनलोड करा",
                data=buffer,
                file_name=f"{original_name}_4x6_Balaji.jpg",
                mime="image/jpeg"
            )
            
        except Exception as e:
            st.error(f"❌ तांत्रिक अडचण आली: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Designed by Balaji Cyber Point, Mangaon</p>", unsafe_allow_html=True)
