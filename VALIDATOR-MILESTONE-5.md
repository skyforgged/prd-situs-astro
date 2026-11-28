# Validator Milestone 5 — Route, Asset, Link, dan Quality Gates

> Status: fungsi pemeriksaan Milestone 5 tersedia dan memiliki unit test, tetapi integrasi end-to-end ke CLI/CI belum selesai. Dokumen ini mencatat rancangan pemeriksaan dan target penggunaan; jangan menganggap contoh CLI di bawah sudah menjalankan seluruh pemeriksaan.

## Tujuan

Milestone 5 menambahkan fungsi pemeriksaan statis lintas dokumen untuk slug, route, canonical, aset, tautan, dan route manifest. Pada kode yang diaudit (2026-11-28), fungsi-fungsi tersebut belum seluruhnya dipanggil oleh entry point CLI. Karena itu, pemeriksaan yang tersedia sebagai fungsi dan unit test belum dapat dianggap aktif melalui satu pemanggilan CLI.

## Pemeriksaan yang ditambahkan

### QG-04 — Slug dan route
- Slug harus lowercase ASCII alfanumerik dengan segmen yang dipisahkan satu tanda hubung.
- Route dihasilkan dengan prefix default: Homepage `/`, Page `/{slug}/`, Article `/articles/{slug}/`, Service `/services/{slug}/`, Category `/categories/{slug}/`.
- Konflik route lintas collection ditolak.
- Prefix dapat dioverride melalui file JSON `--route-prefixes` agar mengikuti keputusan IA proyek.
- Menu tidak menghasilkan route.

### QG-07 — SEO
- Validasi field SEO/fallback dan canonical absolut tetap dijalankan.
- Canonical yang sama (setelah normalisasi trailing slash) pada dua dokumen berbeda ditolak.

### QG-09 — Aset dan tautan
- Referensi media lokal pada field `src` dan `poster` diperiksa terhadap filesystem proyek.
- Markdown link internal ber-path absolut dan URL internal pada props `url`/`href` diperiksa terhadap route yang dihasilkan.
- Media lokal dalam Markdown ikut diperiksa.
- URL eksternal, mailto, tel, data URI, dan fragment tidak diakses melalui jaringan. Pemeriksaan HTTP eksternal sengaja tidak dilakukan pada validator deterministik ini.

### QG-13 — Information Architecture
- Route manifest YAML opsional memetakan path, source, dan status indexability.
- Manifest diperiksa untuk route ganda, route hasil content yang belum dicatat, source yang hilang, serta sitemap XML jika dikonfigurasi.
- Redirect harus memiliki `from` dan `to`, dan tidak boleh berupa self-loop.
- Pemeriksaan ini memvalidasi konsistensi eksplisit; ia tidak menilai relevansi semantik navigasi atau listing.

## Rancangan penggunaan CLI — integrasi masih tertunda

Contoh berikut menunjukkan bentuk pemanggilan yang dituju, bukan bukti bahwa seluruh pemeriksaan Milestone 5 telah terhubung. Pada versi kode yang diaudit, `main()` baru menjalankan `validate_paths()`; fungsi `validate_seo_uniqueness()`, `validate_routes()`, `validate_assets_and_links()`, dan `validate_route_manifest()` belum dipanggil dari entry point. Argumen `--site-root`, `--route-manifest`, dan `--route-prefixes` juga belum diteruskan ke fungsi pemeriksaan tersebut.

Instal dependensi dan jalankan unit test yang tersedia:

```bash
python -m pip install -r requirements-dev.txt
pytest -q
python scripts/validate_content.py src/content --site-root . --route-manifest projects/your-site/route-manifest.yml
```

Perintah di atas menjalankan validator yang terintegrasi saat ini, bukan seluruh rangkaian Milestone 5. Pemetaan collection dapat ditambahkan berulang:

```bash
python scripts/validate_content.py src/content \
  --collection homepage=src/content/homepages \
  --collection menu=src/content/menus \
  --collection page=src/content/pages \
  --collection article=src/content/articles \
  --collection service=src/content/services \
  --collection category=src/content/categories \
  --site-root . \
  --route-manifest projects/your-site/route-manifest.yml
```

Jika strategi route berbeda dari default:

```bash
python scripts/validate_content.py src/content --site-root . \
  --route-prefixes projects/your-site/route-prefixes.json
```

Contoh route-prefixes JSON:

```json
{
  "page": "/",
  "article": "/insight/",
  "service": "/layanan/",
  "category": "/topik/"
}
```

Format manifest minimum:

```yaml
routes:
  - path: /
    source: src/content/homepages/home.md
    indexable: true
  - path: /tentang-kami/
    source: src/content/pages/tentang-kami.md
    indexable: true
  - path: /kontak/
    source: src/pages/kontak.astro
    indexable: true
  - path: /hasil-pencarian/
    source: src/pages/hasil-pencarian.astro
    indexable: false

sitemap: public/sitemap.xml

redirects:
  - from: /profil-lama/
    to: /tentang-kami/
```

Semua route yang dihasilkan dari dokumen konten harus muncul di manifest. Route non-content dapat dicatat dengan source file Astro. Route `indexable: true` harus memiliki source. Sitemap, bila dicantumkan, harus tersedia dan memuat seluruh route indexable.

## Quality Gates: batas otomatisasi

| Gate | Status pada validator referensi | Batas |
|---|---|---|
| QG-01 Frontmatter | Otomatis | Kontrak dan tipe field yang terdaftar |
| QG-02 Document ID | Otomatis | ID unik global dalam root pemindaian |
| QG-03 Block ID | Otomatis | ID unik per dokumen |
| QG-04 Slug/route | Otomatis | Pola slug, route default/override, collision |
| QG-05 Relations | Otomatis | FK dan target collection yang sudah dikontrak |
| QG-06 Block registry | Otomatis | Registry referensi dan subset props eksplisit |
| QG-07 SEO | Otomatis sebagian | Fallback, canonical, duplikasi canonical; metadata hasil render tetap diuji proyek |
| QG-08 Schema.org | Otomatis sebagian | Registry, scope, pasangan block-schema, dan field sumber block; graph JSON-LD hasil render harus diuji proyek |
| QG-09 Assets/links | Otomatis sebagian | Aset lokal dan internal path yang dapat diturunkan; status HTTP eksternal tidak dicek |
| QG-10 Accessibility | Parsial/proyek | Alt yang tersedia di kontrak konten; keyboard, contrast, heading render, dan ARIA memerlukan audit hasil render |
| QG-11 Production build | Proyek | Jalankan build Astro pada CI proyek; repository standar ini tidak memiliki aplikasi Astro untuk dibuild |
| QG-12 Editorial | Manual | Reviewer manusia/ahli harus mencatat persetujuan |
| QG-13 Information Architecture | Otomatis sebagian | Route manifest, source, sitemap, redirect; relevansi IA tetap direview manusia |

Pada workflow yang diaudit, CI repository ini hanya memasang dependensi dan menjalankan `pytest -q`. Belum ada smoke-test `--help` maupun test integrasi yang membuktikan bahwa seluruh fungsi Milestone 5 dijalankan melalui CLI. Setiap proyek Astro tetap wajib menambahkan pemindaian corpus, build produksi, dan audit accessibility/SEO/schema hasil render ke workflow miliknya. Lulusnya unit test repository standar tidak menyatakan sebuah situs turunan otomatis lulus seluruh QG-01–QG-13.

## Format error

Error baru memuat kode gate dan tindakan yang dapat diturunkan, misalnya:
- `[QG-04 INVALID_SLUG]`
- `[QG-04 ROUTE_COLLISION]`
- `[QG-07 DUPLICATE_CANONICAL]`
- `[QG-09 ASSET_NOT_FOUND]`
- `[QG-09 INTERNAL_LINK_NOT_FOUND]`
- `[QG-13 ROUTE_NOT_IN_MANIFEST]`
- `[QG-13 SITEMAP_ROUTE_MISSING]`

## Verifikasi

GitHub Actions pada workflow yang diaudit menjalankan `pytest -q` pada Python 3.12. Workflow belum menjalankan smoke-test `--help` atau test integrasi CLI. Status sukses workflow hanya membuktikan langkah yang benar-benar tercantum di workflow berhasil; bukan bukti bahwa pemeriksaan route/aset/manifest sudah berjalan melalui CLI. Pemeriksaan build produksi, rendered JSON-LD, accessibility browser, dan review editorial menjadi kewajiban workflow/release proyek Astro.

## Penutupan milestone

Milestone 1–4 menyediakan fondasi validator referensi; Milestone 5 memiliki fungsi pemeriksaan dan unit test, tetapi belum selesai secara end-to-end sampai integrasi CLI dan CI dibuktikan. Registry props yang belum memiliki kontrak universal, pemetaan route spesifik, rendered JSON-LD, build, accessibility browser, dan review editorial harus diselesaikan oleh setiap proyek melalui konfigurasi dan Quality Gates proyeknya.
