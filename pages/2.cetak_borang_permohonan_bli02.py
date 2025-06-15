import streamlit as st

# Pastikan hanya pelajar boleh akses
if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

# Tajuk modul
st.set_page_config(page_title="Modul 2: Cetak Borang Permohonan", layout="wide")
st.title("📄 Modul 2: Cetak Borang Permohonan Latihan Industri")

st.write("Sila semak maklumat anda sebelum mencetak borang.")

# (Opsyenal) Butang untuk cetak borang sebagai PDF atau paparkan butang muat turun
if st.button("Cetak Borang Permohonan"):
    st.success("Borang permohonan telah dijana.")
    st.download_button("Muat Turun Borang (PDF)", data="(isi nanti dengan fail PDF)", file_name="borang_permohonan.pdf")
