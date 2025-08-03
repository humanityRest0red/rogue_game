import curses
import time
from domain.entities import WIDTH, HEIGHT


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
                self.draw_board(self.controller.game.map, screen)
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

    def draw_board(self, board, screen):
        for i in range(board.left_board, board.right_board + 1):
            screen.addch(board.up_board + 1, i, '-')
            screen.addch(board.down_board + 1, i, '-')
        for j in range(board.up_board, board.down_board + 1):
            screen.addch(j + 1, board.left_board, '|')
            screen.addch(j + 1, board.right_board, '|')

    def print_action(self, screen):
        screen.addstr(0, 1, 'place holding')

    def print_status(self, screen):
        screen.addstr(HEIGHT, 1, f'Level: 1  Gold: 35\t'
                                 f'Hp: {self.controller.game.player.health}'
                                 f'({self.controller.game.player.max_health})')
