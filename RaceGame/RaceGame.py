import random

import pygame
import pygame.freetype

import itertools
import threading
import time
import sys
done = False

#установка разрешения для игры, времени и названия окна
pygame.init()
clock = pygame.time.Clock()
size = pygame.display.set_mode((600, 1000))
pygame.display.set_caption("ШашкиRace")

#загрузка фоток машин и границ в игру
player = pygame.image.load("car_player.png")
bg = pygame.image.load("bg_road.jpg")
otboynikL = pygame.image.load("otboynik.png")
otboynikR = pygame.image.load("otboynik.png")
npc_car1 = pygame.image.load("npc_car2.png")
npc_car2 = pygame.image.load("npc_car2.png")
npc_car3 = pygame.image.load("npc_car3.png")
npcS_car1 = pygame.image.load("npcS_car2.png")
npcS_car2 = pygame.image.load("npcS_car2.png")
npcS_car3 = pygame.image.load("npcS_car3.png")

#установка картинок по местам на карте
player_rect = player.get_rect()
otboynikL_rect = otboynikL.get_rect()
otboynikR_rect = otboynikR.get_rect()
player_rect.center = (300, 900)
otboynikL_rect.center = (50, 500)
otboynikR_rect.center = (550, 500)
font = pygame.freetype.Font(None, 30)

#назначение скорости машины и опыта
global player_speed
player_speed = 0
go = 0.27
move = 6
global run
run = True
score = 0
tst = 3000
tstS = 6000

bgs = []
bgs.append(pygame.Rect(0,0, 600,1000))

#скорость спавна трафика
trafic_group = pygame.sprite.Group()
traficS_group = pygame.sprite.Group()
spawn_trafic_event = pygame.USEREVENT + 0
pygame.time.set_timer(spawn_trafic_event, 3500)
#spawn_traficS_event = pygame.USEREVENT + 1
#pygame.time.set_timer(spawn_traficS_event, 6000)

game_status = True

def reset():
    global score, paused, run

    player_speed = 0
    player_rect = 0

    score = 0
    paused = False
    run = True
    game_status = True

class Trafic(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        global game_status
        self.rect.y += 15 #скорость встречных авто
        if self.rect.colliderect(player_rect):   #Условия проигрыша
            game_status = False
        elif otboynikR_rect.colliderect(player_rect) or otboynikL_rect.colliderect(player_rect):
            game_status = False
class TraficS(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        global game_status
        self.rect.y += 12 #скорость попутных авто
        if self.rect.colliderect(player_rect): #условия проигрыша
            game_status = False
        elif otboynikR_rect.colliderect(player_rect) or otboynikL_rect.colliderect(player_rect):
            game_status = False

reset()

#Спавн трафика на полосе и обозначение кнопок управления
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == spawn_trafic_event:
            trafic = Trafic((random.choice([155, 250]), random.choice([-1500])), npc_car1)       #350, 440
            trafic_group.add(trafic)
            trafic = Trafic((random.choice([155, 250]), random.choice([-500])), npc_car2)
            trafic_group.add(trafic)
            trafic = Trafic((random.choice([155, 250]), random.choice([-2000])), npc_car3)
            trafic_group.add(trafic)
            trafic = TraficS((random.choice([350, 440]), random.choice([-1500])), npcS_car1)  # 350, 440
            trafic_group.add(trafic)
            trafic = TraficS((random.choice([350, 440]), random.choice([-2000])), npcS_car2)
            trafic_group.add(trafic)
            trafic = TraficS((random.choice([350, 440]), random.choice([-500])), npcS_car3)
            trafic_group.add(trafic)
    if game_status == True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player_rect.centerx += move
        if keys[pygame.K_a]:
            player_rect.centerx -= move
        if keys[pygame.K_w]:
            player_speed -= go
        if keys[pygame.K_s]:
            player_speed += go
        if player_rect.y < 0:
            player_rect.y = 0
            player_speed = 0
        if player_rect.y > 900:
            player_rect.y = 900
            player_speed = 0
        if keys[pygame.K_r]:
            reset()

        player_rect.centery += int(player_speed)
        score += 1
        if score == 1000:
            tst = tst - 500
            tstS = tstS - 500
        if score == 5000:
            tst = tst - 500
            tstS = tstS - 500
        if score == 10000:
            tst = tst - 500
            tstS = tstS - 500

        for bgi in bgs:
            size.blit(bg, bgi)
        size.blit(player, player_rect)
        size.blit(otboynikL, otboynikL_rect)
        size.blit(otboynikR, otboynikR_rect)
        trafic_group.draw(size)
        trafic_group.update()

    else:
        font.render_to(size,(100, 500), f"Разбился!Ваш рейтинг: {score}", (200, 0, 0)) #условия при проигрыше

    font.render_to(size, (200, 10), f"Ваш рейтинг: {score}", (0, 0, 0))


    pygame.display.update()
    clock.tick(60)





pygame.quit()
