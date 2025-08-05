from domain.entities import Player, Enemy


class Game:
    def __init__(self, player, dungeon):
        self.player = player
        self.dungeon = dungeon
        # self.state = None

    def move_player(self, direction):
        i = self.player.current_room
        map_grid = self.dungeon.map_grid
        y = self.player.position.y
        x = self.player.position.x
        if direction == 'up' and map_grid[y - 1][x].is_passable():
            self.player.position.y -= 1
        elif direction == 'down' and map_grid[y + 1][x].is_passable():
            self.player.position.y += 1
        elif direction == 'left' and map_grid[y][x - 1].is_passable():
            self.player.position.x -= 1
        elif direction == 'right' and map_grid[y][x + 1].is_passable():
            self.player.position.x += 1

    def attack(self):
        pass

    # def spawn_enemy(self):
    #     self.enemies.append(Enemy())
