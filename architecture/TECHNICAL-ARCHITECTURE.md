# Technical Architecture Specification — Astro

> Status: Draft standar teknis
> Versi: 0.1
> Berlaku untuk: proyek Astro yang mengadopsi PRD Situs Astro

## 1. Tujuan dan batas

Dokumen ini menjembatani Website Constitution dan Content Contract dengan implementasi Astro. Constitution tetap menjadi aturan tertinggi; spesifikasi proyek boleh memilih detail implementasi selama tidak melanggarnya.

## 2. Struktur proyek minimum

Struktur final dapat menyesuaikan skala situs, tetapi pemisahan tanggung jawab berikut wajib dipertahankan:

```text
src/
  content/                 # Markdown sumber konten
  components/              # Komponen presentasi reusable
  layouts/                 # Kerangka halaman
  pages/                   # Routing Astro
  lib/
    content/               # Query, relasi, dan normalisasi konten
    schema/                # Pembentukan graph JSON-LD
    validation/            # Validator kontrak
  config/                  # Konfigurasi teknis dan UI generik
docs/                      # Dokumentasi internal proyek
scripts/                   # Quality gates dan utilitas
```

Nama collection, penempatan file, dan strategi routing harus didaftarkan dalam dokumen keputusan proyek. Konten substantif tidak boleh dipindahkan ke `config/` hanya demi kemudahan implementasi.

## 3. Content collections dan parsing

1. Setiap jenis konten memiliki schema validasi tersendiri; jangan membuat satu schema universal yang mengizinkan semua field di semua dokumen.
2. Nama collection harus konsisten dengan jenis konten pada Content Contract.
3. Astro Content Collections/Zod atau mekanisme setara digunakan untuk validasi tipe dasar saat build.
4. Aturan lintas collection (ID global, relasi, slug lintas route) memerlukan validator tambahan karena tidak cukup divalidasi oleh schema satu file.
5. Frontmatter YAML harus diparse secara konsisten. Timestamp dinormalisasi/diterima hanya dalam ISO 8601 UTC presisi detik sesuai Constitution.
6. Field yang tidak dikenal harus ditolak kecuali kontrak secara eksplisit mengizinkannya.

## 4. Identitas dan registry ID

- `document.id`: integer positif dan unik global lintas semua collection.
- `block.id`: integer positif, unik hanya dalam satu dokumen.
- Validator mengumpulkan seluruh ID dokumen sebelum pemeriksaan relasi.
- Konflik ID dokumen harus menghasilkan error yang menyebut kedua file dan jenis kontennya.
- ID tidak boleh dihasilkan dari urutan file, slug, atau judul saat build.
- Proyek boleh memelihara `docs/ID-REGISTRY.md` atau registry mesin; registry bukan sumber kebenaran pengganti ID di frontmatter, melainkan alat audit.

## 5. Block registry dan rendering

Setiap komponen block didaftarkan dalam satu registry eksplisit. Setiap entri minimal mendefinisikan:

- Nama `component` yang digunakan di Markdown.
- Schema props dan tipe data, termasuk properti wajib/opsional.
- Komponen Astro renderer.
- Dukungan schema block: tidak didukung atau daftar tipe Schema.org yang diizinkan.
- Aturan aksesibilitas, gambar, tautan, dan perilaku responsif.

Renderer memetakan nama block ke komponen terdaftar. Block tidak dikenal atau props tidak valid harus menggagalkan validasi/build; jangan memakai fallback diam-diam yang menyembunyikan kesalahan konten.

Urutan block mengikuti urutan array Markdown. Komponen tidak boleh mengambil alih urutan melalui hard-coded section halaman.

## 6. Relasi antarkonten

1. Bangun indeks `document.id -> {collection, document, path}` untuk seluruh konten.
2. Validasi setiap foreign key terhadap collection target yang diizinkan.
3. Periksa kardinalitas, optionality, duplikasi ID dalam array, dan target yang hilang.
4. Hindari query berulang yang memindai semua collection untuk setiap relasi; gunakan indeks yang dibangun sekali.
5. Relasi dua arah hanya dibuat bila kontrak mengharuskannya; jika ada, tetapkan sumber kebenaran dan aturan sinkronisasi.
6. Kegagalan relasi harus menunjukkan field, ID target, collection target, dan file sumber.

## 7. SEO dan canonical

Kontrak `seo` berada di Content Contract. Implementasi minimal harus:

- Menurunkan title/description SEO dari field utama bila override tidak diberikan.
- Menghasilkan canonical absolut dari konfigurasi site URL dan route final.
- Menghasilkan title, description, canonical, robots, Open Graph, dan Twitter metadata secara konsisten.
- Mencegah canonical relatif, duplikasi tag, dan metadata kosong.
- Menggunakan satu sumber konfigurasi untuk site URL, nama situs, default image, locale, dan identitas organisasi.
- Memastikan metadata halaman sesuai konten yang terlihat.

Detail properti nested `robots`, `openGraph`, dan `twitter` wajib didefinisikan dalam schema implementasi proyek dan tidak boleh menerima properti bebas.

## 8. Schema.org dan JSON-LD

1. Setiap dokumen menyediakan tipe schema utama sebagaimana Content Contract.
2. Generator menghasilkan satu graph koheren per halaman, bukan satu script JSON-LD terpisah untuk setiap block secara otomatis.
3. Gunakan `@id` stabil berbasis URL kanonis dan fragmen entitas yang konsisten.
4. Hubungkan entitas terkait menggunakan relasi yang benar, misalnya `mainEntity`, `isPartOf`, `provider`, `publisher`, atau `about` sesuai konteks.
5. Schema block hanya diproses bila tipe tersebut terdaftar pada block registry.
6. Jangan membuat node duplikat untuk entitas yang sama; gabungkan properti yang saling melengkapi.
7. Semua properti harus didukung konten nyata. Data tersembunyi atau tidak benar tidak boleh dimarkup.
8. Validasi JSON yang dihasilkan dan jalankan pemeriksaan Schema.org/rich result secara terpisah. Validitas Schema.org tidak menjamin eligibility rich result.

## 9. Routing dan slug

- Setiap dokumen yang dipublikasikan harus memiliki route yang deterministik.
- Slug harus divalidasi terhadap aturan karakter dan keunikan route.
- Slug bukan foreign key.
- Perubahan slug memerlukan kebijakan redirect bila URL lama pernah dipublikasikan.
- Homepage dan menu boleh memiliki identifier internal tetapi route khususnya harus didefinisikan eksplisit.
- Route konflik lintas collection harus menggagalkan validasi.

## 10. Aset dan tautan

- Semua aset lokal yang direferensikan harus tersedia.
- Tautan internal harus menunjuk route yang valid atau anchor yang tersedia.
- Gambar utama dan gambar informatif wajib memiliki alt deskriptif.
- Pipeline gambar boleh menghasilkan format turunan (misalnya WebP/AVIF) tanpa mengubah sumber konten asli.
- URL eksternal harus divalidasi berdasarkan protokol yang diizinkan.

## 11. Konfigurasi UI dan konten

Konfigurasi UI boleh menyimpan label generik seperti “Baca selengkapnya”, “Kembali”, teks loading, dan pesan validasi. Konfigurasi tidak boleh menyimpan judul section, deskripsi layanan, isi FAQ, atau copy editorial spesifik halaman yang seharusnya berada di Markdown.

## 12. Perintah validasi

Setiap proyek wajib menyediakan perintah terdokumentasi yang setara dengan:

```bash
npm run validate:content
npm run validate:relations
npm run validate:links
npm run validate:schema
npm run build
```

Nama script dapat berbeda mengikuti package manager, tetapi seluruh pemeriksaan harus dapat dijalankan secara lokal dan di CI. `build` saja bukan pengganti seluruh validator.

## 13. Keputusan khusus proyek

Setiap penyimpangan atau pilihan yang belum ditetapkan standar harus dicatat dalam `docs/decisions/` dengan konteks, keputusan, alternatif, konsekuensi, dan status. Keputusan proyek tidak boleh melemahkan Constitution.

## 14. Hal yang harus ditetapkan sebelum implementasi

- Nama collection dan lokasi file.
- Schema final seluruh jenis konten yang dipakai.
- Block registry dan kontrak props setiap block.
- Struktur lengkap SEO nested.
- Strategi registry ID dan validator lintas collection.
- Route, canonical, redirect, dan aturan slug.
- Graph JSON-LD serta strategi pengujian.
- Daftar perintah quality gates dan integrasi CI.