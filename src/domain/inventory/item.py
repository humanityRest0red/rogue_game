class Item:
    type = ["Potion", "Scroll", "Food", "Weapon"]  #, "Door Key"]

    def __init__(self, y: int, x: int, type: str, subtype: str):
        self.y = y
        self.x = x
        self.type = type
        self.subtype = subtype
