# Project Initialization Workflow

> Status: Draft — workflow operasional
> Versi: 0.1
> Berlaku untuk: proyek situs yang mengadopsi PRD Situs Astro

## 1. Tujuan dan kedudukan

Dokumen ini mengatur urutan kerja System Analyst, AGENT AI, dan developer sejak repository proyek baru diterima sampai proyek dinyatakan siap diimplementasikan.

Workflow adalah prosedur operasional, bukan pengganti standar normatif. Otoritas tetap mengikuti Website Constitution, Content Contract, Content & Information Architecture, Technical Architecture, dan Quality Gates. Template di direktori ini merupakan artefak untuk merekam hasil setiap tahap.

**Larangan utama:** agen tidak boleh memulai implementasi halaman, komponen, collection, atau kode aplikasi hanya karena sudah memahami gambaran umum proyek. Implementasi dimulai setelah Implementation Readiness Review disetujui, kecuali pengguna secara eksplisit meminta prototipe/eksperimen terbatas. Pengecualian harus diberi label eksperimen dan tidak boleh dianggap arsitektur final.

## 2. Prinsip operasional

1. **Evidence before assumption.** Pisahkan fakta terverifikasi, temuan riset, asumsi, hipotesis, dan keputusan.
2. **User need before keyword.** Keyword adalah masukan riset, bukan unit otomatis pembentukan URL.
3. **Model before page production.** Tetapkan entitas, kontrak, dan relasi sebelum produksi konten.
4. **IA before routing implementation.** Route dan navigasi mengikuti intent dan hierarki informasi.
5. **Contract before code.** Field, schema, komponen, dan perilaku memiliki kontrak sebelum implementasi.
6. **Smallest sufficient architecture.** Jangan menambahkan collection, fitur, integrasi, atau abstraksi tanpa kebutuhan yang dapat dijelaskan.
7. **Traceability.** Keputusan penting dapat ditelusuri ke kebutuhan, bukti, pemilik, dan acceptance criteria.
8. **Iterative gates.** Tahap boleh diulang jika ditemukan konflik, risiko, atau bukti baru.
9. **No fabricated completion.** Status gate hanya lulus berdasarkan artefak dan pemeriksaan nyata.
10. **Human approval for material decisions.** Keputusan bisnis, klaim publik, biaya, risiko hukum, dan keputusan yang tidak dapat dipulihkan memerlukan persetujuan pihak berwenang.

## 3. Status dan mekanisme gate

Gunakan status:
- Not started
- In progress
- Blocked
- Ready for review
- Approved
- Rework required
- Not applicable (wajib disertai alasan dan approver)

Sebuah tahap hanya dapat Approved jika keluaran wajib tersedia, tidak ada pertanyaan kritis yang belum dijawab, asumsi berisiko diverifikasi/dimitigasi/diterima pemilik, acceptance criteria terpenuhi, dan reviewer/approver tercatat.

Jika ada kekurangan, catat blocker, dampak, pemilik, dan langkah penyelesaian. Pekerjaan non-dependen boleh berjalan, tetapi gate prasyarat tidak boleh dilewati.

## 4. Alur tahap

### Phase 0 — Repository & Standard Onboarding

**Tujuan:** memahami repository, instruksi, standar, dan batas kewenangan.

**Masukan:** repository dan branch yang ditetapkan pengguna, brief awal, instruksi proyek, serta akses file/sumber.

**Pekerjaan agen:**
1. Baca README dan AGENTS.md proyek.
2. Identifikasi stack, struktur, status repository, branch, commit terakhir, file yang ada, dan pekerjaan terdahulu.
3. Baca standar PRD Situs Astro yang relevan: Constitution, Content Contract, Frontmatter Templates, Content & Information Architecture, Technical Architecture, Quality Gates, Content Quality Standard, dan Project Architecture Templates.
4. Identifikasi dokumen yang sudah ada agar tidak membuat duplikasi atau menimpa keputusan terdahulu.
5. Catat batas akses, sumber yang belum dapat dibaca, dan kemampuan verifikasi.

**Keluaran:** ringkasan baseline repository; daftar standar yang berlaku; inventaris artefak tersedia/dibutuhkan; daftar akses, dependensi, dan blocker.

**Gate 0:**
- [ ] Instruksi dan standar utama telah dibaca.
- [ ] Branch dan batas perubahan jelas.
- [ ] Kondisi repository dan artefak lama dipahami.
- [ ] Tidak ada perubahan file sebelum baseline selesai, kecuali diminta.

### Phase 1 — Project Discovery & Brief

**Tujuan:** memahami masalah, organisasi, pengguna, tujuan, dan batas proyek.

**Masukan:** permintaan pengguna, wawancara/brief pemilik, dokumen bisnis, produk, layanan, regulasi, dan operasional.

**Pekerjaan agen:**
1. Rumuskan masalah, tujuan, kelompok pengguna, dan tugas pengguna.
2. Inventaris penawaran, layanan, produk, proses, wilayah operasi, dan batas klaim.
3. Bedakan fakta yang memiliki bukti dari asumsi.
4. Identifikasi tujuan bisnis dan indikator keberhasilan yang dapat diukur.
5. Catat batasan, dependensi, risiko, dan pertanyaan terbuka.
6. Jangan mengisi kekosongan informasi bisnis dengan fakta rekaan.

**Keluaran:** PROJECT-BRIEF.md; fact/evidence register; assumption & open-question register; daftar stakeholder dan approver.

**Gate 1:**
- [ ] Masalah dan tujuan proyek dapat dijelaskan.
- [ ] Kelompok pengguna dan tugas utamanya diketahui.
- [ ] Penawaran, cakupan, serta pengecualian tercatat.
- [ ] Fakta dan asumsi dibedakan.
- [ ] Pertanyaan kritis memiliki pemilik dan rencana verifikasi.
- [ ] Pemilik proyek menyetujui brief atau menyatakan bagian yang masih terbuka.

### Phase 2 — Research & Evidence

**Tujuan:** memperoleh bukti untuk keputusan konten, produk, dan arsitektur.

**Masukan:** Project Brief, daftar pertanyaan/asumsi, sumber primer, dokumen internal, data pengguna, hasil pencarian, dan referensi.

**Pekerjaan agen:**
1. Prioritaskan sumber primer: pemilik proses, dokumen resmi, regulasi, dokumentasi produk, data operasional, dan sumber otoritatif.
2. Gunakan sumber sekunder untuk konteks dan pembanding; jangan menyamakan opini pihak ketiga dengan fakta.
3. Analisis kompetitor/referensi untuk memahami pola, kualitas jawaban, celah informasi, dan pengalaman pengguna—bukan menyalin struktur atau konten.
4. Catat tanggal akses/publikasi untuk informasi yang berubah dari waktu ke waktu.
5. Untuk klaim teknis, hukum, keselamatan, sertifikasi, dan regulasi, tentukan kebutuhan review ahli.
6. Catat sumber bertentangan, kualitas bukti, keterbatasan, dan hal yang belum pasti.
7. Jangan menganggap hasil pencarian keyword sebagai bukti tunggal kebutuhan halaman tersendiri.

**Keluaran:** research/evidence log; ringkasan kebutuhan dan pertanyaan pengguna; benchmark/referensi beserta interpretasi; daftar gap informasi dan validasi ahli; pembaruan assumption register.

**Gate 2:**
- [ ] Klaim material memiliki sumber yang dapat ditelusuri.
- [ ] Sumber primer diprioritaskan dan keterbatasan dicatat.
- [ ] Temuan dipisahkan dari rekomendasi.
- [ ] Gap dan konflik bukti tercatat.
- [ ] Klaim berisiko tidak dianggap final tanpa review sesuai.

### Phase 3 — Intent Mapping & Page Opportunity

**Tujuan:** menerjemahkan kebutuhan menjadi kelompok intent dan peluang jawaban, bukan daftar URL berbasis keyword.

**Masukan:** Project Brief, research/evidence log, data pencarian/pengguna bila tersedia.

**Pekerjaan agen:**
1. Kelompokkan kebutuhan berdasarkan tugas, pertanyaan, tahap keputusan, intent, dan jawaban yang dibutuhkan.
2. Petakan kebutuhan ke kandidat halaman, section, navigasi, fungsi, atau jawaban non-halaman.
3. Gabungkan kebutuhan dengan intent dan jawaban inti yang sama.
4. Pisahkan halaman hanya jika kebutuhan, proses, bukti, risiko, atau tindakan pengguna berbeda secara material.
5. Identifikasi keyword cannibalization, doorway pages, thin content, dan duplikasi.
6. Prioritaskan berdasarkan nilai pengguna, nilai bisnis, bukti permintaan, kompetensi organisasi, biaya pemeliharaan, dan risiko.
7. Nyatakan kebutuhan yang belum cukup bukti sebagai hipotesis, bukan rencana final.

**Keluaran:** intent map; page opportunity matrix; keputusan gabung/pisah/section/tidak dibuat; prioritas dan alasan; daftar kebutuhan riset tambahan.

**Gate 3:**
- [ ] Setiap kandidat halaman memiliki intent/tugas dan jawaban utama.
- [ ] Tidak ada satu URL otomatis untuk setiap keyword.
- [ ] Keputusan gabung/pisah memiliki alasan.
- [ ] Risiko tumpang tindih dan thin content diperiksa.
- [ ] Prioritas mempertimbangkan nilai pengguna dan kemampuan memberi jawaban.
- [ ] Kandidat yang belum terbukti tidak diperlakukan sebagai keputusan final.

### Phase 4 — Content Modeling & Content Contract

**Tujuan:** menentukan entitas dan struktur data sebelum konten diproduksi.

**Masukan:** intent map yang disetujui, Content Contract, Frontmatter Templates, dan sumber kebenaran.

**Pekerjaan agen:**
1. Identifikasi entitas yang dibutuhkan; jangan membuat collection hanya karena contoh template tersedia.
2. Tentukan collection, tanggung jawab, apakah menghasilkan route, dan pemilik akurasi.
3. Tentukan sumber kebenaran untuk fakta lintas halaman.
4. Tentukan field frontmatter lengkap dengan tipe, kewajiban, validasi, dan fallback.
5. Gunakan Frontmatter Templates sebagai checklist field; jangan menghilangkan field wajib karena belum diketahui. Catat nilai yang belum tersedia sebagai blocker/status sesuai.
6. Definisikan ID dokumen unik global lintas collection dan ID block unik dalam dokumen pemilik.
7. Definisikan foreign key numerik, target collection, kardinalitas, optionality, keunikan array, dan perilaku target hilang.
8. Tetapkan schema utama dokumen; schema block hanya bila relevan.
9. Definisikan taksonomi hanya jika memiliki tujuan jelas.
10. Rencanakan registry, schema validation, dan relation validation.

**Keluaran:** CONTENT-MODEL.md; matriks relasi; kontrak field/frontmatter proyek; ID registry design; sumber kebenaran dan pemilik data.

**Gate 4:**
- [ ] Setiap collection memiliki tujuan.
- [ ] Field dan tipe tidak ambigu.
- [ ] Field wajib/opsional dan fallback ditentukan.
- [ ] ID global dan ID block lokal dibedakan.
- [ ] Seluruh relasi memiliki target dan kardinalitas.
- [ ] Sumber kebenaran dan pemilik akurasi diketahui.
- [ ] Kontrak selaras dengan Content Contract universal.
- [ ] Tidak ada entitas atau field spekulatif yang dipaksakan.

### Phase 5 — Information Architecture & Route Design

**Tujuan:** mengubah intent dan model konten menjadi struktur informasi yang dapat dipahami dan dinavigasi.

**Masukan:** intent map dan content model yang disetujui serta standar Content & Information Architecture.

**Pekerjaan agen:**
1. Susun hierarki topik, halaman, dan relasi berdasarkan kebutuhan pengguna.
2. Buat sitemap dan route manifest; pastikan route unik lintas jenis halaman.
3. Tentukan canonical, trailing slash, redirect, indexability, sitemap inclusion, dan kebijakan parameter.
4. Rancang menu, footer, breadcrumb, dan aturan target. Target internal memakai ID dokumen sesuai kontrak.
5. Rancang internal linking dan related content dengan sumber relasi, filter, sorting, tie-break, batas hasil, dan empty state.
6. Tentukan listing, arsip, pagination, filter, dan perilaku URL bila diperlukan.
7. Evaluasi halaman lokal hanya jika cakupan dan nilai lokal nyata dapat dibuktikan; bedakan alamat fisik dan area layanan.
8. Rancang CTA berdasarkan tugas dan tahap keputusan; pastikan target/tindakan tersedia.
9. Periksa route yatim, konflik intent, kedalaman navigasi, duplikasi, dan jalur pengguna terputus.

**Keluaran:** INFORMATION-ARCHITECTURE.md; route manifest/sitemap; navigation & breadcrumb specification; internal linking rules; listing/conversion rules; local coverage policy bila relevan.

**Gate 5:**
- [ ] Semua route memiliki tujuan dan jenis halaman.
- [ ] Tidak ada route konflik.
- [ ] Canonical, indexability, redirect, dan sitemap konsisten.
- [ ] Navigasi dan breadcrumb memiliki sumber target valid.
- [ ] Internal linking dan listing deterministik.
- [ ] Halaman lokal memiliki bukti dan diferensiasi nyata.
- [ ] CTA mengarah ke tindakan tersedia.
- [ ] Struktur mendukung tugas pengguna.

### Phase 6 — Content Experience & Editorial Specification

**Tujuan:** menetapkan bagaimana tiap jenis halaman menjawab kebutuhan dengan akurat, berguna, dan dapat dipelihara.

**Masukan:** brief, research, intent map, content model, IA, Content Quality Standard, dan reviewer substansi/ahli.

**Pekerjaan agen:**
1. Definisikan tujuan, audiens, pertanyaan utama, bukti, dan batas klaim setiap page type.
2. Tentukan struktur informasi sesuai kebutuhan; jangan memaksakan outline sama untuk semua halaman.
3. Tentukan komponen/block yang benar-benar dibutuhkan.
4. Tentukan sumber, metode verifikasi, reviewer, dan pemilik akurasi klaim material.
5. Tentukan kebijakan gambar, sumber aset, alt text, hak penggunaan, dan visual pendukung pemahaman.
6. Tetapkan CTA dan tautan kontekstual.
7. Tetapkan kebijakan tanggal, review berkala, konten usang, merge, redirect, dan retirement.
8. Jangan menggunakan jumlah kata sebagai target kelulusan universal; kedalaman mengikuti kompleksitas dan kebutuhan pembaca.

**Keluaran:** editorial/page-type specification; block/component requirements; evidence and review requirements; content governance/lifecycle; content brief halaman prioritas bila diminta.

**Gate 6:**
- [ ] Tiap jenis halaman memiliki tujuan dan kebutuhan informasi.
- [ ] Struktur tidak diduplikasi tanpa alasan.
- [ ] Klaim dan sumber verifikasi ditentukan.
- [ ] Reviewer dan pemilik akurasi jelas.
- [ ] Kebijakan aset dan konten usang ditetapkan.
- [ ] Content Quality Standard diterapkan tanpa target kata arbitrer.

### Phase 7 — Technical Architecture

**Tujuan:** menerjemahkan kontrak konten dan IA menjadi rancangan teknis Astro yang dapat dibangun dan diverifikasi.

**Masukan:** content model/frontmatter, IA/route manifest, editorial/component requirements, Technical Architecture, dan Quality Gates.

**Pekerjaan agen:**
1. Tetapkan versi Astro, runtime, package manager, adapter, hosting, dan batas lingkungan.
2. Rancang struktur repository, content collections, schema, layouts, components, dan route generation.
3. Tetapkan block registry, schema props, renderer, fallback, dan aturan komponen tidak dikenal.
4. Rancang ID registry dan validator ID global.
5. Rancang relation resolver/index, validasi target, dan perilaku target hilang.
6. Rancang route/link validator, asset validation, dan fixture valid/invalid.
7. Tetapkan SEO metadata, nested schema, canonical, robots, Open Graph/Twitter, JSON-LD graph dan @id sesuai konten nyata.
8. Tetapkan image pipeline, format, ukuran, alt validation, dan loading strategy.
9. Petakan Quality Gates ke script lokal dan CI; bedakan gate otomatis dari review manusia.
10. Tetapkan logging, monitoring, deployment, nama environment variables, rollback, dan risiko operasional.
11. Jangan memilih dependency atau layanan pihak ketiga sebelum kebutuhan dan trade-off dinyatakan.

**Keluaran:** TECHNICAL-ARCHITECTURE.md; keputusan/ADR teknis; rencana validator dan quality gates; dependency/deployment plan.

**Gate 7:**
- [ ] Semua pilihan teknis menjawab kebutuhan yang disetujui.
- [ ] Schema dan registry memiliki tanggung jawab jelas.
- [ ] ID, relasi, route, aset, dan JSON-LD memiliki strategi validasi.
- [ ] Quality Gates dipetakan ke cara verifikasi.
- [ ] Build, deployment, dan rollback dipahami.
- [ ] Risiko dan trade-off dicatat.
- [ ] Tidak ada keputusan teknis penting yang hanya tersirat dalam percakapan.

### Phase 8 — PRD & Acceptance Criteria

**Tujuan:** menyatukan keputusan menjadi spesifikasi implementasi terstruktur dan dapat diuji.

**Masukan:** keluaran Phase 0–7, daftar keputusan/pertanyaan terbuka, prioritas, dan batas proyek.

**Pekerjaan agen:**
1. Susun PRD berdasarkan tujuan, pengguna, scope, requirement fungsional/non-fungsional, data, IA, pengalaman konten, SEO, integrasi, dan operasional yang relevan.
2. Setiap requirement memiliki ID, deskripsi, prioritas, alasan/sumber, dan acceptance criteria.
3. Pisahkan must-have, should-have, could-have, dan out-of-scope.
4. Kaitkan requirement dengan halaman, collection, komponen, ADR, dan quality gate.
5. Nyatakan error state, empty state, loading state, fallback, dan edge cases.
6. Tandai asumsi dan keputusan yang menunggu persetujuan.
7. Periksa konflik antar dokumen dan hapus duplikasi requirement.
8. Jangan mengubah keputusan disetujui secara diam-diam; perubahan material harus dicatat dan ditinjau.

**Keluaran:** PRD proyek; requirement traceability matrix; acceptance criteria; backlog implementasi berprioritas; daftar out-of-scope dan open decisions.

**Gate 8:**
- [ ] Requirement dapat dipahami dan diuji.
- [ ] Setiap requirement memiliki alasan/sumber dan prioritas.
- [ ] Acceptance criteria tidak ambigu.
- [ ] Requirement terhubung ke dokumen arsitektur dan quality gates.
- [ ] Konflik dan asumsi terbuka terlihat.
- [ ] Scope dan out-of-scope disetujui.

### Phase 9 — Implementation Readiness Review

**Tujuan:** memastikan proyek siap masuk implementasi tanpa memindahkan keputusan arsitektur yang belum selesai kepada developer secara tersembunyi.

**Pemeriksaan:**
- [ ] Project Brief disetujui.
- [ ] Research/evidence log cukup untuk keputusan kritis.
- [ ] Intent map dan page opportunity disetujui.
- [ ] Content model, frontmatter, ID, dan relation matrix disetujui.
- [ ] Sitemap, route manifest, navigasi, breadcrumb, dan internal linking disetujui.
- [ ] Listing, local coverage, dan conversion policy diputuskan atau dinyatakan tidak berlaku dengan alasan.
- [ ] Editorial specification, sumber fakta, dan governance ditetapkan.
- [ ] Technical Architecture dan ADR penting disetujui.
- [ ] PRD, acceptance criteria, prioritas, dan out-of-scope lengkap.
- [ ] Quality Gates dan strategi test/CI dapat dijalankan pada proyek.
- [ ] Risiko, dependensi, serta keputusan terbuka memiliki pemilik dan mitigasi.
- [ ] Pemilik proyek menyetujui dimulainya implementasi.

**Hasil review:**
- Ready: semua prasyarat kritis terpenuhi dan persetujuan tercatat.
- Ready with accepted risks: hanya risiko non-blocking yang eksplisit diterima pemilik.
- Blocked: keputusan/dependensi kritis belum selesai.
- Rework: artefak perlu diperbaiki sebelum diajukan ulang.

Tidak ada status Ready otomatis hanya karena seluruh file template telah dibuat.

## 5. Jalur iterasi dan perubahan

Jika bukti baru mengubah keputusan:
1. Catat temuan dan sumbernya.
2. Identifikasi keputusan dan artefak terdampak.
3. Kembali ke phase paling awal yang relevan.
4. Perbarui dokumen dan requirement yang terpengaruh.
5. Periksa dampak ke route, data, relasi, konten, komponen, SEO, dan acceptance criteria.
6. Buat ADR jika keputusan material mengubah arsitektur.
7. Minta persetujuan ulang bila perubahan menyentuh keputusan yang sebelumnya disetujui.

Perubahan redaksional kecil tidak perlu ADR. Perubahan material terhadap model data, route, integrasi, keamanan, deployment, atau perilaku sistem harus memiliki catatan keputusan.

## 6. Aturan kerja AGENT AI

- Mulai dengan membaca instruksi repository dan standar yang berlaku; jangan menganggap semua file proyek baru.
- Kerjakan phase sesuai urutan dan laporkan phase/status saat menyerahkan hasil.
- Jangan membuat data bisnis, bukti, volume pencarian, kemampuan organisasi, alamat, testimoni, sertifikasi, atau klaim kepatuhan.
- Ajukan pertanyaan ketika jawaban pengguna diperlukan untuk keputusan kritis; jangan membanjiri pengguna dengan pertanyaan yang dapat ditunda.
- Kelompokkan pertanyaan yang saling bergantung; izinkan pekerjaan non-blocking berjalan.
- Jangan mengubah file atau commit jika pengguna hanya meminta analisis/review.
- Ikuti branch dan workflow Git yang ditentukan pengguna; jangan membuat branch tanpa izin.
- Jangan mengklaim build, test, validator, atau deployment berhasil tanpa menjalankan dan memeriksa hasilnya.
- Jangan menandai checklist lulus berdasarkan keberadaan dokumen semata.
- Saat menyelesaikan phase, berikan ringkasan keputusan, artefak, blocker, bukti verifikasi, dan rekomendasi tahap berikutnya.
- Jika pengguna meminta implementasi/prototipe sebelum gate selesai, jelaskan risiko dan batasi pekerjaan sesuai persetujuan; catat keputusan yang belum final.

## 7. Template laporan akhir setiap phase

| Field | Isi |
|---|---|
| Phase | [Nomor dan nama] |
| Status | [Not started/In progress/Blocked/Ready for review/Approved/Rework required/Not applicable] |
| Artefak dibuat/diubah | [Path] |
| Keputusan utama | [Ringkasan] |
| Bukti/sumber | [Rujukan] |
| Pertanyaan/blocker | [Daftar atau Tidak ada] |
| Pemeriksaan dilakukan | [Pemeriksaan nyata] |
| Persetujuan | [Nama/role/tanggal atau Belum] |
| Langkah berikutnya | [Phase/tindakan] |

## 8. Relasi dengan dokumen template

| Phase | Dokumen template utama |
|---|---|
| 0 | Baseline repository dan README proyek |
| 1 | PROJECT-BRIEF.md |
| 2 | Evidence log proyek (buat sesuai kebutuhan) |
| 3 | INFORMATION-ARCHITECTURE.md — bagian intent map |
| 4 | CONTENT-MODEL.md |
| 5 | INFORMATION-ARCHITECTURE.md, LISTING-AND-CONVERSION.md, LOCAL-COVERAGE.md bila relevan |
| 6 | CONTENT-GOVERNANCE.md dan spesifikasi editorial proyek |
| 7 | TECHNICAL-ARCHITECTURE.md dan decisions/ADR-TEMPLATE.md |
| 8 | PRD proyek dan requirement traceability matrix |
| 9 | Implementation Readiness Review |

## 9. Batasan dan evaluasi workflow

Workflow versi 0.1 perlu diuji pada satu proyek Astro nyata. Setelah adopsi pertama, evaluasi:
- apakah urutan phase efisien untuk tipe proyek berbeda;
- apakah artefak wajib terlalu banyak atau ada keputusan yang belum tertampung;
- apakah gate dapat diverifikasi dan tidak sekadar administratif;
- apakah agen dapat mengikuti instruksi tanpa pertanyaan berulang;
- apakah perubahan antarphase dapat ditelusuri;
- apakah phase dapat digabung untuk proyek sederhana tanpa mengurangi kontrol keputusan kritis.

Penyederhanaan diperbolehkan berdasarkan kompleksitas proyek, tetapi tidak boleh menghilangkan validasi fakta, kontrak data, route, keputusan teknis, acceptance criteria, dan persetujuan readiness yang relevan.
