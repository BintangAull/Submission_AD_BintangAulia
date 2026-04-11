# 📊 Dashboard Project

Project ini merupakan aplikasi **dashboard interaktif** yang dibangun menggunakan Streamlit untuk menganalisis *E-Commerce Public Dataset*.
Melalui dashboard ini, pengguna dapat mengeksplorasi data dan mendapatkan insight melalui visualisasi yang interaktif di browser.
Project ini dikembangkan sebagai **submission akhir modul Analisis Data** pada program **Dicoding – Coding Camp 2026 (Powered by DBS)**, dengan tujuan untuk menerapkan teknik analisis data dan visualisasi secara end-to-end.

---

## ✨ Fitur
- Dashboard interaktif berbasis Streamlit
- Visualisasi hasil analisis data
- Mudah dijalankan secara lokal (local environment)

---

## 📁 Struktur Project

```text
dashboard-project/
├── dashboard/
│   └── dashboard.py
├── data/
├── Notebook.ipynb
├── requirements.txt
└── README.md
```

---

## ⚙️ Persiapan Environment

Sebelum menjalankan project, pastikan sudah terinstall:

- Python ≥ 3.12
- pip (Python package manager)
- virtual environment (disarankan)

---

## 🧪 1. Membuat Virtual Environment

Jalankan perintah berikut di terminal pada folder project:

```
python -m venv .venv
```

## 2. Mengaktifkan Virtual Environment


- Windows:
    ``.venv\Scripts\activate``
- Mac/Linux:
    ``.venv/bin/activate``

## 3. Install Requirements

Setelah virtual environment aktif, install semua library yang dibutuhkan:


``
pip install -r requirements.txt
``

Jika error, terjadi pastikan pip sudah terbaru atau silahkan cari tau sendiri la dah ada gpt 

``
python -m pip install --upgrade pip
``

## 4. Menjalankan Dashboard 

``
streamlit run dashboard/dashboard.py
``