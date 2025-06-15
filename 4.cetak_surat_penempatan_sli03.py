
import streamlit as st
import sqlite3
import os
from docx import Document

st.set_page_config(page_title="Cetak Surat Penempatan (SLI03)", layout="wide")
st.title("📄 Cetak Surat Penempatan (SLI03)")

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")
template_path = "template/surat_penempatan_sli03.docx"
output_path = f"generated/surat_penempatan_{pelajar_id}.docx"

os.makedirs("generated", exist_ok=True)

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Pastikan maklumat tersedia
c.execute("SELECT * FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
pelajar = c.fetchone()

c.execute("SELECT * FROM maklumat_industri WHERE pelajar_id=?", (pelajar_id,))
industri = c.fetchone()

if not pelajar or not industri:
    st.warning("Sila lengkapkan maklumat peribadi dan maklumat industri dahulu.")
    st.stop()

if st.button("Jana Surat Penempatan"):
    doc = Document(template_path)
    gantian = {
        "<<nama>>": pelajar[1],
        "<<no_ic>>": pelajar[2],
        "<<no_pelajar>>": pelajar[0],
        "<<program>>": pelajar[3],
        "<<syarikat>>": industri[1],
        "<<alamat_syarikat>>": industri[2],
        "<<pegawai>>": industri[3],
        "<<telefon_pegawai>>": industri[5],
        "<<emel_pegawai>>": industri[4],
        "<<tarikh_mula>>": industri[6],
        "<<tarikh_tamat>>": industri[7],
    }

    for p in doc.paragraphs:
        for key, val in gantian.items():
            if key in p.text:
                p.text = p.text.replace(key, val)

    doc.save(output_path)
    with open(output_path, "rb") as f:
        st.download_button("📥 Muat Turun Surat", f, file_name=f"Surat_Penempatan_{pelajar_id}.docx")
