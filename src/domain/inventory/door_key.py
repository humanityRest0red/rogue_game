# from random import choice

from domain.inventory.item import Item


# class DoorKey(Item):
#     colors_list = ['Red', 'Green', 'Blue']
#     def __init__(self, y, x):
#         random_color = choice(DoorKey.colors_list)
#         super().__init__(y, x, "Door Key", random_color)
#         self.item_type = f"{random_color} Key"

class DoorKey(Item):
    colors_list = ['Red', 'Green', 'Blue']
    def __init__(self, y, x, color):
        super().__init__(y, x, f"{color} Key", color)
        self.color = color
        # self.item_type = f"{random_color} Key"