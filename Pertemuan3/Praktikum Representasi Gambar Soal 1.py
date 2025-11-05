# Program Grid 10x10
lebar = 10
tinggi = 10

for y in range(tinggi):
    for x in range(lebar):
        if x == 4 and y == 6:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
