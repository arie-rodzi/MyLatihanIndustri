import streamlit as st
import sqlite3
import os

DB_FILE = 'database/latihan_industri.db'
UPLOAD_DIR = 'uploads/passport'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_maklumat_pelajar_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS maklumat_pelajar (
            pelajar_id INTEGER PRIMARY KEY,
            nama TEXT, no_ic TEXT, no_pelajar TEXT, program TEXT, alamat TEXT,
            no_tel TEXT, emel TEXT, passport TEXT
        )
    """)
    conn.commit()
    conn.close()

def simpan_maklumat(data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        REPLACE INTO maklumat_pelajar 
        (pelajar_id, nama, no_ic, no_pelajar, program, alamat, no_tel, emel, passport) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

st.title("Borang Maklumat Peribadi (BLI-01)")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk sebagai pelajar terlebih dahulu.")
else:
    init_maklumat_pelajar_table()
    pelajar_id = st.session_state.user_id
    nama = st.text_input("Nama Penuh")
    no_ic = st.text_input("No. Kad Pengenalan")
    no_pelajar = st.text_input("No. Pelajar")
    program = st.text_input("Program")
    alamat = st.text_area("Alamat")
    no_tel = st.text_input("No. Telefon")
    emel = st.text_input("Emel")
    passport = st.file_uploader("Gambar Passport", type=["jpg", "jpeg", "png"])

    if st.button("Simpan Maklumat"):
        if passport:
            passport_path = os.path.join(UPLOAD_DIR, f"{pelajar_id}_{passport.name}")
            with open(passport_path, "wb") as f:
                f.write(passport.getbuffer())
            simpan_maklumat((pelajar_id, nama, no_ic, no_pelajar, program, alamat, no_tel, emel, passport_path))
            st.success("Maklumat peribadi berjaya disimpan.")
        else:
            st.warning("Sila muat naik gambar passport.")
