# Office Asset Loan (`office_asset_loan`)

Custom module Odoo Community Edition 19.0 untuk mencatat inventaris kantor dan peminjamannya, supaya jelas siapa yang membawa barang apa, tidak ada barang dipinjam ganda, dan peminjaman yang lewat tenggat mudah terlihat.

## Versi Odoo
Odoo Community Edition 19.0

## Fitur
- Pencatatan inventaris kantor (kode unik, kategori, kondisi, catatan, archive).
- Nomor peminjaman otomatis (LOAN/0001, LOAN/0002, dst).
- Alur status peminjaman: Draft, Borrowed, Returned, Cancelled.
- Validasi tanggal: tenggat tidak boleh lebih awal dari tanggal pinjam.
- Aset yang sedang dipinjam atau berkondisi rusak tidak bisa dipinjam.
- Peminjaman berstatus Borrowed atau Returned tidak bisa dihapus.
- Tab Loan History pada form aset.
- Hak akses untuk Internal User.

## Cara Instalasi
1. Salin folder `office_asset_loan` ke dalam folder addons Odoo.
2. Tambahkan path addons tersebut di `odoo.conf` (`addons_path`).
3. Jalankan Odoo, lalu buka menu **Apps** dan klik **Update Apps List**.
4. Cari **Office Asset Loan**, lalu klik **Install**.

## Screenshot

### List Peminjaman
![List Peminjaman](screenshots/list-peminjaman.png)

### Form Peminjaman (Status Borrowed)
![Form Peminjaman](screenshots/form-borrowed.png)

### Form Aset
![Form Aset](screenshots/form-aset.png)

## Author
Sri Wulan Novera