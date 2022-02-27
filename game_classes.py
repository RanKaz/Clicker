from constants import *


# Класс описывающий частицу
class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, image):
        super().__init__(all_sprites)
        self.image = image
        self.set_image()
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def set_image(self):
        # сгенерируем частицы разного размера
        fire = [self.image]
        for scale in (5, 10, 20, 30):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen.get_rect()):
            self.kill()


# Класс, описывающий кнопку
class Button(pygame.sprite.Sprite):
    def __init__(self,
                 btn_image, x, y,
                 text="", text_size=72,
                 description="", descr_offset_x=0, descr_offset_y=0,
                 icon=pygame.Surface((0, 0)), icon_offset_x=0, icon_offset_y=0):
        super(Button, self).__init__(buttons)
        self.image = btn_image  # Изображение кнопки
        self.standard_image = btn_image  # Изображение кнопки
        self.width, self.height = self.image.get_width(), self.image.get_height()  # Ширина и высота
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (x, y)
        self.x, self.y = x, y
        self.text = text  # Текст кнопки
        self.text_size = text_size  # Размер текста кнопки
        self.description = description  # Описание (информация, что делает кнопка)
        self.description_offset_x = descr_offset_x  # Расположение описания относительно кнопки по x
        self.description_offset_y = descr_offset_y  # Расположение описания относительно кнопки по y
        self.icon = icon
        self.icon_offset_x = icon_offset_x
        self.icon_offset_y = icon_offset_y
        self.hovered = False  # Флаг о наведении на кнопку

    # Функция, устанавливающая иконку
    def set_icon(self):
        screen.blit(self.icon, (self.rect.center[0] + self.icon_offset_x,
                                self.rect.center[1] + self.icon_offset_y))

    # Функция увеличивает кнопку (выделяет/подсвечивает)
    def highlight(self):
        self.image = pygame.transform.scale(self.image,
                                            (int(self.width * SCALE_COEFFICIENT),
                                             int(self.height * SCALE_COEFFICIENT)))
        self.rect = self.image.get_rect()
        difference_width = (self.width - int(self.width * SCALE_COEFFICIENT)) // 2
        difference_height = (self.height - int(self.height * SCALE_COEFFICIENT)) // 2
        self.rect.x = self.x + difference_width
        self.rect.y = self.y + difference_height

    # Функция возвращает картинку кнопки в изначальную (после наведения)
    def set_default_image(self):
        self.rect = self.standard_image.get_rect()
        self.rect.x, self.rect.y = self.pos
        self.hovered = False
        self.image = self.standard_image

    # Проверяет наведён ли курсор на кнопку
    def on_hovered(self, pos):
        if self.rect.collidepoint(*pos):
            self.hovered = True
            return True
        return False

    # Изменяет текст на кнопке
    def change_text(self, text):
        self.text = text

    def change_description(self, text):
        self.description = text

    # Устанавливает описание кнопки над ней
    def set_description(self):
        set_text(self, self.description, 16, False,
                 self.description_offset_x, self.description_offset_y)

    # Функция, выполняющаяся каждый цикл (высчитывает текущий кадр, накладывает текст)
    def update(self):
        self.set_description()
        self.set_icon()
        set_text(self, self.text, self.text_size)


# Класс, описывающий достижение
class Achievement(pygame.sprite.Sprite):
    def __init__(self, image, text):
        super(Achievement, self).__init__(achievements)
        self.image = image
        self.rect = self.image.get_rect()
        self.has_shown = False
        self.allow_to_show = False
        self.hide = True
        self.text = text
        self.x = 678
        self.y = 0
        self.text_size = 24
        self.set_default_coordinates()

    def set_default_coordinates(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if not self.hide:
            if not self.has_shown:
                achievements.draw(screen)
                set_text(self, self.text, self.text_size, False, 0, 20, False, BLACK)


# Класс, описывающий Поле для ввода текста
class TextBox(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super(TextBox, self).__init__()
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


class InfoLabel(pygame.sprite.Sprite):
    def __init__(self, image_name, x):
        super(InfoLabel, self).__init__(info_labels)
        self.image_name = image_name
        self.image = load_image(self.image_name)
        self.data = get_data()
        self.name = ""
        self.score = 0
        self.auto_score = 0
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.dy = 10
        self.x = x
        self.length = 0
        self.set_position()

    def set_position(self):
        self.rect.x = self.x

    def scroll_down(self):
        self.dy += SCROLLING_SPEED

    def scroll_up(self):
        self.dy -= SCROLLING_SPEED

    def render(self):
        for i in range(len(self.data)):
            self.image = load_image(self.image_name)
            self.name = str(self.data[i][1])
            self.score = str(self.data[i][2])
            self.auto_score = str(self.data[i][3])
            font_text = pygame.font.Font("./data/fonts/BIP.ttf", 36)
            text_result = font_text.render(self.name, True, WHITE)
            text_result_center = text_result.get_rect(center=self.image.get_rect().center)
            self.image.blit(text_result, (text_result_center.x - 260, text_result_center.y))
            text_result = font_text.render(self.score, True, WHITE)
            text_result_center = text_result.get_rect(center=self.image.get_rect().center)
            self.image.blit(text_result, text_result_center)
            text_result = font_text.render(self.auto_score, True, WHITE)
            text_result_center = text_result.get_rect(center=self.image.get_rect().center)
            self.image.blit(text_result, (text_result_center.x + 300, text_result_center.y))
            screen.blit(self.image, (self.rect.x, ((self.image.get_height() + 20) * i + 114) + self.dy))
        self.length = -(self.height * len(self.data)) + (self.height * 2)
