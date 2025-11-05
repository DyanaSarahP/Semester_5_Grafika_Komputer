import matplotlib.pyplot as plt

# Titik awal dan akhir
x1, y1 = 0, 0
x2, y2 = 5, 3

# Hitung jumlah langkah berdasarkan perbedaan terbesar
steps = max(abs(x2 - x1), abs(y2 - y1))

# Hitung perubahan tiap langkah
dx = (x2 - x1) / steps
dy = (y2 - y1) / steps

# Inisialisasi titik awal
x = x1
y = y1

# Simpan koordinat untuk digambar
x_points = []
y_points = []

# Hitung semua titik koordinat pada garis
for i in range(steps + 1):
    x_points.append(round(x, 2))
    y_points.append(round(y, 2))
    x += dx
    y += dy

# Tampilkan daftar titik di terminal
print("Titik-titik koordinat garis dari (0,0) ke (5,3):")
for i in range(len(x_points)):
    print(f"({x_points[i]}, {y_points[i]})")

# --- Gambar garis menggunakan matplotlib ---
plt.figure(figsize=(5, 4))
plt.plot(x_points, y_points, marker='o', color='blue')
plt.title("Garis dari (0,0) ke (5,3)")
plt.xlabel("Sumbu X")
plt.ylabel("Sumbu Y")
plt.grid(True)
plt.axis("equal")  # agar proporsi X dan Y sama
plt.show()
