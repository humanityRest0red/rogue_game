from domain.entities import Player, Enemy


class Game:
    def __init__(self, player, dungeon):
        self.player = player
        self.dungeon = dungeon
        # self.state = None

    def move_player(self, direction):
        i = self.player.current_room
        if direction == 'up' and self.player.position.y - 1 > self.dungeon.rooms[i].top:
            self.player.position.y -= 1
        elif direction == 'down' and self.player.position.y + 1 < self.dungeon.rooms[i].bottom:
            self.player.position.y += 1
        elif direction == 'left' and self.player.position.x - 1 > self.dungeon.rooms[i].left:
            self.player.position.x -= 1
        elif direction == 'right' and self.player.position.x + 1 < self.dungeon.rooms[i].right:
            self.player.position.x += 1

    def attack(self):
        pass

    # def spawn_enemy(self):
    #     self.enemies.append(Enemy())
