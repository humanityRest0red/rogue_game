import time
import random

from domain.map.floor import Floor
from domain.map.exit import Exit
from domain.map.validator import KeysValidator
from domain.player import Player
from domain.enemies import Enemy
from domain.inventory import Item
from domain.cell import Cell
from domain.state import State
from domain.difficulty_adjuster import DifficultyAdjuster
from domain.inventory.door_key import DoorKey


class Game:
    def __init__(self, name, h, w):
        self.map_grid = None
        self.fog_grid = None
        self.validator = None
        self.keys_map = None
        self.keys = None
        self.items = None
        self.enemies = None
        self.exit = None
        self.floor = None
        random.seed(time.time())

        self.height = h
        self.width = w
        self.level = 0
        self.current_room_id = random.randint(0, 8)

        self.difficulty_adjuster = DifficultyAdjuster()
        self.state = State()
        self.player = Player(name=name, current_room_id=self.current_room_id, y=0, x=0)

        self.gen_next_floor()

    def gen_next_floor(self):
        self.level += 1

        if self.level > 1:
            self.difficulty_adjuster.update(self.state, levels_passed=self.level - 1)

        self.floor = Floor(self.height, self.width)
        self.exit = Exit(self.current_room_id, self.floor.rooms)

        self.init_first_room()

        self.enemies = []
        self.items = []
        self.keys = []

        self.correct_player_coordinates()
        self.spawn_entities()
        self.keys_map = [item for item in self.items if isinstance(item, DoorKey)]
        self.validator = KeysValidator(self.floor, self.current_room_id, self.keys_map)
        self.validate_floor()
        self.init_first_room()

        self.fog_grid = self.create_fog_grid()
        self.map_grid = self.create_map_grid()

    def validate_floor(self, max_attempts=50):
        start_room = self.floor.get_room_by_id(self.current_room_id)
        start_door = random.choice(start_room.doors)
        if start_door.color != 'White':
            first_key = DoorKey(self.player.y, self.player.x, start_door.color)
            self.player.inventory.doorkeys = []
            self.player.inventory.doorkeys.append(first_key)
            self.validator.available_keys.add(start_door.color)

        self.validator.available_keys.clear()

        self.validator.visited_rooms.add(start_room.id)

        attempts = 0
        while not self.validator.bfs() and len(self.keys) != 3 and attempts < max_attempts:
            visited_rooms_excluding_current = self.validator.visited_rooms - {self.current_room_id}
            if not visited_rooms_excluding_current:
                break

            rand_visited_room_id = random.choice(list(visited_rooms_excluding_current))
            room = self.floor.get_room_by_id(rand_visited_room_id)

            remaining_colors = list({'Red', 'Green', 'Blue'} - self.validator.available_keys)
            if not remaining_colors:
                remaining_colors = ['Red', 'Green', 'Blue']

            rand_color = random.choice(remaining_colors)

            new_key = self.generate_rand_doorkey(room, rand_color)
            self.keys.append(new_key)
            self.keys_map.append(new_key)
            self.validator.keys_map.append(new_key)

            if rand_color != 'White':
                self.validator.available_keys.add(rand_color)

            self.validator.visited_rooms.clear()
            self.validator.visited_rooms.add(start_room.id)

            attempts += 1

        if attempts >= max_attempts:
            raise Exception("Can't validate the floor.")

        return True

    def generate_rand_doorkey(self, room, color=None):
        while True:
            x = random.randint(room.x, room.x_)
            y = random.randint(room.y, room.y_)
            if room.id != self.current_room_id or x != self.player.x or y != self.player.y:
                break
        if not color:
            color = random.choice(['Red', 'Green', 'Blue'])
        return DoorKey(y, x, color)

    def correct_player_coordinates(self) -> None:
        self.player.y = (self.floor.rooms[self.current_room_id].y + self.floor.rooms[self.current_room_id].y_) // 2
        self.player.x = (self.floor.rooms[self.current_room_id].x + self.floor.rooms[self.current_room_id].x_) // 2
        self.player.inventory.doorkeys.clear()

    def init_first_room(self):
        room = self.floor.rooms[self.current_room_id]
        room.is_discovered = True
        room.is_fogged = False
        self.update_current_room()

    def update_current_room(self):
        room = self.floor.rooms[self.current_room_id]
        y, x = self.player.y, self.player.x

        if room.is_inside_the_room(y, x) or (y, x) in room.doors_coordinates:
            return

        self.floor.rooms[self.current_room_id].is_fogged = True

        for room in self.floor.rooms:
            if room.is_inside_the_room(y, x) or (y, x) in room.doors_coordinates:
                self.current_room_id = room.id
                self.floor.rooms[self.current_room_id].is_discovered = True
                self.fill_fog()

    def update_current_corridor(self):
        y, x = self.player.y, self.player.x

        if not (y, x) in self.floor.rooms[self.current_room_id].doors_coordinates:
            return

        point = None
        if self.map_grid[y][x + 1] == Cell.room:
            point = (y, x - 1)
        elif self.map_grid[y][x - 1] == Cell.room:
            point = (y, x + 1)
        elif self.map_grid[y + 1][x] == Cell.room:
            point = (y - 1, x)
        elif self.map_grid[y - 1][x] == Cell.room:
            point = (y + 1, x)

        if not point:
            return

        for cor in self.floor.corridors:
            if point in cor.corridor:
                cor.is_discovered = True

    def fill_fog(self):
        room = self.floor.rooms[self.current_room_id]
        y, x = self.player.y, self.player.x

        cell_symb = not room.is_inside_the_room(y, x)

        for i in range(room.y, room.y_ + 1):
            for j in range(room.x, room.x_ + 1):
                self.fog_grid[i][j] = cell_symb

        # если игрок в двери
        if (y, x) in room.doors_coordinates:
            x_range = y_range = None

            # дверь слева или справа
            if self.map_grid[y][x - 1] == Cell.floor:
                x_range = range(room.x - 1, room.x_ + 1)
            if self.map_grid[y][x + 1] == Cell.floor:
                x_range = range(room.x_ + 1, room.x - 1, -1)
            if x_range:
                shift = 0
                for jx in x_range:
                    for i in range(0, shift):
                        if y + i <= room.y_:
                            self.fog_grid[y + i][jx] = False
                        if y - i >= room.y:
                            self.fog_grid[y - i][jx] = False
                    shift += 1

            # дверь сверху или снизу
            if self.map_grid[y - 1][x] == Cell.floor:
                y_range = range(room.y - 1, room.y_ + 1)
            if self.map_grid[y + 1][x] == Cell.floor:
                y_range = range(room.y_ + 1, room.y - 1, -1)
            if y_range:
                shift = 0
                for iy in y_range:
                    for j in range(0, shift):
                        if x + j <= room.x_:
                            self.fog_grid[iy][x + j] = False
                        if x - j >= room.x:
                            self.fog_grid[iy][x - j] = False
                    shift += 1

    def spawn_entities(self):
        for room in filter(lambda room: room.id != self.current_room_id, self.floor.rooms):
            for _ in range(self.difficulty_adjuster.enemy_spawn_chance // 100 + 1):
                if random.random() < self.difficulty_adjuster.enemy_spawn_chance / 100:
                    enemy = Enemy.spawn(room)
                    enemy.update_difficulty(self.difficulty_adjuster.enemy_difficulty)
                    self.enemies.append(enemy)

            for _ in range(self.difficulty_adjuster.item_spawn_chance // 100 + 1):
                if random.random() < self.difficulty_adjuster.item_spawn_chance / 100:
                    item = Item.spawn(room, self.items)
                    self.items.append(item)

    def create_map_grid(self) -> list[list[Cell]]:
        self.fill_fog()

        self.update_current_room()
        self.update_current_corridor()
        map_grid = [[Cell.map_ for _ in range(self.width)] for _ in range(self.height)]

        door_mapping = {
            'White': Cell.door,
            'Red': Cell.door_red,
            'Green': Cell.door_green,
            'Blue': Cell.door_blue
        }

        for room in self.floor.rooms:
            if not room.is_discovered:
                continue

            for y in range(room.y, room.y_ + 1):
                for x in range(room.x, room.x_ + 1):
                    is_fogged = self.fog_grid[y][x]
                    map_grid[y][x] = [Cell.room, Cell.fog][is_fogged]

            map_grid = self.fill_room_wall(map_grid, room)

            for door in room.doors:
                cell_type = door_mapping.get(door.color)
                if cell_type is not None:
                    map_grid[door.y][door.x] = cell_type

        for corridor in self.floor.corridors:
            if not corridor.is_discovered:
                continue

            for (y, x) in corridor.tiles():
                map_grid[y][x] = Cell.floor

            for door in corridor.doors:
                cell_type = door_mapping.get(door.color)
                if cell_type is not None:
                    map_grid[door.y][door.x] = cell_type

        for item in self.items:
            match item.type:
                case "Gold":
                    cell = Cell.gold
                case "Potion":
                    cell = Cell.potion
                case "Scroll":
                    cell = Cell.scroll
                case "Food":
                    cell = Cell.food
                case "Weapon":
                    cell = Cell.weapon
                case _:
                    raise ValueError(f"Undefined item type: {item.type}")
                # case "Red Key":
                #     cell = Cell.doorkey_r
                # case "Green Key":
                #     cell = Cell.doorkey_g
                # case "Blue Key":
                #     cell = Cell.doorkey_b

            is_fogged = self.fog_grid[item.y][item.x]
            map_grid[item.y][item.x] = [cell, Cell.fog][is_fogged]

        for enemy in self.enemies:
            match enemy.name:
                case 'Zombie':
                    cell = Cell.zombie
                case 'Vampire':
                    cell = Cell.vampire
                case 'Ghost':
                    cell = Cell.ghost
                case 'Unseen Ghost':
                    cell = Cell.ghost_unseen
                case 'Ogre':
                    cell = Cell.ogre
                case 'Snake Wizard':
                    cell = Cell.snake_wizard
                case 'Mimic':
                    cell = Cell.mimic
                case 'Potion':
                    cell = Cell.potion
                case 'Food':
                    cell = Cell.food
                case 'Scroll':
                    cell = Cell.scroll
                case 'Weapon':
                    cell = Cell.weapon
                case 'Red Key':
                    cell = Cell.doorkey_r
                case 'Green Key':
                    cell = Cell.doorkey_g
                case 'Blue Key':
                    cell = Cell.doorkey_b
                case _:
                    raise ValueError(f"Undefined enemy name: {enemy.name}")

            is_fogged = self.fog_grid[enemy.y][enemy.x]
            map_grid[enemy.y][enemy.x] = [cell, Cell.fog][is_fogged]

        for key in self.keys:
            match key.color:
                case 'Red':
                    cell = Cell.doorkey_r
                case 'Green':
                    cell = Cell.doorkey_g
                case 'Blue':
                    cell = Cell.doorkey_b
                case _:
                    raise ValueError(f"Undefined key color: {key.color}")

            is_fogged = self.fog_grid[key.y][key.x]

            map_grid[key.y][key.x] = [cell, Cell.fog][is_fogged]

        is_fogged = self.fog_grid[self.exit.y][self.exit.x]
        map_grid[self.exit.y][self.exit.x] = [Cell.exit_, Cell.fog][is_fogged]

        return map_grid

    @staticmethod
    def fill_room_wall(map_grid, room) -> list[list[int]]:
        for y in range(room.y - 1, room.y_ + 2):
            for x in range(room.x - 1, room.x_ + 2):
                if map_grid[y][x] == Cell.map_:
                    map_grid[y][x] = room.get_wall_symbol(x, y)
        return map_grid

    def create_fog_grid(self) -> list[list[bool]]:
        fog_grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        for room in self.floor.rooms:
            if not room.is_fogged:
                continue

            for y in range(room.y, room.y_ + 1):
                for x in range(room.x, room.x_ + 1):
                    fog_grid[y][x] = True

        return fog_grid

    def is_player_at_exit(self) -> bool:
        return self.player.is_on_cell(self.exit)
