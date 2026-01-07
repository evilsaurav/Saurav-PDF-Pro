import streamlit as st
import fitz  # PyMuPDF (Isse hi Image aur Watermark dono ho jayenge)
import zipfile
from io import BytesIO
from docx import Document # PDF to Word ke liye

# --- Page Config ---
st.set_page_config(page_title="Saurav's PDF Pro Suite", page_icon="🚀", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .block-container { max-width: 850px; padding-top: 2rem; }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white; border-radius: 12px; font-weight: bold;
        border: none; padding: 12px; width: 100%; transition: 0.4s;
    }
    .feature-card {
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-bottom: 25px;
    }
    .dev-note {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white; padding: 30px; border-radius: 20px;
        text-align: center; margin-top: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #1a73e8;'>💎 Saurav's All-in-One PDF Suite</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Professional Tool Built by Saurav Kumar</p>", unsafe_allow_html=True)

# --- Tabs for Tools ---
tabs = st.tabs(["💧 Watermark", "📝 PDF to Word", "🖼️ PDF to Image"])

# 1. WATERMARK TOOL
with tabs[0]:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    wm_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="wm_uploader")
    
    c1, c2 = st.columns(2)
    with c1:
        pos = st.selectbox("Position", ["Top-Right", "Top-Left", "Bottom-Right", "Bottom-Left", "Center"])
        f_size = st.slider("Font Size", 10, 60, 20)
    with c2:
        color_hex = st.color_picker("Text Color", "#1a73e8")
        start_num = st.number_input("Starting Serial", min_value=1, value=1)

    if st.button("Apply Watermark & Sync"):
        if wm_files:
            processed = []
            curr_ser = start_num
            rgb = tuple(int(color_hex.lstrip('#')[i:i+2], 16)/255 for i in (0, 2, 4))
            
            for f in wm_files:
                doc = fitz.open(stream=f.read(), filetype="pdf")
                fname = f.name.replace(".pdf", "")
                for page in doc:
                    w, h = page.rect.width, page.rect.height
                    txt = f"Name: {fname} | Serial: {curr_ser}"
                    tw = len(txt) * (f_size * 0.5)
                    if "Right" in pos: x = w - tw - 40
                    elif "Left" in pos: x = 40
                    else: x = (w-tw)/2
                    y = 50 if "Top" in pos else (h-50 if "Bottom" in pos else h/2)
                    
                    page.insert_text((x, y), txt, fontsize=f_size, color=rgb)
                
                buf = BytesIO()
                doc.save(buf)
                processed.append((f"WM_{f.name}", buf.getvalue()))
                curr_ser += 1
            
            zip_buf = BytesIO()
            with zipfile.ZipFile(zip_buf, "a") as z:
                for n, d in processed: z.writestr(n, d)
            st.download_button("🎁 Download All Watermarked (ZIP)", zip_buf.getvalue(), "Saurav_Watermarked.zip")
    st.markdown("</div>", unsafe_allow_html=True)

# 2. PDF TO WORD TOOL
with tabs[1]:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    word_file = st.file_uploader("Upload PDF to Convert", type="pdf", key="word_uploader")
    if st.button("Convert to Word (.docx)"):
        if word_file:
            doc = fitz.open(stream=word_file.read(), filetype="pdf")
            word_doc = Document()
            for page in doc:
                word_doc.add_paragraph(page.get_text())
            
            word_buf = BytesIO()
            word_doc.save(word_buf)
            st.download_button("📥 Download Word File", word_buf.getvalue(), f"{word_file.name.replace('.pdf','')}.docx")
    st.markdown("</div>", unsafe_allow_html=True)

# 3. PDF TO IMAGE TOOL
with tabs[2]:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    img_file = st.file_uploader("Upload PDF to extract images", type="pdf", key="img_uploader")
    if st.button("Convert Pages to JPG"):
        if img_file:
            # FITZ (PyMuPDF) ka use karke image conversion (No pdf2image needed!)
            doc = fitz.open(stream=img_file.read(), filetype="pdf")
            img_zip = BytesIO()
            with zipfile.ZipFile(img_zip, "a") as z:
                for i in range(len(doc)):
                    page = doc.load_page(i)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # High Quality
                    z.writestr(f"Page_{i+1}.jpg", pix.tobytes("jpg"))
            st.download_button("📥 Download All Images (ZIP)", img_zip.getvalue(), "PDF_to_Images.zip")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Developer Note ---
st.markdown(f"""
    <div class="dev-note">
        <h3>✨ Note from Developer: Saurav Kumar ✨</h3>
        <p>"Solving complex PDF tasks with a single click. Efficiency is the key to success."</p>
        <p><b>Designed & Developed with ❤️ by Saurav</b></p>
    </div>
    """, unsafe_allow_html=True)
