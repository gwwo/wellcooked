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
IMAGE["onion_dispenser_counter"] = _item(4)
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
IMAGE["chef_with_onion"] = {
    "south": _item(3, 3),
    "north": _item(4, 5),
    "west": _item(7, 6),
    "east": _item(5, 7),
}
IMAGE["chef_with_onion_soup"] = {
    "south": _item(1, 2),
    "north": _item(2, 4),
    "west": _item(7, 2),
    "east": _item(3, 6),
}


_item = _load("objects.png")

IMAGE["plate"] = _item(1)
IMAGE["onion"] = _item(2)
IMAGE["pot_with_1_onion"] = _item(4)
IMAGE["pot_with_2_onion"] = _item(5)
IMAGE["pot_with_3_onion"] = _item(6)
IMAGE["pot_with_onion_soup"] = _item(7)
IMAGE["onion_soup"] = _item(8)
