import copy
import random
import sys
import time

# import numpy as np
import pygame as pg

from piece import Piece
from player import Player



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

    def run(self):
        startTime = time.time()
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
        self.setUpPieceDeck(self.player1, screen)
        self.player1.placements[(0, 0)] = Player.Placement("lowerRight")
        self.initialPlacement(self.player1, 0, 0, screen, "lowerRight")
        self.setUpPieceDeck(self.player2, screen)
        self.player2.placements[(0, 19)] = Player.Placement("lowerLeft")
        self.initialPlacement(self.player2, 0, 19, screen, "lowerLeft")
        self.setUpPieceDeck(self.player3, screen)
        self.player3.placements[(19, 19)] = Player.Placement("upperLeft")
        self.initialPlacement(self.player3, 19, 19, screen, "upperLeft")
        self.setUpPieceDeck(self.player4, screen)
        self.player4.placements[(19, 0)] = Player.Placement("upperRight")
        self.initialPlacement(self.player4, 19, 0, screen, "upperRight")
        Player.initInventory(
            self.player1, self.inventoryStartX, self.inventoryStartY, self.tileOffset
        )
        currentPlayer = self.player1
        canDrag = False
        dropped = False
        currPiece = None
        outCounter = 0

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

            if outCounter == 4:
                # time.sleep(10)
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
                print("--- %s seconds ---" % (time.time() - startTime))

                pg.quit()
                sys.exit()
            if currentPlayer.out:
                currentPlayer = self.getNextPlayer(currentPlayer)

            elif currentPlayer.playerType == "AI":
                currentPlayer = self.getRandomMove(currentPlayer, screen)
            mouse_rel = pg.mouse.get_rel()
            if canDrag:
                Piece.drag(currPiece, mouse_rel)
            screen.fill((255, 255, 255, 255))
            screen.blit(self.board, (self.boardStartX, self.boardStartY))
            if not currentPlayer.playerType == "AI":
                Player.printPieces(currentPlayer, screen)
            pg.display.flip()
            clock.tick(144)

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
                    and self.boardArray[rowTile][colTile] == self.tileColor
                    and not ((rowTile, colTile) in player.placements)
                ):
                    player.placements[(rowTile, colTile)] = Player.Placement(
                        self.getPlacementType(player, rowTile, colTile)
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
                                and piece.array[initialTile[0]][initialTile[1]]
                                == "p"
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
        # if there is a 6x6 space, everything in the deck is valid
        # everythingValid = False
        # for row in range(rowTile, rowTile + 7):
        #     for col in range(colTile, colTile + 7):
        #         if self.boardArray[row][col] != self.tileColor:
        #             everythingValid = False
        #             break
        # if everythingValid:
        #     player.placements[(rowTile, colTile)] = copy.deepcopy(player.pieces)
        #     return
        pieceDeck = player.deck[placementPos]
        for piece in pieceDeck:
            piece.x, piece.y = self.tilePos(rowTile, colTile)
            if (placementPos == "lowerLeft" or placementPos == "upperLeft"):
                piece.x -= self.tileOffset * (piece.sizeInTiles[1] - 1)
            if (placementPos == "upperLeft" or placementPos == "upperRight"):
                piece.y -= self.tileOffset * (piece.sizeInTiles[0] - 1)

            if self.pieceWithinBoard(piece) and (
                self.checkValidity(player, piece)
                if player.played
                else self.checkValidityTurn1(player, piece)
            ):
                player.placements[(rowTile, colTile)].append(Piece.insertCopy(piece))
            # screen.fill((255, 255, 255))
            # screen.blit(self.board, (self.boardStartX, self.boardStartY))
            # # Player.printPieces(player, screen)
            # screen.blit(piece.image, (piece.x, piece.y))
            # pg.display.flip()
            # time.sleep(0.05)

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
