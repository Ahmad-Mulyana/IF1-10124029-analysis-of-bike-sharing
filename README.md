# Dashboard Analisis & Clustering Penyewaan Sepeda 🚲

## Deskripsi Proyek

Proyek ini bertujuan untuk melakukan analisis data penyewaan sepeda dan menyajikan hasilnya dalam bentuk dashboard interaktif. Analisis dilakukan melalui pembersihan data, penghapusan outlier, serta penerapan teknik clustering untuk mengelompokkan hari berdasarkan tingkat aktivitas penyewaan.

Hasil analisis kemudian diintegrasikan ke dalam dashboard berbasis Streamlit yang memungkinkan pengguna mengeksplorasi tren penyewaan, kondisi cuaca, musim, serta segmentasi data secara visual dan real-time.

Dashboard ini dirancang untuk membantu memahami pola penggunaan sepeda sehingga dapat mendukung pengambilan keputusan berbasis data.

---

## Alur Proyek

Proyek terdiri dari dua tahap utama:

### 1. Analisis & Clustering Data

Tahapan analisis meliputi:

* Ekstraksi dataset penyewaan sepeda
* Pembersihan data menggunakan metode IQR untuk menghapus outlier
* Normalisasi fitur numerik
* Clustering menggunakan algoritma K-Means
* Pelabelan cluster menjadi:

  * Hari Sepi
  * Hari Normal
  * Hari Ramai

Hasil akhir disimpan dalam file:

```
bike_final_model_ready.csv
```

File ini digunakan oleh dashboard untuk visualisasi clustering.

---

### 2. Dashboard Interaktif

Dashboard menyediakan:

* Filter tanggal, musim, dan cuaca
* KPI penyewaan sepeda
* Scatter plot hasil clustering
* Grafik tren penyewaan
* Tabel data terfilter

Semua visualisasi diperbarui secara otomatis berdasarkan filter pengguna.

---

## Dataset

Dataset penyewaan sepeda mencakup:

* Tanggal penyewaan
* Suhu dan kelembaban
* Kecepatan angin
* Jumlah penyewaan sepeda
* Informasi musim dan cuaca

Dataset utama:

* `day.csv`
* `hour.csv`

Dataset hasil analisis:

* `bike_final_model_ready.csv`

---

## Teknologi yang Digunakan

* Python
* Pandas & NumPy
* Matplotlib & Seaborn
* Scikit-learn (K-Means clustering)
* Streamlit
* Plotly

---

## Struktur Folder

```
further-analysis-of-bike-sharing/
│
├── dashboard/
│   └── dashboard.py                         # Aplikasi dashboard Streamlit
│
├── data/
│   ├── bike_final_model_ready.csv           # Dataset hasil clustering
│   ├── day.csv                              # Dataset harian
│   └── hour.csv                             # Dataset per jam
│
├── notebook/
│   └── k-means.py                           # Script analisis & clustering
│
├── Laporan Analisis Lanjutan Bike-sharing.pdf  # Laporan proyek (PDF)
├── requirements.txt                         # Daftar library Python
└── README.md                                # Dokumentasi proyek
```

Struktur folder ini memisahkan komponen analisis, dataset, dashboard,
dan dokumentasi agar proyek lebih terorganisir serta mudah dipahami.


---

## Cara Menjalankan Analisis Data

Langkah ini digunakan untuk menghasilkan dataset clustering:

1. Jalankan file analisis:

```bash
python pdsd.py
```

2. File hasil clustering akan dibuat:

```
bike_final_model_ready.csv
```

---

## Cara Menjalankan Dashboard (Local)

1. Install dependency:

```bash
pip install -r requirements.txt
```

2. Jalankan dashboard:

```bash
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser.

---

## Dashboard Online

Jika sudah dideploy:

[[https://link-dashboard-streamlit.app](https://link-dashboard-streamlit.app)]

---

## Insight yang Diperoleh

Dashboard membantu pengguna untuk:

* Mengidentifikasi tren penyewaan sepeda
* Memahami pengaruh cuaca dan musim
* Melihat segmentasi hari berdasarkan tingkat aktivitas
* Mengeksplorasi data secara interaktif

---

## Tim Pengembang

* Arkan Thejambangs — Tim Laporan
* [Nama Anggota] — Tim Analisis
* [Nama Anggota] — Tim Dashboard

---

## Catatan

Proyek ini dibuat sebagai bagian dari tugas Ujian Akhir Semester untuk mendemonstrasikan analisis data lanjutan dan visualisasi interaktif berbasis dashboard.
