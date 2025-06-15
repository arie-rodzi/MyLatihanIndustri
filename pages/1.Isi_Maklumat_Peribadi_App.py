# Versi penuh Isi_Maklumat_Peribadi_App.py dengan semakan role dan borang
isi_maklumat_peribadi_app_code = '''
import streamlit as st
import sqlite3

st.set_page_config(page_title="Isi Maklumat Peribadi", layout="wide")
st.title("📋 Isi Maklumat Peribadi")

# Semakan login
if "user_role" not in st.session_state or st.session_state["user_role"] != "pelajar":
    st.warning("Sila log masuk sebagai pelajar terlebih dahulu.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Cipta jadual jika belum wujud
c.execute(\"""
    CREATE TABLE IF NOT EXISTS maklumat_pelajar (
        pelajar_id TEXT PRIMARY KEY,
        nama TEXT,
        ic TEXT,
        program TEXT,
        no_telefon TEXT,
        email TEXT,
        alamat TEXT
    )
\""")
conn.commit()

# Semak sama ada data sudah wujud
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
        program = st.text_input("Program")
        no_telefon = st.text_input("No Telefon")
        email = st.text_input("Email")
        alamat = st.text_area("Alamat Surat-Menyurat")
        submit = st.form_submit_button("Hantar")

        if submit:
            if not nama or not ic or not program:
                st.error("Sila lengkapkan semua maklumat wajib.")
            else:
                c.execute("INSERT INTO maklumat_pelajar VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (pelajar_id, nama, ic, program, no_telefon, email, alamat))
                conn.commit()
                st.success("Maklumat berjaya dihantar.")
                st.experimental_rerun()
'''

# Simpan sebagai fail siap pakai
final_path = "/mnt/data/Isi_Maklumat_Peribadi_App.py"
with open(final_path, "w") as f:
    f.write(isi_maklumat_peribadi_app_code)

final_path

