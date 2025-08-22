import time
import random
from collections import deque

from domain.map.floor import Floor
from domain.map.exit import Exit
from domain.map.validator import KeysValidator
from domain.player import Player
from domain.enemies import Enemy, Zombie
from domain.inventory import Item
from domain.cell import Cell
from domain.state import State
from domain.difficulty_adjuster import DifficultyAdjuster
from domain.inventory.door_key import DoorKey

class Game:
    def __init__(self, name, h, w):
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
            self.difficulty_adjuster.update(self.state, levels_passed=self.level-1)

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
        while not self.validator.bfs() and len(self.keys) != 3  and attempts < max_attempts:
            visited_rooms_excluding_current = self.validator.visited_rooms - {self.current_room_id}
            if not visited_rooms_excluding_current:
                break

            rand_visited_room_id = random.choice(list(visited_rooms_excluding_current))
            room = self.floor.get_room_by_id(rand_visited_room_id)

            remaining_colors = list(set(['Red', 'Green', 'Blue']) - self.validator.available_keys)
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
                if room.id != self.current_room_id or x != self.game.player.x or y != self.game.player.y:
                    break
            if not color:
                color = choice(['Red', 'Green', 'Blue'])
            return DoorKey(y, x, color)

    def correct_player_coordinates(self) -> None:
        self.player.y = (self.floor.rooms[self.current_room_id].y + self.floor.rooms[self.current_room_id].y_) // 2
        self.player.x = (self.floor.rooms[self.current_room_id].x + self.floor.rooms[self.current_room_id].x_) // 2
        self.player.inventory.doorkeys.clear()

    def init_first_room(self):
        room = self.floor.rooms[self.current_room_id]
        room.is_discovered = True
        room.is_foged = False
        self.update_current_room()
        

    def update_current_room(self):
        room = self.floor.rooms[self.current_room_id]
        y, x = self.player.y, self.player.x

        if (room.is_inside_the_room(y, x) or (y, x) in room.doors_coordinates):
            return
        
        self.floor.rooms[self.current_room_id].is_foged = True

        for room in self.floor.rooms:
            if (room.is_inside_the_room(y, x) or (y, x) in room.doors_coordinates):
                self.current_room_id = room.id
                self.floor.rooms[self.current_room_id].is_discovered = True
                self.fill_fog()

    def update_current_corridor(self):
        y, x = self.player.y, self.player.x

        if not (y, x) in self.floor.rooms[self.current_room_id].doors_coordinates:
            return
        
        point = None
        if self.map_grid[y][x+1] == Cell.room: point = (y, x - 1)
        elif self.map_grid[y][x-1] == Cell.room: point = (y, x + 1)
        elif self.map_grid[y+1][x] == Cell.room: point = (y - 1, x)
        elif self.map_grid[y-1][x] == Cell.room: point = (y + 1, x)

        if not point:
            return
                
        for cor in self.floor.corridors:
            if point in cor.corridor:
                cor.is_discovered = True

    def fill_fog(self):
        room = self.floor.rooms[self.current_room_id]
        y, x = self.player.y, self.player.x

        # если игрок за комнатой
        cell_symb = True

        # если игрок внутри комнаты
        if room.is_inside_the_room(y, x):
            cell_symb = False

        for i in range(room.y, room.y_ + 1):
                for j in range(room.x, room.x_ + 1):
                    self.fog_grid[i][j] = cell_symb

        # если игрок в двери
        if (y, x) in room.doors_coordinates:
            x_range = y_range = None
            
            # дверь слева или справа
            if self.map_grid[y][x-1] == Cell.floor:
                x_range = range(room.x - 1, room.x_ + 1)
            if self.map_grid[y][x+1] == Cell.floor:
                x_range = range(room.x_ + 1, room.x - 1, -1)
            if x_range:
                shift = 0
                for jx in x_range:
                    for i in range(0, shift):
                        if y + i <= room.y_:
                            self.fog_grid[y+i][jx] = False
                        if y - i >= room.y:
                            self.fog_grid[y-i][jx] = False
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
                            self.fog_grid[iy][x+j] = False
                        if x - j >= room.x:
                            self.fog_grid[iy][x-j] = False
                    shift += 1


    def spawn_entities(self):
        for room in filter(lambda room: room.id != self.current_room_id, self.floor.rooms):
            for _ in range(self.difficulty_adjuster.enemy_spawn_chance // 100  + 1):
                if random.random() < self.difficulty_adjuster.enemy_spawn_chance / 100:
                    enemy = Enemy.spawn(room)
                    enemy.update_difficulty(self.difficulty_adjuster.enemy_difficulty)
                    self.enemies.append(enemy)
            
            for _ in range(self.difficulty_adjuster.item_spawn_chance // 100  + 1):
                if random.random() < self.difficulty_adjuster.item_spawn_chance / 100:
                    item = Item.spawn(room, self.items)
                    self.items.append(item)


    def create_map_grid(self) -> list[list[Cell]]:
        self.fill_fog()

        self.update_current_room()
        self.update_current_corridor()
        map_grid = [[Cell.map_ for _ in range(self.width)] for _ in range(self.height)]

        for room in self.floor.rooms:
            if not room.is_discovered:
                continue

            for y in range(room.y, room.y_ + 1):
                for x in range(room.x, room.x_ + 1):
                    is_foged = self.fog_grid[y][x]
                    map_grid[y][x] = [Cell.room, Cell.fog][is_foged]

            map_grid = self.fill_room_wall(map_grid, room)
            self.fill_room_wall(map_grid, room)

            for door in room.doors:
                if door.color == 'White':
                    map_grid[door.y][door.x] = Cell.door
                elif door.color == 'Red':
                    map_grid[door.y][door.x] = Cell.door_red
                elif door.color == 'Green':
                    map_grid[door.y][door.x] = Cell.door_green
                elif door.color == 'Blue':
                    map_grid[door.y][door.x] = Cell.door_blue

        for corridor in self.floor.corridors:
            if not corridor.is_discovered:
                continue

            for (y, x) in corridor.tiles():
                map_grid[y][x] = Cell.floor

            for door in corridor.doors:
                if door.color == 'White':
                    map_grid[door.y][door.x] = Cell.door
                elif door.color == 'Red':
                    map_grid[door.y][door.x] = Cell.door_red
                elif door.color == 'Green':
                    map_grid[door.y][door.x] = Cell.door_green
                elif door.color == 'Blue':
                    map_grid[door.y][door.x] = Cell.door_blue

        for item in self.items:
            if item.type == "Gold":
                cell = Cell.gold
            elif item.type == "Potion":
                cell = Cell.potion
            elif item.type == "Scroll":
                cell = Cell.scroll
            elif item.type == "Food":
                cell = Cell.food
            elif item.type == "Weapon":
                cell = Cell.weapon
            # elif item.type == "Red Key":
            #     cell = Cell.doorkey_r
            # elif item.type == "Green Key":
            #     cell = Cell.doorkey_g
            # elif item.type == "Blue Key":
            #     cell = Cell.doorkey_b

            is_foged = self.fog_grid[item.y][item.x]
            map_grid[item.y][item.x] = [cell, Cell.fog][is_foged]

        for enemy in self.enemies:
            if enemy.name == 'Zombie':
                cell = Cell.zombie
            elif enemy.name == 'Vampire':
                cell = Cell.vampire
            elif enemy.name == 'Ghost':
                cell = Cell.ghost
            elif enemy.name == 'Unseen Ghost':
                cell = Cell.ghost_unseen
            elif enemy.name == 'Ogre':
                cell = Cell.ogre
            elif enemy.name == 'Snake Wizard':
                cell = Cell.snake_wizard
            elif enemy.name == 'Mimic':
                cell = Cell.mimic
            elif enemy.name == 'Potion':
                cell = Cell.potion
            elif enemy.name == 'Food':
                cell = Cell.food
            elif enemy.name == 'Scroll':
                cell = Cell.scroll
            elif enemy.name == 'Weapon':
                cell = Cell.weapon
            elif enemy.name == "Red Key":
                cell = Cell.doorkey_r
            elif enemy.name == "Green Key":
                cell = Cell.doorkey_g
            elif enemy.name == "Blue Key":
                cell = Cell.doorkey_b
            
            is_foged = self.fog_grid[enemy.y][enemy.x]
            map_grid[enemy.y][enemy.x] = [cell, Cell.fog][is_foged]
        
        for key in self.keys:
            if key.color == 'Red':
                cell = Cell.doorkey_r
            elif key.color == 'Green':
                cell = Cell.doorkey_g
            elif key.color == 'Blue':
                cell = Cell.doorkey_b
            is_foged = self.fog_grid[key.y][key.x]

            map_grid[key.y][key.x] = [cell, Cell.fog][is_foged]


        is_foged = self.fog_grid[self.exit.y][self.exit.x]
        map_grid[self.exit.y][ self.exit.x] = [Cell.exit_, Cell.fog][is_foged]

        return map_grid
    
    def fill_room_wall(self, map_grid, room):
        for y in range(room.y - 1, room.y_ + 2):
            for x in range(room.x - 1, room.x_ + 2):
                if map_grid[y][x] == Cell.map_:
                    map_grid[y][x] = room.get_wall_symbol(x, y)
        return map_grid

    def create_fog_grid(self):
        fog_grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        for room in self.floor.rooms:
            if not room.is_foged:
                continue

            for y in range(room.y, room.y_ + 1):
                for x in range(room.x, room.x_ + 1):
                    fog_grid[y][x] = True

        return fog_grid

    def is_player_at_exit(self):
        return self.player.is_on_cell(self.exit)