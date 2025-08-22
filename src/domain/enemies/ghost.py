from random import randint, random

from domain.enemies.enemy import Enemy
from domain.setting import GHOST_UNSEE_PERCENT_CHANCE

class Ghost(Enemy):
    '''
    Привидение (отображение: белый g): высокая ловкость; низкая сила, враждебность и здоровье.
    Постоянно телепортируется по комнате и периодически становится невидимым, пока игрок не вступил в бой.
    '''

    def __init__(self, y, x, current_room_id):
        super().__init__(
            y=y, x=x, name='Ghost',
            current_room_id = current_room_id,
            agility=Enemy.agility['HIGH'],
            strength=Enemy.strength['LOW'],
            hostility=Enemy.hostility['LOW'],
            health=Enemy.health['LOW'],
            experience=2
        )

    def chase_player(self, next_cell):
        self.name = 'Ghost'
        super().chase_player(next_cell)

    def pattern_move(self, room):
        self.y = randint(room.y, room.y_)
        self.x = randint(room.x, room.x_)
        if random() < GHOST_UNSEE_PERCENT_CHANCE / 100:
            self.name = "Ghost"
        else:
            self.name = "Unseen Ghost"