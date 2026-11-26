# Information Architecture & Route Plan

> Status: Draft
> Versi: 0.1
> Domain kanonis: [ISI]

## 1. Intent map

Jangan otomatis membuat satu URL untuk setiap keyword atau pertanyaan. Gabungkan kebutuhan dengan intent dan jawaban inti yang sama; pisahkan hanya bila jawaban, bukti, proses, atau tindakan memang berbeda.

| ID | Pengguna | Kebutuhan/pertanyaan | Tahap keputusan | Intent dominan | Jawaban terbaik | Halaman/section kandidat | Bukti |
|---|---|---|---|---|---|---|---|
| INT-01 | [ISI] | [ISI] | [Awareness/Consideration/Decision/Use] | [ISI] | [ISI] | [ISI] | [ISI] |

### Keputusan penggabungan/pemisahan

| Kebutuhan yang tumpang tindih | Keputusan | Alasan intent | Halaman tujuan |
|---|---|---|---|
| [ISI] | [Gabung/Pisah/Section/Tidak dibuat] | [ISI] | [ISI] |

## 2. Sitemap dan route manifest

| Route ID | Path | Jenis halaman | Collection/sumber | Content ID | Tujuan utama | Parent IA | Indexability | Canonical | Status |
|---|---|---|---|---:|---|---|---|---|---|
| R-001 | [ISI] | [ISI] | [ISI] | [ISI] | [ISI] | [ISI/Tidak ada] | [Index/Noindex] | [ISI] | [Planned/Active/Retired] |

Aturan global:
- Trailing slash: [ISI]
- Bahasa URL: [ISI]
- Parameter query: [ISI]
- Canonical: [ISI]
- Redirect: [ISI]
- Konflik route lintas collection: harus gagal validasi.

## 3. Navigasi dan footer

| Menu ID | Lokasi | Sumber dokumen | Label | Target pageId atau URL | Parent | Urutan | Kondisi tampil |
|---|---|---|---|---|---|---:|---|
| M-01 | [header/footer/mobile/utility] | [ISI] | [ISI] | [ISI] | [ISI] | [ISI] | [ISI] |

Setiap item menu memiliki tepat satu target. Target internal memakai ID dokumen; URL eksternal harus absolut dan tervalidasi.

- Maksimum kedalaman menu: [ISI sesuai kontrak]
- Aturan mobile: [ISI]
- Kelompok footer: [ISI]
- Informasi organisasi di footer: [ISI]

## 4. Breadcrumb

| Jenis halaman/route | Breadcrumb diperlukan? | Rantai | Sumber parent | Perilaku tanpa parent |
|---|---|---|---|---|
| [ISI] | [Ya/Tidak] | [ISI] | [Relasi ID/aturan eksplisit] | [ISI] |

Breadcrumb harus mewakili hierarki bermakna bagi pengguna, bukan potongan slug atau parent buatan.

## 5. Internal linking

| Jenis halaman sumber | Target yang relevan | Alasan pengguna | Lokasi tautan | Sumber relasi | Wajib/opsional |
|---|---|---|---|---|---|
| [ISI] | [ISI] | [ISI] | [Body/CTA/Related/Breadcrumb] | [FK/Editorial/manual] | [ISI] |

Pedoman anchor: [ISI]. Jangan menetapkan jumlah tautan sebagai target; setiap tautan harus membantu pengguna.

## 6. URL lama, redirect, dan indexability

| URL lama | URL tujuan | Status redirect | Alasan | Internal link diperbarui? |
|---|---|---|---|---|
| [ISI] | [ISI] | [301/308/Tidak ada] | [ISI] | [Ya/Tidak] |

- Sumber sitemap XML: [ISI]
- Route yang dikecualikan: [ISI]
- Kebijakan filter/pagination: [ISI]

## 7. Validasi IA

- [ ] Semua route memiliki tujuan dan jenis halaman.
- [ ] Route unik dan canonical konsisten.
- [ ] Menu/breadcrumb mengarah ke target yang tersedia.
- [ ] Internal link memiliki alasan dan target yang valid.
- [ ] Redirect dan sitemap sesuai manifest.
- [ ] Tidak ada halaman yang dibuat semata-mata untuk variasi keyword.
