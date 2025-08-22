import pygame
from math import pi, cos, sin

from view.abstract_ui import AbstractGameUI
from view.pygame_view_3d.settings import *
from view.pygame_view_3d.mini_map import MiniMap
from view.pygame_view_3d.texture import Texture
from view.pygame_view_3d.sound import Sound
from domain.cell import Cell
from domain.setting import HEIGHT_MAP, WIDTH_MAP
from domain.enemies import Enemy

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

dir_arr = ['up', 'right', 'down', 'left']

class GameUI3D(AbstractGameUI):
    def __init__(self, controller):
        self.controller = controller
        self.player_angle: float = 3 * pi / 2
        self.direction = UP

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
        self.mini_map = MiniMap(self.screen)

        pygame.display.set_caption("Бандит")

        self.font = pygame.font.Font(None, 36)  # None — шрифт по умолчанию, 36 — размер
        self.sound = Sound()
        self.texture = Texture(self.screen)
    
    def draw_map(self):
        pass

    def draw_player(self):
        pass
        
    def press_key(self):
        pass
        
    def get_action(self):
        pass
    
    def draw_game_entity(self):
        pass

    def update_screen(self):
        pygame.display.flip()

    def scoreboard_loop(self) -> None:
        super().scoreboard_loop()

    def draw_load_menu(self, saves, selected) -> None:
        super().draw_load_menu(saves, selected)

    def show_empty_scoreboard(self) -> None:
        super().show_empty_scoreboard()

    def show_load_menu(self, saves, selected) -> None:
        super().show_load_menu(saves, selected)

    def show_no_saves(self) -> None:
        super().show_no_saves()

    def show_scoreboard(self) -> None:
        super().show_scoreboard()

    def draw_game_over(self, state) -> None:
        super().draw_game_over(state)

    def draw_start_menu(self, menu_line) -> None:
        super().draw_start_menu(menu_line)

    def choose_from_inventory(self, items, title, show_current=None, mode="use"):
        super().choose_from_inventory(items, title, show_current=None, mode="use")
    
    def print_state(self, action) -> None:
        super().print_state(action)

    def draw_win(self) -> None:
        super().draw_win()
    
    def draw_statictic(self) -> None:
        super().draw_statictic()

    def scoreboard_game_menu(self) -> None:
        super().scoreboard_game_menu()

    def draw_name_input(self) -> str:
        return super().draw_name_input()

    def print_state(self, action):
        super().print_state(action)
    
    def log_event(self, y, x, string, color=WHITE):
        text_surface = self.font.render(string, True, (color))
        self.screen.blit(text_surface, (x * 20, y * 30))
        self.update_screen()
   
    def get_key(self):
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return "\x7f"
            elif event.key == pygame.K_RETURN:
                return "\n"
            else:
                return event.unicode
        return "" 

    def draw_start_menu(self, menu_line):
        message_lines = super().draw_start_menu(menu_line)
        self.draw_screen_with_frame (message_lines)

    def draw_screen_with_frame(self, message_lines) -> None:
        self.clear()
        if not message_lines:
            return

        screen_width = WIDTH_SCREEN
        screen_height = HEIGHT_SCREEN

        text_surfaces = [self.font.render(line, True, WHITE) for line in message_lines]
        max_width = max(surf.get_width() for surf in text_surfaces)
        total_height = sum(surf.get_height() for surf in text_surfaces) + (len(message_lines) - 1) * 10

        start_x = (screen_width - max_width) // 2
        start_y = (screen_height - total_height) // 2

        current_y = start_y
        for surf in text_surfaces:
            text_x = (screen_width - surf.get_width()) // 2
            self.screen.blit(surf, (text_x, current_y))
            current_y += surf.get_height() + 10

        pygame.display.flip()


    def draw_world(self):
        self.clear()
        self.draw_floor()
        self.ray_casting()
        self.mini_map.draw(self.controller.game, self.player_angle)
        # self.draw_floor()
        pygame.display.flip()

    def clear(self):
        self.screen.fill(CEILURE)

    def draw_floor(self):
        pygame.draw.rect(self.screen,
                    FLOOR,
                    (0,
                    HEIGHT_SCREEN // 2,
                    WIDTH_SCREEN,
                    HEIGHT_SCREEN // 2))

    def handle_input(self):
        while True:
            event = pygame.event.wait()
        # for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    return dir_arr[self.direction]

                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    return dir_arr[(self.direction + 2) % 4]

                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.direction = (self.direction - 1) % 4
                    self.player_angle -= pi / 2
                    return ""
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.direction = (self.direction + 1) % 4
                    self.player_angle += pi / 2
                    return ""
                elif event.key == pygame.K_RETURN:
                    return 'apply'
                
                elif event.key == pygame.K_q:
                    return 'exit'
                
                elif event.key == pygame.K_e:
                    return 'scroll'
                
                elif event.key == pygame.K_h:
                    return 'weapon'
                
                elif event.key == pygame.K_j:
                    return 'food'
                
                elif event.key == pygame.K_k:
                    return 'potion'
                # else:
                    # return ""
        # return None


    def handle_inventory_input(self):
         while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    return "up"
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    return "down"
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    return "toggle"
                elif event.key == pygame.K_q:
                    return "exit"
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    number = event.key - pygame.K_0
                    return str(number)
                else:
                    return ""


    def ray_casting(self):
        cur_angle = self.player_angle - HALF_FOV
        xp = self.controller.game.player.x
        yp = self.controller.game.player.y

        xo = self.controller.game.player.x + 0.5
        yo = self.controller.game.player.y + 0.5
        for ray in range(NUM_RAYS):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            for depth in range(MAX_DEPTH):
                x = int(xo + depth * cos_a)
                y = int(yo + depth * sin_a)

                if not (0 <= x < WIDTH_MAP and 0 <= y < HEIGHT_MAP):
                    break

                corrected_depth = depth * math.cos(self.player_angle - cur_angle)
                proj_height = min(PROJ_COEFF / (corrected_depth + 0.0001), HEIGHT_SCREEN)

                cell = self.controller.game.map_grid[y][x]
                if cell.is_wall() or cell.is_door() or cell in [Cell.map_, Cell.exit_]:
                    if cell.is_wall() or cell == Cell.map_:
                        color = WALL
                    elif cell == Cell.door:
                        if xp == x and yp == y:
                            color = WHITE
                            continue
                        else:
                            color = BLACK
                    elif cell == Cell.door_red:
                        color = RED
                    elif cell == Cell.door_green:
                        color = GREEN
                    elif cell == Cell.door_blue:
                        color = BLUE
                    elif cell == Cell.exit_:
                        color = GREEN
                    self.draw_cube(corrected_depth, proj_height, ray, color)
                    break
                elif cell.value in ['Zombie', 'Vampire', 'Ghost', 'Ogre', 'Snake Wizard', 'Mimic',
                'Potion', 'Weapon', 'Food', 'Scroll',
                'Red Key', 'Green Key', 'Blue Key']:
                    self.entity_tracing(y, x, cell.value)
                    # break
            cur_angle += DELTA_ANGLE
    
    
    def draw_cube(self, corrected_depth, proj_height, ray, color):
        c_r = color[0] / (1 + corrected_depth * corrected_depth * 0.0001)
        c_g = color[1] / (1 + corrected_depth * corrected_depth * 0.0001)
        c_b = color[2] / (1 + corrected_depth * corrected_depth * 0.0001)

        col = (
            max(0, min(255, int(c_r))),
            max(0, min(255, int(c_g))),
            max(0, min(255, int(c_b)))
        )

        pygame.draw.rect(self.screen,
                        col,
                        (ray * SCALE,
                        HEIGHT_SCREEN // 2 - proj_height // 2,
                        SCALE,
                        proj_height)
                        )
        

    def entity_tracing(self, y, x, entity):
        enemy_x = x
        enemy_y = y

        dx = enemy_x - self.controller.game.player.x
        dy = enemy_y - self.controller.game.player.y

        distance = math.hypot(dx, dy)
        angle_to_enemy = math.atan2(dy, dx)

        delta_angle = angle_to_enemy - self.player_angle
        delta_angle %= 2 * math.pi
        
        if delta_angle > math.pi:
            delta_angle -= 2 * math.pi
        if abs(delta_angle) > HALF_FOV:
            return

        ray_index = int((delta_angle + HALF_FOV) / FOV * NUM_RAYS)

        proj_height = min(PROJ_COEFF / (distance + 0.0001), HEIGHT_SCREEN)

        self.texture.draw(distance, proj_height, ray_index, entity)

