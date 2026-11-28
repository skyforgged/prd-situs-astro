# Validator Otomatis — Milestone 1 dari 5

> Status: Implementasi fondasi dan uji unit awal
> Sasaran: kontribusi tahap pertama menuju kesiapan standar 95%

## Tujuan milestone

Membangun executable baseline yang dapat dipakai lintas proyek Astro tanpa mengasumsikan collection atau block registry tertentu. Tahap ini mengunci invariant global yang sudah ditetapkan Constitution dan Content Contract.

## Cakupan yang sudah diimplementasikan

- Pemindaian rekursif file Markdown pada direktori konten.
- Parsing YAML frontmatter dengan penolakan duplicate key.
- Frontmatter harus berupa mapping/object.
- `id` dokumen wajib integer positif; boolean tidak diterima sebagai integer.
- Keunikan ID dokumen diperiksa global lintas semua file/collection yang dipindai.
- `schema` harus berupa object dengan `type` string non-kosong.
- Jika `slug` ada, nilainya harus string non-kosong.
- Jika `blocks` ada, harus berupa array; setiap block harus object dengan ID positif unik lokal dan `component` non-kosong.
- `publishedDate` dan `updatedDate`, bila ada, harus ISO 8601 UTC presisi detik.
- `updatedDate` tidak boleh lebih awal dari `publishedDate`.
- Pesan error menyebut path dan field/masalah.

## Batas yang sengaja belum diklaim selesai

Milestone ini **belum** memvalidasi kontrak spesifik Homepage, Menu, Page, Article, Service, dan Category; SEO object; Schema Registry lengkap; relasi/FK dan kardinalitas; block registry beserta props; menu target/depth; slug-route collisions; tautan/aset; sitemap; breadcrumb; atau aturan editorial. Pemeriksaan tersebut menjadi tahapan berikutnya dan tidak boleh dianggap lulus hanya karena validator inti lulus.

## Menjalankan

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_content.py src/content
pytest -q
```

`src/content` adalah contoh lokasi; gunakan root yang memuat seluruh collection Markdown proyek agar pemeriksaan ID benar-benar global.

## Hasil uji milestone 1

Uji unit mencakup frontmatter valid, duplicate YAML key, ID dokumen lintas direktori, ID block lokal, timestamp nonkanonis, urutan tanggal, dan penolakan boolean sebagai ID. Hasil aktual dicatat setelah test suite dijalankan pada lingkungan target.
