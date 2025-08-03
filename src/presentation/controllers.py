from domain.game_logic import Game


class GameController:
    def __init__(self, game: Game):
        self.game = game

    def move_player(self, direction):
        self.game.move_player(direction)
        # Можно обновлять состояние UI или логировать действия
