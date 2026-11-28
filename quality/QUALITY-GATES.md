# Quality Gates & Acceptance Criteria

> Status: Standar verifikasi
> Versi: 0.8

## Batas kemampuan validator

Status gate harus ditafsirkan bersama [Batas Kemampuan Standar dan Validator](../docs/CAPABILITY-BOUNDARIES.md). Validator referensi hanya membuktikan pemeriksaan statis yang benar-benar diimplementasikan; ia tidak membuktikan rendering Astro, hasil HTML/JSON-LD, accessibility browser, production build, atau approval editorial. Bukti proyek dan manusia tetap wajib sesuai jenis gate.

## 1. Prinsip

Website dinyatakan memenuhi standar hanya jika validasi konten, relasi, routing, aset, metadata, schema, dan build produksi berhasil. Build Astro yang sukses saja tidak cukup.

## 2. Gerbang wajib

| Gate | Pemeriksaan | Kriteria lulus |
|---|---|---|
| QG-01 Frontmatter | Field wajib, tipe, enum, field tak dikenal | Semua dokumen valid terhadap kontrak jenisnya |
| QG-02 Document ID | ID integer positif lintas collection | Tidak ada duplikasi ID dokumen |
| QG-03 Block ID | ID integer positif per dokumen | Tidak ada duplikasi ID block dalam dokumen yang sama |
| QG-04 Slug/route | Format slug dan konflik route | Tidak ada route konflik; redirect ditangani |
| QG-05 Relations | Target collection, ID, kardinalitas | Semua FK valid dan target tersedia |
| QG-06 Block registry | Nama component dan props | Semua block terdaftar dan props sesuai schema |
| QG-07 SEO | Title, description, canonical, social metadata | Tidak kosong, canonical absolut, tidak duplikat |
| QG-08 Schema.org | JSON-LD valid, sesuai konten, dan sesuai Schema Registry | JSON valid, node konsisten, tidak ada properti fiktif; Schema Registry tersedia, tipe yang dipakai terdaftar beserta scope dan pemetaan field, serta tidak konflik dengan Block Registry |
| QG-09 Assets | Gambar, media, internal/external links | Semua referensi lokal tersedia dan tautan valid |
| QG-10 Accessibility | Alt, heading, label, keyboard, contrast | Tidak ada pelanggaran kritis yang diketahui |
| QG-11 Production build | Build produksi | Exit code sukses |
| QG-12 Editorial quality | Kecukupan, akurasi, orisinalitas, keterbacaan, dan nilai tambah | Review editorial terdokumentasi dan seluruh kriteria yang relevan lulus; tidak menggunakan target jumlah kata sebagai syarat |
| QG-13 Information architecture | Konsistensi sitemap/route manifest, navigasi, breadcrumb, listing, dan kebijakan indexability | Artefak IA proyek tersedia; route yang dipublikasikan, navigasi, breadcrumb, dan listing konsisten dengan keputusan IA; pengecualian terdokumentasi |

## 3. Review editorial

QG-12 merupakan gerbang review manusia/ahli, bukan pemeriksaan otomatis jumlah kata. Reviewer menggunakan [Content Quality Standard](CONTENT-QUALITY-STANDARD.md), menyesuaikan checklist dengan jenis halaman, dan mencatat hasil review pada PR, issue, atau catatan publikasi. Untuk topik berisiko tinggi, reviewer harus memiliki kompetensi yang relevan.

Konten tidak lulus jika memiliki klaim material yang belum diverifikasi, tidak memberi nilai tambah, dibuat massal hanya dengan variasi keyword/lokasi, atau tidak memenuhi tujuan halaman. Panjang konten hanya boleh dipakai sebagai sinyal diagnostik, bukan skor atau target kelulusan.

## 4. Verifikasi Information Architecture

QG-13 memeriksa konsistensi keputusan IA yang dapat dinyatakan secara eksplisit dan diuji. Implementasi proyek harus menentukan artefak mesin yang menjadi acuan (misalnya route manifest atau sitemap configuration) serta menguji:

- Setiap route yang dipublikasikan dipetakan ke jenis dan tujuan halaman dalam sitemap/route manifest.
- Setiap halaman yang seharusnya indexable tercakup dalam sitemap XML; halaman noindex, utilitas, atau pengecualian lain mengikuti kebijakan tertulis.
- Target menu dan breadcrumb mengarah ke route yang tersedia dan sesuai pemetaan IA.
- Listing/related-content menggunakan filter, urutan, batas hasil, dan perilaku empty state yang deterministik sesuai keputusan proyek.
- Perubahan route memperbarui redirect dan referensi navigasi yang relevan.

QG-13 tidak menilai otomatis apakah dua halaman memiliki intent berbeda atau apakah tautan kontekstual benar-benar relevan secara semantik. Penilaian tersebut tetap bagian dari QG-12 dan review arsitektur manusia. QG-13 tidak mewajibkan semua halaman masuk menu utama atau memiliki jumlah tautan tertentu.

## 5. Format laporan error

Setiap validator harus menampilkan:
- Kode gate dan jenis error.
- Path file sumber.
- Field atau block yang bermasalah.
- Nilai/ID terkait bila aman ditampilkan.
- Penjelasan singkat dan tindakan koreksi.

Contoh:

```text
[QG-05 RELATION_NOT_FOUND]
File: src/content/articles/panduan.md
Field: relatedServiceId
Value: 999
Expected target: services
Action: gunakan ID layanan yang tersedia atau hapus relasi opsional.
```

## 6. Acceptance criteria rilis

Rilis dapat diterima jika seluruh gate wajib berstatus lulus, build produksi sukses, dan tidak ada pengecualian yang belum disetujui. QG-12 dinyatakan lulus melalui catatan persetujuan reviewer pada PR, issue, atau catatan publikasi; bukan melalui pemeriksaan otomatis. Pengecualian harus dicatat dengan alasan, cakupan, pemilik, dan batas waktu penyelesaian.

## 7. Test matrix minimum

| Skenario | Hasil yang diharapkan |
|---|---|
| Dua dokumen berbeda memiliki ID sama | Gagal QG-02 |
| Dua dokumen berbeda masing-masing memiliki block ID 1 | Lulus QG-03 |
| Dua block dalam dokumen sama memiliki ID sama | Gagal QG-03 |
| Relasi menunjuk ID yang tidak ada | Gagal QG-05 |
| Relasi menunjuk collection yang salah | Gagal QG-05 |
| Menu memiliki `pageId` dan `url` sekaligus | Gagal QG-01/QG-05 |
| Menu tidak memiliki `pageId` maupun `url` | Gagal QG-01/QG-05 |
| SEO title kosong tetapi title dokumen tersedia | Lulus; fallback digunakan |
| SEO title dan title dokumen sama-sama kosong | Gagal QG-07 |
| Block memakai component tidak terdaftar | Gagal QG-06 |
| Block memiliki props yang tidak dikenal | Gagal QG-06 |
| Timestamp menggunakan offset `+07:00` | Gagal QG-01 |
| `updatedDate` lebih awal dari `publishedDate` | Gagal QG-01 |
| Dua dokumen memiliki timestamp sama | Lulus; timestamp bukan identitas |
| Featured image tidak memiliki alt | Gagal QG-01/QG-10 |
| JSON-LD memiliki JSON tidak valid | Gagal QG-08 |
| Tipe Schema.org dipakai tetapi tidak terdaftar di Schema Registry | Gagal QG-08 |
| Schema Registry dan Block Registry memberi aturan bertentangan untuk satu tipe | Gagal QG-08 |
| `intro` Page, Article, atau Service tidak tersedia | Gagal QG-01 |
| `intro` Page, Article, atau Service bukan string | Gagal QG-01 |
| `intro` hanya berisi whitespace | Gagal QG-01 |
| `intro` berisi lebih dari satu paragraf | Gagal QG-01 |
| `intro` mengandung markup HTML atau Markdown | Gagal QG-01 |
| Intro tidak dirender sebagai paragraf pembuka yang terlihat setelah judul halaman | Gagal QG-08 |
| Page definisi memakai `schema.type: DefinedTerm` sebagai page-level type | Gagal QG-08 |
| Page definisi memakai `schema.mainEntity.type: DefinedTerm` dengan `schema.type` berupa page-level type yang valid (misalnya `WebPage`) | Lulus QG-08 jika pemetaan dan graph valid |
| Article atau Service mendeklarasikan `schema.mainEntity.type: DefinedTerm` | Gagal QG-08; DefinedTerm pada kontrak ini hanya untuk Page glosarium/definisi |
| `schema.mainEntity.type: DefinedTerm` tetapi intro tidak diawali judul dokumen dan kata "adalah" | Gagal QG-08 |
| Judul pada pola intro berbeda hanya dalam kapitalisasi atau spasi berlebih setelah normalisasi | Lulus pemeriksaan pola QG-08 |
| Intro DefinedTerm hanya berisi `<title> adalah` tanpa definisi setelahnya | Gagal QG-08 |
| `description` atau `seo.description` tersedia tetapi `intro` DefinedTerm tidak tersedia | Gagal QG-01/QG-08 |
| Artikel membahas istilah tetapi tidak mendefinisikan satu istilah sebagai tujuan utamanya | Lulus tanpa node DefinedTerm |
| `DefinedTerm.description` diambil dari `description` dokumen atau `seo.description`, bukan `intro` | Gagal QG-08 |
| Node DefinedTerm tidak terhubung melalui `WebPage.mainEntity` atau tidak memiliki `@id` stabil | Gagal QG-08 |
| Build produksi gagal | Gagal QG-11 |
| Konten panjang tetapi repetitif dan tidak memberi nilai tambah | Gagal QG-12 |
| Konten singkat tetapi sudah memenuhi tujuan halaman secara memadai | Dapat lulus QG-12 |
| Halaman lokasi hanya mengganti nama kota tanpa informasi unik | Gagal QG-12 |
| Klaim regulasi/teknis penting tidak memiliki verifikasi yang memadai | Gagal QG-12 |
| Route indexable tidak tercatat dalam sitemap/route manifest tanpa pengecualian | Gagal QG-13 |
| Breadcrumb/menu mengarah ke route yang tidak tersedia | Gagal QG-13 |
| Listing memiliki urutan atau filter yang tidak deterministik | Gagal QG-13 |
| Halaman sengaja tidak ditautkan dari menu utama tetapi dapat ditemukan melalui jalur lain yang ditetapkan | Dapat lulus QG-13 |

## 8. CI dan verifikasi lokal

Validator referensi `scripts/validate_content.py` menjalankan pemeriksaan frontmatter/kontrak, ID, relasi, Block Registry, Schema Registry, SEO/canonical, dan slug/route pada entry point CLI. `--site-root` mengaktifkan aset/internal link; `--route-manifest` mengaktifkan route manifest, sitemap, dan redirect; `--route-prefixes` memuat override JSON. `--contract-registry` mendaftarkan collection proyek tambahan sesuai kontrak ekstensi v1. Mode parsial tetap tersedia untuk diagnosis awal, tetapi **validasi proyek yang dijadikan bukti penerimaan wajib memakai `--require-project-gates`**, yang menolak eksekusi jika `--site-root` atau `--route-manifest` tidak diberikan:

```bash
python scripts/validate_content.py src/content --site-root . --route-manifest projects/nama-proyek/route-manifest.yml --require-project-gates
```

Route default dan format manifest, override prefix, serta batas otomatisasi tiap gate dijelaskan dalam [Validator Milestone 5](../VALIDATOR-MILESTONE-5.md). Workflow repository standar menjalankan smoke-test `python scripts/validate_content.py --help` dan suite `pytest -q`, termasuk test integrasi CLI. Hasil workflow pada commit terbaru tetap harus diperiksa; konfigurasi workflow bukan bukti hasil lulus. Status ini tidak mengurangi kriteria normatif QG-04/QG-07/QG-09/QG-13: setiap proyek tetap wajib membuktikan gate yang relevan melalui integrasi validator atau pemeriksaan proyek yang setara. Setiap proyek Astro wajib menambahkan pemindaian corpus miliknya, production build, serta audit hasil render untuk JSON-LD, SEO, dan accessibility. QG-12 tetap membutuhkan persetujuan reviewer manusia.



Gate otomatis/static yang didukung validator referensi wajib dijalankan dengan mode proyek lengkap. QG-10 memerlukan audit accessibility hasil render/browser; QG-11 memerlukan production build Astro; QG-12 memerlukan review manusia. Ketiganya tidak boleh dianggap lulus dari output validator atau pytest. Gate otomatis dan pemeriksaan proyek QG-10, QG-11, serta QG-13 harus dijalankan secara lokal dan pada CI untuk pull/push yang mengubah konten, schema, komponen block, routing, atau konfigurasi SEO. Perintah final ditetapkan oleh implementasi proyek dan didokumentasikan di README proyek. QG-12 tetap menjadi review manusia: hasilnya dibuktikan dengan catatan persetujuan reviewer pada PR, issue, atau catatan publikasi sebelum rilis, dan tidak diwakili oleh pemeriksaan CI.