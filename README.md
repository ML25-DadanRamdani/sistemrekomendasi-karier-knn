# 🎓 Sistem Rekomendasi Karier Berdasarkan Minat dan Keahlian

## 📌 Latar Belakang & Deskripsi Proyek
Proyek ini adalah aplikasi web interaktif yang dikembangkan sebagai bagian dari penelitian skripsi program studi Teknik Informatika S1. Sistem ini dirancang untuk memecahkan kebingungan yang sering dialami mahasiswa atau pencari kerja dalam menentukan spesialisasi di bidang IT. 

Dengan memanfaatkan algoritma **Machine Learning K-Nearest Neighbor (KNN)**, aplikasi ini mengevaluasi skor minat dan keahlian pengguna pada berbagai bidang IT untuk memberikan rekomendasi jalur karier yang paling optimal dan berbasis data.

## 🚀 Fitur Utama
- **Prediksi Karier Cerdas:** Pengguna dapat menginput metrik keahlian mereka (Pemrograman, Analisis Data, Jaringan, Desain, dan Manajemen) pada skala 1-5. Model akan langsung mengklasifikasikan dan merekomendasikan peran IT yang paling sesuai.
- **Visualisasi & Eksplorasi Data:** Dilengkapi dengan dasbor analitik interaktif untuk melihat sebaran data pelatihan, pola hubungan antar *skill*, dan distribusi target karier secara *real-time*.
- **Informasi Karier Terperinci:** Menyediakan basis data informasi mengenai kebutuhan keahlian spesifik untuk setiap profesi IT (misal: *tools* dan bahasa pemrograman yang wajib dikuasai).

## 🛠️ Teknologi & Tools
Proyek ini dibangun menggunakan *stack* teknologi analisis data dan *machine learning* modern:
- **Bahasa Pemrograman:** Python
- **Machine Learning:** Scikit-Learn (K-Nearest Neighbor)
- **Web Framework:** Streamlit
- **Pengolahan Data:** Pandas, NumPy
- **Visualisasi Data:** Plotly Express

## 📊 Dataset & Metodologi
Model klasifikasi dalam sistem ini dilatih secara kuantitatif menggunakan dataset yang telah dibersihkan, berisi **297 sampel data**. Target klasifikasi mencakup berbagai peran profesional di industri teknologi, antara lain:
- Software Engineer
- Data Analyst
- UI/UX Designer
- IT Project Manager
- Database Administrator
- Network Engineer

##💻 Cara Menjalankan Aplikasi
1. Instal Dependencies (Library)
Sistem ini memerlukan beberapa library utama. Buka terminal/command prompt, lalu instal semua kebutuhan dengan menjalankan perintah berikut:
```bash
pip install streamlit pandas scikit-learn plotly numpy
```
2. Jalankan Aplikasi
Setelah semua library berhasil terinstal, pastikan Anda berada di direktori proyek, lalu jalankan server lokal Streamlit dengan mengeksekusi perintah berikut di terminal:
```bash
streamlit run app.py
```
3. Akses Antarmuka Web
Jika aplikasi berhasil berjalan, terminal akan menampilkan tautan lokal (biasanya berjalan di port default: http://localhost:8501). Buka tautan tersebut di dalam browser Anda untuk mulai menggunakan sistem rekomendasi karier.

---

## 📂 Struktur Folder & File
Berikut adalah susunan direktori dan file utama yang ada di dalam proyek ini:

```text
├── app.py                 # File utama aplikasi web (antarmuka Streamlit)
├── dataset_bersih.csv     # Dataset yang digunakan untuk analisis dan visualisasi
├── model_knn.pkl          # Model Machine Learning (KNN) yang sudah dilatih
├── scaler.pkl             # Model scaler untuk normalisasi/standarisasi input pengguna
├── requirements.txt       # (Opsional) Daftar dependensi library
└── README.md              # Dokumentasi proyek (file ini)
