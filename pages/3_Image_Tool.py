import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
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
# 🎨 २. कॉर्पोरेट UI डिझाईन (CSS)
# ==========================================
st.markdown("""
    <style>
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
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
    
    div[data-baseweb="tab-list"] {
        gap: 8px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    
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

st.markdown("<div class='main-header'>बालाजी सायबर पॉईंट - इमेज प्रोसेसिंग टूलकिट</div>", unsafe_allow_html=True)

# ==========================================
# 📐 कटिंग लाईन फंक्शन (बॉर्डरच्या बाहेर सेफ अंतर)
# ==========================================
def draw_safe_cutting_guides(draw_obj, box, offset=12, line_len=35, color="#666666", width=2):
    x0, y0, x1, y1 = box
    cx0 = x0 - offset
    cy0 = y0 - offset
    cx1 = x1 + offset
    cy1 = y1 + offset
    
    # कॉर्नर कट्स (Corner Crop Lines)
    draw_obj.line([(cx0 - line_len, cy0), (cx0, cy0)], fill=color, width=width)
    draw_obj.line([(cx0, cy0 - line_len), (cx0, cy0)], fill=color, width=width)
    draw_obj.line([(cx1, cy0), (cx1 + line_len, cy0)], fill=color, width=width)
    draw_obj.line([(cx1, cy0 - line_len), (cx1, cy0)], fill=color, width=width)
    draw_obj.line([(cx0 - line_len, cy1), (cx0, cy1)], fill=color, width=width)
    draw_obj.line([(cx0, cy1), (cx0, cy1 + line_len)], fill=color, width=width)
    draw_obj.line([(cx1, cy1), (cx1 + line_len, cy1)], fill=color, width=width)
    draw_obj.line([(cx1, cy1), (cx1, cy1 + line_len)], fill=color, width=width)
    
    # तुटक रेषा (Dotted Cutting Lines)
    dash_len = 15
    space_len = 10
    for x in range(int(cx0), int(cx1), dash_len + space_len):
        draw_obj.line([(x, cy0), (min(x + dash_len, cx1), cy0)], fill="#888888", width=1)
        draw_obj.line([(x, cy1), (min(x + dash_len, cx1), cy1)], fill="#888888", width=1)
    for y in range(int(cy0), int(cy1), dash_len + space_len):
        draw_obj.line([(cx0, y), (cx0, min(y + dash_len, cy1))], fill="#888888", width=1)
        draw_obj.line([(cx1, y), (cx1, min(y + dash_len, cy1))], fill="#888888", width=1)

def auto_crop_card(card_img):
    gray = card_img.convert("L")
    inverted = ImageOps.invert(gray)
    bbox = inverted.getbbox()
    if bbox:
        return card_img.crop(bbox)
    return card_img

# ==========================================
# 🛠️ मुख्य टूल्स (टॅब्स)
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "आधार कटर (4x6)", 
    "ज्येष्ठ नागरिक कार्ड (4x6)",
    "पासपोर्ट फोटो मेकर (9 Photos)",
