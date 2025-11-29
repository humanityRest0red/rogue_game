from random import choice

from domain.inventory.item import Item
from domain.setting import SCROLL_HEALTH, SCROLL_STRENGTH, SCROLL_AGILITY


class Scroll(Item):
    type = {
        "HP": SCROLL_HEALTH,
        "strength": SCROLL_STRENGTH,
        "agility": SCROLL_AGILITY
    }

    def __init__(self, y, x):
        name = choice(list(Scroll.type.keys()))
        super().__init__(y, x, "Scroll", name)
        self.ability = name
        self.amount = Scroll.type[name]