# coding=utf-8
# encoding: 'utf-8'
__author__ = 'xyc'

import itertools
import unicodedata



"""
此case只是该模式用法的结构，非可执行代码
The Factory Method Pattern is intended to be used when we want subclasses to
choose which classes they should instantiate when an object is requested.
"""

BLACK, WHITE = ("BLACK", "WHITE")
DRAUGHT, PAWN, ROOK, KNIGHT, BISHOP, KING, QUEEN = ("DRAUGHT", "PAWN",
                            "ROOK", "KNIGHT", "BISHOP", "KING", "QUEEN")

class AbstractBoard:
    def __init__(self, rows, columns):
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.populate_board()

    def populate_board(self):
        raise NotImplementedError()

    # create_piece 为工厂方法
    def create_piece(self, kind, color):
        color = "White" if color == WHITE else "Black"
        name = {DRAUGHT: "Draught", PAWN: "ChessPawn", ROOK: "ChessRook",
                KNIGHT: "ChessKnight", BISHOP: "ChessBishop",
                KING: "ChessKing", QUEEN: "ChessQueen"}[kind]
        return globals()[color + name]()

    def __str__(self):
        squares = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                square = console(piece, BLACK if (y + x) % 2 else WHITE)
                squares.append(square)
            squares.append("\n")
        return "".join(squares)


class CheckersBoard(AbstractBoard):

    def __init__(self):
        super(CheckersBoard, self).__init__(10, 10)

    def populate_board(self):
        for x in range(0, 9, 2):
            for y in range(4):
                column = x + ((y + 1) % 2)
                for row, color in ((y, BLACK), (y + 6, WHITE)):
                    self.board[row][column] = self.create_piece(DRAUGHT, color)

class ChessBoard(AbstractBoard):
    def __init__(self):
        super(ChessBoard, self).__init__(8, 8)

    def populate_board(self):
        for row, color in ((0, BLACK), (7, WHITE)):
            for columns, kind in (((0, 7), ROOK), ((1, 6), KNIGHT),
                                ((2, 5), BISHOP), ((3,), QUEEN), ((4,), KING)):
                for column in columns:
                    self.board[row][column] = self.create_piece(kind, color)
        for column in range(8):
            for row, color in ((1, BLACK), (6, WHITE)):
                self.board[row][column] = self.create_piece(PAWN, color)

class Piece(str):
    __slots__ = ()


def main():

    # 创建piece类，并将它们通过globals（）放入全局名字空间
    for code in itertools.chain((0x26C0, 0x26C2), range(0x2654, 0x2660)):
        char = chr(code)
        name = unicodedata.name(char).title().replace(" ", "")
        if name.endswith("sMan"):
            name = name[:-4]
        new = (lambda char: lambda Class: Piece.__new__(Class, char))(char)
        new.__name__ = "__new__"
        Class = type(name, (Piece,), dict(__slots__=(), __new__=new))
        # setattr(sys.modules[__name__], name, Class)
        globals()[name] = Class # This does exactly the same thing as the setattr()

    checkers = CheckersBoard()
    print(checkers)
    chess = ChessBoard()
    print(chess)
