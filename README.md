# 📘 Sistem Latihan Industri UiTM (Versi Pelajar + Penyelaras)

Sistem ini dibangunkan menggunakan Python dan Streamlit bagi memudahkan pengurusan proses latihan industri di UiTM. Modul utama termasuk:

## ✅ Modul Pelajar
- Isi Maklumat Peribadi
- Muat Naik BLI-02
- Cetak Borang Permohonan (SLI01/DLI01/BLI02)
- Cetak Surat Penempatan (SLI-03)
- Cetak Borang Lapor Diri (BLI-04)
- Logbook Mingguan (16 minggu)
- Muat Naik Laporan Akhir

## 🛠 Keperluan Sistem
Pastikan anda memasang keperluan berikut sebelum menjalankan sistem:

```bash
pip install -r requirements.txt
```

## 🚀 Cara Jalankan Sistem
```bash
streamlit run app.py
```

## 📁 Struktur Folder
- `pages/` — Modul-modul pelajar
- `template/` — Template rasmi borang .docx
- `generated/` — Dokumen dijana automatik
- `uploads/laporan/` — Laporan akhir pelajar
- `database.db` — Fail SQLite utama

## 📝 Nota
Folder kosong mengandungi fail `.gitkeep` untuk memastikan ia dimuat naik ke GitHub.

Dibangunkan oleh Dr. Zahari Md Rodzi, UiTM Cawangan Negeri Sembilan Kampus Seremban.