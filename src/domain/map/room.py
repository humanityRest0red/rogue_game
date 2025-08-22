from random import randint, sample
from typing import Any

from domain.setting import (HEIGHT_MIN_ROOM, WIDTH_MIN_ROOM, ROOM_INDENT)
from domain.cell import coordinate
from domain.cell import Cell
from domain.map.door import Door

class Room:
    # door_side = {
    #     0: ["bottom", "right"],
    #     1: ["left", "bottom", "right"],
    #     2: ["left", "bottom"],
    #     3: ["top", "bottom", "right"],
    #     4: ["left", "top", "bottom", "right"],
    #     5: ["left", "top", "bottom"],
    #     6: ["top", "right"],
    #     7: ["left","top", "right"],
    #     8: ["left", "top"]
    # }

    door_side = {
        0: ["bottom", "right"],
        1: ["bottom", "right"],
        2: ["bottom"],
        3: ["bottom", "right"],
        4: ["bottom", "right"],
        5: ["bottom"],
        6: ["right"],
        7: ["right"],
        8: []
    }

    def __init__(self, start_x: int, start_y: int, height: int, width: int, id: int):
        self.id = id
        self.x, self.y, self.x_, self.y_ = self.generate_room(start_x, start_y, height, width)
        self.is_discovered = False
        self.is_foged = True
        self.sides = self.door_side[self.id].copy()
        self.doors_coordinates = set()
        self.doors = []

    def generate_room(self, x: int, y: int, height: int, width: int) -> tuple[int, int, int, int]:
        # Размер доступного пространства с учётом отступов
        available_width = width - ROOM_INDENT * 2
        available_height = height - ROOM_INDENT * 2

        # Проверка, влезает ли минимальная комната
        if available_width < WIDTH_MIN_ROOM or available_height < HEIGHT_MIN_ROOM:
            raise ValueError("Unable to create room: not enough space for minimum room size")

        r_width = randint(WIDTH_MIN_ROOM, available_width)
        r_height = randint(HEIGHT_MIN_ROOM, available_height)

        room_x = randint(x + ROOM_INDENT, x + width - ROOM_INDENT - r_width)
        room_y = randint(y + ROOM_INDENT, y + height - ROOM_INDENT - r_height)

        # Возвращаем координаты прямоугольника комнаты: (левый верхний угол, правый нижний)
        return room_x, room_y, room_x + r_width - 1, room_y + r_height - 1

    def random_door_side(self) -> list[str]:
        return sample(self.sides, k=randint(1, len(self.sides))) if self.sides else self.sides

    def remove_side(self, side: str):
        if side in self.sides:
            self.sides.remove(side)
    # was
    def generate_doors(self, side: str) -> tuple[int, str, coordinate]:
        self.remove_side(side)
        match side:
            case "top":
                door_position = self.y - 1, randint(self.x + 1, self.x_ - 1)
                next_ = self.id - 3, "bottom"
            case "bottom":
                door_position = self.y_ + 1, randint(self.x + 1, self.x_ - 1)
                next_ = self.id + 3, "top"
            case "left":
                door_position = randint(self.y + 1, self.y_ - 1), self.x - 1
                next_ = self.id - 1, "right"
            case "right":
                door_position = randint(self.y + 1, self.y_ - 1), self.x_ + 1
                next_ = self.id + 1, "left "
            case _:
                raise ValueError(f"Unable to generate door with an unknown side {side}")
            
        door = Door(door_position[0], door_position[1], self.id, side)
        self.doors_coordinates.add(door_position)
        self.doors.append(door)

        return *next_, door


    def get_wall_symbol(self, x, y):
        char = Cell.map_
        if (x == self.x - 1 or x == self.x_ + 1) and self.y <= y <= self.y_:
            char = Cell.vert_wall
        elif (y == self.y - 1 or y == self.y_ + 1) and self.x <= x <= self.x_:
            char = Cell.horiz_wall
        elif y == self.y - 1 and x == self.x - 1:
            char = Cell.top_left_wall
        elif x == self.x - 1 and y == self.y_ + 1:
            char = Cell.bottom_left_wall
        elif x == self.x_ + 1 and y == self.y - 1:
            char = Cell.top_right_wall
        elif x == self.x_ + 1 and y == self.y_ + 1:
            char = Cell.bottom_right_wall

        return char

    def is_valid_coordinate(self, x: int, y: int) -> bool:
        return self.x + 1 <= x <= self.x_ - 1 and self.y + 1 <= y <= self.y_ - 1

    def is_inside_the_room(self, y: int, x: int) -> bool:
        return self.x <= x <= self.x_ and self.y <= y <= self.y_
    
    @classmethod
    def from_saved(cls, id: int, x: int, y: int, x_: int, y_: int):
        room = cls.__new__(cls)  # создаём объект без вызова __init__
        room.id = id
        room.x, room.y, room.x_, room.y_ = x, y, x_, y_
        room.is_discovered = False
        room.is_foged = True
        room.sides = cls.door_side.get(id, []).copy()
        room.doors_coordinates = set()
        room.doors = []
        return room
