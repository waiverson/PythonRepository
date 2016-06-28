# coding=utf-8
__author__ = 'xyc'


# The Command Pattern is used to encapsulate commands as objects. This
# makes it possible, for example, to build up a sequence of commands for deferred
# execution or to create undoable commands.
# 讲一个请求封装为一个对象，从而是你可用不同的请求对客户进行参数化；对请求排队或记录请求日志，以及支持可撤销的操作。

class Grid:
    def __init__(self, width, height):
        self.__cells = [["white" for _ in range(height)] for _ in range(width)]

    def cell(self, x, y, color=None):
        if color is None:
            return self.__cells[x][y]
        self.__cells[x][y] = color

    @property
    def rows(self):
        return len(self.__cells[0])

    @property
    def columns(self):
        return len(self.__cells)


class UndoableGrid(Grid):
    def create_cell_command(self, x, y, color):
        def undo():
            self.cell(x, y, undo.color)
        def do():
            undo.color = self.cell(x, y) # Subtle!
            self.cell(x, y, color)
        return Command(do, undo, "Cell")

    def create_rectangle_macro(self, x0, y0, x1, y1, color):
        macro = Macro("Rectangle")
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                macro.add(self.create_cell_command(x, y, color))
        return macro

class Command:
    def __init__(self, do, undo, description=""):
        assert callable(do) and callable(undo)
        self.do = do
        self.undo = undo
        self.description = description

    def __call__(self):
        self.do()

class Macro:
    def __init__(self, description=""):
        self.description = description
        self.__commands = []

    def add(self, command):
        if not isinstance(command, Command):
            raise TypeError("Expected object of type Command, got {}".format(type(command).__name__))
        self.__commands.append(command)

    def __call__(self):
        for command in self.__commands:
            command()

    do = __call__

    def undo(self):
        for command in reversed(self.__commands):
            command.undo()

grid = UndoableGrid(8, 3) # (1) Empty
redLeft = grid.create_cell_command(2, 1, "red")
redRight = grid.create_cell_command(5, 0, "red")
redLeft() # (2) Do Red Cells
redRight.do() # OR: redRight()
greenLeft = grid.create_cell_command(2, 1, "lightgreen")
greenLeft() # (3) Do Green Cell
rectangleLeft = grid.create_rectangle_macro(1, 1, 2, 2, "lightblue")
rectangleRight = grid.create_rectangle_macro(5, 0, 6, 1, "lightblue")
rectangleLeft() # (4) Do Blue Squares
rectangleRight.do() # OR: rectangleRight()
rectangleLeft.undo() # (5) Undo Left Blue Square
greenLeft.undo() # (6) Undo Left Green Cell
rectangleRight.undo() # (7) Undo Right Blue Square
redLeft.undo() # (8) Undo Red Cells
redRight.undo()