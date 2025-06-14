import streamlit as st
import sqlite3
import os
from docx import Document

TEMPLATE = "template/NS BLI-04 Borang Lapor Diri Di Organisasi.docx"
GENERATED = "generated/borang_lapor_diri.docx"
DB_FILE = 'database/latihan_industri.db'

def fetch_pelajar(pelajar_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
    d1 = c.fetchone()
    c.execute("SELECT * FROM penempatan_pelajar WHERE pelajar_id=?", (pelajar_id,))
    d2 = c.fetchone()
    conn.close()
    return d1, d2

def generate_borang(d1, d2):
    doc = Document(TEMPLATE)
    replace = {
        "<<nama>>": d1[1], "<<no_ic>>": d1[2], "<<no_pelajar>>": d1[3],
        "<<program>>": d1[4], "<<nama_syarikat>>": d2[1], "<<alamat>>": d2[2],
        "<<pegawai>>": d2[3], "<<no_tel>>": d2[5], "<<emel>>": d2[4],
        "<<tarikh_mula>>": d2[6], "<<tarikh_tamat>>": d2[7]
    }
    for p in doc.paragraphs:
        for k, v in replace.items():
            if k in p.text:
                p.text = p.text.replace(k, v)
    doc.save(GENERATED)

st.title("Cetak Borang Lapor Diri (BLI-04)")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk.")
else:
    d1, d2 = fetch_pelajar(st.session_state.user_id)
    if d1 and d2:
        if st.button("Jana Borang"):
            generate_borang(d1, d2)
            with open(GENERATED, "rb") as f:
                st.download_button("Muat Turun Borang", f, file_name="BLI-04_Lapor_Diri.docx")
    else:
        st.info("Maklumat belum lengkap.")