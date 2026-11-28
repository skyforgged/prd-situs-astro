# Astro Component & Block Catalog

> Katalog gabungan komponen dan content block dari tiga proyek Astro: Konsultan SLF, Konsultan SNI/TKDN, dan TNV Certification. Dokumen ini menjadi rujukan pemilihan dan perencanaan komponen untuk proyek Astro lain; bukan kewajiban untuk mengimplementasikan seluruh katalog.

- **Status:** Inventaris awal berbasis kode pada branch `main`.
- **Sumber:** repositori dan jalur file dicantumkan pada bagian sumber.
- **Prinsip:** nama block yang dipakai dalam konten dibedakan dari nama file komponen yang merendernya. Keberadaan file komponen tidak otomatis berarti komponen tersebut terdaftar sebagai block frontmatter.
- **Cakupan:** daftar mencakup block terdaftar, block struktur halaman, komponen UI/shared, dan komponen page/layout yang ditemukan. Fungsi dijelaskan secara ringkas berdasarkan nama dan peran implementasinya; kontrak props rinci perlu ditinjau dari file sumber saat akan diadopsi.

## 1. Model klasifikasi

| Kategori | Makna |
|---|---|
| Content block | Unit konten yang dapat disusun dari data konten/frontmatter dan dikenali oleh renderer. |
| Page-structure block | Unit struktur halaman seperti hero, listing, grid tautan, atau kontak. |
| UI component | Elemen antarmuka yang dipakai oleh block, halaman, atau layout. |
| Page component | Komponen khusus bagian halaman atau homepage. |
| Layout/site component | Kerangka dan navigasi lintas halaman. |
| Utility/renderer | Komponen atau modul pendukung rendering; bukan block editorial yang ditulis penulis konten. |

Nama block SLF/SNI-TKDN menggunakan properti `component`; TNV menggunakan discriminator `type`. Keduanya adalah bentuk implementasi berbeda dan tidak boleh dianggap memiliki kontrak data identik.

## 2. Daftar gabungan content block

Nama pada kolom pertama adalah nama konseptual/identifier konten. Variasi alias atau perbedaan implementasi dicatat pada kolom sumber.

| Nama block | Keterangan | Sumber/implementasi |
|---|---|---|
| `card` | Kartu konten untuk menampilkan judul, ringkasan, dan/atau tautan. | SLF, SNI/TKDN — `ContentCard.astro` |
| `faq` | Kumpulan pertanyaan dan jawaban; dapat ditampilkan sebagai accordion. | SLF, SNI/TKDN — `FaqBlock.astro`; TNV — `type: faq` |
| `cta` | Ajakan bertindak dengan teks dan tautan/aksi. | SLF, SNI/TKDN — `CtaBlock.astro`; TNV — `type: cta` |
| `table` | Informasi dalam bentuk tabel umum. | SLF, SNI/TKDN — `TableBlock.astro` |
| `note` | Catatan, penjelasan tambahan, atau informasi yang perlu ditonjolkan. | SLF, SNI/TKDN — `NoteBlock.astro` |
| `steps` | Urutan langkah untuk prosedur atau instruksi. | SLF, SNI/TKDN — `StepsBlock.astro` |
| `stats` | Angka atau indikator statistik yang ditonjolkan. | SLF, SNI/TKDN — `StatsBlock.astro` |
| `glossary` | Kumpulan istilah beserta definisinya. | SLF, SNI/TKDN — `GlossaryBlock.astro` |
| `quote` | Kutipan atau pernyataan yang ditampilkan secara khusus. | SLF, SNI/TKDN — `QuoteBlock.astro` |
| `section` | Bagian editorial artikel dengan struktur heading dan isi. | SLF, SNI/TKDN — `ArticleSectionBlock.astro` |
| `process-timeline` | Proses atau tahapan yang disajikan sebagai linimasa. | SLF, SNI/TKDN — `ProcessTimeline.astro` |
| `checklist-card` | Kartu berisi butir-butir pemeriksaan atau persyaratan. | SLF, SNI/TKDN — `ChecklistCard.astro` |
| `comparison-table` | Perbandingan beberapa opsi, kondisi, atau kriteria dalam tabel. | SLF, SNI/TKDN — `ComparisonTable.astro` |
| `document-list` | Daftar dokumen, berkas, atau persyaratan administratif. | SLF, SNI/TKDN — `DocumentList.astro` |
| `image-panel` | Panel yang menggabungkan gambar dengan teks penjelas. | SLF, SNI/TKDN — `ImagePanel.astro` |
| `feature-card-grid` | Sekumpulan kartu fitur/keunggulan dalam grid. | SLF, SNI/TKDN — `FeatureCardGrid.astro` |
| `stats-grid` | Sekumpulan indikator statistik dalam grid. | SLF, SNI/TKDN — `StatsGrid.astro` |
| `source-links` | Kumpulan tautan sumber, referensi, atau dokumen rujukan. | SLF, SNI/TKDN — `SourceLinks.astro` |
| `contact-panel` | Panel informasi kontak dan cara menghubungi organisasi. | SLF, SNI/TKDN — `ContactPanel.astro`; TNV page block `contact` |
| `multi-step-form` | Formulir interaktif yang dibagi menjadi beberapa tahapan. | SLF — `MultiStepForm.astro`; file tersedia tetapi tidak terdaftar pada registry block SNI/TKDN |
| `page-header` | Header pengantar untuk halaman non-homepage. | SLF, SNI/TKDN — `PageHeaderBlock.astro` |
| `home-hero` | Area hero utama khusus homepage. | SLF, SNI/TKDN — `HomeHeroBlock.astro` |
| `service-list` | Daftar layanan yang tersedia. | SLF, SNI/TKDN — `ServiceListBlock.astro` |
| `home-process` | Penjelasan ringkas proses kerja pada homepage. | SLF, SNI/TKDN — `HomeProcessBlock.astro` |
| `article-list` | Daftar artikel atau konten editorial. | SLF, SNI/TKDN — `ArticleListBlock.astro` |
| `home-cta` | CTA yang dirancang khusus untuk homepage. | SLF, SNI/TKDN — `HomeCtaBlock.astro` |
| `not-found` | Tampilan untuk kondisi halaman atau data tidak ditemukan. | SLF, SNI/TKDN — `NotFoundBlock.astro` |
| `content-section` | Section editorial generik dengan judul, deskripsi, item, dan pilihan layout. | TNV — `type: content-section` |
| `howto` | Panduan prosedural berisi langkah-langkah; mendukung layout steps, timeline, dan compact. | TNV — `type: howto` |
| `hero` | Struktur hero halaman dengan eyebrow, judul, deskripsi, dan gambar. | TNV page structure — `type: hero` |
| `link-grid` | Grid tautan ke halaman, layanan, atau sumber lain. | TNV page structure — `type: link-grid` |
| `listing` | Deklarasi daftar koleksi, dengan sumber services, trainings, schedules, atau articles. | TNV page structure — `type: listing`; penanganan listing dilakukan route terkait, bukan renderer editorial generik |
| `upcoming-schedules` | Deklarasi tampilan jadwal pelatihan mendatang. | TNV page structure — `type: upcoming-schedules`; schema didefinisikan, rendering dapat dilakukan oleh komponen/route khusus |
| `contact` | Page-structure block untuk informasi kontak. | TNV page structure — `type: contact` |

### 2.1 Variasi layout dan variant block

Variasi berikut merupakan opsi dari block induk, bukan block baru.

| Block | Opsi | Keterangan |
|---|---|---|
| `content-section` | `numbered-grid` | Item ditampilkan dalam grid bernomor. |
| `content-section` | `editorial` | Item disusun sebagai uraian editorial. |
| `content-section` | `bento` | Grid kartu dengan penekanan ukuran/ruang pada item tertentu. |
| `content-section` | `highlight` | Item disajikan sebagai poin-poin yang ditonjolkan. |
| `content-section` | `feature-list` | Daftar fitur dengan penanda visual. |
| `content-section` | `comparison` | Dua item ditampilkan berdampingan untuk perbandingan. |
| `howto` | `steps` | Langkah-langkah berurutan. |
| `howto` | `timeline` | Langkah disajikan sebagai linimasa. |
| `howto` | `compact` | Penyajian langkah yang lebih ringkas. |
| `cta` | `primary` | CTA utama. |
| `cta` | `secondary` | CTA sekunder dengan penekanan visual lebih ringan. |
| `cta` | `ghost` | CTA bergaya tautan/teks. |
| `content-section.surface` | `white`, `blue`, `navy`, `mint`, `coral`, `cream` | Pilihan permukaan/tema section pada implementasi TNV. |

## 2.2 Kontrak data dan status renderer yang telah diverifikasi

Bagian ini merangkum kontrak yang dapat dibaca langsung dari registry dan schema sumber. Ringkasan ini bukan pengganti schema/TypeScript asli.

### A. Registry SLF dan SNI/TKDN

Kedua proyek menggunakan registry `src/components/blocks.ts` dengan pola `component` sebagai discriminator. Hasil pemeriksaan file registry:

| Identifier | Komponen renderer | SLF | SNI/TKDN | Catatan |
|---|---|---:|---:|---|
| `card` | `ContentCard` | Ya | Ya | Kartu konten generik. |
| `faq` | `FaqBlock` | Ya | Ya | Pertanyaan dan jawaban. |
| `cta` | `CtaBlock` | Ya | Ya | Ajakan bertindak. |
| `table` | `TableBlock` | Ya | Ya | Tabel informasi. |
| `note` | `NoteBlock` | Ya | Ya | Catatan/penekanan informasi. |
| `steps` | `StepsBlock` | Ya | Ya | Langkah berurutan. |
| `stats` | `StatsBlock` | Ya | Ya | Statistik. |
| `glossary` | `GlossaryBlock` | Ya | Ya | Istilah dan definisi. |
| `quote` | `QuoteBlock` | Ya | Ya | Kutipan. |
| `section` | `ArticleSectionBlock` | Ya | Ya | Section editorial artikel. |
| `process-timeline` | `ProcessTimeline` | Ya | Ya | Tahapan proses berbentuk timeline. |
| `checklist-card` | `ChecklistCard` | Ya | Ya | Checklist persyaratan/pemeriksaan. |
| `comparison-table` | `ComparisonTable` | Ya | Ya | Tabel komparasi. |
| `document-list` | `DocumentList` | Ya | Ya | Daftar dokumen. |
| `image-panel` | `ImagePanel` | Ya | Ya | Gambar dan penjelasan. |
| `feature-card-grid` | `FeatureCardGrid` | Ya | Ya | Grid kartu fitur. |
| `stats-grid` | `StatsGrid` | Ya | Ya | Grid statistik. |
| `source-links` | `SourceLinks` | Ya | Ya | Tautan sumber/referensi. |
| `contact-panel` | `ContactPanel` | Ya | Ya | Panel kontak. |
| `page-header` | `PageHeaderBlock` | Ya | Ya | Header halaman internal. |
| `home-hero` | `HomeHeroBlock` | Ya | Ya | Hero homepage. |
| `service-list` | `ServiceListBlock` | Ya | Ya | Daftar layanan. |
| `home-process` | `HomeProcessBlock` | Ya | Ya | Proses kerja di homepage. |
| `article-list` | `ArticleListBlock` | Ya | Ya | Daftar artikel. |
| `home-cta` | `HomeCtaBlock` | Ya | Ya | CTA homepage. |
| `not-found` | `NotFoundBlock` | Ya | Ya | Tampilan tidak ditemukan. |
| `multi-step-form` | `MultiStepForm` | Ya | Tidak | Hanya terdaftar pada registry SLF. |

**Kesimpulan registry:** ada 26 identifier yang sama pada kedua proyek dan satu identifier tambahan (`multi-step-form`) pada SLF. Registry adalah bukti utama status block; keberadaan komponen di folder tidak boleh dipakai untuk menyimpulkan bahwa ia terdaftar.

Sumber verifikasi:
- SLF: [`src/components/blocks.ts`](https://github.com/skyforgged/konsultan-slf/blob/main/src/components/blocks.ts)
- SNI/TKDN: [`src/components/blocks.ts`](https://github.com/skyforgged/konsultan-sni-tkdn/blob/main/src/components/blocks.ts)

### B. Kontrak editorial TNV

TNV menggunakan discriminator `type`, bukan `component`. Berdasarkan schema Zod di `src/content.config.ts`, kontrak editorial yang dipakai `BlockRenderer.astro` adalah:

| Type | Field utama | Field opsional / variasi | Perilaku |
|---|---|---|---|
| `content-section` | `title` | `id`, `surface`, `layout`, `eyebrow`, `description`, `items[]` | Section editorial dengan pilihan layout. Setiap item berisi `title` dan `description`. |
| `faq` | `items[]` berisi `question` dan `answer` | `id`, `surface` | FAQ dengan elemen disclosure/details. Minimal satu item. |
| `howto` | `steps[]` berisi `title` dan `description` | `id`, `surface`, `layout`, `title`; setiap step dapat memiliki `image` | Panduan langkah demi langkah; minimal satu step. |
| `cta` | Tidak ada satu field teks yang wajib selain struktur objek | `id`, `surface`, `variant`, `title`, `description`, `link` | CTA dengan varian primary/secondary/ghost; link, bila ada, memiliki label. |

Nilai enum yang terverifikasi:
- `surface`: `white`, `blue`, `navy`, `mint`, `coral`, `cream`.
- `content-section.layout`: `numbered-grid`, `editorial`, `bento`, `highlight`, `feature-list`, `comparison`.
- `howto.layout`: `steps`, `timeline`, `compact`.
- `cta.variant`: `primary`, `secondary`, `ghost`.
- `id`: format lowercase kebab-case.

### C. Kontrak page-structure TNV

| Type | Field utama | Field opsional / variasi | Status rendering generik |
|---|---|---|---|
| `hero` | `title`, `description` | `id`, `surface`, `eyebrow`, `image`, `imageAlt` | Dirender oleh `PageHero` melalui `PageBlockRenderer`. |
| `link-grid` | `items[]`, setiap item memiliki `title` dan `href` | `id`, `surface`, `eyebrow`, `title`; item dapat memiliki `eyebrow`, `description`, `actionLabel` | Dirender oleh `LinkGrid` melalui `PageBlockRenderer`. |
| `listing` | `source` | `id`, `surface`, `eyebrow`, `title`, `description`, teks/tautan empty state dan action | Didefinisikan di schema, tetapi sengaja tidak dirender oleh `PageBlockRenderer`; markup item disediakan route terkait. |
| `upcoming-schedules` | `title` | `id`, `surface`, `eyebrow`, `description`, empty state | Didefinisikan di schema; tidak termasuk cabang renderer generik `PageBlockRenderer`. |
| `contact` | `title` | `id`, `surface`, `eyebrow`, `description`, `labels` untuk email/phone/address | Dirender oleh `ContactPanel` melalui `PageBlockRenderer`. |

Nilai `listing.source` yang diizinkan: `services`, `trainings`, `schedules`, `articles`.

**Penting:** schema yang menerima sebuah type tidak membuktikan bahwa renderer generik menampilkan type tersebut. Untuk TNV, `listing` dan `upcoming-schedules` adalah contoh eksplisit: schema tersedia, tetapi rendering ditangani di luar alur generik atau belum menjadi cabang renderer tersebut.

Sumber verifikasi:
- [TNV — content schema](https://github.com/skyforgged/tnvcertification/blob/main/src/content.config.ts)
- [TNV — editorial renderer](https://github.com/skyforgged/tnvcertification/blob/main/src/components/BlockRenderer.astro)
- [TNV — page renderer](https://github.com/skyforgged/tnvcertification/blob/main/src/components/page/PageBlockRenderer.astro)

### D. Pemisahan koleksi konten dan block

TNV memakai schema block yang sama untuk field `blocks` pada `articles`, `services`, `training`, dan `pages`. Namun, tidak semua collection adalah halaman editorial:
- `articles`, `services`, `training`, dan `pages` dapat memiliki `blocks`.
- `trainingSchedules` adalah data event/jadwal dengan schema tersendiri, bukan halaman editorial berbasis block.
- `categories` adalah record taksonomi, bukan halaman editorial.
- `certifications` memakai base entry schema tetapi tidak mendeklarasikan `blocks` pada schema collection saat ini.

Jangan menyimpulkan bahwa semua collection otomatis menerima seluruh block hanya karena beberapa collection memakai `pageBlockSchema`.

---

## 3. Daftar gabungan UI component

Komponen berikut dapat digunakan oleh block, halaman, atau layout. Nama file adalah nama implementasi yang ditemukan; komponen dengan fungsi serupa tidak otomatis memiliki props atau API yang sama.

| Nama komponen | Keterangan | Sumber |
|---|---|---|
| `ArticleCard` | Kartu ringkasan artikel. | SLF, SNI/TKDN, TNV |
| `ArticleListBlock` | Komponen daftar artikel; juga terdaftar sebagai block di SLF/SNI-TKDN. | SLF, SNI/TKDN |
| `ArticlePreviousArticles` | Navigasi/daftar artikel sebelumnya. | SLF, SNI/TKDN |
| `ArticleRelatedArticles` | Daftar artikel yang terkait dengan artikel aktif. | SLF, SNI/TKDN |
| `ArticleSectionBlock` | Komponen section editorial artikel; terkait dengan block `section`. | SLF, SNI/TKDN |
| `Badge` | Label ringkas untuk status, kategori, atau penanda. | SLF, SNI/TKDN |
| `Button` | Tombol UI dengan gaya konsisten. | SLF, SNI/TKDN |
| `ButtonLink` | Tautan yang ditampilkan dengan gaya tombol. | TNV |
| `BlockShell` | Pembungkus visual/struktur untuk block. | SNI/TKDN |
| `Breadcrumbs` | Navigasi hierarki halaman. | TNV |
| `ChecklistCard` | Kartu checklist. | SLF, SNI/TKDN |
| `ComparisonTable` | Tabel perbandingan. | SLF, SNI/TKDN |
| `ContactPanel` | Panel kontak. | SLF, SNI/TKDN, TNV page |
| `Container` | Pembatas lebar dan alignment konten. | TNV |
| `ContentCard` | Kartu konten umum. | SLF, SNI/TKDN |
| `CtaBlock` | Komponen CTA. | SLF, SNI/TKDN |
| `CtaSection` | Section CTA yang digunakan oleh renderer TNV. | TNV |
| `DocumentList` | Daftar dokumen/persyaratan. | SLF, SNI/TKDN |
| `Dropdown` | Menu atau pilihan yang dapat dibuka-tutup. | SLF, SNI/TKDN |
| `FaqBlock` | Komponen FAQ. | SLF, SNI/TKDN |
| `FeatureCardGrid` | Grid kartu fitur. | SLF, SNI/TKDN |
| `FeaturedImage` | Gambar utama artikel/halaman. | TNV |
| `GlossaryBlock` | Komponen glosarium. | SLF, SNI/TKDN |
| `HomeCtaBlock` | CTA homepage. | SLF, SNI/TKDN |
| `HomeHero` | Hero homepage. | TNV |
| `HomeHeroBlock` | Hero homepage pada sistem block SLF/SNI-TKDN. | SLF, SNI/TKDN |
| `HomeLinkGrid` | Grid tautan homepage. | TNV |
| `HomeListingSection` | Section listing pada homepage. | TNV |
| `HomeProcessBlock` | Section proses kerja homepage. | SLF, SNI/TKDN |
| `ImagePanel` | Panel gambar dan teks. | SLF, SNI/TKDN |
| `LanguageFlag` | Penanda visual bahasa. | TNV |
| `LanguageSwitcher` | Pengalih bahasa. | TNV |
| `LinkGrid` | Grid tautan pada halaman. | TNV |
| `ListingSection` | Section untuk menampilkan daftar koleksi. | TNV |
| `MainMenuHero` | Hero untuk menu atau halaman kategori utama. | TNV |
| `Modal` | Dialog overlay untuk informasi atau interaksi. | SLF, SNI/TKDN |
| `MultiStepForm` | Formulir multi-tahap. | SLF |
| `NotFoundBlock` | Tampilan kondisi tidak ditemukan. | SLF, SNI/TKDN |
| `NoteBlock` | Komponen catatan. | SLF, SNI/TKDN |
| `PageHeaderBlock` | Header halaman. | SLF, SNI/TKDN |
| `PageHero` | Hero untuk halaman internal. | TNV |
| `PageUpdatedArticles` | Informasi/daftar artikel yang diperbarui. | SLF, SNI/TKDN |
| `ProcessTimeline` | Linimasa proses. | SLF, SNI/TKDN |
| `QuoteBlock` | Komponen kutipan. | SLF, SNI/TKDN |
| `RelatedArticles` | Daftar artikel terkait. | SLF, SNI/TKDN |
| `Section` | Pembungkus section halaman. | TNV |
| `SectionHeading` | Heading/judul section. | TNV |
| `ServiceCard` | Kartu ringkasan layanan. | SNI/TKDN, TNV |
| `ServiceListBlock` | Daftar layanan. | SLF, SNI/TKDN |
| `SiteFooter` | Footer situs. | SLF, SNI/TKDN, TNV |
| `SiteHeader` | Header dan navigasi utama situs. | SLF, SNI/TKDN, TNV |
| `SourceLinks` | Kumpulan tautan sumber/referensi. | SLF, SNI/TKDN |
| `StatsBlock` | Tampilan statistik. | SLF, SNI/TKDN |
| `StatsGrid` | Grid statistik. | SLF, SNI/TKDN |
| `StepsBlock` | Komponen langkah-langkah. | SLF, SNI/TKDN |
| `TableBlock` | Tabel umum. | SLF, SNI/TKDN |
| `TestimonialGrid` | Grid testimoni. | SLF, SNI/TKDN |
| `TrainingCard` | Kartu program pelatihan. | TNV |
| `TrainingScheduleMonths` | Pengelompokan/penyajian jadwal pelatihan per bulan. | TNV |
| `UpcomingSchedules` | Komponen jadwal mendatang. | TNV |

## 3.1 Kontrak props komponen terverifikasi (sampel lintas proyek)

Bagian ini mulai mendokumentasikan API komponen yang dibaca dari implementasi aktual. Sebagian komponen SLF/SNI-TKDN mengambil props langsung dari `Astro.props` tanpa deklarasi interface TypeScript; karena itu tipe di bawah hanya dinyatakan sejauh dapat dibuktikan dari penggunaan di dalam file. Jangan memperlakukan props yang belum disebut sebagai tidak didukung.

### A. Komponen konten bersama — SLF dan SNI/TKDN

| Komponen | Props yang terverifikasi | Struktur data / perilaku | Sumber |
|---|---|---|---|
| `ContentCard` | `id?`, `heading`, `icon?`, `class?`, `body?` | `body` adalah array bagian bertipe `p`, `list`, atau `image`. Paragraf memakai `text`; list memakai `items`, `ordered?`; image memakai `src`, `alt`, `caption?`. Bagian dapat memiliki class tambahan. | SLF `shared/ContentCard.astro` |
| `FaqBlock` | `id?`, `heading?`, `items`, `class?` | Setiap item memakai `question` dan `answer`. Render menggunakan `details/summary` native, sehingga disclosure tetap berbasis HTML. | SLF `shared/FaqBlock.astro` |
| `CtaBlock` | `id?`, `heading?`, `message`, `button?`, `serviceHref?`, `serviceLabel?`, `class?` | CTA memakai konfigurasi situs untuk WhatsApp. `button` memiliki default dari UI config; `serviceLabel` default ke `button`. Link layanan dan WhatsApp dapat ditampilkan terpisah. | SLF `shared/CtaBlock.astro` |
| `NoteBlock` | `id?`, `variant?`, `title?`, `text?`, `class?` | `variant` default `info`; varian yang ditemukan: `info`, `success`, `warning`, `danger`. Judul dapat memakai label default dari UI config. | SLF `shared/NoteBlock.astro` |
| `StepsBlock` | `id?`, `heading?`, `items`, `class?` | Setiap item menggunakan `title` dan `text`; nomor urut dihasilkan otomatis. | SLF `shared/StepsBlock.astro` |
| `TableBlock` | `id?`, `heading?`, `head`, `rows`, `class?` | `head` adalah array string; `rows` adalah array dari array string. Tabel dibungkus area horizontal-scroll untuk layar sempit. | SLF `shared/TableBlock.astro` |
| `ContactPanel` | `id`, `title`, `intro`, `hoursTitle`, `hours: string[]`, `formTitle`, `serviceOptions: string[]` | Identitas organisasi, nomor telepon/WhatsApp, alamat, dan label bersama dibaca dari konfigurasi situs; bukan dikirim ulang sebagai props halaman. | SLF `shared/ContactPanel.astro` |
| `MultiStepForm` | `id?`, `heading`, `intro?`, `submitLabel?`, `successMessage?`, `steps?` | Default `id = msf`, `submitLabel = Kirim`, `steps = []`. Struktur internal setiap step/field perlu mengikuti implementasi lengkap; jangan menebak skema field dari nama komponen. | SLF `shared/MultiStepForm.astro` |

Catatan styling: beberapa komponen menerima prop `class` sebagai objek slot kelas, misalnya `class.section`, `class.heading`, `class.list`, dan slot khusus lainnya. Ini bukan selalu string CSS class biasa. Periksa komponen tujuan sebelum menyalin pola props tersebut.

### B. Komponen page, kartu, dan media — TNV Certification

| Komponen | Props terverifikasi | Perilaku / batasan | Sumber |
|---|---|---|---|
| `PageHero` | `block: HeroBlock`, `fallbackImage: { src, alt }`, flag opsional: `isHomepage`, `isServices`, `isCsms`, `isTrainings`, `isArticles`, `isAbout` | Mengonsumsi objek block hero, fallback image, serta konteks jenis halaman. Tidak setara otomatis dengan `HomeHeroBlock` SLF. | TNV `page/PageHero.astro` |
| `LinkGrid` | `block: LinkGridBlock` | Menerima objek block, bukan daftar props terpisah. Bentuk item mengikuti schema `link-grid` di `content.config.ts`. | TNV `page/LinkGrid.astro` |
| `ContactPanel` | `block: ContactBlock` | Informasi organisasi berasal dari konfigurasi `organization.contact`; block dapat mengubah judul dan label melalui schema. | TNV `page/ContactPanel.astro` |
| `ArticleCard` | `article: Article`, `headingLevel?: 2 \| 3` | Heading default `h3`; menerima objek artikel domain, bukan title/href sederhana. Format tanggal mengikuti bahasa artikel. | TNV `ArticleCard.astro` |
| `ServiceCard` | `title`, `description`, `href`, `label?` | `label` default `Layanan`. Kartu tautan layanan sederhana. | TNV `ServiceCard.astro` |
| `TrainingCard` | `title`, `description`, `href`, `label?` | `label` default `Program pelatihan`. Serupa secara visual dengan ServiceCard, tetapi konteks kontennya berbeda. | TNV `TrainingCard.astro` |
| `LanguageSwitcher` | `lang: string` | Mengambil opsi bahasa berdasarkan pathname aktif melalui `getLanguageOptions`; bukan sekadar daftar bahasa statis. | TNV `LanguageSwitcher.astro` |
| `FeaturedImage` | `src`, `alt`, `width?`, `height?`, `aspect?`, `fit?`, `priority?`, `class?` | Default dimensi 1200×675, aspect `video`, fit `cover`, priority `false`; aspect: `video` atau `fourThree`; fit: `cover` atau `contain`. | TNV `FeaturedImage.astro` |

### C. Contoh bentuk pemakaian (ilustratif, bukan kontrak lintas-proyek)

Contoh berikut menunjukkan bentuk data yang sesuai dengan implementasi SLF yang diperiksa. Nama field harus tetap dicocokkan dengan registry/schema proyek tempat komponen akan dipakai.

```yaml
blocks:
  - component: faq
    heading: Pertanyaan umum
    items:
      - question: Apa persyaratannya?
        answer: Persyaratan mengikuti kondisi dan jenis bangunan.

  - component: note
    variant: warning
    title: Perlu diperhatikan
    text: Pastikan dokumen pendukung telah diperiksa.

  - component: steps
    heading: Tahapan proses
    items:
      - title: Pemeriksaan awal
        text: Meninjau data dan dokumen yang tersedia.
      - title: Pelaksanaan
        text: Melaksanakan pekerjaan sesuai ruang lingkup.
```

Contoh ini hanya untuk bentuk struktur. Ia tidak menyatakan bahwa semua proyek menggunakan discriminator `component`; TNV menggunakan `type` dan kontrak tersendiri.

### D. Aturan adopsi API komponen

1. Ambil props dari source component dan schema/registry pada commit yang sama.
2. Jika komponen memakai objek domain (misalnya `article: Article` atau `block: HeroBlock`), gunakan tipe domain tersebut; jangan meratakan menjadi props baru tanpa adapter yang disengaja.
3. Jika komponen membaca konfigurasi global seperti identitas organisasi, tandai dependensi tersebut sebelum mengadopsinya ke situs lain.
4. Dokumentasikan default props dan enum yang benar-benar ada di source.
5. Bedakan prop wajib dari prop yang hanya tampak dipakai; jika tidak ada deklarasi tipe, tandai tipe sebagai perlu verifikasi.
6. Untuk komponen interaktif, catat sumber state, validasi, submit destination, status penyimpanan data, keyboard behavior, dan pesan sukses/error sebelum dianggap siap dipakai ulang.
7. Contoh YAML di katalog adalah ilustrasi struktur, bukan jaminan lolos validasi tanpa pemeriksaan schema proyek target.

---

## 3.2 Kontrak komponen lintas kategori yang telah diperiksa

Bagian ini mencatat implementasi konkret yang diperiksa langsung pada file sumber. Props yang disebutkan di bawah adalah kontrak yang terlihat pada implementasi saat audit; bukan berarti seluruh komponen dengan nama serupa di tiga proyek memiliki API identik.

### A. SEO, structured data, dan navigasi lokasi

| Komponen | Proyek / file | API terverifikasi | Perilaku dan batasan |
|---|---|---|---|
| `SeoJsonLd` | SNI/TKDN — `src/components/SeoJsonLd.astro` | `data: Record<string, unknown>` | Serialisasi objek JSON-LD ke `application/ld+json`; karakter `<` di-escape menjadi `\\u003c`. Komponen ini hanya mencetak schema yang diberikan; tidak membangun graph, memvalidasi vocabulary, atau menentukan entitas. |
| `HowTo` | SNI/TKDN — `src/components/HowTo.astro` | `title`, `description`, `steps: { title, text }[]` | Menghasilkan konten langkah berurutan dan JSON-LD `HowTo` dengan `HowToStep`. Kicker/catatan berasal dari `siteConfig`; id heading masih statis (`howto-title`), sehingga perlu diperbaiki jika dipakai lebih dari sekali pada satu halaman. |
| `FAQ` | SNI/TKDN — `src/components/FAQ.astro` | `items: { question, answer }[]`, `title?` | FAQ terlihat menggunakan native `details/summary`. Judul default dan kicker bergantung pada `siteConfig`. Komponen visual ini tidak otomatis menyisipkan FAQPage JSON-LD pada file yang diperiksa. |
| `Breadcrumbs` | TNV — `src/components/Breadcrumbs.astro` | `items: { label, href? }[]`, `lang?: "id" \| "en"` | Breadcrumb visual dengan `nav`, `ol`, dan `aria-current="page"` pada item akhir. Label navigasi bilingual. File ini tidak menghasilkan BreadcrumbList JSON-LD; schema harus ditangani terpisah. |

**Keputusan arsitektur:** pisahkan komponen visual breadcrumb/FAQ dari generator JSON-LD. Satu komponen boleh merender keduanya hanya bila kontrak dan validasi data menjamin bahwa konten schema identik dengan konten yang benar-benar terlihat. `SeoJsonLd` sebaiknya tetap menjadi komponen output generik, sementara pembentuk schema per tipe entitas berada di helper/factory yang diuji.

### B. Header, footer, dan navigasi

| Komponen | Proyek / file | API terverifikasi | Perilaku dan batasan |
|---|---|---|---|
| `SiteHeader` | SLF — `src/components/shared/SiteHeader.astro` | `variant?: "default" \| "home"`, `ariaLabel?` | Memilih menu dan CTA dari `ui.nav` berdasarkan variant; logo dan alt dari konfigurasi brand. Tidak menerima daftar menu secara langsung. |
| `SiteHeader` | SNI/TKDN — `src/components/shared/SiteHeader.astro` | `variant?`, `ariaLabel?` | Navigasi, brand, dan CTA dibaca dari `siteConfig`; menu seluler memakai native `details`. Active state membandingkan pathname secara persis. |
| `SiteHeader` | TNV — `src/components/SiteHeader.astro` | `lang: string` | Menggunakan konfigurasi organisasi/navigation, menentukan active route dengan prefix untuk halaman layanan, serta menyertakan `LanguageSwitcher`. API dan perilaku multilingual spesifik proyek. |
| `SiteFooter` | SLF — `src/components/shared/SiteFooter.astro` | `ariaLabel?`, `group?: "slf" \| "pbg"`, `serviceTitle?` | Mengambil collection layanan aktif untuk menyusun tagline dinamis; kontak, alamat, logo, dan navigasi berasal dari konfigurasi global. Menggunakan `getCollection`, sehingga bukan footer presentasional murni. |
| `SiteFooter` | SNI/TKDN — `src/components/shared/SiteFooter.astro` | `ariaLabel?`, `brandCopy?` (string atau array) | Link layanan dan eksplorasi berasal dari `siteConfig`; menerima override copy brand. |
| `SiteFooter` | TNV — `src/components/SiteFooter.astro` | `lang: string`, `description?` | Navigasi footer berkelompok dan diterjemahkan sesuai bahasa; organisasi dan pengaturan situs berasal dari modul konfigurasi. |

**Keputusan arsitektur:** standardisasi struktur aksesibilitas (landmark, label navigasi, fokus keyboard, active state, mobile behavior), bukan memaksakan satu API header/footer. Data menu, bahasa, identitas brand, CTA, dan sumber kontak harus diinjeksi melalui konfigurasi/site adapter proyek.

### C. Kartu artikel, layanan, dan program

| Komponen | Proyek / file | API terverifikasi | Perilaku dan batasan |
|---|---|---|---|
| `ArticleCard` | SLF — `src/components/shared/ArticleCard.astro` | `article: CollectionEntry<"articles">`, `headingLevel?: 2 \| 3` | Mengonsumsi entry Astro Content langsung; URL dibentuk dari `article.data.slug`; tanggal memakai locale UI dan zona `Asia/Jakarta`. Alt gambar kosong pada implementasi ini, sehingga gambar kartu diperlakukan dekoratif. |
| `ArticleCard` | TNV — `src/components/ArticleCard.astro` | `article: Article`, `headingLevel?: 2 \| 3` | Mengonsumsi model domain Article; URL dibentuk dari slug; gambar wajib memakai `featuredImage.src/alt`; tanggal mengikuti bahasa artikel dan UTC. |
| `ServiceListBlock` | SLF — `src/components/shared/ServiceListBlock.astro` | `id?`, `eyebrow?`, `heading?`, `description?`, `variant?: "listing" \| "home"`, `columns?: 2 \| 3`, `showBenefits?: boolean` | Mengambil collection services sendiri, menyaring draft/status aktif, mengurutkan `order`, dan opsional mengambil tiga benefit pertama dari `feature-card-grid`. Sangat terikat pada schema collection dan slug layanan SLF. |
| `ServiceCard` | TNV — `src/components/ServiceCard.astro` | `title`, `description`, `href`, `label?` | Kartu presentasional sederhana dengan label default “Layanan”. |
| `ServiceCard` | SNI/TKDN — `src/components/ServiceCard.astro` | `title`, `description`, `href`, `eyebrow`, `number?` | Elemen akar berupa tautan; eyebrow wajib, nomor default `01`. Kontrak tidak sama dengan TNV. |
| `TrainingCard` | TNV — `src/components/TrainingCard.astro` | `title`, `description`, `href`, `label?` | Kartu program pelatihan; label default “Program pelatihan”. |

**Keputusan arsitektur:** kartu generik sebaiknya menerima view-model eksplisit (`title`, `summary`, `href`, `image?`, `date?`, `eyebrow?`) atau adapter dari model domain. Jangan membuat satu komponen generik bergantung langsung pada tiga bentuk data Article/Service yang berbeda.

### D. Statistik, fitur, checklist, dan testimoni

| Komponen | Proyek / file | API terverifikasi | Perilaku dan batasan |
|---|---|---|---|
| `StatsBlock` | SLF — `src/components/shared/StatsBlock.astro` | `id?`, `heading?`, `items: { value, label }[]`, `class?` | Komponen section; `class` merupakan object slot seperti `section`, `heading`, `grid`, `item`, `value`, dan `label`, bukan sekadar string CSS. |
| `StatsGrid` | SLF — `src/components/shared/StatsGrid.astro` | `id: string`, `items: { value: string, label: string }[]` | Grid statistik presentasional; label aksesibilitas berasal dari `ui.stats`. |
| `FeatureCardGrid` | SLF — `src/components/shared/FeatureCardGrid.astro` | `id`, `title`, `columns?: 2 \| 3`, `items: { title, description?, points? }[]` | Section fitur dengan heading dan daftar poin opsional. |
| `ChecklistCard` | SLF — `src/components/shared/ChecklistCard.astro` | `id`, `title`, `description?`, `items: { label, detail?, required? }[]`, `note?` | Checklist informatif; teks label wajib berasal dari UI config. Tanda centang bersifat dekoratif, bukan input interaktif. |
| `TestimonialGrid` | SLF — `src/components/shared/TestimonialGrid.astro` | `id`, `title`, `items: { quote, name, industry }[]` | Menampilkan kutipan dan atribusi. Tidak ada rating, foto, verifikasi identitas, atau schema review pada implementasi yang diperiksa. Jangan menambahkan klaim review terstruktur tanpa dasar dan kebijakan validasi. |

### E. Interaksi dan elemen kontrol

| Komponen | Proyek / file | API terverifikasi | Perilaku dan batasan |
|---|---|---|---|
| `Modal` | SLF — `src/components/shared/Modal.astro` | `id`, `open?: boolean`, `title?`, `size?: "sm" \| "md" \| "lg" \| "xl"`; slot konten | Menggunakan native `dialog`, `showModal()`, tombol penutup `form method="dialog"`, klik backdrop, dan trigger berbasis `data-modal-open`. Inisialisasi script mencari seluruh `[data-modal]`; perlu uji beberapa instance, focus return, Escape, dan integrasi navigasi keyboard saat adopsi. |
| `Dropdown` | SLF — `src/components/shared/Dropdown.astro` | `label?`, `align?: "left" \| "right"`; slot | Menggunakan native `details/summary`; tanpa state JavaScript. Konten slot diposisikan absolut. Perlu memastikan perilaku tutup saat klik di luar bila kebutuhan UI mensyaratkannya. |
| `Button` | SLF — `src/components/shared/Button.astro` | `variant?: "primary" \| "secondary" \| "ghost" \| "outline"`, `size?: "sm" \| "md" \| "lg"`, `disabled?`, `type?`; slot | Tombol HTML native; default variant primary, size md, type button. Bukan link; navigasi harus menggunakan komponen link terpisah. |
| `MultiStepForm` | SLF — `src/components/shared/MultiStepForm.astro` | Kontrak tingkat atas telah dicatat pada §3.1; bentuk field/step rinci belum seluruhnya diverifikasi | Jangan mengadopsi sebelum schema field, validasi, state, tujuan submit, status penyimpanan, error/success, dan aksesibilitas keyboard diperiksa bersama script pendukung. |

## 3.3 Matriks adopsi lintas proyek

Status berikut adalah rekomendasi konsolidasi berdasarkan implementasi yang diperiksa, bukan klaim bahwa komponen sudah dipindahkan atau diuji di proyek target.

| Kelompok | Status rekomendasi | Standar bersama yang perlu ditetapkan | Yang harus tetap spesifik proyek |
|---|---|---|---|
| Output JSON-LD | `approved-pattern` | Komponen output aman; escaping; satu sumber data antara konten terlihat dan schema; pengujian JSON parse dan schema | Factory untuk Organization, LocalBusiness, Service, Article, FAQPage, HowTo, BreadcrumbList, dan tipe domain lainnya |
| FAQ / HowTo | `approved-with-adapter` | Kontrak item yang jelas, semantic HTML, heading unik, schema hanya untuk konten yang terlihat | Label UI, copy, dan tipe schema yang sesuai dengan konten aktual |
| Breadcrumbs | `approved-pattern` | Item `label/href`, item terakhir current page, landmark dan urutan navigasi | Terjemahan, strategi URL, dan pembentukan BreadcrumbList |
| Header / footer | `project-specific-shell` | Aksesibilitas, responsive behavior, active state, focus visible, semantic landmarks | Logo, menu, CTA, bahasa, alamat, kontak, footer copy dan sumber data |
| Article / service / training cards | `approved-with-view-model` | Struktur kartu, heading level, link focus, alt gambar, tanggal valid | Adapter dari CollectionEntry Astro, model Article, Service, Training dan pola permalink |
| Statistik / fitur / checklist | `candidate-shared` | Data-driven props, heading/id unik, semantic list, responsive grid | Token visual, label, dan aturan klaim angka |
| Testimonial | `project-specific-until-governed` | Struktur kutipan dan atribusi yang jujur | Bukti persetujuan, identitas, rating, moderasi, dan kebijakan review |
| Modal / dropdown / button | `approved-with-a11y-tests` | Native semantics, keyboard, focus, disabled, ukuran target, state konsisten | Design tokens, trigger convention, dan integrasi form/router |
| Multi-step form | `specialized-component` | Schema field, validasi, keyboard, status, error handling dan submit contract | Alur bisnis, endpoint, persetujuan, penyimpanan, dan kebijakan data |

### Aturan sebelum komponen dipromosikan menjadi standar bersama

1. **API stabil:** props wajib/opsional, default, enum, slot, dan tipe data ditulis eksplisit.
2. **Tidak mengunci konfigurasi:** komponen presentasional menerima data/config lewat props; akses global config atau content collection harus menjadi adapter yang disengaja.
3. **Tidak mengunci model konten:** gunakan adapter dari collection/model domain ke view-model komponen.
4. **SEO tidak boleh implisit:** komponen visual tidak dianggap menghasilkan structured data kecuali benar-benar menyisipkan JSON-LD dan memiliki tes.
5. **Aksesibilitas dapat diuji:** heading hierarchy, landmark, label, keyboard, focus, alt text, dan state interaktif menjadi bagian acceptance criteria.
6. **Multi-instance aman:** hindari id statis dan selector global yang menyebabkan benturan ketika komponen muncul lebih dari sekali.
7. **Bukti implementasi:** catat file, repository, dan commit yang diperiksa; jangan menganggap kesamaan nama sebagai kesamaan kontrak.

## 4. Renderer, layout, dan komponen pendukung

Bagian ini dicatat agar inventaris lengkap, tetapi item-item ini bukan block konten yang seharusnya ditulis langsung oleh editor.

| Nama | Jenis | Keterangan | Sumber |
|---|---|---|---|
| `BlockRenderer` | Renderer | Memetakan identifier block ke komponen implementasi. | SLF, SNI/TKDN, TNV |
| `PageBlockRenderer` | Renderer halaman | Mengelompokkan dan merender page-structure block serta editorial block. | TNV |
| `PageBlocks` | Komponen/renderer | Lapisan komponen page blocks pada proyek SNI/TKDN. | SNI/TKDN |
| `FAQ` | Komponen khusus | Komponen FAQ tingkat atas; bukan identifier registry block `faq` yang sama secara otomatis. | SNI/TKDN |
| `HowTo` | Komponen khusus | Komponen HowTo tingkat atas; jangan disamakan tanpa pemeriksaan dengan renderer `howto` TNV. | SNI/TKDN |
| `RelatedLinks` | Komponen khusus | Penyajian tautan terkait. | SNI/TKDN |
| `SeoJsonLd` | Komponen SEO | Penyisipan structured data JSON-LD. | SNI/TKDN |
| `ServiceCard` | Komponen kartu | Kartu layanan yang digunakan pada daftar/halaman layanan. | SNI/TKDN, TNV |
| `BaseLayout` / `Layout` | Layout | Kerangka dasar dokumen dan halaman. | SLF, SNI/TKDN, TNV |
| `ArticleLayout` | Layout | Kerangka halaman artikel. | SLF, TNV |
| `ServiceLayout` | Layout | Kerangka halaman layanan. | SLF, TNV |
| `WidePageLayout` | Layout | Kerangka halaman dengan area konten lebar. | TNV |
| `TrainingLayout` | Layout | Kerangka halaman program pelatihan. | TNV |
| `ScheduleLayout` | Layout | Kerangka halaman jadwal. | TNV |
| `ScheduleArchiveLayout` | Layout | Kerangka arsip jadwal. | TNV |

## 5. Catatan konsolidasi dan batasan

1. **Jangan menyamakan identifier block dengan nama komponen.** Contoh: `faq` adalah identifier data, sedangkan `FaqBlock.astro` adalah implementasi renderer.
2. **Jangan menyamakan komponen yang kebetulan bernama sama.** `ContactPanel` di SLF/SNI-TKDN dan TNV dapat mempunyai props, markup, styling, dan tanggung jawab berbeda.
3. **Block TNV memakai kontrak berbeda.** TNV menggunakan `type`; SLF/SNI-TKDN menggunakan `component`. Adopsi ke proyek baru harus menetapkan satu kontrak kanonis dan adapter bila perlu.
4. **Ketersediaan file tidak sama dengan registrasi.** Contoh `TestimonialGrid` ada sebagai file tetapi tidak tercantum pada registry block SLF/SNI-TKDN.
5. **Page block yang hanya didefinisikan dalam schema belum tentu dirender oleh renderer generik.** Pada TNV, `listing` dan `upcoming-schedules` didefinisikan dalam schema page, sementara implementasi listing ditangani oleh route/komponen khusus.
6. **Structured data bukan efek otomatis dari nama block.** FAQ, HowTo, dan block lain hanya boleh menghasilkan Schema.org jika kontrak data, konten yang terlihat, validasi, dan kebijakan schema proyek mengizinkannya.
7. **Jangan menganggap daftar ini sebagai API props.** Sebelum implementasi, periksa interface/props, Zod schema, renderer, styling, responsive behavior, dan tests pada sumber.
8. **Jangan mengadopsi komponen bisnis tanpa validasi konteks.** Misalnya form kontak, testimonial, statistik, dan daftar layanan membutuhkan data yang benar-benar tersedia dan disetujui.

## 6. Sumber repositori

Inventaris ini diturunkan dari branch `main` pada tiga repository berikut. Commit sumber yang diperiksa saat penyusunan:

| Repository | Commit | Area sumber utama |
|---|---|---|
| [konsultan-slf](https://github.com/skyforgged/konsultan-slf) | [`288b86c`](https://github.com/skyforgged/konsultan-slf/commit/288b86cce5f1cad82df13abaf71d78535698bf61) | `src/components/blocks.ts`, `src/components/shared/`, `src/components/blocks/BlockRenderer.astro` |
| [konsultan-sni-tkdn](https://github.com/skyforgged/konsultan-sni-tkdn) | [`6b47eae`](https://github.com/skyforgged/konsultan-sni-tkdn/commit/6b47eae2121b9d1d09331e920d27ac5f4ef9ef7c) | `src/components/blocks.ts`, `src/components/shared/`, `src/content.config.ts` |
| [tnvcertification](https://github.com/skyforgged/tnvcertification) | [`1b5f08a`](https://github.com/skyforgged/tnvcertification/commit/1b5f08ae92d9f2d1d81f2d3bfe142b344590ef2b) | `src/components/BlockRenderer.astro`, `src/components/page/`, `src/content.config.ts`, `src/data/pages.ts` |

### File sumber utama

- [SLF — block registry](https://github.com/skyforgged/konsultan-slf/blob/main/src/components/blocks.ts)
- [SLF — shared components](https://github.com/skyforgged/konsultan-slf/tree/main/src/components/shared)
- [SNI/TKDN — block registry](https://github.com/skyforgged/konsultan-sni-tkdn/blob/main/src/components/blocks.ts)
- [SNI/TKDN — shared components](https://github.com/skyforgged/konsultan-sni-tkdn/tree/main/src/components/shared)
- [TNV — content schema](https://github.com/skyforgged/tnvcertification/blob/main/src/content.config.ts)
- [TNV — editorial block renderer](https://github.com/skyforgged/tnvcertification/blob/main/src/components/BlockRenderer.astro)
- [TNV — page block renderer](https://github.com/skyforgged/tnvcertification/blob/main/src/components/page/PageBlockRenderer.astro)

## 7. Pemeliharaan katalog

Saat proyek Astro baru menambah block atau component yang layak dipakai ulang:

- Tambahkan item ke kategori yang tepat.
- Catat identifier konten dan nama file implementasi secara terpisah.
- Cantumkan props/schema, varian, dependensi, accessibility, responsive behavior, structured-data behavior, serta contoh pemakaian.
- Catat repository, path, dan commit sumber.
- Tandai status `candidate`, `approved`, `deprecated`, atau `project-specific`.
- Jangan menghapus varian atau perbedaan implementasi hanya demi menyatukan nama.
- Perbarui katalog setelah perubahan registry/renderer, bukan hanya setelah penambahan file komponen.
