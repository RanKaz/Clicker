from game_classes import *
from constants import *


# Функия запуска экрана приветствия
def greeting_screen():
    show_leaderboard_flag = False
    reg_btn = None
    enter_btn = None
    info_label = InfoLabel(LEADERBOARD_LABEL, 106)
    while True:
        buttons.empty()
        if not show_leaderboard_flag:
            reg_btn = Button(BTN_IMAGE, 320, 208, "РЕГИСТРАЦИЯ", 48)
            enter_btn = Button(BTN_IMAGE, 320, 326, "ВХОД", 48)
        leaderboard_btn = Button(BTN_IMAGE, 320, 500, "ТАБЛИЦА РЕКОРДОВ", 36)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if not show_leaderboard_flag:
                    if reg_btn.on_hovered(mouse_pos):
                        return registration_window()
                    if enter_btn.on_hovered(mouse_pos):
                        return enter_window()
                if leaderboard_btn.on_hovered(mouse_pos):
                    show_leaderboard_flag = True
                if event.button == 4:
                    for sprite in info_labels:
                        if sprite.dy < 0:
                            sprite.scroll_down()
                elif event.button == 5:
                    for sprite in info_labels:
                        if sprite.dy > info_label.length:
                            sprite.scroll_up()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                show_leaderboard_flag = False
        screen.blit(BG_IMAGE, (0, 0))
        if show_leaderboard_flag:
            info_label.render()
            screen.blit(LEADERBOARD_TITLE, (106, 0))
        else:
            check_hovered()
            buttons.draw(screen)
            buttons.update()
        # Отрисовка
        pygame.display.flip()
        clock.tick(FPS)


# Функция регистрации игрока
def registration_window():
    text = ""
    wait_timer = 0
    error = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text != "" and len(text) > MIN_TEXT_LENGTH:
                        return create_account(text)
                    else:
                        error = True
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < MAX_TEXT_LENGTH:
                        if event.unicode in ACCEPTED_SYMBOLS:
                            text += event.unicode
        textbox = TextBox(INPUT_BOX, 212, 248)
        screen.blit(BG_IMAGE, (0, 0))
        screen.blit(INPUT_BOX, (212, 248))
        if error:
            set_text(screen,
                     "СЛИШКОМ КОРОТКОЕ ИМЯ",
                     24, False, 0, -150, True, RED)
        set_text(screen,
                 "Ваш индентификационный номер будет расположен в верхнем",
                 24, False, 0, 150, True, WARNING)
        set_text(screen,
                 "правом углу во время игры, чтобы зайти в свой аккаунт, "
                 "вам придётся запомнить его",
                 24, False, 0, 200, True, WARNING)
        text_result = set_text(textbox, text, 72)
        wait_rect = pygame.Surface((10, 50))
        wait_rect.fill(WHITE)
        wait_timer += 1
        if wait_timer % 100 <= 50:
            width = text_result.width
            x = text_result.x + width
            screen.blit(wait_rect, (x, 320))
        # Отрисовка
        pygame.display.flip()
        clock.tick(FPS)


def enter_window():
    text = ""
    wait_timer = 0
    error = False
    data = [i[0] for i in get_data()]
    while True:
        screen.blit(BG_IMAGE, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(text) == 8 and text.upper() in data:
                        return text.upper()
                    else:
                        error = True
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < MAX_TEXT_LENGTH:
                        if event.unicode in ACCEPTED_SYMBOLS:
                            text += event.unicode
        if error:
            set_text(screen,
                     "Идентификационный номер введён неверно",
                     36, False, 0, 150, True, RED)
        textbox = TextBox(INPUT_BOX, 212, 248)
        screen.blit(INPUT_BOX, (212, 248))
        set_text(screen,
                 "Введите ваш идентификационный номер",
                 36, False, 0, -150, True, WHITE)
        text_result = set_text(textbox, text, 72)
        wait_rect = pygame.Surface((10, 50))
        wait_rect.fill(WHITE)
        wait_timer += 1
        if wait_timer % 100 <= 50:
            width = text_result.width
            x = text_result.x + width
            screen.blit(wait_rect, (x, 320))
        # Отрисовка
        pygame.display.flip()
        clock.tick(FPS)


def game(identifier):
    game_data = load_progress(identifier)

    score = game_data["score"]

    incomes = {"clicker": game_data['clicker'], "farmer": game_data['farmer'],
               "farm1": game_data['farm'], "farm2": game_data['super_farm']}

    achievements_states = str(game_data["achievements_states"])

    prices = {"clicker": 10 * (2 ** (incomes["clicker"] - 1)),
              "farmer": 150 * (COEFFICIENTS["farmer"] ** get_power(incomes["farmer"])),
              "farm1": 2000 * (COEFFICIENTS["farm1"] ** get_power(incomes["farm1"])),
              "farm2": 10000 * (COEFFICIENTS["farm2"] ** get_power(incomes["farm2"]))
              }

    id_, name = game_data["id_"], game_data["name"]

    timer = 0
    timer_count = 0
    auto_income = game_data['income']
    total_income = game_data['income']
    checked = None

    achievements_objects = [Achievement(ACHIEVEMENT_IMAGE, ACHIEVEMENTS[i]) for i in range(5)]
    for i in range(5):
        if achievements_states[i] == "2":
            achievements_objects[i].has_shown = True

    while True:
        timer += 1
        buttons.empty()
        cookie_btn = Button(COOKIE_IMAGE, 50, 196, str(score), 72,
                            f"ДОХОД: {auto_income} ПЕЧЕН / СЕК", 0, -250)
        clicker_upgrade_btn = Button(BTN_IMAGE, 589, 180, "", 72,
                                     f"Купить кликер за {prices['clicker']}", 2, 0,
                                     ICONS["clicker"], -180, -35)
        farmer_upgrade_btn = Button(BTN_IMAGE, 589, 288, "", 72,
                                    f"Купить фермера за {prices['farmer']}", 15, 0,
                                    ICONS["farmer"], -180, -35)
        farm1_upgrade_btn = Button(BTN_IMAGE, 589, 396, "", 72,
                                   f"Купить ферму за {prices['farm1']}", 13, 0,
                                   ICONS["farm_lvl1"], -180, -35)
        farm2_upgrade_btn = Button(BTN_IMAGE, 589, 504, "", 72,
                                   f"Купить супер-ферму за {prices['farm2']}", 40, 0,
                                   ICONS["farm_lvl2"], -180, -35)

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                update_db(identifier, score, auto_income, incomes, achievements_states)
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                if cookie_btn.on_hovered(mouse_pos):
                    income = incomes["clicker"]
                    score += income
                    total_income += income
                    create_particles(mouse_pos, f"+{income}", 1)
                if clicker_upgrade_btn.on_hovered(mouse_pos):
                    price = prices["clicker"]
                    if score >= price:
                        score -= price
                        prices["clicker"] *= 2
                        incomes["clicker"] += 1
                        checked = check_achievement(score, incomes)
                        create_particles(mouse_pos, "", 20, STAR_PARTICLE)
                    else:
                        show_error("НЕДОСТАТОЧНО ПЕЧЕНЕК!")
                if farmer_upgrade_btn.on_hovered(mouse_pos):
                    price = prices["farmer"]
                    coefficient = COEFFICIENTS["farmer"]
                    if score >= price:
                        if incomes["farmer"] == 0:
                            incomes["farmer"] += 1
                        score -= price
                        incomes["farmer"] *= coefficient
                        prices["farmer"] *= 2
                        checked = check_achievement(score, incomes)
                        create_particles(mouse_pos, "", 25, STAR_PARTICLE)
                    else:
                        show_error("НЕДОСТАТОЧНО ПЕЧЕНЕК!")
                if farm1_upgrade_btn.on_hovered(mouse_pos):
                    price = prices["farm1"]
                    coefficient = COEFFICIENTS["farm1"]
                    if score >= price:
                        if incomes["farm1"] == 0:
                            incomes["farm1"] += 1
                        score -= price
                        incomes["farm1"] *= coefficient
                        prices["farm1"] *= 2
                        create_particles(mouse_pos, "", 30, STAR_PARTICLE)
                        checked = check_achievement(score, incomes)
                    else:
                        show_error("НЕДОСТАТОЧНО ПЕЧЕНЕК!")
                if farm2_upgrade_btn.on_hovered(mouse_pos):
                    price = prices["farm2"]
                    coefficient = COEFFICIENTS["farm2"]
                    if score >= price:
                        if incomes["farm2"] == 0:
                            incomes["farm2"] += 1
                        score -= price
                        incomes["farm2"] *= coefficient
                        prices["farm2"] *= 2
                        create_particles(mouse_pos, "", 50, STAR_PARTICLE)
                        checked = check_achievement(score, incomes)
                    else:
                        show_error("НЕДОСТАТОЧНО ПЕЧЕНЕК!")
        if score >= 10000000:
            checked = check_achievement(score, incomes)
        check_hovered()
        screen.blit(BG_IMAGE, (0, 0))
        set_info(id_, name)
        if checked:
            index = checked - 1
            if not achievements_objects[index].has_shown:
                achievements_objects[index].hide = False
                if timer_count == 5:
                    timer_count = 0
                    achievements_objects[index].hide = True
                    achievements_objects[index].has_shown = True
                    achievements_states = f"{achievements_states[:index]}2" \
                                          f"{achievements_states[index + 1:]}"
                    checked = None
                else:
                    if timer % 30 == 0:
                        timer_count += 1
                    create_particles((850, 80), "", 1, STAR_PARTICLE)
        auto_income = sum([i[1] for i in incomes.items() if i[0] != "clicker"])
        if timer % 10 == 0:
            score += auto_income
        if timer % 60 == 0:
            total_income = auto_income
        cookie_btn.change_description(f"ДОХОД: {total_income} ПЕЧЕН / СЕК")
        cookie_btn.change_text(str(score))
        # Отрисовка
        buttons.draw(screen)
        buttons.update()
        all_sprites.draw(screen)
        all_sprites.update()
        achievements.update()
        pygame.display.flip()
        clock.tick(FPS)


# Устанавливает информацию об игроке
def set_info(id_, name):
    set_text(screen, id_, 24, False, 420, -310, True)
    set_text(screen, name, 24, False, 420, -270, True)


def get_power(power):
    count = 0
    if power == 0:
        return count
    while power % 2 == 0:
        power //= 2
        count += 1
    return count


def load_progress(identifier):
    progress_data = get_info(identifier)
    id_, name, score, income, clicker, farmer, farm, super_farm, achievements_states = \
        progress_data

    return {
        "id_": id_, "name": name, "score": score, "income": income,
        "clicker": int(clicker), "farmer": int(farmer),
        "farm": int(farm), "super_farm": int(super_farm),
        "achievements_states": str(achievements_states)
    }


def check_hovered():
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        if btn.on_hovered(mouse_pos):
            btn.highlight()
        else:
            btn.set_default_image()


def create_particles(position, text, particle_count=5, image=0):
    # возможные скорости
    numbers = range(-5, 6)
    text_image = text_to_image(text)
    for _ in range(particle_count):
        if image:
            Particle(position, random.choice(numbers), random.choice(numbers), image)
        else:
            Particle(position, random.choice(numbers), random.choice(numbers), text_image)


def text_to_image(text):
    font_text = pygame.font.Font("./data/fonts/BIP.ttf", 120)
    text_result = font_text.render(text, True, WHITE)
    return text_result


def show_error(error):
    timer = 0
    while timer < 150:
        screen.blit(BG_IMAGE, (0, 0))
        timer += 1
        set_text(screen, error, 72, True, 0, 0, True, RED)
        pygame.display.flip()
        clock.tick(FPS)


def show_achievement(achievements_data):
    for achievement in achievements_data:
        if achievement["allow_to_show"] and not achievement["has_shown"]:
            set_text(screen, "ПОЗДРАВЛЯЕМ ВЫ ПОЛУЧИЛИ ДОСТИЖЕНИЕ!", 36, False,
                     achievement['x'], achievement['y'], True, GOLD)
            set_text(screen, f"Вы {achievement['text']}", 36, False,
                     achievement['x'], achievement['y'], True, GOLD)


def check_achievement(score, incomes):
    achievement_id = None
    if incomes["clicker"] == 2:
        achievement_id = 1
    if incomes["farmer"] == 2:
        achievement_id = 2
    if incomes["farm1"] == 2:
        achievement_id = 3
    if incomes["farm2"] == 4:
        achievement_id = 4
    if score >= 10000000:
        achievement_id = 5
    return achievement_id
