from game_functions import *


def main():
    identifier = greeting_screen()
    game(identifier)
    terminate()


if __name__ == '__main__':
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("CLICKER")  # Название окна
    main()
