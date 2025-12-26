<img width="1919" height="1005" alt="Algoritma Gambar Lingkaran dan Polygon" src="https://github.com/user-attachments/assets/fc45f535-6d6e-4600-a1ab-2012fab49193" />
Program ini menampilkan tiga algoritma dasar grafika komputer menggunakan modul turtle di Python. Program menggambar garis, lingkaran, dan poligon dengan pendekatan titik demi titik (pixel-based drawing).
1. Fungsi Bantuan
   setup_turtle() menyiapkan objek turtle dengan kecepatan maksimum dan menyembunyikan kursor.
   draw_pixel() menggambar satu titik (dot) di koordinat (x, y) dengan warna tertentu.
2. Algoritma DDA (WARNA BIRU)
   Menggambar garis dari (x1, y1) ke (x2, y2) dengan menghitung pertambahan kecil (x_inc, y_inc) pada tiap langkah.
   Setiap titik hasil perhitungan digambar secara bertahap untuk memperlihatkan proses pembentukan garis.
3. Algoritma Midpoint Circle (WARNA MERAH)
   Menggambar lingkaran menggunakan prinsip simetri delapan titik (8-way symmetry).
   Variabel p digunakan sebagai parameter keputusan (decision parameter) untuk menentukan posisi piksel berikutnya.
4. Polygon (Menggunakan DDA) (WARNA HIJAU)
   Menggambar bentuk poligon tertutup segitiga dengan cara menghubungkan setiap titik menggunakan algoritma DDA.
