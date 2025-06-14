import streamlit as st
import sqlite3

DB_FILE = 'database/latihan_industri.db'

def update_password(pelajar_id, new_pw):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET katalaluan=? WHERE pelajar_id=?", (new_pw, pelajar_id))
    conn.commit()
    conn.close()

st.title("Tukar Katalaluan")

if 'user_id' not in st.session_state:
    st.warning("Sila log masuk terlebih dahulu.")
else:
    lama = st.text_input("Katalaluan Lama", type="password")
    baru = st.text_input("Katalaluan Baru", type="password")
    sahkan = st.text_input("Sahkan Katalaluan Baru", type="password")
    if st.button("Kemaskini"):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT katalaluan FROM users WHERE pelajar_id=?", (st.session_state.user_id,))
        actual = c.fetchone()[0]
        conn.close()
        if lama != actual:
            st.error("Katalaluan lama tidak betul.")
        elif baru != sahkan:
            st.error("Katalaluan baru tidak sepadan.")
        else:
            update_password(st.session_state.user_id, baru)
            st.success("Katalaluan berjaya dikemaskini.")
