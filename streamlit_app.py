import streamlit as st
import requests
from PIL import Image

# --- CONFIGURATION ---
API_URL = "http://localhost:8001/api/v1/analyze-image"  # Update to actual endpoint

# --- PAGE STYLE ---
st.set_page_config(page_title="CIMCON Digital - Bearing RCFA", layout="centered")

# --- GLOBAL CSS STYLING ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif !important;
            background-color: #ffffff !important;
            color: #0a2240 !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        .title {
            font-size: 2rem;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .subtitle {
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
        }

        .section {
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        .result-card {
            background: #f1f2f6;
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            white-space: pre-wrap;
        }

        .result-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }

        .result-label {
            font-weight: 600;
            display: block;
            margin-top: 1rem;
            margin-bottom: 0.25rem;
        }

        .recommendation-list {
            margin-top: 0.5rem;
            padding-left: 1.2rem;
        }

        .recommendation-list li {
            margin-bottom: 0.4rem;
        }

        .stButton>button {
            background-color: #0a2240;
            color: #fff;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.6rem 1rem;
        }

        .stFileUploader, .stSelectbox, .stRadio {
            font-size: 1rem;
        }

        .stMarkdown {
            white-space: pre-wrap;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="title">🛠️ CIMCON Digital - Bearing RCFA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Root Cause Failure Analysis for Bearings using AI</div>', unsafe_allow_html=True)

# --- INPUT SECTION ---
st.markdown('<div class="section"><b>1️⃣ Upload Bearing Image</b></div>', unsafe_allow_html=True)
image_file = st.file_uploader("Upload Bearing Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if image_file:
    st.image(Image.open(image_file), caption="Uploaded Image", use_container_width=True)

st.markdown('<div class="section"><b>2️⃣ Select Motor Mounting</b></div>', unsafe_allow_html=True)
motor_mounted = st.radio("Select Motor Mounting", ("Yes", "No"), horizontal=True, label_visibility="collapsed")

st.markdown('<div class="section"><b>3️⃣ Select Bearing Type</b></div>', unsafe_allow_html=True)
bearing_type = st.selectbox(
    "Select Bearing Type",
    [
        "ball_bearing",
        "roller_bearing",
        "thrust_bearing",
        "needle_bearing",
        "spherical_bearing",
        "tapered_roller"
    ],
    label_visibility="collapsed"
)

# --- ANALYZE BUTTON ---
st.markdown('<div class="section"></div>', unsafe_allow_html=True)
analyze_btn = st.button("🔍 Analyze Bearing", use_container_width=True)

if analyze_btn:
    if image_file and bearing_type:
        with st.spinner("Analyzing image and generating report..."):
            files = {"image": (image_file.name, image_file.getvalue(), image_file.type)}
            data = {
                "motor_mounted": motor_mounted,
                "bearing_type": bearing_type
            }
            try:
                response = requests.post(API_URL, files=files, data=data)
                if response.status_code == 200:
                    result = response.json()
                    analysis = result.get("analysis", {})
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown('<div class="result-title">📝 Analysis Report</div>', unsafe_allow_html=True)
                    st.markdown(f'<span class="result-label">Observed Damage:</span>{analysis.get("observed_damage", "-")}', unsafe_allow_html=True)
                    st.markdown(f'<span class="result-label">Failure Mode:</span>{analysis.get("failure_mode", "-")}', unsafe_allow_html=True)
                    st.markdown(f'<span class="result-label">Root Cause(s):</span>{"<br>".join(analysis.get("root_cause_analysis", []))}', unsafe_allow_html=True)
                    st.markdown(f'<span class="result-label">Confidence Score:</span>{round(analysis.get("confidence_score", 0)*100)}%', unsafe_allow_html=True)
                    st.markdown('<span class="result-label">Recommendations:</span>', unsafe_allow_html=True)
                    st.markdown('<ul class="recommendation-list">' + ''.join(f"<li>{rec}</li>" for rec in analysis.get("recommendations", [])) + '</ul>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
    else:
        st.error("Please provide all required information.")

# --- FOOTER ---
st.markdown("""
    <hr>
    <center>
    <span style='color: #0a2240; font-size: 0.9rem; font-family: "Montserrat", sans-serif;'>Powered by CIMCON Digital | AI RCFA Demo</span>
    </center>
""", unsafe_allow_html=True)
