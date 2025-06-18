import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Kelulusan SLI-01", layout="wide")
st.title("📄 Kelulusan Surat Permohonan Latihan Industri (SLI-01)")

# Pastikan login sebagai penyelaras
if "user_role" not in st.session_state or st.session_state["user_role"] != "penyelaras":
    st.warning("Modul ini hanya untuk penyelaras.")
    st.stop()

# Sambung ke database
conn = sqlite3.connect("database/latihan_industri.final.db")
c = conn.cursor()

# Cipta jadual jika belum wujud
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

# Ambil semua pelajar
c.execute("SELECT pelajar_id, nama FROM maklumat_pelajar")
pelajar_list = c.fetchall()

for pelajar_id, nama in pelajar_list:
    with st.expander(f"{nama} ({pelajar_id})", expanded=False):
        # Ambil maklumat pelajar
        c.execute("SELECT ic, program, no_telefon, email, alamat FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
        ic, program, no_telefon, email, alamat = c.fetchone()

        st.markdown(f"""
        **Maklumat Pelajar:**
        - **IC:** {ic}
        - **Program:** {program}
        - **Telefon:** {no_telefon}
        - **Email:** {email}
        - **Alamat:** {alamat}
        """)

        # Semak status permohonan terkini
        c.execute("SELECT status_lulus, tarikh_lulus FROM status_permohonan WHERE pelajar_id=?", (pelajar_id,))
        row = c.fetchone()
        if row:
            status_lulus, tarikh_lulus = row
            if status_lulus == "LULUS":
                st.success(f"✅ LULUS pada {tarikh_lulus}")
            else:
                st.info("❌ BELUM LULUS")
        else:
            st.info("❌ BELUM LULUS")

        # Butang lulus
        if st.button(f"✅ Luluskan SLI-01 untuk {nama}", key=f"lulus_{pelajar_id}"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format 24-jam
            c.execute("SELECT 1 FROM status_permohonan WHERE pelajar_id=?", (pelajar_id,))
            if c.fetchone():
                c.execute("""
                    UPDATE status_permohonan
                    SET status_lulus = ?, tarikh_lulus = ?
                    WHERE pelajar_id = ?
                """, ("LULUS", current_time, pelajar_id))
            else:
                c.execute("""
                    INSERT INTO status_permohonan (pelajar_id, status_lulus, tarikh_lulus)
                    VALUES (?, ?, ?)
                """, (pelajar_id, "LULUS", current_time))
            conn.commit()
            st.success(f"✅ Permohonan telah diluluskan pada {current_time}")
            st.rerun()

conn.close()
