from presentation.ui import GameUI
from presentation.controllers import GameController
from domain.game_logic import Game
from domain.entities import Player, Dungeon, Enemy, Room, Point


def main():
    # enemies: Enemy = []
    dungeon = Dungeon()
    dungeon.add_room(Room(left=5, right=15, top=2, bottom=5))
    dungeon.add_room(Room(left=35, right=55, top=1, bottom=5))
    dungeon.add_room(Room(left=63, right=78, top=0, bottom=4))
    dungeon.add_room(Room(left=20, right=40, top=8, bottom=12))
    dungeon.add_room(Room(left=55, right=62, top=8, bottom=12))
    # dungeon.add_room(Room(left=20, right=40, top=10, bottom=16))
    game = Game(Player("Ruslan", position=Point(6,4)), dungeon)
    controller = GameController(game)
    ui = GameUI(controller)

    ui.run()


if __name__ == "__main__":
    main()
