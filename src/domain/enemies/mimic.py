from random import choice

from domain.enemies.enemy import Enemy
from domain.inventory.item import Item


class Mimic(Enemy):
    """
    Мимик (белая m) - который имитирует предметы. Высокая ловкость, низкая сила, высокое здоровье и низкая враждебность.
    """
    def __init__(self, y, x, current_room_id):
        super().__init__(
            y=y, x=x, name='Mimic',
            current_room_id = current_room_id,
            agility=Enemy.agility['HIGH'],
            strength=Enemy.strength['LOW'],
            hostility=Enemy.hostility['LOW'],
            health=Enemy.health['HIGH'],
            experience=3
        )
        self.view = choice(Item.type)
        self.name = self.view

    def move(self, map_grid, player, room):
        path = self.find_shortest_path(map_grid, player)
        if not path is None and len(path) <= self.hostility:
            self.x, self.y = path[0]
            self.name = 'Mimic'
        else:
            self.name = self.view
