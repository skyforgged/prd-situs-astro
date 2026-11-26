# QG-12 — Sample Editorial Review: TNV Certification

> Status: Snapshot diagnosis awal; hasil audit terkini dan klasifikasi seluruh situs ada di [QG12-FULL-SITE-EDITORIAL-AUDIT.md](QG12-FULL-SITE-EDITORIAL-AUDIT.md)  
> Tanggal review: 2026-11-26  
> Repository: `skyforgged/tnvcertification`  
> Commit implementasi: `778bac514124d139eac8bf02367ed6c6c3d7362a`  
> Standar: Content Quality & Editorial Standard 1.1

## Catatan status terkini

Dokumen ini dipertahankan sebagai rekaman kondisi sebelum remediasi pada tiga halaman sampel. Artikel Posisi Kualitas, artikel Pengendalian Risiko Kualitas, dan halaman Pelatihan Auditor Internal ISO 9001 telah diremediasi. Perubahan pada repository implementasi telah lolos seluruh workflow CI pada commit `1b5f08ae92d9f2d1d81f2d3bfe142b344590ef2b`. Gunakan audit penuh untuk status setelah remediasi dan backlog seluruh situs.

## 1. Ruang lingkup dan metode

Review ini menguji penerapan QG-12 pada lima halaman representatif:
- 3 artikel;
- 1 halaman layanan sertifikasi;
- 1 halaman program pelatihan.

Penilaian mempertimbangkan intent, kecukupan dan kedalaman proporsional, nilai tambah, akurasi dan bukti, pengalaman/keahlian, keterbacaan, serta CTA/internal link. Jumlah kata tidak digunakan sebagai skor atau syarat lulus.

Fakta ISO 9001:2026 dan masa transisi diperiksa terhadap sumber primer ISO, ISO/TC 176/SC 2, dan Global ACI. Review ini tidak mengklaim telah memverifikasi kredensial, status akreditasi, ruang lingkup akreditasi, pengalaman auditor, atau data operasional TNV Certification; semua itu membutuhkan bukti dari pemilik situs.

## 2. Ringkasan hasil

| Halaman | Jenis | Status QG-12 | Alasan utama |
|---|---|---|---|
| `articles/posisi-kualitas-sebagai-talenta-kompetitif` | Artikel | **Belum lulus** | Terlalu umum; tidak menjelaskan peran, kompetensi, jalur pengembangan, atau contoh kerja; kutipan tidak memiliki sumber |
| `articles/sertifikasi-iso-9001-2015` | Artikel | **Lulus bersyarat** | Jawaban dan rujukan resmi cukup baik; slug dan translationKey masih menyebut 2015 meski isi sudah 2026; tambahkan detail timeline yang relevan |
| `articles/mengendalikan-risiko-kualitas-di-pabrik` | Artikel | **Belum lulus** | Hanya mengidentifikasi dan menyebut kontrol umum; tidak ada metode, contoh risiko, prioritas, atau bukti; kutipan tidak bersumber |
| `services/sertifikasi-iso-9001-2026` | Layanan | **Lulus bersyarat** | Struktur dan rujukan resmi baik; perlu memperjelas layanan/otoritas penyedia, bukti kompetensi, batas ruang lingkup, dan detail proses yang benar-benar berlaku |
| `training/pelatihan-auditor-internal-iso-9001` | Program pelatihan | **Belum lulus** | Belum menjelaskan hasil belajar, peserta sasaran, silabus, metode, durasi, evaluasi, fasilitator, atau informasi pendaftaran |

Status bersyarat berarti struktur dan substansi dasar menjanjikan, tetapi halaman belum boleh dianggap final sebelum tindakan koreksi dan bukti yang relevan diperiksa.

## 3. Temuan per halaman

### 3.1 Artikel: Posisi Kualitas sebagai Talenta Kompetitif

**Status: Belum lulus QG-12.**

Isi hanya memuat dua section singkat setelah hero:
- Nilai yang dibawa talenta kualitas.
- Jalur pengembangan kompetensi.

Keduanya masih berupa pernyataan umum. Artikel belum menjawab secara memadai:
- Apa peran spesifik talenta kualitas dalam organisasi dan bagaimana batasnya terhadap fungsi produksi, QA, QC, dan manajemen?
- Kompetensi teknis dan perilaku apa yang diperlukan?
- Apa contoh pekerjaan atau keputusan sehari-hari?
- Bagaimana jalur pengembangan kompetensi yang realistis?
- Bagaimana organisasi menilai kontribusi peran tersebut?

Kalimat `"Mutu bukanlah peralatan, tetapi cara berpikir setiap pekerja."` disajikan sebagai kutipan tanpa atribusi. Jika bukan kutipan dari sumber yang dapat ditelusuri, hilangkan tanda kutip dan posisikan sebagai pernyataan editorial, atau cantumkan sumber yang benar.

**Tindakan:** kembangkan substansi dengan contoh peran dan kompetensi yang benar-benar dapat dipertanggungjawabkan. Jika tidak tersedia nilai tambah atau sumber keahlian, pertimbangkan menggabungkan artikel ke artikel yang lebih luas daripada mempertahankan halaman tipis.

### 3.2 Artikel: Sertifikasi ISO 9001:2026

**Status: Lulus bersyarat QG-12.**

Kekuatan:
- Menjelaskan ruang lingkup sistem manajemen mutu, tahapan sertifikasi, dan peralihan dari edisi 2015.
- Menjelaskan bahwa sertifikasi tidak menggantikan tanggung jawab organisasi dan bukan jaminan produk selalu bebas ketidaksesuaian.
- Memiliki tautan ke ISO dan ISO/TC 176/SC 2.
- Tidak mengklaim bahwa semua organisasi harus menggunakan satu struktur dokumen yang sama.

Fakta utama yang diperiksa sesuai sumber resmi:
- ISO 9001:2026 diterbitkan pada 16 September 2026 dan menggantikan edisi ISO 9001:2015.
- Global ACI menetapkan masa transisi tiga tahun sampai 30 September 2029 untuk transisi sertifikat yang tercakup dalam persyaratan transisi tersebut.
- Mulai 31 Maret 2028, sertifikasi terakreditasi baru/awal hanya dapat diterbitkan terhadap ISO 9001:2026 dalam lingkup persyaratan Global ACI yang berlaku.

Sumber primer:
- ISO, [ISO launches update to world’s most widely used quality management standard](https://www.iso.org/news/2026/09/ISO9001-2026).
- ISO/TC 176/SC 2, [ISO 9001:2026 has been released](https://committee.iso.org/sites/tc176sc2/home/news/content-left-area/news-and-updates/news-2.html).
- Global ACI, [Transition Requirements for ISO 9001:2026](https://global-aci.org/en/news/global-aci-publishes-transition-requirements-for-iso-90012026/).
- Dokumen normatif transisi: [Global ACI-TECH-3-TR 2029-09-30 (M), PDF](https://sys.global-aci.org/uploads/documents/TECH-3-TR_2029-09-30_%28M%29_ISO_9001_2026_Transition_v1_01.pdf).

Perbaikan yang diperlukan:
1. Tambahkan timeline ringkas yang membedakan tenggat untuk badan akreditasi, lembaga sertifikasi, sertifikasi baru/awal, dan organisasi yang telah tersertifikasi. Jangan menyajikan semua tenggat sebagai kewajiban yang sama bagi semua pihak.
2. Jelaskan bahwa ketentuan Global ACI berlaku pada signatory MRA dan lembaga sertifikasi terakreditasi dalam lingkup yang relevan. Untuk organisasi tertentu, jadwal dan mekanisme transisi harus dikonfirmasi kepada lembaga sertifikasi penerbit.
3. Perbarui slug dan `translationKey` yang masih menyebut `2015`. Sebelum mengubah URL yang sudah dipublikasikan, periksa riwayat indeks/backlink/traffic; jika URL dipertahankan karena nilai historis, dokumentasikan keputusan tersebut. Jika dipindahkan, buat redirect permanen dan perbarui seluruh internal link.
4. Tambahkan penulis/reviewer atau sumber keahlian bila tersedia; jangan membuat identitas atau pengalaman yang tidak dapat dibuktikan.

### 3.3 Artikel: Mengendalikan Risiko Kualitas di Pabrik

**Status: Belum lulus QG-12.**

Isi hanya menyebut:
- Memetakan sumber risiko seperti bahan baku, mesin, dan pergantian shift.
- Menilai risiko berdasarkan kemungkinan dan dampak.
- Contoh kontrol berupa pemeriksaan tambahan, pemeliharaan, dan prosedur kerja.

Topik ini menjanjikan, tetapi belum menjadi panduan yang dapat diterapkan. Pembaca belum mendapat cara melakukan penilaian, menentukan prioritas, memilih kontrol, memeriksa efektivitas, atau menindaklanjuti risiko yang berubah.

Konten dapat diperkuat dengan contoh yang diverifikasi dari proses manufaktur, misalnya:
- perubahan pemasok atau spesifikasi bahan baku;
- parameter proses yang keluar dari batas kendali;
- kegagalan alat ukur atau mesin;
- kesalahan identifikasi/traceability;
- pergantian operator atau shift;
- produk tidak sesuai dan risiko lolos ke pelanggan.

Jika memakai FMEA, control plan, SPC, HACCP, atau metode lain, jelaskan konteks penerapannya dan jangan menyatakan satu metode wajib untuk semua pabrik. Gunakan satu contoh sederhana yang menunjukkan identifikasi, penyebab, dampak, penilaian, kontrol, pemilik tindakan, dan verifikasi efektivitas.

Kalimat `"Setiap risiko yang tidak terukur akan menjadi ancaman bagi mutu."` tidak memiliki atribusi. Hapus tanda kutip kecuali sumbernya dapat diverifikasi.

**Tindakan:** ubah menjadi panduan operasional dengan contoh dan batas penerapan. Jika penulis tidak memiliki sumber atau pengalaman relevan, lakukan riset sumber primer/ahli dan review kompeten sebelum publikasi.

### 3.4 Layanan: Sertifikasi Sistem Manajemen Mutu ISO 9001:2026

**Status: Lulus bersyarat QG-12.**

Kekuatan:
- Menjelaskan standar terkini, ruang lingkup sistem, gambaran proses sertifikasi, transisi, persiapan implementasi, FAQ, dan rujukan resmi.
- Menghindari janji bahwa sertifikasi otomatis menjamin kualitas produk.
- Menyebut bahwa proses dan ketentuan mengikuti skema serta prosedur yang berlaku.
- Menggunakan sumber resmi untuk klaim tanggal publikasi dan transisi.

Kesenjangan utama:
1. Halaman belum cukup menjelaskan siapa penyedia layanan dan batas kewenangannya. Tambahkan identitas badan sertifikasi, status akreditasi dan ruang lingkupnya hanya jika bukti resmi tersedia. Jangan menampilkan logo atau klaim akreditasi tanpa hak dan bukti.
2. Jelaskan proses permohonan yang benar-benar dijalankan TNV, termasuk informasi awal yang diperlukan, tahapan audit, penanganan ketidaksesuaian, keputusan sertifikasi, surveilans, dan sertifikasi ulang. Bedakan praktik umum dari prosedur spesifik TNV.
3. Tambahkan faktor yang memengaruhi waktu dan biaya bila data yang sah tersedia. Jika tidak dapat dipastikan sebelum peninjauan ruang lingkup, nyatakan faktor penentunya dan jangan membuat angka estimasi.
4. Perjelas batas layanan: sertifikasi tidak sama dengan konsultasi implementasi atau jaminan kelulusan audit. Hindari klaim hasil yang tidak dapat dikendalikan.
5. Hubungkan CTA dengan proses permohonan atau kontak yang benar-benar aktif. Label CTA saja tidak cukup bila target tindakannya tidak jelas bagi pengguna.

**Tindakan:** pertahankan struktur halaman; lengkapi informasi operasional dan bukti organisasi yang telah diverifikasi. Klaim akreditasi, ruang lingkup, waktu, dan biaya harus mendapat persetujuan pemilik substansi.

### 3.5 Program: Pelatihan Auditor Internal ISO 9001

**Status: Belum lulus QG-12.**

Halaman saat ini hanya menjelaskan ruang lingkup, tahapan pemeriksaan, dan administrasi sertifikasi dalam satu section. Itu belum cukup untuk membantu calon peserta memutuskan apakah program sesuai kebutuhannya.

Informasi yang perlu tersedia jika memang merupakan bagian dari program:
- profil peserta yang dituju dan prasyarat;
- hasil belajar yang terukur;
- silabus/topik dan pembagian sesi;
- metode belajar dan latihan audit;
- durasi, format, bahasa, dan lokasi;
- metode evaluasi/kelulusan dan dokumen yang diterima peserta;
- identitas dan kompetensi fasilitator yang dapat diverifikasi;
- jadwal, biaya, kuota, dan cara pendaftaran, atau tautan ke jadwal aktif.

Jangan mengisi detail yang belum disetujui. Jika program belum memiliki jadwal atau biaya tetap, jelaskan bahwa informasi diberikan setelah jadwal dibuka atau melalui kanal pendaftaran yang tersedia. Jangan menyiratkan pelatihan ini menghasilkan sertifikasi kompetensi auditor kecuali skema dan otoritasnya memang ada.

**Tindakan:** lengkapi informasi program dari pemilik pelatihan. Bila program belum siap ditawarkan, pertimbangkan status draft/noindex sampai informasi minimum tersedia.

## 4. Pola lintas halaman

### Kekuatan
- Intro dan meta description dibedakan.
- Featured image mempunyai alt yang terkait dengan judul.
- Block hero dan section memiliki urutan yang jelas.
- Artikel ISO 9001:2026 dan layanan mencantumkan rujukan resmi.
- Halaman layanan menyertakan FAQ dan CTA.

### Kelemahan
- Beberapa artikel masih berupa pernyataan generik tanpa contoh, metode, atau bukti.
- Kutipan tanpa atribusi berpotensi memberi kesan ada sumber/pakar padahal tidak ada.
- Informasi yang membantu keputusan pengguna belum konsisten tersedia pada halaman layanan dan training.
- Penulis/reviewer dan kompetensi belum tampak pada sampel yang diperiksa.
- Slug dan translationKey artikel ISO 9001 masih membawa identitas edisi lama meskipun judul dan isi sudah diperbarui.

### Prinsip tindak lanjut
Jangan menambah panjang artikel secara mekanis. Tambahkan hanya informasi yang menyelesaikan pertanyaan pembaca, memperjelas batas, memberi contoh nyata, atau menyediakan bukti yang dapat diperiksa.

## 5. Prioritas remediasi

| Prioritas | Halaman/area | Tindakan |
|---|---|---|
| P0 | Artikel 0001 dan 0003 | Tulis ulang substansi atau gabungkan; hapus kutipan tanpa sumber |
| P0 | Pelatihan Auditor Internal ISO 9001 | Lengkapi informasi keputusan peserta; pastikan klaim sertifikat pelatihan akurat |
| P1 | Layanan ISO 9001:2026 | Verifikasi identitas, akreditasi, ruang lingkup, dan proses spesifik TNV; perjelas CTA |
| P1 | Artikel ISO 9001:2026 | Putuskan slug legacy, perbarui metadata identitas, tambahkan timeline yang relevan |
| P1 | Semua halaman berisiko teknis | Tetapkan pemilik substansi dan reviewer yang kompeten |
| P2 | Seluruh artikel dan training | Audit sampel tambahan untuk menemukan pola halaman tipis atau duplikasi intent |

## 6. Keputusan QG-12 untuk sampel

- **Belum dapat menyatakan QG-12 situs lulus.**
- Dua artikel dinilai belum lulus, satu artikel lulus bersyarat, satu layanan lulus bersyarat, dan satu halaman training belum lulus.
- Review ini adalah diagnosis sampel. Sebelum rilis penuh, semua halaman indexable perlu diklasifikasikan menurut jenis dan risiko, lalu direview sesuai checklist yang relevan.
- Untuk klaim standar/regulasi, catat URL sumber, tanggal verifikasi, reviewer, dan batas penerapan. Untuk halaman layanan/training, bukti internal organisasi sama pentingnya dengan sumber publik.

## 7. Langkah berikutnya

1. Remediasi tiga halaman berstatus belum lulus.
2. Minta bukti internal yang diperlukan untuk halaman layanan dan training; jangan mengarang data operasional.
3. Perluas review ke seluruh halaman indexable, mulai dari halaman dengan risiko teknis dan keputusan bisnis tertinggi.
4. Catat persetujuan reviewer manusia pada PR/issue/publikasi sebagai bukti QG-12.
