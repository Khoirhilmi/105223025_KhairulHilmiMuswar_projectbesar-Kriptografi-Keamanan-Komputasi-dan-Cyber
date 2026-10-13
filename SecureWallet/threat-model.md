# Threat Model STRIDE — SecureWallet

Skala awal: kemungkinan (K) dan dampak (D) 1–5. Skor = K × D. Nilai adalah estimasi untuk prototipe lokal, bukan pengukuran statistik.

| ID | Elemen DFD | STRIDE | Ancaman spesifik dan aset terdampak | K | D | Skor | Alasan kondisi produk |
|---|---|---|---|---:|---:|---:|---|
| T-01 | DFD-02 | Tampering | Pengguna mengubah nominal setelah payload ditandatangani; A-01 | 3 | 5 | 15 | Input lokal mudah diubah, tetapi signature seharusnya mendeteksi perubahan |
| T-02 | DFD-03, DFD-04 | Spoofing | Penyerang mengganti kunci publik yang diasosiasikan dengan pengirim; A-03, A-07 | 3 | 5 | 15 | Prototipe belum memiliki registrasi identitas/kunci tepercaya |
| T-03 | DFD-03 | Repudiation | Pemilik menyangkal transaksi karena tidak ada bukti pengikatan kunci ke identitas; A-02, A-04 | 3 | 4 | 12 | Signature membuktikan penggunaan kunci, bukan otomatis identitas hukum seseorang |
| T-04 | DFD-03 | Information Disclosure | Kunci privat bocor dari memori atau kelak tersimpan ke file/repository; A-02 | 2 | 5 | 10 | Demo tidak menyimpan kunci, namun pengembangan berikutnya bisa keliru menyimpannya |
| T-05 | DFD-04, DFD-05 | Tampering | Penyerang mengubah transaksi lama dan menghitung ulang hash rantai lokal; A-05 | 3 | 4 | 12 | Hash chain lokal tidak punya checkpoint eksternal/penyimpanan immutable |
| T-06 | DFD-02 | Elevation of Privilege | Input tidak divalidasi dan kelak digunakan untuk melewati aturan transaksi; A-01, A-07 | 2 | 4 | 8 | Demo memvalidasi field dasar; aturan saldo/otorisasi belum ada |
| T-07 | DFD-04 | Tampering | Tanda tangan Base64 rusak atau signature tidak cocok tetap diterima akibat penanganan error salah; A-04, A-07 | 2 | 5 | 10 | Jalur verifikasi adalah titik keputusan kritis; harus fail-closed |
| T-08 | DFD-01, DFD-02 | Denial of Service | Input sangat besar atau berulang membebani proses; A-06 | 2 | 3 | 6 | CLI lokal membatasi paparan, tetapi tidak ada batas ukuran umum untuk layanan jaringan |
| T-09 | DFD-05 | Information Disclosure | Riwayat kelak berisi nama/nomor akun nyata dan terbaca pihak lain; A-01, A-05 | 2 | 4 | 8 | Saat ini data sintetis, belum ada kontrol akses penyimpanan produksi |
| T-10 | DFD-03 | Tampering | Parameter kriptografi diturunkan ke RSA lemah atau hash usang; A-02, A-04 | 2 | 5 | 10 | Implementasi saat ini menetapkan RSA 2048 dan SHA-256; perubahan konfigurasi dapat merusak keamanan |
| T-11 | DFD-02, DFD-04 | Spoofing | Transaksi yang sudah ditandatangani dikirim ulang (replay) bila nanti ada API; A-01, A-07 | 3 | 4 | 12 | Nonce ada pada payload, tetapi belum ada penyimpanan nonce persisten untuk mencegah pemakaian ulang |
| T-12 | DFD-05 | Denial of Service | File riwayat dihapus atau rusak sehingga audit tidak dapat dilakukan; A-05 | 2 | 4 | 8 | Belum ada backup atau pemulihan karena ini prototipe lokal |

## Catatan interpretasi
- Spoofing: pemalsuan identitas/kunci.
- Tampering: perubahan payload, konfigurasi, atau riwayat.
- Repudiation: penyangkalan tindakan; signature saja tidak membuktikan identitas dunia nyata.
- Information Disclosure: pengungkapan kunci atau data riwayat.
- Denial of Service: membuat fungsi tidak tersedia.
- Elevation of Privilege: memperoleh kemampuan yang tidak semestinya, terutama bila kelak ada akun/otorisasi.
