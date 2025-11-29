# from random import uniform

# from domain.inventory.item import Item
# from domain.cell import Cell


# class Treasure(Item):
#     type = {
#         "Chest": 20,
#         "Ring": 5,
#         "Crown": 15,
#         "Goblet": 10
#     }
#     def __init__(self, y: int, x: int, subtype: str, level: int):
#         super().__init__(y, x ,"Treasure", subtype)
#         self.amount = int(uniform(10, 20 + level) * (level / 7))
    

# class Chest(Treasure):
#     def __init__(self, y: int, x: int, subtype: str, level: int):
#         super().__init__(y, x ,"Chest", subtype)
#         self.amount = int(uniform(10, 20 + level) * (level / 7))


# class Ring(Treasure):
#     def __init__(self, y: int, x: int, subtype: str, level: int):
#         super().__init__(y, x ,"Ring", subtype)
#         self.amount = int(uniform(10, 20 + level) * (level / 7))


# class Crown(Treasure):
#     def __init__(self, y: int, x: int, subtype: str, level: int):
#         super().__init__(y, x ,"Crown", subtype)
#         self.amount = int(uniform(10, 20 + level) * (level / 7))


# class Goblet(Treasure):
#     def __init__(self, y: int, x: int, subtype: str, level: int):
#         super().__init__(y, x ,"Goblet", subtype)
#         self.amount = int(uniform(10, 20 + level) * (level / 7))
