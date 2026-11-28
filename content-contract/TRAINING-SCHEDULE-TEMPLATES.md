# Frontmatter Templates — Training dan Schedule

> Status: template ekstensi referensi
> Mengikuti: Project Collection Contract Extensions v1 dan Kontrak Collection Training dan Schedule 1.0

Template ini sengaja menggunakan nama field tanpa nilai. Template bukan dokumen siap-publikasi. Pertahankan field wajib walaupun nilainya belum tersedia; jangan mengarang ID, tanggal, relasi, URL pendaftaran, lokasi, instruktur, atau data schema.

## 1. Training

```yaml
---
id:
ulid:
type:
trainingSlug:
slug:
title:
description:
categoryIds:
pubDate:
updatedDate:
draft:
image:
hero:
blocks:
---
```

Ketentuan:
- `id` integer positif dan unik global.
- `ulid` opsional sesuai keputusan proyek.
- `type` bernilai `training`.
- `trainingSlug` adalah natural key unik dan stabil untuk relasi schedule.
- `slug` menentukan route detail training.
- `pubDate` dan `updatedDate` wajib memiliki timezone/offset. Format timestamp proyek harus konsisten.
- `categoryIds` hanya boleh digunakan bila target kategori dan relasinya terdaftar.
- `hero` dan `blocks` mengikuti schema proyek dan block registry; jangan menebak props.
- `image` harus menunjuk aset yang ada dan memiliki alternatif teks deskriptif pada kontrak media proyek.

## 2. Schedule

```yaml
---
id:
ulid:
type:
scheduleId:
publisherId:
trainingSlug:
batchNo:
slug:
title:
description:
startDate:
endDate:
dateLabel:
timezone:
pubDate:
updatedDate:
status:
registration:
delivery:
venue:
completion:
sites:
---
```

Ketentuan:
- `type` bernilai `schedule`.
- `scheduleId` adalah identifier bisnis, bukan ID global dokumen.
- `publisherId` wajib hanya jika model proyek multi-publisher menggunakannya dan targetnya didefinisikan.
- `trainingSlug` wajib menunjuk tepat satu dokumen training.
- `startDate` dan `endDate` menggunakan format ISO date atau datetime sesuai kontrak proyek.
- `timezone` harus merupakan identifier IANA yang valid, misalnya `Asia/Jakarta`.
- `dateLabel` adalah label tampilan yang harus konsisten dengan tanggal terstruktur.
- `status` hanya: `scheduled`, `ongoing`, `completed`, `postponed`, atau `cancelled`.
- `registration`, `delivery`, `venue`, `completion`, dan `sites` adalah object opsional; isi hanya berdasarkan nested schema proyek.
- Informasi privat akses online, data peserta, token meeting, dan data personal tidak boleh dimasukkan ke konten publik.

## 3. Kerangka relasi

Relasi referensi schedule ke training:

```yaml
# Di dokumen schedule
trainingSlug:
```

Target harus cocok tepat satu dokumen:

```yaml
# Di dokumen training
trainingSlug:
```

Relasi balik berupa query schedule berdasarkan `trainingSlug`; jangan menambahkan array scheduleIds ke training kecuali ada kebutuhan cache yang terdokumentasi dan divalidasi.

## 4. Checklist sebelum dokumen dianggap siap

- [ ] Field wajib lengkap dan sesuai tipe.
- [ ] ID global tidak bertabrakan dengan collection lain.
- [ ] Slug menghasilkan route unik.
- [ ] `trainingSlug` schedule cocok dengan tepat satu training.
- [ ] Tanggal mulai tidak melewati tanggal selesai.
- [ ] Zona waktu valid dan sesuai dengan offset datetime.
- [ ] Status schedule sesuai keadaan sebenarnya.
- [ ] Nested object lolos schema proyek.
- [ ] Aset, URL, dan tautan registrasi valid.
- [ ] Schema Course/Event sesuai konten dan mapping registry.
- [ ] Dokumen lolos quality gates proyek.
