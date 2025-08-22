from random import choice


class Exit:
    def __init__(self, player_spawn_room_id, rooms):
        possible_ids = [i for i in range(9) if i != player_spawn_room_id]
        self.id = choice(possible_ids)
        self.x = (rooms[self.id].x + rooms[self.id].x_) // 2
        self.y = (rooms[self.id].y + rooms[self.id].y_) // 2
        
    @classmethod
    def from_data(cls, data: dict) -> "Exit":
        exit = cls.__new__(cls)  # создаём без вызова __init__
        exit.id = data['id']
        exit.x = data['x']
        exit.y = data['y']
        return exit