import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Setup Konfigurasi Halaman (Mobile Responsive Layout)
st.set_page_config(page_title="NILAVIA | Academic Self-Management", layout="wide", initial_sidebar_state="expanded")

# Inject Tailwind CSS (CDN) dan Bootstrap Icons
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
<style>
    /* Mengatur warna utama dan secondary */
    :root {
        --primary-color: #45a5a5;
        --primary-light: rgba(69, 165, 165, 0.1);
        --secondary-color: #f8c420;
    }
    
    /* Override font & Streamlit defaults */
    h1, h2, h3, h4 {
        color: var(--primary-color) !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 700 !important;
    }
    
    /* Styling tombol kustom Streamlit */
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 0.5rem !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: bold !important;
        width: 100%;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: var(--secondary-color) !important;
        color: #1f1f1f !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }

    /* Custom Container Classes */
    .nilavia-card {
        background-color: #ffffff;
        border-left: 5px solid var(--primary-color);
        padding: 1.25rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .nilavia-banner {
        background-color: var(--primary-light);
        border: 1px solid var(--primary-color);
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1.5rem;
    }
    
    /* Status Colors */
    .text-maintain { color: #10B981; } /* Green */
    .text-adjust { color: #F59E0B; }   /* Yellow */
    .text-support { color: #EF4444; }  /* Red */
    
    /* Memastikan teks pada daftar terbaca dengan jelas (hitam/abu-abu gelap) */
    .readable-list {
        color: #374151 !important; /* Warna gray-700 Tailwind */
    }
    .readable-list li {
        color: #374151 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Model AI
@st.cache_resource
def load_model():
    return joblib.load('nilavia_xgb_model.pkl')

try:
    model = load_model()
except:
    st.warning("Model 'nilavia_xgb_model.pkl' tidak ditemukan. Pastikan file berada di folder yang sama.")
    model = None

# Sidebar Menu Navigasi
with st.sidebar:
    st.markdown("<div class='text-center mb-6'><h1 class='text-4xl'><i class='bi bi-leaf'></i> NILAVIA</h1><p class='text-gray-500 text-sm mt-1'>AI Early Warning & Academic Self-Management</p></div>", unsafe_allow_html=True)
    
    selected_menu = option_menu(
        menu_title=None,
        options=["Kondisi Akademik", "Prediksi Akademik"],
        icons=["house", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#f8c420", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#f3f4f6"},
            "nav-link-selected": {"background-color": "#45a5a5"},
        }
    )

# -------------------------------------------------------------
# HELPER UI COMPONENT
# -------------------------------------------------------------
def render_header_banner(title, subtitle):
    st.markdown(f"""
    <div class='nilavia-banner'>
        <h2 class='text-2xl mb-2'><i class='bi bi-cpu'></i> {title}</h2>
        <b style='color: var(--primary-color);'>MANAGE SMARTER, NOT PUSH HARDER.</b><br>
        <p class='text-gray-700 mt-2'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

import base64
import os

# Fungsi helper untuk membaca file lokal dan mengubahnya menjadi Base64 string
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return "" # Return string kosong jika gambar tidak ditemukan

# URL Logo Aplikasi diubah menjadi data Base64
LOGO_RUANGGURU = get_base64_image("ruangguru.png")
LOGO_ZENIUS = get_base64_image("zenius.png")
LOGO_PAHAMIFY = get_base64_image("pahamify.png")

# -------------------------------------------------------------
# MENU 1: DEFAULT (Penyesuaian Dummy Pemahaman Jelek 30%)
# -------------------------------------------------------------
if selected_menu == "Kondisi Akademik":
    render_header_banner("Kondisi Akademik Saya", "Berikut adalah ringkasan kesehatan akademikmu saat ini. Segera evaluasi area yang membutuhkan perhatian!")

    # Data Statis Dummy disesuaikan dengan pemahaman materi turun ke 30%
    dummy_score = 79.0 
    dummy_ip = 2.80 
    
    col_viz, col_text = st.columns([1.2, 1])
    
    with col_viz:
        st.markdown("<h3 class='text-xl mb-4'><i class='bi bi-pie-chart-fill'></i> AI ANALYSIS VISUALIZATION</h3>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Overall Performance", "Radar Indikator"])
        
        with tab1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = dummy_score,
                number = {'suffix': "%", 'font': {'color': '#F59E0B'}}, # Warna disesuaikan
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Academic Health Score", 'font': {'size': 18}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#F59E0B"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "#e5e7eb",
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.1)"},
                        {'range': [50, 75], 'color': "rgba(245, 158, 11, 0.1)"},
                        {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.1)"}],
                    'threshold': {'line': {'color': "#F59E0B", 'width': 4}, 'thickness': 0.75, 'value': dummy_score}
                }
            ))
            fig_gauge.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with tab2:
            categories = ['Kedisiplinan', 'Tugas', 'Bertanya', 'Pemahaman', 'Kehadiran', 'IP', 'Kedisiplinan']
            # Diubah pemahamannya menjadi 30
            values = [100, 100, 75, 30, 100, (dummy_ip/4.0)*100, 100] 
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values, theta=categories, fill='toself',
                fillcolor='rgba(245, 158, 11, 0.4)',
                line=dict(color='#F59E0B', width=2), marker=dict(color='#EF4444', size=8)
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(l=40, r=40, t=40, b=20))
            st.plotly_chart(fig_radar, use_container_width=True)

    with col_text:
        st.markdown("<h3 class='text-xl mt-4 lg:mt-0 mb-3'><i class='bi bi-bullseye'></i> 03 — PREDICT</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='p-4 mb-4 rounded-lg bg-yellow-50 border border-yellow-200'>
            <h4 class='text-adjust text-lg'><i class='bi bi-exclamation-triangle-fill'></i> ADJUST (PERLU PENYESUAIAN)</h4>
            <p class='text-gray-700 mt-1'>IP: <b>{dummy_ip}</b>. Ada indikator yang menurun tajam, khususnya pada pemahaman materi. Lakukan penyesuaian strategi belajar segera agar tidak menumpuk menjadi beban besar di akhir semester.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 class='text-xl mb-3'><i class='bi bi-search'></i> 04 — EXPLAIN</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='nilavia-card border-l-4' style='border-color: #F59E0B;'>
            <ul class='list-disc pl-5 text-gray-700'>
                <li class='mb-1'><i class='bi bi-exclamation-circle text-red-400 mr-2'></i> <b>Pemahaman Materi (30%)</b>: Terdeteksi penurunan drastis. Indikator ini paling krusial untuk menghadapi ujian.</li>
                <li><i class='bi bi-info-circle text-blue-400 mr-2'></i> Indikator lain seperti kehadiran dan pengumpulan tugas masih baik. Masalah utama ada di penyerapan materi.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 class='text-xl mb-3'><i class='bi bi-compass'></i> 05 & 06 — RECOMMEND & MANAGE</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='nilavia-card'>
            <ul class='list-none readable-list'>
                <li class='mb-3'><i class='bi bi-arrow-right-circle text-blue-500 mr-2'></i> <b>Konsultasi Segera:</b> Jadwalkan waktu dengan dosen atau asisten dosen terkait mata kuliah yang tertinggal.</li>
                <li class='mb-3'><i class='bi bi-laptop text-blue-500 mr-2'></i> <b>Gunakan Aplikasi Belajar Tambahan:</b> Coba pelajari ulang konsep dari sudut pandang berbeda menggunakan platform edukasi di bawah ini. Klik untuk menuju situs:</li>
            </ul>
            <div class='flex gap-3 flex-wrap mt-2'>
                <a href='https://www.ruangguru.com' target='_blank' style='text-decoration: none;'>
                    <div style='background-color: #f3f4f6; color: #1f2937; padding: 6px 12px; border-radius: 8px; font-size: 0.9rem; font-weight: bold; display: flex; align-items: center; gap: 8px; cursor: pointer; border: 1px solid #e5e7eb; transition: 0.3s;' onmouseover="this.style.backgroundColor='#e5e7eb'" onmouseout="this.style.backgroundColor='#f3f4f6'">
                        <img src='{LOGO_RUANGGURU}' alt='Ruangguru' style='width: 24px; height: 24px; border-radius: 4px;'> Ruangguru
                    </div>
                </a>
                <a href='https://www.zenius.net' target='_blank' style='text-decoration: none;'>
                    <div style='background-color: #f3f4f6; color: #1f2937; padding: 6px 12px; border-radius: 8px; font-size: 0.9rem; font-weight: bold; display: flex; align-items: center; gap: 8px; cursor: pointer; border: 1px solid #e5e7eb; transition: 0.3s;' onmouseover="this.style.backgroundColor='#e5e7eb'" onmouseout="this.style.backgroundColor='#f3f4f6'">
                        <img src='{LOGO_ZENIUS}' alt='Zenius' style='width: 24px; height: 24px; border-radius: 4px;'> Zenius
                    </div>
                </a>
                <a href='https://pahamify.com' target='_blank' style='text-decoration: none;'>
                    <div style='background-color: #f3f4f6; color: #1f2937; padding: 6px 12px; border-radius: 8px; font-size: 0.9rem; font-weight: bold; display: flex; align-items: center; gap: 8px; cursor: pointer; border: 1px solid #e5e7eb; transition: 0.3s;' onmouseover="this.style.backgroundColor='#e5e7eb'" onmouseout="this.style.backgroundColor='#f3f4f6'">
                        <img src='{LOGO_PAHAMIFY}' alt='Pahamify' style='width: 24px; height: 24px; border-radius: 4px;'> Pahamify
                    </div>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# MENU 2: PREDIKSI (Input dinamis untuk XGBoost)
# -------------------------------------------------------------
elif selected_menu == "Prediksi Akademik":
    render_header_banner("Analisis Kondisi Akademik", "Masukkan data akademik terbaru dan rutinitas perilakumu di bawah ini untuk melihat prediksi dan rekomendasi dari Model AI.")

    st.markdown("<h3 class='text-xl mb-4'><i class='bi bi-collection'></i> 01 — COLLECT</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        datang = st.selectbox("Kedisiplinan (Datang)", ['Tidak Pernah Telat', 'Jarang', 'Selalu (Sering Telat)'])
        tugas = st.selectbox("Konsistensi (Kumpul Tugas)", ['Selalu', 'Jarang'])
    with col2:
        tanya = st.selectbox("Partisipasi (Bertanya)", ['Selalu', 'Sering', 'Sesekali', 'Tak Pernah'])
        # Set default index = 2 agar otomatis terpilih '30(%)'
        paham = st.selectbox("Persepsi (Pemahaman Materi)", ['100(%)', '50(%)', '30(%)', 'Tak Paham Satupun Mk'], index=2)
    with col3:
        hadir = st.selectbox("Keterlibatan (Kehadiran)", ['100(%)', '80(%)', '60(%)', '40(%)'])
        ip = st.number_input("Capaian Akademik (IP)", min_value=0.00, max_value=4.00, value=2.80, step=0.01)

    # Mapping Input ke Numerik
    dict_datang = {'Selalu (Sering Telat)': 1, 'Jarang': 2, 'Tidak Pernah Telat': 3}
    dict_tugas = {'Jarang': 1, 'Selalu': 3}
    dict_tanya = {'Tak Pernah': 1, 'Sesekali': 2, 'Sering': 3, 'Selalu': 4}
    dict_paham = {'Tak Paham Satupun Mk': 0, '30(%)': 30, '50(%)': 50, '100(%)': 100}
    dict_hadir = {'40(%)': 40, '60(%)': 60, '80(%)': 80, '100(%)': 100}

    # Hitung Persentase Real
    score_datang = (dict_datang[datang] / 3) * 100
    score_tugas = (dict_tugas[tugas] / 3) * 100
    score_tanya = (dict_tanya[tanya] / 4) * 100
    score_paham = dict_paham[paham]
    score_hadir = dict_hadir[hadir]
    score_ip = (ip / 4.0) * 100
    overall_score = np.mean([score_datang, score_tugas, score_tanya, score_paham, score_hadir, score_ip])

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Jalankan Prediksi AI", use_container_width=True) and model is not None:
        st.markdown("<hr class='my-6'>", unsafe_allow_html=True)
        
        input_data = np.array([[dict_datang[datang], dict_tugas[tugas], dict_tanya[tanya], dict_paham[paham], dict_hadir[hadir], ip]])
        prediction = model.predict(input_data)[0]
        
        col_viz, col_text = st.columns([1.2, 1])
        
        with col_viz:
            st.markdown("<h3 class='text-xl mb-4'><i class='bi bi-pie-chart-fill'></i> 02 — AI ANALYSIS</h3>", unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["Overall Performance", "Radar Indikator"])
            with tab1:
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number", value = overall_score,
                    number = {'suffix': "%", 'font': {'color': '#45a5a5'}},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Academic Health Score", 'font': {'size': 18}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "#f8c420"}, 'bgcolor': "white",
                        'borderwidth': 2, 'bordercolor': "#e5e7eb",
                        'steps': [
                            {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.1)"},
                            {'range': [50, 75], 'color': "rgba(245, 158, 11, 0.1)"},
                            {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.1)"}],
                        'threshold': {'line': {'color': "#ef4444", 'width': 4}, 'thickness': 0.75, 'value': overall_score}
                    }
                ))
                fig_gauge.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True)

            with tab2:
                categories = ['Kedisiplinan', 'Tugas', 'Bertanya', 'Pemahaman', 'Kehadiran', 'IP', 'Kedisiplinan']
                values = [score_datang, score_tugas, score_tanya, score_paham, score_hadir, score_ip, score_datang]
                fig_radar = go.Figure(data=go.Scatterpolar(
                    r=values, theta=categories, fill='toself',
                    fillcolor='rgba(69, 165, 165, 0.4)', line=dict(color='#45a5a5', width=2), marker=dict(color='#f8c420', size=8)
                ))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(l=40, r=40, t=40, b=20))
                st.plotly_chart(fig_radar, use_container_width=True)

        with col_text:
            st.markdown("<h3 class='text-xl mt-4 lg:mt-0 mb-3'><i class='bi bi-bullseye'></i> 03 — PREDICT</h3>", unsafe_allow_html=True)
            if prediction == 0:
                st.markdown("""
                <div class='p-4 mb-4 rounded-lg bg-green-50 border border-green-200'>
                    <h4 class='text-maintain text-lg'><i class='bi bi-check-circle-fill'></i> MAINTAIN (STABIL)</h4>
                    <p class='text-gray-700 mt-1'>Kondisi akademikmu stabil. Pertahankan pola belajar saat ini.</p>
                </div>
                """, unsafe_allow_html=True)
            elif prediction == 1:
                st.markdown("""
                <div class='p-4 mb-4 rounded-lg bg-yellow-50 border border-yellow-200'>
                    <h4 class='text-adjust text-lg'><i class='bi bi-exclamation-triangle-fill'></i> ADJUST (PERLU PENYESUAIAN)</h4>
                    <p class='text-gray-700 mt-1'>Ada indikator yang menurun. Lakukan penyesuaian agar tidak menumpuk menjadi beban besar.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='p-4 mb-4 rounded-lg bg-red-50 border border-red-200'>
                    <h4 class='text-support text-lg'><i class='bi bi-x-circle-fill'></i> SEEK SUPPORT (BUTUH PERHATIAN)</h4>
                    <p class='text-gray-700 mt-1'>Kondisimu berisiko. Pertimbangkan mencari dukungan akademik secepatnya.</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<h3 class='text-xl mb-3'><i class='bi bi-search'></i> 04 — EXPLAIN</h3>", unsafe_allow_html=True)
            issues = []
            if dict_tugas[tugas] == 1: issues.append("Pengumpulan Tugas Menurun")
            if dict_paham[paham] <= 30: issues.append("Pemahaman Materi Rendah")
            if dict_hadir[hadir] <= 60: issues.append("Tingkat Kehadiran Rendah")
            if dict_datang[datang] == 1: issues.append("Sering Terlambat / Kedisiplinan Waktu")
            if ip < 3.3: issues.append("Indeks Prestasi (IP) di bawah standar optimal")
            
            if not issues:
                st.markdown("""
                <div class='nilavia-card'>
                    <p class='text-gray-700'><i class='bi bi-lightbulb-fill text-yellow-400'></i> Semua indikator dalam batas wajar. Konsistensimu sangat baik!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                issue_html = "<ul class='list-disc pl-5 text-gray-700'>"
                for issue in issues:
                    issue_html += f"<li class='mb-1'><i class='bi bi-exclamation-circle text-red-400 mr-2'></i> {issue}</li>"
                issue_html += "</ul>"
                
                st.markdown(f"""
                <div class='nilavia-card'>
                    <b class='text-gray-800 block mb-2'>Area yang Perlu Perhatian:</b>
                    {issue_html}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<h3 class='text-xl mb-3'><i class='bi bi-compass'></i> 05 & 06 — RECOMMEND & MANAGE</h3>", unsafe_allow_html=True)
            
            recs_html = "<ul class='list-none readable-list'>"
            
            if prediction == 0 and not issues:
                recs_html += "<li class='mb-2'><i class='bi bi-check2-square text-green-500 mr-2'></i> <b>Jaga Ritme:</b> Manfaatkan sisa waktumu untuk hobi atau istirahat.</li>"
                recs_html += "<li><i class='bi bi-check2-square text-green-500 mr-2'></i> <b>Konsisten:</b> Pola belajarmu sudah sangat efektif, jangan membebani diri lebih jauh.</li>"
            else:
                if len(issues) == 0:
                    recs_html += "<li class='mb-2'><i class='bi bi-arrow-right-circle text-blue-500 mr-2'></i> <b>Evaluasi Berkala:</b> Periksa kembali jadwal belajarmu secara keseluruhan.</li>"
                
                if "Pengumpulan Tugas Menurun" in issues:
                    recs_html += "<li class='mb-2'><i class='bi bi-clipboard-check text-blue-500 mr-2'></i> <b>Prioritaskan Tugas:</b> Pecah tugas besar menjadi bagian kecil. Buat to-do list berdasarkan deadline terdekat.</li>"
                if "Pemahaman Materi Rendah" in issues:
                    recs_html += "<li class='mb-2'><i class='bi bi-people-fill text-blue-500 mr-2'></i> <b>Konsultasi:</b> Jangan ragu berdiskusi dengan teman kelompok atau mengikuti sesi mentoring.</li>"
                    recs_html += f"""
                    <li class='mb-2'>
                        <i class='bi bi-laptop text-blue-500 mr-2'></i> <b>Platform Tambahan:</b> Coba pelajari ulang materi via aplikasi:
                        <div class='flex gap-2 flex-wrap mt-2 mb-2'>
                            <a href='https://www.ruangguru.com' target='_blank' style='text-decoration: none;'>
                                <div style='background-color: #f3f4f6; color: #1f2937; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; display: flex; align-items: center; gap: 6px; cursor: pointer; border: 1px solid #e5e7eb;'>
                                    <img src='{LOGO_RUANGGURU}' alt='Ruangguru' style='width: 16px; height: 16px; border-radius: 4px;'> Ruangguru
                                </div>
                            </a>
                            <a href='https://www.zenius.net' target='_blank' style='text-decoration: none;'>
                                <div style='background-color: #f3f4f6; color: #1f2937; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; display: flex; align-items: center; gap: 6px; cursor: pointer; border: 1px solid #e5e7eb;'>
                                    <img src='{LOGO_ZENIUS}' alt='Zenius' style='width: 16px; height: 16px; border-radius: 4px;'> Zenius
                                </div>
                            </a>
                            <a href='https://pahamify.com' target='_blank' style='text-decoration: none;'>
                                <div style='background-color: #f3f4f6; color: #1f2937; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; display: flex; align-items: center; gap: 6px; cursor: pointer; border: 1px solid #e5e7eb;'>
                                    <img src='{LOGO_PAHAMIFY}' alt='Pahamify' style='width: 16px; height: 16px; border-radius: 4px;'> Pahamify
                                </div>
                            </a>
                        </div>
                    </li>"""
                if "Tingkat Kehadiran Rendah" in issues or "Sering Terlambat / Kedisiplinan Waktu" in issues:
                    recs_html += "<li class='mb-2'><i class='bi bi-alarm text-blue-500 mr-2'></i> <b>Evaluasi Pola Tidur:</b> Atur alarm lebih awal dan kurangi begadang. Kehadiran fisik adalah langkah awal memahami materi.</li>"
                if "Indeks Prestasi (IP) di bawah standar optimal" in issues:
                    recs_html += "<li class='mb-2'><i class='bi bi-journal-bookmark text-blue-500 mr-2'></i> <b>Fokus Mata Kuliah Inti:</b> Identifikasi mata kuliah dengan bobot SKS besar dan alokasikan waktu ekstra untuk mata kuliah tersebut.</li>"
                    
            recs_html += "</ul>"
            
            st.markdown(f"""
            <div class='nilavia-card'>
                {recs_html}
            </div>
            """, unsafe_allow_html=True)