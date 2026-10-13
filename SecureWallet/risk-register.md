# Risk Register — SecureWallet

Skala: kemungkinan (K) 1 sangat jarang sampai 5 sangat sering; dampak (D) 1 rendah sampai 5 kritis. Skor = K × D. Prioritas tinggi dipilih berdasarkan skor dan konsekuensi aset.

| Risiko | Ancaman terkait | K | D | Skor | Prioritas | Alasan | Kontrol/rencana | Pemetaan lanjutan |
|---|---|---:|---:|---:|---|---|---|---|
| R-01 Nominal transaksi diubah | T-01 | 3 | 5 | 15 | P1 | Perubahan nominal bisa mengubah makna transaksi; payload ditandatangani sehingga verifikasi wajib | Kanonisasi payload; RSA-PSS/SHA-256; tolak signature tidak valid; tes perubahan nominal | Tugas 2: validasi dan pengujian tampering |
| R-02 Kunci publik palsu dipasangkan dengan identitas | T-02 | 3 | 5 | 15 | P1 | Tanpa registrasi kunci, signature valid belum membuktikan pemilik akun | Untuk prototipe dokumentasikan batasan; tahap berikutnya ikat kunci ke identitas melalui proses registrasi tepercaya dan rotasi/revokasi | Tugas 2: model identitas/kunci |
| R-03 Riwayat ditulis ulang | T-05 | 3 | 4 | 12 | P1 | Penyerang yang dapat menulis ulang seluruh file bisa membangun ulang hash chain | Checkpoint hash di lokasi terpisah/append-only log; backup; verifikasi rantai saat baca | Tugas 3: audit log dan penyimpanan |
| R-04 Penggunaan ulang transaksi (replay) | T-11 | 3 | 4 | 12 | P1 | Nonce belum dicek terhadap daftar transaksi yang sudah diproses | Simpan ID/nonce yang telah dipakai secara atomik; tolak duplikat; tes pengiriman ulang | Tugas 2: aturan anti-replay |
| R-05 Kunci privat bocor | T-04 | 2 | 5 | 10 | P1 | Siapa pun yang memperoleh kunci dapat membuat tanda tangan yang tampak valid | Jangan commit kunci; jangan log kunci; gunakan secret manager/HSM atau OS keystore untuk produksi; rencana rotasi dan pencabutan | Tugas 3: pengelolaan kunci |
| R-06 Signature invalid diterima | T-07 | 2 | 5 | 10 | P2 | Kegagalan verifikasi harus menghasilkan penolakan, bukan penerimaan | Fail-closed; uji signature rusak/kunci salah; tangani error spesifik | Tugas 2: pengujian negatif |
| R-07 Parameter kriptografi melemah | T-10 | 2 | 5 | 10 | P2 | Konfigurasi lemah menurunkan kepercayaan pada signature | Gunakan API tingkat tinggi `cryptography`; RSA 2048+ dan SHA-256; review perubahan | Tugas 3: pemeriksaan dependensi dan konfigurasi |

## Lima risiko prioritas
P1: R-01, R-02, R-03, R-04, R-05. P2: R-06, R-07. Prioritas mempertimbangkan konsekuensi keamanan, bukan skor saja.

## Bukti yang perlu ditunjukkan saat demonstrasi
1. Jalankan `python -m unittest discover -s tests -v`.
2. Tunjukkan transaksi asli lolos verifikasi.
3. Ubah nominal tanpa membuat signature baru; verifikasi harus gagal.
4. Tunjukkan tes rantai hash mendeteksi perubahan.
5. Jelaskan bahwa hash chain lokal tidak mencegah penyerang mengganti seluruh rantai, dan bahwa identitas pemilik kunci belum disediakan oleh signature saja.
