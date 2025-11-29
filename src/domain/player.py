import random

from domain.enemies import Enemy
from domain.inventory.inventory import Inventory, Item
from domain.setting import PLAYER_START_HEALTH, PLAYER_START_AGILITY, PLAYER_START_STRENGTH
from domain.cell import Cell


class Player:
    def __init__(self, name: str, current_room_id: int, y: int, x: int):
        self.name: str = name
        self.current_room_id: int = current_room_id
        self.x: int = x
        self.y: int = y

        self.max_health: int = PLAYER_START_HEALTH
        self.health: int = self.max_health
        self.agility: int = PLAYER_START_AGILITY
        self.strength: int = PLAYER_START_STRENGTH
        self.gold: int = 0

        self.experience_level: int = 1
        self.experience: int = 0

        self.inventory = Inventory()
        self.timers: dict[str, int] = {}
        self.bonus_values: dict[str, int] = {}
        self.weapon = None
        self.is_sleeping = False

    def move(self, direction, map_grid, enemies, items, keys, floor) -> bool:
        has_moved = False

        if self.is_sleeping:
            self.is_sleeping = False
            return has_moved

        match direction:
            case 'up':
                new_y, new_x = self.y - 1, self.x
            case 'down':
                new_y, new_x = self.y + 1, self.x
            case 'left':
                new_y, new_x = self.y, self.x - 1
            case 'right':
                new_y, new_x = self.y, self.x + 1
            case _:
                raise ValueError(f"error direction: {direction}")

        next_cell = map_grid[new_y][new_x]
        enemy = self.enemy_with_collision(enemies, new_y, new_x)
        if enemy:
            self.attack(enemy)
            if enemy.health <= 0:
                self.get_treasures(enemy)
                self.increase_experience(enemy.experience)
                enemies.remove(enemy)
        elif next_cell.is_passable():
            self.y = new_y
            self.x = new_x

            item = self.is_on_item(items)
            if item:
                self.pick_up_item(item)
                items.remove(item)

            key = self.is_on_item(keys)
            if key:
                self.pick_up_item(key)
                keys.remove(key)
            has_moved = True

        elif self.closed_door_is_passible(next_cell):
            for k in self.inventory.doorkeys:
                if (next_cell == Cell.door_red and k.color == 'Red') or \
                        (next_cell == Cell.door_green and k.color == 'Green') or \
                        (next_cell == Cell.door_blue and k.color == 'Blue'):
                    self.inventory.doorkeys.remove(k)
                    map_grid[new_y][new_x] = Cell.door
                    floor.open_corridor(new_y, new_x)
                    break

            self.y = new_y
            self.x = new_x
            has_moved = True

        return has_moved

    def closed_door_is_passible(self, next_cell) -> bool:
        return next_cell == Cell.door_red and \
               any(k.color == 'Red' for k in self.inventory.doorkeys) \
               or next_cell == Cell.door_green and any(k.color == 'Green' for k in self.inventory.doorkeys) \
               or next_cell == Cell.door_blue and any(k.color == 'Blue' for k in self.inventory.doorkeys)

    def get_treasures(self, enemy: Enemy) -> str:
        treasure_types = ["Golden", "Silver", "Brilliant", "Ancient"]
        treasure_items = ["Crown", "Ring", "Chest", "Coins", "Relic"]

        treasure = random.choice(treasure_types) + " " + random.choice(treasure_items)

        amount = enemy.hostility * enemy.strength * enemy.agility // 10
        self.gold += amount
        return treasure

    def is_on_cell(self, cell) -> bool:
        return self.y == cell.y and self.x == cell.x

    def is_on_item(self, items) -> Item | None:
        for item in items:
            if self.is_on_cell(item):
                return item
        return None

    @staticmethod
    def enemy_with_collision(enemies, next_y, next_x) -> Enemy | None:
        for enemy in enemies:
            if enemy.y == next_y and enemy.x == next_x:
                return enemy
        return None

    def attack(self, enemy) -> (int, int):
        if enemy.name == 'Vampire' and enemy.shield:
            enemy.shield = False
            return 0, 0

        if self.weapon:
            strength = self.strength + self.weapon.amount
        else:
            strength = self.strength

        damage_array = [0, strength // 2, strength]
        if self.agility > enemy.agility:
            weights = [1, 2, 3]
        elif self.agility < enemy.agility:
            weights = [3, 2, 1]
        else:
            weights = [1, 1, 1]

        damage = random.choices(damage_array, weights=weights, k=1)[0]
        enemy.health -= damage

        i = damage_array.index(damage)

        return damage, i

    def pick_up_item(self, item) -> Item:
        # if not self.inventory.count_item_inventory(item):
        #     return None
        match item.type:
            case "Food":
                self.inventory.food.append(item)
            case "Weapon":
                self.inventory.weapons.append(item)
            case "Potion":
                self.inventory.potions.append(item)
            case "Scroll":
                self.inventory.scrolls.append(item)
            case "Red Key" | "Green Key" | "Blue Key":
                self.inventory.doorkeys.append(item)
            case _:
                raise ValueError("Item is not correct")

        return item

    def drop_item(self, item: Item, items: list[Item], map_grid: list[list[Cell]]) -> bool:
        is_droppable = False
        neighbor_cells = [(self.y + 1, self.x), (self.y - 1, self.x), (self.y, self.x + 1), (self.y, self.x - 1)]
        for cell in neighbor_cells:
            if map_grid[cell[0]][cell[1]].is_dropable:
                is_droppable = True

        if is_droppable:
            while True:
                y, x = random.choice(neighbor_cells)
                if map_grid[y][x].is_dropable:
                    items.append(item)
                    return True
        else:
            return False

    def take_weapon(self, weapon, items: list[Item], map_grid) -> None:
        if not self.weapon or (self.weapon and self.drop_item(weapon, items, map_grid)):
            self.weapon = weapon
            self.inventory.weapons.remove(weapon)

    def increase_experience(self, experience) -> None:
        self.experience += experience
        while self.experience // 10 >= self.experience_level:
            self.level_up()

    def level_up(self) -> None:
        self.experience_level += 1
        self.max_health += 5
        self.restore_health(5)

    def restore_health(self, amount) -> None:
        self.health = min(self.max_health, self.health + amount)

    def use_food(self, food) -> None:
        self.restore_health(food.amount)
        self.inventory.food.remove(food)

    def use_scroll(self, scroll) -> None:
        match scroll.subtype:
            case "HP":
                self.max_health += scroll.amount
                self.health += scroll.amount
            case "strength":
                self.strength += scroll.amount
            case "agility":
                self.agility += scroll.amount
        self.inventory.scrolls.remove(scroll)

    def use_potion(self, potion) -> None:
        match potion.ability:
            case "HP":
                self.max_health += potion.amount
                self.health += potion.amount
            case "strength" | "agility":
                setattr(self, potion.ability, getattr(self, potion.ability) + potion.amount)

        self.timers[potion.ability] = potion.duration
        self.bonus_values[potion.ability] = potion.amount
        self.inventory.potions.remove(potion)

    def update_timers(self) -> None:
        expired = []
        for effect in list(self.timers.keys()):
            self.timers[effect] -= 1
            if self.timers[effect] <= 0:
                expired.append(effect)

        for effect in expired:
            amount = self.bonus_values.get(effect, 0)
            match effect:
                case "HP":
                    self.max_health -= amount
                    self.health = min(self.health, self.max_health)
                case "strength" | "agility":
                    setattr(self, effect, getattr(self, effect) - amount)

            self.timers.pop(effect, None)
            self.bonus_values.pop(effect, None)
