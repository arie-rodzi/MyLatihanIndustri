import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="Debug Kelulusan SLI-01", layout="wide")
st.title("🐞 Debug: Kelulusan SLI-01")

# Pastikan login sebagai penyelaras
if "user_role" not in st.session_state or st.session_state["user_role"] != "penyelaras":
    st.warning("Modul ini hanya untuk penyelaras.")
    st.stop()

# Sambung ke DB
conn = sqlite3.connect("database/latihan_industri.final.db")
c = conn.cursor()

# Pastikan jadual wujud
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

# Ambil pelajar
c.execute("SELECT pelajar_id, nama FROM maklumat_pelajar")
pelajar_list = c.fetchall()

for pelajar_id, nama in pelajar_list:
    with st.expander(f"{nama} ({pelajar_id})"):
        c.execute("SELECT ic, program, no_telefon, email, alamat FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
        ic, program, no_telefon, email, alamat = c.fetchone()

        st.markdown(f"""
        - **IC:** {ic}
        - **Program:** {program}
        - **Email:** {email}
        """)

        # Semak status lulus
        c.execute("SELECT status_lulus FROM status_permohonan WHERE pelajar_id=?", (pelajar_id,))
        row = c.fetchone()
        status_lulus = row[0] if row else None
        st.info(f"Status Lulus Semasa: {status_lulus if status_lulus else '❌ BELUM'}")

        # Debug button
        if st.button(f"✅ Klik untuk LULUSKAN {nama}", key=pelajar_id):
            try:
                c.execute("SELECT 1 FROM status_permohonan WHERE pelajar_id = ?", (pelajar_id,))
                exists = c.fetchone()
                if exists:
                    st.write("➡️ Kemaskini status...")
                    c.execute("""
                        UPDATE status_permohonan
                        SET status_lulus = ?, tarikh_lulus = ?
                        WHERE pelajar_id = ?
                    """, ("LULUS", date.today().isoformat(), pelajar_id))
                else:
                    st.write("➡️ Masukkan rekod baru...")
                    c.execute("""
                        INSERT INTO status_permohonan (pelajar_id, status_lulus, tarikh_lulus)
                        VALUES (?, ?, ?)
                    """, (pelajar_id, "LULUS", date.today().isoformat()))
                conn.commit()
                st.success("✅ Berjaya diluluskan.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Ralat berlaku: {e}")

conn.close()
