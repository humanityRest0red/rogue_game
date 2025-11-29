from domain.player import Player
from domain.enemies import Enemy, Ogre


menu_states = ('start_game', 'load_game', 'show_score', 'exit')


class State:
    game_state = ('play', 'exit', 'win', 'game_over')

    def __init__(self):
        self.player: str = ''
        self.enemy: str = ''
        self.item: str = ''

        self.killed_by: str = ''
        self.treasures: str = ''
        self.game_state: str = 'play'
        # self.is_gameover: bool = False
        # self.is_win: bool = False
        # self.is_exit: bool = False
        
        self.damage_taken: int = 0
        self.damage_dealt: int = 0
        self.food_used: int = 0
        self.potions_used: int = 0
        self.scrolls_used: int = 0
        self.enemies_killed: int = 0
        self.cells_passed: int = 0
        self.player_hp_percent: int = 100

        Enemy.attack = self.enemy_attack_wrapper(Enemy.attack, self)
        Ogre.attack = self.enemy_attack_wrapper(Ogre.attack, self)

        Player.attack = self.player_attack_wrapper(Player.attack, self)
        Player.pick_up_item = self.player_pick_up_wrapper(Player.pick_up_item, self)
        Player.get_treasures = self.player_get_treasures_wrapper(Player.get_treasures, self)
        Player.level_up = self.player_level_up_wrapper(Player.level_up, self)

        Player.use_potion = self.player_use_item_wrapper(Player.use_potion, self)
        Player.use_scroll = self.player_use_item_wrapper(Player.use_scroll, self)
        Player.use_food = self.player_use_item_wrapper(Player.use_food, self)

        Player.move = self.player_move_wrapper(Player.move, self)

    def reset_states(self):
        self.player = ''
        self.enemy = ''
        self.item = ''

    @staticmethod
    def enemy_attack_wrapper(method, state):
        def wrapped(self, player):
            is_ogre_resting = self.name == 'Ogre' and self.is_resting

            damage, i = method(self, player)
            if i == 0:
                state.enemy = f'{self.name} misses you'
            elif i == 1:
                state.enemy = f'{self.name} hit you for {damage} damage'
            else:
                state.enemy = f'{self.name} scored an excellent hit on you for {damage} damage'
            
            if is_ogre_resting:
                state.enemy = 'Ogre is resting for one move'
            if self.name == 'Snake Wizard' and player.is_sleeping:
                state.enemy += '. Enemy sends you to the Kingdom of Dreams'
            if player.health <= 0:
                state.killed_by = self.name
            
            state.player_hp_percent = player.health * 100 // player.max_health
            if i > 0:
                state.damage_taken += damage

            return damage, i
        return wrapped

    @staticmethod
    def player_attack_wrapper(method, state):
        def wrapped(self, enemy):
            missing_on_vampire_msg = ''
            if enemy.name == 'Vampire' and enemy.shield:
                missing_on_vampire_msg = ' for the first time'

            damage, i = method(self, enemy)
            if i == 0:
                state.player = f'You miss the {enemy.name}' + missing_on_vampire_msg
            elif i == 1:
                state.player = f'You hit the {enemy.name} for {damage} damage'
            else:
                state.player = f'You scored an excellent hit on the {enemy.name} for {damage} damage'
            if enemy.health <= 0:
                state.player += f'.    You have slain the {enemy.name}!'
                state.enemies_killed += 1

            state.damage_dealt += damage

            return damage, i
        return wrapped

    @staticmethod
    def player_pick_up_wrapper(method, state):
        def wrapped(*args, **kwargs):
            item = method(*args, **kwargs)
            match item.type:
                case "Gold":
                    state.item = f'You find {item.amount} gold pieces'
                case "Food":
                    state.item = f'You pick up a {item.subtype}'
                case "Weapon":
                    state.item = f'You pick up a {item.subtype}'
                case "Potion":
                    state.item = f'You pick up a Potion of {item.subtype} {item.strength_label}'
                case "Scroll":
                    state.item = f'You pick up a Scroll of {item.subtype}'
                case "Red Key":
                    state.item = f'You pick up a {item.subtype}'
                case "Green Key":
                    state.item = f'You pick up a {item.subtype} Key'
                case "Blue Key":
                    state.item = f'You pick up a {item.subtype} Key'

                case None:
                    state.item = f'Your inventory is full. Cannot pick up {item.subtype}'
            return item
        return wrapped

    @staticmethod
    def player_get_treasures_wrapper(method, state):
        def wrapped(*args, **kwargs):
            name = method(*args, **kwargs)
            state.item = f'You have got the {name}'
            return name
        return wrapped

    @staticmethod
    def player_level_up_wrapper(method, state):
        def wrapped(self):
            method(self)
            state.item = f'Welcome to level {self.experience_level}'
        return wrapped

    @staticmethod
    def player_use_item_wrapper(method, state):
        def wrapped(*args, **kwargs):
            method(*args, **kwargs)
            if "food" in method.__name__:
                state.food_used += 1
            elif "potion" in method.__name__:
                state.potions_used += 1
            elif "scroll" in method.__name__:
                state.scrolls_used += 1
        return wrapped

    @staticmethod
    def player_move_wrapper(method, state):
        def wrapped(*args, **kwargs):
            has_moved = method(*args, **kwargs)
            if has_moved:
                state.cells_passed += 1
            return has_moved
        return wrapped
