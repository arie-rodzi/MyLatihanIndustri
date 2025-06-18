import streamlit as st
import sqlite3
from datetime import datetime
import os
import shutil
import zipfile
from pathlib import Path

st.set_page_config(page_title="Cetak Surat Permohonan SLI-01", layout="wide")
st.title("📄 Cetak Surat Permohonan SLI-01")

# Semak akses
if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")

# Sambung ke pangkalan data
conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Ambil maklumat pelajar & penyelaras
c.execute("""
    SELECT p.pelajar_id, p.nama, p.no_ic, p.kod_program, p.emel,
           s.nama_penyelaras, s.email_penyelaras, s.kod_program, s.tarikh_lulus
    FROM maklumat_pelajar p
    JOIN status_permohonan s ON p.pelajar_id = s.pelajar_id
    WHERE p.pelajar_id = ?
""", (pelajar_id,))
data = c.fetchone()

if not data:
    st.error("Maklumat pelajar atau status permohonan tidak lengkap.")
    st.stop()

# Data pengganti
replacements = {
    "«NOMBOR_ID_PELAJAR»": data[0],
    "«NAMA_PENUH_HURUF_BESAR»": data[1].upper(),
    "«NOMBOR_KAD_PENGENALAN»": data[2],
    "«NAMA_PROGRAM»": data[3],
    "«EMEL_PELAJAR»": data[4],
    "«NAMA_PENYELARAS»": data[5],
    "«email_penyelaras»": data[6],
    "«kod_pogram»": data[7],
    "«TARIKH_SURAT»": data[8],
    "«TARIKH_MULA_LI»": "1/10/2025",
    "«TARIKH_TAMAT_LI»": "31/3/2026"
}

template_path = "template/NS_SLI01_DLI01_BLI02_FIXED.docx"

def replace_docx_xml(template_path, replacements, output_path):
    temp_zip = template_path.replace(".docx", ".zip")
    shutil.copyfile(template_path, temp_zip)
    extract_dir = Path("temp_extract")
    with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    doc_xml_path = extract_dir / "word" / "document.xml"
    with open(doc_xml_path, "r", encoding="utf-8") as f:
        content = f.read()
    for key, val in replacements.items():
        content = content.replace(key, val)
    with open(doc_xml_path, "w", encoding="utf-8") as f:
        f.write(content)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as docx_zip:
        for foldername, _, filenames in os.walk(extract_dir):
            for filename in filenames:
                file_path = Path(foldername) / filename
                arcname = file_path.relative_to(extract_dir)
                docx_zip.write(file_path, arcname)
    shutil.rmtree(extract_dir)
    os.remove(temp_zip)

# Butang jana surat
if st.button("🖨️ Jana Surat Permohonan"):
    output_file = f"Surat_Permohonan_SLI01_{pelajar_id}_FINAL.docx"
    output_path = f"/mnt/data/{output_file}"
    replace_docx_xml(template_path, replacements, output_path)
    st.success("Surat berjaya dijana.")
    with open(output_path, "rb") as f:
        st.download_button("📥 Muat Turun Surat", f, file_name=output_file)
