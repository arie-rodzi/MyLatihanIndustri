import streamlit as st
import sqlite3

st.set_page_config(page_title="Senarai Pelajar Mengikut Penyelia Akademik", layout="wide")
st.title("📄 Senarai Pelajar & Maklumat Industri Berdasarkan Penyelia Akademik")

# Sambungan ke pangkalan data
conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Input ID penyelia
penyelia_id = st.text_input("Masukkan ID Penyelia Akademik (contoh: A001)")
search = st.button("Cari Pelajar")

if search and penyelia_id:
    # Semak kewujudan ID
    c.execute("SELECT COUNT(*) FROM maklumat_pelajar WHERE penyelia_akademik_id=?", (penyelia_id,))
    if c.fetchone()[0] == 0:
        st.error("❌ Tiada pelajar dijumpai untuk ID ini.")
    else:
        # Ambil maklumat lengkap pelajar dan industri
        c.execute("""
            SELECT 
                p.nama, p.pelajar_id, p.kod_program,
                i.nama_syarikat, i.alamat1, i.alamat2, i.bandar, i.poskod, i.negeri,
                i.nama_pegawai, i.emel_pegawai, i.telefon_pegawai
            FROM maklumat_pelajar p
            JOIN maklumat_industri i ON p.pelajar_id = i.pelajar_id
            WHERE p.penyelia_akademik_id = ?
        """, (penyelia_id,))
        results = c.fetchall()

        if results:
            st.write(f"### 📋 Senarai Pelajar di bawah penyelia `{penyelia_id}`")
            for r in results:
                nama_pelajar, pelajar_id, program, syarikat, alamat1, alamat2, bandar, poskod, negeri, pegawai, emel, telefon = r
                alamat_penuh = f"{alamat1}, {alamat2}, {bandar}, {poskod}, {negeri}"
                st.markdown(f"""
                **Nama Pelajar:** {nama_pelajar}  
                **ID Pelajar:** {pelajar_id}  
                **Program:** {program}  
                **Nama Syarikat:** {syarikat}  
                **Alamat:** {alamat_penuh}  
                **Penyelia Industri:** {pegawai}  
                **Emel Pegawai:** {emel}  
                **Telefon Pegawai:** {telefon}  
                ---
                """)
        else:
            st.warning("Pelajar ditemui, tetapi belum lengkapkan maklumat industri.")

conn.close()
