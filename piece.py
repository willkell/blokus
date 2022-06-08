import copy

import pygame as pg


class Piece:
    def __init__(
        self,
        x=0,
        y=0,
        color=(0, 0, 0),
        width=0,
        height=0,
        sizeInTiles=[0, 0],
        numTiles=0,
        symmetryX=False,
        symmetryY=False,
    ):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.color = color
        self.sizeInTiles = sizeInTiles
        self.array = []
        self.numTiles = numTiles
        self.symmetryX = symmetryX
        self.symmetryY = symmetryY
        for _ in range(sizeInTiles[1] + 2):
            rowArray = []
            for _ in range(sizeInTiles[0] + 2):
                rowArray.append("x")
            self.array.append(rowArray)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if hasattr(v, "copy") and callable(getattr(v, "copy")):
                setattr(result, k, v.copy())
            else:
                setattr(result, k, copy.deepcopy(v, memo))
        return result

    def drag(self, mouse_rel):
        self.x += mouse_rel[0]
        self.y += mouse_rel[1]

    def flipOverX(self):
        self.image = pg.transform.flip(self.image, True, False)
        newArray = []
        # for row in range(len(self.array)):
        #     rowArray = []
        #     for col in range(len(self.array[0])):
        #         rowArray.append("x")
        #     newArray.append(rowArray)
        # row = 0
        # col = 0
        # for r in self.array:
        #     for c in reversed(r):
        #         newArray[row][col] = c
        #         col += 1
        #     row += 1
        #     col = 0
        # self.array = newArray
        for r in self.array:
            rowArray = []
            for c in reversed(r):
                rowArray.append(c)
            newArray.append(rowArray)
        self.array = newArray

    def flipOverY(self):
        self.image = pg.transform.flip(self.image, False, True)
        newArray = []
        # for row in range(len(self.array)):
        #     rowArray = []
        #     for col in range(len(self.array[0])):
        #         rowArray.append("x")
        #     newArray.append(rowArray)
        # row = 0
        # col = 0
        # for r in reversed(self.array):
        #     for c in r:
        #         newArray[row][col] = c
        #         col += 1
        #     row += 1
        #     col = 0
        # self.array = newArray
        for r in reversed(self.array):
            rowArray = []
            for c in r:
                rowArray.append(c)
            newArray.append(rowArray)
        self.array = newArray

    def rotateCCW(self):
        # print("before rotation:")
        # self.printArray()
        self.image = pg.transform.rotate(self.image, -90)
        temp = self.width
        self.width = self.height
        self.height = temp
        temp = self.sizeInTiles[0]
        self.sizeInTiles[0] = self.sizeInTiles[1]
        self.sizeInTiles[1] = temp
        # rotate array counterclockwise
        newArray = []
        for row in range(len(self.array[0])):
            rowArray = []
            for col in range(len(self.array)):
                rowArray.append("x")
            newArray.append(rowArray)
        row = 0
        col = 0

        for i in range(len(self.array[0])):
            for j in reversed(range(len(self.array))):
                newArray[row][col] = self.array[j][i]
                col += 1
            row += 1
            col = 0
        self.array = newArray
        # set symmetry
        temp = self.symmetryX
        self.symmetryX = self.symmetryY
        self.symmetryY = temp
        # print("after rotation:")
        # self.printArray()

    def rotateCW(self):
        self.image = pg.transform.rotate(self.image, 90)
        temp = self.width
        self.width = self.height
        self.height = temp
        temp = self.sizeInTiles[0]
        self.sizeInTiles[0] = self.sizeInTiles[1]
        self.sizeInTiles[1] = temp
        # rotate array clockwise
        newArray = []
        for row in range(len(self.array[0])):
            rowArray = []
            for col in range(len(self.array)):
                rowArray.append("x")
            newArray.append(rowArray)
        row = 0
        col = 0

        for i in reversed(range(len(self.array[0]))):
            for j in range(len(self.array)):
                newArray[row][col] = self.array[j][i]
                col += 1
            row += 1
            col = 0
        self.array = newArray
        # set symmetry
        temp = self.symmetryX
        self.symmetryX = self.symmetryY
        self.symmetryY = temp

    def printArray(self):
        for row in self.array:
            for char in row:
                print(char + " ", end="")
            print("\n")
        print("\n")

    # .....
    @staticmethod
    def getLong5(tileOffset, tileSize, color):
        width = tileOffset * 5 - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [1, 5], 5, True, True)
        piece.array = [
            ["y", "n", "n", "n", "n", "n", "y"],
            ["n", "p", "p", "p", "p", "p", "n"],
            ["y", "n", "n", "n", "n", "n", "y"],
        ]
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, width, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, 0),
            (tileSize + tileOffset, height),
        )
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset * 2, 0),
            (tileSize + tileOffset * 2, height),
        )
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset * 3, 0),
            (tileSize + tileOffset * 3, height),
        )
        return piece

    # ....
    @staticmethod
    def getLong4(tileOffset, tileSize, color):
        width = tileOffset * 4 - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [1, 4], 4, True, True)
        piece.array = [
            ["y", "n", "n", "n", "n", "y"],
            ["n", "p", "p", "p", "p", "n"],
            ["y", "n", "n", "n", "n", "y"],
        ]

        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, width, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, 0),
            (tileSize + tileOffset, height),
        )
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset * 2, 0),
            (tileSize + tileOffset * 2, height),
        )
        return piece

    # ...
    @staticmethod
    def getLong3(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [1, 3], 3, True, True)
        piece.array = [
            ["y", "n", "n", "n", "y"],
            ["n", "p", "p", "p", "n"],
            ["y", "n", "n", "n", "y"],
        ]
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, width, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, 0),
            (tileSize + tileOffset, height),
        )
        return piece

    # ..
    @staticmethod
    def getLong2(tileOffset, tileSize, color):
        width = tileOffset * 2 - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [1, 2], 2, True, True)
        piece.array = [
            ["y", "n", "n", "y"],
            ["n", "p", "p", "n"],
            ["y", "n", "n", "y"],
        ]
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, width, height), 1)
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        return piece

    # .
    @staticmethod
    def getDot(tileOffset, tileSize, color):
        width = tileOffset - (tileOffset - tileSize)
        height = tileOffset - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [1, 1], 1, True, True)
        piece.array = [
            ["y", "n", "y"],
            ["n", "p", "n"],
            ["y", "n", "y"],
        ]
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, width, height), 1)
        return piece

    #    .
    # ....
    @staticmethod
    def getL4(tileOffset, tileSize, color):
        width = tileOffset * 4 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 4], 5, False, False)
        piece.array = [
            [" ", " ", " ", "y", "n", "y"],
            ["y", "n", "n", "n", "p", "n"],
            ["n", "p", "p", "p", "p", "n"],
            ["y", "n", "n", "n", "n", "y"],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(
            piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset * 2, tileSize)
        )
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, tileSize, tileSize + tileOffset * 4, tileOffset),
            1,
        )
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset * 2, 0, tileOffset, height),
            1,
        )
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, tileOffset), (tileSize, height))
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, tileOffset),
            (tileSize + tileOffset, height),
        )
        return piece

    #   .
    # ...
    @staticmethod
    def getL3(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 3], 4, False, False)
        piece.array = [
            [" ", " ", "y", "n", "y"],
            ["y", "n", "n", "p", "n"],
            ["n", "p", "p", "p", "n"],
            ["y", "n", "n", "n", "y"],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset, tileSize))
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, tileSize, tileSize + tileOffset * 3, tileOffset),
            1,
        )
        pg.draw.rect(
            piece.image, (0, 0, 0), (tileSize + tileOffset, 0, tileOffset, height), 1
        )
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, tileOffset), (tileSize, height))
        return piece

    @staticmethod
    def getL2(tileOffset, tileSize, color):
        width = tileOffset * 2 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 2], 3, False, False)
        piece.array = [
            [" ", "y", "n", "y"],
            ["y", "n", "p", "n"],
            ["n", "p", "p", "n"],
            ["y", "n", "n", "y"],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize, tileSize))
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, tileSize, tileSize + tileOffset * 2, tileOffset),
            1,
        )
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize, 0, tileOffset, height), 1)
        return piece

    @staticmethod
    def getL33(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [3, 3], 5, False, False)
        piece.array = [
            [" ", " ", "y", "n", "y"],
            [" ", " ", "n", "p", "n"],
            ["y", "n", "n", "p", "n"],
            ["n", "p", "p", "p", "n"],
            ["y", "n", "n", "n", "y"],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(
            piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset, tileSize + tileOffset)
        )
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, tileSize + tileOffset, tileSize + tileOffset * 3, tileOffset),
            1,
        )
        pg.draw.rect(
            piece.image, (0, 0, 0), (tileSize + tileOffset, 0, tileOffset, height), 1
        )
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize, tileSize + tileOffset),
            (tileSize, height),
        )
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset * 1, tileSize),
            (tileSize + tileOffset * 2, tileSize),
        )
        return piece

    @staticmethod
    def getPlus(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [3, 3], 5, True, True)
        piece.array = [
            [" ", "y", "n", "y", " "],
            ["y", "n", "p", "n", "y"],
            ["n", "p", "p", "p", "n"],
            ["y", "n", "p", "n", "y"],
            [" ", "y", "n", "y", " "],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileOffset, tileOffset))
        pg.draw.rect(
            piece.image, (0, 1, 0), (tileSize + tileOffset, 0, tileOffset, tileOffset)
        )
        pg.draw.rect(
            piece.image, (0, 1, 0), (0, tileSize + tileOffset, tileOffset, tileOffset)
        )
        pg.draw.rect(
            piece.image,
            (0, 1, 0),
            (tileSize + tileOffset, tileSize + tileOffset, tileOffset, tileOffset),
        )
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, tileSize, tileSize + tileOffset * 2, tileOffset),
            1,
        )
        pg.draw.rect(piece.image, (0, 0, 0), (tileSize, 0, tileOffset, height), 1)
        return piece

    @staticmethod
    def getHat(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 3], 5, True, False)
        piece.array = [
            ["y", "n", "n", "n", "y"],
            ["n", "p", "p", "p", "n"],
            ["n", "p", "n", "p", "n"],
            ["y", "n", "y", "n", "y"],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(
            piece.image, (0, 1, 0), (tileOffset, tileOffset, tileOffset, tileOffset)
        )
        # lines
        pg.draw.rect(
            piece.image, (0, 0, 0), (0, 0, tileSize + tileOffset * 2, tileOffset), 1
        )
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, 0, tileOffset, tileSize + tileOffset),
            1,
        )
        pg.draw.rect(
            piece.image, (0, 0, 0), (0, 0, tileOffset, tileSize + tileOffset), 1
        )
        return piece

    @staticmethod
    def getSquare(tileOffset, tileSize, color):
        width = tileOffset * 2 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 2], 4, True, True)
        piece.array = [
            ["y", "n", "n", "y"],
            ["n", "p", "p", "n"],
            ["n", "p", "p", "n"],
            ["y", "n", "n", "y"],
        ]
        # transparency
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, 0, tileSize + tileOffset, tileSize + tileOffset),
            1,
        )
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, height))
        pg.draw.line(
            piece.image, (0, 0, 0), (0, tileSize), (tileSize + tileOffset, tileSize)
        )
        return piece

    @staticmethod
    def getF(tileOffset, tileSize, color):
        width = tileOffset * 4 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 4], 5, False, False)
        piece.array = [
            ["y", "n", "n", "n", "n", "y"],
            ["n", "p", "p", "p", "p", "n"],
            ["y", "n", "n", "p", "n", "y"],
            [" ", " ", "y", "n", "y", " "],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(
            piece.image, (0, 1, 0), (0, tileOffset, tileSize + tileOffset, tileOffset)
        )
        pg.draw.rect(
            piece.image,
            (0, 1, 0),
            (tileSize + tileOffset * 2 + 1, tileOffset, tileOffset, tileOffset),
        )
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, width, tileOffset), 1)
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, 0, tileOffset, tileSize + tileOffset),
            1,
        )
        pg.draw.line(piece.image, (0, 0, 0), (tileSize, 0), (tileSize, tileSize))
        return piece

    @staticmethod
    def getZ(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [3, 3], 5, False, False)
        piece.array = [
            [" ", " ", "y", "n", "y"],
            ["y", "n", "n", "p", "n"],
            ["n", "p", "p", "p", "n"],
            ["n", "p", "n", "n", "y"],
            ["y", "n", "y", " ", " "],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset, tileOffset))
        pg.draw.rect(
            piece.image,
            (0, 1, 0),
            (tileOffset, tileSize + tileOffset, tileSize + tileOffset, tileOffset),
        )
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, tileOffset, tileOffset, tileSize + tileOffset),
            1,
        )
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, 0, tileOffset, tileSize + tileOffset),
            1,
        )
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileOffset, width, tileSize), 1)
        return piece

    @staticmethod
    def getStair(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [3, 3], 5, False, False)
        piece.array = [
            [" ", " ", "y", "n", "y"],
            [" ", "y", "n", "p", "n"],
            ["y", "n", "p", "p", "n"],
            ["n", "p", "p", "n", "y"],
            ["y", "n", "n", "y", " "],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileSize + tileOffset, tileOffset))
        pg.draw.rect(piece.image, (0, 1, 0), (0, tileOffset, tileOffset, tileOffset))
        pg.draw.rect(
            piece.image,
            (0, 1, 0),
            (tileSize + tileOffset, tileSize + tileOffset, tileOffset, tileOffset),
        )
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, 0, tileOffset, tileSize + tileOffset),
            1,
        )
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (tileOffset, tileOffset, tileOffset, tileSize + tileOffset),
            1,
        )
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, tileSize + tileOffset, tileOffset + 1, tileOffset),
            1,
        )
        pg.draw.line(
            piece.image, (0, 0, 0), (tileOffset, tileOffset), (width, tileOffset)
        )
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileOffset, tileSize + tileOffset - 1),
            (width, tileSize + tileOffset - 1),
        )
        return piece

    @staticmethod
    def getT(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [3, 3], 5, False, True)
        piece.array = [
            ["y", "n", "y", " ", " "],
            ["n", "p", "n", "n", "y"],
            ["n", "p", "p", "p", "n"],
            ["n", "p", "n", "n", "y"],
            ["y", "n", "y", " ", " "],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(
            piece.image, (0, 1, 0), (tileOffset, 0, tileSize + tileOffset, tileOffset)
        )
        pg.draw.rect(
            piece.image,
            (0, 1, 0),
            (tileOffset, tileSize + tileOffset, tileSize + tileOffset, tileOffset),
        )
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, tileOffset, height), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileOffset, width, tileOffset), 1)
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileOffset + tileSize, tileOffset),
            (tileOffset + tileSize, tileOffset + tileSize),
        )
        return piece

    @staticmethod
    def getP(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 3], 5, False, False)
        piece.array = [
            ["y", "n", "n", "y", " "],
            ["n", "p", "p", "n", "y"],
            ["n", "p", "p", "p", "n"],
            ["y", "n", "n", "n", "y"],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(
            piece.image, (0, 1, 0), (tileSize + tileOffset, 0, tileOffset, tileOffset)
        )
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, 0, tileSize + tileOffset, tileSize + tileOffset),
            1,
        )
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileOffset, width, tileSize), 1)
        pg.draw.line(
            piece.image, (0, 0, 0), (tileSize, 0), (tileSize, tileOffset + tileSize)
        )
        return piece

    @staticmethod
    def getSquiggle(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 3], 4, False, False)
        piece.array = [
            [" ", "y", "n", "n", "y"],
            ["y", "n", "p", "p", "n"],
            ["n", "p", "p", "n", "y"],
            ["y", "n", "n", "y", " "],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileOffset, tileOffset))
        pg.draw.rect(
            piece.image,
            (0, 1, 0),
            (tileSize + tileOffset, tileOffset, tileOffset, tileOffset),
        )
        # lines
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (tileOffset, 0, tileSize + tileOffset, tileOffset),
            1,
        )
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (0, tileOffset - 1, tileSize + tileOffset, tileOffset),
            1,
        )
        pg.draw.line(
            piece.image, (0, 0, 0), (tileOffset, tileOffset), (tileOffset, height)
        )
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileOffset + tileSize - 1, 0),
            (tileOffset + tileSize - 1, tileSize),
        )
        return piece

    @staticmethod
    def getWeird(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 3 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [3, 3], 5, False, False)
        piece.array = [
            ["y", "n", "n", "y", " "],
            ["n", "p", "p", "n", "y"],
            ["y", "n", "p", "p", "n"],
            ["y", "n", "p", "n", "y"],
            [" ", "y", "n", "y", " "],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(
            piece.image, (0, 1, 0), (0, tileOffset, tileOffset, tileSize + tileOffset)
        )
        pg.draw.rect(
            piece.image, (0, 1, 0), (tileSize + tileOffset, 0, tileOffset, tileOffset)
        )
        pg.draw.rect(
            piece.image,
            (0, 1, 0),
            (tileSize + tileOffset, tileSize + tileOffset, tileOffset, tileOffset),
        )
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (tileOffset, 0, tileOffset, height), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (0, 0, tileOffset + 1, tileOffset), 1)
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (tileOffset, tileOffset, tileSize + tileOffset, tileOffset),
            1,
        )
        return piece

    @staticmethod
    def getWeird2(tileOffset, tileSize, color):
        width = tileOffset * 3 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 3], 4, True, False)
        piece.array = [
            [" ", "y", "n", "y", " "],
            ["y", "n", "p", "n", "y"],
            ["n", "p", "p", "p", "n"],
            ["y", "n", "n", "n", "y"],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(piece.image, (0, 1, 0), (0, 0, tileOffset, tileOffset))
        pg.draw.rect(
            piece.image, (0, 1, 0), (tileSize + tileOffset, 0, tileOffset, tileOffset)
        )
        # lines
        pg.draw.rect(piece.image, (0, 0, 0), (0, tileOffset, width, tileSize), 1)
        pg.draw.rect(piece.image, (0, 0, 0), (tileOffset, 0, tileSize, height), 1)
        return piece

    @staticmethod
    def getBolt(tileOffset, tileSize, color):
        width = tileOffset * 4 - (tileOffset - tileSize)
        height = tileOffset * 2 - (tileOffset - tileSize)
        piece = Piece(0, 0, color, width, height, [2, 4], 5, False, False)
        piece.array = [
            ["y", "n", "n", "n", "y", " "],
            ["n", "p", "p", "p", "n", "y"],
            ["y", "n", "n", "p", "p", "n"],
            [" ", " ", "y", "n", "n", "y"],
        ]
        # transparency
        piece.image.set_colorkey((0, 1, 0))
        pg.draw.rect(
            piece.image, (0, 1, 0), (tileOffset * 3, 0, tileOffset, tileOffset)
        )
        pg.draw.rect(
            piece.image, (0, 1, 0), (0, tileOffset, tileSize + tileOffset, tileOffset)
        )
        # lines
        pg.draw.rect(
            piece.image, (0, 0, 0), (0, 0, tileSize + 2 * tileOffset, tileOffset), 1
        )
        pg.draw.rect(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, tileOffset - 1, tileSize + tileOffset, tileOffset),
            1,
        )
        pg.draw.line(piece.image, (0, 0, 0), (tileOffset, 0), (tileOffset, tileOffset))
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + 2 * tileOffset, tileOffset),
            (tileSize + 2 * tileOffset, tileSize + tileOffset),
        )
        pg.draw.line(
            piece.image,
            (0, 0, 0),
            (tileSize + tileOffset, 0),
            (tileSize + tileOffset, tileOffset),
        )
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

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def sizeInTiles(self):
        return self.__sizeInTiles

    @sizeInTiles.setter
    def sizeInTiles(self, value):
        self.__sizeInTiles = value

    @property
    def array(self):
        return self.__array

    @array.setter
    def array(self, value):
        self.__array = value

    @property
    def numTiles(self):
        return self.__numTiles

    @numTiles.setter
    def numTiles(self, value):
        self.__numTiles = value

    @property
    def symmetryX(self):
        return self.__symmetryX

    @symmetryX.setter
    def symmetryX(self, value):
        self.__symmetryX = value

    @property
    def symmetryY(self):
        return self.__symmetryY

    @symmetryY.setter
    def symmetryY(self, value):
        self.__symmetryY = value
