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
