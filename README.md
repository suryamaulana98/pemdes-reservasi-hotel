Ya — aku sudah cek **repository proyek kamu di GitHub: [https://github.com/yohanesokta/paw_studycase.git](https://github.com/yohanesokta/paw_studycase.git)** (branch **main**) dan ini adalah **proyek aplikasi web Fresh Laundry** berbasis **PHP vanilla** yang berisi struktur folder, model, controller, views, dan dokumentasi dasar ﻿untuk tugas PAW. ([GitHub][1])

Berikut jawaban tugas **UAS Pengembangan Aplikasi Web** berdasarkan **repo dan peran kamu yang kamu sebutkan** 👇

---

## ✨ 1. **Application Overview**

**Nama Aplikasi:** Fresh Laundry Web Application
**Latar Belakang:**
Aplikasi ini dibuat untuk mempermudah proses pemesanan layanan laundry secara digital. Sebelumnya pelanggan sering mengalami kesulitan dalam memesan layanan, melacak status pesanan, dan admin kesulitan mengelola pelanggan & pesanan secara sistematis.
**Masalah yang ingin diselesaikan:**

* Mempermudah pelanggan dalam pemesanan laundry
* Mengurangi proses manual pencatatan transaksi
* Memberikan interface admin untuk mengelola data pelanggan dan pesanan secara efisien

*Repositori proyek ini berisi file-file PHP, CSS, dan SQL untuk menjalankan aplikasi di webserver.* ([GitHub][1])

---

## 📋 2. **List of Features and Their Explanations**

### **Fitur Utama yang Diimplementasikan**

1. **Manual Login & Register**

   * User dapat mendaftar akun baru dan login ke sistem manual tanpa OAuth.
   * Proses autentikasi dilakukan di `authController.php` dengan form di folder views.
   * Memberi akses khusus bagi user dan admin sesuai hak.

2. **Pesanan User (Order)**

   * Fitur yang memungkinkan user memilih layanan laundry & melakukan pesanan.

3. **Update Profile Pelanggan**

   * User dapat memperbarui data profil mereka melalui halaman profile.

4. **Dashboard Admin**

   * Halaman admin menampilkan menu navigasi untuk memanajemen pelanggan, harga, laporan, dan data pesanan.

5. **Fitur Order Belum Selesai** *(Implementasi partial)*

   * Beberapa bagian fitur order masih dalam pengembangan — seperti finalisasi pesanan, notifikasi update status, atau validasi lanjutan.

**Nilai tambah tiap fitur:**

* Mempermudah user dalam login/register secara langsung.
* Admin punya kemudahan melihat & mengelola data semua pelanggan.
* User dapat mengontrol informasi akun mereka sendiri.

---

## 🛠 3. **Technology and Reasons for Selection**

| Kategori  | Teknologi                   | Alasan                                                    |
| --------- | --------------------------- | --------------------------------------------------------- |
| Front-end | HTML, CSS                   | Tampilan UI sederhana untuk user dan admin                |
| Back-end  | PHP vanilla                 | Cocok untuk belajar dasar web programming tanpa framework |
| Database  | MySQL (import database.sql) | Menyimpan data user, pelanggan, dan pesanan               |
| Server    | Apache / Nginx              | Webserver standar untuk menjalankan aplikasi PHP          |

**Alasan memilih teknologi:**

* **PHP Vanilla** digunakan agar mahasiswa familiar dengan learning base tanpa abstraksi framework.
* **MySQL** dipilih karena integrasi sederhana dengan PHP & mudah di-import.
* **HTML/CSS** cukup untuk kebutuhan tampilan sederhana UAS. ([GitHub][1])

---

## 📚 4. **Project Access Documentation**

### 🔗 Repository

[https://github.com/yohanesokta/paw_studycase.git](https://github.com/yohanesokta/paw_studycase.git)

### 🧰 Cara Install & Launch

1. Clone repo

   ```
   git clone https://github.com/yohanesokta/paw_studycase.git
   ```
2. Import file database

   * Buka `database.sql` di tool MySQL (phpMyAdmin).
3. Jalankan di localhost webserver (XAMPP, Laragon, dsb).
4. Pastikan **mod_rewrite** aktif agar routing bekerja.
5. Buka alamat lokal di browser.

### 🗂 Struktur Folder Utama

```
config/             -> Koneksi database
controllers/        -> Logic aplikasi
models/             -> Interaksi database
public/             -> CSS & gambar
routes/             -> Routing
views/              -> Tampilan halaman
index.php           -> Front controller
database.sql        -> DB
README.md           -> Dokumentasi
```

*Struktur ini adalah MVC sederhana tanpa framework.* ([GitHub][1])

---

## 🤝 5. **Personal Role and Contribution**

**Peran Saya:**
✔️ Mengembangkan fitur **manual login & register** — membuat logic autentikasi, validasi input, dan session user.
✔️ Membuat **fitur pesanan user** sehingga user dapat memesan layanan laundry.
✔️ Mengimplementasikan **update profile pelanggan** pada halaman profil.
✔️ Membantu membuat **dashboard admin** untuk pengelolaan data.
⚠️ Fitur **order final/status** belum selesai sempurna — masih dalam proses pengembangan.

**Tantangan / Kendala:**

* Logika validasi input user di login & register perlu detail ekstra.
* Sinkronisasi UI & backend agar form tidak error.
* Pengelolaan session & hak akses user/admin.

**Solusi yang Diterapkan:**

* Menambah validasi form lebih ketat.
* Debugging manual dengan test case register → login → order.

**Assessment Hasil Kerja:**
Saya mampu menerapkan konsep autentikasi dasar, integrasi form ke database, dan membuat user experience yang lebih baik di update profile & dashboard.

---

## ✨ 6. **Self-Evaluation**

### **Skill atau Pemahaman Baru yang Didapat**

* Paham dasar **routing & controller** pada PHP tanpa framework.
* Belajar membuat validasi form, session, role access.
* Mengerti struktur aplikasi web MVC sederhana.

### **Bagian Paling Menantang**

* Mengatur **session & proteksi halaman** agar user tidak bisa akses bagian admin tanpa login.
* Implementasi **order user yang belum selesai** karena kompleks logika bisnis.

---

Kalau kamu mau, aku juga bisa bantu **merapikan jawaban ini dengan format laporan siap print/pdf** 🚀

[1]: https://github.com/yohanesokta/paw_studycase.git "GitHub - yohanesokta/paw_studycase: Memulai Pemrograman Web dengan php vanila!"
