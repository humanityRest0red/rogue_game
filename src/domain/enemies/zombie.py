from domain.enemies.enemy import Enemy

class Zombie(Enemy):
    '''
    Зомби (отображение: зеленый z): низкая ловкость; средняя сила, враждебность; высокое здоровье.
    '''

    def __init__(self, y, x, current_room_id):
        super().__init__(
            y=y, x=x, name='Zombie',
            current_room_id = current_room_id,
            agility=Enemy.agility['LOW'],
            strength=Enemy.strength['MID'],
            hostility=Enemy.hostility['MID'],
            health=Enemy.health['HIGH'],
            experience=1
        )
