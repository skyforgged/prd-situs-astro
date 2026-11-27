# Project Technical Architecture Decisions

> Status: Draft
> Versi: 0.2
> Astro/runtime/package manager: [ISI]

## 1. Struktur aplikasi

| Area | Keputusan | Lokasi | Alasan |
|---|---|---|---|
| Content collections | [ISI] | [ISI] | [ISI] |
| Components/block registry | [ISI] | [ISI] | [ISI] |
| Schema registry | [ISI] | [ISI] | [ISI] |
| Layouts | [ISI] | [ISI] | [ISI] |
| Routes | [ISI] | [ISI] | [ISI] |
| Content query/relations | [ISI] | [ISI] | [ISI] |
| Schema/JSON-LD | [ISI] | [ISI] | [ISI] |
| Validation | [ISI] | [ISI] | [ISI] |
| Assets | [ISI] | [ISI] | [ISI] |

## 2. Content collections dan schema

- Collection yang digunakan: [ISI]
- Schema per collection: [ISI lokasi]
- Kebijakan unknown fields: [ISI]
- Timestamp parsing: [ISI]
- Slug/route validation: [ISI]

## 3. Identitas dan relasi

- Lokasi ID registry: [ISI]
- Validasi ID global lintas collection: [ISI]
- ID block lokal: [ISI]
- Indeks relasi: [ISI]
- Perilaku target hilang: [ISI]

## 4. Block registry

| component | Schema props | Renderer | Schema.org diizinkan | Pengujian |
|---|---|---|---|---|
| [ISI] | [ISI] | [ISI] | [ISI] | [ISI] |

## 5. SEO dan structured data

- Site URL, locale, identitas organisasi: [ISI]
- Nested SEO schema: [ISI]
- Canonical/robots/Open Graph/Twitter: [ISI]
- Lokasi dan format Schema Registry: [ISI]
- Tipe yang diizinkan, scope, dan pemilik sumber data: [ISI]
- Status dukungan Google dan tanggal verifikasi: [ISI]
- JSON-LD graph dan @id: [ISI]
- Validator schema: [ISI]

## 6. Routing dan aset

- Pemetaan collection ke route: [ISI]
- Kebijakan redirect: [ISI]
- Validasi internal link: [ISI]
- Validasi aset dan alt: [ISI]
- Pipeline gambar: [ISI]

## 7. Quality gates dan CI

| Gate | Perintah | Lokal | CI | Fixture valid/invalid |
|---|---|---|---|---|
| QG-01–QG-11, QG-13 | [ISI] | [Ya/Tidak] | [Ya/Tidak] | [Lokasi] |
| QG-12 | Review manusia | Ya | Tidak | Tidak berlaku; lihat catatan persetujuan |

Perintah validasi:
- Konten: [ISI]
- Relasi: [ISI]
- Route/link: [ISI]
- Schema: [ISI]
- Production build: [ISI]

## 8. Deployment dan operasional

- Hosting/deployment: [ISI]
- Nama environment variables (tanpa nilai rahasia): [ISI]
- Logging/monitoring: [ISI]
- Rollback: [ISI]

## 9. Risiko teknis

| Risiko | Dampak | Mitigasi | Pemilik |
|---|---|---|---|
| [ISI] | [ISI] | [ISI] | [ISI] |

## 10. Kriteria penerimaan

- [ ] Selaras dengan Constitution dan Technical Architecture.
- [ ] Schema collection dan block registry eksplisit.
- [ ] ID global, relasi, route, dan aset tervalidasi.
- [ ] Nested SEO dan graph JSON-LD terdefinisi.
- [ ] Gate otomatis memiliki perintah dan fixture; QG-12 memiliki tempat pencatatan persetujuan reviewer.
- [ ] Build dan CI dapat direproduksi.
