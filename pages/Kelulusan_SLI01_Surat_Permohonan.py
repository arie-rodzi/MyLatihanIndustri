import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="Kelulusan SLI-01", layout="wide")
st.title("📄 Kelulusan Surat Permohonan Latihan Industri (SLI-01)")

# Lindungi ralat jika 'user_role' belum wujud
if "user_role" not in st.session_state or st.session_state.get("user_role") != "penyalaras":
    st.warning("Modul ini hanya untuk penyelaras.")
    st.stop()

# Sambungan ke pangkalan data
conn = sqlite3.connect("database/latihan_industri.db")  # ubah jika fail db lain
c = conn.cursor()

# Pastikan jadual berkaitan wujud
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

# Papar senarai pelajar dan status kelulusan
c.execute("""
    SELECT p.pelajar_id, p.nama, s.status_lulus 
    FROM maklumat_pelajar p 
    LEFT JOIN status_permohonan s ON p.pelajar_id = s.pelajar_id
""")
pelajar_list = c.fetchall()

for pelajar_id, nama, status_lulus in pelajar_list:
    with st.expander(f"{nama} ({pelajar_id})"):
        st.write("Status permohonan:", status_lulus if status_lulus else "❌ Belum Lulus")
        if st.button(f"✅ Luluskan SLI-01 untuk {nama}", key=pelajar_id):
            c.execute("""
                INSERT OR REPLACE INTO status_permohonan 
                (pelajar_id, status_lulus, tarikh_lulus)
                VALUES (?, ?, ?)
            """, (pelajar_id, "LULUS", date.today().isoformat()))
            conn.commit()
            st.success("Permohonan SLI-01 telah diluluskan.")

conn.close()
