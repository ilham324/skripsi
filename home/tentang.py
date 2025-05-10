import streamlit as st

def tentang_page():
    st.title("📘 Tentang Aplikasi")
    st.markdown("""
Aplikasi ini dikembangkan untuk membantu tenaga kesehatan dan pasien 
dalam **memprediksi kemungkinan penyakit** berdasarkan keluhan yang diberikan.

### 🔍 Fitur Utama:
- Analisis data kunjungan pasien
- Mapping diagnosa secara otomatis
- Prediksi penyakit (dapat dikembangkan)
- Tampilan interaktif dan mudah digunakan

🧠 Teknologi: **Streamlit, Scikit-Learn, Python**
    """)
