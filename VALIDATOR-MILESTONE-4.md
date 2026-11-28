# Validator Milestone 4 — Schema Registry dan Block Registry

> Status: implementasi awal selesai; perluasan registry per proyek dilakukan melalui keputusan proyek yang eksplisit.

## Tujuan
Milestone ini membuat deklarasi Schema.org dan block dapat diperiksa oleh validator, bukan hanya diterima sebagai object bebas. Validator tidak menghasilkan JSON-LD dan tidak menggantikan validasi eksternal Schema.org/Google.

## Implementasi

### Schema Registry
- Memisahkan tipe Schema.org untuk scope block, page, dan entity.
- Memvalidasi schema.type dokumen terhadap tipe page-level yang diizinkan.
- Mengakomodasi SiteNavigationElement untuk menu dan Service untuk dokumen service sesuai kontrak yang sudah ada.
- Mengizinkan schema.mainEntity.type: DefinedTerm hanya pada Page.
- Menolak properti schema tingkat frontmatter yang belum didefinisikan.
- Memvalidasi schema block berdasarkan tipe terdaftar dan pasangan component–schema yang diizinkan.

### Pemetaan JSON-LD yang diregistrasikan

Registry menyediakan pemetaan sumber untuk tipe yang mempunyai kontrak eksplisit:
- WebPage: document.title → name, document.description → description, canonical route → url.
- Article: document.title → headline, description → description, tanggal publikasi/pembaruan → datePublished/dateModified, featuredImage → image.
- Service: document.title → name dan document.description → description.
- CollectionPage: document.title → name, document.description → description, canonical route → url.
- SiteNavigationElement: document.title → name.
- FAQPage: items[].question + items[].answer → mainEntity Question/acceptedAnswer.
- HowTo: title/description/steps[].name/steps[].text → HowTo dan HowToStep.
- ItemList: items[] → itemListElement.
- Table: headers/rows → struktur Table.
- ImageObject: src/alt/caption → contentUrl/description/caption.
- DefinedTerm: document.title → name dan document.intro → description.

Pemetaan ini adalah kontrak sumber data bagi implementasi JSON-LD. Validator saat ini memeriksa scope, tipe, pasangan block–schema, dan keberadaan sumber wajib pada block; ia belum merender graph atau memvalidasi setiap properti keluaran JSON-LD.

### Block Registry
- Menambahkan daftar identifier block dari Content Contract dan katalog gabungan komponen.
- Memisahkan block dari UI component; komponen UI yang tidak dideklarasikan sebagai block tidak otomatis dapat dipakai pada frontmatter.
- Memvalidasi nama component, props yang dikenal, props spesifik komponen untuk subset yang kontraknya eksplisit, serta tipe data props.
- Menolak component dan props yang tidak dikenal.
- Registry props konservatif untuk block yang katalog gabungannya belum menyediakan kontrak API tunggal lintas proyek. Proyek harus memperluas kontrak melalui registry proyek.

## Catatan audit konsistensi registry (2026-11-28)

Audit kode menemukan bahwa `SCHEMA_TYPES["page"]` memuat tipe yang lebih banyak daripada mapping pada `SCHEMA_REGISTRY`. Perbaikan menambahkan status eksplisit per scope melalui `SCHEMA_SCOPE_STATUS`: tipe dengan mapping terdaftar dinyatakan `mapped`, sedangkan tipe lain dinyatakan `declaration-only` melalui `SCHEMA_DECLARATION_ONLY_BY_SCOPE` (serta alias page-level `SCHEMA_TYPE_STATUS`). Dengan demikian, scope yang diterima tidak lagi secara implisit mengklaim bahwa semua tipe memiliki mapping generator. Kontrak dokumen inti menolak penggunaan tipe berstatus `declaration-only` sampai proyek menyediakan mapping yang dapat diuji; status tersebut hanya mencatat bahwa tipe ada dalam scope katalog, bukan bahwa validator mendukung JSON-LD-nya.

Kriteria penutupan:
- Setiap tipe yang diizinkan pada scope dan diwajibkan menghasilkan JSON-LD harus memiliki entri registry beserta pemetaan sumber yang eksplisit. Kontrak dokumen inti menolak tipe `declaration-only` sampai mapping proyek disediakan.
- Jika suatu tipe hanya diizinkan untuk deklarasi tetapi belum didukung mapping, status tersebut harus dinyatakan eksplisit (`declaration-only`) dan tidak boleh dianggap sebagai dukungan generator.
- Test registry memastikan setiap page type berada tepat pada salah satu status: `mapped` atau `declaration-only`.
- Test harus mencakup seluruh tipe yang diizinkan pada setiap scope, termasuk tipe yang sengaja belum didukung, dan memastikan tipe `declaration-only` tidak lolos sebagai mapping yang didukung pada scope terkait.
- `googleRichResultSupport` adalah metadata informasional yang perlu ditinjau berkala; nilainya bukan jaminan rich result akan ditampilkan.

Catatan ini mendokumentasikan temuan audit, bukan memperluas atau mengubah daftar tipe normatif.

## Batasan yang disengaja
- Katalog lintas proyek adalah inventaris adopsi, bukan perintah mengimplementasikan seluruh komponen.
- Validator tidak memverifikasi kesesuaian semantik konten, kelayakan rich result, atau kebenaran JSON-LD hasil render.
- Status dukungan Google harus diperiksa ulang saat proyek menetapkan Schema Registry final.
- documentationUrl, verifiedAt, entitySource, dan pemetaan properti lengkap wajib ditetapkan dalam Schema Registry proyek sebelum implementasi JSON-LD; reference validator memeriksa penggunaan tipe dan scope, bukan menjalankan renderer JSON-LD.

## Pengujian
Suite mencakup tipe page tidak dikenal, tipe entity salah scope, DefinedTerm, properti schema tidak dikenal, component tidak terdaftar, props tidak dikenal/tidak sesuai component, tipe props, pasangan block–schema yang tidak diizinkan, dan konsistensi cakupan status semua page type.

Jalankan:

```bash
python -m pytest -q
```

Milestone 5 menangani route/slug collision, aset, tautan internal/eksternal, dan integrasi Quality Gates.
