# 🚀 Platformer - Transformasi 2D (Luar Angkasa)

Proyek ini adalah implementasi **Grafika Komputer** menggunakan **Python + Pygame**.  
Game ini bertema **luar angkasa**, di mana pemain (astronaut) dapat melakukan berbagai **transformasi 2D** seperti **translasi, rotasi, scaling, dan refleksi (mirror)** secara interaktif.

---

## 🪐 Tampilan Game
<img width="1496" height="1006" alt="GameLuarAngkasa" src="https://github.com/user-attachments/assets/8989c133-e48f-43a9-8bad-a86390b189be" />

---

## 🧠 Konsep Grafika yang Digunakan
Proyek ini mengimplementasikan berbagai **konsep dasar grafika komputer**, antara lain:

| Konsep Grafika | Implementasi |
|----------------|---------------|
| 🎯 **Translasi** | Gerakan karakter dan elemen (dash ke kanan, lompat, jatuh) |
| 🔄 **Rotasi** | Aksi serangan (spin attack) dan animasi rotasi portal |
| 🔍 **Scaling** | Efek power-up yang memperbesar karakter sementara |
| 🪞 **Refleksi (Mirror)** | Pemindahan ke dunia dimensi alternatif (mirror world) |
| 🌌 **Animasi Grafika** | Efek bintang berkelap-kelip, portal berputar, dan planet dengan highlight |
| 🧱 **Rendering 2D** | Menggambar objek seperti planet, meteor, karakter, dan kristal secara manual menggunakan koordinat piksel |

---

## ⚙️ c. Algoritma yang Dipakai
| Algoritma | Fungsi |
|------------|--------|
| **Transformasi Translasi** | Menggeser objek secara horizontal dan vertikal |
| **Rotasi Titik 2D** | Memutar karakter dan elemen berdasarkan pusat rotasi |
| **Scaling (Perbesaran/Pengecilan)** | Mengubah ukuran karakter saat mengambil power-up |
| **Refleksi terhadap Sumbu Y** | Membalik tampilan dunia menjadi “mirror world” |
| **Perhitungan Vektor dan Kolisi** | Menentukan arah dan tabrakan antar objek dalam permainan |
| **Efek Twinkling (Sinusoidal)** | Memberikan efek berkilau pada bintang di latar belakang |

---

## 🕹️ d. Cara Menjalankan Program
1. Pastikan **Python 3** dan **Pygame** sudah terinstal
2. Simpan file
3. Jalankan program
4. Gunakan 🎮 Kontrol Permainan

| 🎮 **Tombol** | 🧭 **Fungsi** |
|----------------|----------------|
| `A / D` atau `← / →` | Bergerak ke kiri / kanan |
| `W / ↑ / SPACE` | Melompat |
| `E` | Dash — Translasi cepat ke depan |
| `Q` | Serangan berputar (Rotasi) |
| `H` | Menampilkan atau menyembunyikan instruksi |
| 🌌 **Masuki Portal** | Berpindah ke dunia cermin (Refleksi sumbu-Y) |
)

---
