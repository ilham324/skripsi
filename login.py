import streamlit as st
from pyrebase import pyrebase

# Konfigurasi Firebase
firebaseConfig = {
    "apiKey": "AIzaSyAFVY0GjcLzrg5PrrbmBeZWXJkZGfgihcU",
    "authDomain": "skripsi-86872.firebaseapp.com",
    "databaseURL": "",
    "projectId": "skripsi-86872",
    "storageBucket": "skripsi-86872.appspot.com",
    "messagingSenderId": "722934043351",
    "appId": "1:722934043351:web:89b5b3794efd96ea519692",
    "measurementId": "G-E1RCLT7E9H"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login_page():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state['login'] = True
            st.session_state['email'] = email
            st.success("Login berhasil! Redirecting...")
            st.rerun()  # ✅ menggantikan experimental_rerun
        except Exception as e:
            st.error("Gagal login: email atau password salah.")

def register_page():
    st.title("📝 Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Konfirmasi Password", type="password")
    if st.button("Register"):
        if password != confirm:
            st.error("Password tidak cocok.")
        else:
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("Registrasi berhasil. Silakan login.")
            except Exception as e:
                st.error("Registrasi gagal. Coba email lain.")

def main():
    if 'login' not in st.session_state:
        st.session_state['login'] = False
        st.session_state['email'] = None

    if st.session_state['login']:
        from home import index
        index.main()
    else:
        st.sidebar.title("🔍 Autentikasi")
        menu = st.sidebar.radio("Pilih menu", ["Login", "Register"])
        if menu == "Login":
            login_page()
        else:
            register_page()

if __name__ == "__main__":
    main()
