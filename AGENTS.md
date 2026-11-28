# Instruksi Agen — PRD Situs Astro

## Baca sebelum bekerja
- Sebelum mengklaim fitur/quality gate telah didukung, baca [`quality/CAPABILITY-BOUNDARIES.md`](quality/CAPABILITY-BOUNDARIES.md). Bedakan bukti VALIDATOR, CONTRACT, PROJECT, dan MANUAL; jangan menyamakan kontrak dengan implementasi runtime.

- Untuk perubahan standar, kontrak, validator, template, atau quality gate, periksa [`docs/REQUIREMENTS-TRACEABILITY-MATRIX.md`](docs/REQUIREMENTS-TRACEABILITY-MATRIX.md). Pertahankan ID requirement; perbarui matriks bila sumber normatif atau bukti berubah. Jangan mengklaim gate PROJECT/MANUAL lulus dari test repository standar.

1. Baca `README.md` untuk peta standar.
2. Patuhi `constitution/WEBSITE-CONSTITUTION.md` sebagai aturan tertinggi.
3. Gunakan `content-contract/CONTENT-CONTRACT.md` untuk bentuk data Markdown.
4. Baca `content-contract/FRONTMATTER-TEMPLATES.md` sebelum membuat atau merevisi enam jenis konten inti. Jika proyek mengaktifkan collection ekstensi, baca kontrak dan template ekstensi terkait (misalnya `TRAINING-SCHEDULE-CONTRACT.md` dan `TRAINING-SCHEDULE-TEMPLATES.md`) sebelum membuat dokumennya.
5. Gunakan `architecture/TECHNICAL-ARCHITECTURE.md` untuk keputusan implementasi Astro.
6. Gunakan `architecture/CONTENT-AND-INFORMATION-ARCHITECTURE.md` saat menyusun sitemap, jenis halaman, navigasi, route, internal linking, listing, atau jalur konversi.
7. Gunakan `quality/QUALITY-GATES.md` untuk verifikasi teknis dan editorial.
8. Baca `quality/CONTENT-QUALITY-STANDARD.md` sebelum membuat, merevisi, atau menilai konten yang akan dipublikasikan.
9. Baca `docs/REVIEW-NOTES.md` dan `CHANGELOG.md` sebelum mengubah standar.

## Aturan kerja
- Jangan membuat branch kecuali diminta secara eksplisit; kerjakan pada branch yang sedang ditentukan pengguna.
- Jangan mengubah repository saat pengguna hanya meminta audit, pembacaan, atau pendapat.
- Jangan mengarang hasil build, test, status deployment, atau isi file. Jalankan pemeriksaan yang tersedia atau nyatakan batas verifikasinya.
- Pertahankan pemisahan konten Markdown, komponen presentasi, layout, dan konfigurasi UI.
- Jangan menambahkan jenis konten atau fitur wajib ke semua proyek tanpa dasar Constitution.
- ID dokumen harus unik global lintas collection; ID block hanya unik di dalam dokumen pemilik.
- Relasi pada enam collection inti wajib memakai FK numerik ke ID dokumen target. Collection ekstensi secara default juga memakai FK numerik; natural key hanya boleh digunakan bila extension registry mendukung dan mendeklarasikan target, targetField, kardinalitas, serta keunikan/stabilitas target. Satu relasi hanya boleh memiliki satu sumber kebenaran; jangan menduplikasi FK dan natural key untuk relasi yang sama.
- Jangan membuat schema.org yang tidak didukung konten terlihat atau menjanjikan rich result tanpa memeriksa kebijakan terbaru.
- Setiap perubahan standar harus memperbarui versi dokumen terkait, `CHANGELOG.md`, dan status/bukti pada `docs/REVIEW-NOTES.md`.
- Perubahan implementasi harus menyertakan atau memperbarui pengujian yang relevan.

## Dokumentasi dan komunikasi
- Gunakan Bahasa Indonesia yang jelas untuk dokumen standar, kecuali istilah teknis yang lebih tepat dipertahankan dalam bahasa Inggris.
- Bedakan aturan universal, pilihan arsitektur, dan keputusan khusus proyek.
- Jangan menandai checklist selesai hanya karena file ditulis; sertakan bukti dan hasil verifikasi yang benar-benar dilakukan.

## Saat memulai repository situs baru
- Salin dan gunakan paket [Project Architecture Templates](projects/_template/README.md) sebagai kerangka dokumen arsitektur proyek.
- Lengkapi keputusan yang relevan sebelum implementasi; tandai bagian yang tidak berlaku beserta alasannya, jangan memaksakan fitur.
- Jangan menganggap template sebagai aturan universal baru. Constitution, Content Contract, IA, Technical Architecture, dan Quality Gates tetap menjadi acuan normatif.
- Jangan menandai dokumen arsitektur Approved sebelum keputusan kritis, asumsi berisiko, pemilik, dan bukti persetujuan jelas.


## Workflow inisialisasi proyek
- Ikuti [Project Initialization Workflow](projects/_template/PROJECT-INITIALIZATION-WORKFLOW.md) saat memulai proyek situs baru.
- Selesaikan baseline repository dan phase discovery sebelum menyusun keputusan arsitektur atau membuat implementasi.
- Jangan melewati phase gate yang menjadi prasyarat; status Approved/Ready memerlukan artefak, pemeriksaan, dan persetujuan nyata.
- Jika bukti baru membatalkan keputusan, kembali ke phase terdampak dan perbarui artefak terkait.
- Implementasi normal baru dimulai setelah Implementation Readiness Review disetujui. Prototipe yang diminta lebih awal harus dibatasi dan diberi label eksperimen.
