import pygame
from CONST import *


class ClassSetting:
    def __init__(self, screen, board_width, frame_size):
        self.screen = screen
        self.start_x = board_width + frame_size*2 + 20
        self.frame_size = frame_size
        self.message = ""
        self.message_info = "редактор"
        self.panel_width = 200
        self.buttons = []
        self.init_buttons()

    def init_buttons(self):
        # Настройка кнопок
        button_width, button_height = 150, 40
        start_x = self.start_x
        start_y = self.frame_size + 120

        self.buttons = [
            {"label": "Сменить ход", "rect": pygame.Rect(start_x, start_y, button_width, button_height)},
            {"label": "Сменить цвет", "rect": pygame.Rect(start_x, start_y+60, button_width, button_height)},
            {"label": "Начать играть", "rect": pygame.Rect(start_x, start_y + 220, button_width, button_height)},
            {"label": "Начать заново", "rect": pygame.Rect(start_x, start_y + 280, button_width, button_height)},
        ]

    def draw(self, winner, cur_move=True):
        # Отображение победителя
        font = pygame.font.SysFont("TimesNewRoman", 28)
        text_winner = font.render(f"Победитель: {winner}", True, BLACK)
        self.screen.blit(text_winner, (self.start_x, self.frame_size + 20))

        color_move = "белых" if cur_move else "черных"
        text_cur_move = font.render(f"Ход: {color_move}", True, BLACK)
        self.screen.blit(text_cur_move, (self.start_x, self.frame_size + 70))

        font_button = pygame.font.SysFont("TimesNewRoman", 14)
        # Отрисовка кнопок
        for button in self.buttons:
            pygame.draw.rect(self.screen, WHITE, button["rect"])
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2)
            label = font_button.render(button["label"], True, BLACK)
            label_rect = label.get_rect(center=button["rect"].center)
            self.screen.blit(label, label_rect)

        # режим
        text_cur_move = font_button.render(f"Режим: {self.message_info}", True, BLACK)
        self.screen.blit(text_cur_move, (self.start_x, self.frame_size + 240))

        # сообщение об ошибке
        text_cur_move = font_button.render(self.message, True, RED)
        self.screen.blit(text_cur_move, (self.start_x, self.frame_size + 500))

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["label"]
        return None
