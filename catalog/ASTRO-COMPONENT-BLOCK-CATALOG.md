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
