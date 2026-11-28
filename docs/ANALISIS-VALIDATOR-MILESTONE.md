# Analisis Validator Milestone 1–5

> Tanggal analisis: 2026-11-28
> Status: audit implementasi dan rekomendasi tindak lanjut; bukan perubahan aturan normatif, bukan persetujuan gate, dan bukan bukti bahwa seluruh milestone siap dipakai melalui CLI
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

**Kelemahan — konsistensi scope dan registry**

`SCHEMA_TYPES["page"]` memuat lebih banyak tipe daripada tujuh entri `SCHEMA_REGISTRY`. Akibatnya, sebuah tipe dapat lolos pemeriksaan scope dokumen tanpa memiliki entri registry yang menyediakan `fieldMapping`, `requiredFields`, dan `optionalFields`. Ini menciptakan dua sumber kebenaran: daftar tipe yang diizinkan oleh scope dan daftar tipe yang benar-benar dapat dipetakan ke JSON-LD. Validator perlu menetapkan kebijakan eksplisit: setiap tipe yang diterima harus memiliki mapping registry, atau secara eksplisit ditandai sebagai tipe yang hanya diizinkan tetapi belum memiliki generator/mapping. Untuk kontrak yang mengharuskan JSON-LD, ketiadaan mapping harus menjadi error, bukan lolos validasi.

Nilai `googleRichResultSupport` juga merupakan metadata yang dapat berubah mengikuti kebijakan Google; nilainya perlu ditinjau berkala dan tidak boleh diperlakukan sebagai jaminan bahwa hasil kaya pasti tampil. `CHANGELOG.md:23` mencatat 45 test pada `03610b8`. Jumlah tersebut adalah bukti unit test yang dicatat, bukan bukti bahwa seluruh kombinasi scope dan registry telah konsisten.

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

**Temuan 1 — defect P0: validasi Milestone 5 belum terintegrasi ke CLI**

`main()` pada `scripts/validate_content.py:471-491` hanya memanggil `validate_paths()`. Fungsi `validate_seo_uniqueness`, `validate_routes`, `validate_assets_and_links`, dan `validate_route_manifest` tidak dipanggil dari entry point. Nilai `args.site_root`, `args.route_manifest`, dan `args.route_prefixes` juga tidak dipakai. Pesan sukses di `:489` tetap menyatakan bahwa route, aset, dan IA telah divalidasi.

Dengan demikian klaim "CLI terpadu" pada `CHANGELOG.md:10`, `VALIDATOR-MILESTONE-5.md:34-42`, dan `docs/REVIEW-NOTES.md:290` belum sesuai dengan kode yang dapat dijalankan.

**Temuan 2 — defect P0: smoke-test CLI yang diklaim tidak ada di workflow CI**

`.github/workflows/validator-tests.yml:1-18` hanya menjalankan `pytest -q`; tidak ada langkah `--help`. Commit `6228f1e` yang berjudul "Smoke-test quality gate CLI in CI" kosong. Klaim smoke-test masuk ke `VALIDATOR-MILESTONE-5.md:120,135`, `quality/QUALITY-GATES.md:121`, `CHANGELOG.md:10`, dan `docs/REVIEW-NOTES.md:291`.

**Bukti yang memang benar**

GitHub Actions pada `37651fa` berstatus `success`. Berkas `tests/test_validate_content.py` memuat 50 fungsi `test_` dan menguji fungsi-fungsi Milestone 5 secara langsung pada `:565-644`. Pengujian unit tersedia dan membuktikan fungsi-fungsi tersebut dapat diuji secara terpisah. Namun, unit test itu tidak membuktikan bahwa `main()` memanggil fungsi-fungsi tersebut, bahwa argumen CLI diteruskan dengan benar, atau bahwa kegagalan pemeriksaan menghasilkan exit code non-zero. Ketiganya memerlukan pengujian integrasi CLI. Workflow CI yang diperiksa juga belum menjalankan smoke-test `--help` yang diklaim.

## 3. Uji penerapan pada proyek nyata: training dan schedule

Sumber dibaca hanya untuk analisis di `../pusattraining/pusattraining/`. Tidak ada berkas di proyek tersebut yang diubah.

### 3.1 Konteks

Content Contract 1.5 mendefinisikan enam jenis dokumen: Homepage, Menu, Page, Article, Service, dan Category. Bagian 11 menyatakan jenis lain harus mendapat kontrak tersendiri sebelum dipakai. Validator mengikuti batas yang sama: `ALIASES` dan tabel kewajiban pada `scripts/validate_content.py:14-19,74-81` tidak mengenal `training` maupun `schedule`.

Proyek pusattraining justru memakai keduanya sebagai collection utama, dengan 133 berkas di `src/content/trainings/` dan 116 berkas di `src/content/schedules/`. Keduanya memiliki skema Zod tersendiri di `src/content.config.ts:101-194` dan `:195-259`, termasuk aturan yang belum ada di PRD.

### 3.2 Ketidaksesuaian dengan kontrak PRD

| Aspek | Validator PRD | Isi proyek pusattraining | Dampak |
|---|---|---|---|
| Jenis dokumen | enam kind; parser `--collection` hanya menerima enam kind tersebut | `training` dan `schedule` tidak termasuk daftar kind yang diizinkan | Tidak dapat didaftarkan hanya dengan `--collection training=...`; parser menolak kind di luar enam kontrak inti. Diperlukan mekanisme ekstensi kontrak atau validator proyek-spesifik |
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

1. Tetapkan kontrak `training` dan `schedule` menurut Content Contract bagian 11, mencakup route, field wajib, Schema.org utama, dan relasi antarkoleksi.
2. Tentukan kebijakan alias field, misalnya `pubDate` versus `publishedDate`, sebagai keputusan proyek yang eksplisit, bukan konversi diam-diam.
3. Perluas registry block agar menerima block domain seperti `training-detail-intro` dan `training-schedule-list`, atau nyatakan berada di luar renderer generik seperti yang sudah dicatat katalog.
4. Sambungkan 12 test yang belum masuk CI dan perluas trigger push agar cabang yang mengubah schema training ikut diverifikasi.
5. Sediakan mekanisme ekstensi yang terkontrol untuk kontrak proyek tambahan. `--collection` saat ini hanya memetakan direktori ke salah satu dari enam kind inti; jangan mengklaim bahwa opsi tersebut mendaftarkan kind baru.
6. Setelah kontrak dan mekanisme ekstensi tersedia, jalankan validator terhadap salinan korpus nyata sebagai uji penerapan, dengan hasil yang diharapkan ditulis sesuai kontrak proyek.

## 4. Temuan lintas milestone

1. Enam commit kosong dipakai sebagai catatan bukti: `b1138b2`, `cf7f662`, `898f966`, `1d4b962`, `eae9efa`, dan `6228f1e`.
2. Dokumentasi lebih cepat daripada implementasi pada dua titik: integrasi CLI Milestone 5 dan smoke-test CI.
3. Unit test fungsi Milestone 5 tidak boleh disamakan dengan pengujian integrasi entry point. Klaim bahwa route/aset/tautan/manifest telah divalidasi melalui CLI belum didukung oleh kode `main()` yang diperiksa.
4. Status CI `success` pada commit yang disebutkan diverifikasi melalui GitHub API. Ini hanya membuktikan job yang terpasang pada workflow tersebut berhasil; bukan bukti bahwa smoke-test CLI yang tidak ada telah dijalankan. Jumlah test juga tidak dijalankan ulang secara lokal karena pytest tidak tersedia di lingkungan audit ini.
5. Validator belum memeriksa graph JSON-LD hasil render, accessibility browser, production build Astro, atau kualitas editorial. QG-12 tetap manual.
6. Kontrak enam jenis belum diuji terhadap korpus proyek nyata yang memakai `training` dan `schedule`; kedua collection itu membutuhkan kontrak tambahan, bukan pemaksaan ke jenis inti.

## 5. Matriks tindak lanjut audit

Matriks ini adalah daftar pekerjaan korektif yang diturunkan dari temuan audit. Status menggambarkan kondisi pada saat audit 2026-11-28, bukan status setelah pekerjaan perbaikan dilakukan.

| ID | Prioritas | Temuan | Tindakan yang diperlukan | Kriteria penerimaan | Status saat audit |
|---|---|---|---|---|---|
| AUD-01 | P0 | Entry point CLI hanya menjalankan `validate_paths()` | Integrasikan validasi canonical, routes, assets/links, dan route manifest ke `main()`; teruskan `--site-root`, `--route-manifest`, dan `--route-prefixes` ke fungsi terkait | Semua pemeriksaan yang dikonfigurasi benar-benar berjalan melalui CLI; setiap error membuat exit code non-zero; pesan sukses hanya menyebut pemeriksaan yang benar-benar dijalankan | Belum |
| AUD-02 | P0 | Smoke-test CLI yang diklaim tidak ada di workflow | Tambahkan smoke-test `python scripts/validate_content.py --help` dan test integrasi CLI pada workflow CI | Workflow gagal bila CLI tidak dapat dipanggil, argumen tidak dikenali, atau fixture integrasi yang sengaja invalid tidak menghasilkan kegagalan | Belum |
| AUD-03 | P1 | `SCHEMA_TYPES` dan `SCHEMA_REGISTRY` tidak konsisten | Selaraskan tipe yang diterima dengan entri registry atau tandai secara eksplisit tipe yang belum memiliki mapping; tentukan perilaku untuk tipe tanpa mapping | Tidak ada tipe yang diwajibkan menghasilkan JSON-LD tetapi lolos tanpa mapping; test mencakup setiap tipe yang diizinkan dan setiap pasangan block–schema | Belum |
| AUD-04 | P1 | Validator hanya mengenal enam kind inti | Rancang mekanisme ekstensi kontrak yang eksplisit dan aman untuk collection proyek seperti `training` dan `schedule`; jangan memperluas makna `--collection` secara diam-diam | Kontrak tambahan dapat didaftarkan dengan validasi field, relasi, route, dan schema yang jelas; enam kontrak inti tetap kompatibel dan tetap fail-closed | Belum |
| AUD-05 | P1 | Belum ada uji penerapan yang dapat direproduksi pada korpus proyek nyata | Siapkan fixture/salinan korpus representatif beserta kontrak proyeknya dan jalankan validator setelah mekanisme ekstensi tersedia | Hasil validasi dapat diulang; setiap error/pengecualian dijelaskan oleh kontrak; tidak ada kebutuhan mengubah data proyek agar cocok secara paksa dengan kind inti | Belum |
| AUD-06 | P1 | Test pada proyek pusattraining belum seluruhnya dijalankan CI | Sambungkan test mapping schedule dan structured data training ke workflow serta tinjau trigger branch | Seluruh test yang dimaksud berjalan di CI untuk perubahan schema dan generator terkait; branch/path trigger mencakup sumber yang diuji | Belum |
| AUD-07 | P2 | Beberapa commit audit/evidence kosong | Simpan bukti berupa test, output, atau catatan pada commit yang memiliki perubahan bermakna | Klaim penyelesaian dapat ditelusuri ke diff, test, atau run CI yang relevan; commit kosong tidak dipakai sebagai bukti implementasi | Perlu disiplin proses |

### Urutan penyelesaian yang disarankan

1. Selesaikan AUD-01 dan AUD-02 terlebih dahulu. Keduanya menentukan apakah fitur Milestone 5 benar-benar dapat digunakan dan diverifikasi dari antarmuka yang didokumentasikan.
2. Selesaikan AUD-03 agar scope schema dan kemampuan mapping memiliki satu kebijakan yang konsisten.
3. Rancang AUD-04 sebelum mencoba memvalidasi collection non-inti. Kontrak proyek tidak boleh dipaksakan ke Page atau Article hanya agar lolos validator.
4. Kerjakan AUD-05 dan AUD-06 untuk membuktikan penerapan pada korpus nyata dan memastikan test terkait masuk ke CI.
5. Terapkan AUD-07 sebagai standar pencatatan bukti untuk milestone berikutnya.

## 6. Penilaian saat audit awal (sebelum remediasi)

Bagian ini merekam kesimpulan pada saat audit awal, bukan status implementasi terkini. Kelima milestone telah menghasilkan fondasi yang berarti: kontrak menjadi dapat diuji, relasi dapat diverifikasi, registry mulai memusatkan aturan, dan fungsi Quality Gates tersedia. Namun, status implementasi tidak boleh disamakan dengan status kesiapan operasional. Secara khusus, Milestone 5 belum selesai pada jalur CLI karena `main()` belum memanggil seluruh pemeriksaan yang diklaim; workflow CI juga belum memuat smoke-test CLI. Milestone 4 masih memiliki ketidaksinkronan antara daftar tipe dalam scope dan entri schema registry.

Karena itu, berdasarkan bukti yang tersedia, Milestone 1–3 memiliki bukti implementasi dan test yang dicatat; Milestone 4 memerlukan konsistensi registry; dan Milestone 5 belum layak dinyatakan selesai secara end-to-end. Korpus `pusattraining` menambah kebutuhan desain: `training` dan `schedule` merupakan collection domain yang sah, tetapi belum memiliki kontrak dalam enam jenis inti. Validator PRD tidak dapat dijalankan langsung terhadap korpus tersebut sampai kontrak tambahan dan mekanisme ekstensi ditetapkan.

## 7. Batas verifikasi saat audit awal

Catatan ini disusun dengan membaca isi berkas, riwayat git, dan status check GitHub Actions. Tidak ada build Astro, validator corpus nyata, atau pytest lokal yang dijalankan. Pemeriksaan terhadap proyek pusattraining hanya berupa pembacaan berkas dan metadata GitHub API; tidak ada test, `astro sync`, maupun build yang dijalankan di proyek tersebut. Tidak ada aturan normatif yang diubah oleh catatan ini.


## 8. Status tindak lanjut setelah audit (2026-11-28)

Bagian ini memperbarui status pekerjaan tanpa mengubah tabel historis "Status saat audit" pada Bagian 5.

**Status terkini:** AUD-01 sampai AUD-04 telah ditangani pada repository PRD dan disertai test; AUD-05 baru memiliki fixture representatif, bukan hasil uji seluruh korpus; AUD-06 tetap tertahan oleh hak akses read-only pada repository pusattraining; AUD-07 diterapkan melalui commit bermakna. Hasil CI hijau untuk commit terbaru belum terverifikasi. Rincian bukti dan batasnya ada pada tabel berikut.

| ID | Status tindak lanjut | Bukti / batas |
|---|---|---|
| AUD-01 | Implementasi diterapkan | `main()` kini menjalankan canonical uniqueness dan route validation; meneruskan route prefix; mengaktifkan asset/link checks melalui `--site-root`; dan menjalankan route manifest melalui `--route-manifest`. Test CLI memeriksa exit code gagal dan sukses. |
| AUD-02 | Implementasi diterapkan; hasil CI menunggu run | Workflow menambahkan smoke-test `--help` dan menjalankan pytest yang mencakup test integrasi CLI. Status workflow untuk commit perubahan belum dapat diverifikasi melalui konektor pada sesi ini; jangan tandai lulus sebelum run hijau. |
| AUD-03 | Implementasi diterapkan | Page type dipartisi eksplisit menjadi `mapped` dan `declaration-only`; SiteNavigationElement mendapat mapping. Test memastikan seluruh page type memiliki status tepat. Declaration-only bukan dukungan generator JSON-LD. |
| AUD-04 | Mekanisme ekstensi v1 diterapkan dan diperketat | `--contract-registry` mendukung collection tambahan, required fields, tipe field dasar, schema type beserta `schemaMappings`, enum, route prefix, dan relasi one/many/natural key. Registry kini menolak enum/mapping yang menunjuk field tanpa deklarasi tipe, prefix route tidak ternormalisasi, dan direktori ekstensi yang bertumpang tindih. Parser menerima nilai date/datetime native YAML sesuai tipe deklarasi. Batas nested object, block discriminator, dan refinement domain dicatat pada `docs/CONTRACT-EXTENSIONS.md`. |
| AUD-05 | Fixture representatif tersedia; korpus penuh belum diverifikasi | Test fixture training/schedule memeriksa kontrak ekstensi, route dan relasi. Korpus penuh 249 file pusattraining belum dijalankan melalui validator ini; schema Zod proyek memiliki aturan nested/refinement yang belum seluruhnya direpresentasikan oleh extension v1. |
| AUD-06 | Belum dapat diterapkan pada repo target | Repo `arisciwek/pusattraining` dapat dibaca, tetapi izin GitHub yang tersedia hanya pull/read dan tidak mengizinkan push. Workflow dan test di repo tersebut belum diubah. Perlu akses tulis atau perubahan dilakukan oleh maintainer repo. |
| AUD-07 | Diterapkan pada pekerjaan ini | Perubahan disimpan sebagai commit dengan diff yang bermakna; tidak menggunakan commit kosong sebagai bukti penyelesaian. |

### Catatan batas verifikasi

- Perbaikan lanjutan setelah implementasi ekstensi menutup kasus YAML yang mem-parse tanggal/timestamp menjadi objek `date`/`datetime`, bukan string. Test regresi ditambahkan untuk offset datetime dan tanggal native YAML.
- Registry ekstensi diperketat agar enum, schema mapping, dan route prefix tidak dapat merujuk deklarasi yang tidak konsisten; test negatif ditambahkan.
- Status CI tetap belum dapat dinyatakan hijau hanya berdasarkan keberadaan workflow atau commit. Pemeriksaan status untuk commit terbaru tidak mengembalikan check run yang dapat diverifikasi melalui konektor.

- Clone dan test lokal tidak dapat dilakukan pada lingkungan ini karena akses jaringan container ke GitHub tidak tersedia.
- Workflow validator di repo PRD telah diperbarui, tetapi hasil run hijau untuk commit terbaru belum diperoleh pada saat pembaruan ini.
- Extension v1 adalah fondasi generik, bukan reproduksi penuh Zod schema pusattraining. Validasi nested schema, aturan tanggal lintas-field, timezone IANA, dan graph JSON-LD hasil render tetap harus dijalankan di proyek pusattraining.
- Tidak ada perubahan pada repository `arisciwek/pusattraining` karena hak akses tulis tidak tersedia.
