import streamlit as st
import diagnosa
import tentang
import kontak

def main():
    st.sidebar.title("📋 Menu Navigasi")
    menu = ["Beranda", "Prediksi Penyakit", "Tentang Aplikasi", "Kontak"]
    pilihan = st.sidebar.selectbox("Pilih Menu", menu)

    if pilihan == "Beranda":
        st.title("👋 Selamat Datang di Aplikasi Prediksi Penyakit")
        st.markdown("Gunakan menu di samping untuk mulai melihat data, menganalisis keluhan, atau membaca informasi aplikasi.")
        st.image("https://cdn-icons-png.flaticon.com/512/3209/3209265.png", width=300)

    elif pilihan == "Prediksi Penyakit":
        diagnosa.diagnosa_page()

    elif pilihan == "Tentang Aplikasi":
        tentang.tentang_page()

    elif pilihan == "Kontak":
        kontak.kontak_page()

if __name__ == "__main__":
    main()
