import pygame
import math
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 1000, 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPACE_DARK = (10, 10, 30)
SPACE_BLUE = (25, 25, 60)
BROWN = (80, 60, 40)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (138, 43, 226)
CYAN = (0, 255, 255)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer - Transformasi 2D (Luar Angkasa)")
clock = pygame.time.Clock()

# Kelas untuk Bintang
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.brightness = random.randint(150, 255)
        self.twinkle_speed = random.uniform(0.02, 0.05)
        self.twinkle_phase = random.uniform(0, math.pi * 2)
    
    def update(self):
        self.twinkle_phase += self.twinkle_speed
    
    def draw(self, surface):
        brightness = int(self.brightness * (0.7 + 0.3 * math.sin(self.twinkle_phase)))
        color = (brightness, brightness, brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

# Kelas untuk Planet
class Planet:
    def __init__(self, x, y, radius, color, ring=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.ring = ring
    
    def draw(self, surface):
        # Gambar planet
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Gambar highlight
        highlight_color = tuple(min(c + 50, 255) for c in self.color)
        pygame.draw.circle(surface, highlight_color, 
                         (int(self.x - self.radius//3), int(self.y - self.radius//3)), 
                         self.radius//3)
        
        # Gambar cincin jika ada
        if self.ring:
            ring_color = tuple(c // 2 for c in self.color)
            pygame.draw.ellipse(surface, ring_color, 
                              (self.x - self.radius * 1.5, self.y - self.radius // 4,
                               self.radius * 3, self.radius // 2), 2)

# Fungsi Transformasi 2D
def translate(x, y, dx, dy):
    """Translasi - Menggeser posisi"""
    return x + dx, y + dy

def rotate(x, y, cx, cy, angle):
    """Rotasi - Memutar titik terhadap pusat"""
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    tx = x - cx
    ty = y - cy
    
    rx = tx * cos_a - ty * sin_a
    ry = tx * sin_a + ty * cos_a
    
    return rx + cx, ry + cy

def scale(x, y, cx, cy, sx, sy):
    """Scaling - Memperbesar/memperkecil ukuran"""
    return cx + (x - cx) * sx, cy + (y - cy) * sy

def mirror_y(x, y, mirror_axis):
    """Mirror/Refleksi terhadap sumbu Y"""
    return 2 * mirror_axis - x, y

# Kelas Karakter Pemain dengan Transformasi
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_x = 10
        self.original_y = 5
        self.x = self.original_x
        self.y = self.original_y
        self.width = 40
        self.height = 50
        self.vel_y = 0
        self.on_ground = False
        self.rotation_angle = 0
        self.scale_factor = 1.0
        self.is_dashing = False
        self.dash_cooldown = 0
        self.is_mirrored = False
        self.mirror_axis = WIDTH // 2
        
    def draw(self, surface):
        # Titik-titik karakter (astronaut sederhana)
        points = [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height)
        ]
        
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        
        # Terapkan rotasi
        if self.rotation_angle != 0:
            points = [rotate(px, py, cx, cy, self.rotation_angle) for px, py in points]
        
        # Terapkan scaling
        if self.scale_factor != 1.0:
            points = [scale(px, py, cx, cy, self.scale_factor, self.scale_factor) for px, py in points]
        
        # Terapkan mirror
        if self.is_mirrored:
            points = [mirror_y(px, py, self.mirror_axis) for px, py in points]
            # Warna berbeda di dunia mirror
            pygame.draw.polygon(surface, CYAN, points)
            pygame.draw.polygon(surface, WHITE, points, 2)
        else:
            # Astronaut putih
            pygame.draw.polygon(surface, WHITE, points)
            pygame.draw.polygon(surface, YELLOW, points, 2)
        
        # Gambar helm/kepala astronaut
        head_center = (cx, cy - 5)
        if self.rotation_angle != 0:
            head_center = rotate(head_center[0], head_center[1], cx, cy, self.rotation_angle)
        if self.scale_factor != 1.0:
            head_center = scale(head_center[0], head_center[1], cx, cy, self.scale_factor, self.scale_factor)
        if self.is_mirrored:
            head_center = mirror_y(head_center[0], head_center[1], self.mirror_axis)
        
        helmet_radius = int(12 * self.scale_factor)
        pygame.draw.circle(surface, CYAN if self.is_mirrored else YELLOW, 
                         (int(head_center[0]), int(head_center[1])), helmet_radius)
        pygame.draw.circle(surface, WHITE if self.is_mirrored else SPACE_BLUE, 
                         (int(head_center[0]), int(head_center[1])), helmet_radius - 3)
        
        # Mata
        eye1 = (cx - 8, cy - 8)
        eye2 = (cx + 8, cy - 8)
        
        if self.rotation_angle != 0:
            eye1 = rotate(eye1[0], eye1[1], cx, cy, self.rotation_angle)
            eye2 = rotate(eye2[0], eye2[1], cx, cy, self.rotation_angle)
        if self.scale_factor != 1.0:
            eye1 = scale(eye1[0], eye1[1], cx, cy, self.scale_factor, self.scale_factor)
            eye2 = scale(eye2[0], eye2[1], cx, cy, self.scale_factor, self.scale_factor)
        if self.is_mirrored:
            eye1 = mirror_y(eye1[0], eye1[1], self.mirror_axis)
            eye2 = mirror_y(eye2[0], eye2[1], self.mirror_axis)
        
        pygame.draw.circle(surface, BLACK, (int(eye1[0]), int(eye1[1])), 3)
        pygame.draw.circle(surface, BLACK, (int(eye2[0]), int(eye2[1])), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def dash(self):
        if self.dash_cooldown <= 0:
            self.x, self.y = translate(self.x, self.y, 20, 0)
            self.is_dashing = True
            self.dash_cooldown = 30
    
    def attack_rotate(self):
        self.rotation_angle = (self.rotation_angle + 30) % 360
    
    def collect_power(self):
        self.scale_factor = 1.5
    
    def enter_mirror_world(self):
        self.is_mirrored = not self.is_mirrored
    
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += 5
        
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
        
        # Gravitasi lebih rendah (luar angkasa)
        self.vel_y += 0.5
        self.y += self.vel_y
        
        # Reset on_ground
        self.on_ground = False
        
        # Cek collision dengan semua platform
        player_rect = self.get_rect()
        for platform in platforms:
            platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
            
            # Jika player jatuh dan bertabrakan dengan platform
            if player_rect.colliderect(platform_rect):
                # Jika player jatuh dari atas
                if self.vel_y > 0 and player_rect.bottom <= platform_rect.top + 15:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
        
        # Ground dasar
        if self.y >= HEIGHT - 150 - self.height:
            self.y = HEIGHT - 150 - self.height
            self.vel_y = 0
            self.on_ground = True
        
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        
        if self.scale_factor > 1.0:
            self.scale_factor -= 0.01
        
        if self.rotation_angle > 0:
            self.rotation_angle = max(0, self.rotation_angle - 5)
    
    def jump(self):
        if self.on_ground:
            self.vel_y = -12  # Lompatan lebih tinggi di luar angkasa
            self.on_ground = False

# Kelas Platform (Meteor/Asteroid)
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, surface):
        # Meteor/asteroid
        pygame.draw.rect(surface, (100, 100, 120), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (80, 80, 100), (self.x, self.y, self.width, self.height), 3)
        
        # Tambah detail crater
        for i in range(3):
            cx = self.x + random.randint(10, int(self.width - 10))
            cy = self.y + random.randint(5, int(self.height - 5))
            pygame.draw.circle(surface, (60, 60, 80), (cx, cy), 5)

# Kelas Item Kekuatan (Crystal)
class PowerItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.size = 25
        self.collected = False
        self.glow_phase = 0
    
    def update(self):
        self.glow_phase += 0.1
    
    def draw(self, surface):
        if not self.collected:
            # Crystal yang bersinar
            glow = int(50 * (0.5 + 0.5 * math.sin(self.glow_phase)))
            color = (200 + glow, 50, 200 + glow)
            
            # Gambar crystal
            points = [
                (self.x + self.size//2, self.y),
                (self.x + self.size, self.y + self.size//2),
                (self.x + self.size//2, self.y + self.size),
                (self.x, self.y + self.size//2)
            ]
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, PURPLE, points, 2)
            
            # Efek cahaya
            for i in range(3):
                radius = int((30 + i * 5) * (0.5 + 0.5 * math.sin(self.glow_phase)))
                s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*color, 20), (radius, radius), radius)
                surface.blit(s, (self.x + self.size//2 - radius, self.y + self.size//2 - radius))
    
    def check_collision(self, player_rect):
        item_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        return item_rect.colliderect(player_rect) and not self.collected

# Kelas Portal Dimensi
class MirrorPortal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 60
        self.height = 100
        self.rotation = 0
    
    def update(self):
        self.rotation += 2
    
    def draw(self, surface):
        # Portal berputar
        for i in range(5):
            angle = self.rotation + i * 72
            rad = math.radians(angle)
            x1 = self.x + self.width//2 + math.cos(rad) * 30
            y1 = self.y + self.height//2 + math.sin(rad) * 30
            x2 = self.x + self.width//2 + math.cos(rad) * 40
            y2 = self.y + self.height//2 + math.sin(rad) * 40
            pygame.draw.line(surface, CYAN, (x1, y1), (x2, y2), 3)
        
        # Lingkaran portal
        pygame.draw.circle(surface, (100, 200, 255), 
                         (self.x + self.width//2, self.y + self.height//2), 35, 3)
        pygame.draw.circle(surface, (150, 220, 255), 
                         (self.x + self.width//2, self.y + self.height//2), 25, 2)
    
    def check_collision(self, player_rect):
        portal_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return portal_rect.colliderect(player_rect)

# Buat bintang-bintang
stars = [Star() for _ in range(200)]

# Buat planet
planets = [
    Planet(150, 120, 50, (255, 100, 100), ring=True),  # Planet merah dengan cincin
    Planet(750, 150, 35, (100, 150, 255)),  # Planet biru
    Planet(850, 400, 25, (200, 200, 100)),  # Planet kuning
]

# Setup game objects
player = Player()
platforms = []
power_items = []
mirror_portal = MirrorPortal(WIDTH - 100, HEIGHT - 250)

# Buat platform
platform_data = [
    (0, HEIGHT - 150, WIDTH, 150),
    (200, HEIGHT - 250, 150, 20),
    (450, HEIGHT - 350, 150, 20),
    (700, HEIGHT - 250, 150, 20),
]

for p_data in platform_data:
    platforms.append(Platform(*p_data))

# Buat power items
power_items.append(PowerItem(500, HEIGHT - 400))
power_items.append(PowerItem(300, HEIGHT - 300))

# Variabel game
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 72)
instructions_visible = True
game_won = False
total_crystals = len(power_items)
collected_crystals = 0

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_won:
                # Jika menang, tekan apapun untuk keluar
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    running = False
            else:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_e:
                    player.dash()
                elif event.key == pygame.K_q:
                    player.attack_rotate()
                elif event.key == pygame.K_h:
                    instructions_visible = not instructions_visible
    
    # Update
    if not game_won:
        player.update(platforms)
    mirror_portal.update()
    
    for star in stars:
        star.update()
    
    for item in power_items:
        item.update()
    
    player_rect = player.get_rect()
    for item in power_items:
        if item.check_collision(player_rect):
            if not item.collected:
                collected_crystals += 1
            item.collected = True
            player.collect_power()
    
    # Cek apakah menang
    if collected_crystals >= total_crystals and not game_won:
        game_won = True
    
    if mirror_portal.check_collision(player_rect):
        player.enter_mirror_world()
    
    # Gambar background luar angkasa
    if player.is_mirrored:
        # Dimensi alternatif - lebih terang
        screen.fill((40, 20, 60))
    else:
        # Luar angkasa normal - gelap
        screen.fill(SPACE_DARK)
    
    # Gambar bintang-bintang
    for star in stars:
        star.draw(screen)
    
    # Gambar planet
    for planet in planets:
        planet.draw(screen)
    
    # Gambar garis dimensi
    for i in range(0, HEIGHT, 50):
        alpha = 30 if not player.is_mirrored else 50
        color = (100, 100, 200, alpha) if not player.is_mirrored else (200, 100, 200, alpha)
        pygame.draw.line(screen, color[:3], (WIDTH//2, i), (WIDTH//2, i + 25), 1)
    
    # Gambar platform
    for platform in platforms:
        platform.draw(screen)
    
    # Gambar power items
    for item in power_items:
        item.draw(screen)
    
    # Gambar portal
    mirror_portal.draw(screen)
    
    # Gambar player
    player.draw(screen)
    
    # UI - Instruksi
    if instructions_visible:
        instruction_texts = [
            "TRANSFORMASI 2D - LUAR ANGKASA",
            "Koordinat Awal: (10, 5)",
            "",
            "KONTROL:",
            "A/D atau Arrow: Gerak Kiri/Kanan",
            "SPACE/W: Lompat (Gravitasi Rendah)",
            "E: DASH (Translasi dx=20, dy=0)",
            "Q: ROTASI (Putar 30 derajat)",
            "Ambil Crystal Ungu: SCALING (1.5x)",
            "Masuk Portal: MIRROR (Refleksi sumbu-Y)",
            "H: Sembunyikan instruksi"
        ]
        
        y_offset = 10
        for i, text in enumerate(instruction_texts):
            if i == 0:
                label = font.render(text, True, CYAN if player.is_mirrored else YELLOW)
            else:
                label = small_font.render(text, True, WHITE)
            
            bg_rect = label.get_rect()
            bg_rect.x = 10
            bg_rect.y = y_offset
            bg_surf = pygame.Surface((bg_rect.width + 10, bg_rect.height), pygame.SRCALPHA)
            bg_surf.fill((0, 0, 0, 150))
            screen.blit(bg_surf, (5, y_offset))
            
            screen.blit(label, (10, y_offset))
            y_offset += 25 if i == 0 else 22
    else:
        hint = small_font.render("Tekan H untuk instruksi", True, CYAN)
        screen.blit(hint, (10, 10))
    
    # Status transformasi
    status_y = HEIGHT - 100
    status_texts = [
        f"Posisi: ({int(player.x)}, {int(player.y)})",
        f"Rotasi: {int(player.rotation_angle)}°",
        f"Scale: {player.scale_factor:.2f}x",
        f"Dimensi: {'ALTERNATIF' if player.is_mirrored else 'NORMAL'}",
        f"Crystal: {collected_crystals}/{total_crystals}",
    ]
    
    for i, text in enumerate(status_texts):
        label = small_font.render(text, True, CYAN if player.is_mirrored else YELLOW)
        bg_rect = label.get_rect()
        bg_rect.x = WIDTH - 250
        bg_rect.y = status_y + i * 22
        bg_surf = pygame.Surface((bg_rect.width + 10, bg_rect.height), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 150))
        screen.blit(bg_surf, (WIDTH - 255, status_y + i * 22))
        screen.blit(label, (WIDTH - 250, status_y + i * 22))
    
    # Tampilkan layar kemenangan jika menang
    if game_won:
        # Overlay gelap
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Teks YOU WIN
        win_text = large_font.render("YOU WIN!", True, YELLOW)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        
        # Efek glow untuk teks
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_text = large_font.render("YOU WIN!", True, ORANGE)
            glow_rect = win_text.get_rect(center=(WIDTH // 2 + offset[0], HEIGHT // 2 - 80 + offset[1]))
            screen.blit(glow_text, glow_rect)
        
        screen.blit(win_text, win_rect)
        
        # Pesan selamat
        congrats_text = font.render("Selamat! Semua Crystal Terkumpul!", True, WHITE)
        congrats_rect = congrats_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(congrats_text, congrats_rect)
        
        # Informasi transformasi yang digunakan
        transform_text = small_font.render("Anda telah menguasai semua Transformasi 2D:", True, CYAN)
        transform_rect = transform_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(transform_text, transform_rect)
        
        transformations = [
            "✓ Translasi (Dash)",
            "✓ Rotasi (Spin Attack)",
            "✓ Scaling (Power Up)",
            "✓ Mirror (Dimension Shift)"
        ]
        
        y_pos = HEIGHT // 2 + 70
        for t in transformations:
            t_text = small_font.render(t, True, WHITE)
            t_rect = t_text.get_rect(center=(WIDTH // 2, y_pos))
            screen.blit(t_text, t_rect)
            y_pos += 25
        
        # Tombol keluar
        exit_text = font.render("Tekan ENTER, SPACE atau ESC untuk Keluar", True, YELLOW)
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        
        # Background tombol
        button_bg = pygame.Surface((exit_rect.width + 40, exit_rect.height + 20), pygame.SRCALPHA)
        button_bg.fill((100, 50, 150, 200))
        pygame.draw.rect(button_bg, CYAN, (0, 0, exit_rect.width + 40, exit_rect.height + 20), 3)
        screen.blit(button_bg, (exit_rect.x - 20, exit_rect.y - 10))
        screen.blit(exit_text, exit_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()