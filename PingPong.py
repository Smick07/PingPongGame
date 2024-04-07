from pygame import *

back = (200,255,255)
WIDTH = 600
HEIGHT = 500
window = display.set_mode((WIDTH, HEIGHT))
window.fill(back)

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
    def __init__(self, button_up, button_down, *args):
        self.button_up = button_up
        self.button_down = button_down
        super().__init__(*args)

    
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[self.button_up] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[self.button_down] and self.rect.y < HEIGHT - 155:
            self.rect.y += self.speed
   

score1 = 0
score2 = 0
game = True
finish = False


clock = time.Clock()
FPS = 60

racket1 = Player(K_w, K_s, 'racket.png',30, 200, 30, 150, 4)
racket2 = Player(K_UP, K_DOWN, 'racket.png',520, 200, 30, 150, 4)
ball = GameSprite('tenis_ball.png', HEIGHT/2-25, WIDTH/2-25, 40, 40, 4)

speed_x = 4
speed_y = 4

font.init()
font1 = font.Font(None, 35)
font2 = font.Font(None, 30)
lose1 = font1.render('PLAYER LEFT LOSE!', True, (0,0,0))
lose2 = font1.render('PLAYER RIGHT LOSE!', True, (0,0,0))


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
    if finish != True:
        
        window.fill(back)
        
        racket1.update()
        racket2.update()

        ball.rect.x += speed_x
        ball.rect.y += speed_y
        
        if ball.rect.y < 0 or ball.rect.y > HEIGHT-50:
            speed_y *= -1
        
        if sprite.collide_rect(racket1, ball):
            racket2.speed += 0.4
            speed_x *= -1
            speed_x += 0.8
        
        if sprite.collide_rect(racket2, ball):
            racket1.speed += 0.4
            speed_x *= -1
            
            speed_x -= 0.8
            
        if ball.rect.x < 0:
            score2 += 1
            ball.rect.y = HEIGHT/2-25
            ball.rect.x = WIDTH/2-25
            speed_x = 4
            speed_y = 4
            print(score1, score2)
            
        if ball.rect.x > WIDTH-50:
            score1 += 1
            ball.rect.y = HEIGHT/2-25
            ball.rect.x = WIDTH/2-25
            speed_x = 4
            speed_y = 4
            print(score1, score2)
            
        score1_txt = font2.render(str(score1), True, (0,0,0))
        score2_txt = font2.render(str(score2), True, (0,0,0))
        
        window.blit(score1_txt, (WIDTH/2-20,20))
        window.blit(score2_txt, (WIDTH/2+20,20))


        if score2 >= 2:
            finish = True
            window.blit(lose1, (200,200))
        if score1 >= 2:
            finish = True
            window.blit(lose2, (200,200))

        racket1.reset()
        racket2.reset()
        ball.reset()

    else:
        time.delay(1000)
        speed_x = 4
        speed_y = 4
        ball.rect.y = HEIGHT/2-25
        ball.rect.x = WIDTH/2-25
        score1 = 0
        score2 = 0
        finish = False

    display.update()
    clock.tick(FPS)
