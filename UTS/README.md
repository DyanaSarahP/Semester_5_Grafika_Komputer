# 🧱 Brick Breaker – UTS Grafika Komputer  
### 🎮 Penerapan Transformasi 2D & Algoritma Grafika Komputer

Sebuah **game interaktif bertema paddle dan bola**, yang menampilkan penerapan **transformasi 2D** dan **algoritma grafika komputer dasar** menggunakan **Python (Tkinter)**.  
Game ini melatih pemahaman konsep **pergerakan, pantulan, dan perubahan bentuk objek grafis** dalam sistem koordinat dua dimensi.

---
# 🖼️ Tampilan Game

<img width="900" alt="GameBrickBreaker" src="https://github.com/user-attachments/assets/df015d38-7aa5-4ff0-8b35-c41008613059" />

📸 **Deskripsi Tampilan:**  
Game menampilkan area permainan dengan **bata berwarna-warni**, **bola berputar yang memantul**, serta **paddle** yang dapat **berubah ukuran** saat memperoleh power-up.  
Efek visual sederhana diterapkan untuk **pantulan bola**, **perubahan skala paddle**, dan **animasi power-up** yang jatuh.

---

## 🧠 Konsep Grafika yang Digunakan
Game ini menerapkan **empat transformasi geometris 2D** utama:

| 🔢 Transformasi | 🧭 Penjelasan |
|-----------------|---------------|
| **Translasi** | Menggerakkan objek (bola & paddle) ke arah tertentu. |
| **Rotasi** | Memutar paddle dan bola saat mengenai objek. |
| **Scaling (Skala)** | Memperbesar atau memperkecil paddle saat mendapat power-up. |
| **Refleksi (Mirror)** | Mengubah arah pantulan bola saat menabrak dinding, paddle, atau bata. |

---

## ⚙️ Algoritma yang Digunakan
Selain transformasi 2D, game ini juga mengimplementasikan **dua algoritma dasar grafika komputer** untuk menggambar objek secara manual (pixel-based drawing).

| 🧩 Algoritma | 🧠 Fungsi |
|--------------|-----------|
| **DDA (Digital Differential Analyzer)** | Menggambar **garis batas (border)** area permainan secara bertahap titik demi titik. |
| **Midpoint Circle Algorithm** | Menggambar **bola (circle)** menggunakan pendekatan simetri 8 titik. |
| **Transformasi 2D** | Menerapkan translasi, rotasi, scaling, dan refleksi pada objek dinamis. |
| **Refleksi Vektor** | Mengatur arah **pantulan bola** secara realistis terhadap dinding, paddle, dan bata. |

---

## ⚙️ Cara Menjalankan Program

| 🔢 **Langkah** | 🧭 **Keterangan** |
|----------------|------------------|
| 1️⃣ | Pastikan **Python 3** sudah terinstal. |
| 2️⃣ | Simpan file sesuai nama proyekmu. |
| 3️⃣ | Buka **terminal / command prompt** di lokasi file tersebut. |
| 4️⃣ | Jalankan perintah berikut untuk memulai game: <br> ```python brick_breaker.py``` |

---

## 🎮 Kontrol Permainan

| 🎮 **Tombol** | 🧭 **Fungsi** |
|----------------|----------------|
| 🖱️ **Mouse** | Menggerakkan paddle ke kiri dan kanan |
| ⌨️ **SPACE** | Memulai permainan |
| 🔄 **Q / E** | Memutar paddle ke kiri / kanan |
| ⚖️ **A / D** | Memperkecil / memperbesar paddle (**Scaling**) |

---

## 💡 Kesimpulan

Melalui proyek ini, dapat memahami dan menerapkan berbagai konsep penting antara lain:

- 🧭 **Transformasi 2D**: Translasi, Rotasi, Scaling, dan Refleksi diterapkan pada objek permainan.  
- 🧮 **Algoritma DDA & Midpoint Circle**: Digunakan untuk menggambar garis dan lingkaran secara manual (pixel-based).  
- 🎮 **Interaksi & Animasi 2D**: Menciptakan game sederhana dengan elemen dinamis melalui modul **Tkinter** di Python.  

---
