import pyglet
import pathlib


ITEM_RAW_PIXELS = 15

IMAGE = dict()


def _load(img_file: str):
    img = pyglet.image.load(pathlib.Path(__file__).parent / img_file)
    MARGIN_PIXELS = 1

    def _item(left: int, bottom: int = 1):
        return img.get_region(
            MARGIN_PIXELS + (left - 1) * (ITEM_RAW_PIXELS + 2 * MARGIN_PIXELS),
            MARGIN_PIXELS + (bottom - 1) * (ITEM_RAW_PIXELS + 2 * MARGIN_PIXELS),
            width=ITEM_RAW_PIXELS,
            height=ITEM_RAW_PIXELS,
        )

    return _item


_item = _load("terrain.png")

IMAGE["empty_counter"] = _item(1)
IMAGE["plate_dispenser_counter"] = _item(2)
IMAGE["floor"] = _item(3)
IMAGE["tomato_dispenser_counter"] = _item(7)
IMAGE["pot_counter"] = _item(5)
IMAGE["server_counter"] = _item(6)


_item = _load("chefs.png")


IMAGE["chef_empty_hand"] = {
    "south": _item(5, 4),
    "north": _item(6, 6),
    "west": _item(4, 2),
    "east": _item(1, 7),
}
IMAGE["chef_with_plate"] = {
    "south": _item(1, 3),
    "north": _item(2, 5),
    "west": _item(6, 2),
    "east": _item(3, 7),
}
IMAGE["chef_with_tomato"] = {
    "south": _item(3, 2),
    "north": _item(4, 4),
    "west": _item(2, 1),
    "east": _item(5, 6),
}
IMAGE["chef_with_tomato_soup"] = {
    "south": _item(2, 2),
    "north": _item(3, 4),
    "west": _item(1, 1),
    "east": _item(4, 6),
}


_item = _load("objects.png")

IMAGE["plate"] = _item(1)
IMAGE["tomato"] = _item(15)
IMAGE["pot_with_1_tomato"] = _item(9)
IMAGE["pot_with_2_tomato"] = _item(10)
IMAGE["pot_with_3_tomato"] = _item(11)
IMAGE["pot_with_tomato_soup"] = _item(13)
IMAGE["tomato_soup"] = _item(14)
