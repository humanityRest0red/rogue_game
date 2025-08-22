import pygame
import random
import time

from domain.enemies import Enemy
from domain.game_logic import Game

DIR = './view/pygame_view_3d/sounds'


class Sound():
    def __init__(self):
        random.seed(time.time())
        pygame.mixer.init()
        self.zombie_attack = pygame.mixer.Sound(f"{DIR}/zombie_attack.mp3")

        Enemy.attack = self.enemy_attack_wrapper(Enemy.attack, self)
        Game.gen_next_floor = self.gen_next_floor_wrapper(Game.gen_next_floor, self)

        pygame.mixer.music.load(f"{DIR}/menu.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()

    def gen_next_floor_wrapper(self_method, method, sound):
        def wrapped(*args, **kwargs):
            pygame.mixer.music.stop()
            num = random.randint(1, 7)
            pygame.mixer.music.load(f"{DIR}/level{num}.mp3") 
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play()

            result = method(*args, **kwargs)

            return result
        return wrapped

    def enemy_attack_wrapper(self_method, method, sound):
        def wrapped(self, player):
            # is_ogre_resting = self.name == 'Ogre' and self.is_resting

            damage, i = method(self, player)
            if self.name == "Zombie" and (i == 1 or i == 2):
                sound.zombie_attack.play()
                    # else:
            #     state.enemy = f'{self.name} scored an excellent hit on you for {damage} damage'
            
            # if is_ogre_resting:
            #     state.enemy = f'Ogre is resting for one move'
            # if self.name == 'Snake Wizard' and player.is_sleeping:
            #     pass
            
            return damage, i
        return wrapped