import curses
import time

from domain.setting import WIDTH_MAP, HEIGHT_MAP
from view.curses_view.utils import Color, get_map_case, KEYS
from view.abstract_ui import AbstractGameUI


class GameUI(AbstractGameUI):
    def __init__(self, controller):
        self.controller = controller
        self.screen = None

    def init_curses(self, stdscr):
        self.screen = stdscr
        self.clear()
        self.screen.keypad(True)
        self.set_colors()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.cbreak()
        curses.noecho()

    def draw_world(self) -> None:
        self.clear()
        self.draw_map()
        self.draw_player()
        self.update_screen()

    def draw(self, y, x, string, color=Color.WHITE):
        self.screen.clrtoeol()
        self.screen.addstr(y + 1, x, string, curses.color_pair(color))

    def handle_input(self):
        while True:
            action = self.get_action(self.press_key())
            curses.flushinp()
            if action:
                return action

    def handle_inventory_input(self):
        command = ""
        ch = self.press_key()

        if isinstance(ch, int):
            if ch in KEYS['down']:  # стрелка вниз
                command = "down"
            elif ch in KEYS['up']:  # стрелка вверх
                command = "up"

        # если ch — строка
        elif ch in KEYS['exit']:
            command = "exit"
        elif ch in KEYS['toggle']:  # теперь работает D/d
            command = "toggle"
        elif ch in KEYS['down']:
            command = "down"
        elif ch in KEYS['up']:
            command = "up"
        elif ch.isdigit():
            command = ch

        return command

    def draw_game_entity(self, y, x, string, color) -> None:
        self.log_event(y + 1, x, string, color)

    def log_event(self, y, x, string, color=Color.WHITE) -> None:
        self.screen.addstr(y, x, string, curses.color_pair(color))

    def draw_map(self) -> None:
        for y in range(HEIGHT_MAP):
            for x in range(WIDTH_MAP):
                cell = self.controller.game.map_grid[y][x]
                char, color = get_map_case(cell.value)
                self.draw(y + 1, x, char, color)

    def draw_player(self) -> None:
        self.draw(self.controller.game.player.y + 1, self.controller.game.player.x, '@', Color.YELLOW)

    def press_key(self) -> str:
        return self.screen.get_wch()

    def clear(self) -> None:
        self.screen.clear()

    def update_screen(self) -> None:
        self.screen.refresh()

    def scoreboard_loop(self) -> None:
        super().scoreboard_loop()

    def show_load_menu(self, saves, selected) -> None:
        super().show_load_menu(saves, selected)

    def show_no_saves(self) -> None:
        super().show_no_saves()

    def draw_game_over(self, state) -> None:
        super().draw_game_over(state)

    def draw_start_menu(self, menu_line) -> None:
        super().draw_start_menu(menu_line)

    def choose_from_inventory(self, items, title, show_current=None, mode="use"):
        super().choose_from_inventory(items, title, show_current=show_current, mode=mode)

    def print_state(self, action) -> None:
        super().print_state(action)

    def draw_win(self) -> None:
        super().draw_win()

    def draw_statistics(self, controller) -> None:
        super().draw_statistics(controller)

    def show_scoreboard(self) -> None:
        super().show_scoreboard()

    def show_empty_scoreboard(self) -> None:
        super().show_empty_scoreboard()

    def draw_name_input(self) -> str:
        return super().draw_name_input()

    def draw_screen_with_frame(self, message_lines) -> None:
        # self.clear()

        max_content_width = max(len(line) for line in message_lines)
        padding = 8
        total_width = max_content_width + padding

        top_border = "╔" + "═" * total_width + "╗"
        bottom_border = "╚" + "═" * total_width + "╝"

        empty_line = "║" + " " * total_width + "║"

        content_lines = []
        for line in message_lines:
            padded_line = line.center(max_content_width)
            content_lines.append("║" + padded_line.center(total_width) + "║")

        full_message = [top_border, empty_line] + content_lines + [empty_line, bottom_border]

        start_y = (HEIGHT_MAP - len(full_message)) // 2
        start_x = (WIDTH_MAP - (total_width + 2)) // 2  # +2 для рамки

        for i, line in enumerate(full_message):
            self.log_event(start_y + i, start_x, line)

    def get_key(self) -> str:
        ch = self.press_key()
        if isinstance(ch, str):
            return ch
        elif isinstance(ch, int):
            if ch == curses.KEY_BACKSPACE:
                return "\x7f"
            elif ch in (curses.KEY_ENTER, 10, 13):
                return "\n"
        return ""

    @staticmethod
    def get_action(ch):
        keys = {
            'exit': ['q', 'Q', 'й', 'Й', '\x1b'],
            'apply': ['\n', curses.KEY_ENTER],
            'backspace': ['\x7f', curses.KEY_BACKSPACE],

            'up': ['w', 'W', 'ц', 'Ц', curses.KEY_UP],
            'down': ['s', 'S', 'ы', 'Ы', curses.KEY_DOWN],
            'left': ['a', 'A', 'ф', 'Ф', curses.KEY_LEFT],
            'right': ['d', 'D', 'в', 'В', curses.KEY_RIGHT],

            'scroll': ['e', 'E', 'у', 'У'],
            'weapon': ['h', 'H', 'р', 'Р'],
            'food': ['j', 'J', 'о', 'О'],
            'potion': ['k', 'K', 'л', 'Л']
        }

        for action, symbols in keys.items():
            if ch in symbols:
                return action
        return None

    @staticmethod
    def set_colors():
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(Color.GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(Color.RED, curses.COLOR_RED, -1)
        curses.init_pair(Color.WHITE, curses.COLOR_WHITE, -1)
        curses.init_pair(Color.YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(Color.GOLD, 226, -1)
        curses.init_pair(Color.BLUE, curses.COLOR_BLUE, -1)
        curses.init_pair(Color.wall, 166, -1)
        curses.init_pair(Color.corridor, curses.COLOR_WHITE, 8)
        curses.init_pair(Color.VIOLET, 5, -1)
        curses.init_pair(Color.GRAY, 137, -1)
        curses.init_pair(Color.exit_, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(69, 0, curses.COLOR_BLUE)

    def print_curses_error(self):
        self.clear()
        message = f'     Resize your screen to at least {HEIGHT_MAP}x{WIDTH_MAP}'
        self.log_event(0, 0, message)
        self.update_screen()
        time.sleep(0.5)
