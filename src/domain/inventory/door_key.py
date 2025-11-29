from domain.inventory.item import Item


class DoorKey(Item):
    colors_list = ['Red', 'Green', 'Blue']

    def __init__(self, y, x, color):
        super().__init__(y, x, f"{color} Key", color)
        self.color = color
        # self.item_type = f"{random_color} Key"
