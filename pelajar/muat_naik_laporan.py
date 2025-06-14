import streamlit as st
import os

UPLOAD_DIR = "uploads/laporan"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("Muat Naik Laporan Akhir LI")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk.")
else:
    laporan = st.file_uploader("Pilih Fail Laporan Akhir (PDF)", type=["pdf"])
    if laporan:
        path = os.path.join(UPLOAD_DIR, f"{st.session_state.user_id}_{laporan.name}")
        with open(path, "wb") as f:
            f.write(laporan.getbuffer())
        st.success("Laporan akhir berjaya dimuat naik.")
