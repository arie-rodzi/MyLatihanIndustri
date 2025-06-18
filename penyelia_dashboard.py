
import streamlit as st
import sqlite3

st.set_page_config(page_title="Dashboard Pensyarah", layout="wide")
st.title("👨‍🏫 Dashboard Penyelia Akademik")

# Sambung ke fail DB sebenar
conn = sqlite3.connect("/mnt/data/latihan_industri (6).db")
c = conn.cursor()

# Borang login
with st.sidebar:
    st.subheader("🔐 Log Masuk Pensyarah")
    penyelia_id = st.text_input("Masukkan ID Staf Anda (contoh: PA001)")
    login = st.button("Log Masuk")

if login:
    # Semak sama ada ID wujud dalam kolum penyelia_akademik_id
    c.execute("SELECT DISTINCT penyelia_akademik_id FROM maklumat_pelajar WHERE penyelia_akademik_id=?", (penyelia_id,))
    exists = c.fetchone()

    if exists:
        st.success(f"Selamat datang, {penyelia_id}")

        # Dapatkan senarai pelajar di bawah pensyarah ini
        c.execute("""
            SELECT pelajar_id, nama, kod_program, emel
            FROM maklumat_pelajar
            WHERE penyelia_akademik_id=?
        """, (penyelia_id,))
        pelajar_list = c.fetchall()

        if pelajar_list:
            st.markdown("### 📋 Senarai Pelajar Anda")
            for pelajar_id, nama, kod_program, emel in pelajar_list:
                st.markdown(f"""
                - **Nama Pelajar:** {nama}  
                - **ID Pelajar:** {pelajar_id}  
                - **Program:** {kod_program}  
                - **Emel:** {emel}
                """)
                st.markdown("---")
        else:
            st.info("Tiada pelajar dipadankan dengan anda.")
    else:
        st.error("❌ ID staf tidak wujud dalam sistem.")

conn.close()
