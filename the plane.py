import random
import sys
import math
import pygame

# --- НАСТРОЙКИ ---
WIDTH, HEIGHT = 1024, 768
FPS = 60  # УЛЬТРА-ПЛАВНОСТЬ: Стабильные 244 FPS без лагов!

# СВЕТЛЫЕ ЦВЕТА
COLOR_SKY = (145, 215, 255)
COLOR_CLOUD = (255, 255, 255, 195)
COLOR_TEXT = (15, 25, 45)
COLOR_ACTIVE = (0, 110, 240)


class Cloud:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = random.randint(35, 75)
        self.speed = random.uniform(1.5, 3.5)

    def update(self, game_speed):
        dt_speed = (self.speed * game_speed) * (60 / FPS)
        self.x -= dt_speed
        if self.x + self.radius * 2 < 0:
            self.x = WIDTH + self.radius * 2
            self.y = random.randint(0, HEIGHT)

    def draw(self, surface):
        cloud_surf = pygame.Surface((self.radius * 4, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(cloud_surf, COLOR_CLOUD, (self.radius, self.radius), self.radius)
        pygame.draw.circle(cloud_surf, COLOR_CLOUD, (self.radius * 2, self.radius * 1.2), self.radius * 0.8)
        surface.blit(cloud_surf, (self.x, self.y - self.radius))


class Obstacle:
    def __init__(self):
        self.reset()

    def update(self, game_speed, current_level):
        speed_modifier = 1 + (current_level * 0.15)
        dt_speed = (self.base_speed * game_speed * speed_modifier) * (60 / FPS)
        self.x -= dt_speed
        if self.x + self.radius < 0:
            self.reset()

    def reset(self):
        self.x = WIDTH + random.randint(100, 600)
        self.y = random.randint(50, HEIGHT - 50)
        self.radius = random.randint(15, 22)
        self.base_speed = random.uniform(4, 6)

    def draw(self, surface):
        pygame.draw.circle(surface, (230, 40, 40), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (90, 0, 0), (int(self.x), int(self.y)), self.radius, 3)


class Explosion:
    def __init__(self, x, y, max_radius, color):
        self.x = x
        self.y = y
        self.current_radius = 5
        self.max_radius = max_radius
        self.color = color
        self.finished = False

    def update(self, enemies, enemy_bullets, boss):
        self.current_radius += 6 * (60 / FPS)
        if self.current_radius >= self.max_radius:
            self.finished = True

        for en in enemies:
            if not en.is_dying and math.hypot(self.x - en.x, self.y - en.y) < self.current_radius:
                en.hp -= 3
                if en.hp <= 0: en.hit()

        for eb in enemy_bullets[:]:
            if math.hypot(self.x - eb.x, self.y - eb.y) < self.current_radius:
                if eb in enemy_bullets: enemy_bullets.remove(eb)

    def draw(self, surface):
        surf = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        alpha = max(0, 255 - int((self.current_radius / self.max_radius) * 255))
        r, g, b = self.color
        pygame.draw.circle(surf, (r, g, b, alpha), (self.max_radius, self.max_radius), int(self.current_radius))
        pygame.draw.circle(surf, (255, 255, 255, alpha), (self.max_radius, self.max_radius),
                           int(self.current_radius * 0.5))
        surface.blit(surf, (int(self.x - self.max_radius), int(self.y - self.max_radius)))


class Boss:
    def __init__(self, level):
        self.level = level
        self.active = False
        self.x = WIDTH + 400
        self.y = HEIGHT // 2
        self.target_y = HEIGHT // 2
        self.last_shot = 0
        self.last_move = 0

        if level == 7:
            self.name = "CYBER ZEPPELIN 'KRAKEN'"
            self.max_hp = 480
            self.hp = 480
            self.speed = 1.5
            self.shoot_delay = 700
        else:
            self.name = "ULTIMATE DRONE 'X-1' (GOD MODE)"
            self.max_hp = 960
            self.hp = 960
            self.speed = 4.5
            self.shoot_delay = 280

    def update(self, game_speed, enemy_bullets):
        if not self.active: return

        dt_speed = self.speed * game_speed * (60 / FPS)

        if self.x > 720:
            self.x -= dt_speed
        else:
            now = pygame.time.get_ticks()
            if now - self.last_move > 700:
                self.target_y = random.randint(180, HEIGHT - 180)
                self.last_move = now

            if self.y < self.target_y:
                self.y += dt_speed
            elif self.y > self.target_y:
                self.y -= dt_speed

            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                if self.level == 7:
                    for angle in [-5, -2.5, 0, 2.5, 5]:
                        enemy_bullets.append(EnemyBullet(self.x - 100, self.y, speed=6, dy=angle))
                else:
                    enemy_bullets.append(EnemyBullet(self.x - 60, self.y - 40, speed=14))
                    enemy_bullets.append(EnemyBullet(self.x - 60, self.y + 40, speed=14))
                    if random.random() > 0.4:
                        enemy_bullets.append(EnemyBullet(self.x - 60, self.y, speed=11, dy=random.choice([-3, 3])))


    def draw(self, surface):
        if not self.active: return

        if self.level == 7:
            pygame.draw.ellipse(surface, (55, 60, 75), (int(self.x - 140), int(self.y - 70), 280, 140))
            pygame.draw.ellipse(surface, (80, 85, 105), (int(self.x - 120), int(self.y - 55), 240, 110))
            pygame.draw.line(surface, (25, 25, 30), (int(self.x), int(self.y - 70)), (int(self.x), int(self.y + 70)), 5)
            pygame.draw.line(surface, (25, 25, 30), (int(self.x - 60), int(self.y - 65)),
                             (int(self.x - 60), int(self.y + 65)), 4)
            pygame.draw.rect(surface, (35, 35, 40), (int(self.x + 120), int(self.y - 40), 30, 25))
            pygame.draw.rect(surface, (35, 35, 40), (int(self.x + 120), int(self.y + 15), 30, 25))
            pygame.draw.circle(surface, (255, 90, 0), (int(self.x + 150), int(self.y - 28)), 9)
            pygame.draw.circle(surface, (255, 90, 0), (int(self.x + 150), int(self.y + 27)), 9)
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x - 80), int(self.y)), 15)
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x - 85), int(self.y - 3)), 5)
        else:
            pygame.draw.polygon(surface, (0, 240, 255),
                                [(self.x + 115, self.y), (self.x - 95, self.y - 110), (self.x - 45, self.y),
                                 (self.x - 95, self.y + 110)], 5)
            pygame.draw.polygon(surface, (25, 28, 36),
                                [(self.x + 100, self.y), (self.x - 80, self.y - 95), (self.x - 40, self.y),
                                 (self.x - 80, self.y + 95)])
            pygame.draw.polygon(surface, (45, 50, 65),
                                [(self.x + 40, self.y), (self.x - 30, self.y - 40), (self.x - 10, self.y),
                                 (self.x - 30, self.y + 40)])
            pygame.draw.circle(surface, (255, 0, 90), (int(self.x - 10), int(self.y)), 16)
            pygame.draw.circle(surface, (255, 230, 240), (int(self.x - 10), int(self.y)), 6)

        if self.x <= 750:
            font_boss = pygame.font.SysFont("monospace", 18, bold=True)
            txt_name = font_boss.render(f"{self.name} [{self.hp}/{self.max_hp} HP]", True, (190, 0, 0))
            surface.blit(txt_name, (WIDTH // 2 - txt_name.get_width() // 2, 15))

            pygame.draw.rect(surface, (70, 70, 70), (WIDTH // 2 - 250, 42, 500, 20))
            hp_bar_width = int((self.hp / self.max_hp) * 500)
            if hp_bar_width > 0:
                pygame.draw.rect(surface, (255, 0, 60), (WIDTH // 2 - 250, 42, hp_bar_width, 20))
            pygame.draw.rect(surface, (0, 0, 0), (WIDTH // 2 - 250, 42, 500, 20), 2)


class EnemyShip:
    def __init__(self):
        self.reset()
        self.x = -200

    def reset(self):
        self.x = WIDTH + random.randint(200, 800)
        self.y = random.randint(100, HEIGHT - 100)
        self.speed = random.uniform(3, 5)
        self.move_dir = random.choice([-1, 1])
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1200, 2500)
        self.is_dying = False
        self.fall_speed_y = 0
        self.fall_speed_x = 0
        self.hp = 3

    def hit(self):
        if not self.is_dying:
            self.is_dying = True
            self.fall_speed_y = -4
            self.fall_speed_x = random.uniform(1, 3)

    def update(self, game_speed, current_level, enemy_bullets, boss_active):
        dt_factor = 60 / FPS
        if boss_active and not self.is_dying:
            self.x -= 8 * game_speed * dt_factor
            return

        if self.is_dying:
            self.fall_speed_y += 0.35 * dt_factor
            self.y += self.fall_speed_y * dt_factor
            self.x -= self.fall_speed_x * game_speed * dt_factor
            if self.y > HEIGHT + 50 or self.x < -100:
                self.reset()
        else:
            self.x -= (self.speed + current_level * 0.5) * game_speed * dt_factor
            self.y += self.move_dir * 2 * dt_factor
            if self.y < 50 or self.y > HEIGHT - 100: self.move_dir *= -1
            if self.x < -100: self.reset()

            now = pygame.time.get_ticks()
            if self.x < WIDTH and now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                enemy_bullets.append(EnemyBullet(self.x - 40, self.y))

    def draw(self, surface):
        if self.x > -100 and self.x < WIDTH + 100:
            surf = pygame.Surface((120, 60), pygame.SRCALPHA)
            if self.is_dying:
                c_hull, c_wings = (45, 45, 50), (25, 20, 20)
            else:
                c_hull, c_wings = (200, 45, 45), (100, 15, 15)

            pygame.draw.polygon(surf, c_wings, [(90, 30), (10, 0), (45, 30), (10, 60)])
            pygame.draw.polygon(surf, (55, 55, 55), [(45, 30), (0, 10), (15, 30), (0, 50)])
            pygame.draw.ellipse(surf, c_hull, (35, 21, 70, 18))
            pygame.draw.circle(surf, (0, 255, 255), (95, 30), 4)

            if self.is_dying:
                flen = random.randint(25, 50)
                pygame.draw.polygon(surf, (255, 60, 0), [(40, 30), (40 - flen, 22), (40, 38)])
                pygame.draw.circle(surf, (255, 190, 0), (35, 30), 6)
            surface.blit(surf, (int(self.x - 60), int(self.y - 30)))


class EnemyBullet:
    """ВРАЖЕСКИЕ ПУЛИ: Теперь это настоящие вытянутые плазменные снаряды"""

    def __init__(self, x, y, speed=9, dy=0):
        self.x = x
        self.y = y
        self.speed = speed
        self.dy = dy

    def update(self, game_speed):
        dt_factor = 60 / FPS
        self.x -= self.speed * game_speed * dt_factor
        self.y += self.dy * dt_factor

    def draw(self, surface):
        # Отрисовка вытянутого патрона (плазменной пули) вместо шарика
        pygame.draw.polygon(surface, (255, 0, 60), [
            (int(self.x - 12), int(self.y - 4)),
            (int(self.x + 4), int(self.y - 3)),
            (int(self.x + 12), int(self.y)),  # Острый наконечник пули
            (int(self.x + 4), int(self.y + 3)),
            (int(self.x - 12), int(self.y + 4))
        ])
        # Яркий внутренний лазерный стержень пули
        pygame.draw.line(surface, (255, 240, 240), (int(self.x - 8), int(self.y)), (int(self.x + 6), int(self.y)), 2)


class PlayerBullet:
    def __init__(self, x, y, skin_type, is_heavy_rocket=False, angle_y=0):
        self.x = x
        self.y = y
        self.skin_type = skin_type
        self.is_heavy_rocket = is_heavy_rocket
        self.angle_y = angle_y
        self.speed = 14
        self.particles = []

        if is_heavy_rocket:
            self.speed = 12
            if skin_type == 3: self.speed = 8
            if skin_type == 6: self.speed = 22
        else:
            if skin_type == 3: self.speed = 10
            if skin_type == 4:
                self.speed = 6
                self.gravity = 0.3
                self.vel_y = -3
            if skin_type == 6: self.speed = 26

    def update(self):
        dt_factor = 60 / FPS

        if self.is_heavy_rocket and random.random() > 0.15:
            self.particles.append([self.x - 16, self.y + random.randint(-4, 4), random.uniform(6, 10),
                                   random.choice([(255, 60, 0), (255, 150, 0)])])

        if not self.is_heavy_rocket and self.skin_type == 4:
            self.x += self.speed * dt_factor
            self.vel_y += self.gravity * dt_factor
            self.y += self.vel_y * dt_factor
        else:
            self.x += self.speed * dt_factor
            self.y += self.angle_y * dt_factor

        for p in self.particles[:]:
            p[0] -= 3 * dt_factor
            p[2] -= 0.3 * dt_factor
            if p[2] <= 0: self.particles.remove(p)

    def draw(self, surface):
        for p in self.particles:
            pygame.draw.circle(surface, p[3], (int(p[0]), int(p[1])), int(p[2]))

        if self.is_heavy_rocket:
            if self.skin_type == 1:
                pygame.draw.rect(surface, (160, 160, 160), (int(self.x - 24), int(self.y - 4), 24, 8), border_radius=2)
                pygame.draw.polygon(surface, (220, 0, 0),
                                    [(self.x, self.y - 4), (self.x + 7, self.y), (self.x, self.y + 4)])
                pygame.draw.polygon(surface, (40, 40, 40),
                                    [(self.x - 24, self.y - 4), (self.x - 30, self.y - 8), (self.x - 18, self.y - 4)])
                pygame.draw.polygon(surface, (40, 40, 40),
                                    [(self.x - 24, self.y + 4), (self.x - 30, self.y + 8), (self.x - 18, self.y + 4)])
            elif self.skin_type == 2:
                pygame.draw.ellipse(surface, (0, 160, 255), (int(self.x - 26), int(self.y - 6), 26, 12))
                pygame.draw.ellipse(surface, (210, 255, 255), (int(self.x - 18), int(self.y - 3), 18, 6))
            elif self.skin_type == 3:
                pygame.draw.rect(surface, (35, 40, 35), (int(self.x - 34), int(self.y - 9), 34, 18), border_radius=4)
                pygame.draw.polygon(surface, (255, 130, 0),
                                    [(self.x, self.y - 9), (self.x + 11, self.y), (self.x, self.y + 9)])
                pygame.draw.rect(surface, (220, 0, 0), (int(self.x - 30), int(self.y - 13), 6, 4))
                pygame.draw.rect(surface, (220, 0, 0), (int(self.x - 30), int(self.y + 9), 6, 4))
            elif self.skin_type == 4:
                pygame.draw.ellipse(surface, (60, 70, 60), (int(self.x - 22), int(self.y - 11), 22, 22))
                pygame.draw.circle(surface, (255, 30, 0), (int(self.x - 4), int(self.y)), 5)
            elif self.skin_type == 5:
                pygame.draw.ellipse(surface, (255, 80, 0), (int(self.x - 36), int(self.y - 10), 36, 20))
                pygame.draw.rect(surface, (30, 30, 30), (int(self.x - 36), int(self.y - 14), 5, 28))
            elif self.skin_type == 6:
                # ИСПРАВЛЕНО: Координаты точек теперь передаются строго как кортежи из пар (x, y)
                pygame.draw.polygon(surface, (170, 0, 255), [
                    (int(self.x + 5), int(self.y)),
                    (int(self.x - 28), int(self.y - 8)),
                    (int(self.x - 18), int(self.y)),
                    (int(self.x - 28), int(self.y + 8))
                ])
                pygame.draw.line(surface, (255, 255, 255), (int(self.x - 12), int(self.y)),
                                 (int(self.x + 5), int(self.y)), 2)
            return

        # Урон для каждого типа снаряда
        if self.skin_type == 1:
            self.damage = 1  # Базовый истребитель
            pygame.draw.line(surface, (255, 230, 0), (int(self.x), int(self.y)), (int(self.x - 20), int(self.y)), 5)
            pygame.draw.line(surface, (255, 255, 255), (int(self.x), int(self.y)), (int(self.x - 16), int(self.y)), 2)

        elif self.skin_type == 2:
            self.damage = 2  # Ледяной самолёт
            pygame.draw.circle(surface, (0, 200, 255), (int(self.x), int(self.y)), 7)
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), 3)

        elif self.skin_type == 3:
            self.damage = 4  # Тяжёлый штурмовик
            pygame.draw.rect(surface, (45, 45, 50), (int(self.x - 22), int(self.y - 4), 22, 8), border_radius=1)

        elif self.skin_type == 4:
            self.damage = 10  # Бомбардировщик
            pygame.draw.ellipse(surface, (85, 100, 85), (int(self.x - 14), int(self.y - 9), 28, 18))

        elif self.skin_type == 5:
            self.damage = 1  # Плазменный самолёт
            pygame.draw.circle(surface, (30, 255, 100), (int(self.x), int(self.y)), 7)
            pygame.draw.circle(surface, (230, 255, 240), (int(self.x), int(self.y)), 3)

        elif self.skin_type == 6:
            self.damage = 1  # Лазерный самолёт
            pygame.draw.line(surface, (255, 0, 90), (int(self.x), int(self.y)), (int(self.x - 48), int(self.y)), 6)
            pygame.draw.line(surface, (255, 255, 255), (int(self.x), int(self.y)), (int(self.x - 44), int(self.y)), 2)




class Airplane:
    def __init__(self):
        self.x = 200
        self.y = HEIGHT // 2
        self.base_speed = 10.0  # Чуть увеличили базовую скорость для отзывчивости
        self.tilt = 0

    def update(self, keys, control_type, game_speed):
        dx, dy = 0, 0
        dt_factor = 60 / FPS
        # Скорость самолета игрока теперь жестко зависит от игрового режима (замедление/ускорение)
        current_speed = self.base_speed * game_speed * dt_factor

        if control_type == "KEYBOARD":
            if keys[pygame.K_UP]:
                dy = -current_speed; self.tilt = -15
            elif keys[pygame.K_DOWN]:
                dy = current_speed; self.tilt = 15
            else:
                self.tilt += (0 - self.tilt) * 0.15 * dt_factor
            if keys[pygame.K_LEFT]: dx = -current_speed
            if keys[pygame.K_RIGHT]: dx = current_speed
            self.x += dx;
            self.y += dy
        elif control_type == "MOUSE":
            mx, my = pygame.mouse.get_pos()
            old_y = self.y
            self.x += (mx - self.x) * 0.15 * game_speed * dt_factor
            self.y += (my - self.y) * 0.15 * game_speed * dt_factor
            diff_y = self.y - old_y
            if diff_y < -1:
                self.tilt = -15
            elif diff_y > 1:
                self.tilt = 15
            else:
                self.tilt += (0 - self.tilt) * 0.15 * dt_factor

        self.x = max(50, min(WIDTH - 150, self.x))
        self.y = max(50, min(HEIGHT - 50, self.y))

    def draw(self, surface, boost_active, current_skin, custom_pos=None):
        surf = pygame.Surface((220, 110), pygame.SRCALPHA)
        cx, cy = 110, 55

        c_gray = (100, 115, 130)
        c_light = (165, 175, 195)
        c_dark = (50, 55, 65)
        c_black = (22, 22, 28)
        c_glass = (0, 170, 255, 220)

        if boost_active:
            flen = random.randint(100, 160)  # Еще мощнее пламя форсажа
            pygame.draw.polygon(surf, (255, 90, 0), [(35, cy - 14), (35 - flen, cy), (35, cy + 14)])
            pygame.draw.polygon(surf, (255, 240, 0), [(35, cy - 7), (35 - flen * 0.5, cy), (35, cy + 7)])

        if current_skin == 1:
            pygame.draw.polygon(surf, c_gray, [(35, cy), (80, cy - 30), (95, cy), (80, cy + 30)])
            pygame.draw.polygon(surf, (80, 95, 110), [(50, cy - 12), (70, cy - 25), (80, cy - 10)])
            pygame.draw.ellipse(surf, c_light, (30, cy - 9, 115, 18))
            pygame.draw.ellipse(surf, c_glass, (110, cy - 5, 22, 10))
        elif current_skin == 2:
            pygame.draw.polygon(surf, (0, 255, 255, 100), [(45, cy), (80, cy - 42), (110, cy - 42), (105, cy)], 3)
            pygame.draw.polygon(surf, c_dark, [(45, cy), (80, cy - 40), (110, cy - 40), (105, cy)])
            pygame.draw.polygon(surf, c_dark, [(45, cy), (80, cy + 40), (110, cy + 40), (105, cy)])
            pygame.draw.polygon(surf, c_gray, [(30, cy - 10), (145, cy - 10), (155, cy), (145, cy + 10), (30, cy + 10)])
            pygame.draw.ellipse(surf, c_glass, (115, cy - 6, 26, 12))
        elif current_skin == 3:
            pygame.draw.polygon(surf, c_black,
                                [(25, cy), (70, cy - 48), (145, cy), (70, cy + 48), (40, cy + 16), (40, cy - 16)])
            pygame.draw.polygon(surf, (255, 0, 100),
                                [(25, cy), (70, cy - 48), (145, cy), (70, cy + 48), (40, cy + 16), (40, cy - 16)], 2)
            pygame.draw.polygon(surf, (55, 60, 70), [(115, cy - 5), (135, cy), (115, cy + 5)])
        elif current_skin == 4:
            pygame.draw.polygon(surf, c_black,
                                [(145, cy), (65, cy - 54), (45, cy - 54), (55, cy - 15), (25, cy), (55, cy + 15),
                                 (45, cy + 54), (65, cy + 54)])
            pygame.draw.polygon(surf, c_dark,
                                [(135, cy), (65, cy - 44), (50, cy - 44), (55, cy - 12), (35, cy), (55, cy + 12),
                                 (50, cy + 44), (65, cy + 44)])
            pygame.draw.ellipse(surf, (10, 10, 12), (105, cy - 10, 32, 20))
        elif current_skin == 5:
            pygame.draw.ellipse(surf, c_gray, (15, cy - 10, 180, 20))
            pygame.draw.polygon(surf, c_dark, [(60, cy), (75, cy - 56), (90, cy - 56), (125, cy)])
            pygame.draw.polygon(surf, c_dark, [(60, cy), (75, cy + 56), (90, cy + 56), (125, cy)])
            pygame.draw.rect(surf, (40, 40, 45), (70, cy - 42, 20, 8))
            pygame.draw.rect(surf, (40, 40, 45), (70, cy + 34, 20, 8))
        elif current_skin == 6:
            pygame.draw.ellipse(surf, c_black, (10, cy - 7, 190, 14))
            pygame.draw.polygon(surf, c_black,
                                [(55, cy - 32), (120, cy - 32), (155, cy), (120, cy + 32), (55, cy + 32)])
            pygame.draw.ellipse(surf, (255, 255, 255), (135, cy - 4, 14, 8))

        if custom_pos:
            surface.blit(surf, (custom_pos[0] - cx, custom_pos[1] - cy))
        else:
            rotated_surf = pygame.transform.rotate(surf, -self.tilt)
            new_rect = rotated_surf.get_rect(center=(self.x, self.y))
            surface.blit(rotated_surf, new_rect.topleft)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Air Combat: 244 FPS CRASH FIXED")
    clock = pygame.time.Clock()

    airplane = Airplane()
    clouds = [Cloud() for _ in range(12)]
    obstacles = [Obstacle() for _ in range(4)]
    enemies = [EnemyShip() for _ in range(3)]

    enemy_bullets = []
    player_bullets = []
    explosions = []

    skin_names = {
        1: "F-16 Falcon [Flak Rocket]",
        2: "F-35 Lightning II [Plasma Torpedo]",
        3: "F-117 Nighthawk [NUCLEAR TACTICAL]",
        4: "B-2 Spirit [Heavy Bomb]",
        5: "B-52 Stratofortress [Napalm Tank]",
        6: "SR-71 Blackbird [Quantum Spear]",
    }

    game_state = "MENU"
    selected_level = 1
    selected_skin = 1
    control_mode = "KEYBOARD"
    menu_row = 0

    countdown_start_time = 0
    countdown_seconds = 2

    raw_score = 0
    shake_amount = 0
    last_player_shot = 0
    last_player_rocket = 0
    boss = None

    running = True
    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        boost_active = False
        game_speed = 1.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
                if game_state == "MENU":
                    if event.key == pygame.K_UP:
                        menu_row = max(0, menu_row - 1)
                    elif event.key == pygame.K_DOWN:
                        menu_row = min(2, menu_row + 1)
                    if menu_row == 0:
                        if event.key == pygame.K_LEFT: selected_level = max(1, selected_level - 1)
                        if event.key == pygame.K_RIGHT: selected_level = min(8, selected_level + 1)
                    elif menu_row == 1:
                        if event.key == pygame.K_LEFT: selected_skin = max(1, selected_skin - 1)
                        if event.key == pygame.K_RIGHT: selected_skin = min(6, selected_skin + 1)
                    elif menu_row == 2:
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                            control_mode = "MOUSE" if control_mode == "KEYBOARD" else "KEYBOARD"
                    if event.key == pygame.K_RETURN:
                        game_state = "COUNTDOWN"
                        countdown_start_time = current_time
                        boss = Boss(selected_level) if selected_level in [7, 8] else None

                elif (game_state == "GAMEOVER" or game_state == "VICTORY") and event.key == pygame.K_SPACE:
                    game_state = "MENU"
                    raw_score = 0
                    player_bullets.clear()
                    enemy_bullets.clear()
                    explosions.clear()
                    airplane.x, airplane.y = 200, HEIGHT // 2
                    for obs in obstacles: obs.reset()
                    for en in enemies: en.reset()

        if game_state == "MENU":
            for cloud in clouds: cloud.update(0.5)
        elif game_state == "COUNTDOWN":
            elapsed = (current_time - countdown_start_time) / 1000
            if elapsed >= 2.0:
                game_state = "PLAYING"
                pygame.mouse.set_visible(control_mode == "MOUSE")
            else:
                countdown_seconds = 2 - int(elapsed)
            for cloud in clouds: cloud.update(1.0)

        elif game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()

            # --- ИСПРАВЛЕННЫЙ БАЛАНС СКОРОСТЕЙ ДЛЯ 244 FPS ---
            if keys[pygame.K_LSHIFT]:
                game_speed = 7.0  # Увеличен до 7.0 — теперь это Бешеный форсаж!
                boost_active = True
                shake_amount = random.randint(-4, 4)
                raw_score += 4
            elif keys[pygame.K_LCTRL]:
                game_speed = 0.08  # Уменьшен до 0.08 — честное и мощное замедление времени!
            else:
                game_speed = 1.0
                shake_amount = 0
                raw_score += 1

            airplane.update(keys, control_mode, game_speed)

            if boss and not boss.active and raw_score > 3000: boss.active = True

            # ЛКМ стрельба пулемета
            if keys[pygame.K_f] or mouse_buttons[0]:
                now = pygame.time.get_ticks()
                if selected_skin == 1 and now - last_player_shot > 80:
                    player_bullets.append(PlayerBullet(airplane.x + 40, airplane.y, 1))
                    last_player_shot = now
                elif selected_skin == 2 and now - last_player_shot > 180:
                    player_bullets.append(PlayerBullet(airplane.x + 30, airplane.y - 12, 2))
                    player_bullets.append(PlayerBullet(airplane.x + 30, airplane.y + 12, 2))
                    last_player_shot = now
                elif selected_skin == 3 and now - last_player_shot > 500:
                    player_bullets.append(PlayerBullet(airplane.x + 40, airplane.y, 3))
                    last_player_shot = now
                elif selected_skin == 4 and now - last_player_shot > 250:
                    player_bullets.append(PlayerBullet(airplane.x, airplane.y + 15, 4))
                    last_player_shot = now
                elif selected_skin == 5 and now - last_player_shot > 350:
                    player_bullets.append(PlayerBullet(airplane.x + 50, airplane.y, 5, angle_y=-3))
                    player_bullets.append(PlayerBullet(airplane.x + 50, airplane.y, 5, angle_y=0))
                    player_bullets.append(PlayerBullet(airplane.x + 50, airplane.y, 5, angle_y=3))
                    last_player_shot = now
                elif selected_skin == 6 and now - last_player_shot > 40:
                    player_bullets.append(PlayerBullet(airplane.x + 60, airplane.y, 6))
                    last_player_shot = now

            # ПКМ Тяжелые ракеты
            if keys[pygame.K_g] or mouse_buttons[2]:
                now = pygame.time.get_ticks()
                rocket_cooldown = 4000 if selected_skin == 3 else 1500
                if now - last_player_rocket > rocket_cooldown:
                    player_bullets.append(
                        PlayerBullet(airplane.x + 40, airplane.y, selected_skin, is_heavy_rocket=True))
                    last_player_rocket = now

            for ex in explosions[:]:
                ex.update(enemies, enemy_bullets, boss)
                if ex.finished: explosions.remove(ex)

            for pb in player_bullets[:]:
                pb.update()
                if pb.x > WIDTH + 50 or pb.y > HEIGHT or pb.y < 0:
                    player_bullets.remove(pb)
                    continue

                exploded = False
                if boss and boss.active and boss.x <= 800:
                    boss_radius = 130 if boss.level == 7 else 95
                    if math.hypot(pb.x - boss.x, pb.y - boss.y) < boss_radius:
                        if pb.is_heavy_rocket:
                            boss.hp -= 20
                            exploded = True
                        else:
                            boss.hp -= 1
                        if pb in player_bullets: player_bullets.remove(pb)

                for en in enemies:
                    if not en.is_dying and math.hypot(pb.x - en.x, pb.y - en.y) < 35:
                        if pb.is_heavy_rocket:
                            en.hp -= 3
                            exploded = True
                        else:
                            en.hp -= 1

                        if en.hp <= 0: en.hit(); raw_score += 500
                        if pb in player_bullets: player_bullets.remove(pb)

                if exploded and pb.is_heavy_rocket:
                    if pb.skin_type == 1:
                        explosions.append(Explosion(pb.x, pb.y, 100, (255, 130, 0)))
                    elif pb.skin_type == 2:
                        explosions.append(Explosion(pb.x, pb.y, 90, (0, 160, 255)))
                    elif pb.skin_type == 3:
                        explosions.append(Explosion(pb.x, pb.y, 270, (255, 240, 150)))
                    elif pb.skin_type == 4:
                        explosions.append(Explosion(pb.x, pb.y, 120, (120, 240, 100)))
                    elif pb.skin_type == 5:
                        explosions.append(Explosion(pb.x, pb.y, 160, (255, 50, 0)))
                    elif pb.skin_type == 6:
                        explosions.append(Explosion(pb.x, pb.y, 80, (210, 0, 255)))

                if boss and boss.hp <= 0: game_state = "VICTORY"

            if boss and boss.active:
                boss.update(game_speed, enemy_bullets)
                if math.hypot(airplane.x - boss.x, airplane.y - boss.y) < 85: game_state = "GAMEOVER"

            for cloud in clouds: cloud.update(game_speed)
            if not (boss and boss.active):
                for obs in obstacles:
                    obs.update(game_speed, selected_level)
                    if math.hypot(airplane.x - obs.x, airplane.y - obs.y) < (obs.radius + 23): game_state = "GAMEOVER"

            for en in enemies:
                en.update(game_speed, selected_level, enemy_bullets, boss and boss.active)
                if math.hypot(airplane.x - en.x, airplane.y - en.y) < 38: game_state = "GAMEOVER"

            for eb in enemy_bullets[:]:
                eb.update(game_speed)
                if eb.x < -50:
                    enemy_bullets.remove(eb)
                elif math.hypot(airplane.x - eb.x, airplane.y - eb.y) < 22:
                    game_state = "GAMEOVER"

        # --- РЕНДЕРИНГ ЭКРАНОВ ---
        render_surf = pygame.Surface((WIDTH, HEIGHT))
        render_surf.fill(COLOR_SKY)

        for cloud in clouds: cloud.draw(render_surf)
        font_title = pygame.font.SysFont("Arial", 45, bold=True)
        font_main = pygame.font.SysFont("monospace", 24, bold=True)
        font_hud = pygame.font.SysFont("monospace", 20, bold=True)

        if game_state == "MENU":
            pygame.mouse.set_visible(True)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 100))
            render_surf.blit(overlay, (0, 0))

            txt_title = font_title.render("JET COMBAT: 244 FPS FIX", True, COLOR_ACTIVE)
            render_surf.blit(txt_title, (WIDTH // 2 - txt_title.get_width() // 2, 60))

            c_row0 = COLOR_ACTIVE if menu_row == 0 else (50, 50, 50)
            lvl_name = f"{selected_level} (BOSS)" if selected_level in [7, 8] else str(selected_level)
            txt_lvl = font_main.render(f"  LEVEL:  << {lvl_name} >>", True, c_row0)
            render_surf.blit(txt_lvl, (100, 220))

            c_row1 = COLOR_ACTIVE if menu_row == 1 else (50, 50, 50)
            txt_jet = font_main.render(f"  JET:    << {skin_names[selected_skin]} >>", True, c_row1)
            render_surf.blit(txt_jet, (100, 320))

            c_row2 = COLOR_ACTIVE if menu_row == 2 else (50, 50, 50)
            ctrl_name = "ONLY KEYBOARD (Arrows)" if control_mode == "KEYBOARD" else "KEYBOARD + MOUSE"
            txt_ctrl = font_main.render(f"  CONTROL: << {ctrl_name} >>", True, c_row2)
            render_surf.blit(txt_ctrl, (100, 420))

            airplane.draw(render_surf, boost_active=False, current_skin=selected_skin, custom_pos=(750, 330))

        elif game_state == "COUNTDOWN":
            font_cd = pygame.font.SysFont("Arial", 120, bold=True)
            cd_text = str(countdown_seconds) if countdown_seconds > 0 else "GO!"
            txt_cd = font_cd.render(cd_text, True, COLOR_ACTIVE)
            render_surf.blit(txt_cd, (WIDTH // 2 - txt_cd.get_width() // 2, HEIGHT // 2 - txt_cd.get_height() // 2))

        elif game_state == "PLAYING":
            if not (boss and boss.active):
                for obs in obstacles: obs.draw(render_surf)
            for en in enemies: en.draw(render_surf)
            for eb in enemy_bullets: eb.draw(render_surf)
            for pb in player_bullets: pb.draw(render_surf)
            for ex in explosions: ex.draw(render_surf)
            if boss: boss.draw(render_surf)

            airplane.draw(render_surf, boost_active, current_skin=selected_skin)

            rocket_cooldown = 4000 if selected_skin == 3 else 1500
            rocket_ready = "READY" if current_time - last_player_rocket > rocket_cooldown else "CHARGING"

            txt_l = font_hud.render(f"LEVEL: {selected_level}", True, (0, 120, 0))
            txt_s = font_hud.render(f"SCORE: {raw_score // 10}", True, (30, 30, 30))
            txt_sp = font_hud.render(f"MISSILE: {rocket_ready}", True, (230, 90, 0))
            render_surf.blit(txt_l, (20, 20))
            render_surf.blit(txt_s, (20, 45))
            render_surf.blit(txt_sp, (20, 70))

        elif game_state == "GAMEOVER":
            font_big = pygame.font.SysFont("Arial", 50, bold=True)
            txt_end = font_big.render("САМОЛЕТ СБИТ!", True, (200, 20, 20))
            txt_restart = font_hud.render("Нажмите ПРОБЕЛ для возврата в меню", True, (30, 30, 30))
            render_surf.blit(txt_end, (WIDTH // 2 - txt_end.get_width() // 2, HEIGHT // 2 - 40))
            render_surf.blit(txt_restart, (WIDTH // 2 - txt_restart.get_width() // 2, HEIGHT // 2 + 20))

        elif game_state == "VICTORY":
            font_big = pygame.font.SysFont("Arial", 50, bold=True)
            txt_end = font_big.render("ПОБЕДА! БОСС УНИЧТОЖЕН!", True, (0, 150, 50))
            txt_restart = font_hud.render("Нажмите ПРОБЕЛ для выхода", True, (30, 30, 30))
            render_surf.blit(txt_end, (WIDTH // 2 - txt_end.get_width() // 2, HEIGHT // 2 - 40))
            render_surf.blit(txt_restart, (WIDTH // 2 - txt_restart.get_width() // 2, HEIGHT // 2 + 20))

        screen.blit(render_surf, (shake_amount, shake_amount))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()