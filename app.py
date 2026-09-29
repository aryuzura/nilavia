import os
import base64
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu


# ============================================================
# 1. KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="NILAVIA | Academic Self-Management",
    page_icon=os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logo.png"),
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. TEMA
# ============================================================
for key, value in {
    "theme.base": "light",
    "theme.primaryColor": "#45a5a5",
    "theme.backgroundColor": "#dcefe7",
    "theme.secondaryBackgroundColor": "#ffffff",
    "theme.textColor": "#1f2937"
}.items():
    try:
        st._config.set_option(key, value)
    except Exception:
        pass


# ============================================================
# 3. CSS
# ============================================================
st.markdown("""
<style>

:root {
    --navy: #0f2a43;
    --teal: #45a5a5;
    --yellow: #f8c420;
    --green: #059669;
    --orange: #d97706;
    --red: #dc2626;
    --gray: #4b5563;
}

/* GLOBAL */
.stApp,
[data-testid="stAppViewContainer"],
section[data-testid="stMain"] {
    background: linear-gradient(160deg, #eaf6f0 0%, #d8eee4 55%, #c7e7db 100%) !important;
    color: #1f2937;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1300px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2a43 0%, #1b5566 55%, #45a5a5 100%);
}
section[data-testid="stSidebar"] h1 { color: #ffffff !important; }

/* HEADINGS */
h1, h2, h3, h4 {
    font-family: "Inter", "Segoe UI", sans-serif;
    font-weight: 700 !important;
    color: var(--navy) !important;
    letter-spacing: -0.01em;
}
.nilavia-section-title {
    color: #0f2a43 !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
    margin: 1.6rem 0 0.85rem 0 !important;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid rgba(69, 165, 165, 0.25);
    display: inline-block;
}
h4.text-maintain { color: var(--green) !important; }
h4.text-adjust   { color: var(--orange) !important; }
h4.text-support  { color: var(--red) !important; }

/* BANNER */
.nilavia-banner {
    position: relative;
    background: linear-gradient(115deg, #0f2a43 0%, #174d60 62%, #45a5a5 100%);
    padding: 1.35rem 1.6rem;
    border: 2px dashed #9edbd5;
    border-radius: 0.35rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 5px 16px rgba(15, 42, 67, 0.16);
}
.nilavia-banner::before,
.nilavia-banner::after {
    content: "";
    position: absolute;
    top: 50%;
    width: 18px;
    height: 18px;
    background: #d8eee4;
    border-radius: 50%;
    transform: translateY(-50%);
}
.nilavia-banner::before { left: -10px; }
.nilavia-banner::after { right: -10px; }
.nilavia-banner h2 {
    color: #ffffff !important;
    margin: 0 0 0.25rem 0;
    font-size: 1.5rem !important;
}
.nilavia-banner p, .nilavia-banner span {
    color: #e1edf0 !important;
    margin: 0.45rem 0 0 0;
    font-size: 0.92rem;
}
.nilavia-banner b {
    color: #9edbd5 !important;
    letter-spacing: 0;
    font-size: 0.78rem;
}
@media (max-width: 640px) {
    .nilavia-banner { padding: 1rem 1.1rem; }
    .nilavia-banner h2 { font-size: 1.25rem !important; }
}

/* TOP NAVIGATION */
.nav-brand {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.7rem 0 1.6rem;
}
.nav-brand-logo {
    display: block;
    flex: 0 0 176px;
    width: 176px;
    height: 120px;
    object-fit: cover;
    object-position: center;
}
.nav-brand-copy { min-width: 0; }
.nav-brand-subtitle {
    color: #4b6473;
    font-size: 0.92rem;
    line-height: 1.4;
    margin-top: 0.55rem;
}
.nav-brand-subtitle span { color: #45a5a5; }

/* BUTTON */
.stButton > button {
    background: linear-gradient(90deg, #45a5a5, #0f2a43) !important;
    color: #ffffff !important;
    border-radius: 0.6rem !important;
    border: none !important;
    padding: 0.7rem 1.5rem !important;
    font-weight: 600 !important;
    width: 100%;
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #0f2a43, #45a5a5) !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 14px rgba(15, 42, 67, 0.3) !important;
}

/* CARD */
.nilavia-card {
    background: #ffffff;
    border-left: 5px solid var(--teal);
    padding: 1.1rem 1.25rem;
    border-radius: 0.75rem;
    box-shadow: 0 2px 8px rgba(15, 42, 67, 0.08);
    margin-bottom: 1rem;
    transition: transform 160ms ease, box-shadow 160ms ease;
}
.nilavia-card ul { margin: 0.5rem 0 0 0; padding-left: 1.1rem; }
.nilavia-card li { margin-bottom: 0.5rem; color: #374151; }

/* STATUS CARD */
.status-card {
    padding: 1.1rem 1.25rem;
    border-radius: 0.85rem;
    margin-bottom: 1rem;
    border-left: 5px solid;
    box-shadow: 0 2px 8px rgba(15, 42, 67, 0.08);
    transition: transform 160ms ease, box-shadow 160ms ease;
}
.nilavia-card:hover,
.status-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 14px rgba(15, 42, 67, 0.14);
}
@media (prefers-reduced-motion: reduce) {
    .nilavia-card,
    .status-card { transition: none; }
}
.status-card h4 { margin: 0 0 0.4rem 0 !important; font-size: 1.05rem !important; }
.status-card p {
    margin: 0 !important;
    color: #374151 !important;
    font-size: 0.9rem;
    line-height: 1.55;
}
.status-card.maintain {
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    border-left-color: #059669;
}
.status-card.maintain h4 { color: #059669 !important; }
.status-card.adjust {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    border-left-color: #d97706;
}
.status-card.adjust h4 { color: #d97706 !important; }
.status-card.support {
    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    border-left-color: #dc2626;
}
.status-card.support h4 { color: #dc2626 !important; }

/* COMPARISON CARDS (Simulasi) */
.cmp-card {
    padding: 1.1rem 1.5rem;
    background-position: center;
    background-size: 100% 100%;
    background-repeat: no-repeat;
    filter: drop-shadow(0 3px 8px rgba(15, 42, 67, 0.14));
    height: 100%;
    min-height: 165px;
    position: relative;
    transition: transform 160ms ease, filter 160ms ease;
}
.cmp-card:hover {
    transform: translateY(-3px);
    filter: drop-shadow(0 7px 12px rgba(15, 42, 67, 0.2));
}
.cmp-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
    margin-top: 0.5rem;
}

.cmp-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #6b7280;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.55rem;
}
.cmp-value {
    font-size: 1.35rem;
    font-weight: 800;
    color: #0f2a43;
    line-height: 1.2;
    margin-bottom: 0.3rem;
}
.cmp-value.risk { font-size: 1.9rem; color: #0f2a43; }
.cmp-sub { font-size: 0.82rem; color: #6b7280; margin-top: 0.3rem; line-height: 1.45; }

.cmp-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    margin-top: 0.5rem;
}
.badge-good    { background: #d1fae5; color: #065f46; }
.badge-warning { background: #fef3c7; color: #92400e; }
.badge-danger  { background: #fee2e2; color: #991b1b; }

/* IMPORTANT NOTE */
.cmp-important {
    background: linear-gradient(90deg, #fff7ed 0%, #fef3c7 100%);
    border-left: 4px solid #f8c420;
    border-radius: 0.6rem;
    padding: 0.75rem 1rem;
    margin-top: 0.9rem;
    font-size: 0.88rem;
    color: #78350f;
}
.cmp-important b { color: #0f2a43; }

/* HEALTH BREAKDOWN */
.health-card {
    background: #ffffff;
    border-radius: 0.85rem;
    padding: 1rem 1.15rem;
    box-shadow: 0 2px 10px rgba(15, 42, 67, 0.08);
    margin-top: 0.6rem;
    border-top: 5px solid #45a5a5;
}
.health-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px dashed #e5e7eb;
    font-size: 0.88rem;
}
.health-row:last-child { border-bottom: none; }
.health-label { color: #4b5563; font-weight: 500; }
.health-val { font-weight: 700; color: #0f2a43; }

.health-summary {
    background: #f0f9ff;
    border-left: 4px solid #45a5a5;
    border-radius: 0.6rem;
    padding: 0.8rem 1rem;
    margin-top: 0.85rem;
    font-size: 0.88rem;
    color: #1f2937;
    line-height: 1.55;
}
.health-summary b { color: #0f2a43; }

/* DAY PLAN */
.day-plan-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 0.75rem;
    padding: 0.9rem 1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 6px rgba(15, 42, 67, 0.05);
    min-height: 230px;
    display: flex;
    flex-direction: column;
}
.day-title {
    font-weight: 800;
    color: #0f2a43;
    font-size: 0.95rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #45a5a5;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.day-count {
    font-size: 0.7rem;
    background: #e0f2f1;
    color: #0f2a43;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 700;
}

/* PLOTLY */
div[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border-radius: 0.75rem;
    padding: 0.5rem;
    box-shadow: 0 2px 8px rgba(15, 42, 67, 0.08);
    overflow: hidden;
}

/* INPUT */
[data-testid="stWidgetLabel"] p {
    color: var(--navy) !important;
    font-weight: 600;
    font-size: 0.9rem;
}
div[data-baseweb="select"] > div,
div[data-baseweb="input"] {
    background: #ffffff !important;
    border-radius: 0.6rem !important;
}
div[data-baseweb="select"] > div { border: 1px solid #cbd5e1 !important; }
div[data-baseweb="select"] *,
div[data-baseweb="input"] input,
[data-testid="stNumberInput"] input {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}
div[data-baseweb="select"] svg { fill: #0f2a43 !important; }
[data-testid="stNumberInput"] button {
    background: #ffffff !important;
    color: #0f2a43 !important;
}

/* POPOVER */
div[data-baseweb="popover"] [role="listbox"],
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
div[data-baseweb="menu"],
div[data-baseweb="popover"] [role="option"] {
    background: #0f2a43 !important;
    color: #f8fafc !important;
}
div[data-baseweb="popover"] [role="option"] * {
    color: #f8fafc !important;
}
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] [role="option"]:hover,
div[data-baseweb="popover"] [role="option"][aria-selected="true"] {
    background: #1b5566 !important;
    color: #ffffff !important;
}

/* TEXT */
div[role="radiogroup"] label *,
[data-testid="stCheckbox"] label * {
    color: #1f2937 !important;
    font-size: 0.9rem !important;
}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {
    color: #4b5563 !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.25rem;
    border-bottom: 2px solid #e5e7eb;
    padding: 0 0.25rem;
}
.stTabs [data-baseweb="tab"] {
    padding: 0.55rem 1rem;
    border-radius: 0.5rem 0.5rem 0 0;
    background: transparent;
}
.stTabs [data-baseweb="tab"] p {
    color: #6b7280 !important;
    font-weight: 600;
    font-size: 0.88rem;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #ffffff;
    border-bottom: 2px solid #45a5a5;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] p {
    color: #0f2a43 !important;
    font-weight: 800;
}

/* METRIC */
div[data-testid="stMetric"] {
    background: #ffffff;
    border-left: 5px solid #45a5a5;
    padding: 0.8rem 1rem;
    border-radius: 0.6rem;
    box-shadow: 0 2px 8px rgba(15, 42, 67, 0.08);
    height: 100%;
}
div[data-testid="stMetric"] * { color: #0f2a43 !important; }
div[data-testid="stMetricLabel"] * {
    font-size: 0.75rem !important;
    color: #6b7280 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    font-size: 1.2rem !important;
    white-space: normal !important;
    overflow: visible !important;
    line-height: 1.25 !important;
}

/* SCALLOPED SUMMARY CARDS */
.summary-card-grid {
    display: grid;
    grid-template-columns: 1.25fr 1fr 1.5fr;
    gap: 0.75rem;
    align-items: stretch;
    margin-bottom: 1.1rem;
}
.summary-card {
    min-width: 0;
    min-height: 7rem;
    padding: 1rem 1.25rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background-position: center;
    background-size: 100% 100%;
    background-repeat: no-repeat;
    filter: drop-shadow(0 3px 7px rgba(15, 42, 67, 0.12));
    transition: transform 160ms ease, filter 160ms ease;
}
.summary-card:hover {
    transform: translateY(-4px) scale(1.015);
    filter: drop-shadow(0 6px 10px rgba(15, 42, 67, 0.18));
}
.summary-card-label {
    color: #4b6473;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0.35rem;
}
.summary-card-value {
    color: #0f2a43;
    font-size: 1.15rem;
    font-weight: 700;
    line-height: 1.3;
    overflow-wrap: anywhere;
}
@media (max-width: 700px) {
    .summary-card-grid,
    .cmp-grid { grid-template-columns: 1fr; }
    .cmp-card { height: auto; min-height: 0; }
}
@media (prefers-reduced-motion: reduce) {
    .summary-card { transition: none; }
}

/* ALERT */
[data-testid="stAlert"] {
    background: #ffffff !important;
    border-left: 5px solid #45a5a5 !important;
    border-radius: 0.6rem;
    box-shadow: 0 2px 8px rgba(15, 42, 67, 0.08);
    padding: 0.9rem 1rem;
}
[data-testid="stAlert"] * { color: #1f2937 !important; }

/* INDICATOR CARD */
.indicator-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.7rem 0.9rem;
    align-items: stretch;
}
.indicator-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-left: 4px solid #45a5a5;
    border-radius: 0.7rem;
    padding: 0.9rem 1rem;
    min-width: 0;
    box-shadow: 0 2px 6px rgba(15, 42, 67, 0.05);
}
.indicator-title {
    font-weight: 700;
    color: #0f2a43;
    margin-bottom: 0.3rem;
    font-size: 0.9rem;
}
.indicator-value { font-size: 1.05rem; font-weight: 700; color: #0f2a43; }
.indicator-description {
    font-size: 0.83rem;
    color: #4b5563;
    margin-top: 0.35rem;
    line-height: 1.5;
}
.status-good   { color: #059669; font-weight: 700; font-size: 0.78rem; }
.status-medium { color: #d97706; font-weight: 700; font-size: 0.78rem; }
.status-low    { color: #dc2626; font-weight: 700; font-size: 0.78rem; }
@media (max-width: 640px) {
    .indicator-grid { grid-template-columns: 1fr; }
}

/* INFO BOX */
.info-box {
    background: #f0f9ff;
    border-left: 4px solid #45a5a5;
    padding: 0.75rem 1rem;
    border-radius: 0.6rem;
    margin-bottom: 1rem;
}
.info-box b { color: #0f2a43; }
.info-box span { color: #4b5563; font-size: 0.88rem; }

</style>
""", unsafe_allow_html=True)


# ============================================================
# 4. MODEL
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_model():
    return joblib.load(os.path.join(BASE_DIR, "nilavia_xgb_model.pkl"))

try:
    model = load_model()
except Exception as e:
    st.error(
        f"Model gagal dimuat: {type(e).__name__}: {e}. "
        "Jika muncul 'No module named xgboost', jalankan: python -m pip install xgboost"
    )
    model = None


# ============================================================
# 5. SESSION STATE
# ============================================================
DAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]

if "ran" not in st.session_state:
    st.session_state["ran"] = False
if "history" not in st.session_state:
    st.session_state["history"] = []
if "last" not in st.session_state:
    st.session_state["last"] = None
if "celebrated" not in st.session_state:
    st.session_state["celebrated"] = False
if "action_plans" not in st.session_state:
    st.session_state["action_plans"] = {day: [] for day in DAYS}
if "task_counter" not in st.session_state:
    st.session_state["task_counter"] = 0
if "plan_source" not in st.session_state:
    st.session_state["plan_source"] = None


# ============================================================
# 6. MAPPING
# ============================================================
DICT_DATANG = {"Selalu (Sering Telat)": 1, "Jarang": 2, "Tidak Pernah Telat": 3}
DICT_TUGAS  = {"Jarang": 1, "Selalu": 3}
DICT_TANYA  = {"Tak Pernah": 1, "Sesekali": 2, "Sering": 3, "Selalu": 4}
DICT_PAHAM  = {"Tak Paham Satupun Mk": 0, "30(%)": 30, "50(%)": 50, "100(%)": 100}
DICT_HADIR  = {"40(%)": 40, "60(%)": 60, "80(%)": 80, "100(%)": 100}


# ============================================================
# 7. HELPERS
# ============================================================
def render_header_banner(title, subtitle):
    st.markdown(
        f'<div class="nilavia-banner">'
        f'<h2>{title}</h2>'
        f'<b>MANAGE SMARTER, NOT PUSH HARDER.</b>'
        f'<p>{subtitle}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


def render_section(title):
    st.markdown(f'<div class="nilavia-section-title">{title}</div>',
                unsafe_allow_html=True)


def scalloped_card_background(fill, stroke, width=320, height=120):
    path = ["M 16 8"]

    x = 16
    index = 0
    while x < width - 16:
        next_x = min(x + 12, width - 16)
        control_y = 2 if index % 2 == 0 else 14
        path.append(f"Q {(x + next_x) / 2:g} {control_y} {next_x} 8")
        x = next_x
        index += 1

    path.append(f"Q {width - 8} 8 {width - 8} 16")
    y = 16
    index = 0
    while y < height - 16:
        next_y = min(y + 12, height - 16)
        control_x = width - 2 if index % 2 == 0 else width - 14
        path.append(f"Q {control_x} {(y + next_y) / 2:g} {width - 8} {next_y}")
        y = next_y
        index += 1

    path.append(f"Q {width - 8} {height - 8} {width - 16} {height - 8}")
    x = width - 16
    index = 0
    while x > 16:
        next_x = max(x - 12, 16)
        control_y = height - 2 if index % 2 == 0 else height - 14
        path.append(f"Q {(x + next_x) / 2:g} {control_y} {next_x} {height - 8}")
        x = next_x
        index += 1

    path.append(f"Q 8 {height - 8} 8 {height - 16}")
    y = height - 16
    index = 0
    while y > 16:
        next_y = max(y - 12, 16)
        control_x = 2 if index % 2 == 0 else 14
        path.append(f"Q {control_x} {(y + next_y) / 2:g} 8 {next_y}")
        y = next_y
        index += 1
    path.append("Q 8 8 16 8 Z")

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        'preserveAspectRatio="none">'
        f'<path d="{" ".join(path)}" fill="{fill}" stroke="{stroke}" '
        'stroke-width="2" stroke-linejoin="round"/></svg>'
    )
    return base64.b64encode(svg.encode("ascii")).decode("ascii")


def render_summary_cards(cards):
    image = scalloped_card_background("#ffffff", "#45a5a5")
    items = "".join(
        '<div class="summary-card" '
        f'style="background-image:url(data:image/svg+xml;base64,{image});">'
        f'<div class="summary-card-label">{label}</div>'
        f'<div class="summary-card-value">{value}</div>'
        '</div>'
        for label, value in cards
    )
    st.markdown(
        f'<div class="summary-card-grid">{items}</div>',
        unsafe_allow_html=True
    )


def get_status_label(pred):
    return {0: "🟢 MAINTAIN", 1: "🟡 ADJUST", 2: "🔴 SEEK SUPPORT"}.get(int(pred), "UNKNOWN")


def calculate_scores(datang, tugas, tanya, paham, hadir, ip):
    s_datang = (DICT_DATANG[datang] / 3) * 100
    s_tugas  = (DICT_TUGAS[tugas] / 3) * 100
    s_tanya  = (DICT_TANYA[tanya] / 4) * 100
    s_paham  = DICT_PAHAM[paham]
    s_hadir  = DICT_HADIR[hadir]
    s_ip     = (ip / 4.0) * 100
    overall  = np.mean([s_datang, s_tugas, s_tanya, s_paham, s_hadir, s_ip])
    return s_datang, s_tugas, s_tanya, s_paham, s_hadir, s_ip, overall


def calculate_risk(proba):
    return float(proba[1] * 50 + proba[2] * 100)


def get_indicator_status(value):
    if value >= 80:   return "Baik", "status-good"
    elif value >= 60: return "Perlu dijaga", "status-medium"
    else:             return "Perlu perhatian", "status-low"


def get_indicator_description(name, value):
    m = {
        "Kedisiplinan": ["Kedisiplinan waktu terlihat konsisten.",
                         "Masih terdapat beberapa keterlambatan yang perlu diperhatikan.",
                         "Keterlambatan cukup sering dan perlu diperbaiki."],
        "Konsistensi Tugas": ["Pengumpulan tugas cukup konsisten.",
                              "Beberapa tugas masih perlu dikelola lebih teratur.",
                              "Konsistensi pengumpulan tugas perlu menjadi perhatian."],
        "Partisipasi": ["Partisipasi dalam proses pembelajaran cukup aktif.",
                        "Partisipasi masih dapat ditingkatkan.",
                        "Interaksi dalam pembelajaran masih relatif rendah."],
        "Pemahaman Materi": ["Pemahaman materi berada pada tingkat yang baik.",
                             "Beberapa materi masih perlu dipelajari kembali.",
                             "Pemahaman materi perlu mendapatkan perhatian lebih."],
        "Kehadiran": ["Kehadiran cukup konsisten.",
                      "Terdapat beberapa ketidakhadiran yang perlu dievaluasi.",
                      "Tingkat kehadiran cukup rendah."],
        "IP": ["Capaian IP berada pada tingkat yang baik.",
               "Capaian IP masih dapat ditingkatkan.",
               "Capaian IP perlu menjadi salah satu fokus evaluasi."],
    }
    if name not in m:
        return "Belum ada keterangan."
    return m[name][0] if value >= 80 else m[name][1] if value >= 60 else m[name][2]


def render_indicator_details(indicators):
    st.markdown(
        '<div class="info-box">'
        '<b>Penjelasan Indikator</b><br>'
        '<span>Setiap indikator menunjukkan kondisi akademik berdasarkan data yang kamu masukkan.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    cards = []
    for idx, (name, value) in enumerate(indicators.items()):
        status, status_class = get_indicator_status(value)
        desc = get_indicator_description(name, value)
        cards.append(
            f'<div class="indicator-card">'
            f'<div class="indicator-title">{name}</div>'
            f'<div class="indicator-value">{value:.0f}% '
            f'<span class="{status_class}">• {status}</span></div>'
            f'<div class="indicator-description">{desc}</div>'
            f'</div>'
        )
    st.markdown(
        f'<div class="indicator-grid">{"".join(cards)}</div>',
        unsafe_allow_html=True
    )


def render_status(prediction):
    config = {
        0: ("maintain", "🟢 MAINTAIN (STABIL)",
            "Kondisi akademikmu relatif stabil. Pertahankan kebiasaan yang sudah berjalan baik."),
        1: ("adjust", "🟡 ADJUST (PERLU PENYESUAIAN)",
            "Terdapat beberapa indikator yang perlu diperhatikan. Lakukan penyesuaian pada kebiasaan belajar."),
        2: ("support", "🔴 SEEK SUPPORT (BUTUH PERHATIAN)",
            "Beberapa indikator perlu perhatian lebih. Pertimbangkan mencari dukungan akademik."),
    }
    cls, title, desc = config.get(int(prediction), config[0])
    st.markdown(
        f'<div class="status-card {cls}">'
        f'<h4>{title}</h4>'
        f'<p>{desc}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


def generate_issues(datang, tugas, paham, hadir, ip):
    issues = []
    if DICT_TUGAS[tugas] == 1:         issues.append("Pengumpulan Tugas Menurun")
    if DICT_PAHAM[paham] <= 30:        issues.append("Pemahaman Materi Rendah")
    if DICT_HADIR[hadir] <= 60:        issues.append("Tingkat Kehadiran Rendah")
    if DICT_DATANG[datang] == 1:       issues.append("Sering Terlambat / Kedisiplinan Waktu")
    if ip < 3.3:                        issues.append("Indeks Prestasi Perlu Ditingkatkan")
    return issues


def render_explanation(issues):
    render_section("04 EXPLAIN")

    if not issues:
        st.markdown(
            '<div class="nilavia-card">'
            '<p style="color:#374151;margin:0;">'
            '💡 Tidak terdapat indikator utama yang berada pada kondisi perhatian. '
            'Tetap lakukan evaluasi secara berkala.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )
        return

    items = "".join(
        f'<li style="margin-bottom:0.4rem;">⚠️ {i}</li>' for i in issues
    )
    st.markdown(
        '<div class="nilavia-card">'
        '<b style="color:#1f2937;">Area yang Perlu Perhatian:</b>'
        f'<ul style="margin-top:0.6rem;color:#374151;">{items}</ul>'
        '</div>',
        unsafe_allow_html=True
    )


def render_platform_links():
    platforms = [
        ("https://www.ruangguru.com", "ruangguru.png", "Ruangguru"),
        ("https://www.zenius.net", "zenius.png", "Zenius"),
        ("https://pahamify.com", "pahamify.png", "Pahamify"),
    ]
    links = []
    for url, image_name, name in platforms:
        image_path = os.path.join(BASE_DIR, image_name)
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("ascii")
        links.append(
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
            'style="display:inline-flex;align-items:center;gap:7px;'
            'text-decoration:none;background:#f3f4f6;color:#1f2937;'
            'padding:6px 12px;border-radius:7px;border:1px solid #e5e7eb;'
            'font-weight:600;font-size:0.85rem;">'
            f'<img src="data:image/png;base64,{image_data}" alt="" '
            'style="width:18px;height:18px;object-fit:contain;">'
            f'{name}</a>'
        )
    st.markdown(
        '<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;">'
        + "".join(links)
        + '</div>',
        unsafe_allow_html=True
    )


def render_recommendations(issues, prediction):
    render_section("05 & 06 RECOMMEND & MANAGE")

    recs = []
    if not issues and prediction == 0:
        recs.extend([
            ("Jaga Ritme", "Pertahankan pola belajar yang sudah berjalan baik."),
            ("Evaluasi Berkala", "Lakukan check-in rutin agar perubahan terlihat lebih awal."),
            ("Berikan Waktu Istirahat", "Seimbangkan belajar dengan istirahat agar ritme tetap stabil."),
        ])
    else:
        if "Pengumpulan Tugas Menurun" in issues:
            recs.append(("Kelola Tugas", "Buat to-do list berdasarkan deadline; pecah tugas besar."))
        if "Pemahaman Materi Rendah" in issues:
            recs.append(("Pelajari Ulang Materi", "Gunakan catatan, video, atau latihan soal."))
            recs.append(("Diskusi", "Diskusikan materi sulit dengan teman, tutor, atau dosen."))
        if "Tingkat Kehadiran Rendah" in issues:
            recs.append(("Perbaiki Kehadiran", "Evaluasi penyebab dan buat pengingat jadwal."))
        if "Sering Terlambat / Kedisiplinan Waktu" in issues:
            recs.append(("Atur Persiapan", "Siapkan perlengkapan sebelumnya; gunakan alarm."))
        if "Indeks Prestasi Perlu Ditingkatkan" in issues:
            recs.append(("Evaluasi Prioritas", "Identifikasi mata kuliah yang butuh perhatian lebih."))
            recs.append(("Target Bertahap", "Buat target akademik realistis dan evaluasi berkala."))

    items = "".join(
        f'<li style="margin-bottom:0.65rem;">'
        f'<span style="color:#45a5a5;font-size:1rem;">➜</span>'
        f'<b style="color:#1f2937;"> {t}:</b> '
        f'<span style="color:#374151;">{d}</span>'
        f'</li>'
        for t, d in recs
    )
    st.markdown(
        '<div class="nilavia-card">'
        f'<ul style="list-style:none;padding-left:0;margin:0;">{items}</ul>'
        '</div>',
        unsafe_allow_html=True
    )

    if "Pemahaman Materi Rendah" in issues:
        st.markdown(
            '<p style="color:#374151;margin-bottom:5px;"><b>Alternatif sumber belajar:</b></p>',
            unsafe_allow_html=True
        )
        render_platform_links()


# ============================================================
# GAUGE
# ============================================================
def render_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "suffix": "%",
            "font": {"color": "#0f2a43", "size": 34, "family": "Inter"}
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "#cbd5e1",
                "tickfont": {"size": 10, "color": "#94a3b8"},
                "tickvals": [0, 25, 50, 75, 100]
            },
            "bar": {"color": "#45a5a5", "thickness": 0.30},
            "bgcolor": "white",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50],   "color": "rgba(239, 68, 68, 0.08)"},
                {"range": [50, 75],  "color": "rgba(245, 158, 11, 0.08)"},
                {"range": [75, 100], "color": "rgba(16, 185, 129, 0.08)"},
            ],
            "threshold": {
                "line": {"color": "#f8c420", "width": 4},
                "thickness": 0.75,
                "value": score
            }
        }
    ))
    fig.update_layout(
        height=270,
        margin=dict(l=30, r=30, t=15, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#1f2937"
    )
    return fig


# ============================================================
# HEALTH SCORE — FIXED (HTML flat, tidak bocor)
# ============================================================
def render_health_breakdown(indicators, overall):
    sorted_items = sorted(indicators.items(), key=lambda x: x[1])
    worst = sorted_items[0]
    best  = sorted_items[-1]

    if overall >= 80:
        level, level_class = "BAIK", "status-good"
        summary = (
            f"Skor kamu <b>{overall:.1f}/100</b> menunjukkan kondisi akademik "
            "berada pada level <b>baik</b>. Kekuatan utama ada pada "
            f"<b>{best[0]}</b> ({best[1]:.0f}%). Pertahankan ritme belajar dan "
            "lakukan evaluasi berkala agar konsisten."
        )
    elif overall >= 60:
        level, level_class = "CUKUP", "status-medium"
        summary = (
            f"Skor kamu <b>{overall:.1f}/100</b> berada pada level <b>cukup</b>. "
            f"Kekuatan ada pada <b>{best[0]}</b> ({best[1]:.0f}%), namun "
            f"<b>{worst[0]}</b> ({worst[1]:.0f}%) masih menjadi titik lemah "
            "yang perlu ditingkatkan."
        )
    else:
        level, level_class = "PERLU PERHATIAN", "status-low"
        summary = (
            f"Skor kamu <b>{overall:.1f}/100</b> berada pada level "
            "<b>perlu perhatian</b>. Ada beberapa indikator yang butuh "
            f"perbaikan serius, terutama <b>{worst[0]}</b> ({worst[1]:.0f}%) "
            f"dan <b>{sorted_items[1][0]}</b> ({sorted_items[1][1]:.0f}%)."
        )

    rows = "".join(
        f'<div class="health-row">'
        f'<span class="health-label">{name}</span>'
        f'<span class="health-val {get_indicator_status(val)[1]}">{val:.0f}%</span>'
        f'</div>'
        for name, val in sorted(indicators.items(), key=lambda x: -x[1])
    )

    st.markdown(
        '<div class="health-card">'
        '<div style="display:flex;justify-content:space-between;'
        'align-items:center;margin-bottom:0.5rem;">'
        '<b style="color:#0f2a43;font-size:0.95rem;">Breakdown Skor</b>'
        f'<span class="{level_class}" style="font-size:0.8rem;">● {level}</span>'
        '</div>'
        f'{rows}'
        f'<div class="health-summary">{summary}</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# RADAR
# ============================================================
def render_radar(scores):
    categories = ["Kedisiplinan", "Tugas", "Bertanya", "Pemahaman", "Kehadiran", "IP"]
    values = [scores["Kedisiplinan"], scores["Konsistensi Tugas"],
              scores["Partisipasi"], scores["Pemahaman Materi"],
              scores["Kehadiran"], scores["IP"]]
    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(69, 165, 165, 0.30)",
        line=dict(color="#45a5a5", width=2),
        marker=dict(color="#f8c420", size=8)
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100],
                            tickvals=[0, 20, 40, 60, 80, 100],
                            gridcolor="#cbd8df",
                            tickfont=dict(size=14, color="#334155"),
                            ticks="outside", ticklen=4, tickcolor="#64748b"),
            angularaxis=dict(
                gridcolor="#d9e2e8",
                linecolor="#cbd5e1",
                tickfont=dict(size=12, color="#1f2937")
            )
        ),
        showlegend=False,
        height=420,
        margin=dict(l=35, r=35, t=55, b=30),
        paper_bgcolor="white", plot_bgcolor="white",
        font_color="#1f2937"
    )
    return fig


# ============================================================
# COMPARISON CARDS — FIXED
# ============================================================
def status_badge(pred):
    if pred == 0:
        return "Aman", "badge-good"
    elif pred == 1:
        return "Waspada", "badge-warning"
    return "Bahaya", "badge-danger"


def render_comparison_cards(current_pred, sim_pred, current_risk, sim_risk):
    cur_label, cur_badge = status_badge(current_pred)
    sim_label, sim_badge = status_badge(sim_pred)
    current_background = scalloped_card_background("#f0fbf9", "#45a5a5", height=180)
    simulated_background = scalloped_card_background("#f2f6fa", "#0f2a43", height=180)

    delta = sim_risk - current_risk
    if delta < -1:
        delta_variant = "delta-down"
        delta_background = scalloped_card_background("#ecfdf5", "#059669", height=180)
        delta_sub = "Risiko <b>turun</b> dibandingkan kondisi sekarang. Perubahan ini berpotensi positif."
        delta_badge_class, delta_badge_text = "badge-good", "MEMBAIK"
    elif delta > 1:
        delta_variant = "delta-up"
        delta_background = scalloped_card_background("#fef2f2", "#dc2626", height=180)
        delta_sub = "Risiko <b>naik</b> dibandingkan kondisi sekarang. Perlu dievaluasi kembali."
        delta_badge_class, delta_badge_text = "badge-danger", "MEMBURUK"
    else:
        delta_variant = "delta-flat"
        delta_background = scalloped_card_background("#fffbeb", "#d97706", height=180)
        delta_sub = "Risiko <b>relatif sama</b>. Coba ubah indikator lain untuk melihat pengaruhnya."
        delta_badge_class, delta_badge_text = "badge-warning", "STABIL"

    st.markdown(
        '<div class="cmp-grid">'

        '<div class="cmp-card current" '
        f'style="background-image:url(data:image/svg+xml;base64,{current_background});">'
        '<div class="cmp-label">🎯 Status Sekarang</div>'
        f'<div class="cmp-value">{get_status_label(current_pred)}</div>'
        f'<div class="cmp-sub">Level: <b>{cur_label}</b></div>'
        f'<span class="cmp-badge {cur_badge}">{cur_label.upper()}</span>'
        '</div>'

        '<div class="cmp-card simulated" '
        f'style="background-image:url(data:image/svg+xml;base64,{simulated_background});">'
        '<div class="cmp-label">🧪 Status Simulasi</div>'
        f'<div class="cmp-value">{get_status_label(sim_pred)}</div>'
        f'<div class="cmp-sub">Level: <b>{sim_label}</b></div>'
        f'<span class="cmp-badge {sim_badge}">{sim_label.upper()}</span>'
        '</div>'

        f'<div class="cmp-card {delta_variant}" '
        f'style="background-image:url(data:image/svg+xml;base64,{delta_background});">'
        '<div class="cmp-label">📊 Perubahan Risiko</div>'
        f'<div class="cmp-value risk">{delta:+.0f}%</div>'
        f'<div class="cmp-sub">{delta_sub}</div>'
        f'<span class="cmp-badge {delta_badge_class}">{delta_badge_text}</span>'
        '</div>'

        '</div>',
        unsafe_allow_html=True
    )


def render_risk_gauge_compare(current_risk, sim_risk):
    st.markdown(
        '<div style="margin-top:1.2rem;background:#ffffff;border-radius:0.75rem;'
        'padding:1rem 1.15rem;box-shadow:0 2px 10px rgba(15,42,67,0.08);">'

        '<div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">'
        '<b style="color:#0f2a43;font-size:0.88rem;">Skor Risiko Sekarang</b>'
        f'<span style="color:#0f2a43;font-weight:700;">{current_risk:.0f}%</span>'
        '</div>'
        '<div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin-bottom:0.9rem;">'
        f'<div style="background:linear-gradient(90deg,#45a5a5,#0f2a43);'
        f'height:100%;width:{min(current_risk,100):.0f}%;border-radius:10px;"></div>'
        '</div>'

        '<div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">'
        '<b style="color:#0f2a43;font-size:0.88rem;">Skor Risiko Simulasi</b>'
        f'<span style="color:#0f2a43;font-weight:700;">{sim_risk:.0f}%</span>'
        '</div>'
        '<div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;">'
        f'<div style="background:linear-gradient(90deg,#f8c420,#d97706);'
        f'height:100%;width:{min(sim_risk,100):.0f}%;border-radius:10px;"></div>'
        '</div>'

        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# DAY PLAN
# ============================================================
def auto_fill_plan_from_issues(issues, last):
    source = {
        "Pengumpulan Tugas Menurun": ["Buat to-do list tugas"],
        "Pemahaman Materi Rendah": ["Pelajari ulang materi sulit", "Kerjakan latihan soal"],
        "Tingkat Kehadiran Rendah": ["Cek jadwal kuliah besok"],
        "Sering Terlambat / Kedisiplinan Waktu": ["Siapkan perlengkapan malam ini"],
        "Indeks Prestasi Perlu Ditingkatkan": ["Review nilai & target mingguan"],
    }
    tasks = [t for issue in issues for t in source.get(issue, [])]
    if not tasks:
        tasks = ["Evaluasi belajar 15 menit", "Review target mingguan"]

    if last and last.get("study_hours", 0) < 5:
        tasks.append("Tambah waktu belajar bertahap")
    if last and last.get("sleep_hours", 7) < 6:
        tasks.append("Perbaiki jadwal tidur")
    if last and last.get("focus_level", 70) < 50:
        tasks.append("Belajar tanpa distraksi 25 menit")

    st.session_state["action_plans"] = {day: [] for day in DAYS}
    for i, task in enumerate(tasks):
        st.session_state["task_counter"] += 1
        st.session_state["action_plans"][DAYS[i % len(DAYS)]].append({
            "id": st.session_state["task_counter"],
            "task": task
        })


def render_day_plan():
    st.markdown(
        '<div class="info-box">'
        '<b>Rencana Aksi Mingguan</b><br>'
        '<span>Tambahkan rencana belajarmu sendiri untuk setiap hari. '
        'Centang jika sudah selesai, atau hapus jika tidak relevan.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    # PERBAIKAN: Looping per baris (isi 3 kolom per baris) agar urutan hari tidak berantakan
    for i in range(0, len(DAYS), 3):
        cols = st.columns(3, gap="medium")
        for j in range(3):
            if i + j < len(DAYS):
                day = DAYS[i + j]
                with cols[j]:
                    tasks = st.session_state["action_plans"][day]
                    done = sum(1 for t in tasks if st.session_state.get(f"chk_{t['id']}", False))

                    st.markdown(
                        '<div class="day-title">'
                        f'<span>📅 {day}</span>'
                        f'<span class="day-count">{done}/{len(tasks)}</span>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    if tasks:
                        for task in tasks:
                            c_cb, c_del = st.columns([8, 1])
                            with c_cb:
                                st.checkbox(task["task"], key=f"chk_{task['id']}")
                            with c_del:
                                if st.button("✕", key=f"del_{task['id']}", help="Hapus"):
                                    st.session_state["action_plans"][day] = [
                                        t for t in tasks if t["id"] != task["id"]
                                    ]
                                    st.rerun()
                    else:
                        st.caption("_Belum ada rencana._")

                    with st.form(f"form_{day}", clear_on_submit=True):
                        new_text = st.text_input(
                            "Tambah rencana",
                            key=f"new_{day}",
                            placeholder=f"Rencana untuk {day}...",
                            label_visibility="collapsed"
                        )
                        submitted = st.form_submit_button("➕ Tambah", use_container_width=True)
                        if submitted and new_text.strip():
                            st.session_state["task_counter"] += 1
                            st.session_state["action_plans"][day].append({
                                "id": st.session_state["task_counter"],
                                "task": new_text.strip()
                            })
                            st.rerun()

                    st.markdown("<div style='margin-bottom:0.6rem;'></div>", unsafe_allow_html=True)

# ============================================================
# 8. TOP NAVIGATION
# ============================================================
with open(os.path.join(BASE_DIR, "Logo.png"), "rb") as logo_file:
    brand_logo = base64.b64encode(logo_file.read()).decode("ascii")

st.markdown(
    '<div class="nav-brand">'
    f'<img class="nav-brand-logo" src="data:image/png;base64,{brand_logo}" alt="">'
    '<div class="nav-brand-copy">'
    '<div class="nav-brand-subtitle">AI EARLY WARNING '
    '<span>•</span> ACADEMIC SELF-MANAGEMENT</div>'
    '</div></div>',
    unsafe_allow_html=True
)

selected_menu = option_menu(
    menu_title=None,
    options=["Kondisi Akademik", "Prediksi Akademik", "Rencana Belajar"],
    icons=["house", "bar-chart", "check2-square"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0.3rem!important",
            "background-color": "rgba(255,255,255,0.48)",
            "border": "1px solid rgba(69,165,165,0.38)",
            "border-radius": "0.85rem"
        },
        "nav": {"background-color": "transparent"},
        "icon": {"color": "#45a5a5", "font-size": "16px"},
        "nav-link": {
            "font-size": "14px", "text-align": "center", "margin": "3px 4px",
            "color": "#334155", "font-weight": "600",
            "border-radius": "0.6rem", "padding": "0.7rem 0.8rem",
            "--hover-color": "#e5f2f1"
        },
        "nav-link-selected": {
            "background-color": "#0f2a43",
            "color": "#ffffff", "font-weight": "700"
        }
    }
)

st.markdown(
    "<hr style='margin:1.15rem 0 1.35rem 0;border-color:rgba(69,165,165,0.42);'>",
    unsafe_allow_html=True
)


# ============================================================
# 9. KONDISI AKADEMIK
# ============================================================
if selected_menu == "Kondisi Akademik":
    render_header_banner(
        "Kondisi Akademik Saya",
        "Lihat ringkasan kondisi akademik dan indikator yang perlu kamu perhatikan."
    )

    last = st.session_state.get("last")
    if last:
        status_text = {0: "🟢 MAINTAIN (stabil)",
                       1: "🟡 ADJUST (perlu penyesuaian)",
                       2: "🔴 SEEK SUPPORT (butuh perhatian)"}
        st.info(f"**Check-in terakhir:** {status_text[last['pred']]} • "
                f"Skor Risiko **{last['risk']:.0f}%** • IP **{last['ip']:.2f}**")
    else:
        st.info("Data di bawah merupakan contoh tampilan. "
                "Buka menu **Prediksi Akademik** untuk memasukkan data sendiri.")

    dummy_score = 79.0
    dummy_ip = 2.80
    dummy_scores = {
        "Kedisiplinan": 100, "Konsistensi Tugas": 100, "Partisipasi": 75,
        "Pemahaman Materi": 30, "Kehadiran": 100, "IP": (dummy_ip / 4) * 100
    }

    display_score = float(last.get("overall", dummy_score)) if last else dummy_score
    display_ip = float(last.get("ip", dummy_ip)) if last else dummy_ip
    display_indicators = last.get("indicators", dummy_scores) if last else dummy_scores
    display_prediction = int(last.get("pred", 1)) if last else 1
    display_issues = last.get("issues", []) if last else ["Pemahaman Materi Rendah"]
    primary_focus = display_issues[0] if display_issues else "Pertahankan ritme"

    render_summary_cards([
        ("Skor Keseluruhan", f"{display_score:.1f}/100"),
        ("Capaian IP", f"{display_ip:.2f}/4.00"),
        ("Fokus Utama", primary_focus),
    ])

    col_viz, col_text = st.columns([1.2, 1], gap="large")

    with col_viz:
        render_section("📊 AI ANALYSIS VISUALIZATION")
        tab1, tab2 = st.tabs(["📈  Overall Performance", "🕸️  Radar Indikator"])
        with tab1:
            st.plotly_chart(render_gauge(display_score), use_container_width=True, theme=None)
            render_health_breakdown(display_indicators, display_score)
        with tab2:
            st.plotly_chart(render_radar(display_indicators), use_container_width=True, theme=None)
            render_indicator_details(display_indicators)

    with col_text:
        render_section("03 PREDICT")
        render_status(display_prediction)
        render_explanation(display_issues)
        render_recommendations(display_issues, display_prediction)


# ============================================================
# 10. PREDIKSI AKADEMIK
# ============================================================
elif selected_menu == "Prediksi Akademik":
    render_header_banner(
        "Analisis Kondisi Akademik",
        "Masukkan data akademik dan kebiasaan belajarmu untuk mendapatkan analisis dari model AI."
    )

    render_section("01 COLLECT")

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        datang = st.selectbox("Kedisiplinan (Datang)",
                              ["Tidak Pernah Telat", "Jarang", "Selalu (Sering Telat)"])
        tugas = st.selectbox("Konsistensi (Kumpul Tugas)", ["Selalu", "Jarang"])
    with col2:
        tanya = st.selectbox("Partisipasi (Bertanya)",
                             ["Selalu", "Sering", "Sesekali", "Tak Pernah"])
        paham = st.selectbox("Persepsi (Pemahaman Materi)",
                             ["100(%)", "50(%)", "30(%)", "Tak Paham Satupun Mk"], index=2)
    with col3:
        hadir = st.selectbox("Keterlibatan (Kehadiran)",
                             ["100(%)", "80(%)", "60(%)", "40(%)"])
        ip = st.number_input("Capaian Akademik (IP)",
                             min_value=0.00, max_value=4.00, value=2.80, step=0.01)

    render_section("🧠 PROFIL KEBIASAAN BELAJAR")
    st.caption("Data berikut digunakan untuk membantu evaluasi kebiasaan dan rekomendasi. "
               "Pada versi model saat ini, data tersebut belum menjadi input XGBoost.")

    p1, p2, p3 = st.columns(3)
    with p1:
        study_hours = st.slider("Rata-rata waktu belajar per minggu",
                                min_value=0, max_value=40, value=7, step=1)
    with p2:
        sleep_hours = st.slider("Rata-rata tidur per malam",
                                min_value=3.0, max_value=10.0, value=7.0, step=0.5)
    with p3:
        focus_level = st.slider("Tingkat fokus saat belajar",
                                min_value=0, max_value=100, value=70, step=5)

    learning_style = st.selectbox(
        "Cara belajar yang paling sering digunakan",
        ["Membaca dan mencatat", "Menonton video", "Latihan soal",
         "Diskusi dengan orang lain", "Belajar mandiri / eksplorasi",
         "Campuran beberapa cara"]
    )

    (score_datang, score_tugas, score_tanya,
     score_paham, score_hadir, score_ip,
     overall_score) = calculate_scores(datang, tugas, tanya, paham, hadir, ip)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Jalankan Prediksi AI", use_container_width=True):
        st.session_state["ran"] = True
        st.session_state["profile"] = {
            "study_hours": study_hours, "sleep_hours": sleep_hours,
            "focus_level": focus_level, "learning_style": learning_style
        }
        st.toast("Analisis selesai! Scroll ke bawah untuk melihat hasil.", icon="✅")

    if st.session_state.get("ran") and model is None:
        st.error("Model AI belum dapat digunakan. Periksa file nilavia_xgb_model.pkl.")

    if st.session_state.get("ran") and model is not None:
        input_data = np.array([[
            DICT_DATANG[datang], DICT_TUGAS[tugas], DICT_TANYA[tanya],
            DICT_PAHAM[paham], DICT_HADIR[hadir], ip
        ]])

        prediction = int(model.predict(input_data)[0])
        proba = model.predict_proba(input_data)[0]
        risk = calculate_risk(proba)

        indicators = {
            "Kedisiplinan": score_datang, "Konsistensi Tugas": score_tugas,
            "Partisipasi": score_tanya, "Pemahaman Materi": score_paham,
            "Kehadiran": score_hadir, "IP": score_ip
        }
        issues = generate_issues(datang, tugas, paham, hadir, ip)

        st.session_state["last"] = {
            "pred": prediction, "risk": risk, "ip": ip, "issues": issues,
            "overall": float(overall_score), "indicators": indicators,
            "study_hours": study_hours, "sleep_hours": sleep_hours,
            "focus_level": focus_level, "learning_style": learning_style
        }

        if st.session_state.get("plan_source") != prediction:
            auto_fill_plan_from_issues(issues, st.session_state["last"])
            st.session_state["plan_source"] = prediction

        st.markdown("<hr style='border-color:#e5e7eb;'>", unsafe_allow_html=True)

        col_viz, col_text = st.columns([1.2, 1], gap="large")

        with col_viz:
            render_section("02 AI ANALYSIS")
            tab1, tab2 = st.tabs(["📈  Overall Performance", "🕸️  Radar Indikator"])

            with tab1:
                st.plotly_chart(render_gauge(overall_score),
                                use_container_width=True, theme=None)
                render_health_breakdown(indicators, overall_score)

            with tab2:
                st.plotly_chart(render_radar(indicators),
                                use_container_width=True, theme=None)
                render_indicator_details(indicators)

        with col_text:
            render_section("03 PREDICT")
            render_status(prediction)
            st.markdown(
                '<div class="nilavia-card">'
                '<b style="color:#0f2a43;">Early Warning Index</b>'
                f'<div style="font-size:1.7rem;font-weight:700;color:#45a5a5;margin-top:0.3rem;">'
                f'{risk:.0f}'
                '</div>'
                '<p style="color:#4b5563;font-size:0.83rem;margin:0.3rem 0 0 0;">'
                'Indeks ini dihitung dari output probabilitas model '
                'dan digunakan sebagai indikator peringatan dini.'
                '</p>'
                '</div>',
                unsafe_allow_html=True
            )

            render_explanation(issues)
            render_recommendations(issues, prediction)

        # SELF MANAGEMENT INSIGHT
        st.markdown("<hr style='border-color:#e5e7eb;'>", unsafe_allow_html=True)
        render_section("🧠 INSIGHT KEBIASAAN BELAJAR")

        h1, h2, h3, h4 = st.columns(4)
        h1.metric("Waktu Belajar", f"{study_hours} jam/minggu")
        h2.metric("Tidur",         f"{sleep_hours:.1f} jam/malam")
        h3.metric("Fokus",         f"{focus_level}%")
        h4.metric("Gaya Belajar",  learning_style)

        habit_notes = []
        if study_hours < 5:    habit_notes.append("Waktu belajar mingguan masih relatif rendah.")
        elif study_hours >= 10: habit_notes.append("Waktu belajar mingguan cukup tinggi.")
        if sleep_hours < 6:    habit_notes.append("Durasi tidur di bawah 6 jam per malam.")
        elif sleep_hours >= 7: habit_notes.append("Durasi tidur cukup.")
        if focus_level < 50:   habit_notes.append("Tingkat fokus perlu ditingkatkan.")
        elif focus_level >= 80: habit_notes.append("Tingkat fokus cukup tinggi.")

        if habit_notes:
            items = "".join(f"<li>{n}</li>" for n in habit_notes)
            st.markdown(
                '<div class="nilavia-card">'
                '<b style="color:#0f2a43;">Pola yang terdeteksi</b>'
                f'<ul style="margin:0.5rem 0 0 0;color:#374151;">{items}</ul>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            st.info("Belum terdapat pola kebiasaan yang perlu mendapat perhatian khusus.")

        # SIMULASI
        st.markdown("<hr style='border-color:#e5e7eb;'>", unsafe_allow_html=True)
        render_section("07 SIMULASI (WHAT-IF)")
        st.caption("Ubah beberapa indikator untuk melihat bagaimana output model berubah.")

        s1, s2, s3, s4 = st.columns(4, gap="medium")
        sim_paham = s1.select_slider("Pemahaman", options=list(DICT_PAHAM.keys()), value=paham)
        sim_hadir = s2.select_slider("Kehadiran", options=list(DICT_HADIR.keys()), value=hadir)
        sim_ip    = s3.slider("IP", 0.0, 4.0, float(ip), 0.01)
        sim_tugas = s4.radio("Kumpul tugas", ["Jarang", "Selalu"],
                             index=0 if tugas == "Jarang" else 1, horizontal=True)

        sim_input = np.array([[
            DICT_DATANG[datang], DICT_TUGAS[sim_tugas], DICT_TANYA[tanya],
            DICT_PAHAM[sim_paham], DICT_HADIR[sim_hadir], sim_ip
        ]])
        sim_pred  = int(model.predict(sim_input)[0])
        sim_proba = model.predict_proba(sim_input)[0]
        sim_risk  = calculate_risk(sim_proba)

        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

        render_comparison_cards(prediction, sim_pred, risk, sim_risk)
        render_risk_gauge_compare(risk, sim_risk)

        if sim_pred < prediction or sim_risk < risk - 1:
            st.markdown(
                '<div class="cmp-important">'
                '✅ <b>Simulasi ini menunjukkan perbaikan.</b> '
                'Dengan mengubah indikator seperti pada simulasi, '
                'status akademikmu berpotensi <b>meningkat</b>. '
                'Pertimbangkan untuk menerapkan perubahan ini secara konsisten.'
                '</div>',
                unsafe_allow_html=True
            )
        elif sim_pred > prediction or sim_risk > risk + 1:
            st.markdown(
                '<div class="cmp-important" style="background:linear-gradient(90deg,#fef2f2,#fee2e2);'
                'border-left-color:#dc2626;color:#7f1d1d;">'
                '⚠️ <b>Perhatian: Simulasi ini memperburuk kondisi.</b> '
                'Jika indikator diubah seperti pada simulasi, '
                'risiko akademikmu <b>naik</b>. Hindari skenario ini.'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="cmp-important">'
                'ℹ️ <b>Perubahan indikator belum mengubah level risiko secara signifikan.</b> '
                'Coba ubah indikator lain untuk melihat pengaruhnya terhadap status akademikmu.'
                '</div>',
                unsafe_allow_html=True
            )

        # SIMPAN CHECK-IN
        render_section("08 SIMPAN CHECK-IN")
        if st.button("💾 Simpan Check-in Hari Ini"):
            st.session_state["history"].append({
                "Waktu": datetime.now().strftime("%d %b %H:%M"),
                "Status": get_status_label(prediction),
                "Risiko": round(risk, 1), "IP": round(ip, 2),
                "Pemahaman": round(score_paham, 0), "Kehadiran": round(score_hadir, 0),
                "Tugas": round(score_tugas, 0), "Waktu Belajar": study_hours,
                "Tidur": sleep_hours, "Fokus": focus_level
            })
            st.toast("Check-in berhasil disimpan!", icon="💾")


# ============================================================
# 11. RENCANA BELAJAR
# ============================================================
elif selected_menu == "Rencana Belajar":
    render_header_banner(
        "Rencana Belajar & Progres",
        "Ubah hasil analisis menjadi langkah nyata dan pantau perubahan kondisi akademik dari waktu ke waktu."
    )

    last = st.session_state.get("last")
    if not last:
        st.info("Belum ada hasil analisis. Buka menu **Prediksi Akademik**, "
                "masukkan data, lalu tekan **Jalankan Prediksi AI**.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Status Terakhir", get_status_label(last["pred"]))
        c2.metric("Skor Risiko", f"{last['risk']:.0f}%")
        c3.metric("IP Saat Ini", f"{last['ip']:.2f}")

        render_section("🎯 TARGET IP")
        default_target = min(4.0, max(3.5, last["ip"]))

        colA, colB = st.columns([1, 2])
        with colA:
            target = st.number_input(
                "Target IP semester ini",
                min_value=0.00,
                max_value=4.00,
                value=float(round(default_target, 2)),
                step=0.01,
                format="%.2f",
                key="target_ip_input"
            )
        with colB:
            st.markdown("<div style='height:1.65rem;'></div>", unsafe_allow_html=True)
            progress_ip = min(last["ip"] / target, 1.0) if target > 0 else 0
            st.progress(progress_ip)
            gap = target - last["ip"]
            if gap > 0:
                st.caption(f"IP sekarang **{last['ip']:.2f}** dari target **{target:.2f}**. "
                           f"Selisih **{gap:.2f}** poin lagi.")
            elif gap == 0:
                st.caption(f"IP sekarang **{last['ip']:.2f}** — tepat di target! 🎉")
            else:
                st.caption(f"IP sekarang **{last['ip']:.2f}** sudah melampaui target **{target:.2f}**! 🎉")

        render_section("✅ RENCANA AKSI MINGGU INI")

        col_reg, col_reset = st.columns([3, 1])
        with col_reset:
            if st.button("🔄 Reset & Isi Rekomendasi AI", use_container_width=True):
                auto_fill_plan_from_issues(last["issues"], last)
                for day in DAYS:
                    for task in st.session_state["action_plans"][day]:
                        st.session_state.pop(f"chk_{task['id']}", None)
                st.toast("Rencana direset dan diisi ulang dari rekomendasi AI!", icon="🔄")
                st.rerun()

        render_day_plan()

        total = sum(len(v) for v in st.session_state["action_plans"].values())
        done = sum(
            1
            for day in DAYS
            for t in st.session_state["action_plans"][day]
            if st.session_state.get(f"chk_{t['id']}", False)
        )

        if total > 0:
            st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
            st.progress(done / total)
            st.caption(f"**{done}** dari **{total}** aksi selesai minggu ini.")

            if done == total:
                if not st.session_state.get("celebrated"):
                    st.balloons()
                    st.session_state["celebrated"] = True
                st.success("Semua aksi selesai! 🎉 Lakukan check-in kembali untuk melihat perubahan.")
            else:
                st.session_state["celebrated"] = False

        st.markdown("<hr style='border-color:#e5e7eb;'>", unsafe_allow_html=True)
        render_section("📈 ACADEMIC JOURNEY")

        hist = st.session_state.get("history", [])
        if hist:
            hdf = pd.DataFrame(hist)
            tab_risk, tab_ip, tab_habit = st.tabs(
                ["📉  Tren Risiko", "📈  Tren IP", "🧠  Kebiasaan"]
            )

            with tab_risk:
                fig_risk = go.Figure()
                fig_risk.add_trace(go.Scatter(
                    x=hdf["Waktu"], y=hdf["Risiko"],
                    mode="lines+markers",
                    line=dict(color="#45a5a5", width=3),
                    marker=dict(size=9, color="#0f2a43")
                ))
                fig_risk.update_layout(
                    yaxis=dict(range=[0, 100], title="Skor Risiko"),
                    xaxis=dict(title=""),
                    height=320,
                    margin=dict(l=60, r=20, t=20, b=40),
                    paper_bgcolor="white", plot_bgcolor="white",
                    font_color="#1f2937"
                )
                st.plotly_chart(fig_risk, use_container_width=True, theme=None)

            with tab_ip:
                fig_ip = go.Figure()
                fig_ip.add_trace(go.Scatter(
                    x=hdf["Waktu"], y=hdf["IP"],
                    mode="lines+markers",
                    line=dict(color="#0f2a43", width=3),
                    marker=dict(size=9, color="#f8c420")
                ))
                fig_ip.update_layout(
                    yaxis=dict(range=[0, 4], title="IP"),
                    xaxis=dict(title=""),
                    height=320,
                    margin=dict(l=60, r=20, t=20, b=40),
                    paper_bgcolor="white", plot_bgcolor="white",
                    font_color="#1f2937"
                )
                st.plotly_chart(fig_ip, use_container_width=True, theme=None)

            with tab_habit:
                if all(c in hdf.columns for c in ["Waktu Belajar", "Tidur", "Fokus"]):
                    st.dataframe(
                        hdf[["Waktu", "Waktu Belajar", "Tidur", "Fokus"]],
                        use_container_width=True, hide_index=True
                    )
                else:
                    st.info("Data kebiasaan belum tersedia pada check-in sebelumnya.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<b style="color:#0f2a43;">Riwayat Check-in</b>',
                        unsafe_allow_html=True)
            st.dataframe(hdf, use_container_width=True, hide_index=True)
        else:
            st.caption("Belum ada check-in. Simpan hasil analisis melalui menu "
                       "**Prediksi Akademik** untuk mulai melihat perkembangan akademik.")