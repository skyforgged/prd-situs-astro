# Content Model & Relation Matrix

> Status: Draft
> Versi: 0.1

## 1. Collection dan tanggung jawab

Jangan membuat collection hanya karena tersedia dalam template standar. Gunakan hanya entitas yang dibutuhkan proyek.

| Collection | Entitas/tanggung jawab | Menghasilkan route? | Kontrak frontmatter | Pemilik akurasi |
|---|---|---|---|---|
| [ISI] | [ISI] | [Ya/Tidak] | [ISI] | [ISI] |

## 2. Sumber kebenaran

| Fakta/informasi | Sumber utama | Lokasi penyimpanan | Digunakan oleh | Mekanisme pembaruan |
|---|---|---|---|---|
| [ISI] | [ISI] | [Markdown/config/sumber eksternal] | [ISI] | [ISI] |

## 3. Matriks relasi

Semua relasi dokumen memakai ID numerik. Definisikan target collection, kardinalitas, optionality, dan perilaku target hilang.

| Field relasi | Collection sumber | Collection target | Kardinalitas | Wajib? | Array unik? | Jika target hilang | Makna relasi |
|---|---|---|---|---|---|---|---|
| [ISI] | [ISI] | [ISI] | [1:1/N:1/1:N/N:N] | [Ya/Tidak] | [Ya/Tidak/NA] | [Build fail/Perilaku lain] | [ISI] |

## 4. Field khusus proyek

| Collection | Field | Tipe | Wajib? | Validasi | Fallback |
|---|---|---|---|---|---|
| [ISI] | [ISI] | [ISI] | [Ya/Tidak] | [ISI] | [ISI/Tidak ada] |

## 5. ID registry

- Lokasi registry: [ISI]
- Mekanisme alokasi ID: [ISI]
- Validasi unik global lintas collection: [ISI]
- Kebijakan ID konten yang dihapus/diarsipkan: [ISI]
- Pemilik: [ISI]

## 6. Taksonomi (bila digunakan)

| Taksonomi | Collection pemilik | Tujuan | Cara direlasikan | Aturan |
|---|---|---|---|---|
| [ISI/Tidak digunakan] | [ISI] | [ISI] | [ISI] | [ISI] |

## 7. Kriteria penerimaan

- [ ] Collection hanya dibuat bila ada kebutuhan nyata.
- [ ] Sumber kebenaran fakta ditentukan.
- [ ] Relasi menggunakan FK numerik.
- [ ] Target, kardinalitas, wajib/opsional, dan target hilang ditetapkan.
- [ ] ID dokumen unik global; ID block lokal per dokumen.
- [ ] Schema setiap collection menolak field tak dikenal.
