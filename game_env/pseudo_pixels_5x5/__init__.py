import numpy as np

import pathlib


ITEM_RAW_PIXELS = 5


def _load(file_name):
    with open(pathlib.Path(__file__).parent / (file_name + ".txt"), "r") as f:
        lines = [l.strip("\n") for l in f if l.strip("\n")]
    assert len(lines) == ITEM_RAW_PIXELS
    assert all(len(l) == ITEM_RAW_PIXELS * 2 for l in lines)
    pixels = np.zeros((ITEM_RAW_PIXELS, ITEM_RAW_PIXELS), np.float32)
    for row, l in enumerate(lines):
        for col in range(ITEM_RAW_PIXELS):
            square = l[col * 2 : col * 2 + 2]
            if square == "██":
                pixels[row, col] = 1.0
            else:
                assert square == "  "
    return pixels


PIXELS = dict()

PIXELS["counter"] = {
    "empty": _load("empty_counter"),
    "tomato_dispenser": _load("tomato_dispenser_counter"),
    "tomato": _load("tomato_on_counter"),
    "server": _load("server_counter"),
    "plate_dispenser": _load("plate_dispenser_counter"),
    "plate": _load("plate_on_counter"),
    "soup": _load("soup_on_counter"),
    "pot": _load("pot_counter"),
    "pot_with_1_cooking": _load("pot_counter_with_1_tomato"),
    "pot_with_2_cooking": _load("pot_counter_with_2_tomato"),
    "pot_ready": _load("pot_counter_with_soup"),
}


def _rotate(pixels):
    return {
        "south": pixels,
        "north": np.flip(pixels, 0),
        "east": np.transpose(pixels),
        "west": np.flip(np.transpose(pixels), 1),
    }


PIXELS["chef"] = {
    "empty": _rotate(_load("chef")),
    "plate": _rotate(_load("chef_with_plate")),
    "soup": _rotate(_load("chef_with_soup")),
    "tomato": _rotate(_load("chef_with_tomato")),
}
