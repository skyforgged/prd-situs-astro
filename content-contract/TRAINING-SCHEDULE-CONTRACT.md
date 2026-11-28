# Kontrak Collection Training dan Schedule

> Status: standar ekstensi domain siap diadopsi proyek
> Versi: 1.2
> Basis: Project Collection Contract Extensions v1

## 1. Tujuan dan posisi dalam arsitektur

Dokumen ini menetapkan model data referensi untuk situs yang menerbitkan program pelatihan/kursus dan jadwal pelaksanaannya. `training` dan `schedule` adalah collection domain, bukan pengganti enam kind inti (`homepage`, `menu`, `page`, `article`, `service`, `category`).

- **Training** adalah definisi program/produk pembelajaran yang relatif stabil: kompetensi, tujuan, materi, sasaran peserta, metode, durasi, prasyarat, dan informasi program.
- **Schedule** adalah satu pelaksanaan/batch dari sebuah training: tanggal, waktu, zona waktu, metode delivery, lokasi, kapasitas/registrasi, status, dan informasi penyelenggaraan.
- Satu training dapat memiliki nol atau banyak schedule.
- Satu schedule wajib terkait tepat ke satu training.
- Schedule tidak boleh disimpan sebagai array jadwal tertanam di training sebagai sumber kebenaran. Listing jadwal dapat dirender melalui relasi.

Collection ini hanya diaktifkan bila situs memang mengelola program dan batch pelatihan. Proyek yang hanya menerbitkan artikel tentang pelatihan tidak perlu mengadopsinya.

## 2. Naming, direktori, dan route

| Collection kind | Direktori default | Route prefix | Contoh route |
|---|---|---|---|
| `training` | `trainings/` | `/training/` | `/training/nama-program/` |
| `schedule` | `schedules/` | `/schedule/` | `/schedule/nama-program-batch-01/` |

Nama direktori dan prefix adalah default referensi; proyek boleh mengganti keduanya melalui registry ekstensi dan route manifest. Prefix harus absolut, ternormalisasi, dan diakhiri slash. Slug harus unik dalam collection dan hasil route tidak boleh bertabrakan dengan route collection lain.

Jangan membuat route schedule berdasarkan tanggal saja: perubahan tanggal tidak boleh mengubah identitas URL. Gunakan slug stabil yang mewakili training dan batch.

## 3. Identitas dan relasi

Setiap dokumen tetap mengikuti invariant ekstensi:
- `id`: integer positif, unik global lintas seluruh collection situs.
- `ulid`: ULID 26 karakter bila proyek membutuhkan identifier publik/terdistribusi; bukan pengganti `id`.
- `slug`: segmen route unik pada collection terkait.
- `trainingSlug`: natural key relasi yang stabil dan unik pada collection training.
- `scheduleId`: identifier bisnis jadwal; berbeda dari `id` internal.
- `batchNo`: label batch yang dapat dibaca manusia; tidak wajib menjadi kunci relasi.

Relasi normatif:

| Sumber | Field | Target | Kardinalitas | Ketentuan |
|---|---|---|---|---|
| schedule | `trainingSlug` | training.`trainingSlug` | one | Wajib; tepat satu target |
| training | — | schedule | zero-to-many | Dibentuk melalui query balik schedule.trainingSlug |

Untuk kontrak referensi ini, `schedule.trainingSlug` ditetapkan sebagai satu-satunya sumber kebenaran relasi schedule → training. Nilainya harus unik, stabil, tidak kosong, dan tidak berubah ketika judul atau slug route berubah. Registry harus mendeklarasikan `target: training`, `targetField: trainingSlug`, dan `cardinality: one`.

Proyek yang memilih FK numerik boleh mengganti model tersebut melalui keputusan arsitektur/ADR: gunakan `trainingId: positive_int` dengan target `training.id`, lalu hapus `trainingSlug` dari relasi dan registry. Jangan mengaktifkan kedua field sebagai relasi paralel.

Relasi balik training → schedule tidak perlu disimpan sebagai daftar ID karena dapat dihitung dari collection schedule. Jika cache relasi disimpan, perlakukan sebagai data turunan dan validasi konsistensinya.

## 4. Kontrak Training

### 4.1 Field

| Field | Wajib | Tipe ekstensi v1 | Arti dan aturan |
|---|---:|---|---|
| `id` | Ya | positive_int | ID global dokumen |
| `ulid` | Sesuai kebutuhan proyek | ulid | ID publik/terdistribusi |
| `type` | Ya | string / enum | Nilai tetap `training` |
| `trainingSlug` | Ya | string | Natural key unik untuk relasi schedule |
| `slug` | Ya | string | Route slug |
| `title` | Ya | string | Nama resmi program |
| `description` | Ya | string | Ringkasan program; jangan disamakan dengan SEO description jika kontrak SEO proyek memisahkannya |
| `categoryIds` | Opsional | positive_int_array | FK ke kategori yang memang ditetapkan proyek |
| `pubDate` | Ya | offset_datetime | Tanggal publikasi dengan offset eksplisit |
| `updatedDate` | Ya | offset_datetime | Waktu pembaruan dengan offset eksplisit |
| `draft` | Opsional | boolean | Status draf; kebijakan publikasi ditentukan proyek |
| `image` | Opsional | string | Referensi aset utama; gunakan object image jika kontrak proyek memerlukannya |
| `hero` | Opsional | object | Data hero yang harus divalidasi oleh schema proyek |
| `blocks` | Opsional | array | Konten terstruktur; wajib mengikuti block registry proyek |

Field domain tambahan yang disarankan (harus ditambahkan ke registry dan Zod schema proyek sebelum digunakan): `trainingCode`, `objectives`, `outcomes`, `targetAudience`, `prerequisites`, `topics`, `duration`, `deliveryModes`, `certificate`, `instructorIds`, dan `faq`. Jangan menambahkan field ini ke dokumen produksi sebelum kontrak proyek mendefinisikan tipe dan validasinya.

### 4.2 Semantik

Training menjawab “program apa yang ditawarkan?” bukan “kapan batch tertentu berlangsung?”. Informasi yang dapat berubah per pelaksanaan—tanggal, jam, venue, status batch, link meeting, kuota—milik schedule.

Jika biaya, durasi, metode, atau instruktur berbeda per batch, nilai final per batch harus berada pada schedule atau relasi penawaran batch; nilai pada training hanya menjadi informasi default/indikatif dan harus diberi label jelas.

### 4.3 Schema.org

Tipe yang direkomendasikan adalah `Course` untuk training apabila isi benar-benar merepresentasikan kursus/program pembelajaran. Pemetaan minimum:

| Schema.org | Sumber |
|---|---|
| `Course.name` | `title` |
| `Course.description` | `description` |

Field tambahan seperti `provider`, `hasCourseInstance`, `courseMode`, `educationalLevel`, `teaches`, `timeRequired`, dan `offers` hanya boleh dirender jika sumber datanya tersedia dan mapping telah didaftarkan. Relasi ke schedule dapat dipetakan ke `hasCourseInstance` bila renderer dan Schema Registry proyek mendukungnya; jangan mengarang instance.

## 5. Kontrak Schedule

### 5.1 Field

| Field | Wajib | Tipe ekstensi v1 | Arti dan aturan |
|---|---:|---|---|
| `id` | Ya | positive_int | ID global dokumen |
| `ulid` | Sesuai kebutuhan proyek | ulid | ID publik/terdistribusi |
| `type` | Ya | string / enum | Nilai tetap `schedule` |
| `scheduleId` | Ya | string | Identifier bisnis jadwal |
| `publisherId` | Ya pada model multi-publisher | string | Identifier penyelenggara; definisikan target/source proyek |
| `trainingSlug` | Ya | string | Relasi ke tepat satu training |
| `batchNo` | Ya | string | Label batch/angkatan |
| `slug` | Ya | string | Route slug stabil |
| `title` | Ya | string | Judul pelaksanaan; harus membedakan batch bila perlu |
| `description` | Ya | string | Ringkasan pelaksanaan |
| `startDate` | Ya | iso_date_or_datetime | Tanggal/waktu mulai |
| `endDate` | Ya | iso_date_or_datetime | Tanggal/waktu selesai |
| `dateLabel` | Ya | string | Label tanggal yang ditampilkan; harus konsisten dengan tanggal terstruktur |
| `timezone` | Ya | string | Identifier zona waktu IANA, misalnya `Asia/Jakarta` |
| `pubDate` | Ya | offset_datetime | Tanggal publikasi |
| `updatedDate` | Ya | offset_datetime | Waktu pembaruan |
| `status` | Ya | enum | `scheduled`, `ongoing`, `completed`, `postponed`, `cancelled` |
| `registration` | Opsional | object | Informasi pendaftaran; nested schema wajib dibuat proyek |
| `delivery` | Opsional | object | Metode pelaksanaan dan akses |
| `venue` | Opsional | object | Tempat fisik/virtual |
| `completion` | Opsional | object | Informasi pascapelaksanaan/sertifikat |
| `sites` | Opsional | object | Referensi situs/publisher bila model proyek memerlukannya |

Jika proyek tidak memakai multi-publisher, `publisherId` harus dihilangkan dari `requiredFields` dan boleh dihilangkan seluruhnya dari dokumen. Bila dipakai, target dan integritasnya harus didefinisikan; jangan membiarkannya menjadi string bebas tanpa makna.

### 5.2 Validasi domain yang wajib ditambahkan proyek

Extension v1 hanya memeriksa tipe luar. Schema proyek (misalnya Zod) dan quality gates wajib memvalidasi:
1. `endDate` tidak lebih awal dari `startDate`.
2. Format tanggal dan waktu konsisten; tanggal tanpa waktu tidak boleh diam-diam dianggap memiliki jam tertentu.
3. `timezone` adalah identifier IANA yang valid dan dipakai konsisten untuk interpretasi jadwal.
4. Jika nilai start/end berupa datetime dengan offset, offset dan timezone tidak boleh saling bertentangan tanpa aturan eksplisit.
5. Status `cancelled` atau `postponed` harus tercermin jelas pada UI dan CTA registrasi tidak boleh tetap tampil seolah pendaftaran normal.
6. Status `completed` tidak boleh diperlakukan sebagai jadwal mendatang.
7. Jika `registration` aktif, URL/metode pendaftaran, periode, dan status pendaftaran harus valid.
8. Jadwal online wajib memiliki instruksi/tautan akses sesuai kebijakan publikasi; informasi privat tidak boleh diekspos sebelum waktunya.
9. Jadwal offline/hybrid harus memiliki lokasi yang memadai sebelum dipublikasikan.
10. `dateLabel` harus dihasilkan dari tanggal terstruktur atau diuji agar tidak berbeda.
11. Slug tetap stabil saat tanggal atau status berubah.

### 5.3 Schema.org

Gunakan `Event` untuk schedule bila dokumen merepresentasikan satu pelaksanaan nyata dengan waktu yang dapat ditentukan. Pemetaan minimum:

| Schema.org | Sumber |
|---|---|
| `Event.name` | `title` |
| `Event.startDate` | `startDate` |
| `Event.endDate` | `endDate` |

Mapping produksi sebaiknya juga mencakup, bila tersedia: `eventStatus`, `eventAttendanceMode`, `location`, `organizer`, `performer`/instructor, `offers`, `image`, dan `description`. Gunakan nilai Schema.org yang sesuai untuk status dan mode kehadiran; jangan menebak properti dari string internal. Jadwal yang dibatalkan/dijadwal ulang harus mencerminkan status aktual.

`Event` tidak boleh digunakan hanya karena sebuah halaman menyebut tanggal. Halaman training yang mendeskripsikan program secara umum tetap `Course`; halaman schedule yang mendeskripsikan satu instance adalah `Event`.

## 6. Listing dan navigasi

- Halaman detail training menampilkan informasi program dan daftar schedule terkait.
- Halaman detail schedule menampilkan ringkasan training induk dan tautan ke halaman training.
- Listing training dan listing schedule adalah halaman/route listing yang ditetapkan di IA proyek; jangan mengasumsikan route listing otomatis dibuat oleh extension.
- Filter status dan tanggal harus memakai field terstruktur, bukan parsing `dateLabel`.
- Default listing mendatang mengecualikan `completed` dan `cancelled`; kebijakan untuk `postponed` ditentukan jelas.
- Schedule yang sudah selesai tetap dapat diakses bila berguna sebagai arsip, tetapi tidak boleh tampil sebagai jadwal mendatang.
- Navigasi, breadcrumb, canonical, pagination, sitemap, dan internal links mengikuti Content & Information Architecture serta route manifest proyek.

## 7. Contoh konfigurasi registry ekstensi (ilustratif, bukan sumber normatif)

Bagian ini hanya menunjukkan cara menerjemahkan sebagian model domain pada Bagian 1–6 ke sintaks extension registry v1. **Kontrak normatif tetap Bagian 1–6 dan 8–9 pada dokumen ini**, bukan daftar `requiredFields` dalam contoh YAML. Jika terdapat perbedaan, kontrak domain mengikat dan contoh konfigurasi wajib diselaraskan.

Contoh ini bukan schema Zod lengkap dan bukan jaminan bahwa seluruh aturan domain dapat dinyatakan di registry. Field opsional seperti `ulid` dan `publisherId` boleh dideklarasikan pada `fieldTypes`, tetapi tidak boleh dimasukkan ke `requiredFields` kecuali proyek secara eksplisit memilihnya sebagai kewajiban. Field yang tidak dideklarasikan di `fieldTypes` tidak boleh digunakan pada konfigurasi v1.

```yaml
version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, type, trainingSlug, slug, title, description, pubDate, updatedDate]
    fieldTypes:
      id: positive_int
      ulid: ulid
      type: string
      trainingSlug: string
      slug: string
      title: string
      description: string
      categoryIds: positive_int_array
      pubDate: offset_datetime
      updatedDate: offset_datetime
      draft: boolean
      image: string
      hero: object
      blocks: array
    fieldEnums:
      type: [training]
    schemaTypes: [Course]
    schemaType: Course
    schemaMappings:
      Course:
        fieldMapping:
          name: title
          description: description
        requiredFields: [title, description]
    routePrefix: /training/

  schedule:
    directory: schedules
    requiredFields: [id, type, scheduleId, trainingSlug, batchNo, slug, title, description, startDate, endDate, dateLabel, timezone, pubDate, updatedDate, status]
    fieldTypes:
      id: positive_int
      ulid: ulid
      type: string
      scheduleId: string
      publisherId: string
      trainingSlug: string
      batchNo: string
      slug: string
      title: string
      description: string
      startDate: iso_date_or_datetime
      endDate: iso_date_or_datetime
      dateLabel: string
      timezone: string
      pubDate: offset_datetime
      updatedDate: offset_datetime
      status: string
      registration: object
      delivery: object
      venue: object
      completion: object
      sites: object
    fieldEnums:
      type: [schedule]
      status: [scheduled, ongoing, completed, postponed, cancelled]
    schemaTypes: [Event]
    schemaType: Event
    schemaMappings:
      Event:
        fieldMapping:
          name: title
          startDate: startDate
          endDate: endDate
        requiredFields: [title, startDate, endDate]
    routePrefix: /schedule/
    relations:
      trainingSlug:
        target: training
        targetField: trainingSlug
        cardinality: one
```

Catatan:
- `ulid` dideklarasikan sebagai field opsional dan sengaja tidak dimasukkan ke `requiredFields`, sesuai tabel field Training/Schedule.
- `publisherId` dideklarasikan sebagai field opsional dan sengaja tidak dimasukkan ke `requiredFields`; jika proyek mengaktifkan multi-publisher, proyek harus menambahkan kontrak target dan pemeriksaan relasi yang sesuai.
- Contoh ini hanya fixture konfigurasi parsial; bukan daftar lengkap validasi domain.
- Tambahkan `fieldTypes` dan validasi nested khusus untuk setiap properti domain yang benar-benar dipakai.
- Validator ekstensi memeriksa mapping sumber minimum, bukan membangun JSON-LD atau memvalidasi seluruh aturan Course/Event.

## 8. Checklist adopsi proyek

- [ ] Keputusan mengaktifkan collection training dan schedule tercatat dalam project brief/ADR.
- [ ] Direktori, route prefix, route listing, dan route detail ditetapkan.
- [ ] ID global dialokasikan lintas collection.
- [ ] Natural key `trainingSlug` unik dan stabil, atau relasi FK numerik dipilih secara eksplisit.
- [ ] Field wajib/opsional dan enum dikunci di registry ekstensi.
- [ ] Nested Zod schema untuk hero, blocks, registration, delivery, venue, completion, dan sites ditetapkan sesuai pemakaian.
- [ ] Validasi tanggal, zona waktu, status, dan aturan publikasi diuji.
- [ ] Schema Registry memetakan Course dan Event secara lengkap sesuai sumber data.
- [ ] UI listing/detail menangani status dan tanggal dengan benar.
- [ ] Fixture valid dan invalid tersedia untuk setiap collection dan setiap aturan domain.
- [ ] Route manifest, sitemap, canonical, breadcrumb, dan internal links diuji.
- [ ] Build Astro dan graph JSON-LD hasil render diuji terpisah dari validator frontmatter.

## 9. Batas dukungan standar

Dokumen ini menetapkan model referensi dan kontrak ekstensi. Ia tidak menyatakan bahwa seluruh field nested, business rules, rendering, pendaftaran, pembayaran, kapasitas peserta, atau JSON-LD telah diimplementasikan oleh validator inti. Proyek tetap bertanggung jawab menambahkan schema domain, renderer, tests, dan integrasi sesuai kebutuhan.
