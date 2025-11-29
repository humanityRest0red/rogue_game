from random import choice

from domain.inventory.item import Item
from domain.setting import FOOD_LOW, FOOD_MID, FOOD_HIGH


class Food(Item):
    type = {
        "apple": FOOD_LOW,
        "bread": FOOD_MID,
        "meat": FOOD_HIGH
    }

    def __init__(self, y, x):
        name = choice(list(Food.type.keys()))
        super().__init__(y, x, "Food", name)
        self.amount = Food.type[name]
