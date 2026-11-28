# Validator Otomatis — Milestone 3 dari 5

> Status: Validasi Foreign Key lintas dokumen
> Cakupan: keberadaan target, target collection, kardinalitas, referensi ambigu, dan siklus relasi yang dilarang

## Tujuan

Milestone 2 memvalidasi bentuk field relasi di dalam satu dokumen. Milestone ini membangun indeks dari seluruh dokumen yang dipindai, lalu menyelesaikan foreign key terhadap ID dokumen global. Nilai numerik yang valid secara sintaksis tidak dianggap valid sebelum targetnya ditemukan dan jenis targetnya sesuai matriks relasi Content Contract 1.5.

## Relasi yang diselesaikan

| Field | Sumber | Target yang diterima | Kardinalitas | Pemeriksaan |
|---|---|---|---|---|
| `pageId` | Item Menu, termasuk children | Homepage atau Page | Tepat satu target pada setiap item | Target ada dan bertipe benar |
| `parentPageId` | Page | Page | 0..1 | Target ada, bertipe Page, bukan diri sendiri, dan hierarki bebas siklus |
| `categoryIds` | Article, Service | Category | 0..N | Setiap target ada dan bertipe Category |
| `relatedArticleIds` | Article | Article | 0..N | Setiap target ada dan bertipe Article; tidak boleh menunjuk dirinya sendiri |
| `relatedServiceId` | Article | Service | 0..1 | Target ada dan bertipe Service |
| `relatedServiceIds` | Service | Service | 0..N | Setiap target ada dan bertipe Service; tidak boleh menunjuk dirinya sendiri |
| `serviceIds` | Block yang mendeklarasikannya | Service | 0..N | Setiap target ada dan bertipe Service |
| `categoryId` | Block `content-list` | Category | 1:1 jika digunakan | Target ada dan bertipe Category |

Relasi jamak tetap mengikuti validasi Milestone 2: harus berupa array ID positif dan tidak boleh mengandung ID duplikat. Relasi tunggal harus berupa satu ID positif, bukan array.

## Relasi yang belum dapat digunakan

- `authorId` → Author/Person.
- `providerId` → Organization/Provider.

Content Contract 1.5 secara eksplisit menyatakan bahwa kontrak jenis konten target tersebut belum tersedia. Karena itu, jika salah satu field diisi, validator menggagalkan pemeriksaan dengan pesan bahwa target contract/collection belum didefinisikan. Validator tidak menerima dokumen sembarang yang kebetulan memiliki ID sama sebagai Author atau Organization. Setelah kontrak target ditetapkan pada perubahan standar berikutnya, relasi ini dapat diaktifkan dengan aturan collection dan kardinalitas yang eksplisit.

## Aturan resolusi

1. Seluruh dokumen yang dipindai diindeks berdasarkan ID global.
2. ID target yang tidak ditemukan menyebabkan gagal.
3. ID target yang muncul lebih dari sekali dianggap ambigu dan menyebabkan gagal; validator tidak memilih salah satu dokumen secara arbitrer.
4. Target harus berada pada collection/jenis yang disebut matriks relasi.
5. Referensi dari menu ditelusuri rekursif hingga children.
6. Referensi block yang sudah dinyatakan dalam Content Contract (`serviceIds` dan `content-list.categoryId`) ikut diperiksa.
7. Hierarki `parentPageId` harus acyclic. Relasi related-content tidak diwajibkan simetris; self-reference pada relasi artikel/layanan ditolak, sedangkan relasi timbal balik antar dua dokumen berbeda tetap diperbolehkan.
8. Field relasi ke target entity yang kontraknya belum ada tidak boleh dipakai.

## Cara menjalankan

Jalankan terhadap root yang mencakup semua collection agar indeks ID dan pemeriksaan FK lengkap:

```bash
python -m pip install -r requirements-dev.txt
pytest -q
python scripts/validate_content.py src/content
```

Untuk direktori collection khusus, gunakan pemetaan yang sama seperti Milestone 2 melalui opsi `--collection KIND=DIR`. Setiap collection yang menjadi target relasi harus termasuk dalam root pemindaian dan dipetakan ke kind yang benar.

## Batas cakupan

Milestone ini memeriksa relasi yang sudah memiliki target collection dalam matriks standar. Ia belum membuat kontrak Author/Person atau Organization/Provider. Ia juga belum memvalidasi seluruh properti relasi dinamis di semua block secara menyeluruh; itu memerlukan Block Registry dan schema props pada Milestone berikutnya. Relasi yang tidak tercantum dalam matriks tidak boleh dianggap otomatis tervalidasi.

Validasi route/slug collision, Schema Registry dan pemetaan JSON-LD, Block Registry/props, referensi aset/tautan, serta integrasi seluruh Quality Gates tetap di luar cakupan milestone ini.

## Bukti pengujian

Suite mencakup target tersedia, target hilang, target salah jenis, menu bertingkat, target Homepage, relasi block, larangan penggunaan Author/Person dan Organization/Provider sebelum kontrak target tersedia, self-reference, serta siklus parent Page. Jumlah akhir dan status CI dicatat setelah workflow GitHub Actions selesai.
