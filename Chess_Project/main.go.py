import pygame

from Login import ClassLogin
from Game import ClassGameChess
# Инициализация Pygame
pygame.init()


def main():
    while True:
        login = ClassLogin()
        login.start_login()

        if login.result:
            game = ClassGameChess()
            game.run()
        else:
            break


pygame.quit()


if __name__ == "__main__":
    main()

