import game
import time


def main():
    start_time = time.time()
    mygame = game.Game()
    mygame.run()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
