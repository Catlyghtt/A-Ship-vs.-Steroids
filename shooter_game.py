from pygame import *
from random import randint
from time import time as timer

#фоновая музыка
mixer.init()
mixer.music.load('ggis2.mp3')
mixer.music.play()
fire_sound = mixer.Sound('strelba-iz-drobovika.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('Зачем ты в это играешь? Да, это победа, но ради чего? И какой ценой? Ты просто тратишь свое время на мнимые победы, за которые ни в чем не выигрываешь? В чем вообще смысл твоего существования?', True, (255, 255, 255))
lose = font1.render('хахаххаха ахах хахаххахахахаххаххаххахааххаххххх!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)


#нам нужны такие картинки:
img_back = "imagee.jpg" #фон игры
img_hero = "rocket.png" #герой
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_ast = 'pills.png'


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
#конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класe)са (Sprit:
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def update(self):
       self.rect.y += self.speed
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

score = 0
lost = 0
max_lost = 3
goal = 40

#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost = lost+1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("space invaders")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 50, 100, 10)

monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 6))
    monsters.add(monster)
bullets = sprite.Group()
steroids = sprite.Group()
for i in range(1, 4):
    steroid = GameSprite(img_ast, randint(80, win_width-80), -40, 80, 50, randint(1, 7))
    steroids.add(steroid)


#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
rel_time = False
num_fire = 0
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
score = 0
while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
       #обновляем фон
       window.blit(background,(0,0))
       text = font2.render('Счет:'+str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))
       text_lose = font2.render('Пропущено:'+str(lost), 1, (255,255,255))
       window.blit(text_lose, (10, 50))

       #производим движения спрайтов
       ship.update()
       #обновляем их в новом местоположении при каждой итерации цикла
       ship.reset()
       monsters.update()
       monsters.draw(window)
       bullets.update()
       bullets.draw(window)
       steroids.update()
       steroids.draw(window)
       if rel_time == True:
           now_time = timer()
           if now_time - last_time < 1.5:
               reloads = font2.render('Downloading killbot.exe', 1, (150, 0, 0))
               window.blit(reloads, (260, 460))
           else:
               num_fire = 0
               rel_time = False
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           score += 1
           monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 6))
           monsters.add(monster)
       if sprite.spritecollide(ship, monsters, False) or lost >= max_lost or sprite.spritecollide(ship, steroids, False):
           finish = True
           window.blit(lose, (200, 200))
       if score >= goal:
            finish = True
            window.blit(win, (200, 200))

       display.update()
    #цикл срабатывает каждые 0.05 секунд
    time.delay(50)