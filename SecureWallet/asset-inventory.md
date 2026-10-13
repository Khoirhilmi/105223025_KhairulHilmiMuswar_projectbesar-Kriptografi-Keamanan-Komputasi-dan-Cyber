# Asset Inventory — SecureWallet

| ID | Aset | Lokasi/aliran | Kebutuhan keamanan | Prioritas | Kontrol awal |
|---|---|---|---|---|---|
| A-01 | Isi transaksi sintetis (ID, pengirim, penerima, nominal, waktu, nonce) | DFD-01, DFD-02 | Integritas, validasi, autentikasi pengirim | Tinggi | Validasi input dan tanda tangan RSA-PSS |
| A-02 | Kunci privat pengirim | DFD-03 | Kerahasiaan dan kontrol penggunaan | Kritis | Dibuat dengan CSPRNG; hanya di memori pada demo; tidak masuk Git |
| A-03 | Kunci publik pengirim | DFD-03 | Integritas dan pengikatan identitas kunci | Tinggi | Dipakai untuk verifikasi; pada produksi perlu registrasi/validasi identitas |
| A-04 | Tanda tangan digital | DFD-02, DFD-04 | Integritas dan bukti bahwa pemegang kunci menandatangani payload | Tinggi | Verifikasi sebelum menerima transaksi |
| A-05 | Riwayat transaksi dan hash rantai | DFD-04 | Deteksi modifikasi dan pengurutan ulang | Tinggi | SHA-256 atas entri deterministik dan hash sebelumnya |
| A-06 | Kode aplikasi dan dependensi | DFD-01 sampai DFD-04 | Integritas dan ketersediaan | Sedang | Dependensi tercatat; tes otomatis; tinjauan perubahan |
| A-07 | Hasil verifikasi/keputusan penerimaan | DFD-04 | Integritas dan akuntabilitas | Tinggi | Transaksi ditolak jika tanda tangan tidak valid |

## Asumsi
- Versi awal berjalan lokal dan memakai data sintetis.
- Belum ada akun nyata, saldo otoritatif, API, database produksi, atau perangkat pengguna.
- Kunci privat demo dibuat sementara dan tidak diekspor. Ancaman pencurian memori tetap relevan sebagai risiko desain bila kelak menjadi layanan.
