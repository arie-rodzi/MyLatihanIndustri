import streamlit as st
import sqlite3
import os
from docx import Document

TEMPLATE = "template/NS SLI01_DLI01_BLI02.docx"
GENERATED = "generated/borang_permohonan.docx"
DB_FILE = 'database/latihan_industri.db'

def fetch_data(pelajar_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
    pelajar = c.fetchone()
    c.execute("SELECT * FROM penempatan_pelajar WHERE pelajar_id=?", (pelajar_id,))
    penempatan = c.fetchone()
    conn.close()
    return pelajar, penempatan

def generate_form(pelajar, penempatan):
    doc = Document(TEMPLATE)
    ganti = {
        "<<nama>>": pelajar[1], "<<no_ic>>": pelajar[2], "<<no_pelajar>>": pelajar[3],
        "<<program>>": pelajar[4], "<<alamat>>": pelajar[5], "<<no_tel>>": pelajar[6],
        "<<emel>>": pelajar[7], "<<nama_syarikat>>": penempatan[1], "<<alamat_syarikat>>": penempatan[2],
        "<<pegawai>>": penempatan[3], "<<emel_pegawai>>": penempatan[4], "<<tel_pegawai>>": penempatan[5],
        "<<tarikh_mula>>": penempatan[6], "<<tarikh_tamat>>": penempatan[7]
    }
    for p in doc.paragraphs:
        for k, v in ganti.items():
            if k in p.text:
                p.text = p.text.replace(k, v)
    doc.save(GENERATED)

st.title("Cetak Borang Permohonan (SLI01/DLI01/BLI02)")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk terlebih dahulu.")
else:
    pelajar, penempatan = fetch_data(st.session_state.user_id)
    if pelajar and penempatan:
        if st.button("Jana Borang Permohonan"):
            generate_form(pelajar, penempatan)
            with open(GENERATED, "rb") as f:
                st.download_button("Muat Turun Borang", f, file_name="Borang_Permohonan_LI.docx")
    else:
        st.info("Maklumat pelajar atau penempatan belum lengkap.")