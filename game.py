import sys

# import numpy as np
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
        self.boardArray = []
        for row in range(20):
            self.boardArray.append([])
            for col in range(20):
                self.boardArray[row].append(self.tileColor)

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
        round = 1

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
                    if dropped and (
                        self.checkValidityTurn1(self.player1, currPiece)
                        if round == 1
                        else self.checkValidity(self.player1, currPiece)
                    ):
                        self.commitToBoard(self.player1, currPiece)
                        dropped = False
                        currPiece = None
                        Player.initInventory(
                            self.player1,
                            self.inventoryStartX,
                            self.inventoryStartY,
                            self.tileOffset,
                        )
                        round += 1
                    else:
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
        self.boardSize = min(self.screenHeight, self.screenWidth) * 0.8
        self.boardStartX = self.screenHeight * 0.05
        self.boardStartY = self.screenHeight * 0.1
        if self.screenWidth > self.screenHeight:
            self.inventoryStartX = self.boardStartX + self.boardSize + self.boardStartX
            self.inventoryStartY = self.boardStartY
        else:
            self.inventoryStartX = self.boardStartX
            self.inventoryStartY = self.boardStartY + self.boardSize + self.boardStartY
        self.tileSize = (self.boardSize - (self.borderSize * 2) - 19) / 20
        self.tileOffset = (self.boardSize - (self.borderSize * 2)) / 20

    def snapToGrid(self, piece):
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

    def dropPiece(self, piece):
        # returns false if piece is not on board
        if (
            piece.x <= self.boardStartX + self.borderSize - self.tileOffset / 2
            or piece.x + piece.width
            >= self.boardStartX
            + self.boardSize
            - self.borderSize
            + self.tileOffset / 2
            - 1
            or piece.y <= self.boardStartY + self.borderSize - self.tileOffset / 2
            or piece.y + piece.height
            >= self.boardStartY
            + self.boardSize
            - self.borderSize
            + self.tileOffset / 2
            - 1
        ):
            return False

        self.snapToGrid(piece)
        return True

    def withinBoard(self, row, col):
        return 0 <= row < 20 and 0 <= col < 20

    def checkValidityTurn1(self, player, piece):
        pieceRow = round(
            (piece.y - self.boardStartY - self.borderSize) / self.tileOffset
        )
        pieceCol = round(
            (piece.x - self.boardStartX - self.borderSize) / self.tileOffset
        )
        return pieceRow == 0 and pieceCol == 0 and piece.array[1][1] == "p"

    def validFailureMsg(self, row, col, should, was):
        return "Tile at row {}, col {} should be {} but was {}".format(
            row, col, should, was
        )

    def checkValidity(self, player, piece):
        # print("Before piece:")
        # for row in range(20):
        #     for col in range(20):
        #         if self.boardArray[row][col] == self.tileColor:
        #             print("n ", end="")
        #         else:
        #             print("y ", end="")
        #     print()
        isValid = False
        rowTileArrStart = round(
            ((piece.y - self.boardStartY - self.borderSize) / self.tileOffset) - 1
        )
        colTileArrStart = round(
            ((piece.x - self.boardStartX - self.borderSize) / self.tileOffset) - 1
        )
        rowTile = rowTileArrStart
        colTile = colTileArrStart
        for row in piece.array:
            for tile in row:
                # print("checking tile at row {}, col {}".format(rowTile, colTile))
                if tile == "p":
                    if (
                        self.withinBoard(rowTile, colTile)
                        and self.boardArray[rowTile][colTile] != self.tileColor
                    ):
                        # print(
                        #     self.validFailureMsg(
                        #         rowTile,
                        #         colTile,
                        #         "empty",
                        #         "full",
                        #     )
                        # )
                        return False
                elif tile == "n":
                    if (
                        self.withinBoard(rowTile, colTile)
                        and self.boardArray[rowTile][colTile] == player.color
                    ):
                        # print(
                        #     self.validFailureMsg(
                        #         rowTile, colTile, "not same color", "same color"
                        #     )
                        # )
                        return False
                elif tile == "y":
                    if (
                        self.withinBoard(rowTile, colTile)
                        and self.boardArray[rowTile][colTile] == player.color
                    ):
                        isValid = True
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart
        # if not isValid:
        #     print("No piece in range")
        return isValid

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
        rowTileArrStart = round(
            ((piece.y - self.boardStartY - self.borderSize) / self.tileOffset) - 1
        )
        colTileArrStart = round(
            ((piece.x - self.boardStartX - self.borderSize) / self.tileOffset) - 1
        )
        rowTile = rowTileArrStart
        colTile = colTileArrStart
        for row in piece.array:
            for tile in row:
                if tile == "p":
                    self.boardArray[rowTile][colTile] = player.color
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart
