# Analisis Pola Situs Referensi — Artikel, Footer, CTA, dan Pagination

> Tanggal analisis: 2026-11-26
> Referensi utama: implementasi Astro rujukan; identitas sumber tidak disimpan di sini
> Referensi pembanding: tiga implementasi Astro lain dengan variasi pola yang sama
> Status: catatan analisis referensi, **bukan** keputusan standar dan bukan kewajiban bagi proyek turunan
> Nomor baris mengikuti isi `main` saat analisis dilakukan

## 1. Tujuan

Dokumen ini merangkum pola antarmuka dan data yang muncul berulang pada situs Astro rujukan, khususnya:

1. Section "Artikel Terbaru" di halaman depan dengan artikel 1–3 terurut DESC.
2. Daftar artikel 4–6 pada halaman layanan.
3. Footer yang berubah mengikuti halaman layanan atau artikel yang berelasi ke layanan.
4. CTA ke halaman layanan dan CTA ke nomor WhatsApp tertentu.
5. Pagination pada halaman indeks artikel.

Tujuannya adalah memisahkan **fakta implementasi** dari **asumsi** dan memberi arah bagi PRD proyek. Sesuai `README.md:35` dan `AGENTS.md`, pola di sini tidak otomatis menjadi aturan universal; kebutuhan spesifik tetap disimpan di bawah `projects/<nama-proyek>/`.

## 2. Ringkasan lintas repo

Keterangan: ✅ ada di kode, ⚠️ hanya sebagian atau hanya direncanakan, ❌ tidak ada, — tidak ada kode Astro yang dapat diverifikasi.

| Pola | konsultan-slf | confinedspace | pusattraining | damkar | jasa-perijinan-slf |
|---|---|---|---|---|---|
| Artikel terbaru 1–3, DESC | ✅ | ✅ | ✅ | ✅ | ⚠️ direncanakan |
| Artikel 4–6 | ✅ | ✅ | ⚠️ | ⚠️ | ❌ |
| Artikel terkait di detail layanan | ✅ 3 item | ✅ 3 item | ❌ | ❌ | ⚠️ direncanakan |
| Footer mengikuti layanan/artikel | ✅ | ✅ | ⚠️ deskripsi saja | ❌ statis | ❌ |
| CTA ke layanan | ✅ | ✅ | ✅ | ✅ | ⚠️ direncanakan |
| CTA WhatsApp | ✅ 1 nomor | ✅ 1 nomor | ✅ 1 nomor | ✅ 2 nomor | ⚠️ "nomor kontak" umum |
| Pagination indeks artikel | ❌ | ❌ | ✅ `/artikel/` | ❌ | ⚠️ bersyarat |

Kesimpulan cepat: pola 1 dan 4 hampir konsisten di semua repo dengan kode. Pola 2, 3, dan 5 **tidak** konsisten, jadi tidak boleh dianggap sebagai kebiasaan bersama tanpa verifikasi proyek.

## 3. Temuan per pola

### 3.1 Artikel terbaru 1–3

Pada `konsultan-slf`, pola ini berasal dari konten, bukan dari komponen:

- `src/content/pages/home.md:59-65` — block `article-list` dengan `mode: latest`, `offset: 0`, `limit: 3`, `heading: "Artikel dan panduan"`.
- `src/components/shared/ArticleListBlock.astro:6-9` — menyaring `!draft` dan `contentType !== 'local-seo'`, mengurutkan **`pubDate` DESC** dengan tie-break `id` DESC, lalu `slice(0, 3)`.
- `src/config/ui.ts:67-68` — eyebrow "Insight & panduan" dan tautan "Semua artikel →". Heading utama tetap berasal dari frontmatter.

Pola yang sama ada di `confinedspace` (`src/content/pages/home.md:14-21`, `ArticleListBlock.astro:18-26`), `pusattraining` (`src/pages/index.astro:250`, `LatestArticlesSection.astro:10-23`), dan `damkar` (`src/pages/index.astro:65`, `LatestArticlesSection.astro:10-22`). Namun **field pengurut tidak seragam**: `konsultan-slf` memakai `pubDate`, sedangkan tiga repo lainnya memakai `updatedDate` sebagai prioritas pertama. Jadi kata "DESC" saja tidak cukup; field penentu urutan harus dinyatakan eksplisit di PRD proyek.

### 3.2 Angka 4–6 ternyata `offset: 3, limit: 3`

Angka "4–6" bukan sekadar jumlah artikel, melainkan **potongan ke-4 sampai ke-6** dari daftar yang sama:

- `konsultan-slf`: `src/content/pages/services.md:24-30` — `mode: listing`, `offset: 3`, `limit: 3`, dirender di `/services/` (`src/pages/services/index.astro:7-18`).
- `confinedspace`: `src/content/pages/services.md:24-30` — pola identik di `/services/`.
- `damkar`: `src/pages/layanan/index.astro:70` — `offset={3} limit={3}`, tetapi datanya global, bukan per layanan.
- `pusattraining`: pola serupa ada di index pelatihan, bukan di detail layanan.

Halaman **detail** layanan adalah hal lain. Di `konsultan-slf`, detail layanan memuat 3 artikel terkait:

- `src/layouts/ServiceLayout.astro:97` — `<RelatedArticles ... type="service" id={service.data.id} />`.
- `src/components/shared/RelatedArticles.astro:14` — `articlesForParent(articles, type, id, 3, excludeId)`.
- `src/utils/related.ts:11-13` — filter `relatedType === 'service' && relatedId === id`, urut `updatedDate ?? pubDate` DESC, `slice(0, 3)`.

`confinedspace` juga memakai 3 artikel terkait di detail layanan (`src/pages/services/[slug].astro:156-157`, `RelatedArticles.astro:17-18`). Sebaliknya, `pusattraining` dan `damkar` tidak memiliki section ini di detail layanan.

**Catatan penting untuk penulisan PRD:** bedakan tiga hal yang sering tertukar — (a) artikel terbaru di homepage, (b) potongan artikel ke-4–6 di index layanan, dan (c) artikel terkait di detail layanan. Ketiganya memakai mekanisme berbeda.

### 3.3 Footer yang berubah sesuai konteks

Di `konsultan-slf`, footer benar-benar bergantung pada halaman:

- `src/components/shared/SiteFooter.astro:6-12` — menerima props `ariaLabel`, `group`, dan `serviceTitle`.
- `src/components/shared/SiteFooter.astro:15-30` — tagline default dari `ui.footer.tagline`; jika `serviceTitle` ada, tagline menjadi "`{site.name} menyediakan jasa {serviceTitle}.`"; jika tidak, layanan aktif dipilih berdasarkan `group`.
- `src/layouts/ServiceLayout.astro:99` — detail layanan mengirim `group` dan `serviceTitle` dari `service.data.title`.
- `src/layouts/ArticleLayout.astro:38-45,202` — detail artikel mengirim `serviceTitle` dari layanan terkait, dengan fallback `group` dari kategori.
- Homepage dan halaman indeks memanggil `<SiteFooter />` tanpa props (`src/pages/index.astro:28`, `src/pages/services/index.astro:18`, `src/pages/articles/index.astro:18`).

Relasi artikel ke layanan dibatasi satu layanan: `src/content.config.ts:311-313` memakai pasangan `relatedType` + `relatedId`, bukan array layanan. `confinedspace` melakukan hal serupa lewat props `serviceTitle`/`serviceTitles`. Di `pusattraining`, yang berubah hanya `footerDescription`, sedangkan tautan footer tetap statis. Di `damkar`, footer identik di semua halaman.

### 3.4 CTA ke layanan dan CTA WhatsApp

**CTA ke layanan.** `konsultan-slf` memakai block `cta` dengan field `serviceHref` dan `serviceLabel` (`src/content.config.ts:41-49`, `src/components/shared/CtaBlock.astro:4,12-14`, contoh `src/content/articles/biaya-waktu-faktor-penentu.md:99-104`). Homepage memakai block `home-cta` dengan `ctaHref: "/services/"` (`home.md:66-72`). `pusattraining` lebih selaras dengan kontrak karena memakai `serviceId` numerik (`src/content.config.ts:281`, `src/pages/artikel/[slug].astro:50-53,230-238`).

**CTA WhatsApp.** Di `konsultan-slf`, nomor tunggal `6285947468548` berada di `src/config/site.ts:5` dan dipakai di `CtaBlock.astro:5-6`, `SiteFooter.astro:49-50`, `ArticleLayout.astro:198`, dan `ContactPanel.astro:54,128`. Nomor tidak berbeda per layanan maupun per tujuan; yang berbeda adalah pesan dan label tombol. `confinedspace` juga memakai satu nomor (`src/config/site.ts:8`). `damkar` memakai dua nomor berdasarkan tujuan — pendaftaran `6282268066126` dan konsultasi `6281298053891` (`src/config/site.ts:60-65`) — bukan berdasarkan layanan.

Jadi "nomor WA yang ditentukan" perlu ditegaskan: ditentukan **di mana** (config pusat), **untuk tujuan apa** (konsultasi/pendaftaran), dan **apakah berbeda per layanan**. Data rujukan menunjukkan nomor bersifat global.

### 3.5 Pagination indeks artikel

Pada `konsultan-slf`, pagination **tidak ada**:

- `src/pages/articles/index.astro:7-18` hanya mengambil dokumen `pages/articles` dan merender block.
- `src/content/pages/articles.md:21-23` memakai `mode: listing` tanpa `limit`. Karena default `limit = 0`, `ArticleListBlock.astro:9` melakukan `slice(offset, undefined)` sehingga menampilkan semua artikel.
- Tidak ditemukan `perPage`, `totalPages`, `pagination`, atau `currentPage` dalam 56 berkas `.astro`/`.ts` di `src/`.

`confinedspace` juga menampilkan semua artikel non-draft (`src/pages/articles/index.astro:9-11,33-35`). Yang benar-benar punya pagination adalah `pusattraining`, tetapi di rute **`/artikel/`**, bukan `/articles/`: `pageSize = 9`, halaman 2+ dibuat sebagai static path (`src/pages/artikel/index.astro:8-14`, `src/pages/artikel/[slug].astro:19-25,143-165`), UI ada inline di `ArticleIndexListing.astro:14-25,67-88`. Komponen generik `Pagination.astro` di repo itu tidak dipakai.

Jadi klaim "paging di halaman `/articles/`" **tidak** terbukti pada repo rujukan utama. Bila pagination memang diperlukan, rute, `perPage`, canonical, dan perilaku halaman kosong harus menjadi keputusan PRD proyek.

## 4. Hubungan dengan standar PRD Situs Astro

**Sudah tercakup oleh standar yang ada:**

- Relasi artikel–layanan: `relatedServiceId` di `content-contract/CONTENT-CONTRACT.md:180` dan matriks relasi `:421`, dengan aturan ID numerik di `:348-364`.
- Pemisahan data dan presentasi: label tidak boleh ditulis di komponen (`constitution/WEBSITE-CONSTITUTION.md:119`); blok dan registry di `architecture/TECHNICAL-ARCHITECTURE.md:52-62`.
- Navigasi footer sebagai dokumen konten: item tautan footer dapat dikelola melalui dokumen Menu dengan `location: footer` di `CONTENT-CONTRACT.md` bagian 4. Ini **hanya mengatur navigasi**, bukan tagline/deskripsi footer, pemilihan layanan kontekstual, atau logika footer dinamis.
- Schema block opsional: `CONTENT-CONTRACT.md:342-346` — daftar artikel tidak perlu memaksakan schema.

**Belum diatur eksplisit di standar global:**

- Kontrak blok `article-list`: `mode`, `offset`, `limit`, field pengurut, dan tie-break.
- Aturan footer dinamis berbasis props/layout.
- Kontrak target layanan untuk CTA tunggal: Content Contract saat ini belum mendefinisikan field `serviceId` pada block CTA. `serviceIds` yang tercantum dalam matriks adalah relasi jamak untuk Homepage/block, bukan otomatis kontrak CTA tunggal. Jika CTA harus menunjuk layanan, proyek perlu mendefinisikan field relasi numerik dan memasukkannya ke matriks relasi.
- Sumber nomor WhatsApp dan aturan pemilihan nomor berdasarkan tujuan.
- Pagination indeks artikel: konvensi rute, `perPage`, canonical, dan empty state.

**Batas kewenangan:** `README.md:35` menyimpan kebutuhan khusus di `projects/<nama-proyek>/`, dan `AGENTS.md` melarang menambahkan fitur wajib ke semua proyek tanpa dasar Constitution. Karena itu dokumen ini berhenti sebagai catatan referensi; perubahan standar hanya boleh dilakukan lewat usulan perubahan standar yang eksplisit.

## 5. Catatan perbaikan untuk implementasi proyek

Bersifat non-normatif, terutama bila `konsultan-slf` dipakai sebagai template:

1. **Samakan nama field tanggal.** Kontrak memakai `publishedDate` (`CONTENT-CONTRACT.md:182-183`), sedangkan repo rujukan memakai `pubDate`. Pilih satu dan turunkan ke validator.
2. **Ganti `serviceHref` dengan relasi yang didefinisikan secara eksplisit.** `serviceHref: "/services/..."` adalah URL di frontmatter (`content.config.ts:41-49`), sementara `CONTENT-CONTRACT.md` mengarahkan relasi dokumen menggunakan ID numerik. Jangan menganggap `serviceId` sudah menjadi field universal: definisikan `serviceId` (0..1) khusus untuk block CTA dalam kontrak proyek dan matriks relasi, atau gunakan field relasi yang sudah ada bila kardinalitas dan sumbernya memang sesuai. Komponen membangun route dari entitas layanan yang tervalidasi.
3. **Pusatkan pembentukan URL WhatsApp.** Nomor sudah ada di `config/site.ts`, tetapi prefix `https://wa.me/` ditulis ulang di lima komponen. Satu helper yang menghasilkan href lebih mudah diuji.
4. **Pisahkan konten navigasi footer dari konten/aturan footer.** `location: footer` mengelola tautan navigasi saja. Tagline, deskripsi kontekstual, teks hak cipta, dan aturan pemilihan layanan adalah kebutuhan terpisah; pindahkan literal UI ke konfigurasi UI atau model konten yang sesuai, dan jangan menganggap dokumen Menu telah mencakupnya. Heading "Artikel terkait layanan" di `ServiceLayout.astro:97` juga merupakan label UI yang perlu mengikuti konfigurasi UI.
5. **Putuskan pagination di PRD proyek.** Jika tidak diinginkan, nyatakan bahwa indeks menampilkan seluruh artikel; jika diinginkan, tentukan rute dan `perPage` secara eksplisit agar tidak muncul dua konvensi (`/articles/` vs `/artikel/`).

## 6. Batas verifikasi

Analisis dilakukan dengan membaca kode melalui GitHub API dan `raw.githubusercontent.com`, tanpa menjalankan build, validator, atau test. Repo `jasa-perijinan-slf` hanya berisi dokumen perencanaan, sehingga temuan pada kolom tersebut bersifat rencana, bukan implementasi. Tidak ada klaim bahwa seluruh pola berlaku pada produksi situs; galat pada nomor baris dapat terjadi bila cabang `main` diperbarui setelah tanggal analisis.
