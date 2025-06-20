import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Logbook Mingguan", layout="wide")
st.title("📘 Logbook Mingguan Pelajar")

if st.session_state.get("user_role") != "pelajar":
    st.warning("Modul ini hanya untuk pelajar.")
    st.stop()

pelajar_id = st.session_state.get("user_id", "")

# Sambung ke database
conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Input borang logbook mingguan
with st.form("logbook_form"):
    minggu = st.number_input("Minggu", min_value=1, max_value=20, step=1)
    aktiviti = st.text_area("Catat Aktiviti Mingguan Anda", height=150)
    submitted = st.form_submit_button("Simpan Logbook")
    if submitted:
        # Semak jika minggu tersebut sudah wujud untuk pelajar
        c.execute("SELECT 1 FROM logbook WHERE pelajar_id=? AND minggu=?", (pelajar_id, minggu))
        if c.fetchone():
            c.execute("""
                UPDATE logbook
                SET aktiviti = ?
                WHERE pelajar_id = ? AND minggu = ?
            """, (aktiviti, pelajar_id, minggu))
        else:
            c.execute("""
                INSERT INTO logbook (pelajar_id, minggu, aktiviti)
                VALUES (?, ?, ?)
            """, (pelajar_id, minggu, aktiviti))
        conn.commit()
        st.success(f"Logbook minggu ke-{minggu} telah disimpan.")

# Papar semua logbook pelajar termasuk status pengesahan
st.markdown("---")
st.subheader("📖 Paparan Semua Logbook")

c.execute("""
    SELECT minggu, aktiviti, disahkan_oleh_industri, disahkan_oleh_akademik
    FROM logbook
    WHERE pelajar_id = ?
    ORDER BY minggu
""", (pelajar_id,))
rows = c.fetchall()

df = pd.DataFrame(rows, columns=[
    "minggu", "aktiviti", "disahkan_oleh_industri", "disahkan_oleh_akademik"
])

if not df.empty:
    df["minggu"] = df["minggu"].astype(int)
    df = df.rename(columns={
        "minggu": "Minggu",
        "aktiviti": "Aktiviti",
        "disahkan_oleh_industri": "Pengesahan Penyelia Industri",
        "disahkan_oleh_akademik": "Pengesahan Penyelia Akademik"
    })
    st.dataframe(df, use_container_width=True)
else:
    st.info("Tiada logbook dimasukkan setakat ini.")
