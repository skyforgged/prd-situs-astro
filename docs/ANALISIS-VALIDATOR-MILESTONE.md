# Analisis Validator Milestone 1–5

> Tanggal analisis: 2026-11-28
> Status: catatan tinjauan, bukan perubahan aturan normatif dan bukan persetujuan gate
> Objek: 59 commit antara `fa3d50a` dan `37651fa` pada repository standar ini
> Pemeriksaan tambahan: penerapan pada korpus nyata di `../pusattraining/pusattraining/`

## 1. Konteks

Commit-commit yang ditarik mencakup 5 milestone validator otomatis dan mengubah 14 berkas: implementasi validator, registry, test, workflow CI, requirements, README, CHANGELOG, Quality Gates, Review Notes, dan satu berkas dokumen per milestone.

Penilaian ini dibatasi pada isi yang ada di checkout dan status GitHub Actions yang diverifikasi melalui GitHub API. Tidak ada perubahan normatif, sehingga versi dokumen standar tidak dinaikkan oleh catatan ini.

## 2. Analisis per milestone

### Milestone 1 — Fondasi validator (`02ea5f1`–`cf7f662`)

**Isi**

- Parser frontmatter ketat dan penolakan YAML duplicate key: `scripts/validate_content.py:13-45`.
- Invariant global: `id` harus integer positif dan boolean ditolak (`:47`), ID unik lintas collection (`:297-313`), `schema` berupa object dengan `type`, `slug` non-kosong, ID block unik lokal, timestamp ISO 8601 UTC presisi detik, serta `updatedDate` tidak lebih awal dari `publishedDate`.
- Workflow CI `pytest` pada Python 3.12: `.github/workflows/validator-tests.yml`.

**Kekuatan**

Fail-closed terhadap YAML duplicate key dan tipe ID. Batas cakupan dinyatakan eksplisit di `VALIDATOR-MILESTONE-1.md:24-26`, sehingga milestone ini tidak mengklaim kontrak per jenis lebih awal.

**Bukti**

`VALIDATOR-MILESTONE-1.md:40` mencatat 10 unit test. GitHub Actions memang berjalan; check `validator-tests` pada commit `37651fa` berstatus `success`. Pytest tidak terpasang pada lingkungan pemeriksaan ini, sehingga jumlah test tidak dijalankan ulang secara lokal.

**Catatan**

Commit `b1138b2` ("Record validator milestone 1 in changelog") dan `cf7f662` ("Record green validator CI result") kosong, tanpa perubahan berkas. Klaim bukti pada keduanya tidak tersimpan sebagai diff git.

### Milestone 2 — Kontrak per jenis dokumen (`3173e37`–`7d56a7d`)

**Isi**

- Enam kontrak didefinisikan terpisah: `scripts/validate_content.py:74-81`.
- SEO fallback dan canonical: `:89-98`.
- `intro` satu paragraf teks biasa dan aturan `DefinedTerm`: `:99-115`.
- `featuredImage`: `:116-125`; menu target, URL, enum, dan kedalaman: `:126-145`; bentuk relasi numerik dan array ID unik: `:159-169`.
- Inferensi nama direktori dan pemetaan eksplisit `--collection KIND=DIR`: `:14-19,179-187`.

**Kekuatan**

Validator tidak memaksa satu schema universal, selaras dengan prinsip Content Contract 1.5. Collection yang tidak dikenali menghasilkan error eksplisit, bukan dilewati diam-diam.

**Kelemahan**

Deteksi markup `intro` memakai heuristik regex dan backtick pada `:104`, sementara awalan `DefinedTerm` di-hard-code sebagai `" adalah "` pada `:112-115`. Keduanya cukup spesifik untuk Bahasa Indonesia agar disebut aturan lintas proyek tanpa penjelasan lebih lanjut.

**Bukti**

`VALIDATOR-MILESTONE-2.md:63` dan `CHANGELOG.md:38` mencatat 22 test pada GitHub Actions Python 3.12.

### Milestone 3 — Integritas relasi lintas dokumen (`b0b1c25`–`eae9efa`)

**Isi**

- Indeks ID global serta pemeriksaan target hilang, ambigu, dan salah jenis: `scripts/validate_content.py:192-212`.
- Menu bertingkat: `:249-258`; FK pada block `serviceIds` dan `content-list.categoryId`: `:260-278`.
- Larangan self-reference: `:226-247`; siklus `parentPageId` terdeteksi: `:280-294`.

**Kekuatan**

Relasi gagal bila target tidak ditemukan atau ID duplikat; validator tidak memilih target secara arbitrer. Batas `authorId` dan `providerId` dinyatakan jujur di `VALIDATOR-MILESTONE-3.md:25-30` karena kontrak jenis target belum tersedia.

**Catatan**

Tiga commit berisi klaim tanpa diff: `898f966` (scope), `1d4b962` (perbaikan fixture), dan `eae9efa` (verifikasi CI). `VALIDATOR-MILESTONE-3.md:63` mencatat 34 test.

### Milestone 4 — Schema Registry dan Block Registry (`fbfb0dc`–`660101a`)

**Isi**

- Pemisahan scope tipe Schema.org: `scripts/registries.py:2-6`.
- Daftar 36 `BLOCK_COMPONENTS`: `:9-15`; `COMMON` dan 17 props spesifik komponen: `:16-45`.
- Tujuh entri `SCHEMA_REGISTRY` dengan `fieldMapping`, `requiredFields`, `optionalFields`, `googleRichResultSupport`, dan `documentationUrl`: `:49-57`.
- Validator fail-closed pada tipe, props, dan pasangan component–schema: `:59-113`.

**Kekuatan**

Component dan props yang tidak dikenal ditolak. Pasangan block–schema dibatasi, dan field sumber wajib untuk FAQ, HowTo, serta ItemList ikut diperiksa (`:101-112`). Pemisahan block dari UI component ditegaskan di `VALIDATOR-MILESTONE-4.md:31-36`.

**Kelemahan**

`SCHEMA_TYPES["page"]` memuat lebih banyak tipe daripada tujuh entri `SCHEMA_REGISTRY`. Sebuah tipe dapat lolos pemeriksaan scope tanpa memiliki `fieldMapping`, dan validator tidak menandai ketiadaan itu. Nilai `googleRichResultSupport` juga memerlukan pemeliharaan saat kebijakan berubah. `CHANGELOG.md:23` mencatat 45 test pada `03610b8`.

### Milestone 5 — Route, aset, tautan, dan Quality Gates (`685fbae`–`37651fa`)

**Isi**

- Duplikat canonical: `scripts/validate_content.py:317-328`.
- Slug, route per collection, override prefix, dan collision: `:330-357`.
- Referensi aset lokal dan internal link dari props serta Markdown: `:359-424`.
- Route manifest, sitemap, source file, dan redirect: `:426-468`.
- Opsi CLI `--site-root`, `--route-manifest`, `--route-prefixes`: `:471-479`.
- Quality Gates naik dari versi 0.6 menjadi 0.7 pada `quality/QUALITY-GATES.md`.

**Kekuatan**

Error memakai kode gate yang dapat ditindaklanjuti, misalnya `[QG-04 INVALID_SLUG]`, `[QG-07 DUPLICATE_CANONICAL]`, dan `[QG-13 ROUTE_NOT_IN_MANIFEST]`. Prefix route dapat dioverride. Validator sengaja tidak mengakses HTTP eksternal sehingga tetap deterministik.

**Temuan 1 — integrasi CLI belum terjadi**

`main()` pada `scripts/validate_content.py:471-491` hanya memanggil `validate_paths()`. Fungsi `validate_seo_uniqueness`, `validate_routes`, `validate_assets_and_links`, dan `validate_route_manifest` tidak dipanggil dari entry point. Nilai `args.site_root`, `args.route_manifest`, dan `args.route_prefixes` juga tidak dipakai. Pesan sukses di `:489` tetap menyatakan bahwa route, aset, dan IA telah divalidasi.

Dengan demikian klaim "CLI terpadu" pada `CHANGELOG.md:10`, `VALIDATOR-MILESTONE-5.md:34-42`, dan `docs/REVIEW-NOTES.md:290` belum sesuai dengan kode yang dapat dijalankan.

**Temuan 2 — smoke-test CI tidak ada di workflow**

`.github/workflows/validator-tests.yml:1-18` hanya menjalankan `pytest -q`; tidak ada langkah `--help`. Commit `6228f1e` yang berjudul "Smoke-test quality gate CLI in CI" kosong. Klaim smoke-test masuk ke `VALIDATOR-MILESTONE-5.md:120,135`, `quality/QUALITY-GATES.md:121`, `CHANGELOG.md:10`, dan `docs/REVIEW-NOTES.md:291`.

**Bukti yang memang benar**

GitHub Actions pada `37651fa` berstatus `success`. Berkas `tests/test_validate_content.py` memuat 50 fungsi `test_` dan menguji fungsi-fungsi Milestone 5 secara langsung pada `:565-644`. Pengujian unit tersedia; yang belum adalah penyambungannya ke CLI dan ke langkah CI tambahan.

## 3. Uji penerapan pada proyek nyata: training dan schedule

Sumber dibaca hanya untuk analisis di `../pusattraining/pusattraining/`. Tidak ada berkas di proyek tersebut yang diubah.

### 3.1 Konteks

Content Contract 1.5 mendefinisikan enam jenis dokumen: Homepage, Menu, Page, Article, Service, dan Category. Bagian 11 menyatakan jenis lain harus mendapat kontrak tersendiri sebelum dipakai. Validator mengikuti batas yang sama: `ALIASES` dan tabel kewajiban pada `scripts/validate_content.py:14-19,74-81` tidak mengenal `training` maupun `schedule`.

Proyek pusattraining justru memakai keduanya sebagai collection utama, dengan 133 berkas di `src/content/trainings/` dan 116 berkas di `src/content/schedules/`. Keduanya memiliki skema Zod tersendiri di `src/content.config.ts:101-194` dan `:195-259`, termasuk aturan yang belum ada di PRD.

### 3.2 Ketidaksesuaian dengan kontrak PRD

| Aspek | Validator PRD | Isi proyek pusattraining | Dampak |
|---|---|---|---|
| Jenis dokumen | enam kind; collection asing ditolak | `training` dan `schedule` tidak ada di `ALIASES` | Perlu pemetaan eksplisit `--collection`; tanpa itu ber error |
| Identitas | `id` integer positif | `id` plus `ulid` 26 karakter (`src/content.config.ts:4-6`) | ULID tidak memiliki padanan di kontrak PRD |
| Tanggal | `publishedDate` dan `updatedDate` UTC presisi detik (`scripts/validate_content.py:171-176`) | `pubDate` dan `updatedDate` dengan offset; `startDate` dan `endDate` berupa tanggal kalender | Nama field PRD tidak ada, sehingga pemeriksaan tanggal tidak berjalan |
| SEO dan schema | `schema` dan `seo` wajib berupa object (`:84-98`) | 0 dari 133 training dan 0 dari 116 schedule memuat field tersebut | Korpus ditolak apa adanya |
| Block | discriminator `component` (`:265`) | discriminator `type`, 1353 kemunculan di kedua collection | Registry block tidak mengenali type yang dipakai |

Ini bukan kesalahan proyek. Ini bukti bahwa kontrak PRD belum mencakup dua jenis konten yang benar-benar dipakai. Sesuai Content Contract bagian 11, keduanya memerlukan kontrak tersendiri, bukan dipaksa mengikuti kontrak Page atau Article.

### 3.3 Pemeriksaan yang berjalan di proyek pusattraining

- `npm run check` menjalankan `astro sync && tsc --noEmit`, sehingga skema Zod mengaudit frontmatter training dan schedule saat sinkronisasi konten.
- Schedule memiliki refinement tambahan: `endDate` tidak boleh sebelum `startDate`, `updatedDate` tidak boleh sebelum `pubDate`, `timezone` harus nama zona IANA yang valid, dan `countryCode` dua huruf (`src/content.config.ts:9-63,195-259`).
- Generator schedule menguji tabrakan `id` numerik maupun `scheduleId` string (`scripts/generate-schedule-frontmatter.test.mjs:31-35`).
- Terdapat enam berkas test dengan total 32 test Node. Workflow CI menjalankan empat di antaranya, yaitu 20 test.
- Dua berkas belum tersambung ke CI: `scripts/schedule-mapping-config.test.mjs` (5 test) memiliki skrip `test:schedules:mappings` di `package.json`, tetapi tidak dipanggil di `.github/workflows/ci.yml`; `scripts/training-structured-data.test.mjs` (7 test) tidak memiliki skrip npm sama sekali.
- Tujuh test structured data training memeriksa graph JSON-LD, antara lain Course sebagai `mainEntity` tunggal dan Organization yang lengkap untuk setiap status. Ini melengkapi kelemahan pada bagian 2: validator PRD memeriksa bentuk frontmatter, bukan graph hasil render.
- Trigger push CI hanya mencakup `main` dan satu cabang fitur schedule (`.github/workflows/ci.yml:4-9`). Cabang yang memuat pekerjaan schema training tidak termasuk daftar itu, dan GitHub API tidak menunjukkan check run untuk commit teratasnya. Dengan demikian bukti CI otomatis untuk perubahan training tidak tersedia.

### 3.4 Makna terhadap penilaian

Temuan ini mengonfirmasi prioritas P1 dari penilaian awal: pengujian penerapan PRD pada proyek nyata belum terjadi. Kelima milestone validator diuji dengan fixture sintetis yang mengikuti enam kontrak PRD. Korpus pusattraining menunjukkan bahwa proyek nyata dapat memiliki jenis konten, nama field, dan format block yang berbeda secara sah selama dinyatakan sebagai keputusan proyek.

Tindakan yang disarankan untuk menutup celah ini, tanpa mengubah standar dalam catatan ini:

1. Tetapkan kontrak `training` dan `schedule` menurut Content Contract bagian 11, mencakup route, field wajib, Schema.org utama, dan relasi ke collection training.
2. Tentukan kebijakan alias field, misalnya `pubDate` versus `publishedDate`, sebagai keputusan proyek yang eksplisit, bukan konversi diam-diam.
3. Perluas registry block agar menerima block domain seperti `training-detail-intro` dan `training-schedule-list`, atau nyatakan berada di luar renderer generik seperti yang sudah dicatat katalog.
4. Sambungkan 12 test yang belum masuk CI dan perluas trigger push agar cabang yang mengubah schema training ikut diverifikasi.
5. Jalankan validator PRD minimal sekali terhadap salinan korpus nyata sebagai uji penerapan, dengan hasil yang diharapkan ditulis sesuai kontrak proyek.

## 4. Temuan lintas milestone

1. Enam commit kosong dipakai sebagai catatan bukti: `b1138b2`, `cf7f662`, `898f966`, `1d4b962`, `eae9efa`, dan `6228f1e`.
2. Dokumentasi lebih cepat daripada implementasi pada dua titik: integrasi CLI Milestone 5 dan smoke-test CI.
3. Status CI `success` diverifikasi melalui GitHub API, tetapi jumlah test tidak dijalankan ulang secara lokal karena pytest tidak tersedia di lingkungan ini.
4. Validator belum memeriksa graph JSON-LD hasil render, accessibility browser, production build Astro, atau kualitas editorial. QG-12 tetap manual.
5. Kontrak enam jenis belum diuji terhadap korpus proyek nyata yang memakai `training` dan `schedule`.

## 5. Penilaian

Kelima milestone bergerak tepat pada prioritas P0 dan P1: kontrak menjadi dapat diuji, relasi dapat diverifikasi, registry membuat aturan tidak lagi interpretatif, dan Quality Gates memperoleh pemetaan automasi.

Yang masih menghalangi klaim "selesai" bukan cakupan teori, melainkan penyambungan implementasi ke entry point yang didokumentasikan dan kesesuaian bukti CI dengan klaimnya. Fungsi dan test Milestone 5 sudah ada, tetapi CLI belum memanggilnya dan smoke-test yang diklaim tidak terdapat di workflow. Uji pada korpus pusattraining menambah satu celah lagi: dua jenis konten yang dipakai proyek nyata belum memiliki kontrak di PRD, jadi validator tidak dapat dijalankan langsung terhadap korpus tersebut.

## 6. Batas verifikasi

Catatan ini disusun dengan membaca isi berkas, riwayat git, dan status check GitHub Actions. Tidak ada build Astro, validator corpus nyata, atau pytest lokal yang dijalankan. Pemeriksaan terhadap proyek pusattraining hanya berupa pembacaan berkas dan metadata GitHub API; tidak ada test, `astro sync`, maupun build yang dijalankan di proyek tersebut. Tidak ada aturan normatif yang diubah oleh catatan ini.
