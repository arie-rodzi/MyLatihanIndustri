import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="Kelulusan SLI-01", layout="wide")
st.title("📄 Kelulusan Surat Permohonan Latihan Industri (SLI-01)")

if "user_role" not in st.session_state or st.session_state["user_role"] != "penyelaras":
    st.warning("Modul ini hanya untuk penyelaras.")
    st.stop()

conn = sqlite3.connect("database/latihan_industri.final.db")
c = conn.cursor()

c.execute("SELECT pelajar_id, nama, status_lulus FROM maklumat_pelajar LEFT JOIN status_permohonan USING(pelajar_id)")
pelajar_list = c.fetchall()

for pelajar_id, nama, status_lulus in pelajar_list:
    with st.expander(f"{nama} ({pelajar_id})"):
        # Papar maklumat lengkap pelajar
        c.execute("SELECT ic, program, no_telefon, email, alamat FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
        maklumat = c.fetchone()
        if maklumat:
            ic, program, no_telefon, email, alamat = maklumat
            st.markdown(f"""
            - **No IC:** {ic}
            - **Program:** {program}
            - **No Telefon:** {no_telefon}
            - **Email:** {email}
            - **Alamat:** {alamat}
            """)
        st.write("Status permohonan:", status_lulus if status_lulus else "❌ Belum Lulus")

        if st.button(f"✅ Luluskan SLI-01 untuk {nama}", key=pelajar_id):
            c.execute("""INSERT OR REPLACE INTO status_permohonan 
                         (pelajar_id, status_lulus, tarikh_lulus) 
                         VALUES (?, ?, ?)""", (pelajar_id, "LULUS", date.today().isoformat()))
            conn.commit()
            st.success("Permohonan SLI-01 telah diluluskan.")

conn.close()
