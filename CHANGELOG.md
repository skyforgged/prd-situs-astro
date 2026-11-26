# Changelog

Semua perubahan standar yang berdampak pada proyek turunan dicatat di sini.

## 2026-11-26

### Added
- Content Quality & Editorial Standard 1.0: menetapkan people-first content, kecukupan konten tanpa target jumlah kata, orisinalitas, akurasi, transparansi, dan review editorial.
- Blank frontmatter templates for Homepage, Menu, Page, Article, Service, and Category, with explicit agent usage instructions.
- Technical Architecture Specification untuk implementasi Astro.
- Quality Gates dan acceptance criteria.
- Instruksi repository untuk agen melalui `AGENTS.md`.
- `docs/ANALISIS-POLA-SITUS.md`: catatan non-normatif berisi verifikasi pola artikel 1–3 dan 4–6, footer dinamis, CTA layanan/WhatsApp, serta pagination pada lima repo Astro rujukan.

### Changed
- AGENTS.md: mewajibkan agen membaca standar Content & Information Architecture saat menyusun sitemap, route, navigasi, internal linking, listing, atau konversi.
- Quality Gates 0.2: menambahkan QG-12 untuk review editorial manusia/ahli dan test case untuk konten repetitif, halaman lokasi duplikatif, serta verifikasi klaim.
- README, AGENTS.md, dan Role System Analyst: mengintegrasikan standar kualitas editorial ke alur kerja PRD dan publikasi.
- Content Contract 1.2: links the frontmatter templates and requires agents to consult them when creating content documents.
- Constitution 1.1: memperjelas bahwa keunikan global hanya berlaku untuk ID dokumen; ID block lokal per dokumen.
- Constitution 1.1: menetapkan timestamp ISO 8601 UTC presisi detik, relasi waktu publikasi/pembaruan, dan batas konten vs label UI.
- Constitution 1.1: menegaskan jenis konten opsional sesuai kebutuhan situs.
- Content Contract 1.1: menambahkan kontrak SEO, featured image, matriks relasi, dan aturan timestamp.
- Role System Analyst: menghapus placeholder dan menyelaraskan alur PRD dengan standar repository.
- README: memperbarui peta dokumen, keputusan standar, dan tautan lisensi.

### Fixed
- Constitution 1.2: daftar quality gate tidak lagi menyebut keunikan global untuk seluruh ID numerik; bunyi tersebut kini membatasi keunikan pada ID dokumen konten dan mengakui ID block lokal.
- Content Contract 1.3: aturan menu tidak lagi memuat dua versi batas kedalaman, enum `location` mencantumkan `utility`, dan subjudul objek bersama dinomori ulang sebagai 13.1 serta 13.2.
- Frontmatter Templates 1.2: rujukan versi diselaraskan dengan Content Contract 1.3.
- Quality Gates 0.3: QG-12 ditegaskan sebagai review manusia yang dibuktikan dengan catatan persetujuan; aturan CI dibatasi pada gate otomatis QG-01 sampai QG-11.
- Content Quality Standard 1.1: baris dokumen utilitas tidak lagi menyamakan menu dan navigasi dengan jenis halaman.

### Rationale and impact
- Menghilangkan ambiguitas yang dapat menyebabkan validator salah menolak ID block yang sah.
- Membuat format waktu dan foreign key dapat diuji secara konsisten.
- Memisahkan aturan universal dari pilihan fitur setiap proyek.
- Menyediakan acuan teknis dan quality gates sebelum standar dipakai pada proyek turunan.
- Menyelaraskan teks aturan yang tertinggal dari rilis sebelumnya agar pembaca tidak menemukan dua bunyi yang bertentangan.
- Menghindari optimasi berbasis jumlah kata dan mengarahkan penilaian pada manfaat, kelengkapan proporsional, orisinalitas, serta akurasi.
- Membedakan gate otomatis dari persetujuan editorial manusia agar CI tidak disangka dapat menggantikan review.

### Compatibility
- Proyek turunan perlu memastikan timestamp frontmatter menggunakan UTC `YYYY-MM-DDTHH:mm:ssZ`.
- Relasi yang sebelumnya menggunakan objek bebas seperti `author` harus dimigrasikan ke ID numerik jika targetnya merupakan dokumen konten.
- Timestamp yang sama pada dua dokumen tetap valid; jangan menggunakannya sebagai primary key.
- Koreksi ini tidak mengubah perilaku yang dimaksud, hanya menyelaraskan teks aturan dengan keputusan yang sudah berlaku.
- Proyek turunan perlu menyediakan tempat pencatatan persetujuan QG-12, misalnya checklist PR atau catatan publikasi.

### Added
- Content Architecture & Information Architecture 0.1: prinsip model konten, jenis halaman, kelompok topik, URL/canonical, internal linking, listing/pagination, halaman lokal, CTA, dan tata kelola konten.

### Changed
- README: menautkan Content & Information Architecture sebagai standar arsitektur konten dan IA.

### Rationale and impact
- Menetapkan kerangka IA yang menghubungkan kebutuhan pengguna, model konten, navigasi, route, internal linking, dan konversi tanpa menjadikan pola satu situs sebagai kewajiban universal.

### Compatibility
- Dokumen IA 0.1 berstatus draft. Setiap proyek tetap harus menetapkan sitemap, route, relasi, listing, pagination, footer, CTA, dan kebijakan lokalnya sendiri. Tidak ada jumlah halaman, kata, atau tautan yang diwajibkan secara global.


### Changed
- Website Constitution 1.3: memasukkan Content & Information Architecture ke hierarki acuan dan memperjelas bahwa mekanisme pencatatan/validasi ID global wajib tersedia.
- Technical Architecture 0.2: mewajibkan mekanisme ID registry/validator dan menambahkan keputusan IA yang harus ditetapkan sebelum implementasi.
- Quality Gates 0.4: menambahkan QG-13 untuk konsistensi artefak IA, sitemap, navigasi, breadcrumb, listing, dan indexability.

### Rationale and impact
- Mencegah ketidakjelasan otoritas antara standar IA dan spesifikasi teknis.
- Menutup perbedaan redaksi antara kewajiban ID global pada Constitution dan pilihan mekanisme pada Technical Architecture.
- Membuat keputusan IA yang sebelumnya hanya berupa dokumen perencanaan dapat diverifikasi pada implementasi situs.
- QG-13 hanya mengotomatisasi konsistensi yang dapat dinyatakan eksplisit; relevansi semantik dan perbedaan intent tetap memerlukan review manusia melalui QG-12.

### Compatibility
- Proyek yang mengadopsi standar harus memiliki mekanisme registry atau validator ID global, tidak cukup hanya menyatakan bahwa ID seharusnya unik.
- Proyek harus menyediakan artefak IA yang dapat diperiksa (misalnya sitemap/route manifest dan aturan listing). Tidak semua halaman wajib masuk menu utama atau memiliki jumlah tautan tertentu.
- QG-13 perlu diimplementasikan pada proyek Astro; repository standar ini belum memiliki aplikasi atau validator untuk menjalankannya.


### Added — Project Architecture Templates 0.1
- Paket template proyek di projects/_template/ untuk Project Brief, Information Architecture, Content Model & Relations, Listing & Conversion, Local Coverage, Content Governance, Technical Architecture, dan ADR.
- Panduan penggunaan membedakan template proyek dari standar universal serta mengizinkan bagian Tidak berlaku dengan alasan.

### Rationale and impact
- Mengubah daftar keputusan pra-implementasi dalam Content & Information Architecture dan Technical Architecture menjadi artefak kerja yang dapat disalin ke repository situs.
- Mengurangi keputusan implisit dan membantu agen AI/developer mencatat intent, route, relasi, navigasi, listing, konversi, cakupan lokal, governance, serta pilihan teknis secara konsisten.

### Compatibility
- Template tidak mengubah Constitution, Content Contract, atau Quality Gates dan tidak mewajibkan semua fitur.
- Proyek harus menghapus/menandai bagian yang tidak relevan hanya setelah menilai kebutuhan; keputusan dan field yang belum diketahui tidak boleh diisi dengan asumsi.
- Template 0.1 belum diuji terhadap implementasi situs Astro nyata; paket ini merupakan artefak dokumentasi, bukan validator.


### Added — Project Initialization Workflow 0.1 / Template Pack 0.2
- Ditambahkan projects/_template/PROJECT-INITIALIZATION-WORKFLOW.md dengan 10 phase dari repository onboarding hingga Implementation Readiness Review.
- Workflow menetapkan masukan, aktivitas, keluaran, acceptance gate, status, jalur iterasi, aturan AGENT AI, dan format laporan phase.
- README, AGENTS.md, dan panduan template ditautkan ke workflow.

### Rationale and impact
- Mengubah template dokumen menjadi proses kerja yang berurutan dan dapat diawasi.
- Mencegah agen memulai implementasi sebelum kebutuhan, bukti, model konten, IA, kontrak teknis, dan acceptance criteria cukup jelas.
- Memberi ruang iterasi: temuan baru dapat mengembalikan pekerjaan ke phase terdampak.

### Compatibility
- Workflow tidak menggantikan Constitution, Content Contract, IA, Technical Architecture, atau Quality Gates.
- Gate yang tidak relevan hanya boleh berstatus Not applicable dengan alasan dan persetujuan.
- Workflow 0.1 belum diuji melalui adopsi proyek Astro nyata; evaluasi setelah penerapan pertama tetap diperlukan.
