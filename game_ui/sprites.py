import pyglet
from pyglet import gl
from typing import Union


from game.roles import Pot, Ingredient, Dish, Server, Counter
from game import Player

# how many pixels in the game's measurement of 1
PIXELS_PER_UNIT = 60

from .assets import IMAGE, ITEM_RAW_PIXELS



class PixelSprite(pyglet.sprite.Sprite):
    def __init__(self, img, x: float, y: float, batch):
        super().__init__(
            img, int(x * PIXELS_PER_UNIT), int(y * PIXELS_PER_UNIT), batch=batch
        )
        self.current_x, self.current_y = x, y
        self.scale = PIXELS_PER_UNIT / ITEM_RAW_PIXELS
        self.pixelate()

    def pixelate(self):
        gl.glTexParameteri(
            self._texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST
        )
        gl.glTexParameteri(
            self._texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST
        )

    def set_image(self, img):
        self.image = img
        self.pixelate()

    def set_position(self, x: Union[float, None] = None, y: Union[float, None] = None):
        if x != None:
            self.current_x, self.x = x, int(x * PIXELS_PER_UNIT)
        if y != None:
            self.current_y, self.y = y, int(y * PIXELS_PER_UNIT)


class FloorSprite(PixelSprite):
    def __init__(self, x, y, batch):
        super().__init__(IMAGE["floor"], x, y, batch)


class PlayerSprite(PixelSprite):
    def __init__(self, x: float, y: float, batch):
        super().__init__(IMAGE["chef_empty_hand"]["south"], x, y, batch)

    def update_image(self, player: Player):
        holding = player.describe_holding()
        mapping = {
            "empty": "chef_empty_hand",
            "plate": "chef_with_plate",
            "soup": "chef_with_onion_soup",
            "onion": "chef_with_onion",
        }
        label = mapping[holding]
        self.set_image(IMAGE[label][player.facing])


class CounterSprite(PixelSprite):
    def __init__(self, counter: Counter, x, y, batch):
        holding = counter.describe_holding()
        mapping = {
            "empty": "empty_counter",
            "pot": "pot_counter",
            "onion_dispenser": "onion_dispenser_counter",
            "plate_dispenser": "plate_dispenser_counter",
            "server": "server_counter",
        }
        label = mapping[holding]
        super().__init__(IMAGE[label], x, y, batch)
        self.overlay = PixelSprite(IMAGE[label], x, y, batch)
        self.overlay.visible = False

    def update_overlay_image(self, counter: Counter):
        holding = counter.describe_holding()
        mapping = {
            "onion": "onion",
            "plate": "plate",
            "soup": "onion_soup",
            "pot_with_1_cooking": "pot_with_1_onion",
            "pot_with_2_cooking": "pot_with_2_onion",
            "pot_with_3_cooking": "pot_with_3_onion",
            "pot_ready": "pot_with_onion_soup",
        }
        if holding in mapping:
            label = mapping[holding]
            self.overlay.set_image(IMAGE[label])
            self.overlay.visible = True
        else:
            self.overlay.visible = False
