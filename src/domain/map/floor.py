from domain.map.room import Room
from domain.map.corridor import Corridor
from random import choice


class Floor:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.x = 0
        self.y = 0
        self.rooms = self.generate_level_room()
        self.corridors = []
        self.door_map = {}
        self.generate_corridors()
        self.color_doors()

    def color_doors(self):
        colored = []
        colors = ['Red', 'Green', 'Blue']
        for i in range(len(colors)):
            while True:
                corridor = choice(self.corridors)
                if corridor not in colored:
                    for door in corridor.doors:
                        for d in self.rooms[corridor.room1].doors:
                            if d.x == door.x and d.y and door.y:
                                d.color = colors[i]

                        for d in self.rooms[corridor.room2].doors:
                            if d.x == door.x and d.y and door.y:
                                d.color = colors[i]

                        door.color = colors[i]

                    self.door_map[corridor.room1][corridor.room2]['color'] = colors[i]
                    self.door_map[corridor.room2][corridor.room1]['color'] = colors[i]

                    colored.append(corridor)
                    break

    def open_corridor(self, y, x):
        d1_obj = None
        d2_obj = None

        # Находим двери в коридоре по координатам
        for corridor in self.corridors:
            if (corridor.doors[0].y == y and corridor.doors[0].x == x) or \
                    (corridor.doors[1].y == y and corridor.doors[1].x == x):
                d1_obj = corridor.doors[0]
                d2_obj = corridor.doors[1]

        # Открываем двери (меняем цвет)
        if d1_obj:
            d1_obj.color = 'White'
        if d2_obj:
            d2_obj.color = 'White'

        # Теперь ищем эти двери в комнатах и тоже меняем их цвет
        for room in self.rooms:
            for door in room.doors:
                if d1_obj and door.y == d1_obj.y and door.x == d1_obj.x:
                    door.color = 'White'
                if d2_obj and door.y == d2_obj.y and door.x == d2_obj.x:
                    door.color = 'White'

    def generate_level_room(self) -> list[Room]:
        rooms = []
        w_size = self.width // 3
        h_size = self.height // 3
        w_step = w_size - 1
        h_step = h_size - 1

        room_id = 0
        for col in range(3):
            for row in range(3):
                x = self.x + w_step * row
                y = self.y + h_step * col
                room = Room(x, y, h_size, w_size, room_id)
                rooms.append(room)
                room_id += 1
        return rooms

    def generate_corridors(self) -> None:
        self.corridors = []
        self.door_map = {}

        for room in self.rooms:
            for side in room.random_door_side():
                try:
                    target_id, target_side, door_a = room.generate_doors(side)
                    if 0 <= target_id < len(self.rooms):
                        target_room = self.rooms[target_id]
                        _, _, door_b = target_room.generate_doors(target_side.strip())
                        door_b.color = door_a.color

                        # Добавляем двери a и b в door_map
                        if room.id not in self.door_map:
                            self.door_map[room.id] = {}
                        self.door_map[room.id][target_id] = {
                            'side': target_side,
                            'color': door_a.color
                        }
                        if target_room.id not in self.door_map:
                            self.door_map[target_room.id] = {}
                        self.door_map[target_room.id][room.id] = {
                            'side': side,
                            'color': door_b.color
                        }
                        self.door_map[room.id][target_id]['pair_color'] = door_b.color
                        self.door_map[target_room.id][room.id]['pair_color'] = door_a.color

                        # Определим направление
                        direction = "h" if side in ["left", "right"] else "v"
                        a_position = door_a.y, door_a.x
                        b_position = door_b.y, door_b.x
                        corridor = Corridor(a_position, b_position, room.id, direction)
                        self.corridors.append(corridor)
                except Exception as e:
                    print(f"Error generate corridors: {e}")

    def get_room_by_id(self, room_id: int) -> Room | None:
        for room in self.rooms:
            if room.id == room_id:
                return room
        return None
