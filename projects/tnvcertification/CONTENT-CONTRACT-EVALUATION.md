# Evaluasi Content Contract terhadap implementasi TNV Certification

> Status: Snapshot review teknis awal, sebelum revisi standar 2026-11-27\
> Tanggal: 2026-11-26\
> Standar yang diperiksa: Website Constitution 1.3, Content Contract 1.3, Frontmatter Templates 1.2, Quality Gates 0.4\
> Repository implementasi: `skyforgged/tnvcertification`\
> Commit implementasi yang diperiksa: `778bac514124d139eac8bf02367ed6c6c3d7362a`

## Catatan status 2026-11-27

Dokumen ini dipertahankan sebagai snapshot evaluasi terhadap Content Contract 1.3 dan Frontmatter Templates 1.2. Setelah evaluasi ini, standar global direvisi menjadi Content Contract 1.4 lalu 1.5, dan Frontmatter Templates 1.3 lalu 1.4. Field `intro` pada bagian 3 dan rekomendasi pada bagian 4.4 telah ditindaklanjuti pada 1.4: `intro` kini wajib pada Page, Article, dan Service serta dipisahkan dari `seo.description`. Katalog dan registry Schema.org pada bagian 4.3 juga ditindaklanjuti sebagai katalog tipe dan Schema Registry wajib di Content Contract 1.4. Content Contract 1.5 selanjutnya memisahkan page-level schema dari entitas `DefinedTerm`: `schema.type` tetap `WebPage` atau subtype halaman yang tepat, sedangkan entitas istilah dinyatakan di `schema.mainEntity.type: DefinedTerm` dengan `title` sebagai `DefinedTerm.name` dan `intro` sebagai `DefinedTerm.description`. Temuan lain, seperti ID dokumen numerik global, ID block numerik, dan relasi berbasis slug, belum diubah oleh revisi tersebut; jangan membaca dokumen ini sebagai penilaian terhadap standar terbaru.

## 1. Kesimpulan

Implementasi TNV Certification telah membuktikan beberapa pola arsitektur yang baik: content collections memakai schema Zod per jenis, konten editorial disimpan dalam Markdown dengan frontmatter dan blocks, block registry berbentuk discriminated union, relasi artikel-ke-layanan divalidasi secara eksplisit, dan JSON-LD dibangun dari data terstruktur serta konfigurasi situs.

Namun, implementasi ini **belum sepenuhnya sesuai dengan Website Constitution 1.3 dan Content Contract 1.3**. Perbedaannya bukan hanya perbedaan nama field. Ada konflik pada identitas dokumen, foreign key, identitas block, field Schema.org, dan sumber navigasi.

Karena Constitution menyatakan aturan tersebut berlaku lintas proyek, perbedaan ini tidak boleh dianggap sebagai pengecualian yang sah hanya karena build berhasil. Sebaliknya, standar global juga tidak boleh diubah hanya berdasarkan satu implementasi. Rekomendasi saat ini adalah mencatat temuan dan keputusan yang diperlukan, lalu memilih secara eksplisit antara migrasi proyek atau revisi standar setelah pola ini dibandingkan dengan proyek Astro nyata lain.

**Tidak ada dokumen standar global yang diubah dalam evaluasi ini pada tanggal review; tindak lanjut revisi tercatat dalam "Catatan status 2026-11-27" di atas.**

## 2. Bukti implementasi yang diperiksa

Pemeriksaan dilakukan pada file berikut di repository TNV Certification:

- `src/content.config.ts`
- `src/content-validation.ts`
- `src/lib/content-validation.ts`
- `src/lib/article-service-relations.ts`
- `src/lib/block-ids.ts`
- `src/data/collections.ts`
- `src/site.ts`
- `src/lib/structured-data.ts` dan pemanggil structured-data pada route
- Sampel artikel, layanan, dan pelatihan di `src/content/`
- `AGENTS.md` dan `docs/architecture.md`

Validasi nyata pada commit yang diperiksa: GitHub Actions berhasil menjalankan type/Astro checks, lint, tests, production build, audit page images, SEO/link audit, IA audit, dan block-section audit. Hasil IA pada build terbaru: 85 file HTML, 47 halaman indexable, dan 47 URL sitemap. Perbaikan lanjutan menghilangkan warning slug kategori bilingual, konflik route CSMS dengan generic slug route, dan direktori collection yang belum tersedia. [Run CI](https://github.com/skyforgged/tnvcertification/actions/runs/45855726180).

Build tetap menampilkan warning non-blocking tentang direktori collection `certifications` yang belum tersedia, slug kategori bilingual yang sama, dan kandidat route `/[slug]` yang bertabrakan dengan `/csms/[slug]`. Warning ini perlu ditindaklanjuti terpisah dari evaluasi kontrak.

## 3. Matriks kesesuaian

| Area | Standar PRD | Implementasi TNV Certification | Penilaian |
|---|---|---|---|
| Sumber konten | Dokumen konten Markdown dengan frontmatter | Artikel, layanan, training, halaman, kategori, dan jadwal memakai file Markdown | Sesuai secara prinsip |
| Schema per jenis | Schema khusus setiap jenis dokumen | Collection memakai Zod schema terpisah | Sesuai secara prinsip |
| ID dokumen | Integer positif, unik global lintas collection | Field `id` numerik diwajibkan pada service; artikel, training, pages, categories, certifications, dan training schedules tidak memilikinya | **Tidak sesuai** |
| ID block | Integer positif, unik lokal | Block memakai `id` string kebab-case dan opsional | **Tidak sesuai** |
| Relasi | Foreign key numerik ke ID target | Article `serviceId` numerik; categoryIds, relatedServiceSlugs, relatedTrainingSlugs, trainingSlug, dan serviceSlug memakai string slug | **Sebagian sesuai** |
| Schema utama | Field `schema.type` pada setiap dokumen Markdown | Schema.org dirakit melalui fungsi structured-data berdasarkan collection dan data konten; tidak ada field `schema` wajib di frontmatter | **Tidak sesuai secara literal; pola implementasi layak dipertimbangkan untuk standar** |
| SEO | Object `seo` dengan fallback | `metaDescription` menjadi field langsung; title dan canonical ditangani oleh layout/komponen | Perlu pemetaan proyek |
| Tanggal publikasi | `publishedDate` dan `updatedDate` | Menggunakan `pubDate`; `updatedDate` opsional. Validator mewajibkan pubDate untuk konten terbit | Perlu pemetaan proyek; aturan updatedDate berbeda |
| Intro | `description` sebagai ringkasan dokumen | Field `intro` terpisah, wajib, dan harus menjadi paragraf setelah H1/hero | Adaptasi yang lebih ketat dan berguna |
| Featured image | Sesuai jenis konten | Satu object `featuredImage` wajib untuk konten terbit; alt divalidasi terhadap judul | Lebih ketat daripada kontrak umum |
| Block registry | `component` wajib, props sesuai registry | `type` menjadi discriminator; Zod discriminated union memvalidasi props | Sesuai secara fungsi, berbeda nama field |
| Menu/navigasi | Menu yang dikelola sebagai konten disimpan di Markdown | Primary/footer navigation berada di `src/site.ts` | Perlu keputusan apakah ini konfigurasi aplikasi atau konten editorial |
| Body konten | Markdown sebagai sumber konten | Halaman editorial memakai frontmatter blocks tanpa Markdown body | Adaptasi proyek yang telah divalidasi |
| Unknown fields | Field di luar kontrak harus ditolak | Schema menggunakan `z.object`; belum ditemukan bukti fixture yang memastikan unknown top-level fields ditolak | **Belum terbukti; perlu test eksplisit** |

## 4. Temuan yang paling penting

### 4.1 Identitas dokumen dan foreign key

Constitution mewajibkan ID numerik global dan melarang slug menjadi foreign key. Pada implementasi saat ini, hanya layanan yang memiliki ID numerik. Sebagian relasi menggunakan slug eksplisit, misalnya:

- Artikel → layanan: `serviceId` (numerik).
- Artikel → training: `relatedTrainingSlugs` (string).
- Training → layanan: `relatedServiceSlugs` (string).
- Training schedule → training: `trainingSlug` (string).
- Training schedule → layanan: `serviceSlug` (string).
- Konten → kategori: `categoryIds` berisi slug string.

Relasi slug eksplisit tetap lebih baik daripada menebak relasi dari judul atau kemiripan kata, tetapi belum memenuhi kontrak foreign key numerik.

Jika Constitution dipertahankan, proyek memerlukan migrasi bertahap: ID numerik untuk seluruh dokumen, registry/validator keunikan global, lalu migrasi setiap relasi ke ID target. Slug tetap dipertahankan sebagai identitas URL, bukan identitas relasi. Jangan melakukan migrasi massal sebelum inventaris jumlah dokumen, relasi, dan dampak terhadap query selesai.

### 4.2 ID block dan anchor HTML

Block saat ini memakai ID string semantik seperti `hero-layanan` dan `iso9001-area-sistem`. Nilai tersebut dipakai untuk anchor yang dapat dibaca dan stabil ketika urutan block berubah. Standar PRD saat ini mengharuskan ID block integer.

Ada dua pilihan:
1. Pertahankan ID numerik sebagai identitas block dan tambahkan field `anchor` string untuk fragment URL; atau
2. Revisi standar agar block boleh memakai stable string key yang unik dalam dokumen.

Pilihan kedua lebih sederhana untuk authoring, tetapi merupakan perubahan standar dan perlu keputusan eksplisit. Jangan menyamakan ID dokumen global dengan anchor block.

### 4.3 Schema.org yang diturunkan dari tipe konten

Implementasi tidak menulis `schema: { type: ... }` pada setiap frontmatter. Route dan fungsi structured-data menghasilkan graph seperti Service, Article, WebPage, Organization, dan BreadcrumbList berdasarkan collection, konten, serta `site.ts`.

Ini menghindari pengulangan deklarasi schema dan mengurangi risiko frontmatter menyatakan tipe yang bertentangan dengan entitas sebenarnya. Secara teknis, pendekatan ini dapat lebih kuat daripada field bebas, asalkan:
- mapping collection → primary Schema.org type terdokumentasi;
- field JSON-LD hanya diambil dari sumber data kanonis;
- graph diuji dan tidak memuat klaim/properti yang tidak didukung konten terlihat;
- tipe yang tidak dapat ditentukan otomatis dapat di-override melalui keputusan yang tervalidasi.

**Rekomendasi:** pertimbangkan revisi Constitution agar Schema.org utama boleh dideklarasikan di frontmatter atau diturunkan secara deterministik dari content type melalui mapping teknis yang wajib diuji. Ini perlu diuji pada proyek lain sebelum menjadi aturan universal.

### 4.4 Kontrak field dan tanggal

Nama field proyek berbeda dari kontrak standar:
- `intro` dan `metaDescription` menggantikan pola `description` dan object `seo`.
- `pubDate` digunakan sebagai tanggal publikasi.
- `updatedDate` opsional dan sitemap memakai fallback ke pubDate.

Pemisahan intro dan meta description memberi fungsi editorial yang jelas. Sementara itu, optional `updatedDate` mencegah tanggal pembaruan palsu ketika belum ada perubahan substantif. Keduanya layak menjadi masukan revisi standar. Nama `pubDate` sendiri dapat tetap menjadi keputusan proyek jika mapping-nya terdokumentasi.

### 4.5 Menu sebagai konfigurasi aplikasi

Navigasi saat ini menjadi bagian dari `src/site.ts`, yang juga merupakan SSOT identitas dan pengaturan situs. Ini konsisten secara teknis untuk menu statis yang hanya diubah melalui code review, tetapi berbeda dari Constitution yang mengharuskan menu yang tampil sebagai konten dikelola melalui Markdown.

Keputusan perlu membedakan:
- menu editorial yang perlu dikelola editor tanpa perubahan kode; dan
- konfigurasi navigasi struktural yang memang menjadi bagian dari aplikasi.

Jika menu tidak membutuhkan workflow editorial, standar dapat menyediakan pengecualian konfigurasi yang eksplisit. Jika menu harus dapat dikelola editor, pindahkan ke content collection dan gunakan relasi ID.

### 4.6 Unknown fields dan validasi ketat

Schema collection menggunakan `z.object(...)`. Perlu fixture yang mengirim field frontmatter tidak dikenal untuk memastikan build benar-benar gagal. Jangan menganggap penggunaan Zod otomatis berarti unknown field ditolak; perilaku default object schema perlu dikonfirmasi atau dibuat strict secara eksplisit.

## 5. Rekomendasi keputusan

| Prioritas | Keputusan/tindakan | Rekomendasi |
|---|---|---|
| P0 | ID dokumen dan relasi numerik | Pertahankan sebagai aturan Constitution untuk sementara; buat rencana migrasi proyek sebelum menyatakan conformant |
| P0 | ID block | Putuskan apakah memakai numeric ID + anchor terpisah atau mengubah standar menjadi stable string key |
| P1 | Schema.org utama | Uji opsi schema yang diturunkan deterministik dari collection; jangan memaksa duplikasi field tanpa manfaat |
| P1 | Unknown fields | Tambahkan fixture valid/invalid yang membuktikan field asing ditolak |
| P1 | updatedDate | Evaluasi untuk menjadikan updatedDate opsional dengan fallback ke tanggal publikasi |
| P1 | Menu di site.ts | Tetapkan pengecualian konfigurasi atau pindahkan ke Markdown berdasarkan kebutuhan editor |
| P2 | Nama field | Dokumentasikan mapping `pubDate`, `intro`, dan `metaDescription` pada arsitektur proyek |
| P2 | Kategori bilingual | Pastikan ID entry loader unik per bahasa; jangan mengandalkan slug identik dalam satu collection tanpa strategi ID |
| P2 | Block discriminator | Dokumentasikan `type` sebagai padanan proyek untuk `component` |

## 6. Batas kesimpulan

Evaluasi ini tidak mengubah standar global dan tidak menyatakan implementasi TNV Certification telah memenuhi seluruh Quality Gates PRD. Build dan test yang berhasil membuktikan konsistensi terhadap validator proyek yang ada, bukan otomatis kesesuaian terhadap seluruh aturan Constitution.

QG-13 pada implementasi pertama memeriksa route aktual, sitemap, canonical, navigasi, breadcrumb, redirect, dan keluarga route. Setelah review ini, coverage listing juga diperkuat dalam CI: urutan artikel deterministik (effectiveDate, pubDate, file ID, slug), rank homepage 1–3 dan service index 4–6 tanpa duplikasi, relasi artikel berdasarkan serviceId eksplisit, pagination arsip, serta filter/urutan jadwal pelatihan. Cakupan tersebut diuji melalui test suite yang dijalankan bersama audit IA. Yang masih belum menjadi pemeriksaan universal adalah seluruh empty state dan seluruh varian listing pada semua halaman; hal tersebut tetap perlu dipetakan sebelum menyatakan QG-13 lengkap.

QG-12 belum dinilai oleh laporan ini. Penilaian editorial memerlukan review sampel konten nyata terhadap Content Quality Standard, termasuk akurasi, bukti sumber, kedalaman proporsional, orisinalitas, dan manfaat bagi pembaca.

## 7. Tahap berikutnya

1. Setujui keputusan yang menyentuh Constitution (ID, block ID, Schema.org, updatedDate, dan menu).
2. Lengkapi pemetaan kontrak proyek TNV Certification agar semua penyimpangan memiliki alasan dan status yang jelas.
3. Lengkapi cakupan QG-13 untuk listing/related-content dan perubahan route.
4. Lanjutkan review QG-12 pada sampel artikel, layanan, dan training yang sudah dipublikasikan.
