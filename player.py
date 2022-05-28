import pygame as pg

from piece import Piece


class Player:
    def __init__(self, playerNum):
        self.playerNum = playerNum
        self.score = 0
        self.pieces = []
        self.color = (0, 0, 0)

    def initInventory(self, inventoryStartX, inventoryStartY, tileOffset):
        placeX = inventoryStartX
        placeY = inventoryStartY
        maxHeight = 0
        for piece in self.pieces:
            if (
                placeX + piece.width
                > pg.display.get_surface().get_size()[0] - tileOffset
            ):
                placeX = inventoryStartX
                placeY += maxHeight + tileOffset
                maxHeight = 0
            piece.x = placeX
            piece.y = placeY
            placeX += piece.width + tileOffset
            if piece.height > maxHeight:
                maxHeight = piece.height

    def printPieces(self, surface):
        for piece in self.pieces:
            surface.blit(piece.image, (piece.x, piece.y))

    def initPieces(self, tileOffset, tileSize, color):
        self.pieces.append(Piece.getLong5(tileOffset, tileSize, color))
        self.pieces.append(Piece.getLong4(tileOffset, tileSize, color))
        self.pieces.append(Piece.getLong3(tileOffset, tileSize, color))
        self.pieces.append(Piece.getLong2(tileOffset, tileSize, color))
        self.pieces.append(Piece.getDot(tileOffset, tileSize, color))
        self.pieces.append(Piece.getL4(tileOffset, tileSize, color))
        self.pieces.append(Piece.getL3(tileOffset, tileSize, color))
        self.pieces.append(Piece.getL2(tileOffset, tileSize, color))
        self.pieces.append(Piece.getL33(tileOffset, tileSize, color))
        self.pieces.append(Piece.getPlus(tileOffset, tileSize, color))
        self.pieces.append(Piece.getHat(tileOffset, tileSize, color))
        self.pieces.append(Piece.getSquare(tileOffset, tileSize, color))
        self.pieces.append(Piece.getF(tileOffset, tileSize, color))
        self.pieces.append(Piece.getZ(tileOffset, tileSize, color))
        self.pieces.append(Piece.getStair(tileOffset, tileSize, color))
        self.pieces.append(Piece.getT(tileOffset, tileSize, color))
        self.pieces.append(Piece.getP(tileOffset, tileSize, color))
        self.pieces.append(Piece.getSquiggle(tileOffset, tileSize, color))
        self.pieces.append(Piece.getWeird(tileOffset, tileSize, color))
        self.pieces.append(Piece.getWeird2(tileOffset, tileSize, color))
        self.pieces.append(Piece.getBolt(tileOffset, tileSize, color))

    def checkForDrag(self, pos):
        for piece in self.pieces:
            if (
                piece.x < pos[0] < piece.x + piece.width
                and piece.y < pos[1] < piece.y + piece.height
            ):
                return True, piece
        return False, None

    def removePiece(self, piece):
        self.pieces.remove(piece)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
