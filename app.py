import streamlit as st
import sqlite3
import os

# Lokasi fail database
DB_FILE = 'database/latihan_industri.db'

# Pastikan folder wujud
os.makedirs("database", exist_ok=True)

# Fungsi login
def login(no_pelajar, katalaluan):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT pelajar_id, peranan FROM users WHERE pelajar_id=? AND katalaluan=?", (no_pelajar, katalaluan))
    result = c.fetchone()
    conn.close()
    return result if result else None

# Sediakan jadual users jika belum wujud
def setup_users_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            pelajar_id TEXT PRIMARY KEY,
            katalaluan TEXT NOT NULL,
            peranan TEXT NOT NULL
        )
    ''')
    # Contoh pengguna untuk login
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", ("2023123456", "1234", "pelajar"))
    conn.commit()
    conn.close()

setup_users_table()

# Konfigurasi halaman
st.set_page_config(page_title="Sistem Latihan Industri", layout="wide")
st.title("📘 Sistem Latihan Industri UiTM")

# Log masuk
if 'user_id' not in st.session_state:
    no_pelajar = st.text_input("No. Pelajar / ID")
    katalaluan = st.text_input("Katalaluan", type="password")
    if st.button("Log Masuk"):
        user_data = login(no_pelajar, katalaluan)
        if user_data:
            st.session_state.user_id = user_data[0]
            st.session_state.user_role = user_data[1]
            st.success(f"Log masuk berjaya sebagai {st.session_state.user_role}.")
            st.rerun()
        else:
            st.error("Maklumat tidak sah.")
else:
    st.success(f"Selamat datang, ID: {st.session_state.user_id} ({st.session_state.user_role})")
    st.info("Sila gunakan menu di sebelah kiri untuk mengakses modul mengikut peranan anda.")
