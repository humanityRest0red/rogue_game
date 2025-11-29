from collections import deque
from random import choices

from domain.setting import ENEMY_HEALTH_MIN, ENEMY_HEALTH_MAX, ENEMY_AGILITY_MIN, \
    ENEMY_AGILITY_MAX, ENEMY_STRENGTH_MIN, ENEMY_STRENGTH_MAX, ENEMY_HOSTILITY_MIN, \
    ENEMY_HOSTILITY_MAX


class Enemy:
    @staticmethod
    def define_stats(min_, max_):
        return {
            'LOW': min_,
            'MID': (2 * (min_ + max_)) // 3 - min_,
            'HIGH': (2 * (min_ + max_) * 2) // 3 - max_,
            'MAX': max_
        }

    health = define_stats(ENEMY_HEALTH_MIN, ENEMY_HEALTH_MAX)
    agility = define_stats(ENEMY_AGILITY_MIN, ENEMY_AGILITY_MAX)
    strength = define_stats(ENEMY_STRENGTH_MIN, ENEMY_STRENGTH_MAX)
    hostility = define_stats(ENEMY_HOSTILITY_MIN, ENEMY_HOSTILITY_MAX)

    def __init__(self, x, y, name, current_room_id, health, agility, strength, hostility, experience):
        self.x: int = x
        self.y: int = y
        self.name: str = name
        self.current_room_id: int = current_room_id

        self.health: int = health
        self.agility: int = agility
        self.strength: int = strength
        self.hostility: int = hostility
        self.experience: int = experience

        self.direction: str = 'left'

    def make_action(self, map_grid, player, room):
        if self.is_close_by(player):
            self.attack(player)
        else:
            self.move(map_grid, player, room)

    def is_close_by(self, player):
        return (self.y == player.y and abs(self.x - player.x) == 1) or \
               (self.x == player.x and abs(self.y - player.y) == 1)

    def attack(self, player):
        damage_array = [0, self.strength // 2, self.strength]
        if self.agility > player.agility:
            weights = [1, 2, 3]
        elif self.agility < player.agility:
            weights = [3, 2, 1]
        else:
            weights = [1, 1, 1]

        damage = choices(damage_array, weights=weights, k=1)[0]
        player.health -= damage

        i = damage_array.index(damage)

        return damage, i

    def move(self, map_grid, player, room):
        path = self.find_shortest_path(map_grid, player)
        if not path is None and len(path) <= self.hostility:
            self.chase_player(path[0])
        else:
            self.pattern_move(room)

    def chase_player(self, next_cell):
        self.x, self.y = next_cell

    def find_shortest_path(self, map_grid, target):
        rows = len(map_grid)
        cols = len(map_grid[0])
        visited = [[False] * cols for _ in range(rows)]
        parent = [[None] * cols for _ in range(rows)]

        # Очередь для BFS: хранит кортежи (x, y)
        queue = deque()
        queue.append((self.x, self.y))
        visited[self.y][self.x] = True

        # Направления: вверх, вниз, влево, вправо
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.popleft()
            if x == target.x and y == target.y:
                # Вышли к цели — восстанавливаем путь
                path = []
                while (x, y) != (self.x, self.y):
                    path.append((x, y))
                    x, y = parent[y][x]
                path.reverse()
                return path  # список клеток от начальной до цели

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows:
                    if not visited[ny][nx] and map_grid[ny][nx].is_passable():
                        visited[ny][nx] = True
                        parent[ny][nx] = (x, y)
                        queue.append((nx, ny))

        return None  # путь не найден

    def pattern_move(self, room, step=1) -> None:
        if self.direction == 'right':
            if self.x + step <= room.x_:
                self.x += step
            else:
                self.direction = 'left'
                self.x -= step
        else:
            if self.x - step >= room.x:
                self.x -= step
            else:
                self.direction = 'right'
                self.x += step

    def update_difficulty(self, difficulty) -> None:
        self.agility = int(self.agility * difficulty)
        self.strength = int(self.strength * difficulty)
        # self.hostility=int(self.hostility * difficulty)
        self.health = int(self.health * difficulty)
