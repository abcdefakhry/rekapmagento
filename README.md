# Rekonsiliasi Data PSH & Member - Magento Lois

Aplikasi web client-side (murni offline tanpa server) untuk mengotomasi proses rekonsiliasi data transaksi PSH dan profil member antara sistem POS (Kasir) dan sistem Magento Lois.

## Fitur Utama

### 1. Rekonsiliasi Data PSH & Magento Lois
- Pemisahan Non-Member Otomatis: Memfilter baris transaksi dengan mbrps == 9999999999 ke sheet DATA NON MEMBER.
- Perhitungan Point Magento: Memisahkan nilai poin menjadi Point Positif dan Point Negatif.
- Pembuatan Sheet Rekap Bersih: Menyusun referensi Transaction No., Point Positif, dan Point Negatif.
- Pencocokan Transaksi: Menghubungkan nops dengan Transaction No. untuk menentukan Point Magento, status (SAMA, TIDAK SAMA, TRANSAKSI TIDAK DITEMUKAN), dan keterangan.
- AutoFilter & Summary Box: Menghasilkan 4 sheet (DATA MEMBER, DATA NON MEMBER, DATA MAGENTO, REKAP BERSIH) dengan AutoFilter terpasang otomatis pada baris 1.

### 2. Rekonsiliasi Data Member & Magento Lois
- Standarisasi LAC No (Key): Normalisasi otomatis 10 digit (leading zero) untuk kode LAC angka.
- Validasi Nama & Point: Memeriksa kesesuaian Nama (SESUAI / TIDAK SESUAI) dan Saldo Point (SAMA / TIDAK SAMA).
- Validasi Ganda & Keterangan: Menandai data yang cocok vs yang perlu dicek manual.
- Cek Duplikat Member: Mendeteksi duplikasi kode member (kdmbr).
- Output 3 Sheet: DATA MEMBER PUSAT, MAGENTO DATA MEMBER PUSAT, dan HASIL ANALISIS (lengkap dengan AutoFilter baris 1 dan tabel summary rekap).

---

## Cara Menggunakan

1. Clone repositori ini atau unduh filenya.
2. Buka file index.html langsung di browser (Google Chrome, Safari, Edge, Firefox).
3. 100% Offline: Tidak membutuhkan koneksi internet atau server backend. Semua proses berjalan langsung di browser laptop Anda dengan keamanan data terjamin.
