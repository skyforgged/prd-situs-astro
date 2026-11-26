# Changelog

Semua perubahan standar yang berdampak pada proyek turunan dicatat di sini.

## 2026-11-26

### Added
- Content Quality & Editorial Standard 1.0: menetapkan people-first content, kecukupan konten tanpa target jumlah kata, orisinalitas, akurasi, transparansi, dan review editorial.
- Blank frontmatter templates for Homepage, Menu, Page, Article, Service, and Category, with explicit agent usage instructions.
- Technical Architecture Specification untuk implementasi Astro.
- Quality Gates dan acceptance criteria.
- Instruksi repository untuk agen melalui `AGENTS.md`.

### Changed
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

### Rationale and impact
- Menghilangkan ambiguitas yang dapat menyebabkan validator salah menolak ID block yang sah.
- Membuat format waktu dan foreign key dapat diuji secara konsisten.
- Memisahkan aturan universal dari pilihan fitur setiap proyek.
- Menyediakan acuan teknis dan quality gates sebelum standar dipakai pada proyek turunan.
- Menyelaraskan teks aturan yang tertinggal dari rilis sebelumnya agar pembaca tidak menemukan dua bunyi yang bertentangan.
- Menghindari optimasi berbasis jumlah kata dan mengarahkan penilaian pada manfaat, kelengkapan proporsional, orisinalitas, serta akurasi.

### Compatibility
- Proyek turunan perlu memastikan timestamp frontmatter menggunakan UTC `YYYY-MM-DDTHH:mm:ssZ`.
- Relasi yang sebelumnya menggunakan objek bebas seperti `author` harus dimigrasikan ke ID numerik jika targetnya merupakan dokumen konten.
- Timestamp yang sama pada dua dokumen tetap valid; jangan menggunakannya sebagai primary key.
- Koreksi ini tidak mengubah perilaku yang dimaksud, hanya menyelaraskan teks aturan dengan keputusan yang sudah berlaku.