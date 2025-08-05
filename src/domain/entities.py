from enum import Enum


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    # def mid_y(self, other):
        # return Point(self.x, abs(self.y - other.y) // 2))


class Player:
    def __init__(self, name, current_room_id=0, position=Point(5, 5)):
        self.name = name
        self.position = position
        self.current_room_id = current_room_id
        self.max_health = 25
        self.health = self.max_health
        self.agility = 10
        self.strength = 12

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


class NeighborInfo:
    def __init__(self, index, is_horizontal):
        self.index = index
        self.is_horizontal = is_horizontal

class Room:
    def __init__(self, ind, left=0, top=0, w=10, h=3):
        self.left = left
        self.top = top
        self.right = left + w
        self.bottom = top + h
        self.neighbors = self.get_neighbors(ind)

    def get_neighbors(self, ind) -> list[NeighborInfo]:
        if ind == 0:
            return [NeighborInfo(1, True), NeighborInfo(3, False)]
        elif ind == 6:
            return [NeighborInfo(7, True)]
        elif ind == 8:
            # return [NeighborInfo(7, True), NeighborInfo(5, False)]
            return []
        elif ind == 2:
            return [NeighborInfo(5, False)]

        elif ind == 1:
            return [NeighborInfo(2, True), NeighborInfo(4, False)]
        elif ind == 7:
            return [NeighborInfo(8, True)]
        elif ind == 3:
            return [NeighborInfo(4, True), NeighborInfo(6, False)]
        elif ind == 5:
            return [NeighborInfo(8, False)]
        
        elif ind == 4:
            return [ NeighborInfo(5, True), NeighborInfo(7, False)]

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top


class CellType(Enum):
    EMPTY = 0
    WALL = 1
    FLOOR = 2
    ROOM = 3
    ENTRY = 4

    def is_passable(self):
        return self in {CellType.FLOOR, CellType.ROOM, CellType.ENTRY}


HEIGHT = 30
WIDTH = 80

MAX_ROOMS = 9
ROOM_MIN_WIDTH = 6
ROOM_MAX_WIDTH = 25
ROOM_MIN_HEIGHT = 4
ROOM_MAX_HEIGHT = 6

import random
import time

class Dungeon:
    def __init__(self, level=1):
        self.level = level
        self.room_list = []
        self.tunnels = []
        self.map_cells = [[CellType.EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

        self.rooms_vertical_count = 3
        self.rooms_horizontal_count = 3
        self.generate_rooms()
        self.generate_tunnels()

    def generate_rooms(self):
        random.seed(time.time())
        top_border = random.randint(0, 3) # todo 5
        for i in range(self.rooms_vertical_count):
            left_border = random.randint(0, 3) # todo 5
            max_h = 0
            for j in range(self.rooms_horizontal_count):
                w = random.randint(ROOM_MIN_WIDTH, ROOM_MAX_WIDTH)
                h = random.randint(ROOM_MIN_HEIGHT, ROOM_MAX_HEIGHT)
                self.place_room(Room(left=left_border, top=top_border, w=w, h=h, ind=i*3+j))

                left_border += random.randint(w + 4, w + 8)
                max_h = max(max_h, h)
            top_border += random.randint(max_h + 4, max_h + 6)

    def place_room(self, room: Room):
        self.room_list.append(room)
        for i in range(room.left, room.right + 1):
            self.map_cells[room.top][i] = CellType.WALL
            self.map_cells[room.bottom][i] = CellType.WALL
        for j in range(room.top, room.bottom + 1):
            self.map_cells[j][room.left] = CellType.WALL
            self.map_cells[j][room.right] = CellType.WALL
        for i in range(room.top + 1, room.bottom):
            for j in range(room.left + 1, room.right):
                self.map_cells[i][j] = CellType.ROOM
        
    def generate_tunnels(self):
        for room in (self.room_list):
            for neighbor in room.neighbors:
                self.add_tunnel(room, self.room_list[neighbor.index], neighbor.is_horizontal)

    def add_tunnel(self, room1, room2, is_horizontal):
        if is_horizontal: 
            start = Point(x=room1.right, y=random.randint(room1.top + 1, room1.bottom - 1))
            end = Point(x=room2.left, y=random.randint(room2.top + 1, room2.bottom - 1))
        else:
            start = Point(x=random.randint(room1.left + 1, room1.right - 1), y=room1.bottom)
            end = Point(x=random.randint(room2.left + 1, room2.right - 1), y=room2.top)
        
        x1, y1 = start.x, start.y
        x2, y2 = end.x, end.y

        x_mid = (x1 + x2) // 2
        y_mid = (y1 + y2) // 2
        
        if is_horizontal:
            # Проходим по горизонтали
            for x in range(x1, x_mid):
                self.map_cells[y1][x] = CellType.FLOOR
            # Проходим по вертикали
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.map_cells[y][x_mid] = CellType.FLOOR
            # Проходим по горизонтали
            for x in range(x_mid, x2 + 1):
                self.map_cells[y2][x] = CellType.FLOOR
        else:
            # Проходим по вертикали
            for y in range(y1, y_mid):
                self.map_cells[y][x1] = CellType.FLOOR
            # Проходим по горизонтали
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.map_cells[y_mid][x] = CellType.FLOOR
             # Проходим по вертикали
            for y in range(y_mid, y2 + 1):
                self.map_cells[y][x2] = CellType.FLOOR
        # Обозначаем входы/выходы
        self.map_cells[y1][x1] = CellType.ENTRY
        self.map_cells[y2][x2] = CellType.ENTRY

# class GameState:
#     def __init__(self):
#         pass
