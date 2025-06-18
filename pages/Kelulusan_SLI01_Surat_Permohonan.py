import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="Debug Kelulusan SLI-01", layout="wide")
st.title("🛠️ Debug: Kelulusan Surat Permohonan SLI-01")

if "user_role" not in st.session_state or st.session_state["user_role"] != "penyelaras":
    st.warning("Modul ini hanya untuk penyelaras.")
    st.stop()

conn = sqlite3.connect("database/latihan_industri.final.db")
c = conn.cursor()

# Debug: pastikan jadual wujud
c.execute("PRAGMA table_info(status_permohonan)")
st.write("Struktur jadual status_permohonan:", c.fetchall())

# Debug: semak semua pelajar
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

        c.execute("SELECT status_lulus FROM status_permohonan WHERE pelajar_id=?", (pelajar_id,))
        row = c.fetchone()
        status_lulus = row[0] if row else None
        st.write("Status Lulus:", status_lulus if status_lulus else "❌")

        if st.button(f"✅ Luluskan SLI-01 untuk {nama}", key=pelajar_id):
            try:
                c.execute("""
                    INSERT INTO status_permohonan (pelajar_id, status_lulus, tarikh_lulus)
                    VALUES (?, ?, ?)
                    ON CONFLICT(pelajar_id) DO UPDATE SET
                        status_lulus=excluded.status_lulus,
                        tarikh_lulus=excluded.tarikh_lulus
                """, (pelajar_id, "LULUS", date.today().isoformat()))
                conn.commit()
                st.success("Berjaya diluluskan.")
                st.rerun()
            except Exception as e:
                st.error(f"Gagal luluskan: {e}")

conn.close()
