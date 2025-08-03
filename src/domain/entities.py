HEIGHT = 22
WIDTH = 80


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Player:
    def __init__(self, name):
        self.name = name
        self.position = Point(15, 15)
        self.max_health = 25
        self.health = self.max_health
        self.agility = 10


class Enemy:
    def __init__(self, type_, health, agility, strength, hostility):
        self.position = Point()
        self.type = type_
        self.health = health
        self.agility = agility
        self.strength = strength
        self.hostility = hostility


class Zombie(Enemy):
    def __init__(self):
        super().__init__(type_='Zombie', health=50, agility=10, strength=15, hostility=0)


class Map:
    def __init__(self):
        self.left_board = 10
        self.right_board = 20
        self.up_board = 10
        self.down_board = 20


# class GameState:
#     def __init__(self):
#         self.player = Player("Hero")
