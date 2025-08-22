import pygame

from view.pygame_view_3d.settings import *
from domain.setting import WIDTH_MAP, HEIGHT_MAP
SHIFT_X = WIDTH_SCREEN // 2
SHIFT_Y = HEIGHT_SCREEN * 4 // 5

class MiniMap():
    def __init__(self, screen):
        self.screen = screen

    def draw(self, game, player_angle) -> None:
        pygame.draw.rect(
                self.screen,
                BLACK,
                (SHIFT_X, SHIFT_Y, MINI_MAP_COEF * WIDTH_MAP, MINI_MAP_COEF * HEIGHT_MAP)
            )
        pygame.draw.rect(
                self.screen,
                WHITE,
                (SHIFT_X, SHIFT_Y, MINI_MAP_COEF * WIDTH_MAP, MINI_MAP_COEF * HEIGHT_MAP), 1
            )
        # self.draw_health_bar(game.player, MINI_MAP_COEF * WIDTH_MAP + 5, 5)


        for y in range(HEIGHT_MAP):
            for x in range(WIDTH_MAP):
                cell = game.map_grid[y][x]
                if game.map_grid[y][x].is_wall():
                    self.draw_actor(y, x, BROWN)
                elif cell.value in ['Door', 'Floor']:
                    self.draw_actor(y, x, WHITE)
                elif cell.value == 'Red Door':
                    self.draw_actor(y, x, RED)
                elif cell.value == 'Green Door':
                    self.draw_actor(y, x, GREEN)
                elif cell.value == 'Blue Door':
                    self.draw_actor(y, x, BLUE)
                elif cell.value == 'Zombie':
                    self.draw_actor(y, x, GREEN, width=3)
                elif cell.value == 'Vampire':
                    self.draw_actor(y, x, RED, width=3)
                elif cell.value == 'Ghost':
                    self.draw_actor(y, x, WHITE, width=3)
                elif cell.value == 'Ogre':
                    self.draw_actor(y, x, YELLOW, width=3)
                elif cell.value == 'Snake Wizard':
                    self.draw_actor(y, x, WHITE, width=3)
                elif cell.value == 'Mimic':
                    self.draw_actor(y, x, WHITE, width=3)
                
                
                elif cell.value == 'Food':
                    self.draw_item(y, x, RED, width=3)
                elif cell.value == 'Potion':
                    self.draw_item(y, x, VIOLET, width=3)
                elif cell.value == 'Scroll':
                    self.draw_item(y, x, BROWN, width=3)
                elif cell.value == 'Weapon':
                    self.draw_item(y, x, WHITE, width=3)
                
                elif 'Key' in cell.value:
                    self.draw_key(y, x, cell.value, width=3)

                elif cell.value == 'Exit':
                    self.draw_item(y, x, GREEN, width=3)

        self.draw_player(game.player, player_angle)


    def draw_health_bar(self, player, x, y) -> None:
        hp_percent = player.health / player.max_health
        pygame.draw.rect(
                self.screen,
                RED,
                (x, y,
                5 * 100,
                MINI_MAP_COEF * 2),
                0
        )

        pygame.draw.rect(
                self.screen,
                GREEN,
                (x, y,
                5 * 100 * hp_percent,
                MINI_MAP_COEF * 2),
                0
        )


    def draw_player(self, player, player_angle):
        self.draw_actor(player.y, player.x, YELLOW, 3)

        start_x = SHIFT_X + player.x * MINI_MAP_COEF + MINI_MAP_COEF / 2
        start_y = SHIFT_Y + player.y * MINI_MAP_COEF + MINI_MAP_COEF / 2
        end_x = start_x + MINI_MAP_COEF * math.cos(player_angle)
        end_y = start_y + MINI_MAP_COEF * math.sin(player_angle)
        pygame.draw.line(
            self.screen,
            YELLOW,
            (start_x, start_y),
            (end_x, end_y),
            1
        )

    def draw_actor(self, y, x, color, width=1):
        pygame.draw.rect(
                self.screen,
                color,
                (SHIFT_X + x * MINI_MAP_COEF, SHIFT_Y + y * MINI_MAP_COEF, MINI_MAP_COEF, MINI_MAP_COEF),
                width
            )

    def draw_item(self, y, x, color, width=1):
        pygame.draw.circle(
                self.screen,
                color,
                (SHIFT_X + (x + 0.5) * MINI_MAP_COEF, SHIFT_Y + (y + 0.5) * MINI_MAP_COEF),
                MINI_MAP_COEF * 0.5,
                width
            )
        
    def draw_key(self, y, x, key, width=1):
        if key == 'Red Key':
            color = RED
        elif key == 'Green Key':
            color = GREEN
        else:
            color = BLUE

        triangle_points = [(SHIFT_X + x * MINI_MAP_COEF, SHIFT_Y + (y - 0.5) * MINI_MAP_COEF),
                            (SHIFT_X + x * MINI_MAP_COEF, SHIFT_Y + (y + 0.5) * MINI_MAP_COEF),
                            (SHIFT_X + (x + 0.5) * MINI_MAP_COEF, SHIFT_Y + y * MINI_MAP_COEF),
                            ]
        pygame.draw.polygon(
                self.screen,
                color,
                triangle_points,
                width
            )