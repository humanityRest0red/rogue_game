import sys

from controller.controllers import GameController


def main():
    mode = "Curses"
    if len(sys.argv) > 1:
        mode = "Pygame"
    controller = GameController(mode)
    controller.run()


if __name__ == "__main__":
    main()
