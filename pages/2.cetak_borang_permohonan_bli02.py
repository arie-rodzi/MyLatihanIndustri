import streamlit as st
import sqlite3
from docx import Document
from datetime import datetime
import os

st.set_page_config(page_title="Cetak Surat Penempatan", layout="wide")
st.title("📄 Cetak Surat Penempatan (SLI-03)")

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")

conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Dapatkan maklumat pelajar
c.execute("SELECT nama, no_ic, kod_program, emel FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))

data_pelajar = c.fetchone()

# Dapatkan maklumat penyelaras
c.execute("SELECT status_lulus, nama_penyelaras, email_penyelaras, kod_program, tarikh_lulus FROM status_permohonan WHERE pelajar_id=?", (pelajar_id,))
data_permohonan = c.fetchone()

if not data_pelajar or not data_permohonan:
    st.error("Maklumat pelajar atau permohonan tidak lengkap.")
    st.stop()

nama, no_ic, kod_program, email = data_pelajar
status_lulus, nama_penyelaras, email_penyelaras, kod_program_permohonan, tarikh_lulus = data_permohonan

# Load template
template_path = "template/NS SLI-03 Surat Penempatan Latihan Industri di Organisasi.docx"
doc = Document(template_path)

# Fungsi ganti placeholder dalam semua run
def ganti_placeholder(doc, placeholder, value):
    for p in doc.paragraphs:
        for run in p.runs:
            if placeholder in run.text:
                run.text = run.text.replace(placeholder, value)

# Ganti semua placeholder
today = datetime.today().strftime("%Y-%m-%d")
ganti_placeholder(doc, "«NAMA_PENUH_HURUF_BESAR»", nama.upper())
ganti_placeholder(doc, "«NOMBOR_KAD_PENGENALAN»", no_ic)
ganti_placeholder(doc, "«NOMBOR_ID_PELAJAR»", pelajar_id)
ganti_placeholder(doc, "«NAMA_PROGRAM»", kod_program)
ganti_placeholder(doc, "«TARIKH_SURAT»", today)
ganti_placeholder(doc, "«TARIKH_MULA_LI»", "2025-09-02")
ganti_placeholder(doc, "«TARIKH_TAMAT_LI»", "2025-12-20")
ganti_placeholder(doc, "«NAMA_PENYELARAS»", nama_penyelaras)
ganti_placeholder(doc, "«email_penyelaras»", email_penyelaras)
ganti_placeholder(doc, "«kod_pogram»", kod_program)
ganti_placeholder(doc, "«EMEL_PELAJAR»", email)

# Simpan dokumen
output_dir = "generated"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"Surat_Penempatan_{pelajar_id}.docx")
doc.save(output_path)

with open(output_path, "rb") as file:
    st.success("Surat penempatan berjaya dijana.")
    st.download_button("📥 Muat Turun Surat", file, file_name=f"Surat_Penempatan_{pelajar_id}.docx")

