from enum import Enum


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    # def mid_y(self, other):
        # return Point(self.x, abs(self.y - other.y) // 2))


class Player:
    def __init__(self, name, current_room=0, position=Point(5, 5)):
        self.name = name
        self.position = position
        self.current_room = current_room
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


class Room:
    def __init__(self, left=0, top=0, w=10, h=3):
        self.left = left
        self.top = top
        self.right = left + w
        self.bottom = top + h

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
        self.rooms = []
        self.tunnels = []
        self.map_grid = [[CellType.EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

        self.h_rooms_count = 3
        self.w_rooms_count = 3
        self.add_rooms()
        self.add_tunnels()

    def add_rooms(self):
        random.seed(time.time())
        top_border = random.randint(0, 3) # todo 5
        for i in range(self.h_rooms_count):
            left_border = random.randint(0, 3) # todo 5
            max_h = 0
            for j in range(self.w_rooms_count):
                w = random.randint(ROOM_MIN_WIDTH, ROOM_MAX_WIDTH)
                h = random.randint(ROOM_MIN_HEIGHT, ROOM_MAX_HEIGHT)
                self.add_room(Room(left=left_border, top=top_border, w=w, h=h))

                left_border += random.randint(w + 4, w + 8)
                max_h = max(max_h, h)
            top_border += random.randint(max_h + 4, max_h + 6)

    def add_room(self, room: Room):
        self.rooms.append(room)
        for i in range(room.left, room.right + 1):
            self.map_grid[room.top][i] = CellType.WALL
            self.map_grid[room.bottom][i] = CellType.WALL
        for j in range(room.top, room.bottom + 1):
            self.map_grid[j][room.left] = CellType.WALL
            self.map_grid[j][room.right] = CellType.WALL
        for i in range(room.top + 1, room.bottom):
            for j in range(room.left + 1, room.right):
                self.map_grid[i][j] = CellType.ROOM
        
    def add_tunnels(self):
        for i in range(self.w_rooms_count - 1):
            start = Point(x=self.rooms[i].right, y=random.randint(self.rooms[i].top + 1, self.rooms[i].bottom - 1))
            end = Point(x=self.rooms[i + 1].left, y=random.randint(self.rooms[i + 1].top + 1, self.rooms[i + 1].bottom - 1))
            self.add_tunnel(start, end)

    def add_tunnel(self, start_point: Point, end_point: Point, is_horizontal=True):
        self.tunnels.append((start_point, end_point))
        x1, y1 = start_point.x, start_point.y
        x2, y2 = end_point.x, end_point.y

        x1, x2 = min(x1, x2), max(x1, x2)
        x_mid = (x1 + x2) // 2
        y1, y2 = min(y1, y2), max(y1, y2)
        y_mid = (y1 + y2) // 2
        
        if is_horizontal:
            # Проходим по горизонтали
            for x in range(x1, (x2 + x1) // 2):
                self.map_grid[y1][x] = CellType.FLOOR
            # Проходим по вертикали
            for y in range(y1, y2 + 1):
                self.map_grid[y][x_mid] = CellType.FLOOR
            # Проходим по горизонтали
            for x in range((x2 + x1) // 2, x2 + 1):
                self.map_grid[y2][x] = CellType.FLOOR
        else:
            # Проходим по вертикали
            for y in range(y1, (y1 + y2) // 2):
                self.map_grid[y][x1] = CellType.FLOOR
            # Проходим по горизонтали
            for x in range(x1, x2 + 1):
                self.map_grid[y_mid][x] = CellType.FLOOR
             # Проходим по вертикали
            for y in range(y1, y2 + 1):
                self.map_grid[y][x2] = CellType.FLOOR
        # Обозначаем входы/выходы
        self.map_grid[y1][x1] = CellType.ENTRY
        self.map_grid[y2][x2] = CellType.ENTRY

# class GameState:
#     def __init__(self):
#         pass
