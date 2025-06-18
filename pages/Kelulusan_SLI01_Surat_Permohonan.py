import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="Kelulusan SLI-01", layout="wide")
st.title("📄 Kelulusan Surat Permohonan Latihan Industri (SLI-01)")

# Semakan login
if "user_role" not in st.session_state or st.session_state["user_role"] != "penyelaras":
    st.warning("Modul ini hanya untuk penyelaras.")
    st.stop()

# Sambung ke database
conn = sqlite3.connect("database/latihan_industri.final.db")
c = conn.cursor()

# Pastikan jadual status_permohonan wujud
c.execute("""
    CREATE TABLE IF NOT EXISTS status_permohonan (
        pelajar_id TEXT PRIMARY KEY,
        status_lulus TEXT,
        tarikh_lulus TEXT,
        status_sli03 TEXT,
        status_bli02 TEXT
    )
""")
conn.commit()

# Papar semua pelajar dari jadual maklumat_pelajar
c.execute("SELECT pelajar_id, nama FROM maklumat_pelajar")
pelajar_list = c.fetchall()

for pelajar_id, nama in pelajar_list:
    with st.expander(f"{nama} ({pelajar_id})"):
        # Ambil maklumat lengkap pelajar
        c.execute("SELECT ic, program, no_telefon, email, alamat FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
        data = c.fetchone()
        if data:
            ic, program, no_telefon, email, alamat = data
            st.markdown(f"""
            **Maklumat Pelajar:**
            - **No IC:** {ic}
            - **Program:** {program}
            - **No Telefon:** {no_telefon}
            - **Email:** {email}
            - **Alamat:** {alamat}
            """)

        # Semak status permohonan
        c.execute("SELECT status_lulus FROM status_permohonan WHERE pelajar_id=?", (pelajar_id,))
        status_row = c.fetchone()
        status_lulus = status_row[0] if status_row else None
        st.write("**Status Permohonan:**", status_lulus if status_lulus else "❌ Belum Lulus")

        # Butang kelulusan
        if st.button(f"✅ Luluskan SLI-01 untuk {nama}", key=pelajar_id):
            c.execute("""
                INSERT INTO status_permohonan (pelajar_id, status_lulus, tarikh_lulus)
                VALUES (?, ?, ?)
                ON CONFLICT(pelajar_id) DO UPDATE SET
                    status_lulus=excluded.status_lulus,
                    tarikh_lulus=excluded.tarikh_lulus
            """, (pelajar_id, "LULUS", date.today().isoformat()))
            conn.commit()
            st.success("Permohonan SLI-01 telah diluluskan.")

conn.close()
