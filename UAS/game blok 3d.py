"""
3D TETRIS / BLOCK STACKER
Game Tetris 3D dengan 4 Transformasi Lengkap:
1. TRANSLASI 3D - Geser blok kiri/kanan/depan/belakang
2. ROTASI 3D - Putar blok pada sumbu X, Y, Z
3. SKALA 3D - Perbesar/perkecil blok
4. REFLEKSI 3D - Mirror/flip blok pada sumbu tertentu

MODE BERURUTAN: Blok jatuh satu per satu setiap 3 detik!

Install library:
pip install pygame PyOpenGL PyOpenGL-accelerate
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

class Block:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reset blok ke posisi awal dengan bentuk random"""
        self.pos_x = random.choice([-3, -1, 0, 1, 3])
        self.pos_y = 18.0
        self.pos_z = random.choice([-3, -1, 0, 1, 3])
        self.rotation = [0, 0, 0]
        self.scale = [1.0, 1.0, 1.0]
        self.fall_speed = 0.03
        
        # Pilih bentuk random
        shapes = [
            ([[-0.5, 0, 0], [0.5, 0, 0], [1.5, 0, 0], [2.5, 0, 0]], "I Shape"),
            ([[-0.5, 0, 0], [0.5, 0, 0], [1.5, 0, 0], [1.5, 1, 0]], "L Shape"),
            ([[-0.5, 0, 0], [0.5, 0, 0], [1.5, 0, 0], [0.5, 1, 0]], "T Shape"),
            ([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]], "O Shape"),
            ([[-0.5, 0, 0], [0.5, 0, 0], [0.5, 1, 0], [1.5, 1, 0]], "Z Shape"),
            ([[0, 0, 0], [1, 0, 0], [-1, 0, 0], [0, 1, 0]], "+ Shape"),
            ([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], "3D Cube"),
        ]
        
        self.shape, self.shape_name = random.choice(shapes)
        
        self.color = (
            random.uniform(0.4, 1.0),
            random.uniform(0.4, 1.0),
            random.uniform(0.4, 1.0)
        )
        
        self.is_landed = False
        self.is_active = True
    
    def draw(self, is_current=False):
        """Gambar blok dengan transformasi"""
        glPushMatrix()
        
        # TRANSFORMASI 1: TRANSLASI 3D
        glTranslatef(self.pos_x, self.pos_y, self.pos_z)
        
        # TRANSFORMASI 2: ROTASI 3D
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # TRANSFORMASI 3: SKALA 3D
        glScalef(self.scale[0], self.scale[1], self.scale[2])
        
        # Gambar setiap kubus
        for cube_pos in self.shape:
            self.draw_cube(cube_pos[0], cube_pos[1], cube_pos[2], is_current)
        
        glPopMatrix()
    
    def draw_cube(self, x, y, z, is_current=False):
        """Gambar satu kubus kecil"""
        glPushMatrix()
        glTranslatef(x, y, z)
        
        size = 0.45
        vertices = [
            [-size, -size, -size], [size, -size, -size],
            [size, size, -size], [-size, size, -size],
            [-size, -size, size], [size, -size, size],
            [size, size, size], [-size, size, size]
        ]
        
        faces = [
            [0,1,2,3], [4,5,6,7], [0,1,5,4],
            [2,3,7,6], [0,3,7,4], [1,2,6,5]
        ]
        
        # Gambar faces
        for i, face in enumerate(faces):
            brightness = 0.7 + (i % 3) * 0.1
            if is_current and self.is_active:
                brightness *= 1.4  # Blok aktif lebih terang
            glColor3f(self.color[0] * brightness, 
                     self.color[1] * brightness, 
                     self.color[2] * brightness)
            glBegin(GL_QUADS)
            for vertex in face:
                glVertex3fv(vertices[vertex])
            glEnd()
        
        # Gambar edges
        if is_current and self.is_active:
            glColor3f(1, 1, 0)  # Kuning untuk blok aktif
            glLineWidth(4)
        else:
            glColor3f(0, 0, 0)
            glLineWidth(2)
            
        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
        
        glPopMatrix()
    
    def update(self):
        """Update posisi blok (jatuh otomatis)"""
        if not self.is_landed and self.is_active:
            self.pos_y -= self.fall_speed
            if self.pos_y <= 0:
                self.pos_y = 0
                self.is_landed = True
    
    # TRANSFORMASI 1: TRANSLASI 3D
    def move(self, dx, dy, dz):
        if not self.is_active or self.is_landed:
            return False
            
        new_x = self.pos_x + dx
        new_y = self.pos_y + dy
        new_z = self.pos_z + dz
        
        # Batasi area
        new_x = max(-5, min(5, new_x))
        new_z = max(-5, min(5, new_z))
        
        if dy < 0:
            new_y = max(0, new_y)
        else:
            new_y = min(20, new_y)
        
        self.pos_x = new_x
        self.pos_y = new_y
        self.pos_z = new_z
        
        if self.pos_y <= 0.1:
            self.pos_y = 0
            self.is_landed = True
        
        return True
    
    # TRANSFORMASI 2: ROTASI 3D
    def rotate(self, axis, angle):
        if not self.is_active or self.is_landed:
            return False
        if axis == 'x':
            self.rotation[0] = (self.rotation[0] + angle) % 360
        elif axis == 'y':
            self.rotation[1] = (self.rotation[1] + angle) % 360
        elif axis == 'z':
            self.rotation[2] = (self.rotation[2] + angle) % 360
        return True
    
    # TRANSFORMASI 3: SKALA 3D
    def change_scale(self, factor):
        if not self.is_active or self.is_landed:
            return False
        for i in range(3):
            self.scale[i] = max(0.3, min(2.5, self.scale[i] * factor))
        return True
    
    # TRANSFORMASI 4: REFLEKSI 3D
    def reflect(self, axis):
        if not self.is_active or self.is_landed:
            return False
        if axis == 'x':
            self.scale[0] *= -1
        elif axis == 'y':
            self.scale[1] *= -1
        elif axis == 'z':
            self.scale[2] *= -1
        return True

class Grid:
    def draw(self):
        # Grid lantai
        glColor3f(0.2, 0.2, 0.25)
        glLineWidth(1)
        glBegin(GL_LINES)
        for i in range(-5, 6):
            glVertex3f(i, 0, -5)
            glVertex3f(i, 0, 5)
            glVertex3f(-5, 0, i)
            glVertex3f(5, 0, i)
        glEnd()
        
        # Platform lantai
        glColor3f(0.12, 0.12, 0.18)
        glBegin(GL_QUADS)
        glVertex3f(-5.5, -0.1, -5.5)
        glVertex3f(5.5, -0.1, -5.5)
        glVertex3f(5.5, -0.1, 5.5)
        glVertex3f(-5.5, -0.1, 5.5)
        glEnd()
        
        # Dinding belakang
        glColor3f(0.08, 0.08, 0.12)
        glBegin(GL_QUADS)
        glVertex3f(-5.5, 0, -5.5)
        glVertex3f(5.5, 0, -5.5)
        glVertex3f(5.5, 20, -5.5)
        glVertex3f(-5.5, 20, -5.5)
        glEnd()
        
        # Border lantai
        glColor3f(0.4, 0.4, 0.5)
        glLineWidth(3)
        glBegin(GL_LINE_LOOP)
        glVertex3f(-5, 0.01, -5)
        glVertex3f(5, 0.01, -5)
        glVertex3f(5, 0.01, 5)
        glVertex3f(-5, 0.01, 5)
        glEnd()
        
        # Sumbu koordinat
        glLineWidth(4)
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0.05, 0)
        glVertex3f(3, 0.05, 0)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0.05, 0)
        glVertex3f(0, 3, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0.05, 0)
        glVertex3f(0, 0.05, 3)
        glEnd()

def draw_guide_panel(ui_surface, font_small, display):
    """Gambar panel panduan"""
    panel_x = display[0] - 420
    panel_y = display[1] - 420
    panel_w = 400
    panel_h = 400
    
    panel_rect = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel_rect.fill((20, 20, 30, 220))
    ui_surface.blit(panel_rect, (panel_x, panel_y))
    
    pygame.draw.rect(ui_surface, (100, 150, 255), (panel_x, panel_y, panel_w, panel_h), 2)
    
    y = panel_y + 15
    
    title = font_small.render("📚 PANDUAN KONTROL", True, (100, 200, 255))
    ui_surface.blit(title, (panel_x + 15, y))
    
    y += 35
    
    guides = [
        ("⏱️  Blok jatuh otomatis tiap 3 detik", (255, 255, 100)),
        ("🎯  Kontrol 1 blok sampai landed", (255, 255, 100)),
        ("", None),
        ("1️⃣  TRANSLASI 3D (Geser)", (255, 200, 100)),
        ("   A/D  → Kiri/Kanan", (220, 220, 220)),
        ("   W/S  → Depan/Belakang", (220, 220, 220)),
        ("   Q/E  → Naik/Turun", (220, 220, 220)),
        ("", None),
        ("2️⃣  ROTASI 3D (Putar)", (255, 200, 100)),
        ("   I/K  → Rotasi X", (220, 220, 220)),
        ("   J/L  → Rotasi Y", (220, 220, 220)),
        ("   U/O  → Rotasi Z", (220, 220, 220)),
        ("", None),
        ("3️⃣  SKALA 3D (Ukuran)", (255, 200, 100)),
        ("   +/-  → Besar/Kecil", (220, 220, 220)),
        ("", None),
        ("4️⃣  REFLEKSI 3D (Mirror)", (255, 200, 100)),
        ("   1/2/3 → Mirror X/Y/Z", (220, 220, 220)),
    ]
    
    for text, color in guides:
        if text == "":
            y += 8
        else:
            rendered = font_small.render(text, True, color)
            ui_surface.blit(rendered, (panel_x + 15, y))
            y += 22

def main():
    pygame.init()
    display = (1400, 900)
    
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('3D Tetris Sequential - 4 Transformasi')
    
    # Setup OpenGL
    glClearColor(0.05, 0.05, 0.12, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, display[0]/display[1], 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    # Font
    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 20)
    font_title = pygame.font.Font(None, 52)
    
    ui_surface = pygame.Surface(display, pygame.SRCALPHA)
    
    # Objek game
    grid = Grid()
    current_block = Block()  # Blok yang sedang aktif
    landed_blocks = []  # Blok yang sudah mendarat
    
    clock = pygame.time.Clock()
    score = 0
    total_blocks = 1
    
    # Camera
    camera_angle_y = 45
    camera_distance = 25
    
    # Movement delay
    move_delay = 100
    last_move_time = 0
    
    # Spawn timer
    spawn_timer = 0
    spawn_interval = 3000  # 3 detik
    
    show_guide = True
    
    print("=" * 70)
    print("🎮 3D TETRIS SEQUENTIAL - 4 TRANSFORMASI")
    print("=" * 70)
    print("⏱️  BLOK JATUH BERURUTAN SETIAP 3 DETIK!")
    print()
    print("🎯 Atur 1 blok sampai selesai, lalu blok berikutnya muncul")
    print("🟡 Blok aktif ditandai dengan BORDER KUNING")
    print()
    print("✅ 1. TRANSLASI : A/W/S/D/Q/E")
    print("✅ 2. ROTASI    : I/K, J/L, U/O")
    print("✅ 3. SKALA     : +/-")
    print("✅ 4. REFLEKSI  : 1/2/3")
    print()
    print("⌨️  SPACE : Drop cepat | H : Toggle panduan")
    print("=" * 70)
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        dt = clock.tick(60)
        
        # Update spawn timer jika blok sudah landed
        if current_block.is_landed:
            spawn_timer += dt
        
        # Spawn blok baru jika sudah waktunya
        if current_block.is_landed and spawn_timer >= spawn_interval:
            landed_blocks.append(current_block)
            current_block = Block()
            total_blocks += 1
            spawn_timer = 0
            print(f"\n🆕 Blok #{total_blocks} muncul! ({current_block.shape_name})")
            print(f"📦 Total blok landed: {len(landed_blocks)}")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Toggle panduan
                elif event.key == pygame.K_h:
                    show_guide = not show_guide
                
                # Drop cepat
                elif event.key == pygame.K_SPACE:
                    if current_block.pos_y > 0.5:
                        if current_block.move(0, -0.5, 0):
                            score += 1
                
                # ROTASI
                elif event.key == pygame.K_i:
                    if current_block.rotate('x', 15):
                        score += 2
                        print(f"🔄 Rotasi X: {current_block.rotation[0]:.0f}°")
                elif event.key == pygame.K_k:
                    if current_block.rotate('x', -15):
                        score += 2
                        print(f"🔄 Rotasi X: {current_block.rotation[0]:.0f}°")
                elif event.key == pygame.K_j:
                    if current_block.rotate('y', 15):
                        score += 2
                        print(f"🔄 Rotasi Y: {current_block.rotation[1]:.0f}°")
                elif event.key == pygame.K_l:
                    if current_block.rotate('y', -15):
                        score += 2
                        print(f"🔄 Rotasi Y: {current_block.rotation[1]:.0f}°")
                elif event.key == pygame.K_u:
                    if current_block.rotate('z', 15):
                        score += 2
                        print(f"🔄 Rotasi Z: {current_block.rotation[2]:.0f}°")
                elif event.key == pygame.K_o:
                    if current_block.rotate('z', -15):
                        score += 2
                        print(f"🔄 Rotasi Z: {current_block.rotation[2]:.0f}°")
                
                # SKALA
                elif event.key in [pygame.K_PLUS, pygame.K_EQUALS]:
                    if current_block.change_scale(1.2):
                        score += 3
                        print(f"📏 Skala: {current_block.scale[0]:.2f}x")
                elif event.key == pygame.K_MINUS:
                    if current_block.change_scale(0.8):
                        score += 3
                        print(f"📏 Skala: {current_block.scale[0]:.2f}x")
                
                # REFLEKSI
                elif event.key == pygame.K_1:
                    if current_block.reflect('x'):
                        score += 5
                        print("🪞 Refleksi X")
                elif event.key == pygame.K_2:
                    if current_block.reflect('y'):
                        score += 5
                        print("🪞 Refleksi Y")
                elif event.key == pygame.K_3:
                    if current_block.reflect('z'):
                        score += 5
                        print("🪞 Refleksi Z")
                
                # Kamera
                elif event.key == pygame.K_LEFT:
                    camera_angle_y += 5
                elif event.key == pygame.K_RIGHT:
                    camera_angle_y -= 5
                elif event.key == pygame.K_UP:
                    camera_distance = max(15, camera_distance - 2)
                elif event.key == pygame.K_DOWN:
                    camera_distance = min(40, camera_distance + 2)
        
        # TRANSLASI - Continuous movement
        keys = pygame.key.get_pressed()
        
        if current_time - last_move_time > move_delay:
            moved = False
            if keys[pygame.K_a]:
                if current_block.move(-0.5, 0, 0):
                    score += 1
                    moved = True
            if keys[pygame.K_d]:
                if current_block.move(0.5, 0, 0):
                    score += 1
                    moved = True
            if keys[pygame.K_w]:
                if current_block.move(0, 0, -0.5):
                    score += 1
                    moved = True
            if keys[pygame.K_s]:
                if current_block.move(0, 0, 0.5):
                    score += 1
                    moved = True
            if keys[pygame.K_q]:
                if current_block.pos_y < 19.5 and current_block.move(0, 0.5, 0):
                    score += 1
                    moved = True
            if keys[pygame.K_e]:
                if current_block.pos_y > 0.5 and current_block.move(0, -0.5, 0):
                    score += 1
                    moved = True
            
            if moved:
                last_move_time = current_time
        
        # Update blok aktif
        current_block.update()
        
        # === RENDER 3D ===
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Setup kamera
        cam_x = math.sin(math.radians(camera_angle_y)) * camera_distance
        cam_z = math.cos(math.radians(camera_angle_y)) * camera_distance
        gluLookAt(cam_x, 12, cam_z, 0, 5, 0, 0, 1, 0)
        
        # Gambar objek
        grid.draw()
        
        # Gambar blok landed
        for block in landed_blocks:
            block.draw(False)
        
        # Gambar blok aktif (dengan highlight)
        current_block.draw(True)
        
        # === RENDER UI ===
        ui_surface.fill((0, 0, 0, 0))
        
        # Title
        y = 20
        title = font_title.render("3D TETRIS", True, (0, 255, 255))
        ui_surface.blit(title, (20, y))
        
        y += 60
        mode_text = font_small.render("SEQUENTIAL MODE", True, (255, 200, 100))
        ui_surface.blit(mode_text, (20, y))
        
        y += 40
        score_text = font.render(f"Score: {score}", True, (255, 255, 0))
        ui_surface.blit(score_text, (20, y))
        
        y += 45
        block_num = font_small.render(f"Blok #{total_blocks}", True, (100, 255, 100))
        ui_surface.blit(block_num, (20, y))
        
        y += 25
        shape_text = font_small.render(f"Shape: {current_block.shape_name}", True, (200, 200, 200))
        ui_surface.blit(shape_text, (20, y))
        
        y += 25
        landed_text = font_small.render(f"Landed: {len(landed_blocks)} blok", True, (200, 200, 200))
        ui_surface.blit(landed_text, (20, y))
        
        # Countdown untuk blok berikutnya
        if current_block.is_landed:
            y += 35
            time_left = (spawn_interval - spawn_timer) / 1000
            countdown_text = font_small.render(f"⏱️  Blok baru dalam: {time_left:.1f}s", True, (255, 255, 100))
            ui_surface.blit(countdown_text, (20, y))
        
        # Info blok aktif
        y += 40
        info_title = font_small.render("📦 BLOK AKTIF:", True, (255, 255, 100))
        ui_surface.blit(info_title, (20, y))
        
        y += 26
        pos_text = font_small.render(f"Pos: ({current_block.pos_x:.1f}, {current_block.pos_y:.1f}, {current_block.pos_z:.1f})", True, (200, 200, 200))
        ui_surface.blit(pos_text, (20, y))
        
        y += 24
        rot_text = font_small.render(f"Rot: ({current_block.rotation[0]:.0f}°, {current_block.rotation[1]:.0f}°, {current_block.rotation[2]:.0f}°)", True, (200, 200, 200))
        ui_surface.blit(rot_text, (20, y))
        
        y += 24
        scale_text = font_small.render(f"Scale: {abs(current_block.scale[0]):.2f}x", True, (200, 200, 200))
        ui_surface.blit(scale_text, (20, y))
        
        # Panduan
        if show_guide:
            draw_guide_panel(ui_surface, font_small, display)
        
        # Hint
        hint_text = font_small.render("H-Guide | SPACE-Drop | Arrows-Camera | ESC-Quit", True, (150, 150, 150))
        ui_surface.blit(hint_text, (20, display[1] - 35))
        
        # Legend
        rx = display[0] - 180
        legend_texts = [
            ("🎨 SUMBU:", (200, 200, 200)),
            ("X=Merah", (255, 100, 100)),
            ("Y=Hijau", (100, 255, 100)),
            ("Z=Biru", (100, 100, 255)),
            ("", None),
            ("🟡=Aktif", (255, 255, 100))
        ]
        ry = 20
        for text, color in legend_texts:
            if text == "":
                ry += 10
            else:
                rendered = font_small.render(text, True, color)
                ui_surface.blit(rendered, (rx, ry))
                ry += 28
        
        # Render UI
        texture_data = pygame.image.tostring(ui_surface, "RGBA", True)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, display[0], display[1], 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glRasterPos2i(0, 0)
        glDrawPixels(display[0], display[1], GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        pygame.display.flip()
    
    pygame.quit()
    print(f"\n🎉 Game Selesai!")
    print(f"📊 Final Score: {score}")
    print(f"🧊 Total Blocks: {total_blocks}")
    print(f"📦 Landed: {len(landed_blocks)}")

if __name__ == "__main__":
    main()