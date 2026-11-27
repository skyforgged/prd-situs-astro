# Content Contract — PRD Astro

> Status: Standar data konten  
> Versi: 1.3
> Format sumber: Markdown + YAML frontmatter

## 1. Tujuan

Dokumen ini mendefinisikan kontrak data untuk dokumen konten situs. Setiap jenis konten memiliki kontrak frontmatter tersendiri. Kontrak tidak disatukan menjadi satu skema universal; masing-masing dapat memiliki field wajib, opsional, dan aturan validasi sesuai fungsinya.

Aturan lintas jenis konten seperti ID global, foreign key numerik, sumber Markdown, dan Schema.org mengikuti [Website Constitution](../constitution/WEBSITE-CONSTITUTION.md). Kerangka field frontmatter kosong untuk setiap jenis konten tersedia di [Frontmatter Templates](FRONTMATTER-TEMPLATES.md). Agen AI dan developer wajib merujuk template tersebut saat membuat dokumen baru, lalu mengisi nilainya sesuai kebutuhan dan kontrak.

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

Nilai `location` dibatasi pada enum `header`, `footer`, `mobile`, atau `utility`. Setiap item wajib memiliki `label` string non-kosong dan tepat satu target: `pageId` atau `url`. `url` harus URL absolut. `external: true` hanya boleh dipakai bersama `url`; untuk target internal berbasis `pageId`, properti `external` dihilangkan atau bernilai `false`. Item boleh memiliki `children` berupa array item menu dengan aturan target yang sama. Kedalaman maksimum adalah tiga tingkat termasuk item akar; lebih dalam harus ditolak validator.

### Field

| Field | Wajib | Tipe | Keterangan |
|---|---:|---|---|
| `id` | Ya | integer | ID global |
| `slug` | Ya | string | Identifier menu, misalnya `main-navigation` |
| `title` | Ya | string | Nama internal menu |
| `schema` | Ya | object | Schema utama yang sesuai; dapat berupa `SiteNavigationElement` jika tepat |
| `location` | Ya | string/enum | Posisi menu: `header`, `footer`, `mobile`, atau `utility` |
| `items` | Ya | array | Item navigasi sesuai urutan |
| `updatedDate` | Ya | datetime | Waktu pembaruan |

Setiap item menu wajib memiliki label dan tepat satu target: `pageId` atau `url`. Target internal harus menggunakan ID numerik konten tujuan; URL eksternal harus absolut. Aturan `external`, `children`, dan batas kedalaman mengikuti ketentuan di atas bagian ini.

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
updatedDate: 2026-11-26T03:00:00Z
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
| `description` | Ya | string | Ringkasan singkat halaman untuk kebutuhan umum; bukan pengganti `intro` |
| `intro` | Ya | string | Paragraf pembuka substantif yang ditampilkan sebelum seluruh block konten |
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
intro: PT Contoh memberikan layanan profesional dengan ruang lingkup kompetensi yang dijelaskan pada halaman ini.
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
updatedDate: 2026-11-26T03:00:00Z
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
| `description` | Ya | string | Ringkasan singkat artikel untuk kebutuhan umum; bukan pengganti `intro` |
| `intro` | Ya | string | Paragraf pembuka substantif yang ditampilkan sebelum seluruh block konten |
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
intro: Panduan persiapan dokumen adalah uraian mengenai data dan dokumen yang perlu disiapkan sebelum suatu proses dimulai.
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
updatedDate: 2026-11-26T03:00:00Z
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
| `description` | Ya | string | Ringkasan singkat layanan untuk kebutuhan umum; bukan pengganti `intro` |
| `intro` | Ya | string | Paragraf pembuka substantif yang ditampilkan sebelum seluruh block konten |
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
intro: Konsultasi perizinan adalah layanan pendampingan untuk membantu memahami kebutuhan, persyaratan, dan tahapan proses perizinan sesuai kondisi pemohon.
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
updatedDate: 2026-11-26T03:00:00Z
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
updatedDate: 2026-11-26T03:00:00Z
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

Schema block bersifat opsional, bukan field wajib. Namun, ketika sebuah block merepresentasikan entitas atau struktur yang dikenali Schema.org, agen **wajib mengevaluasi** apakah schema relevan dan tidak boleh menghilangkannya tanpa alasan. Keputusan untuk tidak memakai schema harus didasarkan pada jenis konten, pedoman mesin pencari, dan konteks halaman—bukan karena contoh atau field schema tidak tersedia.

Aturan penerapan:

1. Properti `schema` diletakkan pada level block yang bersangkutan, sejajar dengan `id` dan `component`; bukan di dalam `items` atau `steps`.
2. Bentuk minimalnya adalah object dengan properti `type` berisi nama tipe Schema.org yang valid, mengikuti konvensi kontrak ini.
3. Properti data schema diambil dari field konten block yang benar-benar tersedia. Jangan mengarang jawaban, rating, penulis, tanggal, atau langkah demi melengkapi schema.
4. Schema block harus menggambarkan konten yang terlihat oleh pengguna. Jangan menambahkan schema untuk konten tersembunyi, tidak relevan, atau tidak benar-benar disajikan.
5. Schema block bukan pengganti schema utama dokumen. Keduanya harus digabungkan secara konsisten ke graph JSON-LD halaman tanpa duplikasi atau konflik entitas.
6. Jangan menambahkan schema pada block dekoratif, navigasi, layout, CTA, atau teks umum yang tidak merepresentasikan tipe Schema.org tertentu.
7. Schema tidak menjamin rich result. Agen tidak boleh menjanjikan rich result hanya karena markup ditambahkan.

#### Contoh A — FAQ block dengan FAQPage

Gunakan ketika block benar-benar menampilkan daftar pertanyaan dan jawaban. FAQPage ditempatkan pada block FAQ, bukan pada setiap item.

~~~yaml
blocks:
  - id: 4
    component: faq
    title: Pertanyaan yang sering diajukan
    schema:
      type: FAQPage
    items:
      - question: Apa fungsi dokumen ini?
        answer: Dokumen ini menjelaskan persyaratan dan proses yang perlu dipenuhi.
      - question: Kapan proses dapat dimulai?
        answer: Proses dapat dimulai setelah data awal dan dokumen pendukung tersedia.
~~~

Pemetaan: items[].question menjadi Question.name dan items[].answer menjadi acceptedAnswer.text. Jangan menambahkan FAQPage jika block hanya berisi tautan pertanyaan atau konten yang tidak tampil.

#### Contoh B — HowTo block dengan HowTo

Gunakan ketika halaman menjelaskan satu prosedur yang terdiri dari langkah-langkah berurutan. Setiap langkah harus memiliki nama dan penjelasan yang terlihat.

~~~yaml
blocks:
  - id: 5
    component: how-to
    title: Tahapan persiapan pengajuan
    description: Urutan persiapan sebelum pengajuan dilakukan.
    schema:
      type: HowTo
    steps:
      - name: Pemeriksaan data awal
        text: Periksa identitas pemilik, data bangunan, dan dokumen yang tersedia.
      - name: Pengumpulan dokumen
        text: Siapkan dokumen administrasi dan teknis sesuai kondisi bangunan.
      - name: Evaluasi kelengkapan
        text: Cocokkan dokumen dengan persyaratan proses yang berlaku.
~~~

Pemetaan: title menjadi HowTo.name; description menjadi HowTo.description; steps[].name dan steps[].text menjadi HowToStep.name dan HowToStep.text. Jangan memakai HowTo untuk daftar manfaat, daftar layanan, atau uraian yang bukan prosedur berurutan.

#### Contoh C — ItemList block dengan ItemList

Gunakan ketika block menyajikan daftar item yang bermakna sebagai satu daftar terstruktur. Item yang ditampilkan harus sama dengan item yang dimasukkan ke schema.

~~~yaml
blocks:
  - id: 6
    component: item-list
    title: Dokumen yang perlu disiapkan
    schema:
      type: ItemList
    items:
      - name: Identitas pemilik
        description: Dokumen identitas pihak pemilik bangunan.
      - name: Data bangunan
        description: Informasi fungsi, luas, dan lokasi bangunan.
      - name: Dokumen teknis
        description: Dokumen teknis yang tersedia sesuai kondisi bangunan.
~~~

Pemetaan: items menjadi ItemList.itemListElement; setiap entri direpresentasikan sebagai ListItem dengan posisi urutan yang sesuai. Jika implementasi block menggunakan field lain, registry wajib mendokumentasikan pemetaan tersebut secara eksplisit.

#### Contoh D — block tanpa schema

Tidak semua block memerlukan schema. CTA berikut cukup dirender sebagai antarmuka ajakan bertindak dan tidak diberi schema:

~~~yaml
blocks:
  - id: 7
    component: cta
    title: Konsultasikan kebutuhan Anda
    description: Sampaikan kondisi awal agar tim dapat membantu menentukan langkah berikutnya.
    label: Hubungi kami
    url: https://example.com/kontak
~~~

Tidak adanya properti schema pada contoh ini disengaja, bukan kekurangan data.

#### Kewajiban block registry

Block registry wajib mendefinisikan untuk setiap component:
- Apakah schema didukung, dilarang, atau opsional bersyarat.
- Tipe Schema.org yang diizinkan untuk component tersebut.
- Field block yang menjadi sumber data tiap properti schema.
- Bentuk dan aturan validasi field sumber, termasuk field wajib.
- Cara renderer/JSON-LD builder menggabungkan schema block ke graph halaman.
- Kondisi ketika schema harus dihilangkan.

Contoh: registry faq dapat menetapkan schema.type hanya boleh FAQPage, dengan sumber items[].question dan items[].answer. Registry how-to dapat menetapkan HowTo, dengan sumber title, description, dan steps[].name/text.

Block dengan component tidak terdaftar, tipe schema yang tidak diizinkan, atau field sumber yang tidak sesuai harus menggagalkan validasi. Jika schema bersifat opsional bersyarat dan tidak digunakan, validasi konten tetap dapat lolos selama aturan component di registry terpenuhi.

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

## 13. Kontrak objek bersama

### 13.1 Objek `seo`

Semua dokumen yang menggunakan `seo` wajib memakai object. `title` dan `description` boleh tidak diisi karena memiliki fallback ke field utama dokumen.

`description` pada level dokumen dan `seo.description` memiliki tujuan berbeda dari `intro`:

- `description` adalah ringkasan singkat dokumen untuk kebutuhan umum seperti kartu konten, daftar, arsip, dan fallback metadata.
- `seo.description` adalah teks metadata deskripsi untuk mesin pencari dan platform yang membaca metadata. Nilainya boleh lebih ringkas atau memiliki sudut penyajian berbeda dari `description`. Tidak ada batas karakter universal yang dijadikan syarat validitas kontrak; panjang editorial dapat ditetapkan dalam pedoman proyek. Mesin pencari dapat memotong atau memilih cuplikan lain dari halaman.
- `intro` adalah paragraf pembuka substantif yang benar-benar ditampilkan pada halaman. `intro` bukan meta description dan tidak boleh dipendekkan hanya untuk mengikuti perkiraan batas karakter metadata.

Fallback `seo.description` tetap menggunakan `description` dokumen, bukan `intro`. Jangan otomatis menyalin `intro` ke metadata. Sistem pencarian dan AI dapat menggunakan berbagai bagian halaman; keberadaan `intro` yang informatif membantu menyediakan konteks yang jelas, tetapi tidak menjamin halaman dikutip atau ditampilkan dalam AI Mode maupun fitur pencarian tertentu.

| Field | Wajib | Tipe | Aturan |
|---|---:|---|---|
| `title` | Tidak | string | Fallback ke `title` dokumen |
| `description` | Tidak | string | Fallback ke `description` dokumen |
| `canonical` | Tidak | URL string | URL absolut; fallback ke URL kanonis hasil routing |
| `robots` | Tidak | object | Instruksi indexing; properti final ditetapkan arsitektur |
| `openGraph` | Tidak | object | Override Open Graph; properti final ditetapkan arsitektur |
| `twitter` | Tidak | object | Override Twitter; properti final ditetapkan arsitektur |

Jika fallback juga kosong, validasi gagal. URL canonical harus absolut. Properti nested yang tidak dikenal ditolak oleh validator. Metadata SEO tidak boleh menjadi salinan kedua dari seluruh konten utama.

### 13.2 Field `intro`

`intro` adalah paragraf pertama dari konten utama halaman dan dirender langsung setelah judul utama (serta metadata visual yang ditetapkan layout) dan sebelum block pertama. Intro disimpan sebagai teks biasa, bukan HTML, Markdown, atau block terpisah.

| Field | Wajib | Tipe | Aturan |
|---|---:|---|---|
| `intro` | Ya pada Page, Article, dan Service | string | Satu paragraf substantif, tidak kosong, dan ditampilkan sebagai paragraf pembuka |

Aturan editorial dan validasi:

1. Intro harus menjelaskan topik utama secara langsung, spesifik, faktual, dan dapat dipahami tanpa harus membaca paragraf sebelumnya.
2. Intro tidak boleh hanya berupa slogan, ajakan bertindak, daftar keyword, kalimat pengantar generik, atau pengulangan judul tanpa penjelasan.
3. Untuk dokumen yang secara eksplisit mendefinisikan istilah/konsep dan memakai `schema.type: DefinedTerm`, kalimat pertama wajib mengikuti pola `<judul halaman> adalah <definisi substantif>.` Judul pada awal kalimat harus sama dengan nilai `title` setelah normalisasi spasi dan perbandingan tanpa membedakan huruf besar-kecil. Setelah frasa `adalah`, harus ada definisi yang bermakna, bukan sekadar sinonim atau pengulangan judul.
4. Pola definisi tersebut tidak diwajibkan untuk halaman yang bukan halaman definisi. Untuk halaman non-definisi, intro harus mengikuti tujuan dan bentuk kontennya.
5. Intro tidak boleh memuat klaim yang tidak didukung, data yang dikarang, atau janji hasil.
6. Intro menjadi sumber utama properti `description` pada node `DefinedTerm` jika tipe tersebut digunakan. `title` dipetakan ke `DefinedTerm.name`. Node DefinedTerm harus dihubungkan sebagai `mainEntity` halaman dan memiliki `@id` stabil. Jangan membuat DefinedTerm hanya karena intro diawali definisi; tipe tersebut hanya digunakan bila halaman memang berfokus pada satu istilah yang didefinisikan.
7. Intro harus terlihat oleh pengguna. Jangan hanya memasukkannya ke JSON-LD atau menyembunyikannya dari tampilan halaman.

Validator wajib menggagalkan dokumen Page, Article, atau Service jika `intro` tidak ada, bukan string, kosong setelah trim, berisi lebih dari satu paragraf, atau memuat markup HTML/Markdown. Untuk `schema.type: DefinedTerm`, validator juga wajib memeriksa pola awal `<title> adalah ` secara case-insensitive setelah normalisasi spasi, serta memastikan bagian definisi setelahnya tidak kosong. Validator tidak boleh menganggap keberadaan `intro` saja cukup untuk meloloskan kelayakan semantik DefinedTerm; kesesuaian tipe tetap harus diperiksa.

### 13.3 Objek `featuredImage`

| Field | Wajib | Tipe | Aturan |
|---|---:|---|---|
| `src` | Ya | string | Path aset lokal atau URL media yang diizinkan |
| `alt` | Ya | string | Deskripsi bermakna sesuai konteks gambar dan halaman |
| `width` | Tidak | integer positif | Lebar intrinsik |
| `height` | Tidak | integer positif | Tinggi intrinsik |
| `caption` | Tidak | string | Keterangan yang ditampilkan |
| `credit` | Tidak | string | Kredit sumber bila diperlukan |

`featuredImage` bukan string tunggal. Gambar dekoratif boleh memakai alt kosong hanya pada field block yang secara eksplisit mendukung dekorasi; gambar utama wajib memiliki alt deskriptif.

## 14. Matriks relasi

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

## 15. Aturan waktu dan Schema.org

Semua timestamp wajib memakai ISO 8601 UTC presisi detik: `YYYY-MM-DDTHH:mm:ssZ`, misalnya `2026-11-26T03:00:00Z`. Timestamp dengan offset lokal, tanpa zona waktu, atau presisi milidetik ditolak. Timestamp tidak wajib unik secara global; identitas unik ditentukan oleh ID dokumen.

Jika `publishedDate` dan `updatedDate` tersedia, `updatedDate` harus sama dengan atau lebih baru daripada `publishedDate`. `publishedDate` adalah waktu publikasi pertama dan tidak berubah pada pembaruan editorial biasa; `updatedDate` berubah ketika ada pembaruan substantif.

Contoh `FAQPage` dan `HowTo` dalam dokumen ini hanya menunjukkan pemetaan semantik Schema.org. Contoh bukan jaminan kelayakan rich result. Periksa kebijakan mesin pencari yang berlaku saat implementasi dan pastikan markup sesuai dengan konten yang terlihat serta persyaratan tipe terkait.



## 16. Katalog tipe Schema.org dan ruang lingkup penggunaannya

Bagian ini merupakan inventaris tipe Schema.org yang dapat dipertimbangkan oleh proyek. Daftar ini bukan izin untuk menggunakan semua tipe secara bebas. Setiap penggunaan tetap harus disetujui dalam Schema Registry, sesuai struktur konten, konteks halaman, dan implementasi JSON-LD proyek.

Penting untuk membedakan:
- **Validitas Schema.org:** apakah tipe dan properti merupakan bagian dari kosakata Schema.org.
- **Kesesuaian semantik:** apakah tipe tersebut benar-benar menggambarkan konten atau entitas yang disajikan.
- **Dukungan rich result Google:** apakah Google saat implementasi mendukung tipe tersebut untuk tampilan hasil kaya tertentu dan apakah halaman memenuhi persyaratannya.

Ketiganya tidak sama. Tipe Schema.org yang valid tidak otomatis memenuhi syarat rich result Google.

### 16.1 Tipe yang dapat dipertimbangkan untuk struktur block

Tipe berikut dapat relevan untuk block tertentu apabila data yang diperlukan benar-benar tersedia dan terlihat oleh pengguna.

| Schema.org type | Kegunaan | Contoh block/konten | Catatan penerapan |
|---|---|---|---|
| `FAQPage` | Halaman yang berisi kumpulan pertanyaan dan jawaban | FAQ | Pertimbangkan sebagai entitas halaman; jangan menghasilkan banyak FAQPage yang saling menduplikasi dari beberapa block. |
| `HowTo` | Prosedur yang terdiri dari langkah-langkah | Panduan langkah demi langkah | Gunakan hanya untuk instruksi/prosedur nyata, bukan daftar manfaat atau daftar layanan. |
| `ItemList` | Sekumpulan item yang memiliki makna sebagai satu daftar | Daftar persyaratan, tahapan, atau pilihan | Urutan dan item schema harus sesuai dengan yang ditampilkan. |
| `VideoObject` | Informasi tentang video | Video tutorial, video penjelasan | Harus mengacu pada video yang benar-benar tersedia; properti media dan thumbnail mengikuti kontrak media. |
| `ImageObject` | Informasi tentang gambar | Foto proyek, diagram, ilustrasi teknis | Jangan membuat ImageObject untuk setiap gambar secara otomatis; gunakan jika metadata objek gambar memang diperlukan. |
| `Table` | Tabel sebagai karya/konten terstruktur | Tabel perbandingan atau data | Pastikan pemetaan tabel sesuai kosakata Schema.org dan bukan sekadar menandai semua elemen HTML table. |
| `Course` | Kursus atau program pembelajaran | Katalog kursus/pelatihan | Harus benar-benar merupakan kursus dengan informasi yang relevan, bukan artikel biasa. |
| `Quiz` | Kuis/evaluasi pembelajaran | Kuis dengan pertanyaan dan evaluasi | Gunakan hanya jika ada kuis nyata; jangan menyamakan FAQ dengan Quiz. |
| `Question` | Satu pertanyaan dalam struktur yang sesuai | Item pertanyaan dalam Q&A/FAQ | Umumnya menjadi bagian dari struktur induk yang tepat, bukan schema mandiri untuk setiap teks tanya. |
| `DefinedTerm` | Istilah yang didefinisikan | Glosarium istilah teknis | Definisi harus benar-benar disajikan dan konsisten. |
| `Claim` | Pernyataan/klaim yang dapat diidentifikasi | Klaim yang disertai sumber atau konteks | Jangan menggunakannya untuk klaim pemasaran tanpa dasar. |
| `Quotation` | Kutipan yang diidentifikasi sebagai kutipan | Kutipan regulasi atau pendapat ahli | Kutipan harus akurat, memiliki atribusi/sumber bila diperlukan, dan tampil pada halaman. |
| `SpeakableSpecification` | Penanda bagian konten yang cocok dibacakan | Ringkasan atau bagian artikel tertentu | Ini bukan pengganti schema Article/WebPage dan dukungannya harus diperiksa pada target mesin pencari. |

Katalog di atas merupakan kandidat, bukan kewajiban. Block dekoratif, navigasi, layout, CTA, dan teks umum tidak perlu diberi schema hanya agar setiap block memiliki markup.

### 16.2 Tipe tingkat halaman/dokumen

Tipe berikut menggambarkan halaman atau dokumen secara keseluruhan. Tipe ini umumnya ditetapkan pada frontmatter dokumen, bukan diulang pada setiap block.

| Schema.org type | Kegunaan | Contoh halaman |
|---|---|---|
| `WebPage` | Halaman web umum | Halaman informasional |
| `Article` | Artikel umum | Artikel editorial |
| `BlogPosting` | Artikel blog | Postingan blog |
| `TechArticle` | Artikel teknis | Panduan atau penjelasan teknis |
| `NewsArticle` | Artikel berita | Berita perusahaan/industri |
| `CollectionPage` | Halaman koleksi/kumpulan | Arsip artikel atau kategori |
| `AboutPage` | Halaman tentang entitas | Tentang perusahaan |
| `ContactPage` | Halaman kontak | Kontak perusahaan |
| `ProfilePage` | Halaman profil | Profil orang atau organisasi |
| `SearchResultsPage` | Halaman hasil pencarian | Hasil pencarian internal |
| `QAPage` | Halaman yang berfokus pada satu pertanyaan dan jawaban dari pengguna/komunitas | Forum atau halaman tanya-jawab yang memenuhi karakteristik Q&A |
| `ItemPage` | Halaman yang membahas satu item tertentu | Detail satu item/entitas |

Pemilihan tipe harus mengikuti tujuan utama halaman. Sebagai contoh, halaman artikel teknis dapat memakai `TechArticle` jika memang sesuai, sedangkan halaman arsip artikel lebih tepat dipertimbangkan sebagai `CollectionPage`. `QAPage` tidak boleh dipakai hanya karena halaman memiliki FAQ; karakteristik Q&A-nya harus benar-benar terpenuhi.

### 16.3 Tipe tingkat entitas bisnis, layanan, dan orang

Tipe berikut menggambarkan entitas yang ditawarkan, dimiliki, atau direpresentasikan oleh situs. Tipe-tipe ini umumnya dikelola sebagai node entitas pada graph JSON-LD dan direlasikan dengan halaman yang relevan.

| Schema.org type | Kegunaan | Catatan penerapan |
|---|---|---|
| `Service` | Layanan/jasa | Cocok untuk entitas layanan; hubungkan dengan provider yang benar. |
| `ProfessionalService` | Bisnis jasa profesional | Gunakan jika jenis bisnis dan hierarki tipe memang sesuai; jangan otomatis mengganti semua Organization dengannya. |
| `LocalBusiness` | Bisnis dengan lokasi fisik/lokal | Data lokasi, nama, alamat, dan informasi bisnis harus faktual. |
| `Organization` | Identitas organisasi/badan usaha | Cocok sebagai entitas organisasi utama. |
| `Person` | Individu | Gunakan untuk orang/tenaga ahli yang nyata dan dapat diidentifikasi. |
| `Offer` | Penawaran | Harus merepresentasikan penawaran nyata dengan informasi yang tersedia. |
| `AggregateOffer` | Kumpulan penawaran | Gunakan hanya jika benar-benar ada kumpulan penawaran yang dapat dirangkum. |
| `Review` | Ulasan | Harus berasal dari ulasan yang benar-benar tersedia dan ditampilkan sesuai kebijakan terkait. |
| `AggregateRating` | Ringkasan rating dari sejumlah penilaian | Nilai, jumlah, dan sumber rating harus nyata; dilarang mengarang atau memanipulasi. |
| `ContactPoint` | Titik/kategori kontak organisasi | Hubungkan dengan organisasi yang benar. |
| `PostalAddress` | Alamat pos | Data alamat harus sesuai alamat sebenarnya. |
| `GeoCoordinates` | Koordinat geografis | Koordinat harus akurat dan merujuk pada lokasi entitas yang benar. |

Contoh hubungan semantik yang dapat dibentuk dalam graph:
- `Organization` menggambarkan perusahaan.
- `LocalBusiness` menggambarkan entitas/lokasi bisnis lokal jika sesuai.
- `Service` menggambarkan layanan yang ditawarkan.
- `Offer` menggambarkan penawaran tertentu.
- `Person` menggambarkan tenaga ahli atau individu yang benar-benar ada.
- `ContactPoint`, `PostalAddress`, dan `GeoCoordinates` memberikan informasi pendukung pada entitas yang tepat.

Jangan membuat node Organization, LocalBusiness, Person, atau Service baru pada setiap block. Identitas entitas harus konsisten dan dapat dirujuk kembali melalui `@id` yang stabil.

### 16.4 Tipe untuk kebutuhan situs khusus

Tipe berikut dapat dipakai jika situs memang memiliki jenis konten atau entitas yang sesuai.

| Schema.org type | Kegunaan | Contoh penggunaan |
|---|---|---|
| `Event` | Acara dengan waktu/lokasi atau informasi acara yang relevan | Seminar, webinar, pelatihan |
| `JobPosting` | Lowongan pekerjaan | Halaman karier/lowongan |
| `Dataset` | Kumpulan data yang diterbitkan | Dataset penelitian atau data publik |
| `SoftwareApplication` | Aplikasi perangkat lunak | Halaman produk perangkat lunak |
| `Product` | Produk | Halaman produk yang benar-benar ditawarkan |
| `RealEstateListing` | Listing properti | Situs listing properti |
| `Place` | Tempat/lokasi | Halaman lokasi |
| `GovernmentService` | Layanan pemerintah | Informasi layanan pemerintah yang benar-benar diselenggarakan instansi pemerintah |
| `Permit` | Izin atau dokumen perizinan sebagai entitas | Halaman yang membahas suatu izin secara spesifik dan memenuhi definisi tipe |
| `Legislation` | Peraturan/perundang-undangan | Halaman yang membahas atau merepresentasikan regulasi |
| `DigitalDocument` | Dokumen digital | Dokumen digital yang diterbitkan atau dideskripsikan |
| `Report` | Laporan | Laporan teknis atau laporan resmi |
| `AnalysisNewsArticle` | Artikel berita analisis | Analisis berita yang sesuai definisi tipe |

Konteks konsultan dan perizinan dapat membuat `Service`, `Organization`, `LocalBusiness`, `Legislation`, atau `Permit` relevan. Akan tetapi, artikel yang sekadar menyebut izin atau peraturan tidak otomatis harus menggunakan `Permit` atau `Legislation`. Tipe `GovernmentService` hanya boleh digunakan untuk layanan pemerintah yang sesuai, bukan untuk jasa konsultan swasta yang membantu mengurus layanan tersebut.

### 16.5 Tipe yang tidak boleh dipaksakan

Schema tidak ditambahkan hanya karena:
- nama tipe tersedia di Schema.org;
- sebuah block memiliki judul atau daftar;
- AGENT AI ingin melengkapi jumlah schema;
- schema dianggap sebagai cara otomatis untuk menaikkan ranking;
- contoh implementasi ditemukan pada situs lain tanpa memeriksa kesesuaian konten;
- properti yang diperlukan tidak tersedia dan harus dikarang.

Jika tidak ada tipe yang benar-benar cocok, jangan menambahkan schema. Konten tetap dapat valid tanpa schema block.

## 17. Arsitektur tiga lapisan Schema.org

Implementasi schema proyek harus memisahkan tiga lapisan berikut. Pemisahan ini merupakan pemisahan tanggung jawab data, bukan kewajiban untuk menghasilkan tiga script JSON-LD yang berbeda.

### 17.1 Layer 1 — Block-level schema

Schema yang merepresentasikan struktur atau objek yang disajikan oleh satu bagian konten. Contoh kandidat: `HowTo`, `ItemList`, `VideoObject`, `ImageObject`, `Question`, atau tipe lain yang disetujui registry. `DefinedTerm` yang bersumber dari field dokumen `title` dan `intro` diperlakukan sebagai entity-level node, bukan schema block.

Aturan:
- Schema hanya dibuat jika block dan data sumbernya memenuhi definisi tipe.
- Pemetaan field harus dinyatakan dalam Block Registry.
- Block tidak boleh membuat node entitas global baru yang menduplikasi organisasi, penulis, atau layanan.
- Schema block dapat digabungkan ke graph halaman oleh JSON-LD builder.
- Scope sumber block tidak selalu sama dengan scope entitas Schema.org. Contohnya, beberapa block FAQ pada satu halaman dapat digabungkan ke satu representasi halaman yang sesuai, bukan otomatis menghasilkan beberapa node FAQPage.

### 17.2 Layer 2 — Page-level schema

Schema yang menggambarkan dokumen/halaman secara keseluruhan, misalnya `WebPage`, `Article`, `BlogPosting`, `TechArticle`, `CollectionPage`, `AboutPage`, atau `ContactPage`.

Aturan:
- Ditetapkan melalui kontrak frontmatter dokumen.
- Satu halaman harus memiliki identitas halaman yang konsisten.
- Page-level schema menjadi konteks untuk block dan entitas lain.
- Jangan menghasilkan beberapa node yang menggambarkan halaman yang sama dengan identitas berbeda.
- Gunakan `mainEntity`, `mainEntityOfPage`, `about`, `publisher`, atau properti relasi lain hanya jika maknanya benar dan targetnya tersedia.

### 17.3 Layer 3 — Entity-level schema

Schema yang menggambarkan entitas di luar isi satu block, misalnya `Organization`, `LocalBusiness`, `Service`, `Person`, `DefinedTerm`, `Offer`, dan informasi kontak/lokasi.

Aturan:
- Dikelola dari sumber data entitas yang konsisten, bukan disalin manual ke banyak halaman.
- Setiap entitas harus mempunyai `@id` stabil dan dapat dirujuk dari halaman lain.
- Relasi harus menunjuk entitas yang benar, misalnya provider suatu Service.
- Informasi yang berubah harus memiliki satu sumber kebenaran.
- Jangan membuat rating, review, alamat, koordinat, identitas orang, atau penawaran yang tidak dapat diverifikasi.

Ketiga layer dapat disatukan dalam satu JSON-LD `@graph` pada halaman, sepanjang setiap node memiliki identitas dan relasi yang konsisten. Jumlah script JSON-LD bukan ukuran kualitas; konsistensi graph dan ketepatan semantik lebih penting.

## 18. Schema Registry

Proyek wajib memiliki Schema Registry terkontrol sebagai daftar resmi tipe Schema.org yang boleh digunakan, batas pemakaiannya, serta cara validasinya. Registry ini melengkapi Block Registry; keduanya tidak saling menggantikan.

Setiap entri Schema Registry sekurang-kurangnya mendefinisikan:

| Properti registry | Wajib | Fungsi |
|---|---:|---|
| `schemaType` | Ya | Nama tipe Schema.org yang diizinkan |
| `scope` | Ya | Lapisan penggunaan: `block`, `page`, atau `entity` |
| `supportedComponents` | Untuk scope block | Daftar component yang boleh menggunakan tipe tersebut |
| `supportedDocumentTypes` | Untuk scope page | Jenis dokumen yang boleh menggunakan tipe tersebut |
| `entitySource` | Untuk scope entity | Sumber data resmi entitas |
| `fieldMapping` | Ya | Pemetaan field sumber ke properti Schema.org |
| `requiredFields` | Ya | Field sumber/properti yang wajib tersedia |
| `optionalFields` | Ya | Field tambahan yang boleh digunakan |
| `validationRules` | Ya | Validasi tipe, format, kardinalitas, dan nilai |
| `googleRichResultSupport` | Ya | Status dukungan Google yang diverifikasi, atau `not-applicable/unknown` |
| `mergeStrategy` | Ya | Cara node digabung ke JSON-LD graph |
| `prohibitedUsage` | Ya | Kondisi penggunaan yang dilarang |
| `documentationUrl` | Ya | Referensi dokumentasi Schema.org dan/atau Google yang relevan |
| `verifiedAt` | Ya untuk status Google | Tanggal pemeriksaan status dukungan Google |

Nilai `scope` dibatasi pada `block`, `page`, dan `entity`. Satu tipe dapat memiliki kebijakan berbeda pada implementasi berbeda, tetapi setiap entri registry harus menyatakan scope dan pemilik sumber datanya secara eksplisit.

Status `googleRichResultSupport` harus memakai status terkontrol, sekurang-kurangnya:
- `supported`: tipe/fitur didukung Google untuk rich result tertentu pada saat diverifikasi; persyaratan spesifik tetap harus dipenuhi.
- `not-supported`: tidak ada dukungan rich result Google yang dinyatakan untuk tipe/fitur tersebut pada saat diverifikasi.
- `deprecated`: dukungan yang pernah ada telah dihentikan menurut dokumentasi Google yang diperiksa.
- `unknown`: belum diverifikasi atau dokumentasi tidak cukup.
- `not-applicable`: tipe digunakan untuk semantik Schema.org, bukan dengan tujuan rich result Google.

Status tersebut bukan sifat permanen Schema.org. Periksa kembali dokumentasi Google saat implementasi atau pemeliharaan; catat tanggal verifikasinya. Jangan mengubah status menjadi `supported` hanya karena validator Schema.org menerima markup.

### 18.1 Contoh bentuk entri Schema Registry

Contoh konseptual berikut menunjukkan struktur registry, bukan daftar final semua tipe yang harus diimplementasikan:

~~~yaml
schemaRegistry:
  - schemaType: HowTo
    scope: block
    supportedComponents:
      - how-to
    supportedDocumentTypes:
      - page
      - article
      - service
    fieldMapping:
      name: title
      description: description
      step:
        source: steps
        itemType: HowToStep
        fields:
          name: name
          text: text
    requiredFields:
      - title
      - steps
      - steps[].name
      - steps[].text
    optionalFields:
      - description
    validationRules:
      - steps must contain at least one item
      - every step must have a non-empty name and text
    googleRichResultSupport: not-supported
    mergeStrategy: merge-by-stable-node-id
    prohibitedUsage:
      - benefit lists
      - unordered service lists
      - content that is not a procedure
    documentationUrl:
      - https://schema.org/HowTo
    verifiedAt: 2026-11-27

  - schemaType: DefinedTerm
    scope: entity
    entitySource: document.title+document.intro
    fieldMapping:
      name: title
      description: intro
    requiredFields:
      - title
      - intro
    optionalFields: []
    validationRules:
      - document schema type must explicitly be DefinedTerm
      - intro first sentence must begin with the normalized document title followed by 'adalah'
      - definition must be visible on the page
      - stable entity id must be used and linked as WebPage.mainEntity
    googleRichResultSupport: not-applicable
    mergeStrategy: reuse-entity-node
    prohibitedUsage:
      - ordinary articles that do not define a single term
      - generating a term node from a title without a substantive definition
    documentationUrl:
      - https://schema.org/DefinedTerm
    verifiedAt: 2026-11-27

  - schemaType: Organization
    scope: entity
    entitySource: site.business
    fieldMapping:
      name: business.name
      url: site.url
      address: business.address
    requiredFields:
      - business.name
      - site.url
    optionalFields:
      - business.address
    validationRules:
      - entity id must be stable across pages
      - values must come from the configured business profile
    googleRichResultSupport: unknown
    mergeStrategy: reuse-entity-node
    prohibitedUsage:
      - creating a new organization node per block
      - inventing company details
    documentationUrl:
      - https://schema.org/Organization
    verifiedAt: 2026-11-27
~~~

Contoh di atas harus disesuaikan dengan struktur konfigurasi dan validator proyek. Nilai status Google pada contoh bersifat ilustrasi dan harus diverifikasi terhadap dokumentasi Google ketika registry benar-benar diimplementasikan.

### 18.2 Hubungan Schema Registry dan Block Registry

Block Registry menjawab:
- Component apa yang tersedia?
- Field apa yang wajib dan opsional pada component?
- Bagaimana Astro merender component?
- Schema apa yang boleh dipakai component?
- Bagaimana data block dipetakan ke schema?

Schema Registry menjawab:
- Tipe Schema.org apa yang diakui proyek?
- Scope mana yang diperbolehkan?
- Properti dan field apa yang dibutuhkan?
- Bagaimana tipe tersebut divalidasi?
- Bagaimana node masuk ke graph?
- Bagaimana status dukungan Google diverifikasi?

Jika Block Registry mengizinkan `faq` memakai `FAQPage`, Schema Registry tetap harus mendefinisikan pemetaan dan aturan FAQPage. Keduanya harus konsisten; konflik harus menggagalkan validasi.

## 19. Aturan JSON-LD graph, identitas, dan penggabungan

Semua schema dari tiga layer harus diproses secara konsisten menjadi graph JSON-LD halaman.

Ketentuan:
1. Gunakan `@context` Schema.org yang benar.
2. Gunakan `@graph` untuk menggabungkan beberapa node yang saling berhubungan bila diperlukan.
3. Gunakan `@id` stabil untuk halaman dan entitas yang perlu dirujuk lintas node/halaman.
4. Node yang merepresentasikan entitas sama harus menggunakan identitas yang sama, bukan dibuat ulang dengan ID berbeda.
5. Relasi seperti `publisher`, `provider`, `author`, `mainEntity`, `mainEntityOfPage`, dan `about` hanya dibuat jika hubungan dan targetnya benar.
6. Jangan mengeluarkan properti bernilai kosong, placeholder, atau data yang tidak tersedia.
7. Jangan menggandakan node yang sama dari frontmatter, block, layout, dan konfigurasi situs.
8. Jika dua sumber memberikan nilai yang bertentangan untuk entitas yang sama, tentukan sumber kebenaran melalui arsitektur; jangan memilih secara acak.
9. Schema yang dihasilkan harus sesuai dengan konten yang benar-benar terlihat dan dapat diakses pengguna.
10. JSON-LD harus lolos validasi sintaks dan pemeriksaan semantik yang sesuai.

Strategi merge harus ditentukan oleh arsitektur. Penggabungan tidak boleh sekadar menggabungkan object secara dangkal karena dapat menggandakan array, menimpa properti penting, atau membuat node dengan identitas berbeda. Gunakan identitas node dan aturan properti yang eksplisit.

## 20. Kebijakan Google Rich Results dan pemeliharaan

Schema.org merupakan kosakata semantik yang lebih luas daripada fitur rich result Google. Karena itu:

- Validitas Schema.org tidak menjamin rich result.
- Lolos Schema Markup Validator tidak otomatis berarti lolos Google Rich Results Test.
- Lolos Google Rich Results Test tidak menjamin rich result akan ditampilkan.
- Google dapat membatasi, mengubah, atau menghentikan dukungan rich result tanpa mengubah validitas tipe Schema.org.
- Konten harus memenuhi kebijakan dan persyaratan khusus tipe rich result yang dituju.
- Markup harus mencerminkan konten utama yang terlihat; jangan menyembunyikan atau merekayasa konten untuk memperoleh rich result.
- Review dan rating tidak boleh direkayasa. Perhatikan aturan Google mengenai review pihak pertama/self-serving review dan jenis entitas yang memenuhi syarat.
- FAQPage dan HowTo tetap dapat menjadi tipe Schema.org yang valid meskipun dukungan tampilan rich result Google dapat berbeda atau berubah.
- Jangan menulis klaim pemasaran atau dokumentasi proyek yang menjanjikan posisi ranking atau rich result hanya karena schema diterapkan.

Dokumentasi Google harus diperiksa saat implementasi dan pemeliharaan. Registry harus menyimpan URL referensi serta tanggal verifikasi agar status tidak dianggap permanen.

## 21. Rekomendasi penerapan bertahap

Untuk menghindari registry yang terlalu luas dan sulit divalidasi, penerapan disarankan bertahap:

**Tahap 1 — Tipe inti**
- Page-level: `WebPage`, `Article`/subtype yang relevan, `CollectionPage`, `AboutPage`, dan `ContactPage`.
- Entity-level: `Organization`, `LocalBusiness` jika relevan, `Service`, dan `Person` jika kontrak Person tersedia.
- Block-level: `FAQPage`, `HowTo`, dan `ItemList` sesuai kebijakan scope dan pemetaan.

**Tahap 2 — Media dan konten terstruktur**
- `VideoObject`, `ImageObject`, `DefinedTerm`, `Table`, `Question`, dan `Quotation` jika ada kebutuhan nyata dan field mapping telah ditetapkan.

**Tahap 3 — Tipe khusus**
- `Course`, `Quiz`, `Event`, `JobPosting`, `Dataset`, `Product`, `Permit`, `Legislation`, dan tipe khusus lain hanya ketika jenis konten terkait benar-benar menjadi bagian dari situs.

Urutan tersebut adalah rekomendasi prioritas, bukan kewajiban untuk mengimplementasikan semua tipe. Tipe baru harus melalui proses penambahan registry dan validasi sebelum dapat dipakai oleh konten.

**Keputusan desain:** proyek menggunakan Schema Registry yang terkontrol dan bertahap. Tidak semua block wajib memiliki schema. Schema dipilih berdasarkan makna konten, scope, field yang tersedia, dan kebijakan registry. Lebih baik menggunakan sedikit schema yang tepat, valid, dan konsisten daripada banyak markup yang tidak menggambarkan isi halaman.
