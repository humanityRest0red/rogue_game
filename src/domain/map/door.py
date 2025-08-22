from random import choice

class Door:
    def __init__(self, y: int, x: int, room_id: int, room_side: str):
        self.y = y
        self.x = x
        self.room_id = room_id
        self.side = room_side
        self.color = 'White'