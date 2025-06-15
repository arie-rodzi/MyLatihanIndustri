import streamlit as st

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

st.title("Muat Naik Borang BLI-02")

("Muat Naik Borang BLI-02 & Maklumat Penempatan")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk sebagai pelajar terlebih dahulu.")
else:
    init_penempatan_table()
    pelajar_id = st.session_state.user_id
    nama_syarikat = st.text_input("Nama Syarikat")
    alamat = st.text_area("Alamat Syarikat")
    pegawai = st.text_input("Nama Pegawai Penilai")
    emel = st.text_input("Emel Pegawai")
    no_tel = st.text_input("No. Telefon Pegawai")
    tarikh_mula = st.date_input("Tarikh Mula LI")
    tarikh_tamat = st.date_input("Tarikh Tamat LI")
    bli02 = st.file_uploader("Muat Naik Borang BLI-02", type=["pdf", "docx"])

    if st.button("Hantar BLI-02"):
        if bli02:
            fail_path = os.path.join(UPLOAD_DIR, f"{pelajar_id}_{bli02.name}")
            with open(fail_path, "wb") as f:
                f.write(bli02.getbuffer())
            simpan_penempatan((pelajar_id, nama_syarikat, alamat, pegawai, emel, no_tel,
                               tarikh_mula.isoformat(), tarikh_tamat.isoformat(), fail_path))
            st.success("Borang BLI-02 dan maklumat penempatan berjaya dihantar.")
        else:
            st.warning("Sila muat naik fail BLI-02.")