import streamlit as st
from pyrebase import pyrebase
import subprocess

# Konfigurasi Firebase
firebaseConfig = {
    "apiKey": "AIzaSyAFVY0GjcLzrg5PrrbmBeZWXJkZGfgihcU",
    "authDomain": "skripsi-86872.firebaseapp.com",
    "databaseURL": "",  # Harap isi URL database Anda jika digunakan
    "projectId": "skripsi-86872",
    "storageBucket": "skripsi-86872.appspot.com",
    "messagingSenderId": "722934043351",
    "appId": "1:722934043351:web:89b5b3794efd96ea519692",
    "measurementId": "G-E1RCLT7E9H"
}

# Inisialisasi Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login():
    """Fungsi Login"""
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Login berhasil!")
            st.session_state['user'] = user  # Simpan user di session
            # Pindah ke halaman `home/index.py`
            subprocess.Popen(["streamlit", "run", "home/index.py"])
            st.stop()  # Hentikan eksekusi halaman saat ini
        except Exception as e:
            st.error(f"Terjadi kesalahan saat login: {e}")

def register():
    """Fungsi Registrasi"""
    st.title("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Konfirmasi Password", type="password")
    register_btn = st.button("Register")

    if register_btn:
        if password != confirm_password:
            st.error("Password dan Konfirmasi Password tidak cocok!")
        else:
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("Registrasi berhasil! Silakan login.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat registrasi: {e}")

def main():
    """Fungsi Utama"""
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    st.sidebar.title("Navigasi")
    menu = st.sidebar.radio("Pilih menu", ["Login", "Register"])

    if menu == "Login":
        login()
    elif menu == "Register":
        register()

if __name__ == "__main__":
    main()
