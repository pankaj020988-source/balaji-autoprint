import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
import io
import fitz  # PyMuPDF
import cv2
import numpy as np

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="Balaji Cyber Point - Digital Toolkit", 
    page_icon="🖥️", 
    layout="wide"
)

# ==========================================
# 2. UI Style (CSS)
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

st.markdown("<div class='main-header'>Balaji Cyber Point - Image Processing Toolkit</div>", unsafe_allow_html=True)

# ==========================================
# Helper Functions
# ==========================================
def draw_safe_cutting_guides(draw_obj, box, offset=12, line_len=35, color="#666666", width=2):
    x0, y0, x1, y1 = box
    cx0 = x0 - offset
    cy0 = y0 - offset
    cx1 = x1 + offset
    cy1 = y1 + offset
    
    # Corner Marks
    draw_obj.line([(cx0 - line_len, cy0), (cx0, cy0)], fill=color, width=width)
    draw_obj.line([(cx0, cy0 - line_len), (cx0, cy0)], fill=color, width=width)
    draw_obj.line([(cx1, cy0), (cx1 + line_len, cy0)], fill=color, width=width)
    draw_obj.line([(cx1, cy0 - line_len), (cx1, cy0)], fill=color, width=width)
    draw_obj.line([(cx0 - line_len, cy1), (cx0, cy1)], fill=color, width=width)
    draw_obj.line([(cx0, cy1), (cx0, cy1 + line_len)], fill=color, width=width)
    draw_obj.line([(cx1, cy1), (cx1 + line_len, cy1)], fill=color, width=width)
    draw_obj.line([(cx1, cy1), (cx1 + line_len, cy1)], fill=color, width=width)
    
    # Dotted Border Lines
    dash_len = 15
    space_len = 10
    for x
