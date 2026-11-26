# Content Architecture & Information Architecture

> Status: Draft standar arsitektur konten
> Versi: 0.1
> Berlaku untuk: proyek situs Astro yang mengadopsi PRD Situs Astro
> Kedudukan: melengkapi Website Constitution, Content Contract, dan Technical Architecture; tidak menggantikan ketiganya

## 1. Tujuan

Dokumen ini menetapkan cara merancang hubungan antara tujuan situs, kebutuhan pengguna, jenis halaman, entitas konten, navigasi, dan tautan internal. Sasaran utamanya adalah menghasilkan situs yang mudah dipahami pengguna dan mesin pencari, memiliki struktur informasi yang konsisten, serta dapat dikembangkan tanpa membuat halaman yang saling bersaing atau sekadar mengulang isi.

Dokumen ini membedakan:

- **Content architecture**: model entitas, jenis konten, hubungan, kepemilikan informasi, dan siklus hidup konten.
- **Information architecture (IA)**: pengelompokan, hierarki, label, navigasi, route, dan cara pengguna menemukan informasi.
- **Internal linking architecture**: hubungan kontekstual antarrute yang membantu pengguna berpindah ke informasi atau tindakan berikutnya.

Ketiganya harus dirancang bersama, tetapi tidak boleh dicampur menjadi satu daftar tautan atau satu taksonomi yang dipaksakan.

## 2. Prinsip dasar

1. **Berangkat dari kebutuhan pengguna dan tujuan bisnis.** Struktur tidak dibuat hanya untuk menampung kata kunci.
2. **Satu halaman memiliki tujuan utama yang jelas.** Halaman boleh menjawab beberapa pertanyaan terkait, tetapi harus memiliki intent dan tindakan utama yang dapat dikenali.
3. **Satu sumber kebenaran untuk setiap fakta.** Informasi yang dipakai ulang sebaiknya berasal dari entitas atau konfigurasi yang tepat, bukan disalin ke banyak halaman.
4. **Hierarki tidak harus sama dengan hierarki URL.** Kedalaman folder tidak otomatis menunjukkan hubungan semantik.
5. **Relasi eksplisit lebih baik daripada inferensi.** Gunakan ID dan field relasi yang dikontrak; jangan menebak hubungan dari slug, judul, kategori, atau kemiripan kata.
6. **Navigasi bukan pengganti tautan kontekstual.** Menu membantu orientasi global; tautan dalam isi membantu pemahaman dan perjalanan tugas.
7. **Tidak ada target jumlah kata atau jumlah halaman universal.** Cakupan ditentukan oleh kebutuhan informasi, bukan kuota.
8. **Tidak semua proyek membutuhkan semua jenis halaman.** Jenis konten dan fitur hanya ditambahkan bila ada kebutuhan yang dapat dibuktikan.
9. **Halaman harus memiliki nilai mandiri.** Jangan membuat halaman tipis, doorway, atau variasi lokasi/keyword yang hanya mengganti nama tanpa informasi unik.
10. **Struktur harus dapat diaudit.** Setiap halaman, relasi, dan pola listing harus memiliki aturan yang dapat diuji.

## 3. Tahap perancangan IA

Sebelum menentukan collection, menu, atau URL, lakukan tahapan berikut:

### 3.1 Pemetaan tujuan

Catat tujuan utama situs, kelompok pengguna, tugas yang ingin diselesaikan, penawaran/layanan, wilayah operasional bila relevan, dan tindakan konversi yang benar-benar tersedia.

### 3.2 Pemetaan kebutuhan informasi

Kelompokkan pertanyaan pengguna berdasarkan tahap dan maksudnya, misalnya:

- memahami masalah atau istilah;
- mengetahui persyaratan, proses, biaya, risiko, atau pilihan;
- membandingkan solusi;
- memilih penyedia atau layanan;
- memulai konsultasi, transaksi, pendaftaran, atau tindakan lain.

Daftar ini adalah bahan analisis, bukan kewajiban membuat satu halaman untuk setiap pertanyaan.

### 3.3 Pemetaan intent dan halaman

Untuk setiap kebutuhan, tentukan apakah jawaban terbaik berupa halaman layanan, halaman informasional, artikel/panduan, kategori/arsip, halaman lokasi, alat bantu, atau cukup sebagai section pada halaman yang sudah ada.

Gabungkan kebutuhan yang memiliki intent dan jawaban inti sama. Pisahkan menjadi halaman berbeda hanya bila masing-masing membutuhkan jawaban, bukti, proses, atau tindakan yang memang berbeda.

### 3.4 Pemetaan entitas dan relasi

Identifikasi entitas yang perlu menjadi dokumen konten, data konfigurasi, atau sekadar atribut. Tentukan sumber kebenaran dan kardinalitas relasinya sebelum menulis konten.

### 3.5 Validasi struktur

Uji struktur dengan skenario pengguna: apakah pengguna dapat menemukan jawaban, memahami hubungan halaman, membandingkan pilihan, dan mencapai tindakan berikutnya tanpa bergantung pada pencarian internal atau menu yang terlalu dalam?

## 4. Model jenis halaman dan tanggung jawabnya

Jenis berikut adalah pola konseptual. Proyek boleh memakai subset atau mendefinisikan jenis lain melalui Content Contract.

| Jenis halaman | Tujuan utama | Isi yang menjadi tanggung jawabnya | Bukan pengganti |
|---|---|---|---|
| Homepage | Orientasi dan distribusi ke tujuan utama | Identitas, proposisi nilai, jalur utama, bukti yang relevan, CTA utama | Arsip seluruh konten atau salinan semua layanan |
| Halaman layanan/produk | Menjelaskan penawaran dan membantu pengguna mengambil keputusan | Ruang lingkup, sasaran, hasil, proses, prasyarat, batas layanan, bukti, CTA | Artikel edukasi panjang yang tidak membantu keputusan layanan |
| Halaman informasional | Menjawab kebutuhan informasi yang relatif stabil | Profil, kontak, kebijakan, cara kerja organisasi, informasi legal atau operasional | Artikel berita atau halaman layanan |
| Artikel/panduan | Menjawab pertanyaan, menjelaskan konsep, proses, atau kasus | Pembahasan substantif dengan sumber, konteks, batas, dan pembaruan | Halaman layanan yang hanya diberi label artikel |
| Kategori/arsip | Mengelompokkan dan membantu menjelajahi kumpulan konten | Deskripsi klasifikasi yang berguna, daftar konten, navigasi lanjutan | Halaman SEO tipis yang hanya menampilkan daftar tanpa konteks |
| Halaman lokasi | Menjelaskan layanan atau keberadaan nyata pada wilayah tertentu | Bukti cakupan/kehadiran, konteks lokal, perbedaan proses atau kebutuhan wilayah, cara memperoleh layanan | Duplikasi halaman kota dengan penggantian nama lokasi |
| Halaman utilitas | Menyediakan fungsi bantu atau navigasi | Menu, indeks, pencarian, kalkulator, direktori, atau fungsi lain yang benar-benar ada | Konten editorial yang dipaksakan ke menu |

Perbedaan halaman ditentukan oleh maksud dan substansi, bukan sekadar nama collection atau template visual.

## 5. Hirarki informasi dan pengelompokan

### 5.1 Kelompok topik

Gunakan kelompok topik untuk menghubungkan halaman yang membahas satu domain masalah atau penawaran. Kelompok dapat terdiri dari:

- satu halaman utama/topik inti yang menjelaskan ruang lingkup;
- halaman layanan atau solusi yang relevan;
- artikel yang menjelaskan pertanyaan pendukung;
- halaman kategori bila pengelompokan tersebut membantu penemuan konten.

Tidak semua kelompok harus memiliki pola atau jumlah halaman yang sama. Istilah *pillar* dan *cluster* adalah alat perencanaan, bukan syarat teknis atau jaminan peringkat.

### 5.2 Kategori bukan relasi universal

Kategori membantu klasifikasi dan penjelajahan. Kategori tidak otomatis berarti hubungan editorial yang kuat, hubungan layanan, atau urutan prioritas. Jangan memakai kategori sebagai pengganti field relasi khusus seperti `relatedServiceId`.

### 5.3 Hindari kedalaman navigasi yang tidak perlu

Pengguna sebaiknya dapat mencapai tujuan penting melalui navigasi yang ringkas dan tautan kontekstual. Kedalaman menu ditetapkan pada kontrak Menu; struktur konten yang lebih dalam dapat tetap diakses melalui breadcrumb, indeks, atau tautan relevan.

### 5.4 Breadcrumb

Breadcrumb digunakan bila membantu menunjukkan posisi halaman dalam hierarki informasi. Breadcrumb harus mencerminkan struktur yang benar-benar dipahami pengguna, bukan dibuat otomatis dari potongan slug. Halaman yang tidak memiliki parent alami tidak perlu diberi hierarki palsu.

## 6. Strategi URL dan canonical

1. URL harus singkat, stabil, terbaca, dan mencerminkan topik atau jenis halaman bila hal itu membantu.
2. Jangan memasukkan seluruh hierarki navigasi ke URL hanya demi menunjukkan kedalaman.
3. Perubahan slug pada URL yang sudah dipublikasikan harus memiliki keputusan redirect dan pembaruan tautan internal.
4. Satu konten utama sebaiknya memiliki satu URL kanonis.
5. Filter, sort, parameter tracking, pagination, dan variasi tampilan harus memiliki kebijakan indexability/canonical yang eksplisit.
6. Halaman arsip berpaginasi harus menentukan pola route, canonical, tautan halaman sebelumnya/berikutnya, dan penanganan halaman di luar rentang.
7. Jangan membuat URL terpisah untuk variasi keyword yang memiliki tujuan dan jawaban sama.
8. Route harus unik lintas seluruh jenis konten yang menghasilkan halaman.

Detail pola route dan kebijakan canonical final ditetapkan per proyek sebelum implementasi dan diverifikasi oleh validator.

## 7. Arsitektur internal linking

### 7.1 Tujuan tautan internal

Setiap tautan internal harus membantu setidaknya satu hal: memberi definisi/konteks, memperdalam pembahasan, menunjukkan solusi yang relevan, menyediakan bukti, atau mengarahkan ke langkah berikutnya.

Jangan menambahkan tautan hanya untuk memenuhi jumlah tautan atau mengulang anchor text kata kunci.

### 7.2 Pola relasi yang dapat dipertimbangkan

| Sumber | Tujuan yang mungkin | Alasan |
|---|---|---|
| Homepage | Layanan utama, halaman identitas, kategori/indeks penting | Orientasi dan distribusi |
| Halaman layanan | Artikel persiapan, proses, persyaratan, risiko, layanan terkait yang benar-benar relevan | Membantu evaluasi dan kesiapan |
| Artikel/panduan | Layanan terkait, artikel lanjutan, definisi, sumber resmi | Menghubungkan pengetahuan dengan kebutuhan praktis |
| Kategori/arsip | Konten anggota kategori dan kategori terkait bila bermanfaat | Penemuan dan eksplorasi |
| Halaman lokasi | Layanan yang tersedia pada lokasi tersebut, informasi lokal, kontak/tindakan | Menjelaskan cakupan lokal |
| Breadcrumb/menu | Parent atau tujuan navigasi yang stabil | Orientasi dan perpindahan global |

Tabel ini bukan aturan bahwa setiap halaman harus memiliki semua jenis tautan tersebut.

### 7.3 Relevansi dan anchor text

- Anchor harus menjelaskan tujuan tautan secara wajar dan sesuai konteks.
- Variasikan redaksi secara alami; jangan memaksakan exact-match keyword.
- Hindari anchor generik berulang bila label yang lebih deskriptif tersedia.
- Tautkan ke halaman yang paling tepat, bukan selalu ke homepage.
- Jangan membuat tautan ke halaman draft, noindex, redirect yang tidak perlu, atau route yang tidak tersedia.

### 7.4 Relasi editorial dan tautan navigasi

Relasi konten (misalnya artikel ke layanan) adalah data semantik. Tautan yang tampil pada halaman merupakan keputusan presentasi yang dapat menggunakan relasi tersebut. Menu, footer, related content, CTA, dan tautan di badan artikel memiliki fungsi berbeda; jangan menganggap satu mekanisme otomatis menggantikan yang lain.

### 7.5 Batas otomatisasi

Komponen boleh menampilkan daftar terkait berdasarkan relasi eksplisit dan aturan urutan yang ditentukan. Komponen tidak boleh menebak relevansi hanya dari kesamaan kata, atau menampilkan daftar yang sama pada semua halaman tanpa alasan.

Setiap pola daftar otomatis harus menetapkan:
- sumber konten dan filter publikasi;
- relasi atau kriteria keanggotaan;
- aturan pengurutan dan tie-break;
- jumlah maksimum atau kebijakan tanpa batas;
- pengecualian dokumen saat ini;
- perilaku bila hasil kosong;
- label UI dan lokasi render.

## 8. Arsitektur listing, indeks, dan pagination

Listing adalah pola presentasi, bukan jenis konten baru secara otomatis.

Sebelum membuat listing, tetapkan:

1. sumber koleksi dan jenis dokumen yang boleh tampil;
2. filter status publikasi, draft, tanggal, kategori, atau relasi;
3. field pengurutan (misalnya tanggal publikasi atau pembaruan) dan tie-break deterministik;
4. offset/limit atau strategi pagination;
5. apakah daftar menampilkan seluruh hasil atau subset;
6. perilaku empty state;
7. URL pagination, canonical, dan metadata yang diperlukan;
8. apakah listing perlu deskripsi pengantar atau konteks editorial.

Istilah seperti “artikel terbaru”, “artikel 4–6”, “artikel terkait”, dan “semua artikel” harus diterjemahkan menjadi aturan query yang eksplisit. Jangan mengasumsikan semua situs membutuhkan pagination atau pola offset tertentu. Pilihan tersebut dicatat pada keputusan proyek.

## 9. Halaman lokal dan cakupan wilayah

Halaman lokasi hanya layak dibuat bila organisasi benar-benar melayani atau memiliki hubungan operasional yang dapat dijelaskan pada wilayah tersebut dan halaman memberi nilai lokal yang nyata.

Sebelum membuat halaman lokal, verifikasi:
- layanan benar-benar tersedia untuk wilayah itu;
- ada informasi lokal yang akurat dan dapat dipertanggungjawabkan;
- ada perbedaan kebutuhan, proses, regulasi, akses, bukti kegiatan, atau cara pelayanan yang relevan;
- informasi kontak, alamat, jam, dan klaim keberadaan tidak menyesatkan;
- halaman tidak sekadar mengganti nama kota pada template yang sama.

Jika layanan diberikan secara nasional atau jarak jauh, jelaskan cakupan itu secara transparan. Jangan menyiratkan kantor/cabang fisik pada lokasi yang tidak memiliki keberadaan nyata. Bila tidak ada substansi lokal yang unik, gunakan satu halaman cakupan nasional atau jelaskan area layanan pada halaman utama/layanan.

## 10. Konversi dan CTA

CTA harus mengikuti konteks dan tahap keputusan pengguna. CTA dapat mengarah ke layanan, konsultasi, formulir, kontak, pembelian, atau tindakan lain yang benar-benar tersedia.

Setiap CTA terstruktur harus memiliki target yang tervalidasi dan label yang menjelaskan tindakan. Bila CTA mengarah ke entitas konten, gunakan relasi ID sesuai kontrak; jangan menyimpan URL yang dapat dibentuk dari entitas bila standar proyek telah menetapkan relasi ID. CTA eksternal harus menggunakan URL yang divalidasi.

Jangan menampilkan CTA identik secara berlebihan atau menjanjikan hasil yang tidak dapat dipastikan. Penempatan, jumlah, nomor kontak, pesan, dan variasi CTA adalah keputusan proyek yang harus didokumentasikan.

## 11. Siklus hidup dan tata kelola konten

Setiap jenis konten perlu memiliki aturan:
- siapa yang bertanggung jawab atas akurasi;
- sumber fakta dan bukti;
- kondisi publikasi;
- kapan perlu ditinjau ulang;
- bagaimana menangani informasi usang;
- apakah konten diperbarui, digabung, dialihkan, atau dihapus;
- bagaimana menjaga relasi dan tautan setelah perubahan.

Pembaruan tanggal tidak boleh dilakukan hanya untuk memberi kesan baru. Perubahan tanggal harus mencerminkan pembaruan substantif sesuai Content Contract.

Saat dua halaman tumpang tindih, lakukan evaluasi intent, kelengkapan, performa, dan tujuan bisnis sebelum memutuskan mempertahankan keduanya, menggabungkan, mengalihkan, atau menghapus salah satunya.

## 12. Kualitas struktur dan kriteria penerimaan

Rancangan Content Architecture & IA dapat diterima bila:

- setiap jenis halaman memiliki tujuan dan batas tanggung jawab;
- kebutuhan pengguna dipetakan tanpa otomatis menghasilkan satu halaman per keyword;
- entitas, sumber kebenaran, dan relasi memiliki definisi;
- struktur navigasi dan breadcrumb tidak menciptakan hierarki palsu;
- pola URL, canonical, redirect, dan pagination ditentukan;
- tautan internal memiliki alasan dan target yang valid;
- listing memiliki aturan filter dan urutan deterministik;
- halaman lokal memiliki dasar operasional dan nilai unik;
- CTA memiliki target serta tindakan yang jelas;
- tidak ada halaman yang dibuat semata-mata untuk memperbanyak URL;
- keputusan khusus proyek terdokumentasi dan dapat diuji.

Kriteria ini harus diterjemahkan menjadi quality gate yang dapat diotomatisasi bila memungkinkan. Penilaian kualitas substansi, keaslian informasi, dan manfaat bagi pengguna tetap memerlukan review editorial manusia.

## 13. Dokumen keputusan proyek yang wajib disiapkan

Sebelum implementasi situs, proyek setidaknya harus mencatat:

1. peta tujuan pengguna dan intent utama;
2. sitemap/daftar route beserta tujuan setiap halaman;
3. model entitas dan matriks relasi;
4. taksonomi kategori bila digunakan;
5. strategi URL, canonical, redirect, dan pagination;
6. pola navigasi, breadcrumb, dan footer;
7. aturan internal linking dan related content;
8. kebijakan halaman lokal bila relevan;
9. strategi CTA dan jalur konversi;
10. kebijakan lifecycle, review, dan penggabungan konten.

Dokumen proyek dapat disederhanakan bila ruang lingkup situs kecil, tetapi keputusan yang relevan tidak boleh dibiarkan implisit.

## 14. Batas standar dan keputusan proyek

Dokumen ini memberikan prinsip dan kriteria lintas proyek. Dokumen ini **tidak** menetapkan secara universal:
- jumlah kategori, layanan, artikel, atau halaman lokasi;
- jumlah kata, jumlah tautan, atau jumlah artikel terkait;
- nama route atau bahasa URL;
- jumlah item menu atau section homepage;
- urutan tanggal listing;
- kebutuhan pagination;
- pola footer, CTA, atau WhatsApp;
- kewajiban memiliki halaman lokasi, author, FAQ, testimoni, tim, atau jenis konten lain.

Semua hal tersebut dipilih berdasarkan kebutuhan proyek dan dicatat dalam dokumen arsitektur/keputusan proyek. Perubahan yang akan menjadikannya kewajiban universal harus melalui proses perubahan standar, bukan disimpulkan dari satu situs referensi.
