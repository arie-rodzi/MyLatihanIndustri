import streamlit as st
import sqlite3
import os
from docx import Document

TEMPLATE = "template/NS SLI-03 Surat Penempatan Latihan Industri di Organisasi.docx"
GENERATED = "generated/surat_penempatan.docx"
DB_FILE = 'database/latihan_industri.db'

def fetch_penempatan(pelajar_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM penempatan_pelajar WHERE pelajar_id=?", (pelajar_id,))
    data = c.fetchone()
    conn.close()
    return data

def generate_surat(data):
    doc = Document(TEMPLATE)
    replacements = {
        "<<nama_syarikat>>": data[1],
        "<<alamat>>": data[2],
        "<<pegawai>>": data[3],
        "<<emel>>": data[4],
        "<<no_tel>>": data[5],
        "<<tarikh_mula>>": data[6],
        "<<tarikh_tamat>>": data[7]
    }
    for p in doc.paragraphs:
        for key, val in replacements.items():
            if key in p.text:
                p.text = p.text.replace(key, val)
    doc.save(GENERATED)

st.title("Cetak Surat Penempatan (SLI-03)")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk.")
else:
    data = fetch_penempatan(st.session_state.user_id)
    if data:
        if st.button("Jana Surat"):
            generate_surat(data)
            with open(GENERATED, "rb") as f:
                st.download_button("Muat Turun Surat", f, file_name="SLI-03_Surat_Penempatan.docx")
    else:
        st.info("Maklumat penempatan belum lengkap.")
