from pygame import *
from random import randint
from time import time as timer

clock = time.Clock() 
FPS = 60
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

score = 0 
goal = 16 
lost = 0 
max_lost = 16 
life = 5

#шрифты и надписи
font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 100) 
font3 = font.SysFont('Arial', 100)
win = font1.render('YOU WIN!', True, (0, 255, 0)) 
lose = font1.render('YOU LOSE!', True, (255, 0, 0))
#life1 = font1.render(life, True, (255, 0, 0))

# нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_bullet = "bullet.png"
img_asteroid = "asteroid.png"

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = 3

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed 
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


# класс спрайта-врага   
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += 2#self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):  
    def update(self): 
        self.rect.y -= 4
        if self.rect.y < 5:
            self.kill()

# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
# создаем спрайты
ship = Player(img_hero, 300, win_height - 100, 80, 100, 10)
bullet = Bullet(img_bullet, 327, 400, 30, 30, 1)

monsters = sprite.Group()
for i in range(1, 2):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
    asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
    monsters.add(monster)
    monsters.add(asteroid)

bullets = sprite.Group()

# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна

rel_time = False
num_fire = 0

while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 15 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 15 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        # обновляем фон
        window.blit(background,(0,0))

        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        #bullet.reset()
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 55))
        
        text_life =  font3.render(str(life), 1, (0, 255, 0))
        window.blit(text_life, (650, 10))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            monsters.add(monster)
            monsters.add(asteroid)

        if sprite.spritecollide(ship, monsters, False): #or lost >= max_lost:
            sprite.spritecollide(ship, monsters, True)
            life = life - 1
            #finish = True
            #window.blit(lose, (200, 200))
        if life == -1 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
        #time.delay(40)
        clock.tick(FPS)