import streamlit as st

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

st.title("Cetak Borang Permohonan (BLI-02)")

("Cetak Borang Permohonan (SLI01/DLI01/BLI02)")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk terlebih dahulu.")
else:
    pelajar, penempatan = fetch_data(st.session_state.user_id)
    if pelajar and penempatan:
        if st.button("Jana Borang Permohonan"):
            generate_form(pelajar, penempatan)
            with open(GENERATED, "rb") as f:
                st.download_button("Muat Turun Borang", f, file_name="Borang_Permohonan_LI.docx")
    else:
        st.info("Maklumat pelajar atau penempatan belum lengkap.")