# 🌀 Algoritma DDA, Midpoint Circle, dan Polygon  
### 🧩 Hasil

<img width="1000" alt="Algoritma Gambar Lingkaran dan Polygon" src="https://github.com/user-attachments/assets/fc45f535-6d6e-4600-a1ab-2012fab49193" />

---

## 📘 Deskripsi Program
Program ini menampilkan **tiga algoritma dasar grafika komputer** menggunakan modul **`turtle`** di Python.  
Program menggambar **garis, lingkaran, dan poligon** secara **titik demi titik (pixel-based drawing)** untuk memperlihatkan proses pembentukannya.

---

## 🧩 1. Fungsi Bantuan
🔹 **`setup_turtle()`**  
Menyiapkan objek `turtle` dengan kecepatan maksimum (`speed(0)`) dan menyembunyikan kursor agar fokus pada gambar.  

🔹 **`draw_pixel(x, y, color)`**  
Menggambar satu titik (`dot`) pada koordinat `(x, y)` dengan warna tertentu.

---

## 🔵 2. Algoritma DDA (Digital Differential Analyzer)
**Warna:** Biru 💙  
Algoritma ini digunakan untuk menggambar **garis lurus** dari `(x1, y1)` ke `(x2, y2)` dengan menghitung:
- Selisih `dx` dan `dy`
- Nilai pertambahan kecil (`x_inc`, `y_inc`) setiap langkah
- Setiap titik hasil perhitungan digambar bertahap untuk memperlihatkan **proses pembentukan garis**

📈 **Konsep Utama:** Incremental plotting berdasarkan slope garis.

---

## 🔴 3. Algoritma Midpoint Circle
**Warna:** Merah ❤️  
Algoritma ini menggambar **lingkaran** berdasarkan prinsip **simetri delapan titik (8-way symmetry)**.  
Menggunakan **parameter keputusan `p`** untuk menentukan titik piksel berikutnya apakah bergerak ke timur atau tenggara.  

⚙️ **Konsep Utama:** Perhitungan efisien tanpa trigonometri, hanya menggunakan operasi penjumlahan.

---

## 🟢 4. Polygon (Menggunakan DDA)
**Warna:** Hijau 💚  
Menggambar **bentuk poligon segitiga tertutup** dengan menghubungkan tiga titik menggunakan algoritma **DDA Line**.  
Setiap sisi segitiga dibuat dengan perhitungan inkremental titik per titik.

🔺 **Konsep Utama:** Kombinasi garis DDA untuk membentuk bidang poligon tertutup.

---

## 💡 Kesimpulan
Melalui program ini, dapat memahami tiga algoritma penting :
1. DDA → pembuatan garis lurus  
2. Midpoint Circle → pembuatan lingkaran efisien  
3. DDA Polygon → konstruksi bentuk tertutup dari garis-garis dasar  

---
