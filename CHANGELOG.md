# Changelog

## 2026-11-28 — Integrasi validator (3/5)

### Changed
- Menambahkan mode `--require-project-gates` yang mewajibkan `--site-root` dan `--route-manifest`, sehingga pemeriksaan aset/tautan dan manifest IA tidak dapat terlewat dalam validasi penerimaan proyek.
- Mempertahankan mode parsial untuk diagnosis, tetapi outputnya memberi peringatan eksplisit bila QG-09 atau QG-13 tidak dijalankan.
- Output CLI merinci gate otomatis yang benar-benar dijalankan dan menegaskan bahwa accessibility hasil render (QG-10), production build Astro (QG-11), dan persetujuan editorial (QG-12) tidak dinyatakan lulus oleh validator.
- Memperketat registry ekstensi: `fieldTypes` menjadi allowlist field dokumen; field yang tidak dideklarasikan ditolak. Setiap field pada `requiredFields` harus memiliki deklarasi tipe (kecuali `id` global yang divalidasi secara universal).
- Menambahkan test integrasi CLI untuk konfigurasi lengkap, penolakan konfigurasi parsial pada mode lengkap, dan kegagalan ketika aset wajib tidak ditemukan.
- Menambahkan allowlist field untuk enam kontrak inti dan kontrak ekstensi; field baru harus masuk melalui perubahan kontrak/keputusan proyek eksplisit.

### Verification boundary
- Test baru ditambahkan ke suite pytest dan workflow CI yang menjalankan `pytest -q`; hasil workflow untuk commit ini harus diperiksa sebelum menyatakan CI lulus.
- Fixture integrasi menguji alur CLI pada situs sintetis; bukan pengganti validasi corpus dan build Astro proyek turunan.

## 2026-11-28 — Konsistensi contoh konfigurasi (2/5)

### Changed
- Memisahkan secara eksplisit contoh generik pada Extension Contract dari contoh konfigurasi adopsi Training/Schedule.
- Menegaskan bahwa kontrak Training/Schedule adalah sumber normatif field wajib/opsional dan semantik domain; YAML registry hanya contoh pemetaan subset kemampuan extension v1.
- Menyelaraskan contoh registry dengan kontrak: `ulid` dan `publisherId` tetap dapat dideklarasikan, tetapi tidak diwajibkan secara universal.
- Memperbarui versi Training/Schedule Contract dan Templates menjadi 1.2 serta menegaskan bahwa keberadaan field pada template kosong tidak otomatis menjadikannya wajib.

### Verification boundary
- Perubahan dokumentasi dan YAML diperiksa secara tekstual melalui pembacaan ulang setelah commit.
- Belum menjalankan validator pada fixture ini atau corpus proyek; contoh registry tetap perlu diuji saat diadopsi oleh proyek Astro.

## 2026-11-28 — Konsistensi aturan relasi (1/5)

### Changed
- Constitution 1.4 membedakan aturan FK numerik untuk enam collection inti dan pengecualian natural key yang harus dideklarasikan untuk collection ekstensi.
- Content Contract 1.6 dan AGENTS.md diselaraskan dengan hierarki aturan tersebut.
- Extension Contract memperjelas syarat natural key: target unik, stabil, tidak kosong, tipe kompatibel, target/cardinality eksplisit, dan satu sumber kebenaran.
- Kontrak Training/Schedule 1.1 menetapkan `schedule.trainingSlug -> training.trainingSlug` sebagai relasi tunggal normatif; alternatif FK numerik harus menggantikan, bukan menduplikasi, natural key.
- Template dan contoh registry diperbarui; field `trainingId` yang tidak digunakan sebagai relasi dihapus dari contoh.

### Verification boundary
- Perubahan dokumentasi dan contoh konfigurasi diperiksa ulang melalui pembacaan file setelah commit.
- Tidak menjalankan pytest atau validasi corpus; pekerjaan 1/5 ini adalah penyelarasan aturan dokumentasi dan contoh, bukan perubahan validator.
- Collection inti tidak berubah perilakunya. Extension v1 tetap mensyaratkan pengujian relasi pada proyek yang mengadopsinya.

## 2026-11-28 — Kontrak collection Training dan Schedule

### Added
- Menetapkan `training` sebagai definisi program/kursus dan `schedule` sebagai pelaksanaan/batch, tanpa memaksakan keduanya ke enam kind inti.
- Mendokumentasikan field, route prefix, identitas, relasi satu schedule ke satu training melalui natural key stabil, dan relasi balik training ke banyak schedule.
- Mendefinisikan pemetaan Schema.org `Course` untuk training dan `Event` untuk schedule, dengan batasan agar properti tambahan hanya dirender bila sumber datanya tersedia.
- Menambahkan aturan domain yang wajib divalidasi proyek: rentang tanggal, zona waktu IANA, status jadwal, pendaftaran, venue, akses online, dan kestabilan slug.
- Menambahkan template frontmatter kosong untuk training dan schedule, serta menautkan dokumen dari README dan mekanisme extension contract.

### Scope
- Ini adalah kontrak referensi yang dapat diadopsi proyek. Tidak mengubah enam collection inti dan tidak mengklaim validator ekstensi v1 telah memvalidasi nested schema atau seluruh business rules.
- Proyek tetap wajib menambahkan Zod/domain schema, fixture valid-invalid, renderer, dan pengujian JSON-LD hasil build.

Semua perubahan standar yang berdampak pada proyek turunan dicatat di sini.


## 2026-11-28 — Penyempurnaan remediasi audit validator

### Fixed
- Extension contract validator menerima nilai tanggal dan timestamp native hasil parsing YAML untuk offset_datetime dan iso_date_or_datetime; validasi tidak lagi mengharuskan semua nilai bertipe string.
- Registry ekstensi diperketat: nama field wajib unik, enum hanya boleh merujuk field bertipe, sumber schemaMappings wajib dideklarasikan dalam fieldTypes, prefix route harus path absolut ternormalisasi, dan direktori ekstensi tidak boleh saling tumpang tindih atau memakai nama direktori collection inti.
- Test regresi ditambahkan untuk nilai date/datetime native YAML dan deklarasi registry ekstensi yang tidak konsisten.
- Pemeriksaan internal link mencakup props url, href, actionHref, primaryHref, secondaryHref, dan registrationUrl.

### Verification boundary
- Test lokal belum dijalankan dari sesi ini. Workflow CI telah dikonfigurasi untuk smoke-test CLI dan pytest, tetapi hasil hijau commit terbaru belum dapat diverifikasi melalui status check yang tersedia.
- Korpus penuh pusattraining dan workflow di repo tersebut tetap belum dijalankan/diubah; extension v1 masih memerlukan validasi nested/domain-specific di proyek pemakai.


## 2026-11-28 — Koreksi hasil audit validator

### Koreksi status Milestone 5
- Fungsi validasi slug/route, canonical, aset/tautan, dan route manifest tersedia di kode serta memiliki unit test, tetapi pada kode yang diaudit entry point `main()` belum memanggil seluruh fungsi tersebut.
- Argumen CLI `--site-root`, `--route-manifest`, dan `--route-prefixes` telah dideklarasikan, tetapi belum dipakai untuk mengaktifkan pemeriksaan terkait.
- Workflow `.github/workflows/validator-tests.yml` hanya menjalankan `pytest -q`; klaim bahwa CI menjalankan smoke-test CLI `--help` tidak akurat.
- Karena itu, entri Milestone 5 di bawah harus dibaca sebagai catatan penambahan fungsi dan rancangan penggunaan, bukan pernyataan bahwa integrasi CLI/CI telah selesai. Milestone 5 belum dapat dinyatakan selesai secara end-to-end.
- Catatan ini memperbaiki status implementasi dan bukti verifikasi; tidak mengubah aturan normatif Quality Gates.

## 2026-11-28

### Added — Validator milestone 5
- Menambahkan validasi pola slug, route generation per collection, route-prefix override, dan route collision lintas collection.
- Menambahkan pemeriksaan canonical URL duplikat, referensi aset lokal, internal links dari props dan Markdown, serta route manifest, sitemap, source file, dan bentuk dasar redirect.
- Mendeklarasikan opsi CLI `--site-root`, `--route-manifest`, dan `--route-prefixes`; pada audit 2026-11-28, opsi tersebut belum terhubung ke pemeriksaan Milestone 5. CI menjalankan unit tests (`pytest -q`); smoke-test CLI belum tersedia.
- Menambahkan dokumentasi `VALIDATOR-MILESTONE-5.md`, memperbarui README dan Quality Gates menjadi versi 0.7, serta mencatat batas otomatisasi tiap gate.
- QG-12 tetap manual. QG-08 rendered JSON-LD, QG-10 audit accessibility browser, dan QG-11 production build tetap harus dijalankan oleh setiap proyek Astro; repository standar tidak memiliki aplikasi Astro.

## 2026-11-28

### Added — Validator milestone 4
- Menambahkan Schema Registry referensi untuk scope block, page, dan entity; validator memeriksa tipe schema dokumen, scope mainEntity, properti schema yang dikenal, serta pasangan schema block dan component.
- Menambahkan Block Registry referensi yang mengenali identifier block dari Content Contract dan katalog gabungan; memvalidasi component, props, tipe props, dan subset props spesifik komponen yang kontraknya eksplisit.
- Menolak component, schema type, dan props yang tidak terdaftar.
- Menambahkan suite pengujian Schema Registry dan Block Registry serta dokumentasi VALIDATOR-MILESTONE-4.md.

### Verification
- GitHub Actions pada Python 3.12: **45 passed**; workflow `Validator Tests` berstatus success pada commit `03610b8`.

### Scope and limitations
- Katalog komponen lintas proyek adalah inventaris adopsi, bukan daftar implementasi wajib. Props yang belum memiliki kontrak lintas proyek eksplisit tetap harus ditetapkan pada registry proyek.
- Validator belum menghasilkan atau memvalidasi graph JSON-LD hasil render. Validasi route, slug collision, aset, tautan, dan integrasi Quality Gates tetap menjadi Milestone 5.

## 2026-11-28

### Added — Validator milestone 2
- Validator mengenali kontrak Homepage, Menu, Page, Article, Service, dan Category dengan field wajib dan pemeriksaan tipe/struktur spesifik per jenis.
- Ditambahkan validasi SEO fallback dan canonical, intro satu paragraf teks biasa, DefinedTerm pada Page, featuredImage, menu target/URL/enum/depth, serta bentuk dasar relasi numerik dan array ID unik.
- Nama collection umum diinferensikan dari direktori; proyek dengan nama collection khusus dapat memakai opsi `--collection KIND=DIR`. Collection yang tidak dikenali gagal secara eksplisit.
- Ditambahkan suite pengujian kontrak dan dokumentasi `VALIDATOR-MILESTONE-2.md`.

### Verification
- GitHub Actions pada Python 3.12: **22 passed**; workflow `Validator Tests` berstatus success.
- Validasi keberadaan target FK lintas dokumen, target type/kardinalitas, Block Registry/props, Schema Registry menyeluruh, route/assets/internal links, dan quality gates lanjutan tetap di luar cakupan milestone ini.


### Fixed
- `docs/REVIEW-NOTES.md`: status, versi, dan rujukan baris diselaraskan dengan Content Contract 1.5, Frontmatter Templates 1.4, dan Quality Gates 0.6; rujukan CI kini mengarah ke `quality/QUALITY-GATES.md:120`.
- `projects/tnvcertification/CONTENT-CONTRACT-EVALUATION.md`: catatan status memperbarui tindak lanjut ke 1.5/1.4 tanpa mengubah objek snapshot 1.3/1.2.
- `CHANGELOG.md`: entri adopsi Content Contract 1.4 dipulihkan agar tidak tertimpa entri 1.5.
- `quality/QUALITY-GATES.md`: contoh kelulusan QG-08 memakai "page-level type yang valid (misalnya `WebPage`)", selaras dengan `content-contract/CONTENT-CONTRACT.md:123`; aturan gate tidak diubah.

### Verification
- `git diff --check` bersih; 27 berkas Markdown diperiksa menghasilkan 0 tautan lokal rusak dan 0 code fence tidak seimbang; rujukan baris pada `docs/REVIEW-NOTES.md` masih mengarah ke isi yang dimaksud.
- Tidak ada aturan normatif yang diubah, sehingga versi dokumen tidak dinaikkan.

## 2026-11-28 — Validator audit remediation

### Fixed
- Integrasi CLI Milestone 5: canonical uniqueness, slug/route, asset/internal link, route manifest, sitemap, redirect, serta penggunaan `--site-root`, `--route-manifest`, dan `--route-prefixes`.
- CI validator: menambahkan smoke-test `--help`; suite pytest mencakup test integrasi CLI untuk canonical, internal link, route manifest, dan exit code.
- Schema Registry: seluruh schema type pada scope page/block/entity kini memiliki status eksplisit `mapped` atau `declaration-only`; tipe declaration-only ditolak pada penggunaan dokumen/block sampai project mapping disediakan; mapping SiteNavigationElement, CollectionPage, Table, dan ImageObject tersedia.
- Project Collection Contract Extensions v1: menambahkan `--contract-registry` untuk kind proyek, field/type dasar, schema type beserta `schemaMappings` eksplisit, route prefix, enum field, tipe tanggal/ULID, relasi one/many berbasis ID atau natural key, dan schema type statis/berbasis field; disertai contoh training/schedule.
- Menambahkan fixture test untuk ekstensi training/schedule dan konsistensi cakupan Schema Registry.
- Memperbarui dokumen Milestone 4/5, Quality Gates, dan analisis untuk memisahkan implementasi, bukti CI, dan batas validasi korpus.

### Batas dan pekerjaan yang belum selesai
- Hasil workflow CI pada commit terbaru belum diverifikasi sebagai hijau; perubahan workflow bukan bukti eksekusi sukses.
- Korpus penuh pusattraining belum dijalankan melalui extension validator. Extension v1 belum mencakup validasi nested schema, block discriminator, refinement tanggal/timezone, atau graph JSON-LD hasil render.
- Workflow dan test tambahan pada `arisciwek/pusattraining` belum diubah karena izin GitHub yang tersedia hanya read/pull, tanpa push.
- Test lokal tidak dijalankan karena lingkungan container tidak dapat mengakses GitHub untuk clone repository.

### Compatibility
- Enam kind inti dan semantik `--collection` tidak berubah. Kind proyek tambahan harus didaftarkan secara eksplisit melalui `--contract-registry`.
- Extension registry v1 bersifat opt-in dan memiliki batas yang dijelaskan di `docs/CONTRACT-EXTENSIONS.md`; proyek tetap wajib menambahkan validasi domain dan build/render tests sendiri.

## 2026-11-27

### Added
- Content Contract 1.4: katalog tipe Schema.org, Arsitektur tiga lapisan, Schema Registry berisi field wajib dan status dukungan Google, serta aturan JSON-LD graph. Field `intro` ditetapkan sebagai paragraf pembuka tersendiri pada Page, Article, dan Service, termasuk panduan `DefinedTerm` untuk halaman definisi.
- Content Contract 1.5: memisahkan page-level schema dari entity-level `DefinedTerm`; halaman definisi menggunakan `schema.type` untuk `WebPage` dan `schema.mainEntity.type` untuk `DefinedTerm`. `DefinedTerm.name` dipetakan dari `title` dan `DefinedTerm.description` secara khusus dipetakan dari `intro`.

### Changed
- Frontmatter Templates 1.4: menambahkan kerangka opsional `schema.mainEntity.type` dan checklist pemetaan `DefinedTerm` dari `title` + `intro`.
- Technical Architecture 0.3: Schema Registry menjadi keputusan yang harus ditetapkan sebelum implementasi.
- Project Architecture Templates 0.3 dan `projects/_template/TECHNICAL-ARCHITECTURE.md` 0.2: menyediakan tempat keputusan Schema Registry pada artefak proyek.
- Quality Gates 0.6: memperluas test matrix untuk validasi bentuk dan keterlihatan `intro`, pemisahan page/entity schema, pola definisi `DefinedTerm`, serta sumber `DefinedTerm.description`.
- README: menautkan laporan evaluasi proyek pada `projects/tnvcertification/`.

### Rationale and impact
- Memisahkan paragraf pembuka substantif (`intro`) dari ringkasan dokumen (`description`) dan meta description (`seo.description`).
- Menghindari ambiguitas antara tipe schema halaman dan entitas utama yang didefinisikan halaman.
- Mencegah penggunaan tipe Schema.org hanya karena tersedia di katalog; setiap tipe harus memiliki sumber data, batas penggunaan, dan verifikasi status.
- Menurunkan kewajiban Schema Registry ke artefak proyek dan gate yang dapat diuji, bukan hanya pernyataan di kontrak konten.
- Menandai laporan TNV Certification sebagai snapshot sebelum revisi 1.4/1.5 agar tidak dibaca sebagai penolakan terhadap standar terbaru.

### Compatibility
- Proyek yang sebelumnya memakai `schema.type: DefinedTerm` harus memindahkan deklarasi entitas ke `schema.mainEntity.type: DefinedTerm` dan mempertahankan page-level type pada `schema.type`.
- Untuk DefinedTerm, sumber `DefinedTerm.description` wajib `intro`; `description` dokumen dan `seo.description` tetap memiliki fungsi masing-masing.
- Proyek harus menyiapkan Schema Registry sebelum QG-08 dinyatakan lulus; konflik dengan Block Registry harus menggagalkan validasi.
- Katalog Schema.org bukan daftar tipe wajib. Tipe tetap dipilih berdasarkan konten dan aturan registry proyek.

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

### Fixed — tindak lanjut pull 2026-11-26
- `projects/_template/README.md`: versi paket diselaraskan ke 0.2 sesuai catatan di dalam berkas dan entri Template Pack 0.2.
- `projects/_template/TECHNICAL-ARCHITECTURE.md`: QG-12 dipisahkan dari gate otomatis; template tidak lagi mewajibkan perintah dan fixture CI untuk review editorial.
- `docs/REVIEW-NOTES.md`: checklist yang sudah dibuktikan ditandai selesai dan rujukan baris README diperbarui.
- `docs/ANALISIS-POLA-SITUS.md`: rujukan baris README diperbarui setelah penambahan tautan IA.

### Rationale and impact
- Koreksi ini menjaga konsistensi internal paket template dan catatan bukti tanpa mengubah aturan normatif.
- Pemisahan QG-12 memperjelas bahwa persetujuan editorial dibuktikan oleh reviewer, bukan oleh perintah CI.

### Compatibility
- Tidak ada versi standar normatif yang berubah; perintah dan fixture tetap diwajibkan untuk gate otomatis.
