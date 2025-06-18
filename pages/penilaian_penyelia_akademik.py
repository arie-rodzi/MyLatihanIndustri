import streamlit as st
import sqlite3

st.set_page_config(page_title="Penilaian Penyelia Akademik", layout="wide")
st.title("📝 Penilaian Penyelia Akademik")

if st.session_state.get("user_role") != "penyelia_akademik":
    st.warning("Modul ini hanya untuk penyelia akademik.")
    st.stop()

penyelia_id = st.session_state.get("user_id", "")

conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Dapatkan pelajar diselia
c.execute("SELECT pelajar_id, nama FROM maklumat_pelajar WHERE penyelia_akademik_id=?", (penyelia_id,))
pelajar_list = c.fetchall()

if not pelajar_list:
    st.info("Tiada pelajar diselia oleh anda.")
    st.stop()

pelajar_dict = {f"{nama} ({pid})": pid for pid, nama in pelajar_list}
selected_pelajar = st.selectbox("📌 Pilih Pelajar", options=list(pelajar_dict.keys()))
pelajar_id = pelajar_dict[selected_pelajar]

# Dapatkan maklumat pelajar
c.execute("SELECT * FROM maklumat_pelajar WHERE pelajar_id=?", (pelajar_id,))
pelajar_row = c.fetchone()
kolum = [col[1] for col in c.execute("PRAGMA table_info(maklumat_pelajar);")]
pelajar_data = dict(zip(kolum, pelajar_row)) if pelajar_row else {}

st.markdown("### 🧑‍🎓 BUTIRAN PELAJAR")
st.text(f"Nama: {pelajar_data.get('nama', '-')}")
st.text(f"No. Pelajar: {pelajar_data.get('pelajar_id', '-')}")
st.text(f"Program: {pelajar_data.get('kod_program', '-')}")
st.text(f"No. Telefon: {pelajar_data.get('no_telefon', '-')}")

st.markdown("### 🏢 BUTIRAN ORGANISASI")
st.text(f"Nama Penyelia Industri: {pelajar_data.get('penyelia_industri_id', '-')}")
st.text(f"Alamat: {pelajar_data.get('alamat', '-')}")
st.text(f"No. Telefon Pejabat/HP: {pelajar_data.get('no_telefon', '-')}")

st.markdown("### 👨‍🏫 BUTIRAN PENYELIA AKADEMIK")
st.text(f"Nama Pensyarah: {penyelia_id}")

# Senarai soalan
soalan_clo1 = [
    "Pengenalan latihan industri",
    "Latar belakang organisasi dan tugasan",
    "Laporan aktiviti organisasi dan jabatan",
    "Tugasan/projek pelajar",
    "Keberkesanan tugasan kepada organisasi/komuniti",
    "Kaedah kerja yang digunapakai"
]

soalan_clo5 = [
    "Kekemasan catatan dalam buku log",
    "Keupayaan menterjemah tugasan",
    "Penulisan dan tatabahasa",
    "Kandungan keseluruhan buku log",
    "Disemak oleh penyelia industri"
]

soalan_clo4 = [
    "Maklumat bergambar/carta/lukisan",
    "Kelebihan tugasan semasa LI",
    "Kesimpulan dan cadangan penambahbaikan",
    "Persembahan laporan",
    "Kekemasan format laporan"
]

# Input markah
st.subheader("📚 Penilaian Laporan Akhir (30%) - CLO1")
markah_clo1 = [st.radio(f"{i+1}. {s}", [1, 2, 3, 4, 5], horizontal=True, key=f"clo1_{i}") for i, s in enumerate(soalan_clo1)]

st.subheader("📘 Penilaian Buku Log (10%) - CLO5")
markah_clo5 = [st.radio(f"{i+1}. {s}", [1, 2], horizontal=True, key=f"clo5_{i}") for i, s in enumerate(soalan_clo5)]

st.subheader("📖 Penilaian Laporan Akhir (30%) - CLO4")
markah_clo4 = [st.radio(f"{i+1}. {s}", [1, 2], horizontal=True, key=f"clo4_{i}") for i, s in enumerate(soalan_clo4)]

# Auto-kira markah
total_clo1 = sum(markah_clo1)
total_clo5 = sum(markah_clo5)
total_clo4 = sum(markah_clo4)

markah_30 = round((total_clo1 / 30) * 30, 2)
markah_10 = round((total_clo5 / 10) * 10, 2)
markah_30b = round((total_clo4 / 10) * 30, 2)
markah_total = markah_30 + markah_10 + markah_30b

# Papar markah semasa
st.markdown("### 📊 Markah Semasa")
st.info(f"""
- CLO1 (30%): {markah_30}
- CLO5 (10%): {markah_10}
- CLO4 (30%): {markah_30b}
- **Jumlah Keseluruhan: {markah_total} / 70**
""")

# Butang simpan
if st.button("💾 Simpan Penilaian"):
    c.execute("""
        CREATE TABLE IF NOT EXISTS penilaian_penyelia_akademik (
            pelajar_id TEXT PRIMARY KEY,
            penyelia_id TEXT,
            clo1_q1 INTEGER, clo1_q2 INTEGER, clo1_q3 INTEGER, clo1_q4 INTEGER, clo1_q5 INTEGER, clo1_q6 INTEGER,
            clo5_q1 INTEGER, clo5_q2 INTEGER, clo5_q3 INTEGER, clo5_q4 INTEGER, clo5_q5 INTEGER,
            clo4_q1 INTEGER, clo4_q2 INTEGER, clo4_q3 INTEGER, clo4_q4 INTEGER, clo4_q5 INTEGER,
            markah_clo1 REAL, markah_clo5 REAL, markah_clo4 REAL, markah_total REAL
        )
    """)

    c.execute("""
        REPLACE INTO penilaian_penyelia_akademik VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?
        )
    """, (
        pelajar_id, penyelia_id, *markah_clo1,
        *markah_clo5, *markah_clo4,
        markah_30, markah_10, markah_30b, markah_total
    ))
    conn.commit()
    st.success("✅ Penilaian berjaya disimpan.")

conn.close()
