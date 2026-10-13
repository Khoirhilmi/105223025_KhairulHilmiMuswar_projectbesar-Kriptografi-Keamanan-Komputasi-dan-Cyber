# SecureWallet — Simulasi Dompet Digital dengan Tanda Tangan Digital

## 1. Deskripsi produk
SecureWallet adalah prototipe lokal untuk mempelajari keamanan transaksi dompet digital. Pengguna membuat transaksi sintetis; aplikasi menandatangani isi transaksi dengan RSA-PSS/SHA-256, memverifikasi tanda tangan menggunakan kunci publik, dan menyimpan transaksi pada rantai hash sederhana untuk membantu mendeteksi perubahan riwayat.

**Batasan:** ini bukan layanan pembayaran sungguhan. Tidak ada jaringan, bank, saldo uang nyata, autentikasi produksi, atau perlindungan kunci setara perangkat keras. Rantai hash lokal bukan blockchain dan tidak mencegah penyerang yang dapat mengganti seluruh berkas beserta hash-nya.

## 2. Aset dan kebutuhan kriptografi

| Data/aset | Tujuan keamanan | Prioritas | Kebutuhan komponen yang dapat diuji |
|---|---|---:|---|
| Isi transaksi: ID, pengirim, penerima, nominal, waktu, nonce | Integritas dan autentikasi pengirim | P1 — tinggi | Perubahan satu field harus membuat verifikasi tanda tangan gagal |
| Kunci privat pengirim | Kerahasiaan dan kontrol penggunaan kunci | P1 — tinggi | Kunci dibuat dengan CSPRNG dari pustaka `cryptography`; tidak disimpan atau di-commit ke repository |
| Kunci publik pengirim | Verifikasi tanda tangan | P1 — tinggi | Kunci publik yang sesuai menerima tanda tangan valid; kunci yang berbeda menolak |
| Riwayat transaksi dan hash sebelumnya | Deteksi perubahan urutan/isi riwayat | P2 — tinggi | Perubahan transaksi lama membuat pemeriksaan rantai gagal |
| Hasil verifikasi | Keputusan penerimaan transaksi | P1 — tinggi | Transaksi bertanda tangan tidak valid ditolak |

## 3. Rancangan komponen (masukan–proses–keluaran)

### A. Pembuatan dan penandatanganan transaksi
- **Masukan:** ID, pengirim, penerima, nominal positif, timestamp ISO-8601, nonce.
- **Proses:** serialisasi JSON deterministik UTF-8; hash SHA-256; tanda tangan RSA-PSS dengan MGF1-SHA256 dan salt length sesuai digest.
- **Keluaran:** objek transaksi dan tanda tangan Base64.
- **Keacakan:** kunci RSA dibuat oleh pustaka `cryptography` yang menggunakan sumber keacakan sistem operasi/CSPRNG. Nonce demo bukan pengganti nonce produksi yang dikelola aman.

### B. Verifikasi
- **Masukan:** transaksi, tanda tangan, kunci publik.
- **Proses:** serialisasi ulang isi transaksi yang sama, lalu verifikasi RSA-PSS/SHA-256.
- **Keluaran:** `True` untuk tanda tangan valid; `False` untuk tanda tangan tidak valid.

### C. Rantai hash audit
- **Masukan:** transaksi yang telah ditandatangani dan hash entri sebelumnya.
- **Proses:** SHA-256 atas representasi JSON deterministik entri audit.
- **Keluaran:** hash entri yang menghubungkan riwayat secara berurutan.

**Encoding vs enkripsi:** JSON UTF-8 dan Base64 hanya representasi data, bukan enkripsi. RSA-PSS adalah tanda tangan digital, bukan mekanisme untuk menyembunyikan isi transaksi. SHA-256 menghasilkan hash, bukan enkripsi.

## 4. Alasan pemilihan pustaka
Menggunakan paket Python `cryptography`, pustaka kriptografi terpelihara yang menyediakan implementasi RSA dan primitive hash dengan API tingkat tinggi. Tidak mengimplementasikan algoritma kriptografi sendiri dan tidak memakai sandi klasik untuk perlindungan produk.

## 5. Cara menjalankan

Python 3.10 atau lebih baru direkomendasikan.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v
```

Demo membuat kunci sementara di memori, menandatangani transaksi sintetis, memverifikasinya, lalu mendemonstrasikan penolakan setelah nominal diubah. Kunci privat tidak ditulis ke disk.

## 6. Skenario uji otomatis
1. Tanda tangan transaksi asli valid.
2. Nominal yang dimodifikasi ditolak.
3. Tanda tangan yang diverifikasi dengan kunci publik berbeda ditolak.
4. Transaksi dengan nominal nol ditolak saat validasi.
5. Perubahan entri lama terdeteksi oleh pemeriksaan rantai hash.

Jalankan seluruh skenario dengan satu perintah: `python -m unittest discover -s tests -v`.

## 7. Artefak Keamanan Komputasi dan Cyber
- `asset-inventory.md`: inventaris aset dan kontrol awal.
- `dfd.md`: DFD dengan ID elemen dan dua trust boundary.
- `threat-model.md`: ancaman STRIDE spesifik yang memetakan elemen DFD dan aset.
- `risk-register.md`: penilaian kemungkinan, dampak, lima risiko prioritas, dan rencana kontrol.
- `AI_LOG.md`: catatan penggunaan AI yang perlu disesuaikan dengan penggunaan sebenarnya.

## 8. Tag pengumpulan
Sebelum mengumpulkan, tinjau semua file, jalankan tes, dan pastikan tidak ada rahasia dalam repository. Buat commit lalu tag `sec-0.1`:

```bash
git init
git add .
git commit -m "Initial SecureWallet security baseline"
git tag sec-0.1
git rev-parse --short sec-0.1
git remote add origin https://github.com/<username>/securewallet
git branch -M main
git push -u origin main
git push origin sec-0.1
```

Jika repository GitHub sudah dibuat, sesuaikan langkah `git init`/remote agar tidak menimpa riwayat yang ada. Setelah tenggat, jangan pindahkan tag. Salin URL repository dan hasil `git rev-parse --short sec-0.1` ke kolom pengumpulan.

## 9. Batas keamanan dan pekerjaan lanjutan
- Prototipe belum mengimplementasikan saldo otoritatif, login, otorisasi multi-pengguna, penyimpanan kunci aman, anti-replay persisten, atau layanan jaringan.
- Untuk penggunaan nyata dibutuhkan manajemen kunci yang aman, autentikasi, kontrol akses, pencatatan audit yang tahan manipulasi, backup, pembatasan transaksi, dan tinjauan keamanan profesional.
