from player import Player
from piece import Piece
import pygame as pg
import sys

class Game:
    def __init__(self):
        self.player1 = player.Player(1)
        self.player2 = player.Player(2)
        self.player3 = player.Player(3)
        self.player4 = player.Player(4)
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

    def run(self):
        pg.init()
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.set_up_screen(pg.display.get_surface().get_size()[0], pg.display.get_surface().get_size()[1])
        screen.fill((255, 255, 255, 255))
        screen.blit(self.draw_board(), (self.boardStartX, self.boardStartY))
        clock = pg.time.Clock()
        is_running = True
        Player.initPieces(self.player1, self.tileOffset, self.tileSize, (255, 2, 100)) 
        Player.printPieces(self.player1, screen, self.inventoryStartX, self.inventoryStartY, self.tileOffset)

        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    is_running = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    Player.checkAndDrag(self.player1, event.pos)

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

