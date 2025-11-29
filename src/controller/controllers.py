import curses
import time
import os
import json

from datalayer.save_manager import SaveManager
from datalayer.load_manager import LoadManager
from domain.game_logic import Game
from domain.setting import HEIGHT_MAP, WIDTH_MAP
from domain.state import menu_states
from view.curses_view.ui import GameUI
from view.pygame_view_3d.ui import GameUI3D


class GameController:
    def __init__(self, mod):
        self.game = None
        if mod == "Curses":
            self.view = GameUI(self)
        else:
            self.view = GameUI3D(self)

    def update_menu_state(self, action, menu_line):
        state = 'chosing'

        if action == 'apply':
            state = menu_states[menu_line]
        elif action == 'down':
            menu_line += 1
        elif action == 'up':
            menu_line -= 1

        menu_line %= len(menu_states)

        return state, menu_line

    def menu_loop(self):
        action = ''
        menu_line = 0
        while True:
            try:
                self.view.draw_start_menu(menu_line)

                action = self.view.handle_input()
                state, menu_line = self.update_menu_state(action, menu_line)

                if state == 'chosing':
                    pass
                elif state == 'start_game':
                    self.view.clear()
                    name = self.view.draw_name_input()
                    self.view.clear()
                    if name:
                        self.game = Game(name=name, h=HEIGHT_MAP, w=WIDTH_MAP)
                        self.game_loop()
                    state = 'chosing'
                elif state == 'load_game':
                    self.view.clear()
                    data = self.load_loop()
                    self.view.clear()
                    if data:
                        self.game = LoadManager.load(data)
                        self.game_loop()
                    self.view.clear()
                    state = 'chosing'
                elif state == 'show_score':
                    self.view.clear()
                    self.view.scoreboard_loop()
                    self.view.clear()
                    pass
                    state = 'chosing'
                elif state == 'exit':
                    self.view.clear()
                    break
            except curses.error:
                self.view.print_curses_error()

    def load_loop(self):
        save_dir = "datalayer/saves"
        saves = [f for f in os.listdir(save_dir) if f.endswith(".json")]

        if not saves:
            self.view.show_no_saves()
            self.view.press_key()
            return None

        selected = 0
        while True:
            self.view.show_load_menu(saves, selected)
            action = self.view.handle_input()
            if action == 'exit':
                return None
            elif action == 'up':
                selected = (selected - 1) % len(saves)
            elif action == 'down':
                selected = (selected + 1) % len(saves)
            elif action == 'apply':
                selected_file = os.path.join(save_dir, saves[selected])
                with open(selected_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data

    def inventory_loop(self, item_type: str):
        self.view.clear()
        mode = "use"
        inv = getattr(self.game.player.inventory, item_type)

        if not inv:
            self.view.message(f"{item_type.capitalize()} inventory is empty")
            return

        while True:
            try:
                current = self.game.player.weapon if item_type == "weapons" else None
                self.view.choose_from_inventory(inv, f"Choose {item_type}:", show_current=current, mode=mode)

                action = self.view.handle_inventory_input()

                if action == "exit":
                    break

                elif action == "toggle":
                    mode = "drop" if mode == "use" else "use"

                elif action.isdigit():
                    idx = int(action) - 1
                    if 0 <= idx < len(inv):
                        item = inv[idx]

                        self.use_or_drop(item_type, item, mode, inv)
                        self.view.clear()
                        if not inv:
                            self.game_state = "play"
                            break

            except curses.error:
                self.view.print_curses_error()

    def use_or_drop(self, item_type, item, mode, inv):
        if mode == "use":
            if item_type == "food":
                self.game.player.use_food(item)
            elif item_type == "scrolls":
                self.game.player.use_scroll(item)
            elif item_type == "weapons":
                self.game.player.take_weapon(item, self.game.items, self.game.map_grid)
            elif item_type == "potions":
                self.game.player.use_potion(item)
        else:  # drop
            self.game.player.drop_item(item, self.game.items, self.game.map_grid)
            inv.remove(item)

    def move_player(self, direction):
        self.game.player.move(direction, self.game.map_grid, self.game.enemies, self.game.items, self.game.keys, self.game.floor)

    def use_item(self, item_type):
        match item_type:
            case 'food':
                if self.game.player.inventory.food:
                    self.game.state.item = 'food'
                else:
                    self.game.state.item = 'You have no food'
            case 'scroll':
                if self.game.player.inventory.scrolls:
                    self.game.state.item = 'scrolls'
                else:
                    self.game.state.item = 'You have no scroll'
            case 'potion':
                if self.game.player.inventory.potions:
                    self.game.state.item = 'potions'
                else:
                    self.game.state.item = 'You have no potion'
            case 'weapon':
                if self.game.player.inventory.weapons:
                    self.game.state.item = 'weapons'
                else:
                    self.game.state.item = 'You have no weapon'
            case _:
                self.game.state.item = 'Unknown item'

    def run(self):
        if isinstance(self.view, GameUI):
            curses.wrapper(self.curses_loop)
        else:
            self.menu_loop()

    def curses_loop(self, stdscr):
        self.view.init_curses(stdscr)
        self.menu_loop()

    def update_game_state(self, action):
        check = False

        self.game.state.reset_states()

        if action == 'exit':
            self.game.state.game_state = 'exit'
            SaveManager.save(self.game.player.name, self.game)
            return self.game.state

        if action in ['left', 'right', 'up', 'down']:
            self.move_player(action)
            check = True
        elif action == 'weapon':
            self.use_item('weapon')
        elif action == 'food':
            self.use_item('food')
        elif action == 'scroll':
            self.use_item('scroll')
        elif action == 'potion':
            self.use_item('potion')

        if check:
            if self.game.is_player_at_exit():
                if self.game.level == 21:
                    self.game.state.game_state = 'win'
                else:
                    self.view.clear()
                    self.game.gen_next_floor()
                    SaveManager.save(self.game.player.name, self.game)
            else:
                for enemy in self.game.enemies:
                    enemy.make_action(self.game.map_grid, self.game.player, self.game.floor.rooms[enemy.current_room_id])

            self.game.player.update_timers()
            
            if self.game.player.health <= 0:
                self.game.state.game_state = 'game_over'
            self.game.map_grid = self.game.create_map_grid()

        time.sleep(0.05)
        return self.game.state

    def game_loop(self):
        action = 'start'
        self.update_game_state(action)
        while True:
            try:
                # self.view.clear()
                self.view.draw_world()
                self.view.print_state(action)
                # self.view.draw_statistic()
                action = self.view.handle_input()
                state = self.update_game_state(action)
                if state.game_state == 'exit':
                    self.view.clear()
                    return
                elif state.game_state == 'game_over':
                    break
                elif state.game_state == 'win':
                    break
                elif state.item in ['weapons', 'food', 'scrolls', 'potions']:
                    self.inventory_loop(state.item)
            except curses.error:
                self.view.print_curses_error()

        if state.game_state in ['win', 'game_over']:
            SaveManager.SCOREBOARD(self.game.player.name, self.game)
            if os.path.isfile(f"datalayer/saves/{self.game.player.name}.json"):
                os.remove(f"datalayer/saves/{self.game.player.name}.json")

            if state.game_state == 'win':
                self.view.draw_win()
            elif state.game_state == 'game_over':
                self.view.draw_game_over(state)
