from random import choice

from domain.inventory.item import Item
from domain.setting import WEAPON_LOW, WEAPON_MID, WEAPON_HIGH, WEAPON_MAX


class Weapon(Item):
    type = {
        "Club": WEAPON_LOW,
        "Morning Star": WEAPON_MID,
        "Short Sword": WEAPON_HIGH,
        "Long Sword": WEAPON_MAX
    }
    
    def __init__(self, y, x):
        name = choice(list(Weapon.type.keys()))
        super().__init__(y, x, "Weapon", name)
        self.amount = Weapon.type[name]
