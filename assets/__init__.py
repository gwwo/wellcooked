import pyglet
import pathlib


SPRITE_PIXELS = 15
MARGIN_PIXELS = 1

def _load(img_file: str):
    img = pyglet.image.load(pathlib.Path(__file__).parent/img_file)
    def _item(left: int, bottom: int = 1):
        return img.get_region(
            MARGIN_PIXELS+(left-1)*(SPRITE_PIXELS + 2*MARGIN_PIXELS), 
            MARGIN_PIXELS+(bottom-1)*(SPRITE_PIXELS + 2*MARGIN_PIXELS), 
            width=SPRITE_PIXELS, height=SPRITE_PIXELS)
    return _item

_item = _load('terrain.png')

empty_counter = _item(1)
dish_counter = _item(2)
floor = _item(3)
onion_counter = _item(4)
pot_counter = _item(5)
server_counter = _item(6)


_item = _load('chefs.png')

chef = {
    'empty_hand': {
        'south': _item(5, 4), 'north': _item(6, 6), 'west': _item(4, 2), 'east': _item(1, 7)
    },
    'with_dish': {
        'south': _item(1, 3), 'north': _item(2, 5), 'west': _item(6, 2), 'east': _item(3, 7)
    },
    'with_onion': {
        'south': _item(3, 3), 'north': _item(4, 5), 'west': _item(7, 6), 'east': _item(5, 7)
    },
    'with_onion_soup': {
        'south': _item(1, 2), 'north': _item(2, 4), 'west': _item(7, 2), 'east': _item(3, 6)
    }
}

_item = _load('objects.png')

dish = _item(1)
onion = _item(2)
pot_with_1_onion = _item(4)
pot_with_2_onion = _item(5)
pot_with_3_onion = _item(6)
pot_with_onion_soup = _item(7)
onion_soup = _item(8)


