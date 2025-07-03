import streamlit as st
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder

def mapping_diagnosa_page():
    st.title("🔎 Diagnosa Pasien - Pencarian Global")

    # Input pencarian global
    search_query = st.text_input("🔍 Cari secara global (misalnya: flu, nyeri, infeksi)", "").lower()

    # Bagian 1: Dataset pasien dari CSV
    st.subheader("📄 Dataset Kunjungan Pasien")
    file_path = 'dataset/data_preprocessed.csv'

    try:
        df_csv = pd.read_csv(file_path)

        if search_query:
            df_filtered = df_csv[df_csv.astype(str).apply(lambda row: row.str.lower().str.contains(search_query).any(), axis=1)]
        else:
            df_filtered = df_csv

        st.dataframe(df_filtered)

        with st.expander("ℹ️ Penjelasan Kolom Dataset"):
            st.markdown("""
            - **Usia**: Umur pasien saat kunjungan.  
            - **Jenis Kelamin**: 0 = Laki-laki, 1 = Perempuan (sudah diencoding).  
            - **Keluhan**: Keluhan utama pasien.  
            - **Diagnosa**: Label numerik hasil encoding dari diagnosa asli.  
            - **Tanggal Kunjungan**: Waktu pasien datang berobat.  
            - **Keluhan_Feat**: Jumlah total panjang karakter kata pada keluhan.
            """)
    except FileNotFoundError:
        st.error(f"❌ File '{file_path}' tidak ditemukan.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file CSV: {e}")

    # Bagian 2: Mapping Diagnosa dari JSON
    st.subheader("🧾 Mapping Diagnosa (Nomor ↔ Nama)")
    json_path = 'dataset/data.json'

    try:
        with open(json_path, 'r') as file:
            data = json.load(file)

        df_json = pd.DataFrame(data)

        diagnosa_encoder = LabelEncoder()
        df_json['Diagnosa_encoded'] = diagnosa_encoder.fit_transform(df_json['Diagnosa'])

        diagnosa_mapping = dict(enumerate(diagnosa_encoder.classes_))
        mapping_df = pd.DataFrame(list(diagnosa_mapping.items()), columns=["Nomor", "Nama Diagnosa"])

        if search_query:
            mapping_filtered = mapping_df[mapping_df["Nama Diagnosa"].str.lower().str.contains(search_query)]
        else:
            mapping_filtered = mapping_df

        st.dataframe(mapping_filtered)

        # Penjelasan Diagnosa Umum
        with st.expander("🩺 Penjelasan Diagnosa Umum"):
            diagnosa_penjelasan = {
                "Angina Pektoris": """
**Penyebab:**  
Angina pektoris terjadi akibat berkurangnya aliran darah ke otot jantung.

**Gejala:**  
- Nyeri dada  
- Sesak napas  
- Nyeri menjalar ke lengan
""",
                "Flu": """
**Penyebab:**  
Virus influenza.

**Gejala:**  
- Demam  
- Pilek  
- Batuk  
- Lelah
""",
                "Gastroenteritis": """
**Penyebab:**  
Infeksi usus dari virus atau bakteri.

**Gejala:**  
- Diare  
- Muntah  
- Nyeri perut
""",
                "Gout": """
**Penyebab:**  
Kadar asam urat tinggi.

**Gejala:**  
- Nyeri sendi  
- Bengkak  
- Merah
""",
                "Hernia Diskus": """
**Penyebab:**  
Bantalan tulang belakang menonjol.

**Gejala:**  
- Nyeri punggung  
- Kesemutan  
- Lemah otot
""",
                "Infeksi Saluran Pernafasan": """
**Penyebab:**  
Virus atau bakteri saluran napas.

**Gejala:**  
- Batuk  
- Pilek  
- Demam
""",
                "Insomnia": """
**Penyebab:**  
Stres, gangguan pola tidur.

**Gejala:**  
- Susah tidur  
- Bangun dini  
- Lelah siang hari
""",
                "Osteoarthritis": """
**Penyebab:**  
Kerusakan tulang rawan sendi.

**Gejala:**  
- Nyeri sendi  
- Kaku  
- Bengkak
""",
                "Tonsilitis": """
**Penyebab:**  
Infeksi amandel.

**Gejala:**  
- Sakit tenggorokan  
- Amandel bengkak  
- Demam
""",
                "Vertigo": """
**Penyebab:**  
Masalah telinga dalam atau saraf.

**Gejala:**  
- Pusing berputar  
- Mual  
- Hilang keseimbangan
"""
            }

            for nama, penjelasan in diagnosa_penjelasan.items():
                if search_query in nama.lower() or search_query in penjelasan.lower() or not search_query:
                    st.markdown(f"### 🧾 {nama}")
                    st.markdown(penjelasan)

    except FileNotFoundError:
        st.error("❌ File JSON tidak ditemukan. Periksa kembali path-nya.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file JSON: {e}")
