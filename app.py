
import streamlit as st
import sqlite3

DB_FILE = 'database/latihan_industri.db'

def login(no_pelajar, katalaluan):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT pelajar_id, peranan FROM users WHERE pelajar_id=? AND katalaluan=?", (no_pelajar, katalaluan))
    result = c.fetchone()
    conn.close()
    return result

st.set_page_config(page_title="Sistem Latihan Industri", layout="wide")
st.title("📘 Sistem Latihan Industri UiTM")

peranan_label = {
    "pelajar": "Pelajar",
    "penyelia_industri": "Penyelia Industri",
    "penyelia_akademik": "Penyelia Akademik",
    "penyelaras": "Penyelaras Program"
}

if 'user_id' not in st.session_state:
    no_pelajar = st.text_input("No. Pelajar / ID")
    katalaluan = st.text_input("Katalaluan", type="password")
    if st.button("Log Masuk"):
        user_data = login(no_pelajar, katalaluan)
        if user_data:
            st.session_state.user_id = user_data[0]
            st.session_state.user_role = user_data[1]
            st.success(f"Log masuk berjaya sebagai {peranan_label.get(st.session_state.user_role, st.session_state.user_role)}.")
            st.rerun()
        else:
            st.error("Maklumat tidak sah.")
else:
    role_label = peranan_label.get(st.session_state.user_role, st.session_state.user_role)
    st.success(f"Selamat datang, ID: {st.session_state.user_id} ({role_label})")
    st.info("Sila gunakan menu di sebelah kiri untuk mengakses modul mengikut peranan anda.")

    if st.button("Log Keluar"):
        st.session_state.clear()
        st.experimental_rerun()
