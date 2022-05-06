import pygame as pg
import piece


class Player:
    def __init__(self, playerNum):
        self.playerNum = playerNum
        self.score = 0
        self.pieces = []
        self.out = False
    def printPieces(self, surface):
        placeX = 1000
        placeY = 100
        for piece in self.pieces:
            surface.blit(piece.image, (placeX, placeY))
            piece.x = placeX
            piece.y = placeY
            placeX += 45 * 5
            if (placeX > 2000 - piece.width):
                placeX = 1000
                placeY += 45 * 3
    def initPieces(self, tileOffset, tileSize, color):
        self.pieces.append(piece.Piece.getLong5(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getLong4(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getLong3(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getLong2(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getDot(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getL4(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getL3(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getL2(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getL33(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getPlus(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getHat(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getSquare(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getF(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getZ(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getStair(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getT(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getP(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getSquiggle(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getWeird(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getWeird2(tileOffset, tileSize, color))
        self.pieces.append(piece.Piece.getBolt(tileOffset, tileSize, color))




