# Website Constitution — PRD Astro

> Status: Standar dasar proyek  
> Versi: 1.0  
> Bahasa: Indonesia

## 1. Tujuan dan cakupan

Dokumen ini menetapkan aturan lintas-proyek yang wajib dipatuhi setiap situs berbasis Astro yang menggunakan standar PRD ini. Aturan di sini bersifat konstitusional: PRD proyek boleh menambahkan aturan yang lebih spesifik, tetapi tidak boleh meniadakan atau melemahkan aturan ini tanpa keputusan perubahan standar yang eksplisit.

Constitution mengatur prinsip konten, identitas data, relasi, Schema.org, pemisahan data dan presentasi, serta validasi. Detail implementasi Astro dan kebutuhan bisnis per situs dijabarkan dalam dokumen arsitektur dan PRD proyek masing-masing.

## 2. Prinsip arsitektur utama

1. **Konten adalah data.** Konten situs disimpan sebagai data terstruktur, bukan ditanam langsung di komponen atau layout.
2. **Markdown adalah sumber kebenaran konten.** Frontmatter menjadi kontrak data yang dibaca oleh aplikasi.
3. **Kontrak mengikuti jenis konten.** Homepage, menu, halaman, artikel, layanan, dan jenis konten lain memiliki kontrak frontmatter masing-masing. Kesamaan aturan dasar tidak berarti semua jenis konten harus dipaksa memakai satu skema.
4. **Komponen menyajikan data.** Komponen Astro bertugas merender data dan tidak menjadi tempat penyimpanan konten spesifik halaman.
5. **Layout mengatur kerangka.** Layout mengatur struktur tampilan umum; konten dan urutan bagian halaman berasal dari data.
6. **Validasi adalah bagian dari sistem.** Konten yang tidak memenuhi kontrak harus terdeteksi melalui validasi otomatis sebelum dianggap siap dirilis.

## 3. Sumber konten dan batas pengecualian

### 3.1 Konten situs wajib berbasis Markdown

Seluruh konten substantif yang ditampilkan kepada pengunjung wajib memiliki sumber Markdown dengan frontmatter terstruktur, termasuk namun tidak terbatas pada:

- Homepage.
- Menu utama, menu sekunder, navigasi, dan konfigurasi tautan footer yang tampil sebagai konten.
- Halaman statis dan landing page.
- Artikel, berita, panduan, dan kategori.
- Layanan, produk, portofolio, studi kasus, dan profil.
- FAQ, testimoni, tim, lokasi, serta konten terstruktur lain yang dikelola sebagai entitas konten.

Konten tidak boleh disalin secara terpisah ke komponen Astro, file JSON, atau konfigurasi lain sehingga tercipta dua sumber kebenaran.

### 3.2 Pengecualian

Aturan Markdown tidak mewajibkan semua berkas proyek menjadi Markdown. Berkas kode, konfigurasi teknis aplikasi, konfigurasi build, data operasional non-konten, aset media, dan dokumentasi internal pengembangan dapat menggunakan format yang sesuai. Direktori dokumentasi seperti `docs/` boleh berisi Markdown biasa tanpa kontrak frontmatter konten situs.

Pengecualian tidak boleh digunakan untuk menyimpan konten halaman yang seharusnya dikelola melalui sistem konten.

## 4. Identitas konten

1. Setiap dokumen konten wajib memiliki `id` berupa bilangan bulat positif.
2. **Keunikan ID berlaku secara global dalam satu situs**, lintas seluruh collection dan jenis konten. ID artikel tidak boleh sama dengan ID layanan, halaman, menu, homepage, atau entitas konten lain.
3. ID adalah identitas internal yang stabil. Perubahan judul, slug, URL, atau lokasi file tidak boleh otomatis mengubah ID.
4. Setiap dokumen yang memiliki URL wajib memiliki `slug` berupa string. Slug bukan pengganti ID dan tidak boleh dipakai sebagai foreign key.
5. Slug harus unik pada ruang URL yang relevan. Aturan keunikan slug mengikuti routing situs; aturan ini terpisah dari keunikan ID.
6. ID tidak boleh dibuat ulang hanya karena konten dipindahkan, diperbarui, atau diubah statusnya.
7. Penghapusan konten tidak membuat ID lama bebas dipakai kembali, kecuali ada prosedur migrasi dan keputusan eksplisit.

Satu situs wajib memiliki mekanisme pencatatan atau validasi ID global agar benturan antar-collection dapat dicegah.

## 5. Relasi antarkonten

1. Relasi antardokumen konten wajib menggunakan ID numerik milik dokumen tujuan (foreign key).
2. Relasi tunggal menggunakan satu nilai numerik, misalnya `serviceId: 12`.
3. Relasi jamak menggunakan daftar ID numerik, misalnya `relatedArticleIds: [102, 103]`.
4. Relasi tidak boleh menggunakan slug, judul, URL, nama file, atau label tampilan sebagai pengenal utama.
5. Setiap relasi wajib mendefinisikan collection/jenis konten tujuan, kardinalitas, kewajiban atau opsionalitas, dan perilaku ketika target tidak ditemukan.
6. Referensi yang tidak ditemukan, bertipe salah, atau menunjuk ke ID duplikat harus menyebabkan validasi gagal.
7. Relasi dua arah tidak otomatis diwajibkan. Jika dibutuhkan, aturan sinkronisasi kedua arah harus ditetapkan secara eksplisit.

## 6. Schema.org

### 6.1 Schema utama dokumen

Setiap dokumen konten Markdown wajib memiliki field `schema` yang menyatakan tipe Schema.org utama untuk entitas yang direpresentasikan dokumen tersebut.

Contoh:

```yaml
schema:
  type: Article
```

Nilai `type` harus merupakan tipe Schema.org yang valid dan sesuai dengan makna konten. Contoh tipe yang dapat digunakan sesuai kebutuhan: `WebPage`, `AboutPage`, `ContactPage`, `Article`, `BlogPosting`, `Service`, `Product`, `CollectionPage`, atau tipe lain yang relevan.

Field ini mendeskripsikan entitas utama dokumen, bukan daftar semua schema yang mungkin muncul di halaman.

### 6.2 Schema pada block

1. Setiap block **boleh** memiliki field `schema`; field ini bersifat opsional.
2. Schema block hanya ditambahkan jika block benar-benar menyajikan konten yang dapat dimodelkan secara tepat dengan tipe Schema.org.
3. Block tanpa field `schema` tetap valid dan tetap harus dirender secara normal.
4. Keberadaan field schema pada block tidak otomatis berarti setiap block menghasilkan node JSON-LD terpisah.
5. Generator schema bertanggung jawab menggabungkan data menjadi graph JSON-LD yang konsisten, menghindari duplikasi entitas, dan menghubungkan node yang relevan.
6. Structured data harus sesuai dengan konten yang benar-benar terlihat oleh pengguna. Dilarang menambahkan properti atau informasi yang tidak didukung konten.
7. Penggunaan tipe seperti `FAQPage`, `HowTo`, `Product`, dan tipe lain harus mengikuti pedoman Schema.org serta kebijakan kelayakan rich result mesin pencari yang berlaku. Valid secara Schema.org tidak otomatis berarti memenuhi syarat rich result Google.

Contoh block dengan schema:

```yaml
- id: 2
  component: how-to
  schema:
    type: HowTo
  title: Tahapan proses
  steps:
    - name: Persiapan
      text: Siapkan data yang dibutuhkan.
```

Contoh block tanpa schema:

```yaml
- id: 3
  component: callout
  title: Catatan
  content: Pastikan data telah diperiksa.
```

## 7. Pemisahan konten, komponen, dan layout

1. Konten spesifik halaman harus berasal dari frontmatter dokumen konten.
2. Komponen Astro tidak boleh menyimpan salinan teks, daftar, FAQ, CTA, atau data halaman tertentu yang seharusnya dikelola melalui Markdown.
3. Komponen menerima data melalui props dan bertanggung jawab atas presentasi serta perilaku UI yang relevan.
4. Layout tidak boleh menjadi tempat untuk menulis konten unik suatu halaman.
5. Susunan block ditentukan oleh data konten. Sistem harus mendukung penambahan, penghapusan, dan pengurutan ulang block tanpa mengubah layout halaman.
6. Block yang tidak dikenal atau memiliki properti tidak valid harus terdeteksi saat validasi, bukan diam-diam diabaikan.

## 8. Metadata dan media

- Metadata yang berkaitan dengan konten harus dikelola dalam frontmatter sesuai kontrak jenis konten.
- Setiap gambar konten yang bermakna wajib memiliki teks alternatif (`alt`) deskriptif yang relevan dengan topik dan konteks halaman.
- Metadata SEO, Open Graph, dan data terstruktur harus bersumber dari data konten atau konfigurasi situs yang ditetapkan; jangan membuat sumber data duplikat.
- Informasi yang ditampilkan dan structured data tidak boleh saling bertentangan.

## 9. Validasi dan quality gates

Situs belum dianggap memenuhi standar hanya karena `astro build` berhasil. Proyek wajib menyediakan validasi otomatis sekurang-kurangnya untuk:

1. Keberadaan dan tipe field wajib setiap kontrak konten.
2. Keunikan global seluruh ID numerik.
3. Format dan keunikan slug sesuai aturan routing.
4. Validitas foreign key, target collection, dan kardinalitas relasi.
5. Nama komponen block dan properti yang diizinkan.
6. Struktur serta tipe Schema.org pada dokumen dan block yang memilikinya.
7. Konsistensi sumber metadata, tautan internal, dan aset yang direferensikan.
8. Build produksi.

Validasi harus dapat dijalankan melalui perintah yang terdokumentasi dan menjadi bagian dari pemeriksaan sebelum rilis. Kegagalan validasi wajib menghasilkan pesan yang menunjukkan berkas, field, dan masalah yang ditemukan.

## 10. Hierarki aturan dan perubahan standar

Urutan acuan:

1. Constitution ini.
2. Content Contract standar.
3. Spesifikasi arsitektur teknis Astro.
4. PRD dan keputusan khusus proyek.
5. Implementasi kode.

Dokumen pada tingkat lebih rendah boleh memperinci aturan di atasnya, tetapi tidak boleh bertentangan. Perubahan terhadap aturan global—terutama identitas, relasi, sumber konten, dan schema—harus dicatat sebagai keputusan perubahan standar agar seluruh proyek turunan dapat mengadopsinya secara konsisten.

## 11. Keputusan standar yang telah ditetapkan

Keputusan berikut bersifat final untuk versi standar ini:

| Area | Keputusan |
|---|---|
| Keunikan ID | Global, lintas seluruh jenis/collection konten |
| Schema block | Opsional, digunakan jika relevan |
| Kontrak Markdown | Terpisah berdasarkan jenis konten |

---
Dokumen ini menjadi acuan wajib bagi seluruh PRD situs Astro yang menggunakan standar `prd-situs-astro`.
