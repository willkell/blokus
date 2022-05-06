import player
import piece
import pygame as pg
import sys

class Game:
    def __init__(self):
        self.player1 = player.Player(1)
        self.player2 = player.Player(2)
        self.player3 = player.Player(3)
        self.player4 = player.Player(4)
        self.screenHeight = 1100
        self.screenWidth = self.screenHeight * 2
        self.boardSize = self.screenHeight * 0.8
        self.boardStartX = self.screenHeight * 0.1
        self.boardStartY = self.screenHeight * 0.1
        self.borderSize= 10
        self.tileSize = (self.boardSize - (self.borderSize* 2) - 19) / 20
        self.tileOffset = (self.boardSize - (self.borderSize* 2)) / 20

    def run(self):
        pg.init()
        screen = pg.display.set_mode((self.screenWidth, self.screenHeight))
        screen.fill((255, 255, 255, 255))
        screen.blit(self.draw_board(), (self.boardStartX, self.boardStartY))
        clock = pg.time.Clock()
        is_running = True
        player.Player.initPieces(self.player1, self.tileOffset, self.tileSize, (255, 0, 0)) 
        player.Player.printPieces(self.player1, screen)

        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    is_running = False
                    pg.quit()
                    sys.exit()

            pg.display.flip()
            clock.tick(60)
        

    def draw_board(self):
        board = pg.Surface((self.boardSize, self.boardSize))
        board.fill((100, 100, 100))
        for row in range (20):
            for col in range(20):
                pg.draw.rect(board, (200, 200, 200), pg.Rect(self.borderSize + (col * self.tileOffset), self.borderSize + (row * self.tileOffset), self.tileSize, self.tileSize))
        return board
