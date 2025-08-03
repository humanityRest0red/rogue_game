HEIGHT = 22
WIDTH = 80


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Player:
    def __init__(self, name, current_room=0):
        self.position = Point(5, 5)
        self.current_room = current_room
        self.name = name
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


class Room:
    def __init__(self, left=0, top=0, right=10, bottom=8):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top


class Dungeon:
    def __init__(self, level=1):
        self.level = level
        self.rooms = []

    def add_room(self, room: Room):
        self.rooms.append(room)


# class GameState:
#     def __init__(self):
#         self.player = Player("Hero")
