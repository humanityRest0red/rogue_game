from domain.entities import Player, Enemy


class Game:
    def __init__(self, player, map_):
        self.player = player
        self.map = map_
        # self.state = None

    def move_player(self, direction):
        if direction == 'up' and self.player.position.y - 1 > self.map.up_board:
            self.player.position.y -= 1
        elif direction == 'down' and self.player.position.y + 1 < self.map.down_board:
            self.player.position.y += 1
        elif direction == 'left' and self.player.position.x - 1 > self.map.left_board:
            self.player.position.x -= 1
        elif direction == 'right' and self.player.position.x + 1 < self.map.right_board:
            self.player.position.x += 1

    def attack(self):
        pass

    # def spawn_enemy(self):
    #     self.enemies.append(Enemy())
