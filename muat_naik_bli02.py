import streamlit as st
import sqlite3
import os

DB_FILE = 'database/latihan_industri.db'
UPLOAD_DIR = 'uploads/bli02'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_penempatan_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS penempatan_pelajar (
            pelajar_id INTEGER PRIMARY KEY,
            nama_syarikat TEXT, alamat TEXT, pegawai TEXT,
            emel TEXT, no_tel TEXT, tarikh_mula TEXT, tarikh_tamat TEXT, fail TEXT
        )
    """)
    conn.commit()
    conn.close()

def simpan_penempatan(data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        REPLACE INTO penempatan_pelajar 
        (pelajar_id, nama_syarikat, alamat, pegawai, emel, no_tel, tarikh_mula, tarikh_tamat, fail)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

st.title("Muat Naik Borang BLI-02 & Maklumat Penempatan")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk sebagai pelajar terlebih dahulu.")
else:
    init_penempatan_table()
    pelajar_id = st.session_state.user_id
    nama_syarikat = st.text_input("Nama Syarikat")
    alamat = st.text_area("Alamat Syarikat")
    pegawai = st.text_input("Nama Pegawai Penilai")
    emel = st.text_input("Emel Pegawai")
    no_tel = st.text_input("No. Telefon Pegawai")
    tarikh_mula = st.date_input("Tarikh Mula LI")
    tarikh_tamat = st.date_input("Tarikh Tamat LI")
    bli02 = st.file_uploader("Muat Naik Borang BLI-02", type=["pdf", "docx"])

    if st.button("Hantar BLI-02"):
        if bli02:
            fail_path = os.path.join(UPLOAD_DIR, f"{pelajar_id}_{bli02.name}")
            with open(fail_path, "wb") as f:
                f.write(bli02.getbuffer())
            simpan_penempatan((pelajar_id, nama_syarikat, alamat, pegawai, emel, no_tel,
                               tarikh_mula.isoformat(), tarikh_tamat.isoformat(), fail_path))
            st.success("Borang BLI-02 dan maklumat penempatan berjaya dihantar.")
        else:
            st.warning("Sila muat naik fail BLI-02.")