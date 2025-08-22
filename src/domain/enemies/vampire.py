from domain.enemies.enemy import Enemy
from domain.setting import VAMPIRE_MAX_HEALTH_DAMAGING_PERCENT

class Vampire(Enemy):
    '''
    Вампир (отображение: красная v): высокая ловкость, враждебность и здоровье; средняя сила.
    Отнимает некоторое количество максимального уровня здоровья игроку при успешной атаке.
    Первый удар по вампиру — всегда промах.
    '''

    def __init__(self, y, x, current_room_id):
        super().__init__(
            y=y, x=x, name='Vampire',
            current_room_id = current_room_id,
            agility=Enemy.agility['HIGH'],
            strength=Enemy.strength['MID'],
            hostility=Enemy.hostility['HIGH'],
            health=Enemy.health['HIGH'],
            experience=2
        )
        self.shield = True

    def attack(self, player):
        strength_buffer = self.strength
        self.strength = int(player.max_health * VAMPIRE_MAX_HEALTH_DAMAGING_PERCENT / 100)

        damage, i = super().attack(player)

        self.strength = strength_buffer

        return damage, i
        
