import sys

import numpy as np
import pygame as pg

from piece import Piece
from player import Player


class Game:
    def __init__(self):
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player3 = Player(3)
        self.player4 = Player(4)
        self.screenHeight = 0
        self.screenWidth = 0
        self.boardSize = 0
        self.boardStartX = 0
        self.boardStartY = 0
        self.inventoryStartX = 0
        self.inventoryStartY = 0
        self.borderSize = 10
        self.tileSize = 0
        self.tileOffset = 0
        self.tileColor = (200, 200, 200)
        self.board = pg.Surface((0, 0))
        self.boardArray = [[Tile(self.tileColor)] * 20] * 20

    def run(self):
        pg.init()
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.set_up_screen(
            pg.display.get_surface().get_size()[0],
            pg.display.get_surface().get_size()[1],
        )
        self.board = self.draw_board()
        clock = pg.time.Clock()
        is_running = True
        self.player1.color = (255, 0, 0)
        Player.initPieces(
            self.player1, self.tileOffset, self.tileSize, self.player1.color
        )
        Player.initInventory(
            self.player1, self.inventoryStartX, self.inventoryStartY, self.tileOffset
        )
        canDrag = False
        dropped = False
        currPiece = None

        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
                ):
                    is_running = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    canDrag, currPiece = Player.checkForDrag(self.player1, event.pos)
                if event.type == pg.MOUSEBUTTONUP:
                    if canDrag:
                        dropped = self.dropPiece(currPiece)
                    canDrag = False
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    if dropped:
                        self.commitToBoard(self.player1, currPiece)
                        dropped = False
                        currPiece = None
                        Player.initInventory(
                            self.player1,
                            self.inventoryStartX,
                            self.inventoryStartY,
                            self.tileOffset,
                        )
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    if currPiece:
                        Piece.rotate(currPiece)

            mouse_rel = pg.mouse.get_rel()
            if canDrag:
                Piece.drag(currPiece, mouse_rel)
            screen.fill((255, 255, 255, 255))
            screen.blit(self.board, (self.boardStartX, self.boardStartY))
            Player.printPieces(self.player1, screen)
            pg.display.flip()
            clock.tick(60)

    def draw_board(self):
        board = pg.Surface((self.boardSize, self.boardSize))
        board.fill((100, 100, 100))
        for row in range(20):
            for col in range(20):
                pg.draw.rect(
                    board,
                    self.tileColor,
                    pg.Rect(
                        self.borderSize + (col * self.tileOffset),
                        self.borderSize + (row * self.tileOffset),
                        self.tileSize,
                        self.tileSize,
                    ),
                )
        return board

    def set_up_screen(self, height, width):
        self.screenHeight = width
        self.screenWidth = height
        self.boardSize = self.screenHeight * 0.8
        self.boardStartX = self.screenHeight * 0.05
        self.boardStartY = self.screenHeight * 0.1
        self.inventoryStartX = self.boardStartX + self.boardSize + self.boardStartX
        self.inventoryStartY = self.boardStartY
        self.tileSize = (self.boardSize - (self.borderSize * 2) - 19) / 20
        self.tileOffset = (self.boardSize - (self.borderSize * 2)) / 20

    def dropPiece(self, piece):
        # returns false if piece is not on board
        if (
            piece.x < self.boardStartX
            or piece.x > self.boardStartX + self.boardSize
            or piece.y < self.boardStartY
            or piece.y > self.boardStartY + self.boardSize
        ):
            return False
        # snaps to grid
        tileStartX = self.boardStartX + self.borderSize
        tileStartY = self.boardStartY + self.borderSize
        if (piece.x - tileStartX) % self.tileOffset > self.tileOffset / 2:
            piece.x = (
                piece.x + self.tileOffset - (piece.x - tileStartX) % self.tileOffset
            )
        else:
            piece.x = piece.x - ((piece.x - tileStartX) % self.tileOffset)
        if (piece.y - tileStartY) % self.tileOffset > self.tileOffset / 2:
            piece.y = (
                piece.y + self.tileOffset - (piece.y - tileStartY) % self.tileOffset
            )
        else:
            piece.y = piece.y - ((piece.y - tileStartY) % self.tileOffset)
        return True

    def commitToBoard(self, player, piece):
        # merges board image with piece image
        newBoard = pg.Surface((self.boardSize, self.boardSize))
        newBoard.blit(self.board, (0, 0))
        newBoard.blit(
            piece.image, (piece.x - self.boardStartX, piece.y - self.boardStartY)
        )
        self.board = newBoard
        Player.removePiece(player, piece)
        # merge piece image to board array
        rowTileStart = int(
            (piece.y - self.boardStartY - self.borderSize) / self.tileOffset
        )
        colTileStart = int(
            (piece.x - self.boardStartX - self.borderSize) / self.tileOffset
        )
        rowTile = rowTileStart
        colTile = colTileStart
        for row in np.arange(self.tileOffset / 2, piece.height, self.tileOffset):
            for col in np.arange(self.tileOffset / 2, piece.width, self.tileOffset):
                if piece.image.get_at((int(col), int(row))) == piece.color:
                    self.boardArray[rowTile][colTile].color = piece.color
                colTile += 1
            rowTile += 1
        # sets validity of board
        for row in range(rowTileStart - 1, rowTileStart + piece.sizeInTiles[0] + 1):
            for col in range(colTileStart - 1, colTileStart + piece.sizeInTiles[1] + 1):
                if row >= 0 and row <= 19 and col >= 0 and col <= 19:
                    if self.boardArray[row][col].color == self.tileColor:
                        pass

    def initBoard(self):
        self.boardArray[0][0].valid1 = True
        self.boardArray[0][-1].valid2 = True
        self.boardArray[-1][-1].valid3 = True
        self.boardArray[-1][0].valid4 = True


class Tile:
    def __init__(self, color):
        self.color = color
        self.valid1 = False
        self.valid2 = False
        self.valid3 = False
        self.valid4 = False

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def valid1(self):
        return self._valid1

    @valid1.setter
    def valid1(self, valid1):
        self._valid1 = valid1

    @property
    def valid2(self):
        return self._valid2

    @valid2.setter
    def valid2(self, valid2):
        self._valid2 = valid2

    @property
    def valid3(self):
        return self._valid3

    @valid3.setter
    def valid3(self, valid3):
        self._valid3 = valid3

    @property
    def valid4(self):
        return self._valid4

    @valid4.setter
    def valid4(self, valid4):
        self._valid4 = valid4
