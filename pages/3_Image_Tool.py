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
# Helper Functions
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
                    full_img = Image.open(io.BytesIO(img_data)).convert("RGB")

                    w, h = full_img.size
                    t_pct = top_trim / 100.0
                    b_pct = bottom_trim / 100.0

                    crop_front = full_img.crop((int(w * 0.078), int(h * t_pct), int(w * 0.492), int(h * b_pct)))
                    crop_back = full_img.crop((int(w * 0.508), int(h * t_pct), int(w * 0.922), int(h * b_pct)))

                    PAPER_W, PAPER_HEIGHT = 1200, 1800
                    final_canvas = Image.new("RGB", (PAPER_W, PAPER_HEIGHT), "white")

                    card_w, card_h = 1040, 595
                    front_resized = crop_front.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    back_resized = crop_back.resize((card_w, card_h), Image.Resampling.LANCZOS)

                    front_bordered = ImageOps.expand(front_resized, border=4, fill='black')
                    back_bordered = ImageOps.expand(back_resized, border=4, fill='black')

                    bw, bh = front_bordered.size
                    paste_x = (PAPER_W - bw) // 2
                    y_front = 180
                    y_back = 950

                    final_canvas.paste(front_bordered, (paste_x, y_front))
                    final_canvas.paste(back_bordered, (paste_x, y_back))

                    draw = ImageDraw.Draw(final_canvas)
                    draw_safe_cutting_guides(draw, (paste_x, y_front, paste_x + bw, y_front + bh), offset=12)
                    draw_safe_cutting_guides(draw, (paste_x, y_back, paste_x + bw, y_back + bh), offset=12)

                    st.image(final_canvas, caption="4x6 Print Preview", width=450)

                    id_buffer = io.BytesIO()
                    final_canvas.save(id_buffer, format="PNG", dpi=(300, 300))

                    st.download_button(
                        label="Download 4x6 PNG",
                        data=id_buffer.getvalue(),
                        file_name="Aadhaar_4x6_Layout.png",
                        mime="image/png",
                        use_container_width=True,
                        key="dl_aadhaar_btn"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

# ------------------------------------------
# Tab 2: Senior Citizen Card (Separation Fix)
# ------------------------------------------
with tab2:
    sc_file = st.file_uploader("Senior Citizen Card PDF / Image Upload Kara:", type=["pdf", "png", "jpg", "jpeg"], key="sc_uploader")

    if sc_file is not None:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            split_front = st.slider("Front Card Cut (वरून कुठपर्यंत %)", 15.0, 32.0, 24.0, step=0.5, key="sc_f_slider")
        with col_s2:
            split_back = st.slider("Back Card Cut (खालून कुठपर्यंत %)", 35.0, 58.0, 48.0, step=0.5, key="sc_b_slider")

        if st.button("Generate Senior Citizen Card Layout", type="primary", use_container_width=True, key="btn_sc_gen"):
            with st.spinner("Processing chalu ahe..."):
                try:
                    if sc_file.name.lower().endswith(".pdf"):
                        pdf_bytes = sc_file.read()
                        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                        page = doc[0]
                        pix = page.get_pixmap(dpi=400)
                        img_data = pix.tobytes("png")
                        full_img = Image.open(io.BytesIO(img_data)).convert("RGB")
                    else:
                        full_img = Image.open(sc_file).convert("RGB")

                    w, h = full_img.size

                    # Front: Top part (0 ते split_front)
                    front_raw = full_img.crop((0, 0, w, int(h * (split_front / 100.0))))
                    # Back: Middle part (split_front ते split_back)
                    back_raw = full_img.crop((0, int(h * (split_front / 100.0)), w, int(h * (split_back / 100.0))))

                    front_trimmed = trim_white_edges(front_raw)
                    back_trimmed = trim_white_edges(back_raw)

                    PAPER_W, PAPER_HEIGHT = 1200, 1800
                    card_w, card_h = 1040, 595

                    front_resized = front_trimmed.resize((card_w, card_h), Image.Resampling.LANCZOS)
                    back_resized = back_trimmed.resize((card_w, card_h), Image.Resampling.LANCZOS)

                    front_bordered = ImageOps.expand(front_resized, border=4, fill='black')
                    back_bordered = ImageOps.expand(back_resized, border=4, fill='black')

                    bw, bh = front_bordered.size
                    final_canvas = Image.new("RGB", (PAPER_W, PAPER_HEIGHT), "white")

                    paste_x = (PAPER_W - bw) // 2
                    y_front = 180
                    y_back = 950

                    # दोन्ही वेगवेगळे पेस्ट करणे
                    final_canvas.paste(front_bordered, (paste_x, y_front))
                    final_canvas.paste(back_bordered, (paste_x, y_back))

                    draw = ImageDraw.Draw(final_canvas)
                    draw_safe_cutting_guides(draw, (paste_x, y_front, paste_x + bw, y_front + bh), offset=12)
                    draw_safe_cutting_guides(draw, (paste_x, y_back, paste_x + bw, y_back + bh), offset=12)

                    st.image(final_canvas, caption="Senior Citizen 4x6 Print Preview", width=450)

                    buf = io.BytesIO()
                    final_canvas.save(buf, format="PNG", dpi=(300, 300))

                    st.download_button(
                        label="Download Senior Citizen Card (PNG)",
                        data=buf.getvalue(),
                        file_name="Senior_Citizen_Card_4x6.png",
                        mime="image/png",
                        use_container_width=True,
                        key="dl_sc_btn"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

# ------------------------------------------
# Tab 3: Passport Photo Maker
# ------------------------------------------
with tab3:
    uploaded_image = st.file_uploader("Photo Upload Kara:", type=["jpg", "jpeg", "png"], key="pp_uploader")

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Photo", width=120)

        DPI = 300
        paper_option = st.radio(
            "Paper Size:",
            ("4x6 Paper - 9 Photos", "Full A4 Sheet"),
            key="paper_opt",
            horizontal=True
        )

        if st.button("Generate Passport Sheet", type="primary", use_container_width=True, key="btn_pp"):
            with st.spinner("Processing chalu ahe..."):
                try:
                    if "4x6" in paper_option:
                        canvas_w, canvas_h = int(4 * DPI), int(6 * DPI)
                        cols, rows = 3, 3
                        file_suffix = "4x6_9Photos"

                        id_w, id_h = 350, 450
                        resized_id = ImageOps.fit(img, (id_w, id_h), Image.Resampling.LANCZOS)
                        resized_id = ImageOps.expand(resized_id, border=3, fill='black')

                        sheet = Image.new("RGB", (canvas_w, canvas_h), "white")
                        margin_x = (canvas_w - (cols * resized_id.width)) // (cols + 1)
                        margin_y = (canvas_h - (rows * resized_id.height)) // (rows + 1)

                        for r in range(rows):
                            for c in range(cols):
                                x = margin_x + c * (resized_id.width + margin_x)
                                y = margin_y + r * (resized_id.height + margin_y)
                                sheet.paste(resized_id, (x, y))
                    else:
                        canvas_w, canvas_h = int(8.27 * DPI), int(11.69 * DPI)
                        file_suffix = "A4_Sheet"
                        id_w, id_h = int(3.5 / 2.54 * DPI), int(4.5 / 2.54 * DPI)

                        resized_id = ImageOps.fit(img, (id_w, id_h), Image.Resampling.LANCZOS)
                        resized_id = ImageOps.expand(resized_id, border=3, fill='black')

                        sheet = Image.new("RGB", (canvas_w, canvas_h), "white")
                        margin = 25
                        for y in range(margin, canvas_h - id_h, id_h + margin):
                            for x in range(margin, canvas_w - id_w, id_w + margin):
                                sheet.paste(resized_id, (x, y))

                    buffer = io.BytesIO()
                    sheet.save(buffer, format="PNG", dpi=(DPI, DPI))
                    buffer.seek(0)

                    st.image(sheet, caption="Print Preview", width=450)

                    st.download_button(
                        label="Download Photo Sheet (PNG)",
                        data=buffer,
                        file_name=f"Passport_Sheet_{file_suffix}.png",
                        mime="image/png",
                        use_container_width=True,
                        key="dl_pp_btn"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #94A3B8;'>Balaji Cyber Point, Mangaon, Raigad</p>", unsafe_allow_html=True)
