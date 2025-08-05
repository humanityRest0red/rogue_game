from domain.entities import Player, Enemy


class Game:
    def __init__(self, player, dungeon):
        self.player = player
        self.dungeon = dungeon
        # self.state = None

    def move_player(self, direction):
        map_cells = self.dungeon.map_cells
        y = self.player.position.y
        x = self.player.position.x
        if direction == 'up' and map_cells[y - 1][x].is_passable():
            self.player.position.y -= 1
        elif direction == 'down' and map_cells[y + 1][x].is_passable():
            self.player.position.y += 1
        elif direction == 'left' and map_cells[y][x - 1].is_passable():
            self.player.position.x -= 1
        elif direction == 'right' and map_cells[y][x + 1].is_passable():
            self.player.position.x += 1

    def attack(self):
        pass

    # def spawn_enemy(self):
    #     self.enemies.append(Enemy())
