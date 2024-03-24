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
   

game = True
finish = False


clock = time.Clock()
FPS = 60

racket1 = Player(K_w, K_s, 'racket.png',30, 200, 50, 150, 4)
racket2 = Player(K_UP, K_DOWN, 'racket.png',520, 200, 50, 150, 4)



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
    if finish != True:
        window.fill(back)
        racket1.update()
        racket2.update()
        
        racket1.reset()
        racket2.reset()


    display.update()
    clock.tick(FPS)
