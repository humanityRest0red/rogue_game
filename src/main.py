from presentation.ui import GameUI
from presentation.controllers import GameController
from domain.game_logic import Game
from domain.entities import Player, Dungeon, Enemy, Point


def main():
    game = Game(Player("Ruslan", position=Point(6,4)), Dungeon())
    controller = GameController(game)
    ui = GameUI(controller)

    ui.run()


if __name__ == "__main__":
    main()
