import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import pyrebase
from datetime import datetime

# ==========================
# Konfigurasi Firebase
# ==========================
firebaseConfig = {
    "apiKey": "AIzaSyAFVY0GjcLzrg5PrrbmBeZWXJkZGfgihcU",
    "authDomain": "skripsi-86872.firebaseapp.com",
    "databaseURL": "https://skripsi-86872-default-rtdb.firebaseio.com/",
    "projectId": "skripsi-86872",
    "storageBucket": "skripsi-86872.appspot.com",
    "messagingSenderId": "722934043351",
    "appId": "1:722934043351:web:89b5b3794efd96ea519692",
    "measurementId": "G-E1RCLT7E9H"
}

# Inisialisasi Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# ==========================
# Mapping Diagnosa
# ==========================
mapping_diagnosa = {
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

# ==========================
# Penjelasan Hasil Prediksi
# ==========================
def deskripsi_prediksi(usia, jenis_kelamin, keluhan_asli, keluhan_feat, prediksi_kode, df):
    data_kelas = df[df["Diagnosa"] == prediksi_kode]
    if data_kelas.empty:
        return "Tidak ditemukan data serupa pada dataset."

    rata_usia = data_kelas["Usia"].mean()
    dominan_gender = "Laki-laki" if data_kelas["Jenis Kelamin"].mode()[0] == 0 else "Perempuan"
    rata_keluhan_feat = data_kelas["Keluhan_Feat"].mean()
    gender_str = "Laki-laki" if jenis_kelamin == 0 else "Perempuan"
    nama_penyakit = mapping_diagnosa.get(prediksi_kode, "Tidak diketahui")

    return (
        f"\n🧾 **Hasil Prediksi**\n\n"
        f"Berdasarkan data Anda: usia **{usia} tahun**, jenis kelamin **{gender_str}**, "
        f"keluhan: **{keluhan_asli if keluhan_asli else 'Tidak ada'}**, kemungkinan penyakit adalah "
        f"**{nama_penyakit}**.\n\n"
        f"📌 Karena dalam dataset, pasien dengan ciri usia sekitar **{rata_usia:.0f} tahun**, "
        f"**{dominan_gender}**, dan panjang keluhan **{rata_keluhan_feat:.0f} karakter** sering didiagnosis penyakit ini."
    )

# ==========================
# Halaman Prediksi
# ==========================
def prediksi_page():
    st.title("🧠 Prediksi Penyakit Pasien")
    st.markdown("Masukkan data untuk memprediksi kemungkinan penyakit berdasarkan keluhan pasien.")

    usia = st.number_input("Usia Pasien (5-70 tahun)", min_value=5, max_value=70, value=30)
    jenis_kelamin_str = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

    keluhan_list = [
        "Batuk", "Sakit tenggorokan", "Demam", "Muntah", "Mual", "Nyeri perut",
        "Nyeri sendi", "Nyeri punggung", "Nyeri dada", "Sakit kepala", "Pusing",
        "Kaki bengkak", "Gangguan tidur"
    ]
    keluhan_terpilih = st.multiselect("Pilih Keluhan Utama Pasien", keluhan_list)

    keluhan_input = ", ".join(keluhan_terpilih)
    keluhan_feat = len(keluhan_input)
    jenis_kelamin = 0 if jenis_kelamin_str == "Laki-laki" else 1

    algoritma = st.selectbox("Pilih Algoritma Prediksi", ["Support Vector Machine (SVM)", "Multilayer Perceptron (MLP)"])

    try:
        df = pd.read_csv("dataset/data_preprocessed.csv")
        X = df[["Usia", "Jenis Kelamin", "Keluhan_Feat"]]
        y = df["Diagnosa"].astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        if algoritma == "Support Vector Machine (SVM)":
            model = SVC(kernel='linear', probability=True, random_state=42)
        else:
            model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=3000, random_state=42)

        model.fit(X_train_scaled, y_train)

        if st.button("🔍 Prediksi Sekarang"):
            st.markdown("### 📝 Ringkasan Input Pasien")
            st.markdown(f"- Usia: **{usia} tahun**")
            st.markdown(f"- Jenis Kelamin: **{jenis_kelamin_str}**")
            st.markdown(f"- Keluhan: **{keluhan_input if keluhan_input else 'Tidak ada keluhan'}**")
            st.markdown(f"- Panjang Keluhan: **{keluhan_feat} karakter**")

            input_data = pd.DataFrame([[usia, jenis_kelamin, keluhan_feat]], columns=["Usia", "Jenis Kelamin", "Keluhan_Feat"])
            input_scaled = scaler.transform(input_data)

            hasil_encoded = model.predict(input_scaled)[0]
            proba = model.predict_proba(input_scaled)[0]

            # ======================
            # Skala Probabilitas Maksimum 60%
            # ======================
            max_proba = max(proba)
            scaled_proba = [(p / max_proba) * 0.6 for p in proba]
            confidence = proba[hasil_encoded]
            confidence_scaled = (confidence / max_proba) * 0.6
            confidence_percent = confidence_scaled * 100
            nama_diagnosa = mapping_diagnosa.get(hasil_encoded, "Tidak diketahui")

            st.success(f"✅ Prediksi Penyakit: **{nama_diagnosa}**")
            st.info(f"📊 Probabilitas Keyakinan Model: **{confidence_percent:.0f}%**")

            # Simpan ke Firebase
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data_prediksi = {
                    "timestamp": timestamp,
                    "usia": usia,
                    "jenis_kelamin": jenis_kelamin_str,
                    "keluhan": keluhan_input,
                    "keluhan_panjang": keluhan_feat,
                    "diagnosa": nama_diagnosa,
                    "confidence": f"{confidence_percent:.2f}%"
                }
                db.child("prediksi_pasien").push(data_prediksi)
                st.success("📡 Data berhasil disimpan ke Firebase Realtime Database.")
            except Exception as e:
                st.warning(f"⚠️ Gagal menyimpan ke Firebase: {e}")

            # Probabilitas Semua Kelas
            st.markdown("### 📈 Probabilitas Semua Kelas:")
            proba_df = pd.DataFrame({
                "Penyakit": [mapping_diagnosa.get(i, f"Kode {i}") for i in range(len(proba))],
                "Probabilitas": scaled_proba
            }).sort_values(by="Probabilitas", ascending=False)
            proba_df["Probabilitas"] = (proba_df["Probabilitas"] * 100).round(2).astype(str) + "%"
            st.dataframe(proba_df, use_container_width=True)

            # Penjelasan Prediksi
            st.markdown("### ℹ️ Alasan Pemilihan Prediksi")
            penjelasan = deskripsi_prediksi(usia, jenis_kelamin, keluhan_input, keluhan_feat, hasil_encoded, df)
            st.markdown(penjelasan)

            # Contoh Pasien Serupa
            st.markdown("### 🔍 Contoh Pasien Serupa di Dataset")
            contoh_data = df[df["Diagnosa"] == hasil_encoded].copy()
            contoh_data["Selisih"] = (
                abs(contoh_data["Usia"] - usia) +
                abs(contoh_data["Jenis Kelamin"] - jenis_kelamin) * 10 +
                abs(contoh_data["Keluhan_Feat"] - keluhan_feat)
            )
            st.dataframe(contoh_data.sort_values("Selisih").head(5).drop(columns=["Selisih"]), use_container_width=True)

    except FileNotFoundError:
        st.error("❌ File 'data_preprocessed.csv' tidak ditemukan di folder 'dataset/'.")
    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan: {e}")

# ==========================
# Jalankan Aplikasi
# ==========================
if __name__ == "__main__":
    prediksi_page()
