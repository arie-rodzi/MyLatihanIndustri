import streamlit as st
import sqlite3
import os
from docx import Document

st.set_page_config(page_title="Cetak Borang Lapor Diri (BLI04)", layout="wide")
st.title("📄 Cetak Borang Lapor Diri (BLI04)")

# Semakan login
if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

# ID pelajar dan laluan fail
pelajar_id = st.session_state.get("user_id", "")
template_path = "templates/NS BLI-04 Borang Lapor Diri Di Organisasi.docx"
output_path = f"generated/borang_lapor_diri_{pelajar_id}.docx"
os.makedirs("generated", exist_ok=True)

# Sambungan ke database
conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Ambil data pelajar
c.execute("SELECT * FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
pelajar = c.fetchone()

# Ambil data industri
c.execute("SELECT * FROM maklumat_industri WHERE pelajar_id=?", (pelajar_id,))
industri = c.fetchone()

# Ambil data penyelaras
c.execute("SELECT nama_penyelaras, email_penyelaras FROM status_permohonan WHERE pelajar_id=?", (pelajar_id,))
penyelaras = c.fetchone()

# Semak kewujudan data
if not pelajar or not industri or not penyelaras:
    st.warning("Sila lengkapkan maklumat peribadi, industri dan status permohonan dahulu.")
    st.stop()

# Proses alamat syarikat
alamat_syarikat = ", ".join([industri[2], industri[3], industri[4], industri[5], industri[6]])

# Proses jawatan penyelaras
penyelaras_nama = penyelaras[0]
penyelaras_emel = penyelaras[1]
penyelaras_jawatan = f"Penyelaras Latihan Industri {pelajar[3]}"

# Gantian isi borang
ganti = {
    "<<nama>>": pelajar[1],
    "<<no_ic>>": pelajar[2],
    "<<no_pelajar>>": pelajar[0],
    "<<program>>": pelajar[3],
    "<<syarikat>>": industri[1],
    "<<alamat_syarikat>>": alamat_syarikat,
    "<<pegawai>>": industri[7],
    "<<jawatan_pegawai>>": industri[12] if len(industri) > 12 and industri[12] else "<<jawatan_pegawai>>",
    "<<telefon_pegawai>>": industri[9],
    "<<emel_pegawai>>": industri[8],
    "<<tarikh_mula>>": industri[10],
    "<<tarikh_tamat>>": industri[11],
    "<<penyelaras_nama>>": penyelaras_nama,
    "<<penyelaras_emel>>": penyelaras_emel,
    "<<penyelaras_jawatan>>": penyelaras_jawatan,
}

# Butang jana dan muat turun borang
if st.button("Jana Borang Lapor Diri"):
    doc = Document(template_path)

    for p in doc.paragraphs:
        for key, val in ganti.items():
            if key in p.text:
                p.text = p.text.replace(key, val)

    doc.save(output_path)

    with open(output_path, "rb") as f:
        st.download_button("📥 Muat Turun Borang", f, file_name=f"Borang_Lapor_Diri_{pelajar_id}.docx")
