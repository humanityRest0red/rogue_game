import json
import os

from domain.game_logic import Game
from domain.map.floor import Floor, Room, Corridor
from domain.map.exit import Exit
from domain.inventory import Item, Food, Weapon, Potion, Scroll
from domain.cell import Cell
from domain.inventory.inventory import Inventory
from domain.difficulty_adjuster import DifficultyAdjuster
from domain.state import State
from domain.enemies import Enemy
from domain.player import Player


SAVES_FOLDER = 'datalayer/saves/'

# def count_files_in_folder(folder_path):
#     file_list = os.listdir(folder_path)
#     count = 0
#     for item in file_list:
#         item_path = os.path.join(folder_path, item)
#         if os.path.isfile(item_path):
#             count += 1
#     return count       

class SaveManager:
    @staticmethod
    def save(player_name, game: Game):
        data = {
            'height': game.height,
            'width': game.width,
            'level': game.level,
            'current_room_id': game.current_room_id,
            'difficulty_adjuster': SaveManager.save_difficulty_adjuster(game.difficulty_adjuster),
            'floor': SaveManager.save_floor(game.floor),
            'fog_grid': SaveManager.save_fog_grid(game.fog_grid),
            'map_grid': SaveManager.save_map_grid(game.map_grid),
            'exit': SaveManager.save_exit(game.exit),
            'player': SaveManager.save_player(game.player),
            'enemies': [SaveManager.save_enemy(e) for e in game.enemies],
            'items': [SaveManager.save_item(i) for i in game.items],
            'keys': [SaveManager.save_item(i) for i in game.keys],
            'state': SaveManager.save_state(game.state)
        }
        filename = os.path.join(SAVES_FOLDER, f"{player_name}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def save_map_grid(map_grid: list[list[Cell]]) -> list[list[str]]:
        return [[cell.name for cell in row] for row in map_grid]

    @staticmethod
    def save_fog_grid(fog_grid: list[list[bool]]) -> list[list[int]]:
        return [[int(cell) for cell in row] for row in fog_grid]

    @staticmethod
    def save_floor(floor: Floor):
        return {
            'height': floor.height,
            'width': floor.width,
            'x': floor.x,
            'y': floor.y,
            'rooms': [SaveManager.save_room(r) for r in floor.rooms],
            'corridors': [SaveManager.save_corridor(c) for c in floor.corridors],
        }

    def save_room(room: Room):
        return {
            'id': room.id,
            'x': room.x,
            'y': room.y,
            'x_': room.x_,
            'y_': room.y_,
            'is_discovered': room.is_discovered,
            'is_foged': room.is_foged,
            'doors_coordinates': list(room.doors_coordinates),
            'doors': [
                {
                    'x': d.x,
                    'y': d.y,
                    'room_id': d.room_id,
                    'side': d.side,
                    'color': d.color
                }
                for d in room.doors
            ]
        }

    @staticmethod
    def save_corridor(corridor: Corridor):
        return {
            'start': corridor.start,
            'finish': corridor.finish,
            'room1': corridor.room1,
            'room2': corridor.room2,
            'corridor': list(corridor.corridor.keys()),
            'doors': [
                {
                    'x': d.x,
                    'y': d.y,
                    'room_id': d.room_id,
                    'side': d.side,
                    'color': d.color
                }
                for d in corridor.doors
            ],
            'is_discovered': corridor.is_discovered
        }

    
    @staticmethod
    def save_exit(exit: Exit):
        return {
            'id': exit.id,
            'x': exit.x,
            'y': exit.y,
        }

    @staticmethod
    def save_difficulty_adjuster(difficulty_adjuster: DifficultyAdjuster):
        return {
            'enemy_spawn_chance': difficulty_adjuster.enemy_spawn_chance,
            'enemy_difficulty': difficulty_adjuster.enemy_difficulty,
            'item_spawn_chance': difficulty_adjuster.item_spawn_chance
        }

    @staticmethod
    def save_state(state: State):
        return {
            'player': state.player,
            'enemy': state.enemy,
            'item': state.item,
            'killed_by': state.killed_by,
            'treasures': state.treasures,
            'game_state': state.game_state,
            'damage_taken': state.damage_taken,
            'damage_dealt': state.damage_dealt,
            'food_used': state.food_used,
            'potions_used': state.potions_used,
            'scrolls_used': state.scrolls_used,
            'enemies_killed': state.enemies_killed,
            'cells_passed': state.cells_passed,
            'player_hp_percent': state.player_hp_percent
        }
        
    def save_item(item: Item):
        base = {
            'y': item.y,
            'x': item.x,
            'type': item.type,
            'subtype': item.subtype
        }

        match item.type:
            case "Food":
                base['amount'] = item.amount
            case "Weapon":
                base['amount'] = item.amount
            case "Potion":
                base['ability'] = item.ability
                base['strength_label'] = item.strength_label
                base['amount'] = item.amount
                base['duration'] = item.duration
            case "Scroll":
                pass
            case "Red Key" | "Green Key" | "Blue Key":
                base['color'] = item.color
            case _:
                raise ValueError(f"Unknown item type: {item.type}")

        return base
    
    @staticmethod
    def save_enemy(enemy: Enemy):
        base = {
            'x': enemy.x,
            'y': enemy.y,
            'name': enemy.__class__.__name__,
            'current_room_id': enemy.current_room_id,
            'health': enemy.health,
            'agility': enemy.agility,
            'strength': enemy.strength,
            'hostility': enemy.hostility,
            'experience': enemy.experience,
            'direction': enemy.direction
        }

        match enemy.__class__.__name__:
            case 'Mimic':
                base['view'] = enemy.view
            case 'SnakeWizard':
                base['y_direction'] = enemy.y_direction
            case 'Vampire':
                base['shield'] = enemy.shield
            case 'Ogre':
                base['is_resting'] = enemy.is_resting
            case 'Ghost' | 'Zombie':
                pass
            case _:
                raise ValueError(f"Unknown enemy class: {enemy.__class__.__name__}")

        return base

    @staticmethod
    def save_inventory(inventory: Inventory):
        return {
            'food': [SaveManager.save_item(i) for i in inventory.food],
            'potions': [SaveManager.save_item(i) for i in inventory.potions],
            'scrolls': [SaveManager.save_item(i) for i in inventory.scrolls],
            'weapons': [SaveManager.save_item(i) for i in inventory.weapons],
            'doorkeys': [SaveManager.save_item(i) for i in inventory.doorkeys]
        }

    @staticmethod
    def save_weapon(weapon: Weapon | None):
        return SaveManager.save_item(weapon) if weapon else None

    @staticmethod
    def save_player(player: Player):
        return {
            'name': player.name,
            'current_room_id': player.current_room_id,
            'x': player.x,
            'y': player.y,
            'max_health': player.max_health,
            'health': player.health,
            'agility': player.agility,
            'strength': player.strength,
            'gold': player.gold,
            'experience_level': player.experience_level,
            'experience': player.experience,
            'inventory': SaveManager.save_inventory(player.inventory),
            'timers': player.timers,
            'bonus_values': player.bonus_values,
            'weapon': SaveManager.save_weapon(player.weapon),
            'is_sleeping': player.is_sleeping
        }
        

        
    @staticmethod
    def SCOREBOARD(player_name, game: Game):
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

        record = {
            "player": player_name,
            "gold": game.player.gold,
            "enemies_killed": game.state.enemies_killed,
            "food_used": game.state.food_used,
            "potions_used": game.state.potions_used,
            "scrolls_used": game.state.scrolls_used,
            "damage_taken": game.state.damage_taken,
            "damage_dealt": game.state.damage_dealt,
            "cells_passed": game.state.cells_passed,
            "level_player": game.player.experience_level,
            "level_dugeon": game.level,
            "is_win": game.state.game_state == "win"
        }
        data.append(record)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)