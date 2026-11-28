# Batas Kemampuan Standar dan Validator — PRD Situs Astro

> Versi 1.0 | 2026-11-28  
> Status: dokumentasi normatif tentang batas dukungan repository standar  
> Berlaku untuk: repository PRD ini dan proyek Astro turunan yang mengadopsinya

## 1. Tujuan

Dokumen ini mencegah salah tafsir bahwa keberadaan persyaratan dalam PRD, konfigurasi registry, atau test repository berarti fitur tersebut sudah tersedia sebagai implementasi end-to-end. Setiap kemampuan harus dibaca dalam salah satu dari tiga kategori:

1. **Didukung validator referensi** — pemeriksaan memang diimplementasikan pada `scripts/validate_content.py` atau registry yang dipanggilnya dan dapat dijalankan melalui CLI.
2. **Hanya berupa kontrak/standar** — aturan, struktur data, atau perilaku telah ditentukan dalam dokumen, tetapi repository standar belum menyediakan implementasi runtime lengkap untuk mewujudkannya.
3. **Wajib diimplementasikan proyek turunan** — memerlukan aplikasi Astro, konfigurasi, integrasi, data, browser, layanan eksternal, atau keputusan bisnis milik situs tertentu.

Satu persyaratan dapat melibatkan lebih dari satu kategori. Contohnya, validator dapat memeriksa bentuk SEO frontmatter, sementara proyek turunan tetap harus menghasilkan dan menguji tag SEO pada HTML hasil render.

## 2. Arti status dan cara menggunakannya

| Status | Makna | Bukti yang sah | Bukan bukti |
|---|---|---|---|
| **VALIDATOR** | Kode pemeriksaan tersedia pada repository standar. | Implementasi fungsi, test otomatis, dan hasil eksekusi CLI/CI pada commit tertentu. | Hanya adanya aturan di dokumen atau contoh YAML. |
| **CONTRACT** | Persyaratan normatif telah ditentukan, tetapi tidak otomatis diwujudkan oleh validator/runtime standar. | Dokumen kontrak, arsitektur, template, registry deklaratif. | Menganggap halaman, komponen, atau output sudah berfungsi. |
| **PROJECT** | Implementasi dan bukti harus disediakan situs Astro yang mengadopsi standar. | Kode proyek, test proyek, build, browser audit, CI, atau approval yang relevan. | Test validator referensi saja. |

**Aturan klaim:** status VALIDATOR berarti hanya bagian yang secara eksplisit diperiksa oleh kode. Ia tidak boleh diperluas menjadi klaim bahwa seluruh requirement, halaman, aplikasi, atau situs telah selesai.

## 3. Kemampuan yang sudah didukung validator referensi

Implementasi acuan: `scripts/validate_content.py`, registry pada `scripts/registries.py`, dan test pada `tests/test_validate_content.py`.

| Area | Dukungan aktual validator | Batas pemeriksaan |
|---|---|---|
| Parsing frontmatter | Membaca Markdown UTF-8, mengenali YAML frontmatter, menolak YAML tidak valid dan duplicate key. | Tidak memvalidasi kualitas isi Markdown secara semantik atau tata bahasa. |
| Collection inti | Validasi kontrak field untuk Homepage, Menu, Page, Article, Service, Category; field wajib, tipe dasar, dan allowlist field. | Tidak membuat Astro Content Collections atau mengubah source file. Schema Astro/Zod proyek tetap diperlukan. |
| Identitas | ID dokumen positif dan unik global dalam kumpulan file yang dipindai; ID block positif dan unik dalam satu dokumen. | Tidak menyediakan UI/layanan alokasi ID atau registry operasional bagi tim editor. |
| Timestamp | Memeriksa format UTC ISO 8601 presisi detik dan hubungan publishedDate/updatedDate bila keduanya ada. | Tidak mengatur workflow publikasi atau mengisi tanggal otomatis. |
| Menu | Memeriksa location, label, tepat satu target pageId/url, format target, external flag, dan kedalaman maksimum tiga. | Tidak merender navigasi, menentukan UX, atau memeriksa link menu pada browser. |
| Relasi inti | Memeriksa tipe FK, resolusi target, target kind, beberapa kardinalitas/duplikasi, serta siklus relasi yang dicakup kontrak. | Hanya relasi yang dipetakan pada validator/registry yang diperiksa; bukan ORM, query layer, atau sinkronisasi dua arah runtime. |
| Block registry | Memeriksa nama component yang terdaftar, props yang dikenal, tipe props, aturan komponen tertentu, dan schema block yang diizinkan. | Tidak mengimplementasikan komponen Astro, desain visual, interaksi, responsive behavior, atau accessibility renderer. |
| Schema registry | Memeriksa tipe schema yang terdaftar, pemisahan page/entity scope, properti yang diizinkan, dan aturan DefinedTerm yang dicakup. | Tidak menghasilkan atau memvalidasi seluruh graph JSON-LD akhir pada HTML situs. |
| SEO statis | Memeriksa bentuk SEO object, fallback title/description, format canonical absolut, dan duplikasi canonical pada dokumen yang dipindai. | Tidak menghasilkan meta tags, Open Graph/Twitter tags, canonical final, robots directives, atau memeriksa HTML hasil render. |
| Slug/route | Memeriksa slug kanonis, prefix aman, route hasil derivasi, dan collision berdasarkan konfigurasi/prefix validator. | Tidak membuat file route Astro, memeriksa route hasil build yang tidak tercermin di input, atau menguji navigasi browser. |
| Aset lokal | Menelusuri referensi aset lokal yang didukung dan mendeteksi file yang tidak ditemukan di site root. | Tidak mengoptimalkan gambar, membuat WebP/AVIF, memeriksa kualitas visual, ukuran transfer, atau memastikan aset yang dibuat runtime. |
| Link internal | Memeriksa referensi internal yang didukung terhadap daftar route hasil derivasi. | Tidak melakukan crawl browser end-to-end; tidak memeriksa status HTTP jaringan untuk URL eksternal. |
| Route manifest | Memeriksa struktur manifest, konsistensi route yang diharapkan, source path, sitemap, dan aturan redirect yang didukung. | Tidak membuat sitemap/redirect; tidak membuktikan sitemap yang benar-benar dipublikasikan oleh server. |
| Extension contracts | Memuat registry ekstensi v1; memeriksa fieldTypes, requiredFields, enum, schema mapping, route prefix, relation declaration, serta field frontmatter yang tidak dideklarasikan. | Tidak menyediakan runtime renderer, halaman, listing, form, atau proses domain untuk extension. |
| CLI dan acceptance statis | Menyediakan `--collection`, `--site-root`, `--route-manifest`, `--route-prefixes`, `--contract-registry`, dan `--require-project-gates`. | Mode lengkap tetap hanya menjalankan pemeriksaan statis yang memang tersedia; bukan pengganti build dan browser tests proyek. |

### 3.1 Perintah validasi

Mode diagnosis parsial:

```bash
python scripts/validate_content.py src/content
```

Mode acceptance statis proyek (mewajibkan site root dan route manifest):

```bash
python scripts/validate_content.py src/content \
  --site-root . \
  --route-manifest config/route-manifest.yml \
  --require-project-gates
```

Untuk collection ekstensi, tambahkan `--contract-registry config/content-contracts.yml`; untuk nama direktori/prefix yang berbeda dari default, gunakan `--collection KIND=DIR` dan/atau `--route-prefixes` sesuai kebutuhan. Gunakan `python scripts/validate_content.py --help` untuk opsi yang tersedia pada versi checkout aktual.

## 4. Persyaratan yang saat ini berupa kontrak/standar

Hal-hal berikut telah diatur dalam dokumen normatif atau template, tetapi tidak boleh dianggap telah disediakan sebagai fitur lengkap hanya karena kontraknya ada.

| Area | Sumber normatif | Yang sudah ditetapkan | Yang belum otomatis disediakan oleh standar |
|---|---|---|---|
| Model konten dan frontmatter | Content Contract; Frontmatter Templates; Training/Schedule Contract | Nama kind, field, relasi, bentuk data, kerangka field. | Astro collections aktual, editor konten, migrasi data, dan generator dokumen. |
| Block/component catalog | Component Block Catalog; Content Contract | Nama block, kontrak props, dan perilaku yang diharapkan. | Implementasi file komponen, CSS, interaksi, responsive UI, dan visual regression. |
| Schema.org | Content Contract; Schema Registry; Technical Architecture | Type, scope, property, hubungan entitas, dan batas schema. | Generator JSON-LD lengkap, penggabungan graph runtime, pengujian rich result, dan pemantauan hasil mesin pencari. |
| SEO | Content Contract; Technical Architecture | Field SEO, fallback, canonical, dan metadata yang diharapkan. | Komponen/layout metadata Astro dan verifikasi HTML produksi. |
| Relasi dan query | Content Contract; Technical Architecture | FK, target collection, kardinalitas, dan prinsip query. | Data access layer/runtime query, cache, optimasi, serta API. |
| Routing dan IA | Content & Information Architecture; Technical Architecture | Prinsip sitemap, route, menu, breadcrumb, listing, pagination, internal linking, dan redirect. | Implementasi halaman, query listing, filter/sort, breadcrumb renderer, redirect server/hosting, dan pengujian UX. |
| UI/configuration | Constitution; Technical Architecture; Project Templates | Pemisahan konten substantif dan konfigurasi UI. | Design system, theme tokens, layout, komponen global, dan integrasi CMS. |
| Governance/editorial | Content Quality Standard; Project Templates; Quality Gates | Peran, checklist, prinsip akurasi, lifecycle, dan approval. | Reviewer, workflow persetujuan, audit sumber, dan mekanisme publikasi. |
| Inisialisasi proyek | Project Initialization Workflow dan dokumen template | Tahapan discovery, model, IA, governance, arsitektur, readiness. | Pengumpulan data bisnis, keputusan stakeholder, riset pasar, serta pengisian artefak proyek. |

Kontrak adalah spesifikasi yang mengikat implementasi, bukan bukti implementasi sudah ada.

## 5. Kewajiban implementasi pada proyek Astro turunan

| Kapabilitas proyek | Implementasi minimum yang wajib disediakan proyek | Bukti penerimaan |
|---|---|---|
| Astro application | Struktur source, konfigurasi Astro, package/dependency lock, content collections, layouts, pages, dan komponen. | Typecheck/build produksi berhasil di CI. |
| Rendering konten | Renderer per kind dan pemetaan seluruh block registry ke komponen yang benar. | Render tests atau browser tests untuk setiap block yang digunakan dan halaman representatif. |
| Design system/responsive | Token, typography, spacing, warna, breakpoint, layout, states, dan responsive behavior. | Visual review dan viewport/browser tests. |
| Navigation/IA | Header/footer/menu, breadcrumb, listing, related content, pagination, filter/sort, empty state, dan route. | Route smoke tests, browser/E2E tests, IA review. |
| SEO output | Title, description, canonical, robots, Open Graph, Twitter, metadata image dan locale. | Assertion pada HTML hasil build/render dan pemeriksaan URL canonical. |
| JSON-LD runtime | Graph koheren, @id stabil, relasi entity, sumber data nyata, tanpa node/property duplikat. | Parse JSON-LD hasil render, schema validation, dan review kesesuaian dengan konten terlihat. |
| Media pipeline | File image tersedia, transformasi format/resolusi, dimensi, alt, lazy loading, dan fallback. | Asset build checks, image output checks, serta audit performa. |
| Accessibility | Semantic HTML, keyboard, focus, contrast, heading order, accessible names, labels, dan ARIA. | Automated accessibility scan ditambah audit keyboard/manual pada halaman render. |
| Performance/security | Optimasi JS/CSS/image, cache, headers, dependency hygiene, dan praktik keamanan sesuai hosting. | Lighthouse/performance budget dan security checks proyek. |
| Integrasi eksternal | Form, email, CRM, analytics, search, CMS, API, atau layanan pihak ketiga bila dipilih proyek. | Integration tests atau bukti transaksi end-to-end; secrets dikelola aman. |
| Build/deploy | Build produksi, environment config, hosting adapter, redirects, sitemap, robots, dan deployment workflow. | CI build/deploy log dan smoke test URL yang dipublikasikan. |
| Editorial/release | Review konten, sumber klaim, persetujuan, dan catatan rilis. | Approval reviewer yang dapat ditelusuri; bukan status dari validator. |

Proyek boleh memilih implementasi setara selama memenuhi kontrak dan acceptance criteria. Bila kapabilitas tidak digunakan, dokumentasikan sebagai **Not Applicable** beserta alasan dan dampaknya.

## 6. Pemetaan batas Quality Gates

| Gate | Dukungan validator referensi | Tambahan wajib proyek / manusia |
|---|---|---|
| QG-01 Frontmatter | Otomatis untuk kontrak dan tipe yang terdaftar. | Jalankan terhadap seluruh corpus proyek; schema Astro tetap diuji pada build. |
| QG-02 Document ID | Otomatis untuk ID global pada input yang dipindai. | Pastikan cakupan pemindaian mencakup semua collection dan data yang dipakai. |
| QG-03 Block ID | Otomatis untuk ID block per dokumen. | Pastikan seluruh block yang dirender masuk corpus validator. |
| QG-04 Slug/route | Otomatis untuk derivasi route, slug, prefix, collision. | Uji route hasil build, dynamic routes, dan URL yang benar-benar dipublikasikan. |
| QG-05 Relations | Otomatis untuk FK dan relasi yang dikontrak. | Implementasikan query/runtime behavior dan uji seluruh alur relasi yang digunakan. |
| QG-06 Block registry | Otomatis untuk registry/props yang didukung. | Pastikan setiap komponen terimplementasi dan diuji di browser. |
| QG-07 SEO | Otomatis sebagian: fallback dan canonical statis. | Uji seluruh metadata HTML hasil render. |
| QG-08 Schema.org | Otomatis sebagian: registry dan aturan schema statis. | Generate dan validasi JSON-LD hasil render; review data nyata dan kelayakan rich result secara terpisah. |
| QG-09 Assets/links | Otomatis sebagian: aset lokal dan internal path yang didukung, manifest/sitemap. | Uji hasil build, link browser, status eksternal, dan URL publik bila dibutuhkan. |
| QG-10 Accessibility | Tidak ada audit hasil render penuh pada validator referensi. | Automated scan dan audit keyboard/manual pada aplikasi. |
| QG-11 Production build | Tidak dijalankan oleh validator referensi. | Build Astro pada CI proyek. |
| QG-12 Editorial | Tidak dapat diotomatisasi validator. | Persetujuan reviewer manusia dan release record. |
| QG-13 Information Architecture | Otomatis sebagian: route manifest, sitemap, source, redirect. | Review relevansi struktur, navigasi, listing, dan pengalaman pengguna. |

## 7. Klaim yang dilarang tanpa bukti tambahan

Jangan menyatakan hal-hal berikut hanya berdasarkan validator atau test repository standar:

- "Situs Astro sudah selesai/dapat dijalankan."
- "Semua komponen block sudah tersedia dan tampil benar."
- "SEO dan JSON-LD halaman sudah benar pada HTML produksi."
- "Sitemap dan redirect sudah aktif di hosting."
- "Semua link eksternal aktif."
- "Situs sudah accessible, cepat, aman, atau lolos Lighthouse."
- "Konten sudah akurat, berkualitas, dan disetujui."
- "Seluruh QG-01 sampai QG-13 lulus."

Klaim tersebut memerlukan bukti PROJECT atau MANUAL yang disebutkan pada dokumen ini dan Quality Gates.

## 8. Definition of Done untuk adopsi PRD

Proyek turunan baru dapat menyatakan standar ini telah diadopsi dengan benar jika:

1. Keputusan proyek dan template yang relevan telah diisi atau ditandai Not Applicable dengan alasan.
2. Content model, field, relasi, block, schema, route, dan konfigurasi proyek memiliki implementasi yang sesuai kontrak.
3. Validator referensi dijalankan pada seluruh corpus dengan `--require-project-gates`, site root, route manifest, dan extension registry bila digunakan.
4. Test proyek mencakup rendering, route, metadata SEO, JSON-LD, aset/link, dan perilaku komponen yang digunakan.
5. Accessibility scan, production build, serta pemeriksaan performance/security yang relevan dijalankan di CI proyek.
6. QG-12 memiliki approval manusia dan seluruh pengecualian dicatat.
7. Laporan penerimaan memisahkan hasil VALIDATOR, PROJECT, dan MANUAL; tidak ada status lulus tanpa bukti.

## 9. Pemeliharaan dokumen

Perbarui dokumen ini bila:
- validator menambah/menghapus/mengubah pemeriksaan;
- registry atau extension contract mengubah cakupan yang benar-benar diperiksa;
- test suite mengubah bukti otomatis;
- Quality Gates mengubah batas otomatisasi;
- standar baru memindahkan kemampuan dari kontrak ke implementasi validator atau menetapkan kewajiban proyek baru.

Setiap perubahan harus menyertakan file/fungsi yang berubah, test yang membuktikan perilaku, dan batas yang masih berlaku. Matriks traceability pada `docs/REQUIREMENTS-TRACEABILITY-MATRIX.md`, `VALIDATOR-MILESTONE-5.md`, `quality/QUALITY-GATES.md`, README, dan changelog harus tetap konsisten.

## 10. Riwayat perubahan

| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.0 | 2026-11-28 | Klasifikasi kemampuan validator, kontrak normatif, kewajiban proyek turunan, pemetaan QG, dan Definition of Done. |
