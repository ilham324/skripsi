import streamlit as st
import pandas as pd
import plotly.express as px

from home import diagnosa, prediksi, tentang, kontak, Tabel_data

# Inisialisasi email default
if 'email' not in st.session_state:
    st.session_state['email'] = None

# Mapping angka diagnosa ke nama penyakit
diagnosa_mapping = {
    0: "Angina Pektoris",
    1: "Flu",
    2: "Gastroenteritis",
    3: "Gout",
    4: "Hernia Diskus",
    5: "Infeksi Saluran Pernapasan",
    6: "Insomnia",
    7: "Osteoarthritis",
    8: "Tonsilitis",
    9: "Vertigo"
}

def main():
    st.sidebar.title("📋 Menu Navigasi")

    # Menu dasar
    menu = ["Beranda", "Prediksi Penyakit", "Mapping Diagnosa", "Tentang Aplikasi", "Kontak"]

    # Hanya admin yang bisa akses Tabel
    if st.session_state['email'] == "romandailham@gmail.com":
        menu.append("Tabel")

    pilihan = st.sidebar.selectbox("Pilih Menu", menu)

    if pilihan == "Beranda":
        st.title("🔥 Selamat Datang di Aplikasi Prediksi Penyakit")
        st.markdown("Gunakan menu di samping untuk mulai melihat data, menganalisis keluhan, atau membaca informasi aplikasi.")

        try:
            df = pd.read_csv("dataset/data_preprocessed.csv")
            df['Diagnosa_Nama'] = df['Diagnosa'].map(diagnosa_mapping)

            st.subheader("📊 Jumlah Kasus per Diagnosa")
            chart = df['Diagnosa_Nama'].value_counts().reset_index()
            chart.columns = ['Diagnosa', 'Jumlah Pasien']
            fig = px.bar(chart, x='Diagnosa', y='Jumlah Pasien', color='Diagnosa')
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Gagal memuat data: {e}")

    elif pilihan == "Prediksi Penyakit":
        prediksi.prediksi_page()
    elif pilihan == "Mapping Diagnosa":
        diagnosa.mapping_diagnosa_page()
    elif pilihan == "Tentang Aplikasi":
        tentang.tentang_page()
    elif pilihan == "Kontak":
        kontak.kontak_page()
    elif pilihan == "Tabel":
        Tabel_data.tabel_page()
