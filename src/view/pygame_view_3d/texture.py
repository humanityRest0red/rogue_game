import pygame

from view.pygame_view_3d.settings import RAY_WIDTH, HEIGHT_SCREEN 

DIR = './view/pygame_view_3d/textures'


class Texture():
    def __init__(self, screen):
        self.screen = screen

        self.ZOMBIE = pygame.image.load(f'{DIR}/zombie.png').convert_alpha()
        self.VAMPIRE = pygame.image.load(f'{DIR}/vampire.png').convert_alpha()
        self.GHOST = pygame.image.load(f'{DIR}/ghost.png').convert_alpha()
        self.OGRE = pygame.image.load(f'{DIR}/ogre.png').convert_alpha()
        self.SNAKE_WIZARD = pygame.image.load(f'{DIR}/snake_wizard.png').convert_alpha()
        self.MIMIC = pygame.image.load(f'{DIR}/mimic.png').convert_alpha()

        self.FOOD = pygame.image.load(f'{DIR}/food.png').convert_alpha()
        self.POTION = pygame.image.load(f'{DIR}/potion.png').convert_alpha()
        self.SCROLL = pygame.image.load(f'{DIR}/scroll.png').convert_alpha()
        self.WEAPON = pygame.image.load(f'{DIR}/weapon.png').convert_alpha()

        self.KEY_RED = pygame.image.load(f'{DIR}/key_red.png').convert_alpha()
        self.KEY_GREEN = pygame.image.load(f'{DIR}/key_green.png').convert_alpha()
        self.KEY_BLUE = pygame.image.load(f'{DIR}/key_blue.png').convert_alpha()

        # self.WALL = pygame.image.load(f'{DIR}/wall.png').convert_alpha()
        # self.FLOOR = pygame.image.load(f'{DIR}/floor.png').convert_alpha()

    def draw(self, distance, proj_height, ray_index, entity):
        if entity == 'Zombie':
            texture = self.ZOMBIE
        elif entity == 'Vampire':
            texture = self.VAMPIRE
        elif entity == 'Ghost':
            texture = self.GHOST
        elif entity == 'Ogre':
            texture = self.OGRE
        elif entity == 'Snake Wizard':
            texture = self.SNAKE_WIZARD
        elif entity == 'Mimic':
            texture = self.MIMIC

        elif entity == 'Food':
            texture = self.FOOD
        elif entity == 'Potion':
            texture = self.POTION
        elif entity == 'Scroll':
            texture = self.SCROLL
        elif entity == 'Weapon':
            texture = self.WEAPON

        elif entity == 'Red Key':
            texture = self.KEY_RED
        elif entity == 'Green Key':
            texture = self.KEY_GREEN
        elif entity == 'Blue Key':
            texture = self.KEY_BLUE

        x_center = (ray_index + 0.5) * RAY_WIDTH
        y_center = HEIGHT_SCREEN / 2

        sprite_width = proj_height * texture.get_width() / texture.get_height()
        sprite_height = proj_height

        x1 = int(x_center - sprite_width / 2)
        y1 = int(y_center - sprite_height / 2)

        scaled_texture = pygame.transform.scale(texture, (int(sprite_width), int(sprite_height)))

        self.screen.blit(scaled_texture, (x1, y1))