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

# Pastikan jadual wujud
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
    pass  # Kolum mungkin sudah wujud

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

        # Semak maklumat BLI-02
        c.execute("SELECT * FROM maklumat_industri WHERE pelajar_id=?", (pelajar_id,))
        industry = c.fetchone()
        if not industry:
            st.warning("❌ Maklumat BLI-02 belum dihantar oleh pelajar.")
            continue

        # Papar maklumat syarikat
        st.markdown("### 🏢 Maklumat Syarikat")
        st.write(f"**Nama Syarikat:** {industry[1]}")
        st.write(f"**Alamat:** {industry[2]}")
        st.write(f"**Nama Pegawai:** {industry[3]}")
        st.write(f"**Emel Pegawai:** {industry[4]}")
        st.write(f"**Telefon Pegawai:** {industry[5]}")
        st.write(f"**Tarikh Mula:** {industry[6]}")
        st.write(f"**Tarikh Tamat:** {industry[7]}")

        # Lampirkan fail BLI-02 jika wujud
        file_path = os.path.join(upload_dir, industry[8])
        if os.path.exists(file_path):
            st.markdown(f"[📄 Muat Turun BLI-02]({file_path})")

        # Status SLI-03 semasa
        status_sli03 = permohonan[1]
        tarikh_sli03 = permohonan[2]
        if status_sli03 == "LULUS":
            st.success(f"✅ SLI-03 telah diluluskan pada {tarikh_sli03}")
        else:
            st.info("❌ SLI-03 belum diluluskan")

        # Butang untuk meluluskan
        if st.button(f"✅ Luluskan SLI-03 untuk {nama}", key=f"sli03_{pelajar_id}"):
            tz = pytz.timezone("Asia/Kuala_Lumpur")
            now_malaysia = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            c.execute("UPDATE status_permohonan SET status_sli03 = ?, tarikh_sli03 = ? WHERE pelajar_id = ?",
                      ("LULUS", now_malaysia, pelajar_id))
            conn.commit()
            st.success(f"✅ SLI-03 telah diluluskan pada {now_malaysia}")
            st.rerun()

conn.close()
