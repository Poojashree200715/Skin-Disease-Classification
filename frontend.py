import streamlit as st
from PIL import Image
import time
from datetime import datetime

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="DermaAI | Skin Analysis", page_icon="🩺", layout="wide")

# ---------------------------------------------------
# CUSTOM STYLING — Sidebar dashboard, purple/indigo theme
# ---------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}

    .stApp { background: #F8F7FC; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 1200px; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #EDE9FE;
    }
    .sb-logo {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 1.3rem;
        color: #4C1D95;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 0 1.5rem 0;
    }
    .sb-nav-item {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        padding: 0.65rem 0.9rem;
        border-radius: 10px;
        font-size: 0.9rem;
        color: #6B7280;
        margin-bottom: 0.3rem;
        font-weight: 500;
    }
    .sb-nav-item.active {
        background: #EDE9FE;
        color: #6D28D9;
        font-weight: 700;
    }
    .sb-privacy {
        background: #F5F3FF;
        border-radius: 12px;
        padding: 0.9rem;
        margin-top: 2rem;
        font-size: 0.78rem;
        color: #6D28D9;
    }
    .sb-privacy b { display:block; margin-bottom:0.2rem; }

    /* Top header row */
    .page-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.3rem;
    }
    .page-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: #1E1B2E;
    }
    .page-sub {
        color: #9CA3AF;
        font-size: 0.88rem;
        margin-bottom: 1.3rem;
    }
    .badge-top {
        background: #F5F3FF;
        color: #7C3AED;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.4rem 0.9rem;
        border-radius: 999px;
        border: 1px solid #EDE9FE;
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 14px rgba(76,29,149,0.06);
        border: 1px solid #F1EEFB;
        height: 100%;
    }
    .card-h {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #1E1B2E;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    [data-testid="stFileUploaderDropzone"] {
        border-radius: 14px;
        border: 2px dashed #C4B5FD;
        background: #FAF9FF;
    }

    .upload-meta {
        background: #F5F3FF;
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        font-size: 0.78rem;
        color: #6D28D9;
        margin-top: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Donut */
    .donut-row {
        display: flex;
        align-items: center;
        gap: 1.4rem;
        margin-bottom: 1.2rem;
    }
    .donut {
        width: 96px; height: 96px; border-radius: 50%;
        background: conic-gradient(#7C3AED 0deg, #EDE9FE 0deg);
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .donut-inner {
        width: 76px; height: 76px; background: white; border-radius: 50%;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .donut-inner .pct { font-family:'Poppins',sans-serif; font-weight:800; font-size:1.15rem; color:#4C1D95; }
    .donut-inner .lbl { font-size:0.62rem; color:#9CA3AF; }

    .pred-label { font-size:0.75rem; font-weight:700; color:#7C3AED; text-transform:uppercase; letter-spacing:0.5px; }
    .pred-name { font-family:'Poppins',sans-serif; font-weight:800; font-size:1.35rem; color:#1E1B2E; margin: 0.2rem 0 0.5rem 0; }
    .severity-pill {
        display: inline-flex; align-items:center; gap:0.4rem;
        background:#FEF3C7; color:#92400E; font-size:0.78rem; font-weight:700;
        padding:0.28rem 0.75rem; border-radius:999px;
    }
    .severity-dot { width:7px; height:7px; border-radius:50%; background:#F59E0B; display:inline-block; }

    /* Mini metric cards row */
    .mini-row { display:flex; gap:0.7rem; margin: 1.1rem 0; }
    .mini-card {
        flex:1; background:#FAF9FF; border:1px solid #EDE9FE; border-radius:12px;
        padding:0.7rem 0.5rem; text-align:center;
    }
    .mini-card .ic { font-size:1rem; margin-bottom:0.2rem; }
    .mini-card .mv { font-family:'Poppins',sans-serif; font-weight:700; font-size:0.85rem; color:#1E1B2E; }
    .mini-card .ml { font-size:0.68rem; color:#9CA3AF; text-transform:uppercase; }

    .rec-title { font-size:0.85rem; font-weight:700; color:#1E1B2E; margin: 0.4rem 0 0.7rem 0; }
    .rec-item {
        display:flex; align-items:center; gap:0.6rem; padding:0.5rem 0.7rem;
        font-size:0.85rem; color:#374151; background:#F9FAFB; border-radius:9px; margin-bottom:0.4rem;
    }
    .rec-check {
        width:18px; height:18px; background:#D1FAE5; color:#059669; border-radius:50%;
        display:flex; align-items:center; justify-content:center; font-size:0.65rem; font-weight:700;
        flex-shrink:0;
    }

    .disclaimer-box {
        background: #FAF9FF;
        border: 1px solid #EDE9FE;
        border-radius: 12px;
        padding: 0.8rem 1.1rem;
        font-size: 0.78rem;
        color: #7C7A8C;
        margin-top: 1.2rem;
        text-align: center;
    }

    .empty-state { text-align:center; padding: 3rem 1rem 2rem 1rem; }
    .empty-state .icon { font-size:2.4rem; margin-bottom:0.6rem; opacity:0.5; }
    .empty-state p { color:#9CA3AF; font-size:0.88rem; margin:0; }

    .stButton>button {
        background: linear-gradient(90deg, #7C3AED, #6D28D9);
        color: white; border-radius: 10px; padding: 0.6rem 1.4rem;
        font-weight: 600; border: none; width: 100%; margin-top: 0.7rem;
        box-shadow: 0 4px 14px rgba(124,58,237,0.25);
    }
    .stButton>button:hover { transform: translateY(-1px); }

    .foot { text-align:center; color:#B5B0C9; font-size:0.78rem; margin-top:1.4rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR — visual only, non-functional nav (frontend preview)
# ---------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sb-logo">🩺 DermaAI</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-nav-item">🏠 Dashboard</div>
    <div class="sb-nav-item active">🔬 New Analysis</div>
    <div class="sb-nav-item">🕒 History</div>
    <div class="sb-nav-item">ℹ️ About</div>
    <div class="sb-nav-item">💡 Skin Tips</div>
    <div class="sb-nav-item">⚙️ Settings</div>
    <div class="sb-privacy">
        <b>🔒 Your Privacy Matters</b>
        We do not store your images. All analysis is secure and confidential.
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# UI ONLY — FRONTEND MODULE (Team 1)
# ---------------------------------------------------
# NOTE: Pure frontend. No model loading or prediction logic lives here.
# Team 5 (Preprocessing), Team 4 (CNN Model), Team 2 (Backend/API) will
# plug their pieces into the placeholder block marked below.
# ---------------------------------------------------

st.markdown(f"""
<div class="page-header">
    <div>
        <div class="page-title">Analysis Result</div>
        <div class="page-sub">Here is the result of your skin analysis</div>
    </div>
    <span class="badge-top">🛡️ AI-Powered Skin Analysis</span>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1.15], gap="medium")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-h">📷 Uploaded Image</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("u", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        st.markdown(f'<div class="upload-meta">✅ Image uploaded successfully · {datetime.now().strftime("%b %d, %Y · %I:%M %p")}</div>', unsafe_allow_html=True)
        predict_clicked = st.button("🔍  Analyze Image")
    else:
        predict_clicked = False
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-h">📊 Prediction</div>', unsafe_allow_html=True)

    if uploaded_file is not None and predict_clicked:
        with st.spinner("Analyzing image..."):
            time.sleep(1.2)  # placeholder delay - simulates backend call

        # ---------------------------------------------------
        # PLACEHOLDER RESULT
        # Team 2/4/5 will replace this block with the real call:
        #   result = backend_api.predict(uploaded_file)
        #   disease_name = result["label"]
        #   confidence = result["confidence"]
        # ---------------------------------------------------
        disease_name = "Awaiting Integration"
        confidence_text = "--"
        today_str = datetime.now().strftime("%b %d, %Y")

        st.markdown(f"""
        <div class="donut-row">
            <div class="donut"><div class="donut-inner"><div class="pct">{confidence_text}</div><div class="lbl">Confidence</div></div></div>
            <div>
                <div class="pred-label">Predicted Disease</div>
                <div class="pred-name">{disease_name}</div>
                <span class="severity-pill"><span class="severity-dot"></span> Pending</span>
            </div>
        </div>
        <div class="mini-row">
            <div class="mini-card"><div class="ic">🔬</div><div class="mv">--</div><div class="ml">Condition</div></div>
            <div class="mini-card"><div class="ic">📈</div><div class="mv">--</div><div class="ml">Confidence</div></div>
            <div class="mini-card"><div class="ic">⚠️</div><div class="mv">--</div><div class="ml">Severity</div></div>
            <div class="mini-card"><div class="ic">📅</div><div class="mv">{today_str}</div><div class="ml">Date</div></div>
        </div>
        <div class="rec-title">Recommendations</div>
        <div class="rec-item"><span class="rec-check">✓</span> Preprocessing pipeline — Team 5</div>
        <div class="rec-item"><span class="rec-check">✓</span> CNN model inference — Team 4</div>
        <div class="rec-item"><span class="rec-check">✓</span> API connection — Team 2</div>
        <div class="rec-item"><span class="rec-check">✓</span> Confidence scoring — Team 3</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🔬</div>
            <p>Upload an image and click Analyze to see results here</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-box">
    ⓘ This tool provides AI-based predictions and is not a substitute for professional medical advice.<br>
    Please consult a qualified dermatologist for accurate diagnosis and treatment.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="foot">Frontend Module — Team 1 · Streamlit UI · Skin Disease Classification Project</div>', unsafe_allow_html=True)
