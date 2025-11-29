import curses


class Color:
    GREEN = 1
    RED = 2
    WHITE = 3
    YELLOW = 4
    BLUE = 5
    wall = 6
    corridor = 7
    exit_ = 8
    VIOLET = 9
    GRAY = 10
    GOLD = 11


def get_map_case(entity_name):
    match entity_name:
        case 'Zombie':
            return 'z', Color.GREEN
        case 'Vampire':
            return 'v', Color.RED
        case 'Ghost':
            return 'g', Color.WHITE
        case 'Unseen Ghost':
            return get_map_case('Room')
        case 'Ogre':
            return 'o', Color.YELLOW
        case 'Snake Wizard':
            return 's', Color.WHITE
        case 'Mimic':
            return 'm', Color.WHITE
        case 'Gold':
            return '❁', Color.GOLD
        case 'Crown':
            return '♔', Color.GOLD
        case 'Potion':
            return '🜮', Color.VIOLET
        case 'Scroll':
            return '∫', Color.GRAY
        case 'Food':
            return '♣', Color.RED
        case 'Weapon':
            return '✝', Color.WHITE
        case 'Map':
            return ' ', Color.WHITE
        case 'Fog':
            return ' ', Color.WHITE
        case 'Room':
            return '.', Color.GREEN
        case 'Floor':
            return ' ', Color.corridor
        case 'Door':
            return '╬', Color.wall
        case 'Red Door':
            return '╬', Color.RED
        case 'Green Door':
            return '╬', Color.GREEN
        case 'Blue Door':
            return '╬', Color.BLUE
        case 'Vertical Wall':
            return '║', Color.wall
        case 'Horizontal Wall':
            return '═', Color.wall
        case 'Top Left Wall':
            return '╔', Color.wall
        case 'Top Right Wall':
            return '╗', Color.wall
        case 'Bottom Left Wall':
            return '╚', Color.wall
        case 'Bottom Right Wall':
            return '╝', Color.wall
        case 'Exit':
            return '↓', Color.exit_
        case 'Red Key':
            return '¶', Color.RED
        case 'Blue Key':
            return '¶', Color.BLUE
        case 'Green Key':
            return '¶', Color.GREEN
        case _:
            raise ValueError(f"Unknown entity: {entity_name}")


KEYS = {
    'exit': ['q', 'Q', 'й', 'Й', '\x1b'],
    'apply': ['\n'],

    'up': ['w', 'W', 'ц', 'Ц', curses.KEY_UP],
    'down': ['s', 'S', 'ы', 'Ы', curses.KEY_DOWN],
    'left': ['a', 'A', 'ф', 'Ф', curses.KEY_LEFT],
    'right': ['d', 'D', 'в', 'В', curses.KEY_RIGHT],

    'scroll': ['e', 'E', 'у', 'У'],
    'weapon': ['h', 'H', 'р', 'Р'],
    'food': ['j', 'J', 'о', 'О'],
    'potion': ['k', 'K', 'л', 'Л'],
    'toggle': ['d', 'D', 'в', 'В']
}
