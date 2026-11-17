# Office Asset Loan

**Odoo Community Edition 19.0**  
Custom module untuk mencatat inventaris kantor dan peminjaman internal secara praktis, terstruktur, dan akurat.

---

## 1. Deskripsi Modul
Modul `office_asset_loan` dirancang untuk mempermudah pencatatan inventaris bersama di kantor kecil (seperti proyektor, laptop cadangan, kamera, kabel roll, dll) serta riwayat peminjamannya oleh staf/karyawan internal. Modul ini mengatasi kendala pencatatan manual (via chat/buku) seperti:
- Ketidakjelasan siapa yang sedang memegang suatu barang.
- Barang dipinjam ganda pada waktu yang bersamaan.
- Tidak terpantaunya tenggat waktu pengembalian barang yang sudah lewat (*overdue*).

---

## 2. Fitur Utama
1. **Manajemen Data Inventaris Kantor (`office.asset`)**:
   - Kode aset unik (*SQL Constraint* `UNIQUE(code)`).
   - Kategori aset (*Electronics, Furniture, Vehicle, Other*).
   - Kondisi aset (*Good, Fair, Damaged*).
   - Status ketersediaan (*Available*) terhitung otomatis (*compute field*).
   - Riwayat peminjaman aset (*Loan History*) di form aset.
   - **(Bonus +3)** Smart button **Loans** di form aset dengan *counter* dan akses langsung ke daftar peminjaman.

2. **Manajemen Peminjaman Barang (`office.asset.loan`)**:
   - Penomoran otomatis berurutan (*Sequence* `LOAN/0001`, `LOAN/0002`, dst).
   - Peminjam (*Borrower*) default otomatis ke pengguna yang sedang login.
   - Validasi tenggat waktu (*Due Date* tidak boleh lebih awal dari *Loan Date*).
   - *Auto-fill Due Date* (+7 hari) jika tanggal pinjam diubah dan due date kosong.
   - Validasi ketersediaan dan kondisi barang saat peminjaman diajukan (*Borrow* ditolak jika barang rusak atau sedang dipinjam).
   - Tombol alur transaksi: **Borrow**, **Return** (otomatis isi return date), dan **Cancel**.
   - Proteksi data: peminjaman berstatus *Borrowed* atau *Returned* dilarang dihapus (*unlink protection*).
   - Status visual: Baris *Overdue* berwarna merah (*danger*) dan baris *Returned/Cancelled* redup (*muted*).
   - **(Bonus +3)** Filter **Overdue** pada Search View peminjaman.
   - **(Bonus +2)** Record Rule keamanan: User biasa hanya melihat peminjaman miliknya sendiri, sedangkan Administrator melihat seluruh peminjaman.
   - **(Bonus +2)** Data demo (`demo/`) berisi minimal 3 aset dan 3 transaksi peminjaman.

---

## 3. Aturan Bisnis (Business Rules)
- **BR-1**: Kode aset unik (`models.Constraint('UNIQUE(code)', ...)`).
- **BR-2**: `due_date` tidak boleh lebih awal dari `loan_date` (`@api.constrains`).
- **BR-3**: Penomoran otomatis `LOAN/XXXX` saat record dibuat (`create()` dengan `@api.model_create_multi`).
- **BR-4**: Tombol *Borrow* hanya aktif di status *Draft*. Validasi aset tidak rusak (*damaged*) dan tidak sedang dipinjam.
- **BR-5**: Tombol *Return* hanya aktif di status *Borrowed*. Mengisi `return_date` dengan hari ini dan status menjadi *Returned*.
- **BR-6**: Tombol *Cancel* hanya aktif di status *Draft*. Mengubah status menjadi *Cancelled*.
- **BR-7**: Record berstatus *Borrowed* atau *Returned* dilarang dihapus (`@api.ondelete`).
- **BR-8**: Saat `loan_date` diubah dan `due_date` kosong atau lebih awal, otomatis diset `loan_date + 7 hari` (`@api.onchange`).

---

## 4. Cara Instalasi & Menjalankan

### Cara 1: Menjalankan Tanpa Terminal (Menggunakan File `.json` di VS Code)
Modul ini sudah dilengkapi konfigurasi `.vscode/launch.json` dan `.vscode/tasks.json` sehingga Anda **tidak perlu mengetik perintah terminal secara manual**.

#### Menggunakan Run & Debug (F5) - `launch.json`:
1. Buka folder kerja `C:\odoo` di VS Code.
2. Buka tab **Run and Debug** di sidebar kiri (atau tekan `Ctrl+Shift+D`).
3. Pilih konfigurasi dari dropdown:
   - **Odoo: Start Server**: Menjalankan server Odoo dengan konfigurasi `odoo.conf`.
   - **Odoo: Update Module (office_asset_loan)**: Menjalankan server sekaligus auto-reload modul `office_asset_loan`.
   - **Odoo: Install Module (office_asset_loan)**: Menginstal modul `office_asset_loan` pada database.
4. Tekan tombol hijau **Play** atau tekan `F5` (untuk debug) / `Ctrl+F5` (run without debugging).

#### Menggunakan Task Runner - `tasks.json`:
1. Tekan kombinasi tombol `Ctrl+Shift+B` (Default Build Task) untuk langsung menjalankan server Odoo.
2. Atau buka menu atas: **Terminal -> Run Task...** lalu pilih:
   - `Odoo: Start Server`
   - `Odoo: Update Module (office_asset_loan)`

---

### Cara 2: Instalasi Melalui Tampilan Web Odoo (UI)
1. Buka browser dan akses `http://localhost:8069`.
2. Login sebagai Administrator.
3. Masuk ke menu **Apps**.
4. Aktifkan **Developer Mode** (dari Settings atau tambahkan `?debug=1` pada URL).
5. Klik menu **Update Apps List** dan konfirmasi Update.
6. Cari modul **Office Asset Loan** pada kolom pencarian (hapus filter *Apps* jika perlu).
7. Klik tombol **Activate** / **Install**.

---

## 5. Tangkapan Layar (Screenshots)
*(Sertakan tangkapan layar sistem berikut saat demonstrasi / publikasi)*

1. **List Peminjaman (`office.asset.loan`)**:
   ![List Loans](static/description/screenshot_loans_list.png)
   *Menampilkan daftar peminjaman dengan dekorasi warna (merah untuk overdue, redup untuk returned).*

2. **Form Peminjaman Berstatus Borrowed**:
   ![Form Loan Borrowed](static/description/screenshot_loan_borrowed.png)
   *Menampilkan status Borrowed, tombol Return aktif, dan seluruh field transaksi berstatus read-only.*

3. **Form Aset (`office.asset`)**:
   ![Form Asset](static/description/screenshot_asset_form.png)
   *Menampilkan detail aset, status ketersediaan, smart button Loans, serta tab Loan History.*

---

## 6. Struktur Modul
```text
office_asset_loan/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── office_asset.py
│   └── office_asset_loan.py
├── security/
│   ├── ir.model.access.csv
│   └── office_asset_loan_security.xml
├── data/
│   └── office_asset_loan_sequence.xml
├── demo/
│   └── office_asset_loan_demo.xml
├── views/
│   ├── office_asset_views.xml
│   ├── office_asset_loan_views.xml
│   └── office_asset_menus.xml
└── README.md
```

---

## 7. Kepatuhan Standar Odoo 19 CE
- Menggunakan tag `<list>` (bukan `<tree>`) dan `view_mode="list,form"`.
- Menggunakan ekspresi Python langsung pada `invisible="..."` dan `readonly="..."` (tidak menggunakan `attrs` atau `states`).
- Menggunakan `models.Constraint` untuk SQL Constraint (bukan `_sql_constraints`).
- Menggunakan decorator `@api.model_create_multi` dengan `vals_list` pada `create()`.
- Menggunakan decorator `@api.ondelete(at_uninstall=False)` untuk proteksi hapus record.
- Menggunakan `Command` helper API untuk manipulasi record Many2many / One2many.
- Mengikuti panduan PEP8 dan kaidah pemrograman Odoo 19 CE.

