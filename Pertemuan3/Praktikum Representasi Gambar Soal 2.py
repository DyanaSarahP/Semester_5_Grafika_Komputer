# Program menggambar garis dari (0,0) ke (5,3)

x1, y1 = 0, 0
x2, y2 = 5, 3

dx = x2 - x1
dy = y2 - y1
steps = max(abs(dx), abs(dy))

x_inc = dx / steps
y_inc = dy / steps

x = x1
y = y1

print("Titik-titik garis dari (0,0) ke (5,3):")
for i in range(steps + 1):
    print(f"({round(x)}, {round(y)})")
    x += x_inc
    y += y_inc
