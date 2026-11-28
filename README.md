# PRD Situs Astro

Repository ini menyimpan standar reusable untuk analisis kebutuhan, perancangan, dan pengembangan situs berbasis Astro.

## Standar inti
- [Batas Kemampuan Standar dan Validator](docs/CAPABILITY-BOUNDARIES.md) — membedakan pemeriksaan yang benar-benar tersedia pada validator, aturan yang masih berupa kontrak, dan pekerjaan wajib proyek Astro turunan.
- Matriks traceability persyaratan PRD: [`docs/REQUIREMENTS-TRACEABILITY-MATRIX.md`](docs/REQUIREMENTS-TRACEABILITY-MATRIX.md) — pemetaan requirement ke dokumen normatif, aturan implementasi, test/verifikasi, dan acceptance criteria.


- [Website Constitution](constitution/WEBSITE-CONSTITUTION.md) — aturan universal lintas proyek.
- [Content Contract](content-contract/CONTENT-CONTRACT.md) — kontrak Markdown terpisah berdasarkan jenis konten.
- [Frontmatter Templates](content-contract/FRONTMATTER-TEMPLATES.md) — kerangka field kosong untuk enam jenis konten inti.
- [Training & Schedule Contract](content-contract/TRAINING-SCHEDULE-CONTRACT.md) — kontrak collection ekstensi untuk program pelatihan dan pelaksanaan/batch.
- [Training & Schedule Templates](content-contract/TRAINING-SCHEDULE-TEMPLATES.md) — kerangka field kosong untuk dokumen training dan schedule.
- [Technical Architecture](architecture/TECHNICAL-ARCHITECTURE.md) — panduan penerapan standar pada Astro.
- [Content & Information Architecture](architecture/CONTENT-AND-INFORMATION-ARCHITECTURE.md) — model konten, sitemap, navigasi, URL, internal linking, listing, halaman lokal, dan konversi.
- [Quality Gates](quality/QUALITY-GATES.md) — acceptance criteria dan verifikasi.
- [Content Quality Standard](quality/CONTENT-QUALITY-STANDARD.md) — standar kualitas editorial, kedalaman, akurasi, orisinalitas, dan people-first content.
- [Validator Milestone 1](VALIDATOR-MILESTONE-1.md) — fondasi parser dan invariant global.
- [Validator Milestone 2](VALIDATOR-MILESTONE-2.md) — validasi kontrak Homepage, Menu, Page, Article, Service, dan Category.
- [Validator Milestone 3](VALIDATOR-MILESTONE-3.md) — validasi FK lintas dokumen, target collection, kardinalitas, dan siklus relasi.
- [Validator Milestone 4](VALIDATOR-MILESTONE-4.md) — validasi Schema Registry, Block Registry, dan props komponen.
- [Validator Milestone 5](VALIDATOR-MILESTONE-5.md) — validasi route, aset, tautan, manifest IA, dan integrasi Quality Gates.
- [Project Collection Contract Extensions](docs/CONTRACT-EXTENSIONS.md) — mekanisme eksplisit untuk collection domain di luar enam kind inti.

## Instruksi dan analisis

- [AGENTS.md](AGENTS.md) — instruksi agen yang bekerja di repository.
- [Role System Analyst](ROLE-SYSTEM-ANALYST.md) — pedoman analisis dan penyusunan PRD.
- [Review Notes](docs/REVIEW-NOTES.md) — audit dan tindak lanjut standar.
- [Analisis Pola Situs Referensi](docs/ANALISIS-POLA-SITUS.md) — temuan artikel, footer, CTA, dan pagination dari repo rujukan; bukan aturan wajib.
- [Changelog](CHANGELOG.md) — riwayat perubahan standar.
- [License](LICENSE) — lisensi repository.

## Keputusan standar

1. ID dokumen konten unik secara global lintas collection; ID block unik lokal di dokumen pemilik.
2. Schema block opsional dan hanya digunakan bila relevan.
3. Kontrak Markdown dipisahkan berdasarkan jenis konten.
4. Timestamp konten memakai ISO 8601 UTC presisi detik; timestamp tidak harus unik.
5. Relasi pada enam collection inti menggunakan foreign key numerik dengan target dan kardinalitas eksplisit. Collection ekstensi secara default juga menggunakan FK numerik; natural key hanya menjadi pengecualian terdaftar melalui extension registry dengan targetField yang unik dan stabil. Satu relasi tidak boleh memiliki dua sumber kebenaran.

## Struktur pengembangan

Standar global berada di direktori `constitution/`, `content-contract/`, `architecture/`, dan `quality/`. Kebutuhan khusus setiap situs harus disimpan terpisah di bawah `projects/<nama-proyek>/` dan tidak boleh mengubah aturan universal secara diam-diam.

## Prinsip perubahan

Perubahan standar harus memperbarui versi dokumen terkait, mencatat alasan dan dampaknya di `CHANGELOG.md`, serta memperbarui bukti pada `docs/REVIEW-NOTES.md`.

## Project Architecture Templates

- [Project Architecture Templates](projects/_template/README.md) — starter pack dokumen proyek untuk brief, intent, sitemap/route, content model, relasi, navigasi, internal linking, listing, cakupan lokal, konversi, governance, dan keputusan teknis.

## Project initialization

- [Project Initialization Workflow](projects/_template/PROJECT-INITIALIZATION-WORKFLOW.md) — phase-gated process dari onboarding, discovery, riset, intent mapping, content modeling, IA, editorial dan technical architecture, PRD, hingga Implementation Readiness Review.
