"""
С каждым новым уровнем повышается количество и сложность противников,
снижается количество полезных предметов и повышается количество сокровищ,
которые выпадают с побежденных противников.

Если игрок легко проходит уровни, необходимо увеличивать сложность.
Если игрок сталкивается с трудностями, можно добавлять немного больше полезных
для игрока предметов (например, если игрок часто тратит здоровье —
предоставлять больше аптечек) и понизить количество и сложность врагов.
"""


class DifficultyAdjuster:
    def __init__(self):
        self.enemy_spawn_chance = 60
        self.enemy_difficulty = 1.0
        self.item_spawn_chance = 40

    def update(self, state, levels_passed):
        if state.player_hp_percent > 70:
            self.enemy_difficulty *= 1.2
            self.item_spawn_chance -= 5
            self.enemy_spawn_chance += 5
        elif state.player_hp_percent < 40:
            self.enemy_difficulty *= 0.8
            self.item_spawn_chance += 5
            self.enemy_spawn_chance -= 5

        if state.damage_dealt < state.damage_taken:
            self.enemy_difficulty *= 0.9
        else:
            self.enemy_difficulty *= 1.1

        # if state.enemies_killed < levels_passed / 4:
        #     state.enemy_spawn_chance += 10

        # self.enemy_difficulty = max(0.5, min(3.0, self.enemy_difficulty))
        # self.item_spawn_chance = max(0.5, min(2.0, self.item_spawn_chance))
