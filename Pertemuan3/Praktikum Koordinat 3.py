print("=== Simulasi Sistem Koordinat 10x5 ===")

lebar = 10
tinggi = 5

# Titik yang ingin ditampilkan
x_target = 3
y_target = 2

for y in range(tinggi):
    for x in range(lebar):
        if x == x_target and y == y_target:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
