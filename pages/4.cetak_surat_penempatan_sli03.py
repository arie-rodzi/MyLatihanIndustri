import streamlit as st
import sqlite3
import os
from docx import Document
from docx2pdf import convert

st.set_page_config(page_title="Modul 4: Cetak Surat Penempatan (SLI03)", layout="wide")
st.title("📄 Modul 4: Cetak Surat Penempatan (SLI03)")

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")

template_path = "template/NS_SLI03.docx"
output_docx = f"generated/surat_penempatan_{pelajar_id}.docx"
output_pdf = f"generated/surat_penempatan_{pelajar_id}.pdf"
os.makedirs("generated", exist_ok=True)

conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

c.execute("SELECT * FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
pelajar = c.fetchone()

c.execute("SELECT * FROM maklumat_industri WHERE pelajar_id=?", (pelajar_id,))
industri = c.fetchone()

if not pelajar or not industri:
    st.warning("Sila lengkapkan maklumat pelajar dan industri dahulu.")
    st.stop()

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

def replace_all_paragraphs(doc, replacements):
    for p in doc.paragraphs:
        for key, val in replacements.items():
            if key in p.text:
                inline = p.runs
                for i in range(len(inline)):
                    if key in inline[i].text:
                        inline[i].text = inline[i].text.replace(key, str(val))

def replace_all_tables(doc, replacements):
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, val in replacements.items():
                    if key in cell.text:
                        cell.text = cell.text.replace(key, str(val))

if st.button("📄 Jana & Papar Surat Penempatan"):
    try:
        doc = Document(template_path)
        replace_all_paragraphs(doc, gantian)
        replace_all_tables(doc, gantian)
        doc.save(output_docx)

        # Convert to PDF
        convert(output_docx, output_pdf)

        # Papar ringkasan surat
        st.write("### 📑 Pratonton Kandungan Surat:")
        for key, val in gantian.items():
            st.write(f"- **{key}** → {val}")

        # Muat turun PDF
        with open(output_pdf, "rb") as f:
            st.download_button("📥 Muat Turun Surat (PDF)", f, file_name=f"Surat_Penempatan_{pelajar_id}.pdf")
    except Exception as e:
        st.error(f"❌ Ralat semasa jana surat: {e}")
