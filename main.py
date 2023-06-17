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

fon = pygame.image.load(file_path(r"images\background.png"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))


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
        self.rect.x += self.speedx
        self.rect.y += self.speedy

player = Player(50, 250, 50, 50, r"images\player.png", 0, 0)
enemy1 = GameSprite(340, 260, 30, 30, r"images\enemy.png")
enemy2 = GameSprite(530, 360, 30, 30, r"images\enemy.png")
enemy3 = GameSprite(800, 460, 30, 30, r"images\enemy.png")
finish = GameSprite(785, 60, 50, 50, r"images\chest.png")

walls = pygame.sprite.Group()
wall = GameSprite(10, 220, 20, 110, r"images\fall.png")
wall1 = GameSprite(20, 220, 300, 20, r"images\fall.png")
wall2 = GameSprite(20, 310, 300, 20, r"images\fall.png")
wall3 = GameSprite(300, 310, 20, 200, r"images\fall.png")
wall4 = GameSprite(300, 40, 20, 200, r"images\fall.png")
wall5 = GameSprite(300, 510, 550, 20, r"images\fall.png")
wall6 = GameSprite(300, 20, 550, 20, r"images\fall.png")
wall7 = GameSprite(390, 420, 200, 20, r"images\fall.png")
wall8 = GameSprite(850, 20, 20, 510, r"images\fall.png")
wall9 = GameSprite(390, 110, 270, 20, r"images\fall.png")
wall10 = GameSprite(750, 20, 20, 200, r"images\fall.png")
wall11 = GameSprite(550, 200, 200, 20, r"images\fall.png")
wall12 = GameSprite(550, 110, 20, 100, r"images\fall.png")
wall13 = GameSprite(390, 110, 20, 130, r"images\fall.png")
wall14 = GameSprite(390, 310, 20, 40, r"images\fall.png")
wall15 = GameSprite(390, 310, 200, 20, r"images\fall.png")
wall16 = GameSprite(660, 220, 20, 110, r"images\fall.png")
wall17 = GameSprite(470, 200, 20, 120, r"images\fall.png")
wall18 = GameSprite(760, 310, 100, 20, r"images\fall.png")
wall19 = GameSprite(670, 420, 200, 20, r"images\fall.png")
wall20 = GameSprite(500, 320, 20, 120, r"images\fall.png")
walls.add(wall, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8
, wall9, wall10, wall11, wall12, wall13, wall14, wall15, wall16, wall17, wall18, wall19, wall20)

level = 1
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    player.speedx = 0
                if event.key == pygame.K_a:
                    player.speedx = 0
                if event.key == pygame.K_s:
                    player.speedy = 0
                if event.key == pygame.K_w:
                    player.speedy = 0


    if level == 1:
        window.blit(fon, (0, 0))
        player.show()
        player.update()
        enemy1.show()
        enemy2.show()
        enemy3.show()
        finish.show()
        walls.draw(window)

    clock.tick(FPS)
    pygame.display.update()
  

