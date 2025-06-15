import streamlit as st
import sqlite3
import os

# Pastikan folder database wujud
os.makedirs("database", exist_ok=True)

st.set_page_config(page_title="Isi Maklumat Peribadi", layout="wide")
st.title("📋 Isi Maklumat Peribadi")

# Semakan login
if "user_role" not in st.session_state or st.session_state["user_role"] != "pelajar":
    st.warning("Sila log masuk sebagai pelajar terlebih dahulu.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")

# Sambung ke database
conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Cipta jadual jika belum wujud
c.execute("""
    CREATE TABLE IF NOT EXISTS maklumat_pelajar (
        pelajar_id TEXT PRIMARY KEY,
        nama TEXT,
        ic TEXT,
        program TEXT,
        no_telefon TEXT,
        email TEXT,
        alamat TEXT
    )
""")
conn.commit()

# Semak sama ada data pelajar sudah wujud
c.execute("SELECT * FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
existing = c.fetchone()

if existing:
    st.success("Maklumat telah dihantar.")
    st.write("### Maklumat Tersimpan")
    st.write(f"**Nama:** {existing[1]}")
    st.write(f"**No IC:** {existing[2]}")
    st.write(f"**Program:** {existing[3]}")
    st.write(f"**No Telefon:** {existing[4]}")
    st.write(f"**Email:** {existing[5]}")
    st.write(f"**Alamat:** {existing[6]}")
else:
    with st.form("borang_maklumat"):
        nama = st.text_input("Nama Penuh")
        ic = st.text_input("No Kad Pengenalan")
        program = st.selectbox("Program", ["CS241", "CS248", "CS249", "CS290"])
        no_telefon = st.text_input("No Telefon")
        email = st.text_input("Email")
        alamat = st.text_area("Alamat Surat-Menyurat")
        submit = st.form_submit_button("Hantar")

        if submit:
            if not nama or not ic:
                st.error("Sila lengkapkan semua maklumat wajib.")
            else:
                c.execute("INSERT INTO maklumat_pelajar VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (pelajar_id, nama, ic, program, no_telefon, email, alamat))
                conn.commit()
                st.success("Maklumat berjaya dihantar.")
                st.experimental_rerun()
