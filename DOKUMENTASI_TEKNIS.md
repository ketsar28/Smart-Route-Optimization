# Panduan Singkat Sistem Optimasi Rute (Smart Route Optimization)

Dokumen ini menjelaskan bagaimana program bekerja dalam mencari rute pengiriman yang paling efisien, mulai dari pembagian wilayah hingga hasil akhirnya.

---

## 🚩 1. Menentukan Wilayah Kiriman (`Program/sweep_nn.py`)

Bagian ini bertugas membagi-bagi toko ke dalam beberapa kelompok agar satu kendaraan fokus di satu area saja.

| Bagian           | Baris Kode  | Kegunaan (Bahasa Sederhana)                                                                                                                                                  |
| :--------------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bagi Wilayah** | `41 - 169`  | Mengumpulkan toko yang lokasinya berdekatan. Tujuannya supaya jalur truk tidak berantakan atau saling silang (jalurnya efisien, tidak bolak-balik melewati jalan yang sama). |
| **Urutan Awal**  | `172 - 346` | Membuat daftar urutan pertama toko mana yang harus didatangi agar supir punya panduan awal.                                                                                  |

---

## ⚙️ 2. Mesin Pencari Jalur Terhemat (`Program/rvnd.py`)

Ini adalah bagian yang paling pintar. Komputer akan mencoba ribuan kemungkinan urutan toko untuk mencari jalur yang paling pendek dan hemat bensin.

| Bagian           | Baris Kode  | Kegunaan (Bahasa Sederhana)                                                                                                                                                     |
| :--------------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Cek Muatan**   | `43 - 99`   | Memastikan jumlah barang yang dibawa tidak melebihi kapasitas truk.                                                                                                             |
| **Cek Jam Toko** | `203 - 324` | Memastikan supir sampai sebelum toko tutup (supir tidak datang kepagian atau kemalaman).                                                                                        |
| **Tukar Urutan** | `365 - 399` | Komputer mencoba menukar-nukar posisi toko di dalam satu rute. Misalnya, mencoba urutan Toko A ke B, lalu dicoba B ke A, dicari mana yang paling irit bensin (km paling kecil). |
| **Tukar Truk**   | `755 - 856` | Memindahkan pengiriman dari Truk A ke Truk B jika itu bisa membuat total perjalanan jadi lebih hemat.                                                                           |
| **Bagi Beban**   | `859 - 943` | Jika ada satu truk yang kepenuhan barang, sistem otomatis memindahkan barang tersebut ke truk lain yang masih ada sisa ruang.                                                   |

---

## 🖥️ 3. Tampilan Hasil & Laporan (`Program/gui/tabs/academic_replay_tab.py`)

Bagian ini mengatur bagaimana semua hitungan komputer di atas ditampilkan ke layar agar mudah dibaca.

| Bagian                 | Baris Kode  | Kegunaan (Bahasa Sederhana)                                                                                   |
| :--------------------- | :---------- | :------------------------------------------------------------------------------------------------------------ |
| **Tabel Uji Coba**     | `950 - 985` | Menampilkan semua "percobaan" yang dilakukan komputer sebelum akhirnya memutuskan jalur mana yang paling oke. |
| **Rincian Perjalanan** | `406 - 546` | Menampilkan laporan lengkap: jam tiba, berapa menit supir melayani toko, dan berapa biaya bensinnya.          |

---

## 💡 Ringkasan Cara Kerjanya:

1. **Pilih Area yang Searah**: Toko-toko dikumpulkan berdasarkan lokasinya supaya truk tidak jalan memutar-mutar nggak jelas.
2. **Coba Ribuan Cara**: Komputer melakukan simulasi "tukar-tukar posisi" ribuan kali sampai dapet jalur yang paling dekat jaraknya.
3. **Cek Ulang**: Sistem mengecek: Truknya keberatan muatan nggak? Tokonya sudah buka belum? Kalau semuanya Aman, rute baru dikeluarkan.
