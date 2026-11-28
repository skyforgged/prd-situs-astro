# Catatan Review Standar PRD Situs Astro

> Tanggal tindak lanjut: 2026-11-26, diperbarui 2026-11-28
> Commit awal yang ditinjau: `70c9469`
> Status: seluruh 12 temuan telah ditindaklanjuti, ditambah 3 koreksi lanjutan dan 2 koreksi integrasi editorial pada 2026-11-26; tindak lanjut Content Contract 1.4 dan koreksi 1.5 pada 2026-11-27 serta penyelarasan bukti pada 2026-11-28 tercatat di bawah.

## Ringkasan

| Kelompok | Item | Status |
|---|---:|---|
| Baseline S1–S4 | 4 | Dipertahankan |
| P0 — Kebenaran aturan | 3 | Selesai |
| P1 — Kelengkapan kontrak | 5 | Selesai dengan klarifikasi |
| P2 — Kerapian repository | 4 | Selesai |

## Keputusan penting selama tindak lanjut

1. Keunikan global hanya berlaku untuk **ID dokumen konten**. ID block tetap unik lokal dalam dokumen pemilik.
2. Timestamp memakai ISO 8601 UTC presisi detik (`YYYY-MM-DDTHH:mm:ssZ`). Timestamp tidak diwajibkan unik; identitas unik adalah ID dokumen. `updatedDate` harus sama dengan atau lebih baru dari `publishedDate`.
3. FAQ, testimoni, tim, dan jenis konten lain bukan fitur wajib setiap situs. Jika suatu proyek menggunakannya sebagai entitas konten, kontraknya harus didefinisikan sebelum digunakan.
4. Relasi yang menunjuk Author/Person atau Organization/Provider hanya dapat digunakan setelah kontrak target tersedia.
5. `seo` memiliki kontrak bersama dengan fallback ke `title` dan `description` dokumen. Detail nested yang bergantung pada implementasi harus ditetapkan dalam arsitektur proyek.

## P0 — Kebenaran aturan

### P0-1. ID dokumen global dan ID block lokal
- [x] Selesai. Constitution 1.2 membatasi keunikan global pada ID dokumen konten dan memisahkan validasi ID block.
- Bukti: `constitution/WEBSITE-CONSTITUTION.md:48`, `:147`, `:175`; `content-contract/CONTENT-CONTRACT.md:28`; `quality/QUALITY-GATES.md:75`.
- Verifikasi ulang 2026-11-26: bunyi lama "seluruh ID numerik" pada quality gate sudah diganti dan tidak ditemukan lagi oleh pencarian teks.

### P0-2. Format dan aturan timestamp
- [x] Selesai. Format UTC presisi detik ditetapkan; timestamp tidak harus unik; `updatedDate >= publishedDate`.
- Bukti: Constitution bagian Metadata dan media; Content Contract bagian Aturan waktu dan Schema.org.

### P0-3. Definisi relasi
- [x] Selesai. Matriks relasi menyebut sumber, target, kardinalitas, status, dan perilaku jika target tidak ditemukan. `author` diperjelas menjadi `authorId` numerik.
- Bukti: `content-contract/CONTENT-CONTRACT.md`, bagian Matriks relasi dan kontrak Article/Service.

## P1 — Kelengkapan kontrak

### P1-1. Kontrak objek SEO
- [x] Selesai. Objek `seo` memiliki field, tipe, fallback, dan aturan canonical.
- Bukti: `content-contract/CONTENT-CONTRACT.md`, bagian Kontrak objek bersama.

### P1-2. Definisi field yang sebelumnya hanya dicontohkan
- [x] Selesai. Struktur `featuredImage` didefinisikan. Aturan menu menetapkan tepat satu dari `pageId` atau `url`, serta batas penggunaan `external`.
- Bukti: `content-contract/CONTENT-CONTRACT.md:79`, `:89`, `:93`, `:398-409`.
- Verifikasi ulang 2026-11-26: kalimat lama tentang batas kedalaman yang ditentukan proyek sudah diganti; enum `location` kini memuat `utility` di tabel dan di narasi.

### P1-3. FAQ, testimoni, dan tim
- [x] Selesai dengan klarifikasi. Constitution menyatakan jenis tersebut hanya wajib berbasis Markdown apabila digunakan; bukan fitur wajib semua situs. Kontrak jenis baru wajib dibuat sebelum digunakan.
- Bukti: `constitution/WEBSITE-CONSTITUTION.md`, bagian Sumber konten; `content-contract/CONTENT-CONTRACT.md`, bagian Kontrak yang belum didefinisikan.

### P1-4. Dokumen arsitektur yang dirujuk
- [x] Selesai. Technical Architecture dan Quality Gates telah dibuat dan ditautkan dari README.
- Bukti: `architecture/TECHNICAL-ARCHITECTURE.md`, `quality/QUALITY-GATES.md`, `README.md`.

### P1-5. FAQPage dan HowTo
- [x] Selesai. Contoh dinyatakan sebagai ilustrasi semantik, bukan jaminan kelayakan rich result; kebijakan mesin pencari harus diperiksa saat implementasi.
- Bukti: Constitution bagian Schema.org; Content Contract bagian Aturan waktu dan Schema.org.

## P2 — Kerapian repository

### P2-1. Konten dan label UI
- [x] Selesai. Batas konten substantif dan label UI generik dijelaskan dengan contoh.
- Bukti: `constitution/WEBSITE-CONSTITUTION.md`, bagian Sumber konten dan batas pengecualian; Architecture bagian Konfigurasi UI dan konten.

### P2-2. Role System Analyst
- [x] Selesai. Placeholder niche dan typo heading dihilangkan; standar wajib, lokasi output, dan prinsip analisis ditambahkan. README menautkan LICENSE.
- Bukti: `ROLE-SYSTEM-ANALYST.md`, `README.md`.

### P2-3. AGENTS.md
- [x] Selesai. Instruksi kerja agen, dokumen yang wajib dibaca, dan aturan perubahan standar ditambahkan.
- Bukti: `AGENTS.md`.

### P2-4. Pencatatan perubahan standar
- [x] Selesai. `CHANGELOG.md` dibuat dengan tanggal, perubahan, alasan, dampak, dan catatan kompatibilitas.
- Bukti: `CHANGELOG.md`.

## Tambahan: kerangka frontmatter untuk agen AI

- [x] Ditambahkan `content-contract/FRONTMATTER-TEMPLATES.md` berisi kerangka field kosong untuk Homepage, Menu, Page, Article, Service, dan Category.
- [x] Content Contract 1.3 dan README menautkan template; `AGENTS.md` mewajibkan agen membacanya sebelum membuat atau merevisi dokumen konten.
- Bukti: `content-contract/FRONTMATTER-TEMPLATES.md`, `content-contract/CONTENT-CONTRACT.md`, `AGENTS.md`, dan `README.md`.

## Koreksi lanjutan 2026-11-26

- [x] Quality gate pada konstitusi diselaraskan dengan keputusan ID dokumen global dan ID block lokal.
  - Bukti: `constitution/WEBSITE-CONSTITUTION.md:4`, `:147`; `CHANGELOG.md` bagian Fixed.
  - Verifikasi: pencarian teks "seluruh ID numerik" tidak mengembalikan kecocokan; `quality/QUALITY-GATES.md:75` masih menyatakan block ID 1 di dua dokumen berbeda lulus.
- [x] Aturan menu disatukan menjadi satu bunyi, termasuk enum `location` dan kedalaman maksimal.
  - Bukti: `content-contract/CONTENT-CONTRACT.md:79`, `:89`, `:93`.
  - Verifikasi: pencarian teks "batas kedalaman yang ditentukan proyek" tidak mengembalikan kecocokan; `utility` tercantum di narasi dan tabel.
- [x] Penomoran subjudul objek bersama diperbaiki dan rujukan versi template diselaraskan.
  - Bukti: `content-contract/CONTENT-CONTRACT.md:383`, `:398`; `content-contract/FRONTMATTER-TEMPLATES.md:4-5`.
  - Verifikasi: subjudul kini bernomor 13.1 dan 13.2 di bawah Bab 13; template menyatakan mengikuti Content Contract 1.3.

## Batas verifikasi

Perubahan diverifikasi dengan membaca ulang isi file dan pencarian teks terhadap frasa lama. Repository ini belum memiliki `package.json`, implementasi validator, atau test runner; karena itu belum ada klaim bahwa quality gates telah dijalankan sebagai automated tests. Quality Gates saat ini mendefinisikan kriteria penerimaan yang harus diimplementasikan dan dijalankan pada setiap proyek Astro.

## Tindak lanjut standar editorial 2026-11-26

- [x] Ditambahkan `quality/CONTENT-QUALITY-STANDARD.md` sebagai acuan kualitas editorial lintas jenis halaman.
- [x] Ditegaskan bahwa Google tidak menetapkan preferred word count; panjang konten mengikuti tujuan halaman, kompleksitas, dan kebutuhan pembaca.
- [x] Ditambahkan QG-12 untuk review editorial manusia/ahli, tanpa menjadikan jumlah kata sebagai syarat otomatis.
- [x] `README.md`, `AGENTS.md`, dan `ROLE-SYSTEM-ANALYST.md` ditautkan ke standar editorial.
- Bukti: `quality/CONTENT-QUALITY-STANDARD.md`, `quality/QUALITY-GATES.md`, `README.md`, `AGENTS.md`, dan `ROLE-SYSTEM-ANALYST.md`.
- Batas verifikasi: dokumen standar dan tautan telah diperbarui; belum ada validator atau test runner repository untuk menjalankan gate otomatis. QG-12 memang merupakan review editorial yang harus dicatat oleh reviewer.

## Koreksi integrasi editorial 2026-11-26

- [x] Aturan CI dibedakan dari review editorial QG-12.
  - Bukti: `quality/QUALITY-GATES.md:68`, `:120`, versi 0.6 pada `:4`.
  - Verifikasi: teks "Semua gate harus dijalankan" sudah diganti; QG-01 sampai QG-11 disebut sebagai gate otomatis, QG-12 sebagai persetujuan reviewer sebelum rilis.
- [x] Baris dokumen utilitas tidak lagi menyamakan menu dan navigasi dengan halaman.
  - Bukti: `quality/CONTENT-QUALITY-STANDARD.md:110`, versi 1.1 pada `:4`.
  - Verifikasi: tabel kini memakai label "Dokumen utilitas (homepage, menu, navigasi)".
- Bukti pendukung: `CHANGELOG.md` bagian Fixed, Rationale and impact, serta Compatibility.
- Batas verifikasi: perubahan ini hanya verifikasi baca dan pencarian teks. Belum ada reviewer nyata atau CI yang menjalankan gate karena repo ini tidak memiliki implementasi validator.

## Analisis pola situs referensi 2026-11-26

- [x] Pola artikel 1–3, artikel 4–6, footer dinamis, CTA layanan/WhatsApp, dan pagination dicatat dalam berkas analisis tersendiri.
  - Bukti: `docs/ANALISIS-POLA-SITUS.md`; tautan di `README.md:20`.
  - Verifikasi: lima repo dibaca via GitHub API dan `raw.githubusercontent.com`; `skyforgged/konsultan-slf` dipakai sebagai rujukan utama, empat repo `arisciwek/*` sebagai pembanding.
- [x] Temuan dibedakan menjadi fakta implementasi, bagian yang sudah tercakup standar, bagian yang belum diatur, dan saran non-normatif.
  - Bukti: `docs/ANALISIS-POLA-SITUS.md` bagian 2, 4, dan 5.
  - Verifikasi: tidak ada versi dokumen standar yang diubah; sesuai `AGENTS.md`, pola referensi tidak dijadikan kewajiban global tanpa dasar Constitution.
- Batas verifikasi: analisis hanya membaca kode, tanpa build, validator, atau test runner. Klaim "pola ada di setiap repo" tidak diterima apa adanya; tiga dari lima pola ternyata tidak konsisten lintas repo.

## Tindak lanjut standar sebelum penyusunan IA

1. Implementasikan validator sesuai `architecture/TECHNICAL-ARCHITECTURE.md` dan `quality/QUALITY-GATES.md` pada proyek Astro pertama yang mengadopsi standar.
2. Saat implementasi, validasi ulang detail schema nested SEO dan semua jenis relasi yang benar-benar dipakai proyek.
3. Terapkan QG-12 sebagai review editorial pada konten nyata dan evaluasi apakah checklist perlu penyesuaian menurut jenis situs.
4. Tambahkan ADR jika keputusan arsitektur baru berdampak lintas proyek.

## Content Architecture & IA 2026-11-26

- [x] Ditambahkan `architecture/CONTENT-AND-INFORMATION-ARCHITECTURE.md` versi 0.1.
- [x] Dokumen menetapkan prinsip pemetaan kebutuhan pengguna, tujuan halaman, kelompok topik, relasi konten, navigasi, URL/canonical, internal linking, listing/pagination, halaman lokal, CTA, dan lifecycle.
- [x] Pola yang tidak universal—jumlah halaman/kata/tautan, pagination, footer, CTA/WhatsApp, dan halaman lokasi—ditegaskan sebagai keputusan proyek.
- Bukti: `architecture/CONTENT-AND-INFORMATION-ARCHITECTURE.md`, tautan pada `README.md`, dan entri `CHANGELOG.md`.
- Batas verifikasi: dokumen baru telah ditulis dan ditautkan; belum diuji terhadap proyek implementasi Astro karena repository standar ini tidak memiliki situs aplikasi, validator, atau test runner.

## Langkah lanjutan

1. Selesai: audit konsistensi silang antara Constitution, Content Contract, Technical Architecture, Content & Information Architecture, dan Quality Gates (lihat "Audit konsistensi silang 2026-11-26").
2. Selesai: kriteria IA yang dapat diuji diturunkan menjadi QG-13, tanpa memaksakan keputusan proyek menjadi aturan universal (lihat `quality/QUALITY-GATES.md` 0.4).
3. Selesai: template dokumen proyek untuk sitemap, intent map, matriks relasi, internal linking, dan keputusan route disiapkan (lihat "Project Architecture Templates 2026-11-26").
4. Implementasikan validator sesuai Technical Architecture pada proyek Astro pertama yang mengadopsi standar.
5. Terapkan QG-12 sebagai review editorial pada konten nyata dan evaluasi checklist berdasarkan jenis situs.
6. Tambahkan ADR jika keputusan arsitektur baru berdampak lintas proyek.


## Audit konsistensi silang 2026-11-26

### Temuan dan keputusan

| ID | Temuan | Keputusan/tindakan |
|---|---|---|
| IA-01 | Content & Information Architecture belum tercantum dalam hierarki otoritas Constitution. | Selesai: Constitution 1.3 menempatkan IA setelah Content Contract dan sebelum Technical Architecture. |
| IA-02 | Constitution mewajibkan mekanisme pencatatan/validasi ID global, sedangkan Technical Architecture menyebut registry boleh dipelihara. | Selesai: Technical Architecture 0.2 menegaskan mekanisme wajib; bentuk registry/validator tetap fleksibel. |
| IA-03 | Technical Architecture belum meminta artefak intent map, sitemap, matriks relasi, navigasi, internal linking, listing, kebijakan lokal, dan CTA. | Selesai: daftar keputusan sebelum implementasi diperluas agar selaras dengan dokumen IA. |
| IA-04 | Quality Gates belum memiliki gate khusus untuk menguji kesesuaian implementasi dengan keputusan IA. | Selesai: QG-13 ditambahkan untuk route manifest/sitemap, navigasi, breadcrumb, listing, dan indexability. |
| IA-05 | QG-13 berisiko menilai relevansi semantik secara otomatis. | Diklarifikasi: QG-13 hanya menguji konsistensi terstruktur; intent dan relevansi kontekstual tetap ditinjau manusia melalui QG-12. |

### Pemeriksaan konsistensi yang tidak memerlukan perubahan

- ID dokumen global dan ID block lokal konsisten pada Constitution, Content Contract, Technical Architecture, template frontmatter, dan Quality Gates.
- Schema utama dokumen wajib, sedangkan schema block opsional; contoh dan aturan rendering tidak mewajibkan JSON-LD per block.
- Field relasi numerik dan kardinalitas dijabarkan dalam Content Contract; Technical Architecture menjelaskan indeks dan validasinya.
- Timestamp UTC presisi detik, updatedDate tidak lebih awal dari publishedDate, serta timestamp yang tidak harus unik konsisten pada dokumen terkait.
- Field SEO nested yang belum ditetapkan secara universal tetap menjadi keputusan implementasi proyek; Technical Architecture meminta schema nested eksplisit dan menolak properti bebas.
- Panjang konten bukan target universal; QG-12 menggunakan review editorial dan Content Quality Standard.
- Jenis halaman lokal, FAQ, testimoni, tim, pagination, footer, dan CTA tidak otomatis wajib bagi semua situs.

### Batas dan tindak lanjut

- [x] Baca ulang Constitution, Content Contract, Technical Architecture, Content & Information Architecture, Quality Gates, Content Quality Standard, Frontmatter Templates, dan AGENTS.
- [x] Perbaiki hierarki standar, kewajiban mekanisme ID global, daftar keputusan IA pra-implementasi, dan gate konsistensi IA.
- [ ] Implementasikan QG-13 pada proyek Astro yang mengadopsi standar dan uji dengan fixture valid/tidak valid.
- [x] Siapkan template artefak proyek: intent map, sitemap/route manifest, matriks relasi, navigasi/breadcrumb, internal linking, listing/pagination, local coverage, dan CTA. Bukti: bagian "Project Architecture Templates 2026-11-26" di bawah.
- [ ] Audit ulang kontrak berdasarkan implementasi pertama; khususnya field yang masih membutuhkan kontrak entitas target (Author/Person dan Organization/Provider).

### Bukti perubahan

- constitution/WEBSITE-CONSTITUTION.md 1.3
- architecture/TECHNICAL-ARCHITECTURE.md 0.2
- quality/QUALITY-GATES.md 0.4
- CHANGELOG.md

### Batas verifikasi

Perubahan standar telah diperbarui melalui GitHub dan dibaca ulang. Repository ini tidak memiliki aplikasi Astro, package.json, validator, atau test runner; karena itu QG-13 dan gate lainnya belum dijalankan sebagai automated tests.


## Project Architecture Templates 2026-11-26

- [x] Dibuat paket template proyek pada projects/_template/.
- [x] Paket mencakup Project Brief, Information Architecture (intent map, sitemap/route manifest, navigasi, breadcrumb, internal linking), Content Model & Relation Matrix, Listing & Conversion, Local Coverage, Content Governance, Technical Architecture Decisions, dan ADR template.
- [x] README repository dan AGENTS.md ditautkan ke paket; instruksi agen membedakan template proyek dari standar universal.
- [x] Template menggunakan placeholder eksplisit dan meminta bagian yang tidak relevan diberi status Tidak berlaku beserta alasan.
- Bukti: projects/_template/README.md dan seluruh file template di direktori tersebut; README.md; AGENTS.md; CHANGELOG.md.
- Batas verifikasi: file dibuat melalui GitHub Contents API pada branch default. Belum ada proyek Astro yang mengadopsi template ini, sehingga belum dilakukan uji penerapan terhadap implementasi, validator, atau CI.

### Penilaian hasil

Paket ini menutup tindak lanjut dokumentasi yang meminta template artefak proyek. Template sengaja memisahkan keputusan IA, model konten, dan keputusan teknis; tidak menggabungkannya menjadi satu dokumen raksasa. Tahap berikutnya adalah mengadopsinya pada satu proyek Astro nyata, menguji apakah kolom dan artefaknya cukup, lalu memperbaiki template berdasarkan temuan implementasi.


## Project Initialization Workflow 2026-11-26

- [x] Ditambahkan projects/_template/PROJECT-INITIALIZATION-WORKFLOW.md versi 0.1.
- [x] Workflow memuat 10 phase: Repository & Standard Onboarding; Project Discovery & Brief; Research & Evidence; Intent Mapping & Page Opportunity; Content Modeling & Content Contract; Information Architecture & Route Design; Content Experience & Editorial Specification; Technical Architecture; PRD & Acceptance Criteria; Implementation Readiness Review.
- [x] Setiap phase memiliki tujuan, masukan, pekerjaan, keluaran, dan gate/acceptance checklist.
- [x] Ditambahkan status workflow, aturan iterasi, aturan kerja AGENT AI, format laporan phase, serta relasi phase dengan template dokumen.
- [x] README root, README template, AGENTS.md, dan CHANGELOG.md ditautkan/diperbarui.
- Bukti: projects/_template/PROJECT-INITIALIZATION-WORKFLOW.md; projects/_template/README.md; README.md; AGENTS.md; CHANGELOG.md.
- Batas verifikasi: file dan integrasi dokumentasi diperiksa dengan pembacaan ulang setelah penulisan. Belum diuji pada repository situs Astro nyata, belum ada simulasi agent end-to-end, dan tidak ada automated test runner pada repository standar.

### Penilaian

Workflow menutup kesenjangan antara starter templates dan proses pemakaiannya. Gate akhir tidak otomatis lulus hanya karena file dokumen tersedia; kesiapan memerlukan kualitas isi, bukti, keputusan, dan persetujuan. Tahap evaluasi berikutnya adalah menerapkan workflow pada satu proyek Astro nyata dan mencatat friksi, pengulangan, serta keputusan yang belum tertampung.

## Koreksi dokumentasi setelah pull 2026-11-26

- [x] Versi paket template diselaraskan: `projects/_template/README.md:4` menjadi 0.2, mengikuti `projects/_template/README.md:66` dan entri Template Pack 0.2 di `CHANGELOG.md` (kini 0.3; lihat bagian 2026-11-27).
- [x] `projects/_template/TECHNICAL-ARCHITECTURE.md:66-67,95` memisahkan QG-12 dari gate otomatis sesuai `quality/QUALITY-GATES.md:120`; review editorial tidak lagi diwajibkan memiliki perintah dan fixture CI.
- [x] Checklist yang sudah dibuktikan pada `docs/REVIEW-NOTES.md:149-151,184` ditandai selesai dengan rujukan ke bagian yang memuat buktinya.
- [x] Rujukan baris diperbarui: `docs/ANALISIS-POLA-SITUS.md:19,117` mengarah ke `README.md:35`, dan `docs/REVIEW-NOTES.md:125` mengarah ke `README.md:20`.
- Bukti: perubahan pada empat berkas di atas, entri `Fixed — tindak lanjut pull 2026-11-26` di `CHANGELOG.md`, serta pemeriksaan tautan lokal Markdown tanpa tautan rusak.
- Batas verifikasi: koreksi hanya menyelaraskan metadata, pemetaan gate, dan rujukan; tidak ada aturan normatif baru. Repository tetap tidak memiliki aplikasi, `package.json`, validator, atau test runner sehingga tidak ada build/test yang dijalankan.

## Tindak lanjut Content Contract 1.4 2026-11-27

- [x] `intro` dipisahkan dari `description`/`seo.description` dan diwajibkan pada Page, Article, dan Service.
  - Bukti: `content-contract/CONTENT-CONTRACT.md:4` (versi 1.4 saat itu, kini 1.5), bagian kontrak halaman, artikel, dan layanan; `content-contract/FRONTMATTER-TEMPLATES.md:4` (versi 1.3 saat itu, kini 1.4), template yang bersangkutan dan checklist.
  - Verifikasi: tiga template memuat field `intro`; checklist memuat syarat paragraf pertama dan pola kalimat `DefinedTerm`.
- [x] Katalog tipe, Arsitektur tiga lapisan, Schema Registry, dan aturan graph ditambahkan ke Content Contract 1.4 dan dipertahankan pada 1.5.
  - Bukti: `content-contract/CONTENT-CONTRACT.md` bagian 16 sampai 19.
  - Verifikasi: entri registry mendefinisikan `schemaType`, `scope`, `fieldMapping`, `validationRules`, `googleRichResultSupport`, dan `mergeStrategy`; status Google memakai enum terkontrol.
- [x] Kewajiban Schema Registry diturunkan ke artefak proyek dan gate yang dapat diuji.
  - Bukti: `architecture/TECHNICAL-ARCHITECTURE.md:4` (versi 0.3) bagian 14; `projects/_template/TECHNICAL-ARCHITECTURE.md:4` (versi 0.2) bagian 1 dan 5; `projects/_template/README.md:4` (versi 0.3); `quality/QUALITY-GATES.md:4` (versi 0.6) QG-08 dan test matrix.
  - Verifikasi: pencarian "Schema Registry" menemukan kewajiban di kontrak konten, daftar keputusan pra-implementasi, template arsitektur proyek, dan kriteria QG-08.
- [x] Laporan TNV Certification ditandai sebagai snapshot sebelum revisi dan ditautkan dari README root.
  - Bukti: `projects/tnvcertification/CONTENT-CONTRACT-EVALUATION.md` bagian "Catatan status 2026-11-27"; `projects/tnvcertification/README.md`; `README.md`.
  - Verifikasi: laporan masih menyebut standar 1.3/1.2 sebagai objek yang diperiksa, dengan catatan tindak lanjut ke 1.5/1.4.
- [x] Rujukan baris yang bergeser diperbarui setelah penambahan field dan baris tabel.
  - Bukti: `docs/ANALISIS-POLA-SITUS.md:19,117` dan `docs/REVIEW-NOTES.md:232` kini mengarah ke `README.md:35`; `docs/REVIEW-NOTES.md:230` mengarah ke `projects/_template/TECHNICAL-ARCHITECTURE.md:66-67,95` dan `quality/QUALITY-GATES.md:120`; rujukan QG pada `docs/REVIEW-NOTES.md:28,90,114` diselaraskan dengan test matrix saat ini.
  - Verifikasi: pencarian rujukan baris lama tidak menemukan kecocokan di luar catatan ini.
- [x] `CHANGELOG.md` memperbarui versi, alasan, dampak, dan kompatibilitas untuk perubahan di atas.
  - Bukti: `CHANGELOG.md` bagian 2026-11-27.
  - Verifikasi: perubahan normatif pada dokumen standar dan template memiliki entri serta catatan kompatibilitas.
- Batas verifikasi: pemeriksaan dilakukan dengan membaca ulang isi dokumen, pencarian versi dan frasa kunci, serta pemeriksaan tautan lokal Markdown. Repository ini tidak memiliki aplikasi Astro, `package.json`, validator, atau test runner, sehingga tidak ada build, automated test, atau QG-08 yang dijalankan.

## Penyelarasan bukti setelah Content Contract 1.5 2026-11-28

- [x] Status dan versi dokumen diselaraskan.
  - Bukti: `docs/REVIEW-NOTES.md:3,5`; `content-contract/CONTENT-CONTRACT.md:4` (1.5); `content-contract/FRONTMATTER-TEMPLATES.md:4` (1.4); `quality/QUALITY-GATES.md:4` (0.6).
- [x] Rujukan CI diperbarui setelah test matrix QG-08 diperpanjang.
  - Bukti: `docs/REVIEW-NOTES.md:114,230,251` kini mengarah ke `quality/QUALITY-GATES.md:120`, bukan `:106` yang sekarang berisi kasus `DefinedTerm.description`.
- [x] Entri adopsi Content Contract 1.4 dipulihkan di `CHANGELOG.md`.
  - Bukti: `CHANGELOG.md` bagian 2026-11-27 `Added` memuat entri 1.4 dan 1.5; bagian 2026-11-28 mencatat pemulihannya.
- [x] Laporan TNV Certification mengikuti versi terbaru sebagai tindak lanjut, bukan sebagai objek snapshot.
  - Bukti: `projects/tnvcertification/CONTENT-CONTRACT-EVALUATION.md:5,11`; `:5` tetap 1.3/1.2 karena itulah objek yang diperiksa.
- [x] Contoh kelulusan QG-08 selaras dengan page-level type pada kontrak.
  - Bukti: `quality/QUALITY-GATES.md:99` dan `content-contract/CONTENT-CONTRACT.md:123`; yang diubah hanya contoh, bukan aturan.
- Bukti verifikasi: `git diff --check` bersih; pemeriksaan 27 berkas Markdown menemukan 0 tautan lokal rusak dan 0 code fence tidak seimbang; rujukan baris di atas dicek terhadap isi berkas tujuan.
- Batas verifikasi: tidak ada perubahan normatif, sehingga versi dokumen tidak dinaikkan. Repository ini tetap tidak memiliki aplikasi Astro, `package.json`, validator, atau test runner; tidak ada build, automated test, atau QG-08 yang dijalankan.


## Validator otomatis — Milestone 1 sampai 3, 2026-11-28

- [x] Milestone 1: fondasi parser frontmatter ketat dan invariant global.
- [x] Milestone 2: kontrak Homepage, Menu, Page, Article, Service, Category; fallback SEO dan validasi struktur dasar.
- [x] Milestone 3: resolusi FK lintas dokumen untuk relasi yang target collection-nya telah ditetapkan dalam Content Contract 1.5.
- [x] Relasi menu bertingkat, parent Page, kategori, artikel terkait, layanan terkait, serta referensi block `serviceIds` dan `content-list.categoryId` diperiksa keberadaan dan jenis targetnya.
- [x] ID target yang tidak ditemukan atau ambigu ditolak; hierarki parent Page harus bebas siklus; self-reference relasi artikel/layanan ditolak.
- [x] `authorId` dan `providerId` ditolak bila diisi sampai kontrak Author/Person dan Organization/Provider tersedia, mengikuti matriks relasi Content Contract.
- Bukti: `scripts/validate_content.py`, `tests/test_validate_content.py`, `VALIDATOR-MILESTONE-3.md`.
- Verifikasi: GitHub Actions workflow `Validator Tests`, Python 3.12, **34 passed**; run [46097423874](https://github.com/skyforgged/prd-situs-astro/actions/runs/46097423874).
- Batas verifikasi: validasi properti block yang bersifat dinamis tetap menunggu Block Registry; relasi yang belum memiliki kontrak target tidak diaktifkan. CI ini menguji unit validator, bukan corpus konten situs Astro turunan secara penuh.

## Validator otomatis — Milestone 4 dan 5, 2026-11-28

- [x] Milestone 4: Schema Registry dan Block Registry awal, validasi tipe props, pasangan block-schema, dan pemeriksaan sumber wajib block tersedia; konsistensi penuh antara scope tipe dan entri registry masih perlu ditutup.
- [x] Fungsi Milestone 5: fungsi slug/route collision, canonical duplikat, aset lokal, internal links, route manifest, sitemap, dan redirect dasar tersedia serta memiliki unit test.
- [ ] Integrasi Milestone 5 ke CLI: belum selesai. `main()` pada kode yang diaudit hanya memanggil `validate_paths()`; fungsi validasi Milestone 5 lainnya belum dipanggil dari entry point.
- [ ] Pemakaian argumen Milestone 5: `--site-root`, `--route-manifest`, dan `--route-prefixes` sudah dideklarasikan tetapi belum digunakan oleh `main()` untuk menjalankan pemeriksaan terkait.
- [ ] Smoke-test CLI di CI: belum ada. Workflow `.github/workflows/validator-tests.yml` hanya menjalankan `pytest -q`.
- Bukti: `scripts/registries.py`, `scripts/validate_content.py`, `tests/test_validate_content.py`, `.github/workflows/validator-tests.yml`, `VALIDATOR-MILESTONE-4.md`, dan `VALIDATOR-MILESTONE-5.md`.
- Batas verifikasi: unit test fungsi tidak membuktikan integrasi CLI. Validator generik belum memeriksa graph JSON-LD hasil render, accessibility browser, production build Astro, atau kualitas editorial. QG-12 tetap manual; QG-08/QG-10/QG-11 harus dihubungkan pada workflow setiap proyek Astro.
