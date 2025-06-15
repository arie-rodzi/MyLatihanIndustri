import streamlit as st

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

st.title("Muat Naik Laporan Akhir")

("Muat Naik Laporan Akhir LI")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk.")
else:
    laporan = st.file_uploader("Pilih Fail Laporan Akhir (PDF)", type=["pdf"])
    if laporan:
        path = os.path.join(UPLOAD_DIR, f"{st.session_state.user_id}_{laporan.name}")
        with open(path, "wb") as f:
            f.write(laporan.getbuffer())
        st.success("Laporan akhir berjaya dimuat naik.")
