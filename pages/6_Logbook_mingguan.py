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

# Cipta jadual jika belum wujud
c.execute("""
    CREATE TABLE IF NOT EXISTS logbook (
        pelajar_id TEXT,
        minggu INTEGER,
        aktiviti TEXT,
        tarikh_submit TEXT,
        sah_industri TEXT DEFAULT 'Belum',
        sah_akademik TEXT DEFAULT 'Belum'
    )
""")
conn.commit()

# Tambah kolum jika belum ada (untuk kes backward compatibility)
try:
    c.execute("ALTER TABLE logbook ADD COLUMN sah_industri TEXT DEFAULT 'Belum'")
except sqlite3.OperationalError:
    pass

try:
    c.execute("ALTER TABLE logbook ADD COLUMN sah_akademik TEXT DEFAULT 'Belum'")
except sqlite3.OperationalError:
    pass

conn.commit()

# Input borang logbook mingguan
with st.form("logbook_form"):
    minggu = st.number_input("Minggu", min_value=1, max_value=20, step=1)
    aktiviti = st.text_area("Catat Aktiviti Mingguan Anda", height=150)
    submitted = st.form_submit_button("Simpan Logbook")
    if submitted:
        tarikh_submit = datetime.today().strftime("%Y-%m-%d")
        
        # FIX ERROR: Gantikan REPLACE dengan semakan manual (tanpa ubah struktur)
        c.execute("SELECT 1 FROM logbook WHERE pelajar_id=? AND minggu=?", (pelajar_id, minggu))
        if c.fetchone():
            c.execute("""
                UPDATE logbook
                SET aktiviti = ?, tarikh_submit = ?
                WHERE pelajar_id = ? AND minggu = ?
            """, (aktiviti, tarikh_submit, pelajar_id, minggu))
        else:
            c.execute("""
                INSERT INTO logbook (pelajar_id, minggu, aktiviti, tarikh_submit)
                VALUES (?, ?, ?, ?)
            """, (pelajar_id, minggu, aktiviti, tarikh_submit))
        
        conn.commit()
        st.success(f"Logbook minggu ke-{minggu} telah disimpan.")

# Papar semua logbook pelajar termasuk status pengesahan
st.markdown("---")
st.subheader("📖 Paparan Semua Logbook")

df = pd.read_sql_query(
    """
    SELECT minggu, aktiviti, tarikh_submit, sah_industri, sah_akademik
    FROM logbook
    WHERE pelajar_id=?
    ORDER BY minggu
    """,
    conn,
    params=(pelajar_id,)
)

if not df.empty:
    df["minggu"] = df["minggu"].astype(int)
    
    df = df.rename(columns={
        "minggu": "Minggu",
        "aktiviti": "Aktiviti",
        "tarikh_submit": "Tarikh Penghantaran",
        "sah_industri": "Pengesahan Penyelia Industri",
        "sah_akademik": "Pengesahan Penyelia Akademik"
    })

    st.dataframe(df, use_container_width=True)
else:
    st.info("Tiada logbook dimasukkan setakat ini.")
