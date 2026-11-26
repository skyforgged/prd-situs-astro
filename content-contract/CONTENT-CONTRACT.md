# Content Contract — PRD Astro

> Status: Standar data konten  
> Versi: 1.1  
> Format sumber: Markdown + YAML frontmatter

## 1. Tujuan

Dokumen ini mendefinisikan kontrak data untuk dokumen konten situs. Setiap jenis konten memiliki kontrak frontmatter tersendiri. Kontrak tidak disatukan menjadi satu skema universal; masing-masing dapat memiliki field wajib, opsional, dan aturan validasi sesuai fungsinya.

Aturan lintas jenis konten seperti ID global, foreign key numerik, sumber Markdown, dan Schema.org mengikuti [Website Constitution](../constitution/WEBSITE-CONSTITUTION.md).

## 2. Aturan umum semua kontrak

Semua dokumen konten—apa pun jenisnya—wajib mematuhi ketentuan berikut:

| Field/aturan | Ketentuan |
|---|---|
| `id` | Wajib, integer positif, unik secara global dalam satu situs |
| `slug` | Wajib untuk entitas yang memiliki URL; string |
| `schema` | Wajib; object dengan `type` Schema.org yang valid |
| `blocks` | Wajib untuk jenis dokumen yang menggunakan sistem block; berupa array berurutan |
| ID block | Wajib integer positif dan unik di dalam dokumen pemiliknya; tidak menggantikan ID dokumen global |
| `component` | Wajib pada setiap block; harus terdaftar di block registry |
| `schema` block | Opsional; object Schema.org jika block memang menyajikan konten yang sesuai |
| Relasi | Foreign key numerik ke ID dokumen target, bukan slug atau judul |

**Catatan tentang ID block:** ID global berlaku untuk identitas dokumen konten. ID block adalah identitas lokal dalam satu dokumen dan tidak ikut memakai ruang ID global dokumen. Kombinasi `document.id + block.id` harus cukup untuk mengidentifikasi block secara stabil.

Field umum di atas tidak berarti semua jenis konten memakai daftar field yang sama. Field selain aturan lintas-kontrak ditetapkan per jenis dokumen di bagian berikut.

## 3. Kontrak Homepage

Homepage adalah dokumen konten khusus untuk route root situs. Konten homepage tetap disimpan dalam Markdown dan tidak boleh ditanam sebagai teks tetap di layout.

### Field

| Field | Wajib | Tipe | Keterangan |
|---|---:|---|---|
| `id` | Ya | integer | ID global |
| `slug` | Ya | string | Identifier konten, misalnya `home`; route tetap dipetakan ke `/` |
| `title` | Ya | string | Judul halaman |
| `description` | Ya | string | Ringkasan homepage |
| `schema` | Ya | object | Schema utama, umumnya `WebPage` atau tipe halaman yang tepat |
| `seo` | Ya | object | Metadata SEO sesuai kontrak SEO proyek |
| `blocks` | Ya | array | Susunan seluruh section homepage |
| `updatedDate` | Ya | datetime | Waktu pembaruan dengan zona waktu |

### Contoh

```yaml
---
id: 1
slug: home
title: Nama Perusahaan
description: Deskripsi singkat perusahaan dan layanan utamanya.
schema:
  type: WebPage
seo:
  title: Nama Perusahaan | Layanan Utama
  description: Deskripsi untuk hasil pencarian.
blocks:
  - id: 1
    component: hero
    title: Solusi untuk kebutuhan Anda
    description: Ringkasan proposisi nilai.
  - id: 2
    component: service-grid
    title: Layanan kami
    serviceIds: [12, 13, 14]
updatedDate: 2026-11-26T03:00:00Z
---
```

## 4. Kontrak Menu dan Navigasi

Menu merupakan konten terkelola, bukan array tautan yang ditulis langsung di komponen. Menu utama, menu footer, atau menu lain disimpan sebagai dokumen Markdown masing-masing.

### Field

| Field | Wajib | Tipe | Keterangan |
|---|---:|---|---|
| `id` | Ya | integer | ID global |
| `slug` | Ya | string | Identifier menu, misalnya `main-navigation` |
| `title` | Ya | string | Nama internal menu |
| `schema` | Ya | object | Schema utama yang sesuai; dapat berupa `SiteNavigationElement` jika tepat |
| `location` | Ya | string/enum | Posisi menu, misalnya `header`, `footer`, `mobile` |
| `items` | Ya | array | Item navigasi sesuai urutan |
| `updatedDate` | Ya | datetime | Waktu pembaruan |

Setiap item menu wajib memiliki label dan target. Target internal harus menggunakan ID numerik konten tujuan; URL eksternal boleh menggunakan URL langsung. Submenu boleh bersarang sesuai batas kedalaman yang ditentukan proyek.

### Contoh

```yaml
---
id: 2
slug: main-navigation
title: Menu Utama
schema:
  type: SiteNavigationElement
location: header
items:
  - label: Beranda
    pageId: 1
  - label: Tentang Kami
    pageId: 20
  - label: Hubungi Kami
    pageId: 21
  - label: Situs mitra
    url: https://example.com
    external: true
updatedDate: 2026-11-26T10:00:00+07:00
---
```

## 5. Kontrak Halaman

Digunakan untuk halaman informasional atau halaman statis yang bukan homepage, artikel, atau layanan.

### Field

| Field | Wajib | Tipe | Keterangan |
|---|---:|---|---|
| `id` | Ya | integer | ID global |
| `slug` | Ya | string | Segmen URL |
| `title` | Ya | string | Judul halaman |
| `description` | Ya | string | Ringkasan halaman |
| `schema` | Ya | object | Schema utama, misalnya `AboutPage`, `ContactPage`, atau `WebPage` |
| `seo` | Ya | object | Metadata SEO |
| `featuredImage` | Sesuai kebutuhan | object | Gambar utama beserta alt deskriptif |
| `blocks` | Ya | array | Konten halaman |
| `publishedDate` | Sesuai kebutuhan | datetime | Tanggal publikasi bila halaman memiliki siklus publikasi |
| `updatedDate` | Ya | datetime | Waktu pembaruan |

### Contoh

```yaml
---
id: 20
slug: tentang-kami
title: Tentang Kami
description: Profil dan ruang lingkup perusahaan.
schema:
  type: AboutPage
seo:
  title: Tentang Kami
  description: Profil perusahaan dan kompetensinya.
blocks:
  - id: 1
    component: rich-text
    content: Profil perusahaan dan informasi pendukung.
  - id: 2
    component: image
    src: /images/profil.webp
    alt: Tim perusahaan saat melakukan kegiatan konsultasi teknis.
updatedDate: 2026-11-26T10:00:00+07:00
---
```

## 6. Kontrak Artikel

Digunakan untuk artikel, berita, panduan, insight, atau konten editorial. Perbedaan subtype editorial dapat ditambahkan melalui field khusus atau collection terpisah sesuai kebutuhan proyek.

### Field

| Field | Wajib | Tipe | Keterangan |
|---|---:|---|---|
| `id` | Ya | integer | ID global |
| `slug` | Ya | string | Segmen URL |
| `title` | Ya | string | Judul artikel |
| `description` | Ya | string | Ringkasan artikel |
| `schema` | Ya | object | Umumnya `Article` atau subtype yang tepat |
| `seo` | Ya | object | Metadata SEO |
| `authorId` | Opsional | integer | Relasi ke satu dokumen penulis dengan ID numerik |
| `categoryIds` | Sesuai kebutuhan | integer[] | Relasi ke kategori |
| `relatedArticleIds` | Opsional | integer[] | Relasi artikel terkait |
| `relatedServiceId` | Opsional | integer | Relasi ke layanan utama |
| `featuredImage` | Ya | object | Gambar utama dan alt deskriptif |
| `publishedDate` | Ya | datetime | Tanggal publikasi |
| `updatedDate` | Ya | datetime | Tanggal pembaruan |
| `blocks` | Ya | array | Isi artikel dalam urutan baca |

### Contoh

```yaml
---
id: 102
slug: panduan-persiapan-dokumen
title: Panduan Persiapan Dokumen
description: Hal yang perlu disiapkan sebelum memulai proses.
schema:
  type: Article
seo:
  title: Panduan Persiapan Dokumen
  description: Panduan awal persiapan dokumen.
categoryIds: [30]
relatedArticleIds: [103, 104]
relatedServiceId: 12
featuredImage:
  src: /images/persiapan-dokumen.webp
  alt: Dokumen administrasi yang disusun untuk persiapan proses layanan.
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T10:00:00+07:00
blocks:
  - id: 1
    component: rich-text
    content: Uraian pembuka artikel.
  - id: 2
    component: faq
    title: Pertanyaan umum
    schema:
      type: FAQPage
    items:
      - question: Apa yang perlu disiapkan?
        answer: Data awal sesuai kebutuhan kasus.
---
```

## 7. Kontrak Layanan

Digunakan untuk halaman layanan atau jasa yang ditawarkan oleh organisasi.

### Field

| Field | Wajib | Tipe | Keterangan |
|---|---:|---|---|
| `id` | Ya | integer | ID global |
| `slug` | Ya | string | Segmen URL |
| `title` | Ya | string | Nama layanan |
| `description` | Ya | string | Ringkasan layanan |
| `schema` | Ya | object | Umumnya `Service` |
| `seo` | Ya | object | Metadata SEO |
| `providerId` | Opsional | integer | Relasi ke satu dokumen organisasi/provider |
| `categoryIds` | Opsional | integer[] | Relasi kategori layanan |
| `relatedServiceIds` | Opsional | integer[] | Relasi ke layanan lain |
| `featuredImage` | Sesuai kebutuhan | object | Gambar layanan dan alt deskriptif |
| `blocks` | Ya | array | Penjelasan layanan |
| `updatedDate` | Ya | datetime | Waktu pembaruan |

### Contoh

```yaml
---
id: 12
slug: konsultasi-perizinan
title: Konsultasi Perizinan
description: Pendampingan untuk memahami kebutuhan dan proses perizinan.
schema:
  type: Service
seo:
  title: Konsultasi Perizinan
  description: Informasi layanan konsultasi perizinan.
categoryIds: [31]
featuredImage:
  src: /images/konsultasi-perizinan.webp
  alt: Konsultan sedang membahas dokumen perizinan bersama klien.
blocks:
  - id: 1
    component: hero
    title: Konsultasi Perizinan
    description: Pendampingan berdasarkan kebutuhan kegiatan usaha.
  - id: 2
    component: process
    title: Alur pendampingan
    steps:
      - title: Identifikasi
        description: Pemetaan kebutuhan awal.
updatedDate: 2026-11-26T10:00:00+07:00
---
```

## 8. Kontrak kategori

Kategori adalah entitas konten yang dapat memiliki halaman arsip atau digunakan sebagai klasifikasi. Jika kategori memiliki halaman URL, kategori wajib memiliki `id`, `slug`, `title`, `schema`, dan metadata yang diperlukan untuk halaman arsip. Relasi artikel/layanan ke kategori menggunakan `categoryIds` numerik.

Contoh:

```yaml
---
id: 30
slug: panduan
title: Panduan
description: Kumpulan artikel panduan.
schema:
  type: CollectionPage
seo:
  title: Panduan
  description: Kumpulan panduan dan informasi.
blocks:
  - id: 1
    component: content-list
    source: articles
    categoryId: 30
updatedDate: 2026-11-26T10:00:00+07:00
---
```

## 9. Standar block

### 9.1 Bentuk dasar

Setiap block harus memiliki:
- `id`: integer positif, unik dalam dokumen pemilik.
- `component`: nama komponen yang terdaftar.
- Field lain sesuai kontrak komponen tersebut.
- `schema`: opsional, hanya bila relevan.

Contoh bentuk umum:

```yaml
blocks:
  - id: 1
    component: hero
    title: Judul section
    description: Penjelasan section.
  - id: 2
    component: how-to
    title: Cara melakukan proses
    schema:
      type: HowTo
    steps:
      - name: Langkah pertama
        text: Penjelasan langkah.
```

### 9.2 Registry dan validasi block

Setiap proyek wajib memiliki block registry yang mendefinisikan:
- Nama `component` yang sah.
- Schema properti block (tipe data, wajib/opsional, batasan).
- Komponen Astro yang merender block.
- Apakah block mendukung Schema.org dan tipe schema yang diperbolehkan.
- Aturan aksesibilitas dan kebutuhan media bila relevan.

Block dengan component yang tidak terdaftar atau properti yang tidak sesuai harus menggagalkan validasi.

### 9.3 Aturan schema block

- Schema block bersifat opsional, bukan field wajib.
- Block dekoratif, navigasi, layout, CTA, atau block teks umum biasanya tidak perlu schema tersendiri.
- Block seperti FAQ, HowTo, ItemList, atau Review dapat memiliki schema jika konten dan konteksnya memenuhi ketentuan.
- Schema tidak boleh dipaksakan hanya untuk memenuhi kuota.
- Schema pada block harus konsisten dengan schema utama dokumen dan graph JSON-LD yang dihasilkan.

## 10. Standar relasi

Gunakan nama field yang secara eksplisit menunjukkan ID tujuan, misalnya:

- `relatedServiceId: 12`
- `relatedArticleIds: [102, 103]`
- `categoryIds: [30, 31]`
- `parentPageId: 20`

Jangan gunakan pola seperti `relatedService: konsultasi-perizinan` atau `relatedArticle: panduan-dokumen` sebagai relasi utama.

Validator harus memeriksa:
1. Nilai relasi adalah integer positif (atau array integer positif).
2. ID target ada.
3. Target berasal dari jenis konten yang diizinkan.
4. Kardinalitas sesuai definisi field.
5. Tidak ada ID target duplikat dalam relasi jamak, kecuali memang diizinkan.

## 11. Kontrak yang belum didefinisikan

Jenis konten lain—misalnya produk, lokasi cabang, anggota tim, testimoni, studi kasus, event, FAQ mandiri, atau portofolio—tidak otomatis harus mengikuti salah satu kontrak di atas. Sebelum digunakan, jenis konten baru harus memiliki definisi kontrak tersendiri yang setidaknya mencantumkan:

- Tujuan dan route (jika ada).
- Field wajib dan opsional beserta tipe datanya.
- Schema.org utama.
- Relasi yang diperbolehkan dan targetnya.
- Dukungan block (jika menggunakan block).
- Aturan validasi dan contoh frontmatter yang valid.

## 12. Catatan implementasi

Dokumen ini menetapkan kontrak konseptual. Nama collection Astro, lokasi file, nama field final, format tanggal, struktur objek SEO, strategi ID registry, serta cara menghasilkan JSON-LD harus dipastikan dalam dokumen arsitektur teknis sebelum implementasi. Perubahan nama field antarproyek tidak boleh dilakukan diam-diam; jika berbeda dari kontrak standar, tuliskan sebagai keputusan proyek dan pastikan tidak melanggar Constitution.

## 12. Kontrak objek bersama

### 12.1 Objek `seo`

Semua dokumen yang menggunakan `seo` wajib memakai object. `title` dan `description` boleh tidak diisi karena memiliki fallback ke field utama dokumen.

| Field | Wajib | Tipe | Aturan |
|---|---:|---|---|
| `title` | Tidak | string | Fallback ke `title` dokumen |
| `description` | Tidak | string | Fallback ke `description` dokumen |
| `canonical` | Tidak | URL string | URL absolut; fallback ke URL kanonis hasil routing |
| `robots` | Tidak | object | Instruksi indexing; properti final ditetapkan arsitektur |
| `openGraph` | Tidak | object | Override Open Graph; properti final ditetapkan arsitektur |
| `twitter` | Tidak | object | Override Twitter; properti final ditetapkan arsitektur |

Jika fallback juga kosong, validasi gagal. URL canonical harus absolut. Properti nested yang tidak dikenal ditolak oleh validator. Metadata SEO tidak boleh menjadi salinan kedua dari seluruh konten utama.

### 12.2 Objek `featuredImage`

| Field | Wajib | Tipe | Aturan |
|---|---:|---|---|
| `src` | Ya | string | Path aset lokal atau URL media yang diizinkan |
| `alt` | Ya | string | Deskripsi bermakna sesuai konteks gambar dan halaman |
| `width` | Tidak | integer positif | Lebar intrinsik |
| `height` | Tidak | integer positif | Tinggi intrinsik |
| `caption` | Tidak | string | Keterangan yang ditampilkan |
| `credit` | Tidak | string | Kredit sumber bila diperlukan |

`featuredImage` bukan string tunggal. Gambar dekoratif boleh memakai alt kosong hanya pada field block yang secara eksplisit mendukung dekorasi; gambar utama wajib memiliki alt deskriptif.

## 13. Matriks relasi

Setiap field relasi harus tercantum dalam matriks ini atau matriks khusus proyek yang lebih lengkap. Target yang tidak ditemukan menyebabkan validasi gagal; relasi tidak boleh diam-diam dihapus atau diselesaikan berdasarkan slug.

| Field | Sumber | Target | Kardinalitas | Status | Jika target tidak ditemukan |
|---|---|---|---|---|---|
| `pageId` | Item menu | Page/Homepage | 1:1 | Salah satu target menu wajib | Gagal validasi |
| `authorId` | Article | Author/Person | 0..1 | Opsional; kontrak target harus tersedia | Gagal validasi bila diisi |
| `categoryIds` | Article/Service | Category | 0..N | Opsional | Gagal validasi |
| `relatedArticleIds` | Article | Article | 0..N | Opsional | Gagal validasi |
| `relatedServiceId` | Article | Service | 0..1 | Opsional | Gagal validasi bila diisi |
| `providerId` | Service | Organization/Provider | 0..1 | Opsional; kontrak target harus tersedia | Gagal validasi bila diisi |
| `relatedServiceIds` | Service | Service | 0..N | Opsional | Gagal validasi |
| `serviceIds` | Homepage/block | Service | 0..N | Sesuai kontrak block | Gagal validasi |
| `parentPageId` | Page | Page | 0..1 | Opsional | Gagal validasi bila diisi |
| `categoryId` | Content-list block | Category | 1:1 | Wajib untuk block kategori | Gagal validasi |

Relasi internal menu memakai `pageId` dan menunjuk dokumen yang memiliki route. Item menu eksternal memakai `url`, bukan `pageId`. Tepat satu dari `pageId` atau `url` harus diisi. `external: true` hanya sah bersama `url`. URL eksternal harus absolut dan memakai protokol yang diizinkan.

Relasi ke Author/Person atau Organization/Provider belum boleh digunakan sebelum kontrak jenis konten target tersebut tersedia. Jika entitas tidak dimodelkan sebagai dokumen konten, gunakan struktur non-relasional yang didefinisikan secara eksplisit dalam PRD.

## 14. Aturan waktu dan Schema.org

Semua timestamp wajib memakai ISO 8601 UTC presisi detik: `YYYY-MM-DDTHH:mm:ssZ`, misalnya `2026-11-26T03:00:00Z`. Timestamp dengan offset lokal, tanpa zona waktu, atau presisi milidetik ditolak. Timestamp tidak wajib unik secara global; identitas unik ditentukan oleh ID dokumen.

Jika `publishedDate` dan `updatedDate` tersedia, `updatedDate` harus sama dengan atau lebih baru daripada `publishedDate`. `publishedDate` adalah waktu publikasi pertama dan tidak berubah pada pembaruan editorial biasa; `updatedDate` berubah ketika ada pembaruan substantif.

Contoh `FAQPage` dan `HowTo` dalam dokumen ini hanya menunjukkan pemetaan semantik Schema.org. Contoh bukan jaminan kelayakan rich result. Periksa kebijakan mesin pencari yang berlaku saat implementasi dan pastikan markup sesuai dengan konten yang terlihat serta persyaratan tipe terkait.

