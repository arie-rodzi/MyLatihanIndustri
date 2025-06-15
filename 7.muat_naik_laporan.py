
import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="Muat Naik Laporan", layout="wide")
st.title("📤 Muat Naik Laporan Akhir Latihan Industri")

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")

upload_dir = "uploaded_reports"
os.makedirs(upload_dir, exist_ok=True)

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS laporan (pelajar_id TEXT PRIMARY KEY, nama_fail TEXT, tarikh_upload TEXT)")
conn.commit()

uploaded_file = st.file_uploader("Sila muat naik laporan akhir anda (PDF sahaja)", type=["pdf"])
if uploaded_file is not None:
    save_path = os.path.join(upload_dir, f"{pelajar_id}_laporan.pdf")
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    from datetime import datetime
    tarikh_upload = datetime.today().strftime("%Y-%m-%d")
    c.execute("REPLACE INTO laporan (pelajar_id, nama_fail, tarikh_upload) VALUES (?, ?, ?)",
              (pelajar_id, uploaded_file.name, tarikh_upload))
    conn.commit()
    st.success(f"Laporan '{uploaded_file.name}' telah dimuat naik pada {tarikh_upload}.")

# Paparan status
st.markdown("---")
st.subheader("📄 Status Laporan Terkini")
c.execute("SELECT nama_fail, tarikh_upload FROM laporan WHERE pelajar_id=?", (pelajar_id,))
row = c.fetchone()
if row:
    st.info(f"Laporan '{row[0]}' telah dimuat naik pada {row[1]}.")
else:
    st.warning("Tiada laporan dimuat naik lagi.")
