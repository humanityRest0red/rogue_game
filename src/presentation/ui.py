import curses
import time
from domain.entities import WIDTH, HEIGHT, CellType


class GameUI:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        screen = curses.initscr()
        curses.wrapper(self.main_loop)

    def main_loop(self, screen):
        curses.curs_set(0)
        # screen.resize(HEIGHT, WIDTH)
        while True:
            try:
                screen.clear()

                self.print_action(screen)

                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        map_grid = self.controller.game.dungeon.map_grid
                        if map_grid[i][j] == CellType.FLOOR:
                            screen.addch(i + 1, j, '#')
                        if map_grid[i][j] == CellType.ENTRY:
                            screen.addch(i + 1, j, '/')
                        if map_grid[i][j] == CellType.WALL:
                            screen.addch(i + 1, j, '.')
                self.print_status(screen)

                screen.addch(self.controller.game.player.position.y + 1, self.controller.game.player.position.x, '@')

                ch = screen.getch()
                if ch == ord('q'):
                    break
                elif ch == ord('w') or ch == ord('W'):
                    self.controller.move_player('up')
                elif ch == ord('s') or ch == ord('S'):
                    self.controller.move_player('down')
                elif ch == ord('a') or ch == ord('A'):
                    self.controller.move_player('left')
                elif ch == ord('d') or ch == ord('D'):
                    self.controller.move_player('right')
            except curses.error:
                screen.clear()
                message = f'\tResize your screen to at least {HEIGHT}x{WIDTH}'
                screen.addstr(0, 0, message)
                screen.refresh()
                time.sleep(0.5)

    def print_action(self, screen):
        screen.addstr(0, 1, 'place holding')

    def print_status(self, screen):
        screen.addstr(HEIGHT + 1, 1, f'Level: {self.controller.game.dungeon.level}\t'
                                 f'Gold: 35\t'
                                 f'Hp: {self.controller.game.player.health}'
                                 f'({self.controller.game.player.max_health})')
