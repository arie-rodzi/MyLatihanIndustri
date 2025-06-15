import streamlit as st

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

st.title("Logbook Mingguan")

("Logbook Mingguan (16 Minggu)")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk.")
else:
    init_logbook()
    pelajar_id = st.session_state.user_id
    minggu = st.selectbox("Minggu ke-", list(range(1, 17)))
    aktiviti = st.text_area("Catatan Aktiviti Mingguan")
    if st.button("Simpan Log"):
        simpan_log(pelajar_id, minggu, aktiviti)
        st.success(f"Log Minggu {minggu} disimpan.")
