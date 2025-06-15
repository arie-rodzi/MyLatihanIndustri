import streamlit as st

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

st.title("Cetak Borang Lapor Diri (BLI-04)")

("Cetak Borang Lapor Diri (BLI-04)")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk.")
else:
    d1, d2 = fetch_pelajar(st.session_state.user_id)
    if d1 and d2:
        if st.button("Jana Borang"):
            generate_borang(d1, d2)
            with open(GENERATED, "rb") as f:
                st.download_button("Muat Turun Borang", f, file_name="BLI-04_Lapor_Diri.docx")
    else:
        st.info("Maklumat belum lengkap.")