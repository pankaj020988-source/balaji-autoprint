import streamlit as st
from PIL import Image, ImageOps, ImageDraw
import io
import fitz

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
# Helper Function for Cutting Lines
# ==========================================
def draw_safe_cutting_guides(draw_obj, box, offset=12, line_len=35, color="#666666", width=2):
    x0, y0, x1, y1 = box
    cx0 = x0 - offset
    cy0 = y0 - offset
    cx1 = x1 + offset
    cy1 = y1 + offset

    draw_obj.line([(cx0 - line_len, cy0), (cx0, cy0)], fill=color, width=width)
    draw_obj.line([(cx0, cy0 - line_len), (cx0, cy0)], fill=color, width=width)
    draw_obj.line([(cx1, cy0), (cx1 + line_len, cy0)], fill=color, width=width)
    draw_obj.line([(cx1, cy0 - line_len), (cx1, cy0)], fill=color, width=width)
    draw_obj.line([(cx0 - line_len, cy1), (cx0, cy1)], fill=color, width=width)
    draw_obj.line([(cx0, cy1), (cx0, cy1 + line_len)], fill=color, width=width)
    draw_obj.line([(cx1, cy1), (cx1 + line_len, cy1)], fill=color, width=width)
    draw_obj.line([(cx1, cy1), (cx1 + line_len, cy1)], fill=color, width=width)

    dash_len = 15
    space_len = 10
    for x in range(int(cx0), int(cx1), dash_len + space_len):
        draw_obj.line([(x, cy0), (min(x + dash_len, cx1), cy0)], fill="#888888", width=1)
        draw_obj.line([(x, cy1), (min(x + dash_len, cx1), cy1)], fill="#888888", width=1)
    for y in range(int(cy0), int(cy1), dash_len + space_len):
        draw_obj.line([(cx0, y), (cx0, min(y + dash_len, cy1))], fill="#888888", width=1)
        draw_obj.line([(cx1, y), (cx1, min(y + dash_len, cy1))], fill="#888888", width=1)

def trim_white_edges(im):
    gray = im.convert("L")
    inv = ImageOps.invert(gray)
    bbox = inv.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

# ==========================================
# 3. Main Tabs
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "Aadhaar Cutter (4x6)",
    "Senior Citizen Card (4x6)",
    "Passport Photo Maker (9 Photos)"
])

# ------------------------------------------
# Tab 1: Aadhaar Cutter
# ------------------------------------------
with tab1:
    col_a1, col_a2 = st.columns([2, 1])
    with col_a1:
        pdf_file = st.file_uploader("Aadhaar PDF Upload Kara:", type=["pdf"], key="aadhaar_pdf_uploader")
    with col_a2:
        pdf_password = st.text_input("PDF Password (Asel Tar):", type="password", key="pdf_pass_input")

    if pdf_file is not None:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            top_trim = st.slider("Top Trim (%)", 65.0, 78.0, 72.2, step=0.2, key="top_trim_slider")
        with col_c2:
            bottom_trim = st.slider("Bottom Trim (%)", 88.0, 98.0, 92.5, step=0.2, key="bot_trim_slider")

        if st.button("Generate 4x6 Layout", type="primary", use_container_width=True, key="btn_aadhaar_gen"):
            with st.spinner("Processing chalu ahe..."):
                try:
                    pdf_bytes = pdf_file.read()
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

                    if doc.is_encrypted:
                        if pdf_password:
                            auth_success = doc.authenticate(pdf_password)
                            if not auth_success:
                                st.error("Chukicha password takla ahe.")
                                st.stop()
                        else:
                            st.warning("Krupaya PDF password taka.")
                            st.stop()

                    page = doc[0]
                    pix = page.get_pixmap(dpi=400)
                    img_data = pix.tobytes("png")
                    full_img = Image.open(io
