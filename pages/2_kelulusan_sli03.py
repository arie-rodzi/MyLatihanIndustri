import streamlit as st
import sqlite3
from datetime import datetime
import pytz
import os

st.set_page_config(page_title="Kelulusan SLI-03", layout="wide")
st.title("📄 Kelulusan Surat Penempatan Latihan Industri (SLI-03)")

# Semakan peranan
if "user_role" not in st.session_state or st.session_state["user_role"] != "penyelaras":
    st.warning("Modul ini hanya untuk penyelaras.")
    st.stop()

# Sambung ke pangkalan data
conn = sqlite3.connect("database/latihan_industri.final.db")
c = conn.cursor()

upload_dir = "uploaded/bli02"
os.makedirs(upload_dir, exist_ok=True)

# Cipta fail dummy jika belum wujud
dummy_file_path = os.path.join(upload_dir, "dummy_bli02.pdf")
if not os.path.exists(dummy_file_path):
    with open(dummy_file_path, "wb") as f:
        f.write(b"%PDF-1.4\n% Dummy BLI-02 file\n")

# Pastikan jadual status_permohonan wujud
c.execute("""
    CREATE TABLE IF NOT EXISTS status_permohonan (
        pelajar_id TEXT PRIMARY KEY,
        status_lulus TEXT,
        tarikh_lulus TEXT,
        status_sli03 TEXT,
        status_bli02 TEXT
    )
""")
conn.commit()

# Tambah kolum tarikh_sli03 jika belum wujud
try:
    c.execute("ALTER TABLE status_permohonan ADD COLUMN tarikh_sli03 TEXT")
except sqlite3.OperationalError:
    pass

# Ambil senarai pelajar
c.execute("SELECT pelajar_id, nama FROM maklumat_pelajar")
pelajar_list = c.fetchall()

for pelajar_id, nama in pelajar_list:
    with st.expander(f"{nama} ({pelajar_id})", expanded=False):
        # Semak status kelulusan SLI-01
        c.execute("SELECT status_lulus, status_sli03, tarikh_sli03 FROM status_permohonan WHERE pelajar_id=?", (pelajar_id,))
        permohonan = c.fetchone()
        if not permohonan or permohonan[0] != "LULUS":
            st.warning("❌ SLI-01 belum diluluskan.")
            continue

        # Semak maklumat industri
        c.execute("SELECT * FROM maklumat_industri WHERE pelajar_id=?", (pelajar_id,))
        industry = c.fetchone()
        if not industry:
            st.warning("❌ Maklumat BLI-02 belum dihantar oleh pelajar.")
            continue

        # Isikan fail dummy jika fail_bli02 masih kosong
        if len(industry) > 8 and not industry[8]:
            c.execute("UPDATE maklumat_industri SET fail_bli02 = ? WHERE pelajar_id = ?", ("dummy_bli02.pdf", pelajar_id))
            conn.commit()
            industry = list(industry)
            industry[8] = "dummy_bli02.pdf"

        # Papar maklumat syarikat
        st.markdown("### 🏢 Maklumat Syarikat")
        st.write(f"**Nama Syarikat:** {industry[1]}")
        st.write(f"**Alamat:** {industry[2]}")
        st.write(f"**Nama Pegawai:** {industry[3]}")
        st.write(f"**Emel Pegawai:** {industry[4]}")
        st.write(f"**Telefon Pegawai:** {industry[5]}")
        st.write(f"**Tarikh Mula:** {industry[6]}")
        st.write(f"**Tarikh Tamat:** {industry[7]}")

        # Lampirkan fail
        if len(industry) > 8 and industry[8]:
            file_path = os.path.join(upload_dir, industry[8])
            if os.path.exists(file_path):
                st.markdown(f"[📄 Muat Turun BLI-02]({file_path})")
            else:
                st.warning("❌ Fail BLI-02 tidak dijumpai.")
        else:
            st.warning("❌ Fail BLI-02 belum dimuat naik.")

        # Status SLI-03
        status_sli03 = permohonan[1]
        tarikh_sli03 = permohonan[2]
        if status_sli03 == "LULUS":
            st.success(f"✅ SLI-03 telah diluluskan pada {tarikh_sli03}")
        else:
            st.info("❌ SLI-03 belum diluluskan")

        # Butang lulus
        if st.button(f"✅ Luluskan SLI-03 untuk {nama}", key=f"sli03_{pelajar_id}"):
            now_malaysia = datetime.now(pytz.timezone("Asia/Kuala_Lumpur")).strftime("%Y-%m-%d %H:%M:%S")
            c.execute("UPDATE status_permohonan SET status_sli03 = ?, tarikh_sli03 = ? WHERE pelajar_id = ?",
                      ("LULUS", now_malaysia, pelajar_id))
            conn.commit()
            st.success(f"✅ SLI-03 telah diluluskan pada {now_malaysia}")
            st.rerun()

conn.close()
