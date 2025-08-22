from random import randint
from typing import Any

from domain.cell import coordinate, Cell
from domain.map.door import Door

class Corridor:
    def __init__(self, start: coordinate, finish: coordinate, room_id, direction: str = "h"):
    # def __init__(self, start: coordinate, finish: coordinate, direction: str = "h"):
        self.start, self.finish = self.shift_initials(start, finish, direction)
        self.corridor: dict[coordinate, Any] = {}
        self.doors = []

        self.room1 = room_id
        if direction == "h":
            self.room2 = room_id + 1
            side = 'right'
        else:
            self.room2 = room_id + 3
            side = 'bottom'

        self.doors.append(Door(start[0], start[1], self.room1, side))
        self.doors.append(Door(finish[0], finish[1], self.room2, side))
        self.generate_corridor(direction)
        self.is_discovered = False

    @staticmethod
    def shift_initials(start: coordinate, finish: coordinate, direction: str) -> tuple[coordinate, coordinate]:
        y, x = start
        y_, x_ = finish
        if direction == "v":
            if y > y_:
                new_s, new_f = (y - 1, x), (y_ + 1, x_)
            else:
                new_s, new_f = (y + 1, x), (y_ - 1, x_)
        elif direction == "h":
            if x > x_:
                new_s, new_f = (y, x - 1), (y_, x_ + 1)
            else:
                new_s, new_f = (y, x + 1), (y_, x_ - 1)
        else:
            raise ValueError("direction must be 'v' or 'h'")

        return new_s, new_f

    def generate_corridor(self, direction: str):
        y1, x1 = self.start
        y2, x2 = self.finish
        if direction == "v":
            if x1 == x2:
                self.build_vertical_corridor(y1, y2, x1)
            else:
                y_turn = randint(min(y1, y2), max(y1, y2))
                self.build_vertical_corridor(y1, y_turn, x1)
                self.build_horizontal_corridor(x1, x2, y_turn)
                self.build_vertical_corridor(y2, y_turn, x2)
        elif direction == "h":
            if y1 == y2:
                self.build_horizontal_corridor(x1, x2, y1)
            else:
                x_turn = randint(min(x1, x2), max(x1, x2))
                self.build_horizontal_corridor(x1, x_turn, y1)
                self.build_vertical_corridor(y1, y2, x_turn)
                self.build_horizontal_corridor(x2, x_turn, y2)

    def build_vertical_corridor(self, y1: int, y2: int, x: int):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.corridor[y, x] = Cell.floor

    def build_horizontal_corridor(self, x1: int, x2: int, y: int):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.corridor[y, x] = Cell.floor

    def tiles(self) -> dict[coordinate, Any]:
        return self.corridor.copy()

