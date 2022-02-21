# importing stuff

import pygame
import time
import math

# initializing pygame

pygame.init()

# defining variables

clock = pygame.time.Clock()
autog = 0
coins = 0
display_width = 800
display_height = 600
white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)
light_grey = (224, 224, 224)
light_blue = (173, 216, 230)
blue = (0, 100, 250)

# creating display and caption

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Кликер")


# defining functions
def circle(display, text1, color, x, y, radius):
    pygame.draw.circle(display, (255, 255, 0), (400, 260), 80, 10)
    coin_surface = pygame.Surface((160, 160)).get_rect()
    set_text(coin_surface, text1)
    pygame.draw.circle(display, (128, 128, 0), (400, 260), 75)


# Функция устанавливающая надпись на кнопке
def set_text(surface, text, font_size=72):
    font_text = pygame.font.SysFont("Consolas", font_size)
    text_result = font_text.render(text, True, white)
    gameDisplay.blit(text_result, text_result.get_rect(center=surface.center))
    return text_result.get_rect(center=surface.center)


def autoclicker():
    global coins
    global autog
    time.sleep(0.1)
    coins = coins + autog


def DrawText(text, Textcolor, Rectcolor, x, y, fsize):
    font = pygame.font.Font('freesansbold.ttf', fsize)
    text = font.render(text, True, Textcolor, Rectcolor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(text, textRect)


def rectangle(display, color, x, y, w, h):
    pygame.draw.rect(display, color, (x, y, w, h))


def main_loop():
    global clock
    global autog
    global ver
    global color1
    global color2
    global color3
    mong = 1
    cost = 50
    cost2 = 50
    global coins
    game_running = True
    while game_running:
        if game_running:
            autoclicker()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mopos = pygame.mouse.get_pos()
                if mopos >= (350, 0):
                    if mopos <= (450, 0):
                        coins += mong

                if mopos <= (800, 0):
                    if mopos >= (600, 0):
                        if coins >= cost:
                            coins = coins - cost
                            cost = cost * 1.5
                            mong = mong * 1.1
                            cost = round(cost, 0)

                if mopos >= (50, 0):
                    if mopos <= (245, 0):
                        if coins >= cost2:
                            coins = coins - cost2
                            cost2 = cost2 * 1.5
                            autog = autog + 0.5
                            cost2 = round(cost2, 0)

                if coins == 6666666:
                    print("Поздравляем! Вы прошли игру!")
                    game_running = False


        gameDisplay.fill(light_blue)
        DrawText("Кликер", black, light_blue, 400, 100, 50)
        DrawText("У вас " + str(f'{coins:.2f}') + " монет", black, light_blue, 100, 50, 20)
        DrawText("Улучшить кликер " + str(cost), black, light_blue, 700, 300, 20)
        DrawText("Купить автокликер " + str(cost2), black, light_blue, 150, 370, 20)
        rectangle(gameDisplay, blue, 50, 400, 200, 300)
        circle(gameDisplay, str(mong), blue, 400, 260, 60)
        rectangle(gameDisplay, blue, 600, 317, 200, 300)
        pygame.display.update()
        clock.tick(60)


class Coin(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Coin, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.width = self.rect.width
        self.height = self.rect.height
        self.set_position()

    def set_position(self):
        self.rect.x = self.x
        self.rect.y = self.y


main_loop()
pygame.quit()
quit()