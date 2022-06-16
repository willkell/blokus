import pygame as pg

from piece import Piece


class Player:
    def __init__(self, playerNum, playerType):
        self.playerNum = playerNum
        self.playerType = playerType
        self.score = 0
        self.played = False
        self.out = False
        self.pieces = []
        self.color = (0, 0, 0)
        self.deck = {
            "lowerLeft": [],
            "lowerRight": [],
            "upperLeft": [],
            "upperRight": [],
        }
        self.placements = {}

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

    def removeAllPiece(self, piece):
        for inv in reversed(self.pieces):
            if piece.type == inv.type:
                self.pieces.remove(inv)
        for inv in self.placements:
            for inv2 in reversed(self.placements[inv].pieces):
                if piece.type == inv2.type:
                    self.placements[inv].remove(inv2)
        for inv in self.deck:
            for inv2 in reversed(self.deck[inv]):
                if piece.type == inv2.type:
                    self.deck[inv].remove(inv2)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def placements(self):
        return self._placements

    @placements.setter
    def placements(self, placements):
        self._placements = placements

    @property
    def played(self):
        return self._played

    @played.setter
    def played(self, played):
        self._played = played

    @property
    def playerType(self):
        return self._playerType

    @playerType.setter
    def playerType(self, playerType):
        self._playerType = playerType

    @property
    def out(self):
        return self._out

    @out.setter
    def out(self, out):
        self._out = out

    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, deck):
        self._deck = deck

    class Placement:
        def __init__(self, type):
            self.pieces = []
            self.type = type

        @property
        def pieces(self):
            return self._pieces

        @pieces.setter
        def pieces(self, pieces):
            self._pieces = pieces

        def append(self, piece):
            self.pieces.append(piece)

        def remove(self, piece):
            self.pieces.remove(piece)

        def empty(self):
            return self.pieces == []

        @property
        def type(self):
            return self._type

        @type.setter
        def type(self, type):
            self._type = type
