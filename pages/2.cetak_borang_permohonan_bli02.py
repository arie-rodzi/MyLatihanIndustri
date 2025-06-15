import streamlit as st
import sqlite3
from docx import Document
from io import BytesIO
from datetime import date
from docx2pdf import convert
import os
from tempfile import NamedTemporaryFile
from pdf2image import convert_from_path
from PIL import Image

# Semakan login
if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

st.set_page_config(page_title="Modul 2: Cetak Borang Permohonan", layout="wide")
st.title("📄 Modul 2: Cetak Borang Permohonan Latihan Industri")

pelajar_id = st.session_state.get("user_id", "")

# Sambung ke database
conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Semak maklumat pelajar
c.execute("SELECT nama, ic, program, email FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
pelajar = c.fetchone()

# Semak status kelulusan penyelaras
c.execute("SELECT status_lulus, nama_penyelaras, email_penyelaras, kod_program, tarikh_lulus FROM status_permohonan WHERE pelajar_id=?", (pelajar_id,))
status = c.fetchone()

if not pelajar:
    st.warning("Maklumat pelajar belum lengkap. Sila isi Modul 1 terlebih dahulu.")
    st.stop()

if not status or status[0] != "lulus":
    st.info("Permohonan anda belum diluluskan oleh penyelaras program.")
    st.stop()

# Dapatkan data
nama, ic, program, email = pelajar
_, nama_penyelaras, email_penyelaras, kod_program, _ = status
today = date.today().strftime("%Y-%m-%d")

# Buka dan isi template
doc = Document("templates/NS SLI01_DLI01_BLI02.docx")
for p in doc.paragraphs:
    p.text = p.text.replace("«NOMBOR_ID_PELAJAR»", pelajar_id)
    p.text = p.text.replace("«NOMBOR_KAD_PENGENALAN»", ic)
    p.text = p.text.replace("«NAMA_PENUH_HURUF_BESAR»", nama.upper())
    p.text = p.text.replace("« NAMA_PROGRAM »", program)
    p.text = p.text.replace("«TARIKH_SURAT»", today)
    p.text = p.text.replace("«TARIKH_MULA_LI»", "2025-09-02")
    p.text = p.text.replace("«TARIKH_TAMAT_LI»", "2025-12-20")
    p.text = p.text.replace("«NAMA_PENYELARAS»", nama_penyelaras)
    p.text = p.text.replace("«email_penyelaras»", email_penyelaras)
    p.text = p.text.replace("«kod_pogram»", kod_program)
    p.text = p.text.replace("«ALAMAT_EMEL»", email)

# Simpan ke fail sementara .docx
with NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
    doc.save(tmp_docx.name)

# Tukar ke PDF
pdf_path = tmp_docx.name.replace(".docx", ".pdf")
convert(tmp_docx.name, pdf_path)

# Papar PDF sebagai imej
images = convert_from_path(pdf_path)
st.write("### Pratonton Surat Permohonan (PDF)")
for img in images:
    st.image(img, use_column_width=True)

# Muat turun PDF
with open(pdf_path, "rb") as pdf_file:
    st.download_button("📥 Muat Turun Surat (PDF)", data=pdf_file, file_name="Surat_Permohonan_LI.pdf", mime="application/pdf")
