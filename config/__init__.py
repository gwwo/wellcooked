
from pyglet.window import key
import pathlib
from typing import Union

from game import Action, Player
from game.roles import Pot, Counter, Dish, Server, Ingredient

def load(layout_name: str):
    with open(pathlib.Path(__file__).parent/(layout_name + '.txt'), 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    assert all(len(lines[0]) == len(l) for l in lines[1:])

    # starting from the left lower corner, 
    # the coordinate (x, y) has the char of `layout[x][y]`
    layout = list(map(list, zip(*reversed(lines))))

    kitchen: list[list[Union[Counter, None]]] = []
    players: list[Player] = []
    pots: list[Pot] = []

    for x, col in enumerate(layout):
        c = []
        for y, char in enumerate(col):
            tile = None
            if char == 'X':
                tile = Counter(holding=None)
            elif char == 'P':
                pot = Pot()
                pots.append(pot)
                tile = Counter(holding=pot)
            elif char == 'D':
                tile = Counter(holding=Dish())
                tile.new_one_to_dispense = True
            elif char == 'S':
                server = Server(can_serve_ingredient=layout_name.startswith('simple'))
                tile = Counter(holding=server)
            elif char in ['T']:
                tile = Counter(holding=Ingredient(value='tomato'))
                tile.new_one_to_dispense = True
            elif char in ['1', '2', '3', '4']:
                players.append(Player(x=x, y=y, id=char))
            c.append(tile)
        kitchen.append(c)
    return kitchen, players, pots



USER_INPUT_MAPPING = {
    '1': {
        key.RIGHT: Action.RIGHT,
        key.LEFT: Action.LEFT,
        key.UP: Action.UP,
        key.DOWN: Action.DOWN,
        key.RSHIFT: Action.INTERACT,
    },
    '2': {
        key.D: Action.RIGHT,
        key.A: Action.LEFT,
        key.W: Action.UP,
        key.S: Action.DOWN,
        key.LSHIFT: Action.INTERACT,
    },
    '3': {
        key.L: Action.RIGHT,
        key.J: Action.LEFT,
        key.I: Action.UP,
        key.K: Action.DOWN,
        key.SPACE: Action.INTERACT,
    }
}



