import pygame
from CONST import *


def is_occupied(piece, color=None):
    """
    Проверяет, занята ли клетка на доске.
    :param piece: Фигура
    :param color: Цвет фигуры, с которым нужно сравнить (если указано).
    :return:
        True, если клетка занята и цвет совпадает (или любой, если color=None).
        False, если клетка пуста или цвет не совпадает.
    """
    if piece is None:  # Если клетка пуста
        return False
    if color is None:  # Если цвет не указан, клетка считается занятой
        return True
    return piece.color == color  # Сравниваем цвет фигуры на клетке с заданным


class ChessPiece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.image = None

    def draw(self, screen):
        if self.image:
            rect = self.image.get_rect(center=(self.x * CELL_SIZE+FRAME_SIZE + CELL_SIZE // 2,
                                               self.y * CELL_SIZE+FRAME_SIZE + CELL_SIZE // 2))
            screen.blit(self.image, rect)

    def get_possible_moves(self, board):
        return []

    def can_attack(self, x, y, board):
        """
        Проверяет, может ли фигура атаковать клетку (x, y) на доске.
        """
        return (x, y) in self.get_possible_moves(board)


class King(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = pygame.image.load(f"img/{color}K.png").convert_alpha()

    def get_possible_moves(self, board):
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and not is_occupied(board[ny][nx], self.color):
                    moves.append((nx, ny))
        return moves


class Knight(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = pygame.image.load(f"img/{color}N.png").convert_alpha()

    def get_possible_moves(self, board):
        moves = []
        for dx, dy in [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and not is_occupied(board[ny][nx], self.color):
                moves.append((nx, ny))
        return moves


class Queen(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = pygame.image.load(f"img/{color}Q.png").convert_alpha()

    def get_possible_moves(self, board):
        moves = []
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]
        for dx, dy in directions:
            nx, ny = self.x, self.y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if is_occupied(board[ny][nx], self.color):
                        break
                    moves.append((nx, ny))
                    if is_occupied(board[ny][nx]):
                        break
                else:
                    break
        return moves
