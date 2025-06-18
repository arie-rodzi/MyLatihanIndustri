import streamlit as st
import sqlite3
import os
from docx import Document

st.set_page_config(page_title="Cetak Borang Lapor Diri (BLI04)", layout="wide")
st.title("📄 Cetak Borang Lapor Diri (BLI04)")

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")
template_path = "templates/NS BLI-04 Borang Lapor Diri Di Organisasi.docx"
output_path = f"generated/borang_lapor_diri_{pelajar_id}.docx"

os.makedirs("generated", exist_ok=True)

conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Pastikan maklumat tersedia
c.execute("SELECT * FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
pelajar = c.fetchone()

c.execute("SELECT * FROM maklumat_industri WHERE pelajar_id=?", (pelajar_id,))
industri = c.fetchone()

if not pelajar or not industri:
    st.warning("Sila lengkapkan maklumat peribadi dan industri dahulu.")
    st.stop()

if st.button("Jana Borang Lapor Diri"):
    doc = Document(template_path)
    
    alamat_syarikat = ", ".join([industri[2], industri[3], industri[4], industri[5], industri[6]])
    
    ganti = {
        "<<nama>>": pelajar[1],
        "<<no_ic>>": pelajar[2],
        "<<no_pelajar>>": pelajar[0],
        "<<program>>": pelajar[3],
        "<<syarikat>>": industri[1],
        "<<alamat_syarikat>>": alamat_syarikat,
        "<<pegawai>>": industri[7],
        "<<telefon_pegawai>>": industri[9],
        "<<emel_pegawai>>": industri[8],
        "<<tarikh_mula>>": industri[10],
        "<<tarikh_tamat>>": industri[11],
    }

    for p in doc.paragraphs:
        for key, val in ganti.items():
            if key in p.text:
                p.text = p.text.replace(key, val)

    doc.save(output_path)
    with open(output_path, "rb") as f:
        st.download_button("📥 Muat Turun Borang", f, file_name=f"Borang_Lapor_Diri_{pelajar_id}.docx")
