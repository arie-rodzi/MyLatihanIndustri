
import streamlit as st
import sqlite3

st.set_page_config(page_title="Penilaian Industri", layout="wide")
st.title("📋 Penilaian Pelajar oleh Penyelia Industri")

if st.session_state.get("user_role") != "penyelia_industri":
    st.warning("Modul ini hanya untuk penyelia industri.")
    st.stop()

penyelia_id = st.session_state.get("user_id", "")

conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Dapatkan pelajar yang diselia
c.execute("SELECT pelajar_id, nama FROM maklumat_pelajar WHERE penyelia_industri_id=?", (penyelia_id,))
pelajar_list = c.fetchall()

if not pelajar_list:
    st.info("Tiada pelajar diselia oleh anda.")
    st.stop()

pelajar_dict = {f"{nama} ({pid})": pid for pid, nama in pelajar_list}
selected_pelajar = st.selectbox("Pilih Pelajar", options=list(pelajar_dict.keys()))
pelajar_id = pelajar_dict[selected_pelajar]

# Soalan penilaian
soalan_list = [
    "1. Keupayaan mental",
    "2. Keupayaan fizikal",
    "3. Realiabiliti",
    "4. Tanggungjawab",
    "5. Kebolehan bergaul dan berkomunikasi",
    "6. Kerja berpasukan",
    "7. Inisiatif",
    "8. Penyesuaian diri dengan keadaan kerja",
    "9. Penilaian keseluruhan"
]

markah_list = []
with st.form("penilaian_form"):
    st.subheader("📝 Borang Penilaian")
    for i, soalan in enumerate(soalan_list):
        markah = st.radio(soalan, options=[1, 2, 3, 4, 5], horizontal=True, key=f"q{i+1}")
        markah_list.append(markah)

    submitted = st.form_submit_button("💾 Simpan Penilaian")

    if submitted:
        jumlah = sum(markah_list)
        markah_30 = round((jumlah / 60) * 30, 2)

        c.execute("""
            REPLACE INTO penilaian_penyelia_industri 
            (pelajar_id, penyelia_id, q1, q2, q3, q4, q5, q6, q7, q8, q9, jumlah, markah_30)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pelajar_id, penyelia_id, *markah_list, jumlah, markah_30))
        conn.commit()
        st.success(f"Penilaian berjaya disimpan. Jumlah: {jumlah}, Markah (30%): {markah_30}")
