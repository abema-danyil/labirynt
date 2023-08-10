import pygame
import os 
pygame.init()

def file_path(file_name):
    folder = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder, file_name)
    return path


WIN_WIDTH = 900
WIN_HEIGHT = 600
FPS = 40
WHITE = (255, 255, 255)
YELLOW = (228, 206, 41)
BLUE = (65, 59, 255)
GREEN = (58, 115, 36)
DARK_RED = (203, 9, 9)

fon = pygame.image.load(file_path(r"images\background.png"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

image_menu = pygame.image.load(file_path(r"images\background_menu.png"))
image_menu = pygame.transform.scale(image_menu, (WIN_WIDTH, WIN_HEIGHT))

image_win = pygame.image.load(file_path(r"images\background_win.png"))
image_win = pygame.transform.scale(image_win, (WIN_WIDTH, WIN_HEIGHT))

image_lose = pygame.image.load(file_path(r"images\background_lose.png"))
image_lose = pygame.transform.scale(image_lose, (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(file_path(r"music\fon_music_menu.ogg"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

music_shot = pygame.mixer.Sound(file_path(r"music\rezkiy-zamah.ogg"))
music_shot.set_volume(0.4)

game_name = pygame.font.SysFont("monaco", 100, 1).render("Teraria", True, GREEN)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (width, height))
        
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, width, height, image, speedx, speedy):
        super().__init__(x, y, width, height, image)
        self.speedx = speedx
        self.speedy = speedy
        self.direction = "right"
        self.image_r = self.image
        self.image_l = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.speedx < 0 and self.rect.left > 0 or self.speedx > 0 and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speedx
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speedx < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)
        elif self.speedx > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        
        if self.speedy < 0 and self.rect.top > 0 or self.speedy > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speedy
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speedy < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        elif self.speedy > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
    
    def shot(self):
        if self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 10, 10, r"images\stone.png", 8)
        elif self.direction == "left":
            bullet = Bullet(self.rect.left - 10, self.rect.centery, 10, 10, r"images\stone.png", -8)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, x, y, width, height, image, min_cord, max_cord, direction, speed):
        super().__init__(x, y, width, height, image)
        self.min_cord = min_cord
        self.max_cord = max_cord
        self.direction = direction
        self.speed = speed

    def update(self):
        if self.direction == "left" or self.direction == "right":
            if self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed

            if self.rect.right >= self.max_cord:
                self.direction = "left"
            elif self.rect.left <= self.min_cord:
                self.direction = "right"

        elif self.direction == "up" or self.direction == "down":
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed

            if self.rect.top <= self.min_cord:
                self.direction = "down"
            elif self.rect.bottom >= self.max_cord:
                self.direction = "up"

class Bullet(GameSprite):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, height, image)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.left >= WIN_WIDTH or self.rect.right <= 0:
            self.kill()

class Button():
    def __init__(self, x, y, width, height, color_btn, color_collide, color_text, text, text_size, px, py):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_btn = color_btn
        self.color_collide = color_collide
        self.color = color_btn
        font = pygame.font.SysFont("Arial", text_size)
        self.text = font.render(text, True, color_text)
        self.px = px
        self.py = py

    def show(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.rect.x + self.px, self.rect.y + self.py))
 
btn_start = Button(200, 350, 200, 80, BLUE, DARK_RED, YELLOW, "START", 70, 10, 0)
btn_exit = Button(490, 350, 200, 80, BLUE, DARK_RED, YELLOW, " EXIT", 70, 10, 0)

bullets = pygame.sprite.Group()

player = Player(50, 250, 50, 50, r"images\player.png", 0, 0)

enemys = pygame.sprite.Group()
enemy1 = Enemy(340, 260, 30, 30, r"images\enemy.png", 60, 500, "down", 7)
enemy2 = Enemy(530, 360, 30, 30, r"images\enemy.png", 530, 850, "right", 5)
enemy3 = Enemy(800, 460, 30, 30, r"images\enemy.png", 320, 800, "left", 4)
enemy4 = Enemy(100, 480, 30, 30, r"images\enemy.png", 340, 500, "up", 2.5)
enemy5 = Enemy(140, 470, 30, 30, r"images\enemy.png", 340, 500, "up", 2.5)
enemy6 = Enemy(180, 460, 30, 30, r"images\enemy.png", 340, 500, "up", 2.5)
enemy7 = Enemy(250, 150, 30, 30, r"images\enemy.png", 60, 320, "down", 8)
enemy8 = Enemy(60, 60, 30, 30, r"images\enemy.png", 30, 750, "right", 8)
enemy9 = Enemy(690, 60, 30, 30, r"images\enemy.png", 60, 420, "down", 6)
enemys.add(enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8, enemy9)

finish = GameSprite(785, 60, 50, 50, r"images\chest.png")

key = GameSprite(250, 470, 40, 20, r"images\key.png")

wall_key = GameSprite(750, 150, 110, 20, r"images\fall.png")

walls = pygame.sprite.Group()
wall = GameSprite(10, 220, 20, 110, r"images\fall.png")
wall1 = GameSprite(20, 20, 300, 20, r"images\fall.png")
wall2 = GameSprite(20, 510, 300, 20, r"images\fall.png")
wall3 = GameSprite(300, 310, 20, 40, r"images\fall.png")
wall4 = GameSprite(300, 110, 20, 130, r"images\fall.png")
wall5 = GameSprite(300, 510, 550, 20, r"images\fall.png")
wall6 = GameSprite(300, 20, 550, 20, r"images\fall.png")
wall7 = GameSprite(390, 420, 200, 20, r"images\fall.png")
wall8 = GameSprite(850, 20, 20, 510, r"images\fall.png")
wall9 = GameSprite(390, 110, 270, 20, r"images\fall.png")
wall10 = GameSprite(750, 20, 20, 200, r"images\fall.png")
wall11 = GameSprite(550, 200, 130, 20, r"images\fall.png")
wall12 = GameSprite(550, 110, 20, 100, r"images\fall.png")
wall13 = GameSprite(390, 110, 20, 130, r"images\fall.png")
wall14 = GameSprite(390, 310, 20, 40, r"images\fall.png")
wall15 = GameSprite(390, 310, 200, 20, r"images\fall.png")
wall16 = GameSprite(660, 220, 20, 110, r"images\fall.png")
wall17 = GameSprite(470, 200, 20, 120, r"images\fall.png")
wall18 = GameSprite(760, 310, 100, 20, r"images\fall.png")
wall19 = GameSprite(670, 420, 200, 20, r"images\fall.png")
wall20 = GameSprite(500, 320, 20, 120, r"images\fall.png")
wall21 = GameSprite(10, 320, 20, 210, r"images\fall.png")
wall22 = GameSprite(10, 20, 20, 200, r"images\fall.png")
wall23 = GameSprite(300, 420, 20, 90, r"images\fall.png")
wall24 = GameSprite(100, 310, 200, 20, r"images\fall.png")
wall25 = GameSprite(100, 110, 20, 130, r"images\fall.png")
wall26 = GameSprite(110, 220, 120, 20, r"images\fall.png")
wall27 = GameSprite(100, 110, 130, 20, r"images\fall.png")
wall28 = GameSprite(300, 420, 20, 90, r"images\fall.png")
walls.add(wall, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8
, wall9, wall10, wall11, wall12, wall13, wall14, wall15, wall16, wall17, wall18, wall19, wall20, wall21, wall22, wall23, wall24, wall25, wall26, wall27)

level = 0
game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if level == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.speedx = 4
                    player.direction = "right"
                    player.image = player.image_r
                if event.key == pygame.K_a:
                    player.speedx = -4
                    player.direction = "left"
                    player.image = player.image_l
                if event.key == pygame.K_s:
                    player.speedy = 4
                if event.key == pygame.K_w:
                    player.speedy = -4
                if event.key == pygame.K_SPACE:
                    player.shot( )
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    player.speedx = 0
                if event.key == pygame.K_a:
                    player.speedx = 0 
                if event.key == pygame.K_s:
                    player.speedy = 0
                if event.key == pygame.K_w:
                    player.speedy = 0
                music_shot.play()
        
        elif level == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if btn_start.rect.collidepoint(x, y):
                    btn_start.color = btn_start.color_collide
                elif btn_exit.rect.collidepoint(x, y):
                    btn_exit.color = btn_exit.color_collide
                else:
                    btn_start.color = btn_start.color_btn
                    btn_exit.color = btn_exit.color_btn
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if btn_start.rect.collidepoint(x, y):
                    level = 1
                elif btn_exit.rect.collidepoint(x, y):
                    game = False

        elif level == 11:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if btn_exit.rect.collidepoint(x, y):
                    btn_exit.color = btn_exit.color_collide
                else:
                    btn_exit.color = btn_exit.color_btn
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if btn_exit.rect.collidepoint(x, y):
                    game = False

        elif level == 10:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if btn_exit.rect.collidepoint(x, y):
                    btn_exit.color = btn_exit.color_collide
                else:
                    btn_exit.color = btn_exit.color_btn
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if btn_exit.rect.collidepoint(x, y):
                    game = False

    if level == 1:
        window.blit(fon, (0, 0))
        player.show()
        player.update()
        enemys.draw(window)
        enemys.update()
        finish.show()
        walls.draw(window)
        bullets.draw(window)
        bullets.update()
        key.show()
        wall_key.show()

        if pygame.sprite.collide_rect(player, finish):
            level = 10
            pygame.mixer.music.load(file_path(r"music\win_game.ogg"))
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
        
        if pygame.sprite.spritecollide(player, enemys, False):
            level = 11
            pygame.mixer.music.load(file_path(r"music\fail_game.ogg"))
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)

        pygame.sprite.groupcollide(bullets, walls, True, False)

        pygame.sprite.groupcollide(bullets, enemys, True, True)
        
    elif level == 0:
        window.blit(image_menu, (0, 0))
        window.blit(game_name, (300, 100))
        btn_start.show()
        btn_exit.show()
        
    elif level == 10:
        window.blit(image_win, (0, 0))
        btn_exit.show()

    elif level == 11:
        window.blit(image_lose, (0, 0))
        btn_exit.show()

    clock.tick(FPS)
    pygame.display.update()
  

