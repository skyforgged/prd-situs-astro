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
    schemaMappings:
      Course:
        fieldMapping:
          name: title
          description: description
        requiredFields: [title, description]
    routePrefix: /training/
    relations:
      scheduleIds:
        target: schedule
        cardinality: many

  schedule:
    directory: schedules
    requiredFields: [id, slug, title, schema, updatedDate, startDate, endDate]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      schema: object
      updatedDate: utc_datetime
      startDate: string
      endDate: string
    schemaTypes: [Event]
    schemaMappings:
      Event:
        fieldMapping:
          name: title
          startDate: startDate
          endDate: endDate
        requiredFields: [title, startDate, endDate]
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
- `offset_datetime` (ISO 8601 datetime yang wajib memiliki zona waktu/offset)
- `iso_date_or_datetime` (tanggal ISO atau datetime ISO)
- `ulid` (ULID 26 karakter)
- `string_array` dan `positive_int_array`
- `string_array`
- `positive_int_array`

Setiap `schemaType` wajib memiliki `schemaMappings` yang mendefinisikan `fieldMapping` (property Schema.org ke field sumber) dan `requiredFields`. Proyek dapat menetapkan `schemaType` statis pada registry jika tipe schema tidak disimpan pada frontmatter; jika tidak, validator membaca `schema.type` pada dokumen. Validator memeriksa bahwa field sumber dan field wajib mapping tersedia pada dokumen; mapping ini menjadi kontrak sumber bagi implementasi JSON-LD proyek, bukan generator JSON-LD itu sendiri. Tipe Schema.org yang diterima tanpa mapping ditolak. `fieldEnums` dapat menetapkan enum string pada field.

Relasi v1 mendukung kardinalitas `one` atau `many` dengan target kind dan `targetField`. Default `targetField` adalah `id`; untuk extension collection, relasi juga dapat memakai natural key seperti `trainingSlug`. Tipe field sumber dan target diperiksa kesesuaiannya. Target yang hilang atau ambigu menggagalkan validasi. Semua extension document tetap wajib memakai `id` integer positif yang unik secara global.


## Contoh berbasis collection training/schedule

File `examples/content-contracts/training-schedule.yml` memperlihatkan bentuk ekstensi yang lebih dekat dengan collection training dan schedule: ULID tambahan, `pubDate` ber-offset, tanggal schedule, enum status, tipe schema statis `Course`/`Event`, pemetaan field JSON-LD, route prefix, dan relasi natural key `schedule.trainingSlug -> training.trainingSlug`. Contoh ini tetap hanya memvalidasi tipe field dan relasi yang dideklarasikan; nested Zod schema dan refinement domain proyek belum seluruhnya direplikasi.

## Pemanggilan

```bash
python scripts/validate_content.py src/content \
  --site-root . \
  --contract-registry config/content-contracts.yml \
  --route-manifest config/route-manifest.yml
```

Collection inti tetap dapat dipetakan dengan `--collection KIND=DIR`. Opsi tersebut tetap terbatas pada enam kind inti; ekstensi didaftarkan melalui file registry.

## Batasan v1

- Tipe Schema.org diperiksa terhadap `schemaTypes` dan harus memiliki `schemaMappings`; validator referensi belum menghasilkan JSON-LD.
- Field bertipe `object` dan `array` hanya diperiksa bentuk luarnya. Deklarasi enum wajib menunjuk field yang sudah memiliki tipe; setiap sumber `fieldMapping` dan `requiredFields` pada schema mapping wajib menunjuk field yang dideklarasikan pada `fieldTypes`. Direktori ekstensi tidak boleh bertumpang tindih dengan direktori ekstensi lain atau memakai nama direktori collection inti. `routePrefix` harus berupa path absolut ternormalisasi dan diakhiri `/`. Validasi nested object, discriminator block, refinement lintas-field (misalnya `endDate >= startDate`), validasi timezone IANA, dan semantik domain harus ditambahkan melalui kontrak proyek atau validator khusus.
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
