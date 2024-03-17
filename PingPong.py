from pygame import *
from random import randint 
from time import time as timer

window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(700,500))
window.blit(background,(0,0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        global bullets
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        fire_sound.play()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    

mixer.init()
mixer.music.load('Mesmerizing Galaxy Loop.mp3')
mixer.music.set_volume(0.1)
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.1)

rel_time = False
num_fire = 0
hp = 100
lost = 0
death = 0
player = Player('rocket.png', 300, 380,80,120, 10)


monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for _ in range(6):
    monster = Enemy('ufo.png',randint(80,620), -40, 100, 60, randint(2,6))
    monsters.add(monster)
for _ in range(3):
    asteroid = Enemy('asteroid.png',randint(80,620), -40, 100, 60, randint(2,3))
    asteroids.add(asteroid)

font.init()
font1 = font.Font(None,36)
font2 = font.Font(None,60)
text_lose1 = font2.render('Вы проиграли!', 1 , (255,0,0))
text_win = font2.render('Вы выиграли!', 1 , (255,0,0))
text_reload = font1.render('Wait, reload... ', 1, (255 ,0,0))

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5:
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = timer()
            
    if finish != True:
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
 
        collides = sprite.groupcollide(monsters,bullets, True, True)
        
        for c in collides:
            death += 1
            monster = Enemy('ufo.png',randint(80,620), -40, 100, 60, randint(2,4))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, True):
            hp -= 25
            monster = Enemy('ufo.png',randint(80,620), -40, 100, 60, randint(2,4))
            monsters.add(monster)
        if sprite.spritecollide(player, asteroids, True):
            hp -= 15
            asteroid = Enemy('asteroid.png',randint(80,620), -40, 100, 60, randint(2,4))
            asteroids.add(asteroid)

        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255 ,255,255))
        text_time = font1.render('Убито: ' + str(death), 1, (255 ,255,255))
        text_hp = font1.render('Жизней: ' + str(hp), 1, (255 ,255,255))

        window.blit(background,(0,0))

        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        
        player.reset()

        if death >= 10:
            finish = True
            window.blit(text_win,(225,250))      
        if lost >= 10 or hp <= 0:
            finish = True
            window.blit(text_lose1,(225,250))

        if rel_time == True:
            now = timer()
            if now - start < 3:
               window.blit(text_reload,(310,410))
            else:
                num_fire = 0
                rel_time = False
        
        window.blit(text_lose,(0,0))
        window.blit(text_time,(0,30))
        window.blit(text_hp,(0,60))
        
        display.update()
    else:
        finish = False
        num_fire = 0
        hp = 100
        lost = 0
        death = 0

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        
        time.delay(2000)
        for _ in range(6):
            monster = Enemy('ufo.png',randint(80,620), -40, 100, 60, randint(2,6))
            monsters.add(monster)
        for _ in range(3):
            asteroid = Enemy('asteroid.png',randint(80,620), -40, 100, 60, randint(2,3))
            asteroids.add(asteroid) 
    
    
    time.delay(20)
