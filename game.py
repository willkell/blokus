from player import Player
from piece import Piece
import pygame as pg
import sys

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
        self.borderSize= 10
        self.tileSize = 0
        self.tileOffset = 0
        self.board = pg.Surface((0, 0))

    def run(self):
        pg.init()
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.set_up_screen(pg.display.get_surface().get_size()[0], pg.display.get_surface().get_size()[1])
        self.board = self.draw_board()
        clock = pg.time.Clock()
        is_running = True
        Player.initPieces(self.player1, self.tileOffset, self.tileSize, (255, 2, 100)) 
        Player.initInventory(self.player1, self.inventoryStartX, self.inventoryStartY, self.tileOffset)
        canDrag = False
        dropped = False
        currPiece = None

        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
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
                        Player.initInventory(self.player1, self.inventoryStartX, self.inventoryStartY, self.tileOffset)
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
        for row in range (20):
            for col in range(20):
                pg.draw.rect(board, (200, 200, 200), pg.Rect(self.borderSize + (col * self.tileOffset), self.borderSize + (row * self.tileOffset), self.tileSize, self.tileSize))
        return board
    def set_up_screen(self, height, width):
        self.screenHeight = width
        self.screenWidth = height
        self.boardSize = self.screenHeight * 0.8
        self.boardStartX = self.screenHeight * 0.05
        self.boardStartY = self.screenHeight * 0.1
        self.inventoryStartX = self.boardStartX + self.boardSize + self.boardStartX
        self.inventoryStartY = self.boardStartY
        self.tileSize = (self.boardSize - (self.borderSize* 2) - 19) / 20
        self.tileOffset = (self.boardSize - (self.borderSize* 2)) / 20
    def dropPiece(self,piece):
        # returns false if piece is not on board
        if piece.x < self.boardStartX or piece.x > self.boardStartX + self.boardSize or piece.y < self.boardStartY or piece.y > self.boardStartY + self.boardSize:
            return False
        # snaps to grid
        tileStartX = self.boardStartX + self.borderSize
        tileStartY = self.boardStartY + self.borderSize
        if (piece.x - tileStartX) % self.tileOffset > self.tileOffset / 2:
            piece.x = piece.x + self.tileOffset - (piece.x - tileStartX) % self.tileOffset
        else:
            piece.x = piece.x - ((piece.x - tileStartX) % self.tileOffset)
        if (piece.y - tileStartY) % self.tileOffset > self.tileOffset / 2:
            piece.y = piece.y + self.tileOffset - (piece.y - tileStartY) % self.tileOffset
        else:
            piece.y = piece.y - ((piece.y - tileStartY) % self.tileOffset)
        return True
    def commitToBoard(self, player, piece):
        # merges board with piece image
        newBoard = pg.Surface((self.boardSize, self.boardSize))
        newBoard.blit(self.board, (0, 0))
        newBoard.blit(piece.image, (piece.x - self.boardStartX, piece.y - self.boardStartY))
        self.board = newBoard
        Player.removePiece(player, piece)


        

