HEIGHT = 22
WIDTH = 80


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Player:
    def __init__(self, name, current_room=0, position=Point(5, 5)):
        self.name = name
        self.position = position
        self.current_room = current_room
        self.max_health = 25
        self.health = self.max_health
        self.agility = 10


class Enemy:
    def __init__(self, type_, health, agility, strength, hostility):
        self.position = Point()
        self.type = type_
        self.health = health
        self.agility = agility
        self.strength = strength
        self.hostility = hostility


class Zombie(Enemy):
    def __init__(self):
        super().__init__(type_='Zombie', health=50, agility=10, strength=15, hostility=0)


class Room:
    def __init__(self, left=0, top=0, right=10, bottom=8):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top


EMPTY = 0
WALL = 1
FLOOR = 2

class Dungeon:
    def __init__(self, level=1):
        self.level = level
        self.rooms = []
        self.corridors = []
        self.map_grid = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def add_room(self, room: Room):
        self.rooms.append(room)
        for i in range(room.left, room.right + 1):
            self.map_grid[room.top][i] = WALL
            self.map_grid[room.bottom][i] = WALL
        for j in range(room.top, room.bottom + 1):
            self.map_grid[j][room.left] = WALL
            self.map_grid[j][room.right] = WALL

    def add_corridor(self, start_point: Point, end_point: Point):
        self.corridors.append((start_point, end_point))
        # Прорисовка коридора на карте (например, линией по горизонтали и вертикали)
        x1, y1 = start_point.x, start_point.y
        x2, y2 = end_point.x, end_point.y

        # Пример простого "манхэттенского" пути:
        # сначала по горизонтали
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map_grid[y1][x] = FLOOR
        # затем по вертикали
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map_grid[y][x2] = FLOOR
        

# class GameState:
#     def __init__(self):
#         self.player = Player("Hero")
