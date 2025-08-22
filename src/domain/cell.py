from enum import Enum

coordinate = tuple[int, int]

class Cell(Enum):
    # fog
    fog = 'Fog'

    # Map
    map_ = 'Map'
    room = 'Room'
    floor = 'Floor'

    horiz_wall = 'Horizontal Wall'
    vert_wall = 'Vertical Wall'
    top_left_wall = 'Top Left Wall'
    top_right_wall = 'Top Right Wall'
    bottom_left_wall = 'Bottom Left Wall'
    bottom_right_wall = 'Bottom Right Wall'

    exit_ = 'Exit'
    
    # doors
    door = 'Door'
    door_red = 'Red Door'
    door_green = 'Green Door'
    door_blue = 'Blue Door'

    # treasure
    chest = 'Gold'
    ring = 'Ring'
    crown = 'Crown'
    goblet = 'Goblet'
    
    # item
    potion = 'Potion'
    food = 'Food'
    scroll = 'Scroll'
    weapon = 'Weapon'

    # keys
    doorkey_r = 'Red Key'
    doorkey_g = 'Green Key'
    doorkey_b = 'Blue Key'

    # enemies
    zombie = 'Zombie'
    vampire = 'Vampire'
    ghost = 'Ghost'
    ghost_unseen = 'Unseen Ghost'
    ogre = 'Ogre'
    snake_wizard = 'Snake Wizard'
    mimic = 'Mimic'

    def is_passable(self):
        return self in (Cell.room, Cell.floor, Cell.door, Cell.fog, Cell.exit_) or self.is_item()
    
    def is_dropable(self): # fiix addd
        return self in (Cell.room, Cell.floor, Cell.door)

    def is_door(self): # fiix addd
        return self in (Cell.door, Cell.door_red, Cell.door_green, Cell.door_blue)

    def is_item(self):
        return self in (Cell.potion, Cell.food, Cell.scroll, Cell.weapon,
        Cell.doorkey_r, Cell.doorkey_g, Cell.doorkey_b)

    def is_wall(self):
        return self in (Cell.horiz_wall, Cell.vert_wall, Cell.top_left_wall,
            Cell.top_right_wall, Cell.bottom_left_wall, Cell.bottom_right_wall)
