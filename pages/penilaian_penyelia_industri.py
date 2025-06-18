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

# Maklumat pelajar
c.execute("SELECT nama, no_ic, kod_program, no_telefon, emel, alamat FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
pelajar_info = c.fetchone()

# Maklumat industri
c.execute("SELECT nama_pegawai, nama_syarikat, alamat1, alamat2, bandar, poskod, negeri, telefon_pegawai FROM maklumat_industri WHERE pelajar_id=?", (pelajar_id,))
industri_info = c.fetchone()

# Papar maklumat pelajar dan industri
st.subheader("👤 Maklumat Pelajar")
st.markdown(f"""
- **Nama:** {pelajar_info[0]}
- **No. Pelajar:** {pelajar_id}
- **Program:** {pelajar_info[2]}
- **No. IC:** {pelajar_info[1]}
- **Telefon:** {pelajar_info[3]}
- **Emel:** {pelajar_info[4]}
- **Alamat:** {pelajar_info[5]}
""")

st.subheader("🏢 Maklumat Organisasi")
st.markdown(f"""
- **Nama Penyelia Industri:** {industri_info[0]}
- **Nama Syarikat:** {industri_info[1]}
- **Alamat:** {industri_info[2]}, {industri_info[3]}, {industri_info[4]}, {industri_info[5]}, {industri_info[6]}
- **Telefon:** {industri_info[7]}
""")

# Soalan lengkap dari borang rasmi BLI-05
soalan_list = [
    ("Keupayaan mental (kecerdasan dan keupayaan am dalam menerima dan mendapatkan pengetahuan).", "q1"),
    ("Keupayaan fizikal (ketahanan menjalankan kerja di lapangan).", "q2"),
    ("Realiabiliti (tahap pencapaian kerja yang konsisten).", "q3"),
    ("Tanggungjawab (reaksi pelatih terhadap tanggungjawab yang diberikan kepadanya oleh pihak pengurusan).", "q4"),
    ("Kebolehan bergaul dan berkomunikasi dengan orang lain.", "q5"),
    ("Kerja berpasukan (kebolehan bekerja dalam kumpulan).", "q6"),
    ("Inisiatif (mempunyai keupayaan berdikari dan hanya memerlukan sedikit penyeliaan).", "q7"),
    ("Penyesuaian diri: Masa kerja, kerja lebih masa, kecemasan, ikut peraturan.", "q8"),
    ("Penilaian keseluruhan terhadap pelatih sebagai seorang pekerja.", "q9"),
]

markah_list = []
with st.form("penilaian_form"):
    st.subheader("📝 Borang Penilaian")
    for soalan, key in soalan_list:
        markah = st.radio(f"{soalan}", options=[1, 2, 3, 4, 5], horizontal=True, key=key)
        markah_list.append(markah)

    st.subheader("💬 Kelebihan / Kekurangan Pelajar")
    komen_kelebihan = st.text_area("Nyatakan kekuatan atau kelemahan pelajar", key="kelebihan")

    st.subheader("💭 Komen Lain")
    komen_lain = st.text_area("Komen tambahan jika ada", key="komen")

    keputusan = st.radio("🔎 Keputusan", options=["LULUS", "GAGAL", "TIDAK LENGKAP"], horizontal=True)

    submitted = st.form_submit_button("💾 Simpan Penilaian")

    if submitted:
        jumlah = sum(markah_list)
        markah_30 = round((jumlah / 60) * 30, 2)

        c.execute("""
            REPLACE INTO penilaian_penyelia_industri 
            (pelajar_id, penyelia_id, q1, q2, q3, q4, q5, q6, q7, q8, q9, jumlah, markah_30)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pelajar_id, penyelia_id, *markah_list, jumlah, markah_30))

        # Simpan kelebihan/komen/keputusan dalam table lain (jika ada)
        c.execute("""
            CREATE TABLE IF NOT EXISTS penilaian_lanjutan (
                pelajar_id TEXT PRIMARY KEY,
                kelebihan TEXT,
                komen TEXT,
                keputusan TEXT
            )
        """)
        c.execute("""
            REPLACE INTO penilaian_lanjutan (pelajar_id, kelebihan, komen, keputusan)
            VALUES (?, ?, ?, ?)
        """, (pelajar_id, komen_kelebihan, komen_lain, keputusan))

        conn.commit()
        st.success(f"✅ Penilaian berjaya disimpan. Jumlah Skor: {jumlah}/60, Markah (30%): {markah_30}, Keputusan: {keputusan}")

conn.close()
