# Catatan Review Standar PRD Situs Astro

> Tanggal: 2026-11-26
> Commit yang ditinjau: `70c9469` di `main`
> Catatan ini bukan dokumen standar. Isinya tidak mengubah konstitusi maupun kontrak konten.
> File ini sengaja disimpan di `docs/` sebagai dokumentasi internal, sesuai pengecualian di `constitution/WEBSITE-CONSTITUTION.md:39`.

## Cara membaca checklist

- `- [ ]` berarti belum ada bukti implementasi di repo pada commit yang ditinjau.
- `- [x]` berarti sudah ada bukti di repo, dan buktinya disebut pada bagian **Bukti**.
- Perbarui kotak pada commit yang sama dengan perbaikannya. Jangan dijadikan pekerjaan menyusul.
- Saat menandai selesai, ganti **Bukti saat ini** dengan path dan nomor baris yang baru, lalu cantumkan hasil verifikasinya.
- Karena repo ini belum punya `package.json` atau skrip validasi, verifikasi dilakukan dengan membaca ulang baris yang disebut.

## Status ringkas

| Kelompok | Item | Sudah | Belum |
|---|---|---:|---:|
| Baseline yang sudah ada | S1 s.d. S4 | 4 | 0 |
| P0, kebenaran aturan | P0-1 s.d. P0-3 | 0 | 3 |
| P1, kelengkapan kontrak | P1-1 s.d. P1-5 | 0 | 5 |
| P2, kerapian repo | P2-1 s.d. P2-4 | 0 | 4 |

Tindak lanjut terbuka: **12 item, belum ada yang selesai**.

## Baseline yang sudah terimplementasi

### S1. Tiga keputusan standar sudah konsisten di tiga dokumen

- [x] **Sudah diimplementasikan.**
- **Bukti:** `README.md:10-14`, `constitution/WEBSITE-CONSTITUTION.md:157-165`, `content-contract/CONTENT-CONTRACT.md:28` dan `:340-344`. Keunikan ID global, schema block opsional, kontrak terpisah per jenis konten.
- **Verifikasi:** baca ketiga lokasi dan pastikan bunyinya masih identik setelah ada perubahan lain.

### S2. Tautan dokumen inti di README valid

- [x] **Sudah diimplementasikan.**
- **Bukti:** `README.md:7-8` menunjuk `constitution/WEBSITE-CONSTITUTION.md` dan `content-contract/CONTENT-CONTRACT.md`, keduanya ada.
- **Verifikasi:** buka kedua path dari README, pastikan tidak pindah atau terhapus.

### S3. Dokumen standar punya status dan versi

- [x] **Sudah diimplementasikan.**
- **Bukti:** `constitution/WEBSITE-CONSTITUTION.md:3-5` dan `content-contract/CONTENT-CONTRACT.md:3-5`.
- **Verifikasi:** pastikan versi dinaikkan dan dicatat bila isi standar berubah.

### S4. Lisensi tersedia

- [x] **Sudah diimplementasikan.**
- **Bukti:** `LICENSE:1-3`, MIT atas nama arisciwek.
- **Verifikasi:** README belum menautkan lisensi. Ini bukan error, tetapi bisa ditambahkan di P2-2.

## P0. Kebenaran aturan

### P0-1. Definisi ID numerik global bertabrakan dengan ID block lokal

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `constitution/WEBSITE-CONSTITUTION.md:135` menyatakan "keunikan global seluruh ID numerik". `content-contract/CONTENT-CONTRACT.md:28` menyatakan ID block adalah identitas lokal dalam dokumen pemilik dan tidak ikut ruang ID global.
- **Tindakan:** ubah kalimat di konstitusi menjadi keunikan global untuk seluruh **ID dokumen konten**, bukan seluruh ID numerik. Jika tidak, validator akan menolak dua block dengan `id: 1` di dokumen berbeda.
- **Verifikasi:** baca ulang kedua baris. Tidak boleh ada lagi kata "seluruh ID numerik" yang mencakup ID block.

### P0-2. Format dan aturan timestamp belum ditetapkan, tetapi sudah dipakai dalam contoh

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** enam contoh memakai `2026-11-26T10:00:00+07:00` di `content-contract/CONTENT-CONTRACT.md:71`, `:113`, `:157`, `:204`, `:269`, `:295`. Format tanggal justru ditunda ke dokumen arsitektur di `:378`, dan dokumen itu belum ada. Standar Astro global yang dipakai dalam sesi ini mensyaratkan UTC `YYYY-MM-DDTHH:mm:ssZ`, keunikan timestamp lintas koleksi, serta `updatedDate > publishedDate`.
- **Tindakan:** tetapkan satu format di kontrak atau konstitusi, nyatakan apakah timestamp wajib unik global, dan tambahkan aturan urutan `updatedDate` terhadap `publishedDate`. Setelah itu perbarui keenam contoh agar tidak identik.
- **Verifikasi:** semua contoh memakai format yang ditetapkan, tidak ada dua timestamp sama, dan tidak ada `updatedDate` lebih kecil dari `publishedDate`.

### P0-3. Tabel relasi belum memenuhi kewajiban konstitusinya sendiri

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `constitution/WEBSITE-CONSTITUTION.md:61` mewajibkan setiap relasi mendefinisikan collection target, kardinalitas, kewajiban, dan perilaku ketika target tidak ditemukan. `content-contract/CONTENT-CONTRACT.md:169-181` dan `:227-239` hanya mencantumkan nama field. Field `author` bertipe "object/ID" di `:175` dan `providerId` di `:234` belum jelas bentuknya.
- **Tindakan:** tambahkan kolom target, kardinalitas, wajib/opsional, dan perilaku target hilang pada setiap field relasi. Putuskan apakah `author` memakai ID numerik atau objek, lalu samakan dengan aturan foreign key di `:26` dan `:348-355`.
- **Verifikasi:** setiap field yang berakhir dengan `Id` atau `Ids` memiliki baris tabel lengkap di kontrak dan bisa divalidasi tanpa interpretasi tambahan.

## P1. Kelengkapan kontrak

### P1-1. Objek `seo` diwajibkan tetapi tidak didefinisikan

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `content-contract/CONTENT-CONTRACT.md:45`, `:130`, `:174`, `:233`, `:288` menandai `seo` sebagai wajib. Tidak ada definisi field di dalamnya. `:378` menundanya ke dokumen arsitektur yang belum ada.
- **Tindakan:** buat kontrak objek `seo` minimal, misalnya judul, deskripsi, canonical, dan aturan turunan dari `title` serta `description` bila kosong.
- **Verifikasi:** ada bagian baru yang mendefinisikan `seo` dan semua kontrak merujuk ke bagian itu, bukan mengulang definisi berbeda.

### P1-2. Beberapa field penting hanya dicontohkan, tidak didefinisikan

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `featuredImage` di `content-contract/CONTENT-CONTRACT.md:131` dan `:179`, struktur item menu di `:91`, enum `location` di `:87`, serta batas kedalaman submenu tidak memiliki tipe data dan aturan resmi.
- **Tindakan:** tambahkan tipe dan aturan untuk masing-masing. Untuk item menu, tegaskan bahwa tepat satu dari `pageId` atau `url` harus ada, dan `external: true` hanya boleh dipakai bersama `url`.
- **Verifikasi:** tidak ada lagi field yang bentuknya hanya bisa diketahui dari contoh.

### P1-3. FAQ, testimoni, dan tim diwajibkan sebagai Markdown tetapi belum punya kontrak

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `constitution/WEBSITE-CONSTITUTION.md:26-33` mencantumkan FAQ, testimoni, dan tim sebagai konten wajib Markdown. `content-contract/CONTENT-CONTRACT.md:364-373` menyatakan jenis tersebut belum didefinisikan dan harus punya kontrak sebelum dipakai.
- **Tindakan:** buatkan kontraknya, atau nyatakan dengan tegas bahwa jenis tersebut belum didukung sampai kontrak tersedia, supaya konstitusi tidak menjanjikan sesuatu yang belum bisa divalidasi.
- **Verifikasi:** status keduanya selaras. Tidak ada kewajiban di konstitusi yang tidak punya padanan di kontrak.

### P1-4. Dokumen yang dirujuk kontrak belum ada

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `constitution/WEBSITE-CONSTITUTION.md:151` menaruh spesifikasi arsitektur Astro di urutan ketiga hierarki aturan. `content-contract/CONTENT-CONTRACT.md:12` dan `:378` menunda format tanggal, struktur SEO, strategi registry ID, dan cara menghasilkan JSON-LD ke dokumen itu. `README.md:20` menyebut dokumen akan ditambahkan bertahap, tetapi belum ada.
- **Tindakan:** buat dokumen arsitektur dan quality gates sebelum PRD proyek pertama. Cakup register ID, block registry, kontrak SEO, format tanggal, dan nama perintah validasi.
- **Verifikasi:** semua rujukan silang di konstitusi dan kontrak menunjuk ke file yang ada.

### P1-5. Contoh FAQPage dan HowTo perlu catatan kelayakan rich result

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `content-contract/CONTENT-CONTRACT.md:210-216` dan `:318-325`, serta `constitution/WEBSITE-CONSTITUTION.md:97-103`, memakai `FAQPage` dan `HowTo` sebagai contoh tanpa catatan. Konstitusi `:90` sudah mengingatkan bahwa skema valid belum tentu memenuhi syarat rich result.
- **Tindakan:** tambahkan catatan langsung pada contoh, atau pindahkan ke konteks yang memang memenuhi syarat. Cek ulang kebijakan mesin pencari yang berlaku saat implementasi sebelum menjanjikan target tanpa error atau warning.
- **Verifikasi:** contoh tidak bisa dibaca sebagai jaminan rich result.

## P2. Kerapian repo

### P2-1. Batas konten dan label UI belum ditegaskan

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `constitution/WEBSITE-CONSTITUTION.md:35` melarang salinan konten di konfigurasi lain, sementara `:39` mengecualikan konfigurasi teknis aplikasi. Label tombol dan pesan sistem tidak punya contoh batas yang jelas.
- **Tindakan:** tambahkan satu contoh pasangan, misalnya judul section harus dari frontmatter, sedangkan label "Baca selengkapnya" boleh dari config UI.
- **Verifikasi:** ada contoh eksplisit yang memisahkan keduanya.

### P2-2. Dokumen role analis belum diperbarui mengikuti standar baru

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `ROLE-SYSTEM-ANALYST.md:5` masih berisi placeholder niche, `:13` dan `:32` bertypo `##v`, tidak ada path output, dan tidak ada kewajiban bagi PRD untuk mematuhi konstitusi serta kontrak. README tidak menautkan `LICENSE`.
- **Tindakan:** isi niche, perbaiki heading, tentukan lokasi output PRD, tambahkan klausul kepatuhan standar, dan tautkan lisensi dari README.
- **Verifikasi:** tidak ada placeholder tersisa dan alur dari role ke PRD ke standar bisa diikuti pembaca baru.

### P2-3. `AGENTS.md` masih kosong

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `AGENTS.md` berukuran 0 byte pada commit `70c9469`.
- **Tindakan:** isi dengan konvensi repo, arah pembaca dokumen, dan aturan bahwa perubahan standar wajib memperbarui catatan ini serta versi dokumen.
- **Verifikasi:** file tidak kosong dan isinya tidak bertentangan dengan konstitusi.

### P2-4. Belum ada tempat pencatatan keputusan perubahan standar

- [ ] **Belum diimplementasikan.**
- **Bukti saat ini:** `constitution/WEBSITE-CONSTITUTION.md:155` mewajibkan perubahan aturan global dicatat sebagai keputusan perubahan standar, tetapi repo belum punya `CHANGELOG.md` atau direktori keputusan.
- **Tindakan:** tambahkan `CHANGELOG.md` atau `decisions/`, lalu pakai untuk setiap perubahan pada konstitusi dan kontrak.
- **Verifikasi:** setiap perubahan standar memiliki entri dengan tanggal, alasan, dan dampak ke proyek turunan.

## Langkah berikutnya

1. Selesaikan P0-1 sampai P0-3, lalu tandai kotaknya dan perbarui **Status ringkas**.
2. Lanjut P1-1 sampai P1-5, terutama dokumen arsitektur yang jadi penundaan banyak field di P1-4.
3. Terakhir P2-1 sampai P2-4.
4. Setelah checklist tertutup, gunakan standar ini sebagai dasar penyusunan PRD proyek.
