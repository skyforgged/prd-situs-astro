# Catatan Review Standar PRD Situs Astro

> Tanggal tindak lanjut: 2026-11-26
> Commit awal yang ditinjau: `70c9469`
> Status: seluruh 12 temuan telah ditindaklanjuti, ditambah 3 koreksi lanjutan pada 2026-11-26; lihat catatan verifikasi di bawah.

## Ringkasan

| Kelompok | Item | Status |
|---|---:|---|
| Baseline S1–S4 | 4 | Dipertahankan |
| P0 — Kebenaran aturan | 3 | Selesai |
| P1 — Kelengkapan kontrak | 5 | Selesai dengan klarifikasi |
| P2 — Kerapian repository | 4 | Selesai |

## Keputusan penting selama tindak lanjut

1. Keunikan global hanya berlaku untuk **ID dokumen konten**. ID block tetap unik lokal dalam dokumen pemilik.
2. Timestamp memakai ISO 8601 UTC presisi detik (`YYYY-MM-DDTHH:mm:ssZ`). Timestamp tidak diwajibkan unik; identitas unik adalah ID dokumen. `updatedDate` harus sama dengan atau lebih baru dari `publishedDate`.
3. FAQ, testimoni, tim, dan jenis konten lain bukan fitur wajib setiap situs. Jika suatu proyek menggunakannya sebagai entitas konten, kontraknya harus didefinisikan sebelum digunakan.
4. Relasi yang menunjuk Author/Person atau Organization/Provider hanya dapat digunakan setelah kontrak target tersedia.
5. `seo` memiliki kontrak bersama dengan fallback ke `title` dan `description` dokumen. Detail nested yang bergantung pada implementasi harus ditetapkan dalam arsitektur proyek.

## P0 — Kebenaran aturan

### P0-1. ID dokumen global dan ID block lokal
- [x] Selesai. Constitution 1.2 membatasi keunikan global pada ID dokumen konten dan memisahkan validasi ID block.
- Bukti: `constitution/WEBSITE-CONSTITUTION.md:48`, `:147`, `:175`; `content-contract/CONTENT-CONTRACT.md:28`; `quality/QUALITY-GATES.md:55`.
- Verifikasi ulang 2026-11-26: bunyi lama "seluruh ID numerik" pada quality gate sudah diganti dan tidak ditemukan lagi oleh pencarian teks.

### P0-2. Format dan aturan timestamp
- [x] Selesai. Format UTC presisi detik ditetapkan; timestamp tidak harus unik; `updatedDate >= publishedDate`.
- Bukti: Constitution bagian Metadata dan media; Content Contract bagian Aturan waktu dan Schema.org.

### P0-3. Definisi relasi
- [x] Selesai. Matriks relasi menyebut sumber, target, kardinalitas, status, dan perilaku jika target tidak ditemukan. `author` diperjelas menjadi `authorId` numerik.
- Bukti: `content-contract/CONTENT-CONTRACT.md`, bagian Matriks relasi dan kontrak Article/Service.

## P1 — Kelengkapan kontrak

### P1-1. Kontrak objek SEO
- [x] Selesai. Objek `seo` memiliki field, tipe, fallback, dan aturan canonical.
- Bukti: `content-contract/CONTENT-CONTRACT.md`, bagian Kontrak objek bersama.

### P1-2. Definisi field yang sebelumnya hanya dicontohkan
- [x] Selesai. Struktur `featuredImage` didefinisikan. Aturan menu menetapkan tepat satu dari `pageId` atau `url`, serta batas penggunaan `external`.
- Bukti: `content-contract/CONTENT-CONTRACT.md:79`, `:89`, `:93`, `:398-409`.
- Verifikasi ulang 2026-11-26: kalimat lama tentang batas kedalaman yang ditentukan proyek sudah diganti; enum `location` kini memuat `utility` di tabel dan di narasi.

### P1-3. FAQ, testimoni, dan tim
- [x] Selesai dengan klarifikasi. Constitution menyatakan jenis tersebut hanya wajib berbasis Markdown apabila digunakan; bukan fitur wajib semua situs. Kontrak jenis baru wajib dibuat sebelum digunakan.
- Bukti: `constitution/WEBSITE-CONSTITUTION.md`, bagian Sumber konten; `content-contract/CONTENT-CONTRACT.md`, bagian Kontrak yang belum didefinisikan.

### P1-4. Dokumen arsitektur yang dirujuk
- [x] Selesai. Technical Architecture dan Quality Gates telah dibuat dan ditautkan dari README.
- Bukti: `architecture/TECHNICAL-ARCHITECTURE.md`, `quality/QUALITY-GATES.md`, `README.md`.

### P1-5. FAQPage dan HowTo
- [x] Selesai. Contoh dinyatakan sebagai ilustrasi semantik, bukan jaminan kelayakan rich result; kebijakan mesin pencari harus diperiksa saat implementasi.
- Bukti: Constitution bagian Schema.org; Content Contract bagian Aturan waktu dan Schema.org.

## P2 — Kerapian repository

### P2-1. Konten dan label UI
- [x] Selesai. Batas konten substantif dan label UI generik dijelaskan dengan contoh.
- Bukti: `constitution/WEBSITE-CONSTITUTION.md`, bagian Sumber konten dan batas pengecualian; Architecture bagian Konfigurasi UI dan konten.

### P2-2. Role System Analyst
- [x] Selesai. Placeholder niche dan typo heading dihilangkan; standar wajib, lokasi output, dan prinsip analisis ditambahkan. README menautkan LICENSE.
- Bukti: `ROLE-SYSTEM-ANALYST.md`, `README.md`.

### P2-3. AGENTS.md
- [x] Selesai. Instruksi kerja agen, dokumen yang wajib dibaca, dan aturan perubahan standar ditambahkan.
- Bukti: `AGENTS.md`.

### P2-4. Pencatatan perubahan standar
- [x] Selesai. `CHANGELOG.md` dibuat dengan tanggal, perubahan, alasan, dampak, dan catatan kompatibilitas.
- Bukti: `CHANGELOG.md`.

## Tambahan: kerangka frontmatter untuk agen AI

- [x] Ditambahkan `content-contract/FRONTMATTER-TEMPLATES.md` berisi kerangka field kosong untuk Homepage, Menu, Page, Article, Service, dan Category.
- [x] Content Contract 1.3 dan README menautkan template; `AGENTS.md` mewajibkan agen membacanya sebelum membuat atau merevisi dokumen konten.
- Bukti: `content-contract/FRONTMATTER-TEMPLATES.md`, `content-contract/CONTENT-CONTRACT.md`, `AGENTS.md`, dan `README.md`.

## Koreksi lanjutan 2026-11-26

- [x] Quality gate pada konstitusi diselaraskan dengan keputusan ID dokumen global dan ID block lokal.
  - Bukti: `constitution/WEBSITE-CONSTITUTION.md:4`, `:147`; `CHANGELOG.md` bagian Fixed.
  - Verifikasi: pencarian teks "seluruh ID numerik" tidak mengembalikan kecocokan; `quality/QUALITY-GATES.md:55` masih menyatakan block ID 1 di dua dokumen berbeda lulus.
- [x] Aturan menu disatukan menjadi satu bunyi, termasuk enum `location` dan kedalaman maksimal.
  - Bukti: `content-contract/CONTENT-CONTRACT.md:79`, `:89`, `:93`.
  - Verifikasi: pencarian teks "batas kedalaman yang ditentukan proyek" tidak mengembalikan kecocokan; `utility` tercantum di narasi dan tabel.
- [x] Penomoran subjudul objek bersama diperbaiki dan rujukan versi template diselaraskan.
  - Bukti: `content-contract/CONTENT-CONTRACT.md:383`, `:398`; `content-contract/FRONTMATTER-TEMPLATES.md:4-5`.
  - Verifikasi: subjudul kini bernomor 13.1 dan 13.2 di bawah Bab 13; template menyatakan mengikuti Content Contract 1.3.

## Batas verifikasi

Perubahan diverifikasi dengan membaca ulang isi file dan pencarian teks terhadap frasa lama. Repository ini belum memiliki `package.json`, implementasi validator, atau test runner; karena itu belum ada klaim bahwa quality gates telah dijalankan sebagai automated tests. Quality Gates saat ini mendefinisikan kriteria penerimaan yang harus diimplementasikan dan dijalankan pada setiap proyek Astro.

## Tindak lanjut standar editorial 2026-11-26

- [x] Ditambahkan `quality/CONTENT-QUALITY-STANDARD.md` sebagai acuan kualitas editorial lintas jenis halaman.
- [x] Ditegaskan bahwa Google tidak menetapkan preferred word count; panjang konten mengikuti tujuan halaman, kompleksitas, dan kebutuhan pembaca.
- [x] Ditambahkan QG-12 untuk review editorial manusia/ahli, tanpa menjadikan jumlah kata sebagai syarat otomatis.
- [x] `README.md`, `AGENTS.md`, dan `ROLE-SYSTEM-ANALYST.md` ditautkan ke standar editorial.
- Bukti: `quality/CONTENT-QUALITY-STANDARD.md`, `quality/QUALITY-GATES.md`, `README.md`, `AGENTS.md`, dan `ROLE-SYSTEM-ANALYST.md`.
- Batas verifikasi: dokumen standar dan tautan telah diperbarui; belum ada validator atau test runner repository untuk menjalankan gate otomatis. QG-12 memang merupakan review editorial yang harus dicatat oleh reviewer.

## Langkah lanjutan

1. Implementasikan validator sesuai `architecture/TECHNICAL-ARCHITECTURE.md` dan `quality/QUALITY-GATES.md` pada proyek Astro pertama yang mengadopsi standar.
2. Saat implementasi, validasi ulang detail schema nested SEO dan semua jenis relasi yang benar-benar dipakai proyek.
3. Terapkan QG-12 sebagai review editorial pada konten nyata dan evaluasi apakah checklist perlu penyesuaian menurut jenis situs.
4. Tambahkan ADR jika keputusan arsitektur baru berdampak lintas proyek.