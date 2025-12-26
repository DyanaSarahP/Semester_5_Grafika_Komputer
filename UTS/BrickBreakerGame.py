import tkinter as tk
import math
import random

class BrickBreakerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Brick Breaker - UTS Grafika Komputer")
        
        # Setup canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg='#0a0a1e')
        self.canvas.pack()
        
        # Game state
        self.game_running = False
        self.game_over = False
        self.score = 0
        self.lives = 3
        
        # Ball properties
        self.ball_x = 400
        self.ball_y = 400
        self.ball_radius = 10
        self.ball_vx = 4
        self.ball_vy = -4
        self.ball_rotation = 0  # Untuk rotasi visual
        
        # Paddle properties
        self.paddle_x = 350
        self.paddle_y = 550
        self.paddle_width = 100
        self.paddle_height = 15
        self.paddle_rotation = 0  # Transformasi ROTASI
        self.paddle_scale = 1.0   # Transformasi SKALA
        
        # Bricks (x, y, width, height, color, active)
        self.bricks = []
        self.create_bricks()
        
        # Power-ups list
        self.powerups = []  # (x, y, type, vy)
        
        # Bind controls
        self.canvas.bind('<Motion>', self.move_paddle)
        self.root.bind('<space>', self.start_game)
        self.root.bind('q', self.rotate_paddle_left)
        self.root.bind('e', self.rotate_paddle_right)
        self.root.bind('a', self.scale_paddle_smaller)
        self.root.bind('d', self.scale_paddle_bigger)
        
        # Start drawing
        self.draw_game()
        self.update_game()
        
    def create_bricks(self):
        """Buat bata-bata dengan warna berbeda"""
        colors = ['#ff6b6b', '#ff9f43', '#feca57', '#48dbfb', '#0abde3', '#ee5a6f']
        brick_width = 75
        brick_height = 25
        padding = 5
        
        for row in range(6):
            for col in range(10):
                x = col * (brick_width + padding) + 35
                y = row * (brick_height + padding) + 60
                color = colors[row]
                self.bricks.append({
                    'x': x, 'y': y, 
                    'width': brick_width, 
                    'height': brick_height,
                    'color': color,
                    'active': True,
                    'scale': 1.0  # Untuk animasi pecah
                })
    
    def draw_line_dda(self, x1, y1, x2, y2, color='#ffffff'):
        """Algoritma DDA untuk garis"""
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            return
        
        x_inc = dx / steps
        y_inc = dy / steps
        
        points = []
        x, y = x1, y1
        
        for i in range(int(steps) + 1):
            points.append((int(x), int(y)))
            x += x_inc
            y += y_inc
        
        # Draw dengan canvas line untuk speed
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
    
    def draw_circle_midpoint(self, xc, yc, r, color='#ffffff'):
        """Algoritma Midpoint Circle"""
        x = 0
        y = r
        d = 1 - r
        
        points = []
        
        while x <= y:
            points.extend([
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x),
                (xc + y, yc - x), (xc - y, yc - x)
            ])
            
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
        
        # Draw dengan canvas untuk speed
        self.canvas.create_oval(xc-r, yc-r, xc+r, yc+r, fill=color, outline='#ffffff', width=2)
        
        return points
    
    def translate_point(self, x, y, tx, ty):
        """Transformasi TRANSLASI"""
        return x + tx, y + ty
    
    def rotate_point(self, x, y, cx, cy, angle):
        """Transformasi ROTASI (angle dalam derajat)"""
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        x -= cx
        y -= cy
        
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        
        new_x += cx
        new_y += cy
        
        return new_x, new_y
    
    def scale_point(self, x, y, cx, cy, sx, sy):
        """Transformasi SKALA"""
        x -= cx
        y -= cy
        
        x *= sx
        y *= sy
        
        x += cx
        y += cy
        
        return x, y
    
    def reflect_vector(self, vx, vy, normal_x, normal_y):
        """Transformasi REFLEKSI (untuk mantul bola)"""
        # Reflection formula: V' = V - 2(V·N)N
        dot = vx * normal_x + vy * normal_y
        new_vx = vx - 2 * dot * normal_x
        new_vy = vy - 2 * dot * normal_y
        return new_vx, new_vy
    
    def move_paddle(self, event):
        """Gerakkan paddle mengikuti mouse (TRANSLASI)"""
        self.paddle_x = event.x - (self.paddle_width * self.paddle_scale) // 2
        
        # Keep in bounds
        if self.paddle_x < 10:
            self.paddle_x = 10
        if self.paddle_x > 790 - (self.paddle_width * self.paddle_scale):
            self.paddle_x = 790 - (self.paddle_width * self.paddle_scale)
    
    def rotate_paddle_left(self, event):
        """ROTASI paddle ke kiri (Q)"""
        self.paddle_rotation = max(-15, self.paddle_rotation - 5)
    
    def rotate_paddle_right(self, event):
        """ROTASI paddle ke kanan (E)"""
        self.paddle_rotation = min(15, self.paddle_rotation + 5)
    
    def scale_paddle_smaller(self, event):
        """SKALA paddle mengecil (A)"""
        self.paddle_scale = max(0.6, self.paddle_scale - 0.1)
    
    def scale_paddle_bigger(self, event):
        """SKALA paddle membesar (D)"""
        self.paddle_scale = min(1.5, self.paddle_scale + 0.1)
    
    def start_game(self, event):
        """Mulai game"""
        if not self.game_running and not self.game_over:
            self.game_running = True
    
    def spawn_powerup(self, x, y):
        """Spawn power-up dari bata pecah"""
        if random.random() < 0.3:  # 30% chance
            ptype = random.choice(['scale_up', 'scale_down'])
            self.powerups.append({
                'x': x, 'y': y, 'type': ptype, 'vy': 3
            })
    
    def update_game(self):
        """Update game logic"""
        if self.game_running and not self.game_over:
            # TRANSLASI bola
            self.ball_x += self.ball_vx
            self.ball_y += self.ball_vy
            
            # ROTASI visual bola
            self.ball_rotation += 10
            if self.ball_rotation >= 360:
                self.ball_rotation = 0
            
            # Check collision with walls
            if self.ball_x - self.ball_radius <= 0 or self.ball_x + self.ball_radius >= 800:
                # REFLEKSI horizontal
                self.ball_vx, self.ball_vy = self.reflect_vector(
                    self.ball_vx, self.ball_vy, 
                    1 if self.ball_x < 400 else -1, 0
                )
            
            if self.ball_y - self.ball_radius <= 0:
                # REFLEKSI vertical (atas)
                self.ball_vx, self.ball_vy = self.reflect_vector(
                    self.ball_vx, self.ball_vy, 
                    0, 1
                )
            
            # Check collision with paddle
            paddle_center_x = self.paddle_x + (self.paddle_width * self.paddle_scale) / 2
            paddle_center_y = self.paddle_y + self.paddle_height / 2
            
            # Get paddle corners dengan ROTASI & SKALA
            corners = self.get_paddle_corners()
            
            # Simple paddle collision
            if (self.paddle_x <= self.ball_x <= self.paddle_x + (self.paddle_width * self.paddle_scale) and
                self.paddle_y - self.ball_radius <= self.ball_y <= self.paddle_y + self.paddle_height):
                
                # REFLEKSI dengan sudut berdasarkan ROTASI paddle
                hit_pos = (self.ball_x - paddle_center_x) / ((self.paddle_width * self.paddle_scale) / 2)
                angle = hit_pos * 45 + self.paddle_rotation  # Rotasi paddle mempengaruhi sudut mantul
                
                speed = math.sqrt(self.ball_vx**2 + self.ball_vy**2)
                self.ball_vx = speed * math.sin(math.radians(angle))
                self.ball_vy = -abs(speed * math.cos(math.radians(angle)))
                
                self.ball_y = self.paddle_y - self.ball_radius
            
            # Check collision with bricks
            for brick in self.bricks:
                if not brick['active']:
                    continue
                
                bx, by = brick['x'], brick['y']
                bw, bh = brick['width'] * brick['scale'], brick['height'] * brick['scale']
                
                if (bx <= self.ball_x <= bx + bw and 
                    by <= self.ball_y <= by + bh):
                    
                    brick['active'] = False
                    self.score += 10
                    
                    # REFLEKSI bola
                    # Determine reflection normal
                    center_x = bx + bw/2
                    center_y = by + bh/2
                    
                    dx = self.ball_x - center_x
                    dy = self.ball_y - center_y
                    
                    if abs(dx) > abs(dy):
                        # Hit from side - horizontal reflection
                        self.ball_vx, self.ball_vy = self.reflect_vector(
                            self.ball_vx, self.ball_vy,
                            1 if dx > 0 else -1, 0
                        )
                    else:
                        # Hit from top/bottom - vertical reflection
                        self.ball_vx, self.ball_vy = self.reflect_vector(
                            self.ball_vx, self.ball_vy,
                            0, 1 if dy > 0 else -1
                        )
                    
                    # Spawn power-up
                    self.spawn_powerup(center_x, center_y)
                    
                    break
            
            # Update power-ups (TRANSLASI)
            for powerup in self.powerups[:]:
                powerup['y'] += powerup['vy']
                
                # Check collision with paddle
                if (self.paddle_x <= powerup['x'] <= self.paddle_x + (self.paddle_width * self.paddle_scale) and
                    self.paddle_y <= powerup['y'] <= self.paddle_y + self.paddle_height):
                    
                    # Apply power-up (SKALA)
                    if powerup['type'] == 'scale_up':
                        self.paddle_scale = min(1.8, self.paddle_scale + 0.3)
                    elif powerup['type'] == 'scale_down':
                        self.paddle_scale = max(0.5, self.paddle_scale - 0.2)
                    
                    self.powerups.remove(powerup)
                
                # Remove if off screen
                elif powerup['y'] > 600:
                    self.powerups.remove(powerup)
            
            # Check if ball fell
            if self.ball_y > 600:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                    self.game_running = False
                else:
                    # Reset ball
                    self.ball_x = 400
                    self.ball_y = 400
                    self.ball_vx = 4
                    self.ball_vy = -4
                    self.game_running = False
            
            # Check win condition
            if all(not brick['active'] for brick in self.bricks):
                self.game_over = True
                self.game_running = False
        
        self.draw_game()
        self.root.after(16, self.update_game)  # ~60 FPS
    
    def get_paddle_corners(self):
        """Get paddle corners dengan rotasi & skala"""
        cx = self.paddle_x + (self.paddle_width * self.paddle_scale) / 2
        cy = self.paddle_y + self.paddle_height / 2
        
        w = self.paddle_width * self.paddle_scale
        h = self.paddle_height
        
        corners = [
            (self.paddle_x, self.paddle_y),
            (self.paddle_x + w, self.paddle_y),
            (self.paddle_x + w, self.paddle_y + h),
            (self.paddle_x, self.paddle_y + h)
        ]
        
        # Apply rotation
        rotated = []
        for x, y in corners:
            rx, ry = self.rotate_point(x, y, cx, cy, self.paddle_rotation)
            rotated.append((rx, ry))
        
        return rotated
    
    def draw_game(self):
        """Draw semua elemen"""
        self.canvas.delete('all')
        
        # Draw title & instructions
        self.canvas.create_text(400, 20, text="BRICK BREAKER - GRAFIKA KOMPUTER", 
                                fill='#ffffff', font=('Arial', 16, 'bold'))
        
        self.canvas.create_text(400, 40, 
                                text="SPACE: Start | Q/E: Rotate Paddle | A/D: Scale Paddle | Mouse: Move", 
                                fill='#aaaaaa', font=('Arial', 9))
        
        # Draw bricks (POLIGON + SKALA untuk animasi pecah)
        for brick in self.bricks:
            if brick['active']:
                x, y = brick['x'], brick['y']
                w = brick['width'] * brick['scale']
                h = brick['height'] * brick['scale']
                
                # Gambar poligon untuk brick
                points = [x, y, x+w, y, x+w, y+h, x, y+h]
                self.canvas.create_polygon(points, fill=brick['color'], 
                                           outline='#ffffff', width=1)
        
        # Draw ball (LINGKARAN MIDPOINT + ROTASI visual)
        self.draw_circle_midpoint(int(self.ball_x), int(self.ball_y), 
                                   self.ball_radius, '#ffff00')
        
        # Draw rotation indicator on ball
        angle_rad = math.radians(self.ball_rotation)
        line_x = self.ball_x + self.ball_radius * 0.7 * math.cos(angle_rad)
        line_y = self.ball_y + self.ball_radius * 0.7 * math.sin(angle_rad)
        self.canvas.create_line(self.ball_x, self.ball_y, line_x, line_y, 
                                fill='#ff0000', width=2)
        
        # Draw paddle (POLIGON dengan ROTASI & SKALA)
        corners = self.get_paddle_corners()
        self.canvas.create_polygon(corners, fill='#00ff88', outline='#ffffff', width=2)
        
        # Draw paddle center point
        cx = self.paddle_x + (self.paddle_width * self.paddle_scale) / 2
        cy = self.paddle_y + self.paddle_height / 2
        self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill='#ffffff')
        
        # Draw power-ups (TRANSLASI kebawah)
        for powerup in self.powerups:
            color = '#00ffff' if powerup['type'] == 'scale_up' else '#ff00ff'
            self.canvas.create_oval(powerup['x']-8, powerup['y']-8,
                                    powerup['x']+8, powerup['y']+8,
                                    fill=color, outline='#ffffff')
            symbol = '↑' if powerup['type'] == 'scale_up' else '↓'
            self.canvas.create_text(powerup['x'], powerup['y'], 
                                    text=symbol, fill='#ffffff', font=('Arial', 12, 'bold'))
        
        # Draw borders (GARIS DDA)
        self.draw_line_dda(0, 0, 800, 0, '#4a90e2')
        self.draw_line_dda(0, 0, 0, 600, '#4a90e2')
        self.draw_line_dda(800, 0, 800, 600, '#4a90e2')
        
        # Draw UI
        self.canvas.create_text(100, 580, text=f"Score: {self.score}", 
                                fill='#ffffff', font=('Arial', 14, 'bold'))
        self.canvas.create_text(400, 580, text=f"Lives: {'❤️ ' * self.lives}", 
                                fill='#ff6b6b', font=('Arial', 14))
        self.canvas.create_text(700, 580, 
                                text=f"Paddle: {int(self.paddle_scale*100)}% | {self.paddle_rotation}°", 
                                fill='#ffffff', font=('Arial', 10))
        
        # Game status
        if not self.game_running and not self.game_over:
            self.canvas.create_text(400, 300, text="Press SPACE to Start!", 
                                    fill='#ffff00', font=('Arial', 24, 'bold'))
        
        if self.game_over:
            if self.lives <= 0:
                text = "GAME OVER!"
                color = '#ff0000'
            else:
                text = "YOU WIN!"
                color = '#00ff00'
            
            self.canvas.create_rectangle(200, 250, 600, 350, fill='#000000', outline='#ffffff', width=3)
            self.canvas.create_text(400, 280, text=text, 
                                    fill=color, font=('Arial', 32, 'bold'))
            self.canvas.create_text(400, 320, text=f"Final Score: {self.score}", 
                                    fill='#ffffff', font=('Arial', 18))

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    game = BrickBreakerGame(root)
    root.mainloop()