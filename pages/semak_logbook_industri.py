# Simpan fail semak_logbook_industri.py dengan struktur baru logbook
code = '''
import streamlit as st
import sqlite3

st.set_page_config(page_title="Pengesahan Logbook Industri", layout="wide")
st.title("📘 Pengesahan Logbook oleh Penyelia Industri")

# Semak peranan
if st.session_state.get("user_role") != "penyelia_industri":
    st.warning("Modul ini hanya untuk penyelia industri.")
    st.stop()

penyelia_id = st.session_state.get("user_id", "")

# Sambung ke database
conn = sqlite3.connect("database/latihan_industri.db")
c = conn.cursor()

# Struktur baru logbook
c.execute("""
CREATE TABLE IF NOT EXISTS logbook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pelajar_id TEXT,
    minggu INTEGER,
    aktiviti TEXT,
    disahkan_oleh_industri TEXT,
    disahkan_oleh_akademik TEXT
)
""")

# Dapatkan pelajar yang diselia
c.execute("SELECT pelajar_id, nama FROM maklumat_pelajar WHERE penyelia_industri_id=?", (penyelia_id,))
pelajar_list = c.fetchall()

if not pelajar_list:
    st.info("Tiada pelajar diselia oleh anda.")
    st.stop()

pelajar_dict = {f"{nama} ({pid})": pid for pid, nama in pelajar_list}
selected_pelajar = st.selectbox("📌 Pilih Pelajar", options=list(pelajar_dict.keys()))
pelajar_id = pelajar_dict[selected_pelajar]

# Papar logbook pelajar tersebut
st.subheader("📅 Entri Logbook Mingguan Pelajar")

c.execute("""
SELECT id, minggu, aktiviti, disahkan_oleh_industri 
FROM logbook 
WHERE pelajar_id=? ORDER BY minggu
""", (pelajar_id,))
entries = c.fetchall()

if not entries:
    st.info("Tiada logbook dihantar oleh pelajar ini.")
else:
    for log_id, minggu, aktiviti, disahkan_industri in entries:
        with st.expander(f"📘 Minggu {minggu}:"):
            st.markdown(f"""
            <div style='
                background-color: #f9f9f9;
                padding: 15px;
                border-left: 5px solid #2c91e1;
                font-size: 16px;
                line-height: 1.6;
                border-radius: 6px;
            '>
            <b>Aktiviti:</b><br>{aktiviti}
            </div>
            """, unsafe_allow_html=True)

            if disahkan_industri:
                st.success(f"✅ Telah disahkan oleh {disahkan_industri}")
            else:
                if st.button(f"Sahkan Minggu {minggu}", key=f"sahkan_{log_id}"):
                    c.execute("UPDATE logbook SET disahkan_oleh_industri=? WHERE id=?", (penyelia_id, log_id))
                    conn.commit()
                    st.success(f"Logbook minggu {minggu} telah disahkan.")

conn.close()
'''

# Tulis ke fail
filepath = "/mnt/data/semak_logbook_industri.py"
with open(filepath, "w") as f:
    f.write(code)

filepath
