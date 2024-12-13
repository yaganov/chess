import pygame

import Class_Board
import Class_Piece
import Class_Setting
from CONST import *


class ClassGameChess:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
        self.clock = pygame.time.Clock()
        self.running = False
        self.quit_game = False
        pygame.display.set_caption("Эндшпиль: Король, 2 коня - Король, ферзь")
        self.board = Class_Board.ChessBoard(self.screen)
        self.settings = Class_Setting.ClassSetting(self.screen, WIDTH_BOARD, FRAME_SIZE)
        self.setup_pieces()

    def run(self):
        """ Запуск игры """
        while not self.quit_game:
            self.handle_events()
            self.render()
            if self.running:
                self.check_game_over()
            self.clock.tick(30)

    def handle_events(self):
        """ Обработка действий пользователя """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                button_action = self.settings.handle_click(event.pos)
                if button_action is not None:
                    self.settings.message = ""
                    if button_action == "Сменить ход" and not self.running:
                        self.board.color_cur_move = not self.board.color_cur_move
                    if button_action == "Сменить цвет" and not self.running:
                        self.board.color_player = COLOR_B if self.board.color_player == COLOR_W else COLOR_W
                        self.switch_colors()
                    elif button_action == "Начать играть":
                        if self.running:
                            break
                        if self.board.validate_user_setup():
                            self.settings.message_info = "игра"
                            self.board.selected_piece = None  # выбранная фигура
                            self.board.winner = "-"
                            self.board.highlight_moves = []
                            self.running = True
                        else:
                            self.settings.message = "Невалидная расстановка"
                    elif button_action == "Начать заново":
                        self.running = False
                        self.settings.message_info = "редактор"
                        self.board.clear_board()
                        self.setup_pieces()
                else:
                    if self.running:
                        self.board.handle_click_game_start(event.pos)
                    else:
                        self.board.handle_click_game_stop(event.pos)

    def render(self):
        """ Отрисовка игры """
        self.screen.fill(WHITE)
        self.board.draw_board()
        self.settings.draw(self.board.winner, self.board.color_cur_move)
        for row in self.board.board:
            for piece in row:
                if piece:
                    piece.draw(self.screen)
        pygame.display.flip()

    def check_game_over(self):
        self.board.game_over()
        if self.board.winner != "-":
            self.settings.message_info = "редактор"
            self.running = False

    def setup_pieces(self):
        """ Установка стартовой расстановки """
        self.board.clear_board()
        self.board.board = [[None for _ in range(8)] for _ in range(8)]
        # Установка фигур на доске
        self.board.add_piece(Class_Piece.King(4, 7, COLOR_W))
        self.board.add_piece(Class_Piece.Knight(3, 7, COLOR_W))
        self.board.add_piece(Class_Piece.Knight(5, 7, COLOR_W))
        self.board.add_piece(Class_Piece.Queen(3, 0, COLOR_B))
        self.board.add_piece(Class_Piece.King(4, 0, COLOR_B))

    def switch_colors(self):
        """ Замена белаых фигур на черных и наоборот """
        for y in range(len(self.board.board)):
            for x in range(len(self.board.board[y])):
                piece = self.board.board[y][x]
                if piece:  # Если на клетке есть фигура
                    # Смена цвета
                    piece.color = COLOR_W if piece.color == COLOR_B else COLOR_B
                    # Обновление изображения в зависимости от нового цвета и типа фигуры
                    if isinstance(piece, Class_Piece.King):
                        piece.image = pygame.image.load(f"img/{piece.color}K.png").convert_alpha()
                    elif isinstance(piece, Class_Piece.Knight):
                        piece.image = pygame.image.load(f"img/{piece.color}N.png").convert_alpha()
                    elif isinstance(piece, Class_Piece.Queen):
                        piece.image = pygame.image.load(f"img/{piece.color}Q.png").convert_alpha()


