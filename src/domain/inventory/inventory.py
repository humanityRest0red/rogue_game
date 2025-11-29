from domain.inventory import Item, Food, Weapon, Potion, Scroll, DoorKey


class Inventory:
    max_item_inventory = 9

    def __init__(self):
        self.food: list[Food] = []
        self.potions: list[Potion] = []
        self.scrolls: list[Scroll] = []
        self.weapons: list[Weapon] = []
        self.doorkeys: list[DoorKey] = []

    def count_item_inventory(self, item: Item) -> bool:
        match item.type:
            # case "Gold":
            #     return True
            case "Food":
                return len(self.food) < Inventory.max_item_inventory
            case "Potion":
                return len(self.potions) < Inventory.max_item_inventory
            case "Scroll":
                return len(self.scrolls) < Inventory.max_item_inventory
            case "Weapon":
                return len(self.weapons) < Inventory.max_item_inventory
            # case _:
            #     raise ValueError("Error Item Type Inventory Counter")
