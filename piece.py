import pygame as pg


class Piece:
    def __init__(self, x = 0, y = 0, color = (0, 0, 0), width = 0, height = 0):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.color = color
        self.dragable = False
    # .....
    @staticmethod
    def getLong5(tileOffset, tileSize, color):
        width = tileOffset * 5 - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        pg.draw.rect(piece.image, (0,0,0), (0, 0, width, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        pg.draw.line(piece.image, (0, 0, 0), (tileSize + tileOffset, 0), (tileSize + tileOffset, height))
        pg.draw.line(piece.image, (0, 0, 0), (tileSize + tileOffset*2, 0), (tileSize + tileOffset*2, height))
        pg.draw.line(piece.image, (0, 0, 0), (tileSize + tileOffset*3, 0), (tileSize + tileOffset*3, height))
        return piece
    # ....
    @staticmethod
    def getLong4(tileOffset, tileSize, color):
        width = tileOffset * 4 - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        pg.draw.rect(piece.image, (0,0,0), (0, 0, width, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        pg.draw.line(piece.image, (0, 0, 0), (tileSize + tileOffset, 0), (tileSize + tileOffset, height))
        pg.draw.line(piece.image, (0, 0, 0), (tileSize + tileOffset*2, 0), (tileSize + tileOffset*2, height))
        return piece
    # ...
    @staticmethod
    def getLong3(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        pg.draw.rect(piece.image, (0,0,0), (0, 0, width, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        pg.draw.line(piece.image, (0, 0, 0), (tileSize + tileOffset, 0), (tileSize + tileOffset, height))
        return piece
    # ..
    @staticmethod
    def getLong2(tileOffset, tileSize, color):
        width = tileOffset * 2 - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        pg.draw.rect(piece.image, (0,0,0), (0, 0, width, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        return piece
    # .
    @staticmethod
    def getDot(tileOffset, tileSize, color):
        width = tileOffset - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        pg.draw.rect(piece.image, (0,0,0), (0, 0, width, height), 1)
        return piece
    #    .
    # ....
    @staticmethod
    def getL4(tileOffset, tileSize, color):
        width = tileOffset * 4 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset * 2, tileSize))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileSize, tileSize + tileOffset * 4, tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize + tileOffset * 2, 0, tileOffset, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, tileOffset), (tileSize, height))
        pg.draw.line(piece.image, (0, 0, 0), (tileSize + tileOffset, tileOffset), (tileSize + tileOffset, height))
        return piece

    #   .
    # ...
    @staticmethod
    def getL3(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset,tileSize))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileSize, tileSize + tileOffset * 3, tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize + tileOffset, 0, tileOffset, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, tileOffset), (tileSize, height))
        return piece
    @staticmethod
    def getL2(tileOffset, tileSize, color):
        width = tileOffset * 2 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize,tileSize))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileSize, tileSize + tileOffset * 2, tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize, 0, tileOffset, height), 1)
        return piece
    @staticmethod
    def getL33(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset,tileSize + tileOffset))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileSize + tileOffset, tileSize + tileOffset * 3, tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize + tileOffset, 0, tileOffset, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, tileSize + tileOffset), (tileSize, height))
        pg.draw.line(piece.image, (0, 0, 0), (tileSize + tileOffset * 1, tileSize), (tileSize + tileOffset * 2, tileSize))
        return piece
    @staticmethod
    def getPlus(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0,tileOffset,tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (tileSize + tileOffset,0,tileOffset,tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (0, tileSize + tileOffset,tileOffset,tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (tileSize + tileOffset,tileSize + tileOffset,tileOffset,tileOffset))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileSize, tileSize + tileOffset * 2, tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize, 0, tileOffset, height), 1)
        return piece
    @staticmethod
    def getHat(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (tileSize, tileSize,tileOffset,tileOffset))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, tileSize + tileOffset * 2, tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize + tileOffset, 0,tileOffset, tileSize + tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0,tileOffset, tileSize + tileOffset), 1)
        return piece
    @staticmethod
    def getSquare(tileOffset, tileSize, color):
        width = tileOffset * 2 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, tileSize + tileOffset, tileSize + tileOffset), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        pg.draw.line(piece.image, (0, 0, 0), (0, tileSize), (tileSize + tileOffset, tileSize))
        return piece
    @staticmethod
    def getF(tileOffset, tileSize, color):
        width = tileOffset * 4 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, tileOffset, tileSize + tileOffset,tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (tileSize + tileOffset * 2, tileOffset,tileOffset,tileOffset))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, width, tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize + tileOffset, 0, tileOffset, tileSize + tileOffset), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, tileSize))
        return piece
    @staticmethod
    def getZ(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset,tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (tileOffset, tileSize + tileOffset, tileSize + tileOffset,tileOffset))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileOffset,tileOffset, tileSize +tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize + tileOffset, 0,tileOffset, tileSize +tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileOffset,width,tileSize), 1)
        return piece
    @staticmethod
    def getStair(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset,tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (0, tileOffset,tileOffset,tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (tileSize + tileOffset,tileSize + tileOffset,tileOffset,tileOffset))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize + tileOffset, 0, tileOffset, tileSize +tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileOffset, tileOffset, tileOffset, tileSize +tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileSize + tileOffset,tileOffset + 1, tileOffset), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileOffset, tileOffset), (width, tileOffset))
        pg.draw.line(piece.image, (0, 0, 0), (tileOffset, tileSize + tileOffset-1), (width, tileSize +tileOffset-1))
        return piece
    @staticmethod
    def getT(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (tileOffset, 0, tileSize + tileOffset,tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (tileOffset, tileSize + tileOffset, tileSize + tileOffset,tileOffset))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, tileOffset,height), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileOffset, width,tileOffset), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileOffset + tileSize, tileOffset), (tileOffset + tileSize, tileOffset + tileSize))
        return piece
    @staticmethod
    def getP(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (tileSize + tileOffset, 0, tileOffset,tileOffset))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, tileSize + tileOffset,tileSize + tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileOffset, width,tileSize), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, tileOffset + tileSize))
        return piece
    @staticmethod
    def getSquiggle(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileOffset,tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (tileSize + tileOffset, tileOffset, tileOffset,tileOffset))
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (tileOffset, 0, tileSize + tileOffset,tileOffset), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileOffset-1, tileSize + tileOffset,tileOffset), 1)
        # todo
        return piece
    @staticmethod
    def getWeird(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # todo
        return piece
    @staticmethod
    def getWeird2(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # todo
        return piece
    @staticmethod
    def getBolt(tileOffset, tileSize, color):
        width = tileOffset * 4 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height)
        # todo
        return piece

    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self, value):
        self.__width = value
    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self, value):
        self.__height = value
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, value):
        self.__x = value
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, value):
        self.__y = value
    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self, value):
        self.__color = value
        self.image.fill(value)

