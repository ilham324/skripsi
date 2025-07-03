import streamlit as st
import pandas as pd

def tabel_page():
    st.title("🗄️ Struktur Tabel Database Aplikasi Prediksi Penyakit")

    st.markdown("Berikut adalah desain skema tabel database relasional:")

    # Tabel 1: Pasien
    st.subheader("1. Tabel Pasien")
    data_pasien = {
        "Nama Kolom": ["id_pasien", "nama", "usia", "jenis_kelamin"],
        "Tipe Data": ["INT (PK)", "VARCHAR", "INT", "ENUM"],
        "Keterangan": ["ID unik pasien", "Nama pasien", "Usia pasien", "'Laki-laki' / 'Perempuan'"]
    }
    st.table(pd.DataFrame(data_pasien))

    # Tabel 2: Keluhan
    st.subheader("2. Tabel Keluhan")
    data_keluhan = {
        "Nama Kolom": ["id_keluhan", "keluhan_text"],
        "Tipe Data": ["INT (PK)", "TEXT"],
        "Keterangan": ["ID keluhan", "Isi keluhan (string mentah)"]
    }
    st.table(pd.DataFrame(data_keluhan))

    # Tabel 3: Prediksi
    st.subheader("3. Tabel Prediksi")
    data_prediksi = {
        "Nama Kolom": [
            "id_prediksi", "id_pasien", "id_keluhan", 
            "tanggal_prediksi", "algoritma", "hasil_prediksi", "confidence_score"
        ],
        "Tipe Data": [
            "INT (PK)", "INT (FK)", "INT (FK)", 
            "DATETIME", "VARCHAR", "VARCHAR", "FLOAT"
        ],
        "Keterangan": [
            "ID prediksi", "Relasi ke pasien", "Relasi ke keluhan", 
            "Waktu prediksi dilakukan", "Misal: 'SVM', 'MLP'", 
            "Nama penyakit yang diprediksi", "Probabilitas keyakinan model"
        ]
    }
    st.table(pd.DataFrame(data_prediksi))

    # Tabel 4: Penyakit (Opsional)
    st.subheader("4. Tabel Penyakit (Opsional)")
    data_penyakit = {
        "Nama Kolom": ["id_penyakit", "nama_penyakit", "deskripsi"],
        "Tipe Data": ["INT (PK)", "VARCHAR", "TEXT"],
        "Keterangan": ["ID penyakit", "Nama penyakit", "Penjelasan penyakit (opsional)"]
    }
    st.table(pd.DataFrame(data_penyakit))

    st.info("⚙️ Struktur ini cocok untuk implementasi database relasional seperti MySQL atau PostgreSQL.")
