from domain.enemies.enemy import Enemy


class Ogre(Enemy):
    """
    Огр (отображение: желтый O): ходит по комнате на две клетки. Очень высокая сила и здоровье,
    но после каждой атаки отдыхает один ход, затем гарантированно контратакует;
    низкая ловкость; средняя враждебность.
    """

    def __init__(self, y, x, current_room_id):
        super().__init__(
            y=y, x=x, name='Ogre',
            current_room_id=current_room_id,
            agility=Enemy.agility['LOW'],
            strength=Enemy.strength['MAX'],
            hostility=Enemy.hostility['MID'],
            health=Enemy.health['MAX'],
            experience=3
        )
        self.is_resting = False

    def attack(self, player):
        if self.is_resting:
            self.is_resting = False
            return 0, 0

        damage, i = super().attack(player)
        self.is_resting = True

        return damage, i

    def pattern_move(self, room):
        super().pattern_move(room, step=2)
