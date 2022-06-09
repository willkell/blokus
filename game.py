import copy
import random
import sys
import time

# import numpy as np
import pygame as pg

from piece import Piece
from player import Player

# import time


class Game:
    def __init__(self):
        self.player1 = Player(1, "AI")
        self.player2 = Player(2, "AI")
        self.player3 = Player(3, "AI")
        self.player4 = Player(4, "AI")
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
        self.nextPlayer = {
            self.player1: self.player2,
            self.player2: self.player3,
            self.player3: self.player4,
            self.player4: self.player1,
        }
        self.safeCorners = {
            self.player1: [0, 0],
            self.player2: [0, 19],
            self.player3: [19, 19],
            self.player4: [19, 0],
        }
        self.importantTile = {
            self.player1: [1, 1],
            self.player2: [1, -2],
            self.player3: [-2, -2],
            self.player4: [-2, 1],
        }

    def getRandomMove(self, currentPlayer, screen):
        currentPlayer.played = True
        placement = random.choice(list(currentPlayer.placements.keys()))
        piece = random.choice(currentPlayer.placements[placement])
        currentPlayer.placements.pop(placement)
        currentPlayer.pieces.append(piece)
        currentPlayer.score += piece.numTiles
        self.commitToBoard(currentPlayer, piece, screen)
        self.updatePlacements()
        Player.initInventory(
            currentPlayer,
            self.inventoryStartX,
            self.inventoryStartY,
            self.tileOffset,
        )
        currentPlayer = self.getNextPlayer(currentPlayer)
        Player.initInventory(
            currentPlayer,
            self.inventoryStartX,
            self.inventoryStartY,
            self.tileOffset,
        )
        return currentPlayer

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
        self.player2.color = (0, 255, 0)
        self.player3.color = (0, 0, 255)
        self.player4.color = (255, 255, 0)
        Player.initPieces(
            self.player1, self.tileOffset, self.tileSize, self.player1.color
        )
        Player.initInventory(
            self.player1, self.inventoryStartX, self.inventoryStartY, self.tileOffset
        )
        Player.initPieces(
            self.player2, self.tileOffset, self.tileSize, self.player2.color
        )
        Player.initInventory(
            self.player2, self.inventoryStartX, self.inventoryStartY, self.tileOffset
        )
        Player.initPieces(
            self.player3, self.tileOffset, self.tileSize, self.player3.color
        )
        Player.initInventory(
            self.player3, self.inventoryStartX, self.inventoryStartY, self.tileOffset
        )
        Player.initPieces(
            self.player4, self.tileOffset, self.tileSize, self.player4.color
        )
        Player.initInventory(
            self.player4, self.inventoryStartX, self.inventoryStartY, self.tileOffset
        )
        currentPlayer = self.player1
        canDrag = False
        dropped = False
        currPiece = None
        outCounter = 0
        self.player1.placements[(0, 0)] = []
        self.initialPlacement(self.player1, 0, 0, screen)
        self.player2.placements[(0, 19)] = []
        self.initialPlacement(self.player2, 0, 19, screen)
        self.player3.placements[(19, 19)] = []
        self.initialPlacement(self.player3, 19, 19, screen)
        self.player4.placements[(19, 0)] = []
        self.initialPlacement(self.player4, 19, 0, screen)

        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
                ):
                    is_running = False
                    print("Game over")
                    print("Player 1:", self.player1.score)
                    print("Player 2:", self.player2.score)
                    print("Player 3:", self.player3.score)
                    print("Player 4:", self.player4.score)
                    maxScore = max(
                        self.player1.score,
                        self.player2.score,
                        self.player3.score,
                        self.player4.score,
                    )
                    if self.player1.score == maxScore:
                        print("Player 1 wins", end="")
                    elif self.player2.score == maxScore:
                        print("Player 2 wins", end="")
                    elif self.player3.score == maxScore:
                        print("Player 3 wins", end="")
                    elif self.player4.score == maxScore:
                        print("Player 4 wins", end="")
                    print(" With a score of:", maxScore)

                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    canDrag, currPiece = Player.checkForDrag(currentPlayer, event.pos)
                if event.type == pg.MOUSEBUTTONUP:
                    if canDrag:
                        dropped = self.dropPiece(currPiece)
                    canDrag = False
                if event.type == pg.KEYDOWN and event.key == pg.K_p:
                    currentPlayer = self.getNextPlayer(currentPlayer)
                    Player.initInventory(
                        currentPlayer,
                        self.inventoryStartX,
                        self.inventoryStartY,
                        self.tileOffset,
                    )
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    if dropped and (
                        self.checkValidity(currentPlayer, currPiece)
                        if currentPlayer.played
                        else self.checkValidityTurn1(currentPlayer, currPiece)
                    ):
                        currentPlayer.played = True
                        currentPlayer.pieces.append(currPiece)
                        self.updatePlacements()
                        self.commitToBoard(currentPlayer, currPiece, screen)
                        currentPlayer.score += currPiece.numTiles
                        Player.removeAllPiece(currentPlayer, currPiece)
                        dropped = False
                        currPiece = None
                        Player.initInventory(
                            currentPlayer,
                            self.inventoryStartX,
                            self.inventoryStartY,
                            self.tileOffset,
                        )
                        if len(currentPlayer.placements) == 0:
                            currentPlayer.out = True
                        currentPlayer = self.getNextPlayer(currentPlayer)
                        Player.initInventory(
                            currentPlayer,
                            self.inventoryStartX,
                            self.inventoryStartY,
                            self.tileOffset,
                        )
                        self.updatePlacements()
                    else:
                        Player.initInventory(
                            currentPlayer,
                            self.inventoryStartX,
                            self.inventoryStartY,
                            self.tileOffset,
                        )

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT or event.key == pg.K_f:
                        if currPiece:
                            Piece.rotateCCW(currPiece)
                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        if currPiece:
                            Piece.rotateCW(currPiece)
                    if event.key == pg.K_UP or event.key == pg.K_d:
                        if currPiece and not currPiece.symmetryX:
                            Piece.flipOverX(currPiece)
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        if currPiece and not currPiece.symmetryY:
                            Piece.flipOverY(currPiece)
                    if event.key == pg.K_SPACE:
                        currentPlayer = self.getRandomMove(currentPlayer, screen)

            if not currentPlayer.placements and not currentPlayer.out:
                currentPlayer.out = True
                outCounter += 1

            if currentPlayer.out:
                self.getNextPlayer(currentPlayer)
            if outCounter == 4:
                is_running = False
                print("Game over")
                print("Player 1:", self.player1.score)
                print("Player 2:", self.player2.score)
                print("Player 3:", self.player3.score)
                print("Player 4:", self.player4.score)
                maxScore = max(
                    self.player1.score,
                    self.player2.score,
                    self.player3.score,
                    self.player4.score,
                )
                if self.player1.score == maxScore:
                    print("Player 1 wins", end="")
                elif self.player2.score == maxScore:
                    print("Player 2 wins", end="")
                elif self.player3.score == maxScore:
                    print("Player 3 wins", end="")
                elif self.player4.score == maxScore:
                    print("Player 4 wins", end="")
                print(" With a score of:", maxScore)

                pg.quit()
                sys.exit()

            # elif currentPlayer.playerType == "AI":
            # currentPlayer = self.getRandomMove(currentPlayer, screen)
            mouse_rel = pg.mouse.get_rel()
            if canDrag:
                Piece.drag(currPiece, mouse_rel)
            screen.fill((255, 255, 255, 255))
            screen.blit(self.board, (self.boardStartX, self.boardStartY))
            Player.printPieces(currentPlayer, screen)
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

    def tileWithinBoard(self, row, col):
        return 0 <= row < 20 and 0 <= col < 20

    def pieceWithinBoard(self, piece):
        return (
            piece.x >= self.boardStartX + self.borderSize
            and piece.x + piece.width
            <= self.boardStartX + self.boardSize - self.borderSize
            and piece.y >= self.boardStartY + self.borderSize
            and piece.y + piece.height
            <= self.boardStartY + self.boardSize - self.borderSize
        )

    def isOnSafeCorner(self, player, piece):
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
                    if (
                        rowTile == self.safeCorners[player][0]
                        and colTile == self.safeCorners[player][1]
                    ):
                        return True
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart
        return False

    def checkValidityTurn1(self, player, piece):
        return self.isOnSafeCorner(player, piece)

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
                        self.tileWithinBoard(rowTile, colTile)
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
                        self.tileWithinBoard(rowTile, colTile)
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
                        self.tileWithinBoard(rowTile, colTile)
                        and self.boardArray[rowTile][colTile] == player.color
                    ):
                        isValid = True
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart
        # if not isValid:
        #     print("No piece in range")
        return isValid

    def commitToBoard(self, player, piece, screen):
        # merges board image with piece image
        newBoard = pg.Surface((self.boardSize, self.boardSize))
        newBoard.blit(self.board, (0, 0))
        newBoard.blit(
            piece.image, (piece.x - self.boardStartX, piece.y - self.boardStartY)
        )
        self.board = newBoard
        Player.removeAllPiece(player, piece)
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
                if tile == "p" and self.tileWithinBoard(rowTile, colTile):
                    self.boardArray[rowTile][colTile] = player.color
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart
        rowTile = rowTileArrStart
        colTile = colTileArrStart
        for row in piece.array:
            for tile in row:
                if (
                    tile == "y"
                    and self.tileWithinBoard(rowTile, colTile)
                    and self.boardArray[rowTile][colTile] == self.tileColor
                    and not ((rowTile, colTile) in player.placements)
                ):
                    player.placements[(rowTile, colTile)] = []
                    self.initialPlacement(player, rowTile, colTile, screen)
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart
        # check for new placements, add to player placement list
        # update necessary placements

    def getNextPlayer(self, player):
        return self.nextPlayer[player]

    def initialPlacement(self, player, rowTile, colTile, screen):
        initialPieceX = self.boardStartX + self.borderSize + colTile * self.tileOffset
        initialPieceY = self.boardStartY + self.borderSize + rowTile * self.tileOffset
        initialTile = [1, 1]
        # pieces = copy.deepcopy(player.pieces)
        for piece in player.pieces:
            putBackX = piece.x
            putBackY = piece.y
            for _ in range(4):
                piece.x = initialPieceX
                piece.y = initialPieceY
                initialTile = [1, 1]
                for _ in range(piece.sizeInTiles[0]):
                    for _ in range(piece.sizeInTiles[1]):
                        # screen.fill((255, 255, 255))
                        # screen.blit(self.board, (self.boardStartX, self.boardStartY))
                        # Player.printPieces(player, screen)
                        # pg.display.flip()
                        # time.sleep(0.05)
                        if (
                            self.pieceWithinBoard(piece)
                            and piece.array[initialTile[0]][initialTile[1]] == "p"
                            and (
                                self.checkValidity(player, piece)
                                if player.played
                                else self.checkValidityTurn1(player, piece)
                            )
                        ):
                            player.placements[(rowTile, colTile)].append(
                                copy.deepcopy(piece)
                            )
                        piece.x -= self.tileOffset
                        initialTile[1] += 1
                    piece.y -= self.tileOffset
                    piece.x = initialPieceX
                    initialTile[0] += 1
                    initialTile[1] = 1
                piece.rotateCW()
                piece.flipOverX()
            piece.x = putBackX
            piece.y = putBackY

    def updatePlacements(self):
        emptyPlacements = []
        player = self.player1
        for _ in range(4):
            emptyPlacements = []
            for placement in player.placements:
                for piece in reversed(player.placements[placement]):
                    if not (
                        self.checkValidity(player, piece)
                        if player.played
                        else self.checkValidityTurn1(player, piece)
                    ):
                        player.placements[placement].remove(piece)
                if len(player.placements[placement]) == 0:
                    emptyPlacements.append(placement)
            for p in emptyPlacements:
                player.placements.pop(p)
            player = self.getNextPlayer(player)

    def offloadPlayer(self, player):
        self.nextPlayer[player] = self.nextPlayer[player]
