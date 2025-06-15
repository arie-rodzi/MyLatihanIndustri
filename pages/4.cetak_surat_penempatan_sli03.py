import streamlit as st
import sqlite3
import os
from docx import Document

# Konfigurasi Streamlit
st.set_page_config(page_title="Cetak Surat Penempatan (SLI03)", layout="wide")
st.title("📄 Modul 4: Cetak Surat Penempatan (SLI03)")

# Semakan login pelajar
if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

# ID pelajar dari sesi
pelajar_id = st.session_state.get("user_id", "")
if not pelajar_id:
    st.error("ID pelajar tidak dijumpai dalam sesi.")
    st.stop()

# Laluan template dan output
template_path = "templates/NS SLI-03 Surat Penempatan Latihan Industri di Organisasi.docx"
output_dir = "generated"
output_path = os.path.join(output_dir, f"surat_penempatan_{pelajar_id}.docx")
os.makedirs(output_dir, exist_ok=True)

# Sambungan ke pangkalan data
conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Ambil maklumat pelajar dan industri
c.execute("SELECT * FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
pelajar = c.fetchone()

c.execute("SELECT * FROM maklumat_industri WHERE pelajar_id=?", (pelajar_id,))
industri = c.fetchone()

# Semakan data wajib
if not pelajar:
    st.warning("❌ Maklumat pelajar tidak dijumpai. Sila lengkapkan Modul 2.")
    st.stop()
if not industri:
    st.warning("❌ Maklumat industri tidak dijumpai. Sila lengkapkan Modul 3.")
    st.stop()

# Jana surat penempatan
if st.button("📄 Jana Surat Penempatan"):
    try:
        if not os.path.exists(template_path):
            st.error(f"❌ Template tidak dijumpai: {template_path}")
            st.stop()

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

        # Gantian teks dalam semua perenggan
        for p in doc.paragraphs:
            for key, val in gantian.items():
                if key in p.text:
                    p.text = p.text.replace(key, str(val))

        # Simpan dokumen
        doc.save(output_path)

        # Butang muat turun
        with open(output_path, "rb") as f:
            st.success("✅ Surat penempatan berjaya dijana.")
            st.download_button(
                label="📥 Muat Turun Surat Penempatan",
                data=f,
                file_name=f"Surat_Penempatan_{pelajar_id}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    except Exception as e:
        st.error(f"Ralat semasa menjana surat: {str(e)}")
