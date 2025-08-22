import json
import os

from domain.game_logic import Game
from domain.map.floor import Floor, Room, Corridor
from domain.map.exit import Exit
from domain.inventory import Food, Weapon, Potion, Scroll
from domain.cell import Cell
from domain.inventory.inventory import Inventory
from domain.difficulty_adjuster import DifficultyAdjuster
from domain.state import State
from domain.enemies import Enemy, Zombie, Vampire, Ghost, Ogre, SnakeWizard, Mimic
from domain.player import Player
from domain.map.door import Door
from domain.inventory.door_key import DoorKey


class LoadManager:
    @staticmethod
    def load(data) -> Game:
        game = Game('name', data['height'], data['width'])
        game.current_room_id = data['current_room_id']
        game.difficulty_adjuster = LoadManager.load_difficulty_adjuster(data['difficulty_adjuster'])
        game.level = data['level']
        game.floor = LoadManager.load_floor(data['floor'])
        game.exit = LoadManager.load_exit(data['exit'])
        game.fog_grid = LoadManager.load_fog_grid(data['fog_grid'])
        game.map_grid = LoadManager.load_map_grid(data['map_grid'])
        game.player = LoadManager.load_player(data['player'])
        game.enemies = [LoadManager.load_enemy(e) for e in data['enemies']]
        game.items = [LoadManager.load_item(i) for i in data['items']]
        game.keys = [LoadManager.load_item(i) for i in data['keys']]
        game.state = LoadManager.load_state(data['state'])
        return game

    @staticmethod
    def load_map_grid(data: list[list[str]]) -> list[list[Cell]]:
        return [[Cell[cell_name] for cell_name in row] for row in data]

    @staticmethod
    def load_fog_grid(data: list[list[int]]) -> list[list[bool]]:
        return [[bool(cell) for cell in row] for row in data]
    
    @staticmethod
    def load_floor(data) -> Floor:
        floor = Floor(data['height'], data['width'])
        floor.x = data['x']
        floor.y = data['y']
        floor.rooms = [LoadManager.load_room(r) for r in data['rooms']]
        floor.corridors = [LoadManager.load_corridor(c) for c in data['corridors']]
        return floor

    @staticmethod
    def load_room(data) -> Room:
        room = Room.from_saved(data['id'], data['x'], data['y'], data['x_'], data['y_'])
        room.is_discovered = data['is_discovered']
        room.is_foged = data['is_foged']
        room.doors_coordinates = set(tuple(coord) for coord in data['doors_coordinates'])
        # восстанавливаем двери как объекты
        room.doors = []
        for d in data['doors']:
            door = Door(d['y'], d['x'], d['room_id'], d['side'])  # только 4 аргумента
            door.color = d.get('color', 'White')  # если цвет не сохранён, по умолчанию White
            room.doors.append(door)
        return room

    @staticmethod
    def load_corridor(data) -> Corridor:
        corridor = Corridor(tuple(data['start']), tuple(data['finish']), data['room1'], 'h')
        corridor.corridor = {tuple(k): None for k in data['corridor']}
        corridor.room1 = data['room1']
        corridor.room2 = data['room2']
        corridor.doors = []
        for d in data['doors']:
            door = Door(d['y'], d['x'], d['room_id'], d['side'])
            door.color = d.get('color', 'White')
            corridor.doors.append(door)
        corridor.is_discovered = data['is_discovered']
        return corridor

    @staticmethod
    def load_exit(data) -> Exit:
        return Exit.from_data(data)

    @staticmethod
    def load_state(data) -> State:
        state = State()
        state.player = data.get('player')
        state.enemy = data.get('enemy')
        state.item = data.get('item')
        state.killed_by = data.get('killed_by')
        state.treasures = data.get('treasures')
        state.damage_taken = data.get('damage_taken')
        state.damage_dealt = data.get('damage_dealt')
        state.food_used = data.get('food_used')
        state.potions_used = data.get('potions_used')
        state.scrolls_used = data.get('scrolls_used')
        state.enemies_killed = data.get('enemies_killed')
        state.cells_passed = data.get('cells_passed')
        state.player_hp_percent = data.get('player_hp_percent')
        state.game_state = 'play'
        return state

    @staticmethod
    def load_difficulty_adjuster(data) -> DifficultyAdjuster:
        difficulty_adjuster = DifficultyAdjuster()
        difficulty_adjuster.enemy_spawn_chance = data['enemy_spawn_chance']
        difficulty_adjuster.enemy_difficulty = data['enemy_difficulty']
        difficulty_adjuster.item_spawn_chance = data['item_spawn_chance']
        return difficulty_adjuster

    @staticmethod
    def load_inventory(data) -> Inventory:
        inventory = Inventory()
        inventory.food = [LoadManager.load_item(i) for i in data['food']]
        inventory.potions = [LoadManager.load_item(i) for i in data['potions']]
        inventory.scrolls = [LoadManager.load_item(i) for i in data['scrolls']]
        inventory.weapons = [LoadManager.load_item(i) for i in data['weapons']]
        inventory.doorkeys = [LoadManager.load_item(i) for i in data['doorkeys']]
        return inventory

    @staticmethod
    def load_weapon(data):
        return LoadManager.load_item(data) if data else None

    @staticmethod
    def load_player(data) -> Player:
        player = Player(data['name'], data['current_room_id'], data['y'], data['x'])
        player.max_health = data['max_health']
        player.health = data['health']
        player.agility = data['agility']
        player.strength = data['strength']
        player.gold = data['gold']
        player.experience_level = data['experience_level']
        player.experience = data['experience']
        player.inventory = LoadManager.load_inventory(data['inventory'])
        player.timers = data['timers']
        player.bonus_values = data['bonus_values']
        player.weapon = LoadManager.load_weapon(data['weapon'])
        player.is_sleeping = data['is_sleeping']
        return player

    @staticmethod
    def load_item(data):
        match data['type']:
            case "Food":
                item = Food(data['y'], data['x'])
                item.amount = data['amount']
            case "Weapon":
                item = Weapon(data['y'], data['x'])
                item.amount = data['amount']
            case "Potion":
                item = Potion(data['y'], data['x'])
                item.ability = data['ability']
                item.strength_label = data['strength_label']
                item.amount = data['amount']
                item.duration = data['duration']
            case "Scroll":
                item = Scroll(data['y'], data['x'])
            case "Red Key" | "Green Key" | "Blue Key":
                item = DoorKey(data['y'], data['x'], data['color'])
            case _:
                raise ValueError(f"Unknown item type: {data['type']}")

        item.subtype = data['subtype']
        return item
    
    @staticmethod
    def load_enemy(data) -> Enemy:
        name = data['name']
        match name:
            case 'Mimic':
                enemy = Mimic(data['y'], data['x'], data['current_room_id'])
            case 'Vampire':
                enemy = Vampire(data['y'], data['x'], data['current_room_id'])
            case 'Ogre':
                enemy = Ogre(data['y'], data['x'], data['current_room_id'])
            case 'SnakeWizard':
                enemy = SnakeWizard(data['y'], data['x'], data['current_room_id'])
            case 'Ghost':
                enemy = Ghost(data['y'], data['x'], data['current_room_id'])
            case 'Zombie':
                enemy = Zombie(data['y'], data['x'], data['current_room_id'])
            case _:
                raise ValueError(f"Unknown enemy type: {name}")

        enemy.health = data['health']
        enemy.agility = data['agility']
        enemy.strength = data['strength']
        enemy.hostility = data['hostility']
        enemy.experience = data['experience']
        enemy.direction = data['direction']

        if 'view' in data:
            enemy.view = data['view']
            enemy.name = enemy.view
        if 'y_direction' in data:
            enemy.y_direction = data['y_direction']
        if 'shield' in data:
            enemy.shield = data['shield']
        if 'is_resting' in data:
            enemy.is_resting = data['is_resting']

        return enemy
    @staticmethod
    def SCOREBOARD_LOAD():
        filename = os.path.join("datalayer", "SCOREBOARD.json")

        # Загружаем старые данные (если файл есть)
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        return data

