from abc import ABC, abstractmethod

from domain.setting import WIDTH_MAP, HEIGHT_MAP
from datalayer.load_manager import LoadManager
from view.curses_view.utils import get_map_case


class AbstractGameUI(ABC):
    def __init__(self, controller):
        self.controller = controller
        self.screen = None
        
    @abstractmethod
    def draw_game_entity(self, y, x, string, color):
        pass

    @abstractmethod
    def draw_world(self):
        pass

    @abstractmethod
    def draw_map(self):
        pass

    @abstractmethod
    def draw_player(self):
        pass
        
    @abstractmethod
    def draw_screen_with_frame(self, message_lines):
        pass
        
    @abstractmethod
    def update_screen(self) -> None:
        pass

    @abstractmethod
    def get_key(self):
        pass

    @abstractmethod
    def press_key(self):
        pass

    @abstractmethod
    def get_action(self, ch):
        pass 
    
    @abstractmethod
    def draw_start_menu(self, menu_line) -> None:
        # self.clear()
        LSWITCH, RSWITCH, EMPTY = "<<<", ">>>", "   "
        switcher = {key: (EMPTY, EMPTY) for i, key in enumerate(range(0, 4))}
        switcher[menu_line] = (LSWITCH, RSWITCH)

        message_lines = [
            "",
            "",
            "           GAME  MENU           ",
            "--------------------------------",
            "                                ",
            "                                ",
            f"     {switcher[0][0]}   NEW   GAME   {switcher[0][1]}     ",
            f"     {switcher[1][0]}   LOAD  GAME   {switcher[1][1]}     ",
            f"     {switcher[2][0]}   SCOREBOARD   {switcher[2][1]}     ",
            f"     {switcher[3][0]}   EXIT  GAME   {switcher[3][1]}     ",
            "                                ",
            "                                ",
            "",
            "",
        ]
        self.draw_screen_with_frame(message_lines)
        
    @abstractmethod
    def choose_from_inventory(self, items, title, show_current=None, mode="use", item_type=None):
        if show_current is not None:
            if show_current:
                self.log_event(1, 0, f'Current: {show_current.subtype}')
            else:
                self.log_event(1, 0, 'Current: None')
            start_line = 3
        else:
            self.log_event(1, 0, title)
            start_line = 2

        if item_type == 'potion':
            for i, item in enumerate(items, start=1):
                self.log_event(start_line + i, 0, f'{i}. {item.subtype} {item.strength_label}')
        else:
            for i, item in enumerate(items, start=1):
                self.log_event(start_line + i, 0, f'{i}. {item.subtype}')

        self.log_event(start_line + len(items) + 2, 0,
                        f"Mode: {mode.upper()}  |  Press D to toggle mode  |  Press Q to cancel")
        self.update_screen()
            
    @abstractmethod
    def print_state(self, action) -> None:
        if action == 'start':
            msg = f"Hello, {self.controller.game.player.name}, Welcome to the Dungeons of Doom!"
        else:
            state = self.controller.game.state
            msg = f"{state.player}\n{state.enemy}\n{state.item}".strip()
        self.log_event(0, 0, msg)
        if self.controller.game.player.weapon:
            strength_weapon = self.controller.game.player.weapon.amount
        else:
            strength_weapon = 0
        msg = (f'Level:{self.controller.game.level}    '
                                 f'Hits:{self.controller.game.player.health}'
                                 f'({self.controller.game.player.max_health})   '
                                 f'Str:{self.controller.game.player.strength}'
                                 f'({strength_weapon})   '
                                 f'Gold:{self.controller.game.player.gold}    '
                                 f'Exp:{self.controller.game.player.experience_level}'
                                 f'/{self.controller.game.player.experience}   '
                                 f'    Keys: ')
        self.log_event(HEIGHT_MAP, 1, msg)
        for i, key in enumerate(self.controller.game.player.inventory.doorkeys, start=len(msg) + 1):
            self.log_event(HEIGHT_MAP, i, get_map_case(key.type)[0], get_map_case(key.type)[1])
    
    @abstractmethod
    def draw_win(self):
        self.clear()
        full_message = "ПОздаравалялавлаям хэндл"
        start_y = (HEIGHT_MAP - len(full_message)) // 2
        # start_x = (WIDTH_MAP) // 2  # +2 для рамки
        self.log_event(start_y, 0, full_message)

        self.log_event(start_y + 5, 0, '[Press any key to rankings]')
        self.handle_input()


    @abstractmethod
    def show_no_saves(self):
        message_lines = [
            "",
            "",
            "      No saved games       ",
            "--------------------------------",
            "",
            "   [Press any key to exit]   ",
            "",
            ""
        ]
        self.draw_screen_with_frame(message_lines)

    @abstractmethod
    def show_load_menu(self, saves, selected):
        message_lines = [
            "",
            "",
            "      SAVE CHOICE           ",
            "--------------------------------",
        ]

        for i, save_file in enumerate(saves):
            marker_left = ">>" if i == selected else "  "
            marker_right = "<<" if i == selected else "  "
            message_lines.append(f"   {marker_left} {save_file[:-5]} {marker_right}   ")

        message_lines += [
            "",
            "   Enter - load, Q - cancel   ",
            "",
            ""
        ]

        self.draw_screen_with_frame(message_lines)

    @abstractmethod
    def draw_game_over(self, state):
        self.clear()
        message_lines = [
            "",
            "",
            "R E S T",
            "I N",
            "P E A C E",
            "",
            f"{self.controller.game.player.name}",
            "killed by a",
            f"{state.killed_by}".lower(),
            "",
            f"{self.controller.game.player.gold} Au",
            "2025",
            "",
            ""
        ]

        self.draw_screen_with_frame(message_lines)

        self.log_event(HEIGHT_MAP - 2, 0, '[Press Enter to rankings]')
        self.handle_input()

    @abstractmethod
    def draw_name_input(self):
        name = ""
        max_name_length = 12

        while True:

            textbox = f"[ {name:<{max_name_length}} ]"

            message_lines = [
                "",
                "",
                "           ENTER  NAME           ",
                "--------------------------------",
                "                                ",
                "                                ",
                f"        {textbox}        ",
                "                                ",
                "   Press ENTER to confirm       ",
                "",
                "",
            ]

            self.draw_screen_with_frame(message_lines)

            key = self.get_key()

            if key == '\n':
                if name.strip():
                    break
            elif key == '\x7f':
                name = name[:-1]
            elif len(name) < max_name_length and len(key) == 1 and key.isprintable():
                name += key

        return name


    @abstractmethod
    def show_empty_scoreboard(self):
        message_lines = [
            "",
            "",
            "      SCOREBOARD       ",
            "--------------------------------",
            "",
            "   [Press any key to exit]   ",
            "",
            ""
        ]
        self.draw_screen_with_frame(message_lines)
        
    
    @abstractmethod
    def scoreboard_loop(self) -> None:
        saves = LoadManager.SCOREBOARD_LOAD()

        if not saves:
            self.show_empty_scoreboard()
            self.handle_input()
            return

        saves.sort(key=lambda r: (not r["is_win"], -r["gold"]))

        while True:
            self.show_scoreboard()
            action = self.handle_input()
            if action == 'exit':
                return
    
    @abstractmethod
    def show_scoreboard(self) -> None:
        saves = LoadManager.SCOREBOARD_LOAD()
        message_lines = [
            "",
            "",
            "      SCOREBOARD       ",
            "--------------------------------",
        ]

        header = (
            f"{'Player':<10} | {'Lvl':<3} | {'Dung':<4} | {'Gold':<5} | "
            f"{'Enemies':<7} | {'Food':<4} | {'Potions':<7} | {'Scrolls':<7} | "
            f"{'Dealt':<5} | {'Taken':<5} | {'Cells':<6} | {'Status':<8}"
        )
        message_lines.append(header)
        message_lines.append("-" * len(header))

        for record in saves:
            status = "Winner" if record["is_win"] else "GameOver"
            line = (
                f"{record['player']:<10} | {record['level_player']:^3} | {record['level_dugeon']:^4} | {record['gold']:^5} | "
                f"{record['enemies_killed']:^7} | {record['food_used']:^4} | {record['potions_used']:^7} | {record['scrolls_used']:^7} | "
                f"{record['damage_dealt']:^5} | {record['damage_taken']:^5} | {record['cells_passed']:^6} | {status:^8}"
            )
            message_lines.append(line)

        message_lines += [
            "",
            "   Q — exit   ",
            "",
            ""
        ]

        self.draw_screen_with_frame(message_lines)

    @abstractmethod
    def draw_statictic(self ,conttroler):
        state = conttroler.controller.game.state
        game = conttroler.controller.game
        dif = conttroler.controller.game.difficulty_adjuster
        self.log_event(HEIGHT_MAP + 3, 1, f'enemy_spawn_chance: {dif.enemy_spawn_chance}')
        self.log_event(HEIGHT_MAP + 4, 1, f'enemy_difficulty: {dif.enemy_difficulty}')
        self.log_event(HEIGHT_MAP + 5, 1, f'item_spawn_chance: {dif.item_spawn_chance}')
        self.log_event(HEIGHT_MAP + 6, 1, f'count_items: {len(game.items)}')
        self.log_event(HEIGHT_MAP + 7, 1, f'count_eneymis: {len(game.enemies)}')

        self.log_event(HEIGHT_MAP + 8, 1, f'potions: {state.potions_used}')
        self.log_event(HEIGHT_MAP + 9, 1, f'scrolls: {state.scrolls_used}')
        self.log_event(HEIGHT_MAP + 10, 1, f'food: {state.food_used}')
        self.log_event(HEIGHT_MAP + 11, 1, f'hp_percent: {state.player_hp_percent}')
        self.log_event(HEIGHT_MAP + 12, 1, f'damage_taken: {state.damage_taken}')
        self.log_event(HEIGHT_MAP + 13, 1, f'damage_dealt: {state.damage_dealt}')
        self.log_event(HEIGHT_MAP + 14, 1, f'enemies_killed: {state.enemies_killed}')
        self.log_event(HEIGHT_MAP + 15, 1, f'cells_passed: {state.cells_passed}')
        self.log_event(HEIGHT_MAP + 11, 1, f'keys on floor: {len(game.keys)}')
