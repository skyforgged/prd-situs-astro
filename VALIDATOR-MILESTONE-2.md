# Validator Otomatis — Milestone 2 dari 5

> Status: Implementasi kontrak per jenis dokumen dan pengujian otomatis
> Cakupan: Homepage, Menu, Page, Article, Service, Category

## Tujuan

Melanjutkan invariant global Milestone 1 dengan validasi field wajib, tipe data, dan aturan struktur yang didefinisikan dalam Content Contract 1.5. Validator tidak menyatukan enam jenis dokumen menjadi satu schema universal; setiap jenis memiliki daftar kewajiban tersendiri.

## Kontrak yang diperiksa

| Jenis | Pemeriksaan utama |
|---|---|
| Homepage | slug, title, description, schema, SEO, blocks, updatedDate |
| Menu | slug, title, schema, location enum, items, updatedDate; target item tepat satu dari pageId/url; label; URL absolut HTTP(S); external; kedalaman children maksimum tiga |
| Page | slug, title, description, intro satu paragraf teks biasa, schema, SEO, blocks, updatedDate; aturan DefinedTerm bila dideklarasikan |
| Article | field Page yang relevan, featuredImage wajib, publishedDate dan updatedDate wajib, authorId/relatedServiceId numerik, categoryIds/relatedArticleIds array ID positif unik |
| Service | field Page yang relevan, providerId numerik bila digunakan, categoryIds/relatedServiceIds array ID positif unik; featuredImage opsional |
| Category | slug, title, description, schema, SEO, blocks, updatedDate sesuai pola kategori arsip pada template |

## Aturan objek bersama

- `seo` harus berupa object. `seo.title` dan `seo.description` opsional karena fallback ke `title` dan `description` dokumen; jika keduanya kosong, validasi gagal.
- `seo.canonical`, bila diisi, harus URL absolut HTTP(S).
- `seo.robots`, `seo.openGraph`, dan `seo.twitter`, bila diisi, harus object.
- `featuredImage` harus object; `src` dan `alt` wajib berupa string non-kosong; width/height, bila ada, integer positif.
- `intro` wajib untuk Page, Article, Service; harus satu paragraf, teks biasa, tidak kosong, tanpa HTML/Markdown.
- `schema.type` wajib string non-kosong. `schema.mainEntity`, bila ada, harus object dengan type non-kosong.
- DefinedTerm hanya sah pada Page, tidak boleh menggantikan page-level `schema.type`, dan intro harus dimulai dengan pola `<title> adalah <definisi substantif>`.

## Identifikasi jenis dokumen

Secara default, validator mengenali nama direktori collection berikut (termasuk bentuk tunggal/jamak dan alias umum): homepage/home, menu/navigation, page, article/post, service, category.

Jika proyek menggunakan nama collection atau struktur direktori lain, petakan secara eksplisit:

```bash
python scripts/validate_content.py src/content \
  --collection homepage=src/content/home \
  --collection menu=src/content/navigation \
  --collection page=src/content/pages \
  --collection article=src/content/articles \
  --collection service=src/content/services \
  --collection category=src/content/categories
```

Pemetaan eksplisit mengalahkan inferensi nama direktori. Path yang tidak dapat dikenali akan menghasilkan error, bukan dilewati diam-diam. Pastikan root yang dipindai mencakup seluruh collection agar pemeriksaan ID global tetap benar.

## Menjalankan

```bash
python -m pip install -r requirements-dev.txt
pytest -q
python scripts/validate_content.py src/content
```

## Batas yang belum diklaim selesai

Milestone ini belum memeriksa keberadaan target relasi di seluruh dokumen, jenis target dan kardinalitas lintas dokumen, block registry dan props per component, seluruh Schema.org registry, konflik route/slug, file aset, internal links, sitemap, breadcrumb, maupun aturan editorial semantik di luar pola DefinedTerm. Pemeriksaan tersebut harus ditambahkan pada milestone berikutnya dan tidak boleh dianggap lulus berdasarkan hasil milestone ini.

## Bukti pengujian

Suite unit menguji enam kontrak, fallback SEO, intro/DefinedTerm, featured image, target dan kedalaman menu, relasi bertipe, pemetaan collection khusus, serta invariant Milestone 1. Hasil CI dicatat setelah workflow pada commit akhir milestone selesai.
