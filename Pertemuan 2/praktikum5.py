# a. Buat list berisi tiga pasangan titik dan tampilkan dengan for
titik_list = [(0, 0), (50, 50), (100, 0)]

print("Daftar titik:")
for titik in titik_list:
    print(titik)

# b. Simpan satu titik dalam tuple bernama 'pusat' dan tampilkan nilainya
pusat = (0, 0)
print("\nTitik pusat:", pusat)

# c. Buat dictionary berisi atribut objek dan tampilkan format teks
objek = {"x": 10, "y": 20, "warna": "biru"}
print(f"\nTitik ({objek['x']},{objek['y']}) berwarna {objek['warna']}.")
