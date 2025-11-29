from __future__ import annotations
import random

from domain.enemies.enemy import Enemy
from domain.setting import SNAKE_WIZARD_SLEEP_PERCENT_CHANCE


class SnakeWizard(Enemy):
    """
    Змей-маг (отображение: белая s): очень высокая ловкость. Ходит по карте по диагонали,
    постоянно меняя сторону. У каждой успешной атаки есть вероятность «усыпить» игрока
    на один ход. Высокая враждебность.
    """

    def __init__(self, y, x, current_room_id):
        super().__init__(
            y=y, x=x, name='Snake Wizard',
            current_room_id = current_room_id,
            agility=Enemy.agility['MAX'],
            strength=Enemy.strength['LOW'],
            hostility=Enemy.hostility['HIGH'],
            health=Enemy.health['LOW'],
            experience=2
        )
        self.y_direction = 'up'

    def pattern_move(self, room: Room):
        super().pattern_move(room)
        if self.y_direction == 'down':
            if self.y + 1 <= room.y_:
                self.y += 1
            self.y_direction = 'up'
        else:
            if self.y - 1 >= room.y:
                self.y -= 1
            self.y_direction = 'down'

    def attack(self, player: Player):
        if random.random() < SNAKE_WIZARD_SLEEP_PERCENT_CHANCE / 100:
            player.is_sleeping = True
        super().attack(player)
