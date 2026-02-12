# Panduan Menjalankan Project (Local)

Catatan ini isinya langkah-langkah buat nyiapin dan jalanin aplikasi **Smart Route Optimization** di laptop/komputer lokal.

---

## 📋 Persiapan Awal

Sebelum mulai, pastiin sudah ada:

- **Python 3.9 ke atas** (Paling aman pakai versi 3.10+).
- **Git** (Kalau mau download langsung dari repo).
- **Internet** (Buat download library pas pertama kali setup).

---

## 🛠️ Langkah Setup

### 1. Download Source Code

Buka Terminal atau CMD, terus masuk ke folder tempat nyimpen project ini.

```bash
git clone https://github.com/ketsar28/Smart-Route-Optimization.git
cd Smart-Route-Optimization
```

_(Kalau download ZIP, tinggal ekstrak saja terus buka foldernya lewat terminal)._

### 2. Buat Virtual Environment

Biar library project ini nggak kecampur-campur sama yang lain, saya saranin buat virtual environment dulu:

- **Windows:**
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Library

Pastiin sudah aktif enviroment-nya (biasanya ada tulisan `.venv` di terminal), terus jalanin ini:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Ini bakal otomatis download semua library yang saya pakai (Streamlit, Plotly, dll).

---

## 🚀 Cara Jalanin Aplikasi

Kalau sudah beres semua, tinggal panggil aplikasinya pakai perintah:

```bash
streamlit run Program/gui/app.py
```

Setelah itu:

1.  Bakal muncul alamat URL di terminal (biasanya `http://localhost:8501`).
2.  Tunggu bentar, browser bakal kebuka sendiri nampilin dashboard optimasinya.

---

## 📂 File Penting

- `Program/gui/app.py`: File utama buat jalanin dashboard.
- `Program/data/samples/`: Data contoh (JSON) kalau mau coba-coba skenario rute.
- `requirements.txt`: Daftar library yang saya pakai di project ini.

---

## ❓ Kalau Ada Masalah (Troubleshooting)

**1. 'python' nggak dikenal di terminal**

- Cek lagi instalasi Python-nya, pastiin sudah diceklis bagian "Add to PATH" pas install.

**2. Error ModuleNotFoundError**

- Cek lagi pip install-nya. Kadang perlu diulang atau pastiin virtual env-nya beneran sudah aktif.

**3. Loading-nya agak lama pas pertama buka**

- Wajar kok, Streamlit lagi nyiapin environment di browser. Tunggu saja sampe tulisan "Running" di pojok kanan atas ilang.

---

_Catatan kecil: Project ini dibuat biar urusan routing logistik jadi lebih gampang._
