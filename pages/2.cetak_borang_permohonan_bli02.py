import streamlit as st
import sqlite3
from docx import Document
from io import BytesIO
from datetime import date

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
c.execute("SELECT nama, no_ic, kod_program, emel FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
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

# Dapatkan data untuk surat
nama, no_ic, kod_program, emel_pelajar = pelajar
status_lulus, nama_penyelaras, email_penyelaras, kod_program_status, tarikh_lulus = status

# Gantian dalam surat
today = date.today().strftime("%Y-%m-%d")
doc = Document("templates/NS_SLI01_DLI01_BLI02_FIXED.docx")
for p in doc.paragraphs:
    p.text = p.text.replace("«NOMBOR_ID_PELAJAR»", pelajar_id)
    p.text = p.text.replace("«NOMBOR_KAD_PENGENALAN»", no_ic)
    p.text = p.text.replace("«NAMA_PENUH_HURUF_BESAR»", nama.upper())
    p.text = p.text.replace("«NAMA_PROGRAM»", kod_program)
    p.text = p.text.replace("«TARIKH_SURAT»", today)
    p.text = p.text.replace("«TARIKH_MULA_LI»", "2025-09-02")  # boleh ambil dari DB
    p.text = p.text.replace("«TARIKH_TAMAT_LI»", "2025-12-20")
    p.text = p.text.replace("«NAMA_PENYELARAS»", nama_penyelaras)
    p.text = p.text.replace("«EMAIL_PENYELARAS»", email_penyelaras)
    p.text = p.text.replace("«KOD_PROGRAM»", kod_program)
    p.text = p.text.replace("«EMEL_PELAJAR»", emel_pelajar)

# Simpan ke buffer
buffer = BytesIO()
doc.save(buffer)
buffer.seek(0)

# Papar ringkasan
st.success("Permohonan anda telah diluluskan oleh penyelaras.")
st.write("### Pratonton Ringkasan Surat")
st.markdown(f"""
**Nama:** {nama}  
**No Pelajar:** {pelajar_id}  
**Program:** {kod_program}  
**Tarikh Surat:** {today}  
**Penyelaras:** {nama_penyelaras}  
**Email Penyelaras:** {email_penyelaras}
""")

# Butang muat turun
st.download_button(
    "📥 Muat Turun Surat Permohonan",
    data=buffer,
    file_name="Surat_Permohonan_LI.docx",
    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
