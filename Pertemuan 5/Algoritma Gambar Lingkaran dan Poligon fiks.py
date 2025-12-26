import turtle
import time

# =============================
# 🧩 FUNGSI BANTUAN
# =============================
def setup_turtle():
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    turtle.delay(5)
    return t

def draw_pixel(t, x, y, color="black"):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.dot(3, color)


# =====================================================
# 1️⃣  ALGORITMA DDA (Digital Differential Analyzer)
# =====================================================
def dda_line(t, x1, y1, x2, y2, color="blue"):
    dx = x2 - x1
    dy = y2 - y1
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)
    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1
    for i in range(int(steps) + 1):
        draw_pixel(t, round(x), round(y), color)
        time.sleep(0.002)
        x += x_inc
        y += y_inc


# =====================================================
# 2️⃣  ALGORITMA MIDPOINT CIRCLE
# =====================================================
def midpoint_circle(t, xc, yc, r, color="red"):
    x = 0
    y = r
    p = 1 - r

    while x <= y:
        # 8 titik simetri
        draw_pixel(t, xc + x, yc + y, color)
        draw_pixel(t, xc - x, yc + y, color)
        draw_pixel(t, xc + x, yc - y, color)
        draw_pixel(t, xc - x, yc - y, color)
        draw_pixel(t, xc + y, yc + x, color)
        draw_pixel(t, xc - y, yc + x, color)
        draw_pixel(t, xc + y, yc - x, color)
        draw_pixel(t, xc - y, yc - x, color)

        time.sleep(0.002)
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1


# =====================================================
# 3️⃣  POLIGON (pakai DDA)
# =====================================================
def draw_polygon(t, points, color="green"):
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        dda_line(t, x1, y1, x2, y2, color)


# =====================================================
# 🎨  PROGRAM UTAMA — 1 jendela, posisi kiri-tengah-kanan
# =====================================================

turtle.title("Visualisasi Algoritma DDA, Midpoint Circle, dan Polygon")
t = setup_turtle()

# --- Posisi pusat tiap algoritma ---
offset_DDA = -300     # kiri
offset_MIDPOINT = 0   # tengah
offset_POLYGON = 300  # kanan

# --- DDA Line (kiri) ---
dda_line(t, offset_DDA - 100, 0, offset_DDA + 100, 0, "blue")

# --- Midpoint Circle (tengah) ---
midpoint_circle(t, offset_MIDPOINT, 0, 80, "red")

# --- Polygon (kanan) ---
segitiga = [
    (offset_POLYGON - 50, -50),
    (offset_POLYGON + 50, -50),
    (offset_POLYGON, 80)
]
draw_polygon(t, segitiga, "green")

# =====================================================
# 🏷️  Tambahkan Judul di Bawah Tiap Algoritma
# =====================================================
label = turtle.Turtle()
label.hideturtle()
label.penup()
label.color("black")

# Teks DDA
label.goto(offset_DDA - 70, -120)
label.write("Algoritma DDA Line", font=("Arial", 12, "bold"))

# Teks Midpoint Circle
label.goto(offset_MIDPOINT - 90, -120)
label.write("Algoritma Midpoint Circle", font=("Arial", 12, "bold"))

# Teks Polygon
label.goto(offset_POLYGON - 80, -120)
label.write("Algoritma Polygon (DDA)", font=("Arial", 12, "bold"))

turtle.done()
