import copy
import math
import os
import random
import sys
import time
from multiprocessing import Process
from threading import Thread

import pygame as pg

from piece import Piece
from player import Player


class Game:
    def __init__(self):
        self.player1 = Player(1, "Random")
        self.player2 = Player(2, "Random")
        self.player3 = Player(3, "Random")
        self.player4 = Player(4, "Random")
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
            for _ in range(20):
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

    def getRandomMove(self, currentPlayer, screen):
        currentPlayer.played = True
        placement = random.choice(list(currentPlayer.placements.keys()))
        piece = copy.deepcopy(random.choice(currentPlayer.placements[placement].pieces))
        currentPlayer.placements.pop(placement)
        currentPlayer.pieces.append(piece)
        currentPlayer.score += piece.numTiles
        self.commitToBoard(currentPlayer, piece, screen)
        self.updatePlacements(piece)
        # time.sleep(0.9)
        currentPlayer = self.getNextPlayer(currentPlayer)
        Player.initInventory(
            currentPlayer,
            self.inventoryStartX,
            self.inventoryStartY,
            self.tileOffset,
        )
        return currentPlayer

    def distToCorner(self, player, x):
        return math.sqrt(
            math.pow(x[0] - self.safeCorners[player][0], 2)
            + math.pow(x[1] - self.safeCorners[player][1], 2)
        )

    def distToCenter(self, player, x):
        return math.sqrt(math.pow(x[0] - 10, 2) + math.pow(x[1] - 10, 2))

    def getGreedyMove(self, player, screen):
        player.played = True
        listPlacements = list(player.placements.items())
        maxPlacementsStopped = 0
        bestPlacement = random.choice(list(player.placements.keys()))
        bestPieces = [random.choice(player.placements[bestPlacement].pieces)]
        for place in listPlacements:
            for piece in place[1].pieces:
                if piece.placementsBlocked > maxPlacementsStopped:
                    maxPlacementsStopped = piece.placementsBlocked
                    bestPlacement = place[0]
                    bestPieces = [piece]
                elif piece.placementsBlocked == maxPlacementsStopped:
                    bestPieces.append(piece)

        piece = random.choice(bestPieces)
        player.placements.pop(bestPlacement)
        player.pieces.append(piece)
        player.score += piece.numTiles
        self.commitToBoard(player, piece, screen)
        self.updatePlacements(piece)
        # time.sleep(0.9)
        player = self.getNextPlayer(player)
        Player.initInventory(
            player,
            self.inventoryStartX,
            self.inventoryStartY,
            self.tileOffset,
        )
        return player

    def updateScreen(self, screen, currentPlayer, clock):
        screen.fill((255, 255, 255, 255))
        screen.blit(self.board, (self.boardStartX, self.boardStartY))
        if currentPlayer.playerType == "Human":
            Player.printPieces(currentPlayer, screen)
        pg.display.flip()
        clock.tick(144)

    def getHumanMove(
        self, currentPlayer, screen, clock, startTime
    ):
        canDrag = False
        dropped = False
        currPiece = None
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
                ):
                    self.gameOver(startTime)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    canDrag, currPiece = Player.checkForDrag(currentPlayer, event.pos)
                elif event.type == pg.MOUSEBUTTONUP:
                    if canDrag:
                        dropped = self.dropPiece(currPiece)
                    canDrag = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                    currentPlayer = self.getNextPlayer(currentPlayer)
                    Player.initInventory(
                        currentPlayer,
                        self.inventoryStartX,
                        self.inventoryStartY,
                        self.tileOffset,
                    )
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    if (
                        dropped
                        and currPiece
                        and (
                            self.checkValidity(currentPlayer, currPiece)
                            if currentPlayer.played
                            else self.checkValidityTurn1(currentPlayer, currPiece)
                        )
                    ):
                        currentPlayer.played = True
                        currentPlayer.pieces.append(currPiece)
                        self.commitToBoard(currentPlayer, currPiece, screen)
                        self.updatePlacements(currPiece)
                        currentPlayer.score += currPiece.numTiles
                        Player.removeAllPiece(currentPlayer, currPiece)
                        dropped = False
                        currPiece = None
                        currentPlayer = self.getNextPlayer(currentPlayer)
                        Player.initInventory(
                            currentPlayer,
                            self.inventoryStartX,
                            self.inventoryStartY,
                            self.tileOffset,
                        )
                        return currentPlayer
                    else:
                        Player.initInventory(
                            currentPlayer,
                            self.inventoryStartX,
                            self.inventoryStartY,
                            self.tileOffset,
                        )

                elif event.type == pg.KEYDOWN and currPiece:
                    if event.key == pg.K_RIGHT or event.key == pg.K_f:
                        Piece.rotateCCW(currPiece)
                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        Piece.rotateCW(currPiece)
                    if event.key == pg.K_UP or event.key == pg.K_d:
                        Piece.flipOverX(currPiece)
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        Piece.flipOverY(currPiece)
                    if event.key == pg.K_SPACE:
                        currentPlayer = self.getRandomMove(currentPlayer, screen)
                        return currentPlayer

            mouse_rel = pg.mouse.get_rel()
            if canDrag and currPiece:
                Piece.drag(currPiece, mouse_rel)
            self.updateScreen(screen, currentPlayer, clock)

    def run(self):
        startTime = time.time()
        pg.init()
        screen = pg.display.set_mode((1200, 700))
        self.set_up_screen(
            pg.display.get_surface().get_size()[0],
            pg.display.get_surface().get_size()[1],
        )
        self.board = self.draw_board()
        clock = pg.time.Clock()
        self.initPlayers(screen)
        currentPlayer = self.player1
        outCounter = 0

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
                ):
                    self.gameOver(startTime)

            if not currentPlayer.placements and not currentPlayer.out:
                currentPlayer.out = True
                outCounter += 1

            if outCounter == 4:
                self.gameOver(startTime)

            if currentPlayer.out:
                currentPlayer = self.getNextPlayer(currentPlayer)

            elif currentPlayer.playerType == "Random":
                currentPlayer = self.getRandomMove(currentPlayer, screen)

            elif currentPlayer.playerType == "Greedy":
                currentPlayer = self.getGreedyMove(currentPlayer, screen)

            elif currentPlayer.playerType == "Human":
                currentPlayer = self.getHumanMove(
                    currentPlayer, screen, clock, startTime
                )
            self.updateScreen(screen, currentPlayer, clock)

    def initPlayers(self, screen):
        self.player1.color = (255, 0, 0)
        self.player2.color = (0, 255, 0)
        self.player3.color = (0, 0, 255)
        self.player4.color = (255, 255, 0)
        for player in [self.player1, self.player2, self.player3, self.player4]:
            Player.initPieces(player, self.tileOffset, self.tileSize, player.color)
            Player.initInventory(
                player, self.inventoryStartX, self.inventoryStartY, self.tileOffset
            )
            self.setUpPieceDeck(player, screen)
        self.player1.placements[(0, 0)] = Player.Placement("lowerRight")
        self.initialPlacement(self.player1, 0, 0, screen, "lowerRight")
        self.player2.placements[(0, 19)] = Player.Placement("lowerLeft")
        self.initialPlacement(self.player2, 0, 19, screen, "lowerLeft")
        self.player3.placements[(19, 19)] = Player.Placement("upperLeft")
        self.initialPlacement(self.player3, 19, 19, screen, "upperLeft")
        self.player4.placements[(19, 0)] = Player.Placement("upperRight")
        self.initialPlacement(self.player4, 19, 0, screen, "upperRight")
        Player.initInventory(
            self.player1, self.inventoryStartX, self.inventoryStartY, self.tileOffset
        )

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

    def gameOver(self, startTime):
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
        print("--- %s seconds ---" % (time.time() - startTime))

        pg.quit()
        sys.exit()

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

    def tileWithinBoard(self, row: int, col: int) -> bool:
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
            ((piece.y - self.boardStartY - self.borderSize) / self.tileOffset)
        )
        colTileArrStart = round(
            ((piece.x - self.boardStartX - self.borderSize) / self.tileOffset)
        )
        rowTile = rowTileArrStart
        colTile = colTileArrStart
        for row in piece.array[1:-1]:
            for tile in row[1:-1]:
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
                if self.tileWithinBoard(rowTile, colTile):
                    if (
                        tile == "p"
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
                    if self.boardArray[rowTile][colTile] == player.color:
                        if tile == "n":
                            # print(
                            #     self.validFailureMsg(
                            #         rowTile, colTile, "not same color", "same color"
                            #     )
                            # )
                            return False
                        elif tile == "y":
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
        rowTile = rowTileArrStart + 1
        colTile = colTileArrStart + 1
        for row in piece.array[1:-1]:
            for tile in row[1:-1]:
                if tile == "p":
                    if self.boardArray[rowTile][colTile] != self.tileColor:
                        print("Error: tile already full")
                    self.boardArray[rowTile][colTile] = player.color
                    if (rowTile, colTile) in self.player1.placements:
                        self.player1.placements.pop((rowTile, colTile))
                    if (rowTile, colTile) in self.player2.placements:
                        self.player2.placements.pop((rowTile, colTile))
                    if (rowTile, colTile) in self.player3.placements:
                        self.player3.placements.pop((rowTile, colTile))
                    if (rowTile, colTile) in self.player4.placements:
                        self.player4.placements.pop((rowTile, colTile))
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart + 1
        # screen.blit(piece.image, (piece.x, piece.y))
        # pg.display.flip()
        rowTile = rowTileArrStart
        colTile = colTileArrStart
        for row in piece.array:
            for tile in row:
                if (
                    tile == "y"
                    and self.tileWithinBoard(rowTile, colTile)
                    and self.validForPlayer(player, rowTile, colTile)
                    and not ((rowTile, colTile) in player.placements)
                ):
                    player.placements[(rowTile, colTile)] = Player.Placement(
                        self.getPlacementType(player, rowTile, colTile),
                        self.getPlacementSpace(player, rowTile, colTile),
                    )
                    self.initialPlacement(
                        player,
                        rowTile,
                        colTile,
                        screen,
                        self.getPlacementType(player, rowTile, colTile),
                    )
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart

    def getNextPlayer(self, player):
        return self.nextPlayer[player]

    def getPieceDeck(self, player, rowTile, colTile, screen):
        pieceDeck = []
        initialPieceX = self.boardStartX + self.borderSize + colTile * self.tileOffset
        initialPieceY = self.boardStartY + self.borderSize + rowTile * self.tileOffset
        initialTile = [1, 1]
        # pieces = copy.deepcopy(player.pieces)
        for piece in player.pieces:
            for _ in range(2):
                for _ in range(4):
                    piece.x = initialPieceX
                    piece.y = initialPieceY
                    initialTile = [1, 1]
                    for _ in range(piece.sizeInTiles[0]):
                        for _ in range(piece.sizeInTiles[1]):
                            # screen.fill((255, 255, 255))
                            # screen.blit(self.board, (self.boardStartX, self.boardStartY))
                            # Player.printPieces(player, screen)
                            # screen.blit(piece.image, (piece.x, piece.y))
                            # pg.display.flip()
                            # time.sleep(0.05)
                            if (
                                self.pieceWithinBoard(piece)
                                and piece.array[initialTile[0]][initialTile[1]] == "p"
                                and self.checkValidity(player, piece)
                            ):
                                pieceDeck.append(copy.deepcopy(piece))
                            piece.x -= self.tileOffset
                            initialTile[1] += 1
                        piece.y -= self.tileOffset
                        piece.x = initialPieceX
                        initialTile[0] += 1
                        initialTile[1] = 1
                    if piece.symmetryRotate:
                        break
                    piece.rotateCW()
                if not piece.symmetryY:
                    piece.flipOverY()
                elif not piece.symmetryX:
                    piece.flipOverX()
                else:
                    break
        return pieceDeck

    def initialPlacement(
        self,
        player,
        rowTile,
        colTile,
        screen,
        placementPos,
    ):
        pieceDeck = player.deck[placementPos]
        for piece in pieceDeck:
            piece.x, piece.y = self.tilePos(rowTile, colTile)
            if placementPos == "lowerLeft" or placementPos == "upperLeft":
                piece.x -= self.tileOffset * (piece.sizeInTiles[1] - 1)
            if placementPos == "upperLeft" or placementPos == "upperRight":
                piece.y -= self.tileOffset * (piece.sizeInTiles[0] - 1)

            if self.pieceWithinBoard(piece) and (
                self.checkValidity(player, piece)
                if player.played
                else self.checkValidityTurn1(player, piece)
            ):
                # piece.access = self.getPieceAccess(player, piece, screen)
                player.placements[(rowTile, colTile)].append(Piece.insertCopy(piece))

    def updatePlacements(self, piece):
        pieceRowStart = round(
            ((piece.y - self.boardStartY - self.borderSize) / self.tileOffset)
        )
        pieceColStart = round(
            ((piece.x - self.boardStartX - self.borderSize) / self.tileOffset)
        )
        pieceRowEnd = pieceRowStart + piece.sizeInTiles[0]
        pieceColEnd = pieceColStart + piece.sizeInTiles[1]
        # before you are within the piece
        for row in range(pieceRowStart - 5, pieceRowStart):
            for col in range(
                pieceColStart - 5 + (pieceRowStart - row),
                pieceColEnd + 6 - (pieceRowStart - row),
            ):
                if self.tileWithinBoard(row, col):
                    players = self.whosePlacement(row, col)
                    for player in players:
                        self.updatePlacement(
                            pieceRowStart - row - 2,
                            abs(col - pieceColStart) - 2,
                            player,
                            (row, col),
                        )
        # within the piece
        for row in range(pieceRowStart, pieceRowEnd + 1):
            for col in range(pieceColStart - 5, pieceColEnd + 6):
                if self.tileWithinBoard(row, col):
                    players = self.whosePlacement(row, col)
                    for player in players:
                        self.updatePlacement(
                            1, abs(col - pieceColStart) - 2, player, (row, col)
                        )
        # after you are within the piece
        for row in range(pieceRowEnd + 1, pieceRowEnd + 6):
            for col in range(
                pieceColStart - 5 + (row - pieceRowEnd),
                pieceColEnd + 6 - (row - pieceRowEnd),
            ):
                if self.tileWithinBoard(row, col):
                    players = self.whosePlacement(row, col)
                    for player in players:
                        self.updatePlacement(
                            row - pieceRowStart - 2,
                            abs(col - pieceColStart) - 2,
                            player,
                            (row, col),
                        )

        self.getRidOfEmptyPlacements()

    def whosePlacement(self, row, col):
        players = []
        if (row, col) in self.player1.placements:
            players.append(self.player1)
        if (row, col) in self.player2.placements:
            players.append(self.player2)
        if (row, col) in self.player3.placements:
            players.append(self.player3)
        if (row, col) in self.player4.placements:
            players.append(self.player4)
        return players

    def enemyPlacements(self, player, row, col):
        players = [self.player1, self.player2, self.player3, self.player4]
        players.remove(player)
        places = 0
        for player in players:
            if (row, col) in player.placements:
                places += 1
        return places

    def updatePlacement(self, minHeight, minWidth, player, place):
        for piece in reversed(player.placements[place].pieces):
            if (
                piece.sizeInTiles[0] >= minHeight
                and piece.sizeInTiles[1] >= minWidth
                and not (
                    self.checkValidity(player, piece)
                    if player.played
                    else self.checkValidityTurn1(player, piece)
                )
            ):
                player.placements[place].remove(piece)
            # else:
            # piece.access = self.getPieceAccess(player, piece, player)
        # update the space of the placement
        player.placements[place].space = self.getPlacementSpace(
            player, place[0], place[1]
        )
        # if not player.placements[place]:
        #     player.placements.pop(place)

    def getRidOfEmptyPlacements(self):
        for player in [self.player1, self.player2, self.player3, self.player4]:
            emptyPlacements = []
            for place in player.placements:
                if Player.Placement.empty(player.placements[place]):
                    emptyPlacements.append(place)
            for place in emptyPlacements:
                player.placements.pop(place)

    def setUpPieceDeck(self, player, screen):
        self.boardArray[10][10] = player.color
        player.deck["lowerRight"] = self.getPieceDeck(player, 11, 11, screen)
        player.deck["lowerLeft"] = self.getPieceDeck(player, 11, 9, screen)
        player.deck["upperLeft"] = self.getPieceDeck(player, 9, 9, screen)
        player.deck["upperRight"] = self.getPieceDeck(player, 9, 11, screen)
        self.boardArray[10][10] = self.tileColor

    def tilePos(self, row, col):
        return (
            self.boardStartX + self.borderSize + (col * self.tileOffset),
            self.boardStartY + self.borderSize + (row * self.tileOffset),
        )

    def getPlacementType(self, player, row, col):
        if (
            self.tileWithinBoard(row - 1, col - 1)
            and self.boardArray[row - 1][col - 1] == player.color
        ):
            return "lowerRight"
        elif (
            self.tileWithinBoard(row - 1, col + 1)
            and self.boardArray[row - 1][col + 1] == player.color
        ):
            return "lowerLeft"
        elif (
            self.tileWithinBoard(row + 1, col + 1)
            and self.boardArray[row + 1][col + 1] == player.color
        ):
            return "upperLeft"
        elif (
            self.tileWithinBoard(row + 1, col - 1)
            and self.boardArray[row + 1][col - 1] == player.color
        ):
            return "upperRight"
        else:
            print(row, col)
            while True:
                time.sleep(1)
            # return "none"

    def validForPlayer(self, player: Player, row: int, col: int) -> bool:
        return not (
            (
                self.tileWithinBoard(row, col)
                and self.boardArray[row][col] != self.tileColor
            )
            or (
                self.tileWithinBoard(row, col + 1)
                and self.boardArray[row - 1][col] == player.color
            )
            or (
                self.tileWithinBoard(row + 1, col)
                and self.boardArray[row - 1][col] == player.color
            )
            or (
                self.tileWithinBoard(row, col - 1)
                and self.boardArray[row - 1][col] == player.color
            )
            or (
                self.tileWithinBoard(row - 1, col)
                and self.boardArray[row - 1][col] == player.color
            )
        )

    def getPlacementSpace(self, player: Player, row: int, col: int) -> int:
        space = 0
        # check above for how much space
        checkRow = row - 1
        checkCol = col
        while self.tileWithinBoard(checkRow, checkCol) and self.validForPlayer(
            player, checkRow, checkCol
        ):
            space += 1
            checkRow -= 1
        # check to the right
        checkRow = row
        checkCol = col + 1
        while self.tileWithinBoard(checkRow, checkCol) and self.validForPlayer(
            player, checkRow, checkCol
        ):
            space += 1
            checkCol += 1
        # check to the bottom
        checkRow = row + 1
        checkCol = col
        while self.tileWithinBoard(checkRow, checkCol) and self.validForPlayer(
            player, checkRow, checkCol
        ):
            space += 1
            checkRow += 1
        # check to the right
        checkRow = row
        checkCol = col - 1
        while self.tileWithinBoard(checkRow, checkCol) and self.validForPlayer(
            player, checkRow, checkCol
        ):
            space += 1
            checkCol -= 1

        return space

    def mergePieceArr(self, player, piece, screen):
        rowTileArrStart = round(
            (piece.y - self.boardStartY - self.borderSize) / self.tileOffset
        )
        colTileArrStart = round(
            (piece.x - self.boardStartX - self.borderSize) / self.tileOffset
        )
        rowTile = rowTileArrStart
        colTile = colTileArrStart
        for row in piece.array[1:-1]:
            for tile in row[1:-1]:
                if tile == "p":
                    if self.boardArray[rowTile][colTile] != self.tileColor:
                        print(
                            "Error: ",
                            rowTile,
                            colTile,
                            "tile already full, with ",
                            self.boardArray[rowTile][colTile],
                        )
                    self.boardArray[rowTile][colTile] = player.color
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart

    def clearPieceArr(self, player: Player, piece: Piece, screen: pg.Surface):
        rowTileArrStart = round(
            (piece.y - self.boardStartY - self.borderSize) / self.tileOffset
        )
        colTileArrStart = round(
            (piece.x - self.boardStartX - self.borderSize) / self.tileOffset
        )
        rowTile = rowTileArrStart
        colTile = colTileArrStart
        for row in piece.array[1:-1]:
            for tile in row[1:-1]:
                if tile == "p":
                    self.boardArray[rowTile][colTile] = self.tileColor
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart

    def getPieceAccess(self, player, piece, screen):
        access = 0
        piece.placementsBlocked = 0
        self.mergePieceArr(player, piece, screen)
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
                if (
                    tile == "y"
                    and self.tileWithinBoard(rowTile, colTile)
                    and self.validForPlayer(player, rowTile, colTile)
                ):
                    access += self.getPlaceAccess(
                        player,
                        rowTile,
                        colTile,
                        self.getPlacementType(player, rowTile, colTile),
                    )
                elif tile == "p":
                    piece.placementsBlocked += self.enemyPlacements(
                        player, rowTile, colTile
                    )
                colTile += 1
            rowTile += 1
            colTile = colTileArrStart
        self.clearPieceArr(player, piece, screen)
        return access

    def getPlaceAccess(self, player, rowTile, colTile, placementPos) -> int:
        access = 0
        pieceDeck = player.deck[placementPos]
        for piece in pieceDeck:
            putBackX = piece.x
            putBackY = piece.y
            piece.x, piece.y = self.tilePos(rowTile, colTile)
            if placementPos == "lowerLeft" or placementPos == "upperLeft":
                piece.x -= self.tileOffset * (piece.sizeInTiles[1] - 1)
            if placementPos == "upperLeft" or placementPos == "upperRight":
                piece.y -= self.tileOffset * (piece.sizeInTiles[0] - 1)

            if self.pieceWithinBoard(piece) and (self.checkValidity(player, piece)):
                access += piece.numTiles
            piece.x = putBackX
            piece.y = putBackY

        return access

    def printBoard(self):
        for row in self.boardArray:
            for cell in row:
                if cell == self.tileColor:
                    print("n ", end="")
                else:
                    print("y ", end="")
            print("")

        print("\n")
