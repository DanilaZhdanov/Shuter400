from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, scale_player_x, scale_player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (scale_player_x,scale_player_y) )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >=5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png',  10, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)



lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y>500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



window = display.set_mode((700,500))
background = transform.scale(image.load('istockphoto-471759147-612x612.jpg'), (700,500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
fon1 = font.Font(None, 80)
win = fon1.render('YOU WIN:)', True, (255, 255, 255))
lose = fon1.render('YOU LOSE:)', True, (255, 255, 255))

player = Player('58ab2c7bddc1d15a5ca5c404.png', 5, 300, 409, 80, 100)
monsters = sprite.Group()
for i in range(1, 4):
    monster = Enemy('38dfea4f5f84e2a0b2c2fe1de81c0a52.png',randint(1,2), randint(80, 620), -40, 50, 50)
    monsters.add(monster)

bullets = sprite.Group()
max_lost = 6
score = 0
goal = 10


asteroids = sprite.Group()
for i in range(1,3):
        asteroid = Enemy('719gbxlzpQL._AC_SL1500_.jpg', randint (1, 2), randint(30, 670), -40, 80, 50)
        asteroids.add(asteroid)


run = True
clock = time.Clock()
FPS = 60

finish = False

font.init()
font2 = font.SysFont(None, 36)


life = 3

rel_time = False
num_fire = 0


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire<5 and rel_time == False:
                    num_fire+=1
                    player.fire()
                    fire_sound.play()
                    if num_fire >= 5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
  

    if not finish:
        
        window.blit(background, (0,0))

        player.update()
        player.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('подожди, я перезаряжаюсь.....', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        Collides_list = sprite.groupcollide(monsters, bullets, True, True)
        for c in Collides_list:
            score +=1
            monster = Enemy('38dfea4f5f84e2a0b2c2fe1de81c0a52.png',randint(1,3), randint(80, 620), -40, 50, 50)
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            life -= 1
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)


        if sprite.spritecollide( player, monsters, False) or lost>=max_lost or life == 0:
            finish = True
            window.blit(lose, (200, 150))
        if score >= goal:
            finish = True
            window.blit(win, (200, 150))

        text = font2.render('Счёт: '+str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lost = font2.render('Пропущено: '+str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10,50))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font2.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        display.update()   


    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)    
        for i in range(1, 6):
            monster = Enemy('38dfea4f5f84e2a0b2c2fe1de81c0a52.png',randint(1,3), randint(80, 620), -40, 50, 50)
            monsters.add(monster)

    display.update()
    clock.tick(FPS)






































