import streamlit as st

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

st.title("Cetak Surat Penempatan (SLI-03)")

("Cetak Surat Penempatan (SLI-03)")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk.")
else:
    data = fetch_penempatan(st.session_state.user_id)
    if data:
        if st.button("Jana Surat"):
            generate_surat(data)
            with open(GENERATED, "rb") as f:
                st.download_button("Muat Turun Surat", f, file_name="SLI-03_Surat_Penempatan.docx")
    else:
        st.info("Maklumat penempatan belum lengkap.")
