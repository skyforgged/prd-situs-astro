# Frontmatter Templates — PRD Astro

> Status: Template referensi
> Versi: 1.3
> Mengikuti: Content Contract 1.4

## Cara menggunakan

File ini menyediakan kerangka field frontmatter untuk membantu AI agent dan developer mengenali seluruh struktur data yang harus dipertimbangkan saat membuat dokumen konten.

**Template di bawah sengaja tidak berisi nilai data.** Template bukan dokumen konten valid yang siap dipublikasikan. Isi nilai sesuai kebutuhan proyek sebelum digunakan.

Aturan penggunaan:
- Jangan menghapus field wajib hanya karena nilainya belum diketahui. Biarkan sebagai pekerjaan yang belum lengkap dan minta informasi yang diperlukan.
- Field opsional boleh dihilangkan jika memang tidak digunakan. Jika ditampilkan dalam template, isi hanya ketika relevan.
- Jangan mengarang `id`, relasi, URL, tanggal, Schema.org type, atau isi konten.
- `id` dokumen harus dialokasikan dari registry ID proyek dan unik global lintas collection.
- `blocks` harus mengikuti block registry proyek. Jangan mengarang nama component atau props.
- Timestamp wajib ISO 8601 UTC presisi detik (`YYYY-MM-DDTHH:mm:ssZ`).
- Field dan tipe data final tetap mengikuti Content Contract. Jika template dan kontrak berbeda, Content Contract yang berlaku.

## 1. Homepage

```yaml
---
id:
slug:
title:
description:
schema:
  type:
seo:
  title:
  description:
  canonical:
  robots:
  openGraph:
  twitter:
blocks:
  - id:
    component:
updatedDate:
---
```

Catatan: `slug` homepage merupakan identifier internal; routing tetap dipetakan ke `/`. Tambahkan props block hanya sesuai block registry.

## 2. Menu / navigasi

```yaml
---
id:
slug:
title:
schema:
  type:
location:
items:
  - label:
    pageId:
    url:
    external:
    children:
      - label:
        pageId:
        url:
        external:
updatedDate:
---
```

Catatan: setiap item harus mengisi tepat satu target (`pageId` atau `url`). Jangan mengisi keduanya. `external` hanya digunakan bersama `url`. Kedalaman maksimum tiga tingkat termasuk item akar. `location` mengikuti enum pada Content Contract.

## 3. Halaman

```yaml
---
id:
slug:
title:
description:
intro:
schema:
  type:
seo:
  title:
  description:
  canonical:
  robots:
  openGraph:
  twitter:
featuredImage:
  src:
  alt:
  width:
  height:
  caption:
  credit:
blocks:
  - id:
    component:
publishedDate:
updatedDate:
---
```

Catatan: `featuredImage` dan `publishedDate` opsional sesuai kebutuhan. Hapus seluruh objek/field opsional jika tidak digunakan; jangan membiarkan nilai null pada konten final.

## 4. Artikel

```yaml
---
id:
slug:
title:
description:
intro:
schema:
  type:
seo:
  title:
  description:
  canonical:
  robots:
  openGraph:
  twitter:
authorId:
categoryIds:
relatedArticleIds:
relatedServiceId:
featuredImage:
  src:
  alt:
  width:
  height:
  caption:
  credit:
publishedDate:
updatedDate:
blocks:
  - id:
    component:
---
```

Catatan: `authorId`, `categoryIds`, `relatedArticleIds`, dan `relatedServiceId` bersifat opsional. Semua ID relasi harus menunjuk dokumen target yang benar dan terdaftar. `featuredImage`, `publishedDate`, dan `updatedDate` mengikuti kewajiban kontrak Artikel.

## 5. Layanan

```yaml
---
id:
slug:
title:
description:
intro:
schema:
  type:
seo:
  title:
  description:
  canonical:
  robots:
  openGraph:
  twitter:
providerId:
categoryIds:
relatedServiceIds:
featuredImage:
  src:
  alt:
  width:
  height:
  caption:
  credit:
blocks:
  - id:
    component:
updatedDate:
---
```

Catatan: `providerId`, `categoryIds`, `relatedServiceIds`, dan `featuredImage` opsional. Relasi provider hanya boleh dipakai jika kontrak entitas Organization/Provider sudah tersedia.

## 6. Kategori

```yaml
---
id:
slug:
title:
description:
schema:
  type:
seo:
  title:
  description:
  canonical:
  robots:
  openGraph:
  twitter:
blocks:
  - id:
    component:
updatedDate:
---
```

Catatan: `description` dan `blocks` mengikuti definisi kategori/arsip dalam Content Contract. Jika kategori tidak memiliki halaman arsip, struktur route dan field yang dibutuhkan harus ditetapkan secara eksplisit oleh kontrak proyek.

## 7. Pola block

Kerangka berikut hanya menunjukkan bentuk minimal. Field props tambahan wajib mengikuti definisi component di block registry.

```yaml
blocks:
  - id:
    component:
```

Jika block membutuhkan schema semantik, tambahkan `schema` hanya jika didukung block registry dan sesuai konten yang terlihat:

```yaml
blocks:
  - id:
    component:
    schema:
      type:
```

## 8. Checklist sebelum frontmatter dianggap selesai

- [ ] Semua field wajib sudah memiliki nilai dengan tipe yang benar.
- [ ] ID dokumen unik global dan ID block unik di dokumen tersebut.
- [ ] Slug dan route tidak konflik.
- [ ] `schema.type` valid dan sesuai konten.
- [ ] SEO fallback tidak menghasilkan title atau description kosong.
- [ ] `intro` Page/Article/Service tersedia, berupa satu paragraf substantif, dan tampil sebagai paragraf pertama sebelum block.
- [ ] Jika `schema.type: DefinedTerm`, intro dimulai dengan pola `<title> adalah <definisi substantif>.` dan lolos validasi semantik.
- [ ] Relasi numerik menunjuk target yang tersedia.
- [ ] Block dan props terdaftar di block registry.
- [ ] Featured image memiliki `src` dan alt deskriptif.
- [ ] Timestamp sesuai ISO 8601 UTC presisi detik.
- [ ] Tidak ada field opsional kosong/null yang tidak diperlukan.
- [ ] Dokumen lolos seluruh quality gates proyek.