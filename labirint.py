from pygame import *
init()
finish = False
run = True
back = (200, 255, 255) 
W = 700
H = 500
window = display.set_mode((W, H))
FPS = 60
window.fill(back)
display.set_caption('I.N.')
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        pl_td = sprite.spritecollide(self, brs, False)
        if self.x_speed > 0:
            for p in pl_td:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in pl_td:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        pl_td = sprite.spritecollide(self, brs, False)
        if self.y_speed > 0:
            for p in pl_td:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in pl_td:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('weapon.png', 30, 10, self.rect.right, self.rect.centery, 20)
        bullet.reset()
        bul.add(bullet)

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        if self.rect.x <= 550:
            self.direction = 'right'       
            if self.rect.x >= 400:
                self.direction = 'left'
            if self.direction == 'left':
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > W + 10:
            self.kill()

game_over = transform.scale(image.load('oh.png'), (700, 500))
win = transform.scale(image.load('thumb.png'), (700, 500))
player = Player('hero.png', 80, 80, 5, 400, 0, 0)
final = GameSprite('enemy2.png', 60, 90, 500, 300)
wall_3 = GameSprite('wall.png', 40, 50, 100, 700)
wall_1 = GameSprite('wall.png', 40, 500, 250, 150)
wall_2 = GameSprite('wall.png', 150, 40, 100, 250)
wall_3 = GameSprite('wall.png', 700, 5, 0, -5)
wall_4 = GameSprite('wall.png', 700, 5, 0, 500)
wall_5 = GameSprite('wall.png', 5, 700, -5, 0)
wall_6 = GameSprite('wall.png', 5, 700, 705, 0)
monster = Enemy('enemy.png', 100, 100, 300, 90, 10)
mon = sprite.Group()
mon.add(monster)
bul = sprite.Group()
brs = sprite.Group()
brs.add(wall_1)
brs.add(wall_2)
brs.add(wall_3)
brs.add(wall_4)
brs.add(wall_5)
brs.add(wall_6)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                player.y_speed = -5
            if e.key == K_DOWN:
                player.y_speed = 5
            if e.key == K_RIGHT:
                player.x_speed = 5
            if e.key == K_LEFT:
                player.x_speed = -5
            if e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_UP:
                player.y_speed = 0
            if e.key == K_DOWN:
                player.y_speed = 0
            if e.key == K_RIGHT:
                player.x_speed = 0
            if e.key == K_LEFT:
                player.x_speed = 0
    if finish == False:
        window.fill(back)
        player.reset()
        mon.draw(window)
        final.reset()
        wall_1.reset()
        wall_2.reset()
        wall_3.reset()
        wall_4.reset()
        wall_5.reset()
        wall_6.reset()
        player.update()
        monster.update()
        bul.update()
        bul.draw(window)
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (0, 0))
        if sprite.spritecollide(player, mon, False):
            finish = True
            window.blit(game_over, (0, 0))
        sprite.groupcollide(mon, bul, True, True)
        sprite.groupcollide(bul, brs, True, False)
    time.delay(50)
    display.update()