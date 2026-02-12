# Smart Route Optimization System (Decision Support System)

Dalam era modern di mana efisiensi adalah kunci keberhasilan operasional, manajemen logistik seringkali dihadapkan pada tantangan yang kompleks. Biaya operasional yang tinggi, keterbatasan armada, dan tuntutan waktu pengiriman yang ketat menjadi masalah yang harus diselesaikan setiap hari.

Proyek ini hadir sebagai **Sistem Pendukung Keputusan (Decision Support System)** yang dirancang untuk menjawab tantangan tersebut. Dengan memanfaatkan pendekatan algoritma hibrida yang cerdas, sistem ini mampu mengubah perencanaan rute yang rumit dan memakan waktu menjadi proses yang otomatis, terukur, dan optimal.

## Latar Belakang & Permasalahan

Praktik perencanaan rute manual seringkali menghasilkan solusi yang jauh dari kata efisien. Tanpa bantuan komputasi, manusia sulit untuk mempertimbangkan puluhan variabel secara bersamaan, seperti kemacetan, kapasitas muatan kendaraan yang berbeda-beda, dan jendela waktu (time windows) yang spesifik untuk setiap lokasi.

Dampak dari inefisiensi ini sangat nyata:

1.  **Pemborosan Biaya**: Rute yang tidak optimal berarti jarak tempuh yang lebih jauh, konsumsi bahan bakar yang lebih tinggi, dan biaya perawatan kendaraan yang meningkat.
2.  **Keterlambatan Layanan**: Kegagalan memenuhi jam operasional lokasi tujuan (time windows) dapat menurunkan kepuasan pelanggan atau bahkan menyebabkan kegagalan layanan.
3.  **Utilitas Armada Rendah**: Penggunaan armada yang tidak seimbang seringkali menyebabkan sebagian kendaraan kelebihan muatan sementara yang lain kurang dimanfaatkan.

## Solusi: Pendekatan Optimasi Cerdas

Sistem ini menawarkan pendekatan komprehensif untuk menyelesaikan masalah _Vehicle Routing Problem with Time Windows (VRPTW)_. Solusi kami tidak hanya mencari rute terpendek, tetapi juga rute yang paling "sehat" secara operasional.

### Fitur Utama

**1. Optimasi Multi-Objektif & Armada Heterogen**
Sistem ini mampu mengelola armada yang terdiri dari berbagai jenis kendaraan (misalnya truk besar, van, dan pickup) secara sekaligus. Algoritma akan secara otomatis memilih kombinasi kendaraan yang paling tepat untuk melayani serangkaian permintaan, mempertimbangkan kapasitas dan biaya operasional masing-masing tipe kendaraan.

**2. Transparansi Proses (Academic Replay)**
Salah satu keunggulan utama sistem ini adalah transparansi. Pengguna tidak hanya disuguhi hasil akhir, tetapi juga dapat melihat bagaimana algoritma bekerja langkah demi langkah. Fitur _Academic Replay_ memungkinkan pengguna, peneliti, atau pengambil keputusan untuk memahami logika di balik setiap keputusan rute yang diambil oleh sistem.

**3. Visualisasi Interaktif & Analisis Mendalam**
Hasil optimasi disajikan dalam bentuk peta interaktif yang detail. Pengguna dapat melihat jalur yang ditempuh, beban muatan setiap kendaraan, hingga status pelayanan setiap titik. Jika terdapat lokasi yang tidak dapat dilayani karena kendala tertentu, sistem akan memberikan analisis penyebabnya secara transparan.

**4. Fleksibilitas Data**
Dirancang untuk kemudahan penggunaan, sistem mendukung input data melalui file Excel standar maupun penentuan titik koordinat secara langsung pada peta digital, memberikan fleksibilitas penuh bagi pengguna di lapangan.

## Pendekatan Teknis

Di balik antarmuka yang ramah pengguna, sistem ini ditenagai oleh rangkaian algoritma metaheuristik yang canggih:

- **Inisialisasi Cerdas**: Menggunakan kombinasi _Sweep Algorithm_ dan _Nearest Neighbor_ untuk membentuk kerangka rute awal yang solid berdasarkan sebaran geografis.
- **Eksplorasi Global (Ant Colony System)**: Terinspirasi dari perilaku koloni semut, algoritma ini mengeksplorasi ruang solusi yang luas untuk menemukan rute-rute potensial yang mungkin terlewat oleh metode konvensional.
- **Perbaikan Lokal (RVND)**: Solusi yang ditemukan kemudian dipoles menggunakan metodologi _Randomized Variable Neighborhood Descent_, yang secara iteratif melakukan pertukaran dan pergeseran titik kunjungan untuk meminimalkan total jarak dan biaya hingga mencapai titik optimal.

## Panduan Instalasi & Penggunaan

Untuk menjalankan sistem ini di lingkungan lokal Anda, pastikan Anda telah memiliki Python versi 3.9 atau lebih baru.

**Langkah Instalasi:**

1.  Salin repositori ini ke komputer lokal Anda.
2.  Disarankan untuk membuat _virtual environment_ agar pustaka tidak tercampur dengan proyek lain.
3.  Install seluruh kebutuhan sistem dengan menjalankan perintah:
    `pip install -r requirements.txt`

**Cara Menjalankan:**

Cukup jalankan satu perintah berikut di terminal Anda:
`streamlit run Program/gui/app.py`

Aplikasi akan otomatis terbuka di peramban web default Anda, siap untuk digunakan.

---

_Dikembangkan dengan dedikasi tinggi untuk menghadirkan solusi logistik yang lebih baik dan efisien._
