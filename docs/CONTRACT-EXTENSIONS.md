# Project Collection Contract Extensions

> Status: mekanisme ekstensi v1 untuk collection domain proyek. Ini bukan penambahan kontrak inti Content Contract.

## Tujuan dan batas

Enam kind inti tetap menjadi kontrak lintas proyek: `homepage`, `menu`, `page`, `article`, `service`, dan `category`. Collection domain seperti `training` dan `schedule` tidak boleh dipetakan secara paksa ke Page atau Article.

Validator mendukung file registry proyek melalui `--contract-registry`. Registry ekstensi mendefinisikan direktori, field wajib, tipe field, tipe Schema.org yang diterima, route prefix, dan foreign-key sederhana. Registry harus disimpan dan direview bersama konfigurasi proyek.

## Format v1

```yaml
version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, slug, title, schema, updatedDate]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      schema: object
      updatedDate: utc_datetime
      scheduleIds: positive_int_array
    schemaTypes: [Course]
    routePrefix: /training/
    relations:
      scheduleIds:
        target: schedule
        cardinality: many

  schedule:
    directory: schedules
    requiredFields: [id, slug, title, schema, updatedDate, startDate]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      schema: object
      updatedDate: utc_datetime
      startDate: string
    schemaTypes: [Event]
    routePrefix: /schedule/
```

`directory` relatif terhadap `content_dir` yang diberikan pada CLI. Nama kind ekstensi harus berupa identifier lowercase baru dan tidak boleh menimpa enam kind inti.

Tipe field v1:
- `string`
- `positive_int`
- `boolean`
- `object`
- `array`
- `utc_datetime` (ISO 8601 UTC presisi detik, mengikuti kontrak inti)
- `string_array`
- `positive_int_array`

Relasi v1 mendukung kardinalitas `one` atau `many` dengan target kind yang diindeks berdasarkan ID dokumen. Target yang hilang atau ambigu menggagalkan validasi.

## Pemanggilan

```bash
python scripts/validate_content.py src/content \
  --site-root . \
  --contract-registry config/content-contracts.yml \
  --route-manifest config/route-manifest.yml
```

Collection inti tetap dapat dipetakan dengan `--collection KIND=DIR`. Opsi tersebut tetap terbatas pada enam kind inti; ekstensi didaftarkan melalui file registry.

## Batasan v1

- Tipe Schema.org hanya diperiksa terhadap daftar yang dinyatakan pada `schemaTypes`; validator referensi belum menghasilkan JSON-LD.
- Field bertipe `object` dan `array` hanya diperiksa bentuk luarnya. Validasi nested object, discriminator block, refinement lintas-field (misalnya `endDate >= startDate`), dan semantik domain harus ditambahkan melalui kontrak proyek atau validator khusus.
- Relasi hanya memeriksa ID positif, target kind, keberadaan, dan keunikan target. Tidak ada inferensi relasi otomatis.
- Route dibangun dari `routePrefix` dan `slug`; redirect dan sitemap tetap diverifikasi melalui route manifest.
- Ekstensi tidak mengubah kontrak inti, registry Block lintas proyek, maupun kebijakan Quality Gates.

## Kriteria penerimaan proyek

Sebelum extension registry dipakai pada produksi, proyek harus:
1. Menyimpan registry di repository dan menambahkan fixture valid/invalid untuk setiap collection.
2. Mendefinisikan field, tipe Schema.org, route, dan relasi yang benar-benar dipakai.
3. Menambahkan validasi nested/domain-specific yang tidak dicakup tipe generik v1.
4. Menjalankan validator pada seluruh corpus proyek, lalu mencatat jumlah file, hasil, pengecualian, dan commit.
5. Menjalankan build Astro dan pengujian graph JSON-LD hasil render secara terpisah.
