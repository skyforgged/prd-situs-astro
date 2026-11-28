# Validator Milestone 5 — Route, Asset, Link, dan Quality Gates

> Status: integrasi CLI diperketat dengan mode proyek lengkap; smoke-test dan test integrasi CI tersedia. Uji korpus nyata dan hasil workflow tetap merupakan bukti terpisah.

## Tujuan

Milestone 5 menambahkan pemeriksaan statis lintas dokumen untuk slug, route, canonical, aset, tautan, dan route manifest. Entry point CLI sekarang menjalankan canonical uniqueness dan route checks setiap kali dipanggil; pemeriksaan aset/internal link aktif bila `--site-root` diberikan; pemeriksaan manifest/sitemap/redirect aktif bila `--route-manifest` diberikan (dan mensyaratkan `--site-root`).

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
- Markdown link internal ber-path absolut dan URL internal pada props `url`, `href`, `actionHref`, `primaryHref`, `secondaryHref`, dan `registrationUrl` diperiksa terhadap route yang dihasilkan.
- Media lokal dalam Markdown ikut diperiksa.
- URL eksternal, mailto, tel, data URI, dan fragment tidak diakses melalui jaringan. Pemeriksaan HTTP eksternal sengaja tidak dilakukan pada validator deterministik ini.

### QG-13 — Information Architecture
- Route manifest YAML opsional memetakan path, source, dan status indexability.
- Manifest diperiksa untuk route ganda, route hasil content yang belum dicatat, source yang hilang, serta sitemap XML jika dikonfigurasi.
- Redirect harus memiliki `from` dan `to`, dan tidak boleh berupa self-loop.
- Pemeriksaan ini memvalidasi konsistensi eksplisit; ia tidak menilai relevansi semantik navigasi atau listing.

## Penggunaan CLI

Entry point `main()` menjalankan validasi kontrak, relasi, canonical uniqueness, dan slug/route. Argumen `--site-root` mengaktifkan pemeriksaan aset/internal link; `--route-manifest` mengaktifkan pemeriksaan manifest/sitemap/redirect dan mensyaratkan `--site-root`; `--route-prefixes` memuat override prefix JSON; `--contract-registry` memuat kontrak collection proyek tambahan.

Instal dependensi dan jalankan suite unit serta integrasi CLI:

```bash
python -m pip install -r requirements-dev.txt
pytest -q
python scripts/validate_content.py src/content --site-root . --route-manifest projects/your-site/route-manifest.yml --require-project-gates
```

Perintah di atas mewajibkan pemeriksaan inti, route, canonical, aset/link, serta manifest. Tanpa `--require-project-gates`, CLI berjalan dalam mode parsial untuk diagnosis dan memberi catatan bahwa QG-09/QG-13 dapat belum dijalankan. Opsi `--collection` tetap hanya menerima enam kind kontrak inti. Collection proyek tambahan didaftarkan melalui `--contract-registry` sesuai [Project Collection Contract Extensions](docs/CONTRACT-EXTENSIONS.md).

Pemetaan enam collection inti dapat ditambahkan berulang:

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

### Collection proyek tambahan

Contoh registry untuk `training` dan `schedule` tersedia di `examples/content-contracts/training-schedule.yml`. Jalankan dengan:

```bash
python scripts/validate_content.py src/content \
  --site-root . \
  --contract-registry examples/content-contracts/training-schedule.yml \
  --route-manifest projects/your-site/route-manifest.yml
```

Registry v1 mendukung field wajib/tipe dasar, daftar tipe schema, route prefix, dan relasi ID satu-ke-satu atau satu-ke-banyak. Validasi nested object, block discriminator, dan refinement domain (misalnya urutan tanggal schedule) masih harus ditambahkan oleh proyek; lihat batasan di dokumen ekstensi. Fixture pengujian ekstensi ada di `tests/test_validate_content.py`.

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

Workflow repository ini sekarang menjalankan smoke-test `python scripts/validate_content.py --help` dan `pytest -q`, yang mencakup test integrasi CLI. Status hijau pada commit harus diperiksa dari GitHub Actions; perubahan kode saja bukan bukti test telah lulus. Setiap proyek Astro tetap wajib menambahkan pemindaian corpus, build produksi, dan audit accessibility/SEO/schema hasil render ke workflow miliknya. Lulusnya unit test repository standar tidak menyatakan sebuah situs turunan otomatis lulus seluruh QG-01–QG-13.

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

Workflow sekarang menjalankan smoke-test `--help` dan suite pytest pada Python 3.12. Suite mencakup pemanggilan CLI untuk canonical, internal link, dan route manifest. Status sukses workflow hanya membuktikan langkah yang benar-benar tercantum di workflow berhasil. Pemeriksaan build produksi, rendered JSON-LD, accessibility browser, dan review editorial menjadi kewajiban workflow/release proyek Astro.

## Penutupan milestone

Integrasi Milestone 5 ke CLI dan smoke-test/integration test CI telah diterapkan. Penutupan operasional tetap mensyaratkan workflow hijau pada commit terbaru serta uji corpus proyek nyata. Registry ekstensi v1 adalah mekanisme generik awal, bukan pengganti validasi nested/domain-specific. Registry props yang belum memiliki kontrak universal, pemetaan route spesifik, rendered JSON-LD, build, accessibility browser, dan review editorial harus diselesaikan oleh setiap proyek melalui konfigurasi dan Quality Gates proyeknya.


## Integrasi tahap 3/5 — mode proyek lengkap

CLI menyediakan `--require-project-gates`. Opsi ini mensyaratkan `--site-root` dan `--route-manifest` agar validasi penerimaan tidak dapat diam-diam melewati pemeriksaan aset/internal link (QG-09) dan IA (QG-13). Mode parsial tetap tersedia untuk diagnosis, tetapi outputnya memberi peringatan.

Output sukses menyebut pemeriksaan otomatis yang benar-benar dijalankan dan secara eksplisit menyatakan bahwa QG-10 (accessibility hasil render/browser), QG-11 (Astro production build), serta QG-12 (editorial approval) tidak dinyatakan lulus oleh CLI. CI repository standar menjalankan test integrasi mode lengkap menggunakan fixture; setiap proyek Astro tetap harus menjalankan command lengkap pada corpus dan root proyeknya sendiri.
