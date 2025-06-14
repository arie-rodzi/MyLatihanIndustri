import streamlit as st
import sqlite3
import os

DB_FILE = 'database/latihan_industri.db'

def init_logbook():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logbook (
            pelajar_id INTEGER, minggu INTEGER, aktiviti TEXT,
            PRIMARY KEY (pelajar_id, minggu)
        )
    """)
    conn.commit()
    conn.close()

def simpan_log(pelajar_id, minggu, aktiviti):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        REPLACE INTO logbook (pelajar_id, minggu, aktiviti) VALUES (?, ?, ?)
    """, (pelajar_id, minggu, aktiviti))
    conn.commit()
    conn.close()

st.title("Logbook Mingguan (16 Minggu)")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk.")
else:
    init_logbook()
    pelajar_id = st.session_state.user_id
    minggu = st.selectbox("Minggu ke-", list(range(1, 17)))
    aktiviti = st.text_area("Catatan Aktiviti Mingguan")
    if st.button("Simpan Log"):
        simpan_log(pelajar_id, minggu, aktiviti)
        st.success(f"Log Minggu {minggu} disimpan.")