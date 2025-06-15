
import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="Muat Naik BLI02 & Maklumat Industri", layout="wide")
st.title("📤 Muat Naik Borang BLI-02 dan Isi Maklumat Industri")

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")
upload_dir = "uploaded/bli02"
os.makedirs(upload_dir, exist_ok=True)

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Cipta jadual maklumat industri
c.execute("""
    CREATE TABLE IF NOT EXISTS maklumat_industri (
        pelajar_id TEXT PRIMARY KEY,
        nama_syarikat TEXT,
        alamat TEXT,
        nama_pegawai TEXT,
        emel_pegawai TEXT,
        telefon_pegawai TEXT,
        tarikh_mula TEXT,
        tarikh_tamat TEXT,
        filename TEXT
    )
""")
conn.commit()

# Semak sama ada data sudah ada
c.execute("SELECT * FROM maklumat_industri WHERE pelajar_id=?", (pelajar_id,))
row = c.fetchone()

if row:
    st.success("Maklumat industri telah dihantar.")
    st.write("### Maklumat Syarikat Tersimpan")
    st.write(f"**Nama Syarikat:** {row[1]}")
    st.write(f"**Alamat:** {row[2]}")
    st.write(f"**Nama Pegawai:** {row[3]}")
    st.write(f"**Emel Pegawai:** {row[4]}")
    st.write(f"**Telefon Pegawai:** {row[5]}")
    st.write(f"**Tarikh Mula:** {row[6]}")
    st.write(f"**Tarikh Tamat:** {row[7]}")
    st.markdown(f"[Muat Turun Borang BLI-02]({upload_dir}/{row[8]})")
else:
    with st.form("borang_bli02"):
        nama_syarikat = st.text_input("Nama Syarikat")
        alamat = st.text_area("Alamat Syarikat")
        nama_pegawai = st.text_input("Nama Pegawai Penyelia Industri")
        emel_pegawai = st.text_input("Emel Pegawai")
        telefon_pegawai = st.text_input("Telefon Pegawai")
        tarikh_mula = st.date_input("Tarikh Mula Latihan Industri")
        tarikh_tamat = st.date_input("Tarikh Tamat Latihan Industri")
        uploaded_file = st.file_uploader("Muat naik Borang BLI-02 (PDF/DOCX)", type=["pdf", "docx"])

        submit = st.form_submit_button("Hantar")
        if submit:
            if not uploaded_file:
                st.error("Sila muat naik fail BLI-02.")
            else:
                filename = f"{pelajar_id}_{uploaded_file.name}"
                filepath = os.path.join(upload_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                c.execute("""
                    INSERT INTO maklumat_industri VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pelajar_id, nama_syarikat, alamat, nama_pegawai,
                    emel_pegawai, telefon_pegawai,
                    str(tarikh_mula), str(tarikh_tamat),
                    filename
                ))
                conn.commit()
                st.success("Maklumat dan fail berjaya dihantar.")
                st.experimental_rerun()
