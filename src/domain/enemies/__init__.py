from domain.enemies.enemy import Enemy
from domain.enemies.zombie import Zombie
from domain.enemies.vampire import Vampire
from domain.enemies.ghost import Ghost
from domain.enemies.ogre import Ogre
from domain.enemies.snake_wizard import SnakeWizard
from domain.enemies.mimic import Mimic

from random import choice, randint

enemy_classes = {
    'Zombie': Zombie,
    'Vampire': Vampire,
    'Ghost': Ghost,
    'Ogre': Ogre,
    'Snake Wizard': SnakeWizard,
    'Mimic': Mimic
    }

def spawn(room):
    enemy_type = choice(list(enemy_classes.keys()))
    klass = enemy_classes[enemy_type]
    x = randint(room.x, room.x_)
    y = randint(room.y, room.y_)
    enemy = klass(y, x, room.id)
    return enemy

Enemy.spawn = spawn