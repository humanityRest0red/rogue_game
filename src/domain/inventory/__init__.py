import random

from domain.inventory.item import Item
from domain.inventory.food import Food
from domain.inventory.weapon import Weapon
from domain.inventory.potion import Potion
from domain.inventory.scroll import Scroll
from domain.inventory.door_key import DoorKey


def spawn(room, items: list[Item]):
    while True:
        check = True
        x = random.randint(room.x, room.x_)
        y = random.randint(room.y, room.y_)
        for item in items:
            if item.x == x and item.y == y:
                check = False
                break
        if check:
            break
    
    item_type = random.choice(Item.type)
    match item_type:
        # case "Gold":
        #     return Gold(y, x, "Gold", level)
        case "Potion":
            return Potion(y, x)
        case "Scroll":
            return Scroll(y, x)
        case "Food":
            return Food(y, x)
        case "Weapon":
            return Weapon(y, x)
        case "Door Key":
            return DoorKey(y, x)
        case _:
            raise ValueError("Is Not Item")


Item.spawn = spawn
