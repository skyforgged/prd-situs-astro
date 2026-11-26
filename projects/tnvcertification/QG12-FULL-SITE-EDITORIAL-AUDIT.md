# QG-12 — Full-site Editorial Audit: TNV Certification

> Status: Audit editorial seluruh URL indexable; bukan persetujuan teknis/operasional atas klaim organisasi  
> Tanggal: 2026-11-26  
> Repository implementasi: `skyforgged/tnvcertification`  
> Commit konten yang direview: `839da551f2d492f2d14188e298c81e0e35779133`  
> Standar acuan: Content Quality & Editorial Standard 1.1

## 1. Kesimpulan eksekutif

Audit mencakup **47 URL indexable** pada hasil Information Architecture Audit: 46 halaman berbasis content collection dan satu katalog layanan bahasa Inggris yang dirender secara programatis (`/en/services/`). Konten draft, kategori berstatus planned, dan data jadwal pelatihan yang bukan halaman editorial tidak dihitung sebagai halaman indexable.

Hasil klasifikasi editorial:

| Status | Jumlah URL | Makna |
|---|---:|---|
| Lulus secara editorial | 8 | Konten/halaman memenuhi tujuan utama dan tidak memiliki kekurangan substansi yang menghalangi pembaca |
| Lulus bersyarat | 14 | Struktur dan substansi dasar memadai, tetapi memerlukan verifikasi fakta, bukti organisasi, atau perbaikan metadata |
| Belum lulus | 25 | Halaman terlalu tipis, generik, berulang, atau belum memberi informasi yang dibutuhkan pembaca |

**Kesimpulan: QG-12 seluruh situs belum lulus.** Penyebab dominan bukan panjang halaman, melainkan 12 halaman program pelatihan dan 9 halaman topik CSMS yang masih memakai uraian generik dan berulang. Empat artikel juga memerlukan pengembangan substansi.

Klasifikasi ini adalah audit editorial berbasis konten yang tersedia di repository. Klaim tentang legalitas badan usaha, status akreditasi, ruang lingkup akreditasi, kompetensi instruktur/auditor, pengalaman, dan proses operasional tidak dapat disahkan hanya dari file konten; bukti pemilik situs tetap diperlukan.

## 2. Ruang lingkup audit

### 2.1 Rekonsiliasi URL

| Sumber | Jumlah record | Status publik | Catatan |
|---|---:|---:|---|
| Articles | 11 | 9 | Dua artikel pengendalian dokumen berstatus draft (Indonesia dan Inggris) |
| Services | 8 | 7 | Halaman CSMS penilaian kontraktor masih draft |
| Training | 14 | 14 | Seluruh halaman program tercatat published |
| Pages | 16 | 16 | Termasuk beranda, katalog, halaman CSMS, dan sembilan topik CSMS |
| **Total content collection** | **49** | **46** | Tiga draft dikecualikan dari URL publik |
| Katalog layanan bahasa Inggris | — | 1 | `/en/services/`, dirender dari data layanan |
| **Total URL indexable** | | **47** | Cocok dengan hasil IA audit |

Collection kategori saat diperiksa berstatus `planned`, sehingga bukan halaman editorial publik. Record `trainingSchedules` merupakan data acara/jadwal dan bukan 47 halaman editorial yang dinilai dalam audit ini.

### 2.2 Prinsip penilaian

- Kecocokan dengan intent dan kebutuhan pengguna.
- Kedalaman yang proporsional terhadap jenis halaman.
- Kejelasan, akurasi, batas klaim, dan sumber.
- Contoh, metode, atau langkah yang dapat dipakai pembaca.
- Keunikan substansi dan tidak mengulang paragraf generik.
- Informasi yang diperlukan untuk mengambil keputusan pada layanan/program.
- CTA dan tautan internal yang relevan.
- Halaman katalog dinilai dari kegunaan navigasi dan listing, bukan dipaksa memiliki artikel panjang.

## 3. Hasil per jenis halaman

### 3.1 Artikel — 9 URL

| File / slug | Status | Temuan dan tindakan |
|---|---|---|
| `0001-posisi-kualitas-sebagai-talenta-kompetitif` | Lulus setelah remediasi | Dikembangkan menjadi panduan tentang peran profesional kualitas, kompetensi, contoh kontribusi, jalur pengembangan, indikator, dan dukungan organisasi. Kutipan tanpa sumber dihapus. |
| `0002-sertifikasi-iso-9001-2015` | Bersyarat | Isi sudah membahas edisi 2026 dan transisi, tetapi slug serta translationKey masih menyebut 2015. Tinjau nilai SEO/backlink sebelum mengubah URL; jika dipindah, sediakan redirect permanen. |
| `0003-mengendalikan-risiko-kualitas-di-pabrik` | Lulus setelah remediasi | Dikembangkan dengan pemetaan proses, sumber risiko, contoh hipotetis perubahan pemasok, pemilihan kontrol, metode analisis, pemantauan efektivitas, dan batas penerapan FMEA. |
| `0004-sertifikasi-iso-45001-2018` | Belum lulus | Hanya dua section singkat. Perlu cakupan sistem, contoh identifikasi bahaya dan pengendalian, partisipasi pekerja, tahapan sertifikasi, batas klaim, serta rujukan resmi. Kutipan penutup tanpa sumber harus dihapus atau diberi atribusi yang dapat diverifikasi. |
| `0005-manajemen-beasiswa-kualitas-di-industri` | Belum lulus | Masih berupa saran umum. Perlu model program, analisis kebutuhan kompetensi, kriteria penerima, tata kelola pendanaan, ikatan/retensi bila relevan, pengukuran hasil, dan risiko program. Jangan membuat kebijakan perusahaan seolah fakta. |
| `0006-penilaian-kepatuhan-terhadap-standar-global` | Belum lulus | Baru menyebut pemetaan persyaratan dan pemeriksaan bukti. Perlu metode register kewajiban, penentuan applicability, pemetaan bukti, sampling, penilaian kesenjangan, tindak lanjut, serta perbedaan audit internal dan penilaian pihak ketiga. Kutipan tanpa sumber dihapus. |
| `0007-proses-audit-sertifikasi-iso-9001-2015` | Bersyarat | Substansi audit cukup lengkap, termasuk tahap 1/2, temuan, keputusan, dan transisi. Slug/translationKey masih menyebut 2015; lakukan keputusan URL dan redirect secara sadar. |
| `0008-manajemen-kualitas-nononkonformitas` | Belum lulus | Hanya dua section. Perlu alur containment, koreksi, analisis penyebab, tindakan korektif, verifikasi efektivitas, contoh kasus, dan pembedaan koreksi dari tindakan korektif. Kutipan tanpa sumber dihapus. |
| `0009-manfaat-sertifikasi-iso-9001-2015-bagi-perusahaan` | Bersyarat | Uraian manfaat cukup lengkap dan menghindari jaminan hasil bisnis. Slug/translationKey masih menyebut 2015. Perlu keputusan metadata/URL dan bukti untuk klaim komersial bila ditambahkan. |

**Ringkasan artikel:** 2 lulus, 3 bersyarat, 4 belum lulus.

Dua artikel yang diremediasi telah dikembangkan tanpa menambahkan klaim pengalaman TNV. Perbaikan format YAML dan frontmatter juga masuk ke pemeriksaan CI setelah remediasi.

### 3.2 Layanan — 7 URL

| Halaman | Status | Temuan |
|---|---|---|
| `iso-14001-2026-certification` (EN) | Bersyarat | Uraian EMS, perubahan, audit, transisi, persiapan, dan referensi cukup lengkap. Perlu verifikasi fakta edisi/transisi dan bukti layanan/akreditasi sesuai lingkup. |
| `sertifikasi-fssc-22000` | Bersyarat | Halaman paling komprehensif; mencakup skema, PRP, HACCP, kategori, audit, Version 7, transisi, dan FAQ. Klaim versi, tanggal, serta masa transisi perlu dipelihara dari sumber resmi skema. |
| `sertifikasi-iso-14001-2026` | Bersyarat | Struktur sistem, audit, transisi, FAQ, dan CTA tersedia. Perlu bukti tentang badan sertifikasi, ruang lingkup pengakuan, dan proses layanan aktual. |
| `sertifikasi-iso-45001` | Bersyarat | Cakupan K3, audit, referensi, FAQ, dan CTA cukup. Klaim kompetensi, akreditasi, serta batas layanan harus diverifikasi. |
| `sertifikasi-iso-50001` | Bersyarat | Membahas EnMS, EnPI/EnB, audit, dan FAQ. Pastikan contoh teknis serta ruang lingkup layanan diperiksa oleh reviewer kompeten. |
| `sertifikasi-iso-9001-2026` | Bersyarat | Struktur dan persiapan praktis baik. Tetap memerlukan bukti identitas badan sertifikasi, akreditasi dan ruang lingkup yang berlaku, proses operasional, serta penjelasan batas layanan. |
| `sertifikasi-iso-iec-27001` | Bersyarat | Cakupan ISMS, risiko, SoA, Annex A, audit, dan FAQ tersedia. Perlu review teknis keamanan informasi serta verifikasi bukti penyedia layanan. |

**Ringkasan layanan:** 7 bersyarat, 0 dinyatakan lulus final, 0 belum lulus substansi.

Status bersyarat bukan berarti isi layanan tidak berguna. Artinya konten publik tidak cukup untuk membuktikan otoritas, akreditasi, ruang lingkup, atau pelaksanaan layanan yang ditawarkan. Jangan menambahkan logo akreditasi, nama lembaga, nomor sertifikat, klaim auditor, biaya, atau estimasi waktu tanpa bukti yang disetujui.

### 3.3 Program pelatihan — 14 URL

| Halaman | Status | Temuan dan tindakan |
|---|---|---|
| `pelatihan-auditor-internal-cgmp` | Belum lulus | Hanya hero dan satu section generik. Perlu tujuan belajar, ruang lingkup cGMP, praktik audit, contoh bukti, kompetensi, dan informasi program terverifikasi. |
| `pelatihan-auditor-internal-fssc-22000` | Bersyarat | Materi paling lengkap: tujuan, kompetensi, materi, bukti audit, temuan, tahapan, peserta, sektor, metode, dan FAQ. Tetap perlu silabus final, fasilitator, durasi, metode, evaluasi, biaya, dan dokumen kelulusan yang disetujui. |
| `pelatihan-auditor-internal-iatf-16949` | Belum lulus | Hanya hero dan satu uraian generik. Perlu materi audit otomotif yang tepat, proses audit, contoh bukti, kompetensi, dan batas penggunaan persyaratan IATF. |
| `pelatihan-auditor-internal-iso-13485` | Belum lulus | Hanya hero dan satu uraian generik. Perlu konteks perangkat medis, dokumentasi, traceability, risiko, bukti audit, dan pembatasan sesuai ruang lingkup program. |
| `pelatihan-auditor-internal-iso-14001` | Belum lulus | Hanya hero dan satu uraian generik. Perlu aspek/dampak lingkungan, kewajiban kepatuhan, pengendalian operasional, evaluasi kinerja, dan praktik audit. |
| `pelatihan-auditor-internal-iso-15189` | Belum lulus | Hanya hero dan satu uraian generik. Perlu konteks laboratorium medik, proses pemeriksaan, validitas hasil, risiko, dan bukti audit yang relevan. |
| `pelatihan-auditor-internal-iso-17025` | Belum lulus | Hanya hero dan satu uraian generik. Perlu konteks kompetensi laboratorium, metode, ketertelusuran metrologi, validitas hasil, dan bukti audit. |
| `pelatihan-auditor-internal-iso-22000` | Belum lulus | Hanya hero dan satu uraian generik. Perlu konteks keamanan pangan, HACCP, PRP, bahaya, traceability, dan contoh pemeriksaan. |
| `pelatihan-auditor-internal-iso-22301` | Belum lulus | Hanya hero dan satu uraian generik. Perlu konteks business continuity, analisis dampak bisnis, strategi, latihan, dan evaluasi kesiapan. |
| `pelatihan-auditor-internal-iso-27001` | Belum lulus | Hanya hero dan satu uraian generik. Perlu konteks ISMS, penilaian risiko, SoA, kontrol, bukti, dan praktik audit keamanan informasi. |
| `pelatihan-auditor-internal-iso-45001` | Belum lulus | Hanya hero dan satu uraian generik. Perlu konteks bahaya, risiko K3, hierarki pengendalian, konsultasi pekerja, dan bukti audit. |
| `pelatihan-auditor-internal-iso-50001` | Belum lulus | Hanya hero dan satu uraian generik. Perlu konteks tinjauan energi, EnPI, EnB, data energi, dan bukti audit sistem manajemen energi. |
| `pelatihan-auditor-internal-iso-9001` | Bersyarat | Telah diremediasi dengan tujuan audit, siklus, bukti objektif, temuan, kompetensi, FAQ, dan tautan jadwal. Detail penyelenggaraan yang belum tersedia dinyatakan secara terbuka dan tidak direka. |
| `pelatihan-internal-auditor-migrasi-iso-14001` | Belum lulus | Hanya hero dan satu uraian generik. Perlu dibedakan jelas antara pelatihan audit internal dan pelatihan pemahaman perubahan edisi; materi transisi harus didukung sumber resmi dan silabus. |

**Ringkasan pelatihan:** 2 bersyarat, 12 belum lulus.

Pola yang paling berisiko adalah halaman program yang menyebut "administrasi sertifikasi" seolah pelatihan auditor internal menerbitkan sertifikat sistem manajemen organisasi. Halaman harus membedakan:
- bukti keikutsertaan/penyelesaian pelatihan;
- penilaian kompetensi individu;
- kualifikasi atau sertifikasi personel oleh skema yang berwenang; dan
- sertifikasi sistem manajemen organisasi.

Jangan menyiratkan keempat hal tersebut setara.

### 3.4 Halaman umum dan topik CSMS — 16 URL

| Halaman | Status | Temuan |
|---|---|---|
| `0010-halaman-about-us` | Bersyarat | Tujuan halaman jelas, tetapi deskripsi organisasi masih umum. Tambahkan identitas badan usaha, alamat, struktur tanggung jawab, pengalaman, dan kredensial hanya setelah bukti disetujui. |
| `0020-halaman-home` | Lulus | Berfungsi sebagai pengarah ke layanan, artikel, dan konten utama. Tidak perlu dipaksa menjadi artikel panjang. Pastikan teks hero dan kartu benar-benar menjelaskan cakupan situs. |
| `0021-halaman-services` | Lulus | Halaman katalog layanan; fungsi utamanya menemukan layanan yang relevan. Nilai dari kejelasan label, ringkasan, navigasi, dan empty state, bukan jumlah paragraf. |
| `0022-halaman-csms` | Bersyarat | Halaman pilar menjelaskan CSMS, elemen, area penilaian, dan relasi dengan ISO 45001. Perlu memperjelas sumber/otoritas sembilan elemen: persyaratan CSMS dapat berbeda menurut pemilik proyek atau pemberi kerja. |
| `0023-halaman-trainings` | Lulus | Katalog program pelatihan dan jadwal terdekat. Pastikan kartu program mengarah ke halaman yang berisi informasi keputusan peserta. |
| `0024-halaman-schedules` | Lulus | Halaman jadwal memisahkan data acara dari deskripsi program. Pastikan status, tanggal, metode, lokasi, biaya, kuota, dan tautan pendaftaran hanya tampil jika tersedia dan telah diverifikasi. |
| `0025-halaman-articles` | Lulus | Halaman arsip artikel; kualitasnya bergantung pada navigasi, ringkasan, urutan, pagination, dan relevansi artikel. |
| `0026-halaman-csms-kepemimpinan-komitmen` | Belum lulus | Uraian generik dan section bukti yang terlalu singkat. Perlu indikator komitmen manajemen, alokasi sumber daya, tinjauan, dan contoh bukti yang tidak mengklaim sebagai persyaratan universal. |
| `0027-halaman-csms-kebijakan-sasaran` | Belum lulus | Perlu contoh hubungan kebijakan, sasaran terukur, program kerja, pemantauan, dan bukti persetujuan/revisi. |
| `0028-halaman-csms-organisasi-tanggungjawab` | Belum lulus | Perlu pemetaan peran, kewenangan, koordinasi pemberi kerja-kontraktor, kompetensi, dan alur eskalasi. |
| `0029-halaman-csms-manajemen-risiko` | Belum lulus | Perlu alur identifikasi bahaya, penilaian risiko, hierarchy of controls, JSA/JHA bila sesuai, perubahan pekerjaan, dan verifikasi kontrol. |
| `0030-halaman-csms-perencanaan-prosedur` | Belum lulus | Perlu contoh perencanaan pekerjaan, izin kerja, metode kerja aman, koordinasi SIMOPS bila relevan, dan kontrol perubahan. |
| `0031-halaman-csms-implementasi-pemantauan` | Belum lulus | Perlu penjelasan implementasi pengendalian, inspeksi lapangan, toolbox meeting, pengawasan, pelaporan, dan tindak lanjut. |
| `0032-halaman-csms-audit-tinjauan` | Belum lulus | Perlu program audit, kriteria, bukti, pelaporan, tinjauan manajemen, dan verifikasi tindakan. |
| `0033-halaman-csms-pencapaian-kinerja` | Belum lulus | Perlu indikator leading/lagging yang didefinisikan, denominator, periode, kualitas data, analisis tren, dan batas interpretasi statistik insiden. |
| `0034-halaman-csms-pencapaian-lainnya` | Belum lulus | Ruang lingkup "pencapaian lainnya" terlalu kabur. Tetapkan contoh yang relevan, kriteria penerimaan, bukti, dan cara membedakannya dari delapan elemen inti. |

**Ringkasan halaman umum/topik CSMS:** 5 lulus, 2 bersyarat, 9 belum lulus.

Sembilan topik CSMS menggunakan deskripsi umum yang berulang mengenai area peninjauan dan dokumen yang diperiksa. Ini menghasilkan kesan halaman berbeda tetapi nilai informasinya hampir sama. Setiap halaman perlu memiliki pertanyaan pengguna, bukti, contoh, dan batas ruang lingkup yang khas.

### 3.5 Katalog layanan bahasa Inggris — 1 URL

| URL | Status | Temuan |
|---|---|---|
| `/en/services/` | Lulus | Halaman katalog programatis menyajikan hero dan daftar layanan berbahasa Inggris dari collection. Nilainya adalah navigasi dan discovery; tidak perlu menambah teks panjang yang mengulang halaman layanan. |

## 4. Prioritas remediasi

### P0 — sebelum menyatakan QG-12 lulus

1. Kembangkan 12 halaman training yang masih berupa hero + satu section generik. Jangan menyalin struktur FSSC 22000 secara mekanis; isi harus spesifik pada standar dan program yang benar-benar diselenggarakan.
2. Kembangkan sembilan halaman topik CSMS agar setiap topik punya substansi, contoh, bukti, dan batas penerapan sendiri.
3. Kembangkan artikel 0004, 0005, 0006, dan 0008. Hapus kutipan yang tidak memiliki sumber.
4. Pastikan klaim pelatihan, sertifikasi, akreditasi, dan kompetensi tidak mencampuradukkan pelatihan personel dengan sertifikasi sistem organisasi.

### P1 — perbaikan identitas dan bukti

1. Putuskan penanganan slug/translationKey artikel 0002, 0007, dan 0009 yang masih menyebut ISO 9001:2015. Periksa backlink/traffic sebelum perubahan URL dan buat redirect jika URL berubah.
2. Kumpulkan bukti internal organisasi untuk halaman About dan seluruh layanan: identitas legal, kewenangan, status akreditasi, ruang lingkup, badan penerbit sertifikat, kompetensi, dan proses layanan. Publikasikan hanya klaim yang terbukti dan disetujui.
3. Tetapkan reviewer teknis per domain: mutu, K3, lingkungan, keamanan pangan, laboratorium, energi, keamanan informasi, dan CSMS.
4. Untuk jadwal pelatihan, pastikan informasi acara sinkron dengan halaman program dan status pendaftaran aktual.

### P2 — tata kelola editorial berkelanjutan

1. Tambahkan pemilik konten dan reviewer pada workflow editorial internal.
2. Simpan sumber primer, tanggal verifikasi, dan catatan perubahan untuk setiap klaim standar atau transisi.
3. Lakukan audit ulang setelah remediasi, bukan hanya memeriksa jumlah kata.
4. Terapkan noindex/draft untuk program yang belum memiliki informasi minimum dan belum siap ditawarkan.

## 5. Batas dan kehati-hatian

- Audit ini tidak menyatakan bahwa TNV/Intiprima memiliki atau tidak memiliki akreditasi tertentu. Bukti tersebut tidak dapat dipastikan dari file konten.
- Daftar sembilan elemen CSMS tidak boleh dipresentasikan sebagai standar nasional tunggal jika sumber sebenarnya adalah kriteria perusahaan/pemilik proyek.
- Contoh kasus pada artikel hasil remediasi dinyatakan sebagai ilustrasi, bukan pengalaman klien atau data produksi aktual.
- ISO/IAF/Global ACI facts perlu diperiksa kembali terhadap sumber resmi ketika ada perubahan standar, aturan transisi, atau skema.
- Tidak ada target jumlah kata minimum. Halaman yang memenuhi intent dapat tetap ringkas; halaman yang tipis tidak menjadi baik hanya karena diperpanjang.

## 6. Hubungan dengan Quality Gates

QG-12 merupakan gate editorial dengan kebutuhan review manusia. CI dapat memeriksa kontrak frontmatter, struktur heading, metadata, link, serta aturan teknis lain, tetapi tidak dapat menyetujui akurasi teknis, bukti kompetensi, klaim akreditasi, atau manfaat konten bagi pembaca tanpa peninjau yang kompeten.

QG-13 telah menguji route, sitemap, canonical, navigasi, breadcrumb, redirect, keluarga route, serta sejumlah kebijakan listing melalui test suite. Kelulusan QG-13 tidak menggantikan kelulusan QG-12.

## 7. Status setelah remediasi awal

Tiga halaman yang sebelumnya dipilih untuk remediasi telah diperbarui:
- `0001-posisi-kualitas-sebagai-talenta-kompetitif`;
- `0003-mengendalikan-risiko-kualitas-di-pabrik`;
- `pelatihan-auditor-internal-iso-9001`.

Perubahan telah dikirim ke branch `main` pada commit `839da551f2d492f2d14188e298c81e0e35779133`. Pemeriksaan CI untuk commit ini perlu berstatus sukses sebelum remediasi awal dinyatakan tervalidasi. Dua halaman artikel sudah mendapat materi yang lebih aplikatif; halaman training secara sengaja menyatakan rincian penyelenggaraan yang belum tersedia dan menghindari klaim sertifikat kompetensi.

Audit penuh ini menetapkan backlog yang tersisa; belum ada perubahan massal pada 25 halaman berstatus belum lulus.
