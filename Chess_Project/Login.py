import hashlib
import os
import re

import pygame

WIDTH, HEIGHT = 600, 400

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
RED = (255, 0, 0)


# Файл для сохранения данных
USERS_FILE = "users.txt"

MODE_LOGIN = "login"
MODE_REGISTER = "register"
MODE = {
    MODE_LOGIN: "Вход",
    MODE_REGISTER: "Регистрация",
}

POLE_USER = "user"
POLE_PASSWORD = "password"
TITLE_INPUT = {
    POLE_USER: "Логин: ",
    POLE_PASSWORD: "Пароль: "
}

START_FORM_X, START_FORM_Y = 150, 50
WIDTH_FORM, HEIGHT_FORM = 300, 40
STEP_Y = 50
WIDTH_BUTTON = 200

BUTTON_SWAP_X, BUTTON_SWAP_Y = WIDTH_BUTTON//1.5 + 20, 20

MAX_LEN = 19
MIN_LEN_PASSWORD = 8
MIN_LEN_LOGIN = 3


class ClassLogin:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.mode = MODE_LOGIN
        self.input_active = None      # активное поле
        self.username = ""
        self.password = ""
        self.message = ""
        self.running = True
        self.result = False
        self.button_start_rect = pygame.Rect(START_FORM_X + (WIDTH_FORM-WIDTH_BUTTON)/2,
                                             START_FORM_Y+STEP_Y*4, WIDTH_BUTTON, HEIGHT_FORM)
        self.button_swap_rect = pygame.Rect(self.screen.get_width() - BUTTON_SWAP_X, BUTTON_SWAP_Y,
                                            WIDTH_BUTTON//1.5, HEIGHT_FORM//1.5)
        pygame.display.set_caption(MODE[self.mode])

    def start_login(self):
        clock = pygame.time.Clock()
        while self.running:
            self.draw_window()
            self.handle_events()
            clock.tick(10)

    def draw_window(self):
        self.screen.fill(WHITE)

        # Заголовок
        self.draw_text(
            MODE[self.mode],
            self.screen.get_width()//2 - 20 if self.mode == MODE_LOGIN else self.screen.get_width()//2 - 85, 20)

        # Поля ввода
        self.draw_text(TITLE_INPUT[POLE_USER], START_FORM_X, START_FORM_Y+20)
        pygame.draw.rect(
            self.screen, RED if self.input_active == POLE_USER else GRAY,
            (START_FORM_X, START_FORM_Y+STEP_Y, WIDTH_FORM, HEIGHT_FORM), 2)
        self.draw_text(self.username[-19:], START_FORM_X + 10, START_FORM_Y+STEP_Y + 5)

        # Ввод пароля
        self.draw_text(TITLE_INPUT[POLE_PASSWORD], START_FORM_X, START_FORM_Y+STEP_Y*2+20)
        pygame.draw.rect(
            self.screen, RED if self.input_active == POLE_PASSWORD else GRAY,
            (START_FORM_X, START_FORM_Y+STEP_Y*3, WIDTH_FORM, HEIGHT_FORM), 2)
        self.draw_text("*" * min(len(self.password), MAX_LEN), START_FORM_X + 10, START_FORM_Y+STEP_Y*3 + 10)

        mouse_pos = pygame.mouse.get_pos()
        # Кнопки входа/регистрации
        color_start_button = (80, 80, 255) if self.button_start_rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(self.screen, color_start_button, self.button_start_rect)
        self.draw_text(MODE[self.mode],
                       self.button_start_rect.x+25 if self.mode == MODE_REGISTER else self.button_start_rect.x+70,
                       self.button_start_rect.y+5)

        color_swap_button = (160, 160, 160) if self.button_swap_rect.collidepoint(mouse_pos) else GRAY
        # Кнопка переключения
        pygame.draw.rect(self.screen, color_swap_button, self.button_swap_rect)
        text_button = MODE[MODE_REGISTER] if self.mode == MODE_LOGIN else MODE[MODE_LOGIN]
        self.draw_text(text_button,
                       self.button_swap_rect.x+45 if self.mode == MODE_REGISTER else self.button_swap_rect.x+15,
                       self.button_swap_rect.y + 5, text_type="button")

        # Сообщение
        self.draw_text(self.message, self.screen.get_width()//2 - len(self.message)*4,
                       START_FORM_Y+STEP_Y*5, color=RED, text_type="message")

        # Обновление экрана
        pygame.display.flip()

    # Интерфейс
    def draw_text(self, text, x, y, color=BLACK, text_type="text"):
        """Рисует текст на экране."""
        if text_type == "button":
            font = pygame.font.Font(None, 26)
        elif text_type == "message":
            font = pygame.font.SysFont("Times New Roman", 18)
        else:
            font = pygame.font.SysFont("Times New Roman", 30)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.button_start_rect.collidepoint(event.pos):
                    self.check_input_data()
                elif event.button == 1 and self.button_swap_rect.collidepoint(event.pos):
                    self.swap_window()
                else:
                    x, y = event.pos
                    if (START_FORM_X <= x <= START_FORM_X + WIDTH_BUTTON) and\
                            (START_FORM_Y+STEP_Y <= y <= START_FORM_Y+STEP_Y+HEIGHT_FORM):
                        self.input_active = POLE_USER
                    if (START_FORM_X <= x <= START_FORM_X + WIDTH_BUTTON) and\
                            (START_FORM_Y+STEP_Y*3 <= y <= START_FORM_Y+STEP_Y*3+HEIGHT_FORM):
                        self.input_active = POLE_PASSWORD

            elif event.type == pygame.KEYDOWN:
                if self.input_active == POLE_USER:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode
                elif self.input_active == POLE_PASSWORD:
                    if event.key == pygame.K_BACKSPACE:
                        self.password = self.password[:-1]
                    else:
                        self.password += event.unicode

    def check_input_data(self):
        if self.mode == MODE_REGISTER:
            if self.user_exists():
                self.message = "Пользователь уже существует!"
            elif len(self.username) < MIN_LEN_LOGIN:
                self.message = f"Длинна логина не менее {MIN_LEN_LOGIN}"
            elif not re.match("^[А-Яа-яA-Za-z0-9._-]+$", self.username):
                self.message = "Логин может содержать только буквы, цифры, точки, тире и подчеркивания."
            elif len(self.password) < MIN_LEN_PASSWORD:
                self.message = f"Длинна пароля не менее {MIN_LEN_PASSWORD}"
            elif not re.match("^[А-Яа-яA-Za-z0-9]+$", self.password):
                self.message = "Логин может содержать только буквы, цифры."
            else:
                self.save_user()
                self.swap_window("Регистрация успешна!")
        else:
            if self.verify_user():
                self.result = True
                self.running = False
            else:
                self.message = "Неверные данные!"

    def swap_window(self, message=""):
        self.mode = MODE_LOGIN if self.mode == MODE_REGISTER else MODE_REGISTER
        self.username = ""
        self.password = ""
        self.message = message
        self.input_active = None
        pygame.display.set_caption(MODE[self.mode])

    def hash_password(self):
        """Хеширует пароль с помощью SHA256."""
        return hashlib.sha256(self.password.encode()).hexdigest()

    def save_user(self):
        """Сохраняет пользователя в файл."""
        with open(USERS_FILE, "a") as file:
            file.write(f"{self.username}:{self.hash_password()}\n")

    def user_exists(self):
        """Проверяет, существует ли пользователь."""
        if not os.path.exists(USERS_FILE):
            return False
        with open(USERS_FILE, "r") as file:
            for line in file:
                saved_username, _ = line.strip().split(":")
                if saved_username == self.username:
                    return True
        return False

    def verify_user(self):
        """Проверяет имя пользователя и пароль."""
        if not os.path.exists(USERS_FILE):
            return False
        password_hash = self.hash_password()
        with open(USERS_FILE, "r") as file:
            for line in file:
                saved_username, saved_password_hash = line.strip().split(":")
                if saved_username == self.username and saved_password_hash == password_hash:
                    return True
        return False
