
## a. Judul Proyek
# 🎮 3D Tetris Sequential – 4 Transformasi

<img width="840" height="579" alt="blok3d" src="https://github.com/user-attachments/assets/15e89caf-00b1-4717-bdc3-21d09bd2c04d" />

---

<img width="1911" height="1072" alt="gameblok" src="https://github.com/user-attachments/assets/ecde1102-4c48-4a86-aec1-a6cab9cdfeab" />

---

## b. Konsep Grafika yang Digunakan
Game ini merupakan permainan **Tetris 3D** yang dirancang untuk menerapkan dan mendemonstrasikan konsep dasar **grafika komputer tiga dimensi**. Blok-blok 3D jatuh secara **berurutan setiap 3 detik**, di mana pemain harus menyelesaikan pengaturan satu blok sebelum blok berikutnya muncul.

Konsep grafika komputer yang diterapkan dalam game ini meliputi:
- **Transformasi Translasi**, untuk memindahkan blok ke berbagai arah dalam ruang 3D.
- **Transformasi Rotasi**, untuk memutar blok pada sumbu X, Y, dan Z.
- **Transformasi Skala**, untuk memperbesar atau memperkecil ukuran blok.
- **Transformasi Refleksi**, untuk mencerminkan blok terhadap sumbu tertentu.
- **Sistem Koordinat 3D**, ditampilkan dengan sumbu X (merah), Y (hijau), dan Z (biru).
- **Grid 3D**, sebagai bidang referensi posisi dan pendaratan blok.
- **Highlight Objek Aktif**, ditandai dengan border kuning agar pemain mudah mengenali blok yang sedang dikendalikan.

Game ini juga menampilkan informasi akhir seperti **score**, **jumlah blok**, dan **blok yang berhasil mendarat**, sehingga pemain dapat mengevaluasi hasil permainan.

---

## c. Cara Menjalankan Program
1. Pastikan environment grafika komputer yang dibutuhkan telah terpasang (misalnya OpenGL/GLUT atau library grafika 3D yang digunakan).
2. Buka folder proyek.
3. Jalankan file program utama.
4. Setelah game berjalan, gunakan kontrol berikut:

### 🎮 Kontrol Game
- **Translasi**  
  `A / W / S / D / Q / E`
- **Rotasi**  
  `I / K`, `J / L`, `U / O`
- **Skala**  
  `+ / -`
- **Refleksi**  
  `1 / 2 / 3`
- **Drop cepat**  
  `SPACE`
- **Toggle panduan**  
  `H`

5. Atur satu blok hingga selesai, lalu blok berikutnya akan muncul otomatis setiap **3 detik**.
6. Game akan berakhir setelah seluruh blok selesai diproses dan menampilkan hasil akhir permainan.

---

Game ini dibuat sebagai media pembelajaran untuk memahami **transformasi geometri 3D** melalui implementasi langsung dalam sebuah permainan interaktif.
