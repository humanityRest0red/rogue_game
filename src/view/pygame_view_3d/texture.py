import pygame
import os

from view.pygame_view_3d.settings import RAY_WIDTH, HEIGHT_SCREEN 


class Texture:
    def __init__(self, screen):
        self.screen = screen

        self.images = {
            'Zombie': 'zombie.png',
            'Vampire': 'vampire.png',
            'Ghost': 'ghost.png',
            'Ogre': 'ogre.png',
            'Snake Wizard': 'snake_wizard.png',
            'Mimic': 'mimic.png',

            'Food': 'food.png',
            'Potion': 'potion.png',
            'Scroll': 'scroll.png',
            'Weapon': 'weapon.png',

            'Red Key': 'key_red.png',
            'Green Key': 'key_green.png',
            'Blue Key': 'key_blue.png',

            # 'wall.png'
            # 'floor.png'
        }

        for name in self.images:
            setattr(self, name, self.load_image(self.images[name]))

    @staticmethod
    def load_image(filename):
        textures_dir = './view/pygame_view_3d/textures'
        filepath = os.path.join(textures_dir, filename)
        return pygame.image.load(filepath).convert_alpha()

    def draw(self, proj_height, ray_index, entity):
        texture = getattr(self, entity)

        x_center = (ray_index + 0.5) * RAY_WIDTH
        y_center = HEIGHT_SCREEN / 2

        sprite_width = proj_height * texture.get_width() / texture.get_height()
        sprite_height = proj_height

        scaled_texture = pygame.transform.scale(texture, (int(sprite_width), int(sprite_height)))

        x1 = int(x_center - sprite_width / 2)
        y1 = int(y_center - sprite_height / 2)
        self.screen.blit(scaled_texture, (x1, y1))
