# Project Architecture Templates

> Status: Template proyek
> Versi: 0.2

## Tujuan

Starter pack dokumen arsitektur untuk repository situs Astro. Salin direktori ini ke repository proyek (misalnya sebagai docs/architecture/) lalu isi keputusan yang relevan sebelum implementasi.

Template ini menurunkan Website Constitution, Content Contract, Content & Information Architecture, Technical Architecture, dan Quality Gates menjadi artefak proyek. Template bukan aturan universal baru dan tidak menggantikan dokumen standar tersebut.

## Cara menggunakan

1. Salin direktori ini ke repository proyek.
2. Ganti setiap placeholder [ISI ...] dengan keputusan yang didukung fakta, riset, atau persetujuan pemilik proyek.
3. Jangan mengarang fakta bisnis, layanan, relasi, route, schema, atau kemampuan teknis.
4. Bagian yang tidak relevan harus diberi status Tidak berlaku beserta alasannya; jangan dipaksakan.
5. Bedakan keputusan final, asumsi belum terverifikasi, dan pertanyaan terbuka.
6. Jangan menghapus field/kolom template hanya karena nilainya belum diketahui.
7. Setelah keputusan disetujui, jadikan dokumen sebagai acuan implementasi dan quality gates.

## Daftar template

| File | Tujuan | Kapan digunakan |
|---|---|---|
| PROJECT-BRIEF.md | Tujuan bisnis, pengguna, cakupan, batasan, konversi | Selalu |
| INFORMATION-ARCHITECTURE.md | Intent map, sitemap, route, navigasi, breadcrumb, internal linking | Selalu |
| CONTENT-MODEL.md | Collection, sumber kebenaran, field, ID registry, relasi | Selalu |
| LISTING-AND-CONVERSION.md | Listing, related content, pagination, CTA dan konversi | Jika fitur terkait digunakan |
| LOCAL-COVERAGE.md | Area layanan, lokasi fisik, halaman lokal, bukti cakupan | Jika geografis relevan |
| CONTENT-GOVERNANCE.md | Pemilik akurasi, review, lifecycle, sumber fakta | Selalu |
| TECHNICAL-ARCHITECTURE.md | Collection schema, block registry, SEO, JSON-LD, validator, CI | Selalu |
| decisions/ADR-TEMPLATE.md | Catatan keputusan arsitektur | Setiap keputusan penting |

## Status dokumen

Gunakan Draft, Review, Approved, atau Superseded. Dokumen tidak boleh Approved selama keputusan kritis atau asumsi berisiko masih terbuka.

## Kriteria siap implementasi

- [ ] Tujuan situs, pengguna, dan tindakan utama jelas.
- [ ] Intent dipetakan ke halaman atau section yang tepat; tidak satu URL per keyword.
- [ ] Sitemap dan route memiliki tujuan serta status indexability.
- [ ] Collection, sumber kebenaran, dan relasi dikontrak.
- [ ] Navigasi, breadcrumb, dan internal linking ditentukan.
- [ ] Listing dan query otomatis deterministik.
- [ ] Kebijakan lokal tidak membuat klaim kehadiran yang menyesatkan.
- [ ] CTA memiliki target yang tersedia dan tervalidasi.
- [ ] Lifecycle dan pemilik akurasi konten ditetapkan.
- [ ] ID registry, block registry, validator, schema SEO, dan quality gates direncanakan.
- [ ] Keputusan penting memiliki status, pemilik, dan bukti persetujuan.

## Aturan standar yang tetap berlaku

- ID dokumen konten unik global lintas collection; ID block unik lokal dalam dokumen pemilik.
- Foreign key memakai ID numerik dan target collection eksplisit.
- Route unik lintas jenis konten yang menghasilkan halaman.
- Timestamp memakai ISO 8601 UTC presisi detik.
- Schema utama dokumen wajib; schema block opsional dan harus relevan.
- Tidak ada target jumlah kata, halaman, tautan, kategori, atau lokasi yang berlaku universal.
- Template tidak boleh digunakan untuk melemahkan Constitution atau Content Contract.
## Project initialization workflow

Gunakan [PROJECT-INITIALIZATION-WORKFLOW.md](PROJECT-INITIALIZATION-WORKFLOW.md) sebagai urutan operasional dari onboarding repository hingga Implementation Readiness Review. Workflow ini menggunakan phase gates; pembuatan semua dokumen template tidak otomatis berarti proyek siap implementasi.

Paket template saat ini: **0.2** (menambahkan workflow operasional 0.1).
