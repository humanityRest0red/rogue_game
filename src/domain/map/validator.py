from collections import deque

from domain.map.floor import Floor
from domain.inventory import DoorKey

class KeysValidator:
    """Проверяет возможность обхода всех комнат на уровне."""
    def __init__(self, floor: Floor, start_room_id: int, keys_on_map: list):
        self.floor = floor
        self.start_room_id = start_room_id
        self.rooms = floor.rooms
        self.door_map = floor.door_map
        self.keys_map = keys_on_map
        self.visited_rooms = set()
        self.available_keys = set()

    def bfs(self) -> bool:
        """
        Проверка связности уровня с помощью BFS.
        BFS (Breadth-First Search) - поиск в ширину: 
        алгоритм сначала исследует все соседние узлы текущего уровня, 
        прежде чем перейти к следующему уровню
        """
        queue = deque([self.start_room_id])
        self.visited_rooms.add(self.start_room_id)
        
        while queue:
            current_room_id = queue.popleft()
            
            for neighbor_id in self.door_map.get(current_room_id, {}):
                if neighbor_id not in self.visited_rooms:
                    # Проверяем доступность 2х дверей
                    door_color_out = self.door_map[current_room_id][neighbor_id]['color']
                    door_color_in = self.door_map[neighbor_id][current_room_id]['color']
                    if (door_color_out in self.available_keys and 
                        door_color_in in self.available_keys or 
                        door_color_out == door_color_in == 'White'):
                        self.visited_rooms.add(neighbor_id)
                        queue.append(neighbor_id)
                        # Добавляем ключи из соседней комнаты
                        self.available_keys.update(self.get_keys_from_room(neighbor_id))

        return len(self.visited_rooms) == len(self.rooms)


    def get_keys_from_room(self, room_id: int):
        room = self.floor.get_room_by_id(room_id)
        keys = set()
        for key in self.keys_map:
                if room.is_inside_the_room(key.y, key.x):
                    keys.add(key.color)
        return keys
