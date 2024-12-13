import pygame
from CONST import *

from Class_Piece import King, Knight


class ChessBoard:
    def __init__(self, screen):
        self.screen = screen
        self.color_player = COLOR_W         # c чьей стороны будет отрисовка
        self.color_cur_move = True          # чей ход True - белых, False - черных
        self.selected_piece = None          # выбранная фигура
        self.winner = "-"
        self.highlight_moves = []
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def add_piece(self, piece):
        self.board[piece.y][piece.x] = piece

    def move_piece(self, piece, x, y):
        self.board[piece.y][piece.x] = None
        piece.x, piece.y = x, y
        self.board[y][x] = piece

    def clear_board(self):
        self.color_player = COLOR_W  # c чьей стороны будет отрисовка
        self.selected_piece = None  # выбранная фигура
        self.winner = "-"
        self.highlight_moves = []

    def handle_click_game_start(self, mouse_pos):
        # Определяем клетку, куда был произведен клик
        x, y = (mouse_pos[0] - FRAME_SIZE) // CELL_SIZE, (mouse_pos[1] - FRAME_SIZE) // CELL_SIZE

        # Проверяем, что клик внутри доски
        if 0 <= x < 8 and 0 <= y < 8:
            cur_color = COLOR_W if self.color_cur_move else COLOR_B
            selected_piece = self.board[y][x]

            if selected_piece:  # Если кликнули на фигуру
                if selected_piece.color == cur_color:  # Выбираем фигуру, если цвет соответствует текущему ходу
                    self.selected_piece = selected_piece
                    self.highlight_moves = self.filtering_moves()       # Подсветка доступных ходов
                elif self.selected_piece:                               # Если выбрана фигура, но кликнули на вражескую
                    self.check_move(x, y)
            elif self.selected_piece:  # Если фигура уже выбрана, пытаемся ее переместить
                self.check_move(x, y)

    def filtering_moves(self):
        possible_moves = self.selected_piece.get_possible_moves(self.board)
        result = []
        # Если выбранный ход допустим, фильтруем его с учетом безопасности короля
        for move in possible_moves:
            # Выполним временный ход
            target_x, target_y = move
            original_x, original_y = self.selected_piece.x, self.selected_piece.y
            original_piece = self.board[target_y][target_x]
            self.board[original_y][original_x], self.board[target_y][target_x] = None, self.selected_piece

            # Проверим, остается ли король под атакой после хода
            if not self.is_king_under_attack(self.selected_piece.color):
                result.append(move)
            # Вернуть доску в исходное состояние
            self.board[original_y][original_x], self.board[target_y][target_x] = self.selected_piece, original_piece
        return result

    def check_move(self, x, y):
        """
        Проверяет, можно ли переместить фигуру на выбранную клетку, и выполняет ход, если это возможно.
        Также фильтрует ходы, которые оставляют короля под атакой.
        """
        # Получаем все возможные ходы выбранной фигуры
        possible_moves = self.filtering_moves()

        # Если выбранный ход допустим, фильтруем его с учетом безопасности короля
        if (x, y) in possible_moves:
            # Если ход безопасен, выполняем его
            self.move_piece(self.selected_piece, x, y)

            # Сбрасываем подсветку и выбор
            self.selected_piece = None
            self.highlight_moves = []

            # Меняем ход
            self.color_cur_move = not self.color_cur_move

    def is_king_under_attack(self, color):
        """
        Проверяет, находится ли король указанного цвета под атакой.
        """
        # Находим позицию короля
        king_pos = self.find_king(color)

        # Проверяем, под атакой ли король
        king_x, king_y = king_pos
        attacker_color = COLOR_B if color == COLOR_W else COLOR_W  # Противник

        # Проверяем, может ли какая-либо фигура противника атаковать клетку с королем
        return self.is_square_attacked(king_x, king_y, attacker_color)

    def handle_click_game_stop(self, mouse_pos):
        # Определяем размер клетки
        x, y = (mouse_pos[0] - FRAME_SIZE) // CELL_SIZE, (mouse_pos[1] - FRAME_SIZE) // CELL_SIZE
        # Проверяем, что клик внутри доски
        if 0 <= x < 8 and 0 <= y < 8:
            selected_piece = self.board[y][x]
            if selected_piece:                              # Если кликнули на фигуру
                self.selected_piece = selected_piece
            elif self.selected_piece:                       # Если фигура уже выбрана, пытаемся ее переместить
                # Перемещаем фигуру
                self.move_piece(self.selected_piece, x, y)
                self.selected_piece = None

    def draw_board(self):
        """ Отрисовка шахматной доски """
        # Отрисовка черного фона для краев
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH_BOARD + FRAME_SIZE*2, HEIGHT_BOARD + FRAME_SIZE*2))

        # Отрисовка клеток доски
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                color = LIGHT_BROWN if (x + y) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(
                    self.screen, color,
                    (x * CELL_SIZE + FRAME_SIZE, y * CELL_SIZE + FRAME_SIZE, CELL_SIZE, CELL_SIZE)
                )

        # отрисовка выбранной фигуры
        if self.selected_piece:
            old_x, old_y = self.selected_piece.x, self.selected_piece.y
            pygame.draw.rect(
                self.screen, RED,
                (old_x * CELL_SIZE + FRAME_SIZE, old_y * CELL_SIZE + FRAME_SIZE, CELL_SIZE, CELL_SIZE), 3)

        # Подсветка доступных ходов
        for move in self.highlight_moves:
            # Рисуем рамку желтого цвета вокруг каждой доступной клетки
            pygame.draw.rect(self.screen, (255, 255, 0),  # Желтый цвет
                             (move[0] * CELL_SIZE + FRAME_SIZE, move[1] * CELL_SIZE + FRAME_SIZE, CELL_SIZE, CELL_SIZE),
                             3)  # Рамка толщиной 3

        # Отрисовка букв внизу (a-h)
        font = pygame.font.SysFont(None, 24)
        letters = "abcdefgh"
        if self.color_player == COLOR_B:
            letters = letters[::-1]
        for i, letter in enumerate(letters):
            text = font.render(letter, True, WHITE)
            text_rect = text.get_rect(
                center=(i * CELL_SIZE + FRAME_SIZE + CELL_SIZE // 2, HEIGHT_WINDOW - FRAME_SIZE // 2))
            self.screen.blit(text, text_rect)

        # Отрисовка цифр слева (1-8 снизу вверх)
        rows = [i for i in range(len(self.board))]
        if self.color_player == COLOR_B:
            rows = rows[::-1]
        for i, letter in enumerate(rows):
            text = font.render(str(8-letter), True, WHITE)
            text_rect = text.get_rect(center=(FRAME_SIZE // 2, i * CELL_SIZE + FRAME_SIZE + CELL_SIZE // 2))
            self.screen.blit(text, text_rect)

    def validate_user_setup(self):
        """
        Проверяет, валидна ли текущая расстановка фигур на доске.
        :return: True, если расстановка корректна; иначе False.
        """

        # 1. Найти позиции королей
        white_king_pos = self.find_king(COLOR_W)
        black_king_pos = self.find_king(COLOR_B)

        # 2. Проверить, не стоят ли короли рядом
        if abs(white_king_pos[0] - black_king_pos[0]) <= 1 and abs(white_king_pos[1] - black_king_pos[1]) <= 1:
            return False  # Короли слишком близко друг к другу

        # 3. Проверить, атакован ли каждый король
        white_king_under_attack = self.is_square_attacked(white_king_pos[0], white_king_pos[1], COLOR_B)
        black_king_under_attack = self.is_square_attacked(black_king_pos[0], black_king_pos[1], COLOR_W)

        # 4. Оба короля не могут быть одновременно под атакой
        if white_king_under_attack and black_king_under_attack:
            return False

        # 5. Если ходят белые, черный король не может быть под атакой
        if self.color_cur_move and black_king_under_attack:
            return False

        # 6. Если ходят черные, белый король не может быть под атакой
        if not self.color_cur_move and white_king_under_attack:
            return False

        # 7. Проверить, есть ли мат у текущего игрока
        current_color = COLOR_W if self.color_cur_move else COLOR_B
        if not self.has_valid_moves(current_color):
            return False  # Матовая ситуация, игра бессмысленна

        return True

    def has_valid_moves(self, color):
        """Проверяет, есть ли у игрока с данным цветом хотя бы один валидный ход."""
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece and piece.color == color:
                    for move in piece.get_possible_moves(self.board):
                        # Симулируем ход
                        target_x, target_y = move
                        backup_piece = self.board[target_y][target_x]
                        self.board[y][x], self.board[target_y][target_x] = None, piece

                        # Проверяем, не окажется ли король под шахом
                        king_pos = self.find_king(color)
                        attacked_color = COLOR_W if color == COLOR_B else COLOR_B
                        if king_pos and not self.is_square_attacked(king_pos[0], king_pos[1], attacked_color):
                            # Вернуть доску в исходное состояние
                            self.board[y][x], self.board[target_y][target_x] = piece, backup_piece
                            return True

                        # Вернуть доску в исходное состояние
                        self.board[y][x], self.board[target_y][target_x] = piece, backup_piece
        return False

    def find_king(self, color):
        """Находит короля определенного цвета."""
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color == color:
                    return x, y
        return None

    def is_square_attacked(self, x, y, attacker_color):
        """Проверяет, атакована ли клетка фигурами указанного цвета."""
        for row in self.board:
            for piece in row:
                if piece and piece.color == attacker_color and piece.can_attack(x, y, self.board):
                    return True
        return False

    def game_over(self):
        """
        Проверяет, окончена ли игра (ничья или мат).
        """
        # 1. Проверка, если на доске только король против короля (ничья) или один конь.
        if self.is_only_kings_or_one_knigt():
            self.winner = "Н"
        # 2. Проверка на мат или пат.
        current_color = COLOR_W if self.color_cur_move else COLOR_B
        if not self.has_valid_moves(current_color):
            # Проверяем, в какой ситуации находится игрок: мат или пат.
            if self.is_check(current_color):
                self.winner = "Ч" if self.color_cur_move else "Б"   # Если король под шахом и нет валидных ходов — мат
            else:
                self.winner = "Н"  # Если нет валидных ходов и король не под шахом — пат

    def is_only_kings_or_one_knigt(self):
        """Проверяет, что на доске только короли."""
        queen, knight = 0, 0
        for row in self.board:
            for piece in row:
                if isinstance(piece, King):
                    continue
                elif isinstance(piece, Knight):
                    knight += 1
                elif piece is not None:
                    queen += 1
                    return False
        return knight <= 1 and queen == 0

    def is_check(self, color):
        """Проверяет, находится ли король определенного цвета под шахом."""
        king_pos = self.find_king(color)
        if king_pos:
            return self.is_square_attacked(king_pos[0], king_pos[1], COLOR_W if color == COLOR_B else COLOR_B)
        return False
