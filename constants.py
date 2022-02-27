# Библиотеки, константы для игры, глобальные функции и переменные


import pygame  # Основная библиотека (Движок игры)
import os  # Библиотека для работы с операционной системой
import sys  # Библиотека для работы с файлами
import random  # Библиотека для работы со случайными значениями
import sqlite3  # Библиотека для работы с БД
import string  # Библиотека для работы со строками


# ГЛОБАЛЬНЫЕ ФУНКЦИИ


# Функция выключения
def terminate():
    pygame.quit()
    sys.exit()


# Функция загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('./data/images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Функция, вырезающая кадры со спрайт-листа
def cut_sheet(sheet, columns, rows, obj_width, obj_height):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            image = pygame.transform.scale(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)), (obj_width, obj_height))
            image = image.convert_alpha()
            frames.append(image)
    return frames


# Затухание экрана (Передаётся задержка)
def transition(delay=15):
    for size in range(40):
        black_rect = pygame.Surface((1024, 20 * size))  # - переход сверху - вниз
        black_rect.fill(BLACK)
        screen.blit(black_rect, (black_rect.get_rect(center=screen.get_rect().center)))
        pygame.display.flip()
        pygame.time.delay(delay)


def get_data():
    update_connection()
    sql_request = "SELECT * FROM saves"
    data = [list(j) for j in [i for i in cursor.execute(sql_request)]]
    return data


def get_info(identifier):
    update_connection()
    sql_request = f"SELECT * FROM saves WHERE ID = '{identifier}'"
    info = [list(j) for j in [i for i in cursor.execute(sql_request)]]
    return info[0]


# Функция создания нового профиля для сохранения прогресса
def create_account(name=""):
    update_connection()
    identifier = generate_id(LENGTH_ID)
    sql_request = f"INSERT INTO " \
                  f"saves(ID,NAME,MAX_SCORE,AUTO_INCOME,CLICKER,FARMER,FARM1,SUPER_FARM,ACHIEVEMENTS) " \
                  f"VALUES('{identifier}','{name}',0,0,1,0,0,0,'11111')"
    cursor.execute(sql_request)
    connection.commit()
    update_connection()
    return identifier


# Функция обновления базы данных (сохранение прогресса)
def update_db(identifier, max_score, auto_income, incomes, achievements_states):
    update_connection()
    sql_requests = [f"UPDATE saves SET MAX_SCORE = '{max_score}' WHERE ID = '{identifier}'",
                    f"UPDATE saves SET AUTO_INCOME = {auto_income} WHERE ID = '{identifier}'",
                    f"UPDATE saves SET CLICKER = {incomes['clicker']} WHERE ID = '{identifier}'",
                    f"UPDATE saves SET FARMER = {incomes['farmer']} WHERE ID = '{identifier}'",
                    f"UPDATE saves SET FARM1 = {incomes['farm1']} WHERE ID = '{identifier}'",
                    f"UPDATE saves SET SUPER_FARM = {incomes['farm2']} WHERE ID = '{identifier}'",
                    f"UPDATE saves SET ACHIEVEMENTS = '{achievements_states}' WHERE ID = '{identifier}'"]
    for sql_request in sql_requests:
        cursor.execute(sql_request)
    connection.commit()


def generate_id(length):
    letters = string.ascii_lowercase
    sql_request = "SELECT ID FROM saves"
    identifiers = [str(*i) for i in cursor.execute(sql_request)]
    rand_string = ''.join(random.choice(letters) for _ in range(length)).upper()
    while rand_string in identifiers:
        rand_string = ''.join(random.choice(letters) for _ in range(length)).upper()
    return rand_string


# Функция устанавливающая надпись на кнопке
def set_text(surface, text, font_size, centerize=True,
             x_offset=0, y_offset=0,
             is_screen=False, color=(255, 255, 255)):
    font_text = pygame.font.Font("./data/fonts/BIP.ttf", font_size)
    text_result = font_text.render(text, True, color)
    if is_screen:
        text_result_center = text_result.get_rect(center=screen.get_rect().center)
        if centerize:
            screen.blit(text_result, text_result_center)
        else:
            screen.blit(text_result, (text_result_center.x + x_offset,
                                      text_result_center.y + y_offset))
    else:
        text_result_center = text_result.get_rect(center=surface.rect.center)
        if centerize:
            screen.blit(text_result, text_result_center)
        else:
            screen.blit(text_result, (text_result_center.x + x_offset,
                                      text_result_center.y + y_offset))
        return text_result.get_rect(center=surface.rect.center)


def update_connection():
    connection = sqlite3.connect("./data/databases/saves.sqlite")
    cursor = connection.cursor()


# ОБЪЯВЛЕНИЕ КОНСТАНТ

FPS = 60  # Кадры в секунду (Frame Per Second)
WHITE = pygame.Color("white")  # Белый цвет
BLACK = pygame.Color("black")  # Чёрный цвет
GOLD = (139, 117, 0)  # Золотистый цвет
WARNING = (204, 51, 0)  # Цвет предупреждения
RED = (101, 43, 21)  # Красный (бордовый)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = 1024, 683  # Размеры экрана
SCALE_COEFFICIENT = 1.2  # Коэффициент увеличения объектов
GRAVITY = 1  # Гравитация частиц
LENGTH_ID = 8  # Длина генерируемого идентификатора игрока
ACCEPTED_SYMBOLS = "abcdefghijklmnopqrstuvwxyz" \
                   "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                   "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" \
                   "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" \
                   "0123456789 _"  # Символы которые игрок может вписывать в поле ввода имени
MAX_TEXT_LENGTH = 11  # Максимальная длина имени
MIN_TEXT_LENGTH = 5  # Минимальная длина имени

screen = pygame.display.set_mode(SCREEN_SIZE)  # Объект экрана
clock = pygame.time.Clock()  # Объект часов для отрисовки кадров
connection = sqlite3.connect("./data/databases/saves.sqlite")  # Подключение к базе данных
# с сохранёнными играми
cursor = connection.cursor()  # Курсор подключения для работы с БД
all_sprites = pygame.sprite.Group()  # Группа всех спрайтов
buttons = pygame.sprite.Group()  # Группа спрайтов кнопок
achievements = pygame.sprite.Group()  # Группа спрайтов достижений
info_labels = pygame.sprite.Group()  # Группа спрайтов инфо строк
COOKIE_IMAGE = load_image("cookie.png")  # Загрузка изображения печеньки
BTN_IMAGE = load_image("upgrade_btn.png")  # Загрузка кнопки улучшения
BG_IMAGE = load_image("bg.png")  # Загрузка заднего фона
INPUT_BOX = load_image("input_box.png")  # Загрузка изображения поля для ввода
ACHIEVEMENT_IMAGE = load_image("achievement_label.png")
STAR_PARTICLE = load_image("star_particle.png")
LEADERBOARD_LABEL = "lb_label.png"
LEADERBOARD_BG = load_image("lb_bg.png")
LEADERBOARD_TITLE = load_image("lb_title.png")
icon_sheet = cut_sheet(load_image("icons.png"), 2, 2, 75, 75)
ICONS = {"clicker": icon_sheet[0], "farmer": icon_sheet[1],
         "farm_lvl1": icon_sheet[2], "farm_lvl2": icon_sheet[3]}
ACHIEVEMENTS = ["ПЕРВЫЕ ШАГИ", "ВЕСЁЛАЯ ФЕРМА", "АНГАР???", "СУПЕР-ФЕРМА", "БОГ ПЕЧЕНЬЯ"]
COEFFICIENTS = {"farmer": 2, "farm1": 2, "farm2": 4}
SCROLLING_SPEED = 60  # Скорость прокрутки инфо строк
