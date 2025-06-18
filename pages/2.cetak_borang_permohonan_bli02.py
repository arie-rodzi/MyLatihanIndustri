import streamlit as st
import sqlite3
import os
import zipfile
import shutil
from datetime import date

# Konfigurasi halaman
st.set_page_config(page_title="Cetak Borang Permohonan BLI-02", layout="wide")
st.title("📄 Modul 2: Cetak Borang Permohonan BLI-02")

# Semakan login
if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

# Tetapan laluan template dan output
TEMPLATE_PATH = "templates/NS_SLI01_DLI01_BLI02_FIXED.docx"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fungsi gantian teks dalam .docx XML
def replace_docx_xml(template_path, replacements, output_path):
    temp_zip = "temp_docx.zip"
    shutil.copyfile(template_path, temp_zip)

    with zipfile.ZipFile(temp_zip, 'r') as zin:
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    text = data.decode("utf-8")
                    for key, value in replacements.items():
                        text = text.replace(key, value)
                    data = text.encode("utf-8")
                zout.writestr(item, data)

    os.remove(temp_zip)

# Sambung ke pangkalan data
conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Dapatkan ID pelajar dari sesi
pelajar_id = st.session_state.get("user_id")
st.write("🆔 ID Pelajar:", pelajar_id)

# Ambil maklumat pelajar dan penyelaras (BUANG `mp.email`)
try:
    c.execute("""
        SELECT mp.nama, mp.no_ic, mp.kod_program,
               sp.nama_penyelaras, sp.email_penyelaras, sp.tarikh_lulus
        FROM maklumat_pelajar mp
        LEFT JOIN status_permohonan sp ON mp.pelajar_id = sp.pelajar_id
        WHERE mp.pelajar_id = ?
    """, (pelajar_id,))
    data = c.fetchone()
except Exception as e:
    st.error(f"❌ SQL Error: {e}")
    st.stop()

if not data:
    st.error("⚠️ Maklumat pelajar tidak dijumpai.")
    st.stop()

# Tetapkan data
nama_pelajar, no_ic, kod_program, nama_penyelaras, email_penyelaras, tarikh_lulus = data

# Tetapkan pengganti
replacements = {
    "«NAMA_PENUH_HURUF_BESAR»": nama_pelajar.upper(),
    "«NOMBOR_KAD_PENGENALAN»": no_ic,
    "«NOMBOR_ID_PELAJAR»": pelajar_id,
    "«NAMA_PROGRAM»": kod_program,
    "«NAMA_PENYELARAS»": nama_penyelaras,
    "«KOD_PROGRAM»": kod_program
}

# Laluan simpanan fail akhir
output_path = os.path.join(OUTPUT_DIR, f"Surat_Permohonan_SLI01_{pelajar_id}_FINAL.docx")

# Proses penggantian
replace_docx_xml(TEMPLATE_PATH, replacements, output_path)

# Papar hasil
with open(output_path, "rb") as file:
    st.download_button(
        label="📥 Muat Turun Surat Permohonan SLI01",
        data=file,
        file_name=os.path.basename(output_path),
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
