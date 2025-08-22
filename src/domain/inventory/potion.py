from random import choice

from domain.inventory.item import Item
from domain.setting import POTION_HEALTH, POTION_STRENGTH, POTION_AGILITY


class Potion(Item):
    potion_type = [
        "strength",
        "HP",
        "agility"
    ]

    strength_type = {
        "I":  (1, 5),
        "II": (2, 8),
        "III": (3, 12)
    }

    def __init__(self, y, x):
        name = choice(Potion.potion_type)
        super().__init__(y, x, "Potion", name)
        self.ability = name
        self.strength_label = choice(list(Potion.strength_type.keys()))
        self.amount, self.duration = Potion.strength_type[self.strength_label]

