import streamlit as st
import sqlite3

DB_FILE = 'database/latihan_industri.db'

def login(no_pelajar, katalaluan):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT pelajar_id FROM users WHERE pelajar_id=? AND katalaluan=?", (no_pelajar, katalaluan))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

st.set_page_config(page_title="Sistem Latihan Industri", layout="wide")
st.title("📘 Sistem Latihan Industri UiTM")

if 'user_id' not in st.session_state:
    no_pelajar = st.text_input("No. Pelajar")
    katalaluan = st.text_input("Katalaluan", type="password")
    if st.button("Log Masuk"):
        user_id = login(no_pelajar, katalaluan)
        if user_id:
            st.session_state.user_id = user_id
            st.success("Log masuk berjaya.")
            st.experimental_rerun()
        else:
            st.error("Maklumat tidak sah.")
else:
    st.success(f"Selamat datang, Pelajar ID: {st.session_state.user_id}")
    st.info("Sila gunakan menu di sebelah kiri untuk mengakses modul.")
