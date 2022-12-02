import pyglet
from pyglet import gl
from typing import Union, Tuple


from roles import Pot, Ingredient, Dish, Server
from game import Action, Game, Player
from roles import Counter
import assets
import config


class PixelSprite(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, batch):
        super().__init__(img, int(x * config.VISUAL_UNIT), int(y * config.VISUAL_UNIT), batch=batch)
        self.current_x, self.current_y = x, y
        self.scale = config.VISUAL_UNIT / assets.SPRITE_PIXELS
        self.pixelate()
    def pixelate(self):
        gl.glTexParameteri(self._texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(self._texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    def set_image(self, img):
        self.image = img
        self.pixelate()
    def set_x(self, x: float):
        self.current_x, x = x, int(x * config.VISUAL_UNIT)
        if self._x != x: self.x = x
    def set_y(self, y: float):
        self.current_y, y = y, int(y * config.VISUAL_UNIT)
        if self._y != y: self.y = y


class CounterSprite(PixelSprite):
    def __init__(self, holding: Union[Server, Pot, Ingredient, Dish, None], x, y, batch):
        if holding == None:
            img = assets.empty_counter
        elif type(holding) is Pot:
            img = assets.pot_counter
        elif type(holding) is Ingredient:
            img = assets.onion_counter
        elif type(holding) is Dish:
            img = assets.dish_counter
        elif type(holding) is Server:
            img = assets.server_counter
        super().__init__(img, x, y, batch)
        self.overlay = PixelSprite(img, x, y, batch)
        self.overlay.visible = False

    def update_image(self, holding: Union[Pot, Ingredient, Dish, None]):
        img = None
        if type(holding) is Ingredient:
            img = assets.onion
        elif type(holding) is Dish:
            if holding.content == None:
                img = assets.dish
            else:
                img = assets.onion_soup
        elif type(holding) is Pot:
            ingred_num = len(holding.soup)
            if ingred_num == 1:
                img = assets.pot_with_1_onion
            elif ingred_num == 2:
                img = assets.pot_with_2_onion
            elif ingred_num == 3:
                if holding.need_cooking > 0:
                    img = assets.pot_with_3_onion
                else:
                    img = assets.pot_with_onion_soup
        if img != None:
            self.overlay.set_image(img)
            self.overlay.visible = True
        else:
            self.overlay.visible = False

class PlayerSprite(PixelSprite):
    def __init__(self, x: float, y: float, batch):
        super().__init__(assets.chef['empty_hand']['south'], x, y, batch)
    def update_image(self, holding: Union[None, Dish, Ingredient], facing: str):
        if holding == None:
            img = assets.chef['empty_hand']
        elif type(holding) is Dish:
            if holding.content == None:
                img = assets.chef['with_dish']
            else:
                img = assets.chef['with_onion_soup']
        elif type(holding) is Ingredient:
            img = assets.chef['with_onion']
        self.set_image(img[facing])

from random import randint

class GameUI():

    def __init__(self, game: Game):

        width = game.kitchen_w * config.VISUAL_UNIT
        height = game.kitchen_h * config.VISUAL_UNIT
        window = pyglet.window.Window(width, height)

        batch = pyglet.graphics.Batch()
        c_sprites: dict[Counter, CounterSprite] = dict()
        p_sprites: dict[Player, PlayerSprite] = dict()
        f_sprites: list[PixelSprite] = []

        for x in range(game.kitchen_w):
            for y in range(game.kitchen_h):
                tile = game.kitchen[x][y]
                if tile == None:
                    f_sprites.append(PixelSprite(assets.floor, x, y, batch))
                elif type(tile) is Counter:
                    c_sprites[tile] = CounterSprite(tile.holding, x, y, batch)

        # w, h = game.player_w, game.player_h
        for player in game.players:
            # rect.anchor_position = (w-1)/2*visual_unit, (h-1)/2*visual_unit
            p_sprites[player] = PlayerSprite(player.x, player.y, batch)

        self.window = window

        self.c_sprites, self.p_sprites, self.f_sprites = c_sprites, p_sprites, f_sprites
        self.game = game
        self.batch = batch

        self.pressed: int = dict()
        self.triggered: int = dict()

        for p in game.players:
            mapping = config.USER_INPUT_MAPPING[p.id]
            for key, action in mapping.items():
                if action == Action.INTERACT:
                    self.triggered[key] = False
                else:
                    self.pressed[key] = False

        self.is_closed = False
        def on_close():
            self.window.close()
            self.is_closed = True
        self.window.push_handlers(on_close)

        def on_key_press(symbol, modifiers):
            if symbol in self.pressed:
                self.pressed[symbol] = True
            elif symbol in self.triggered:
                self.triggered[symbol] = True
        def on_key_release(symbol, modifiers):
            if symbol in self.pressed:
                self.pressed[symbol] = False
        self.window.push_handlers(on_key_press, on_key_release)

        self.clock = pyglet.clock.Clock()
        self.clock.schedule_interval(self.players_moving, 1/120.0)

        self.window.switch_to()
        self.window.clear()
        self.batch.draw()
        self.window.flip()
        self.is_paused = True

    def sync(self):
        # print('start syncing')
        if self.is_closed: return
        self.players_turn_and_interact()
        self.is_paused = False
        while True:
            self.clock.tick()
            self.window.dispatch_events()
            if self.is_closed:
                break
            self.window.clear()
            self.batch.draw()
            self.window.flip()
            if self.is_paused:
                break
        # print('synced')

    def listen(self):
        actions = {p.id: Action.NOOP for p in self.game.players}
        if self.is_closed: return actions
        self.window.dispatch_events()
        for p_id in actions:
            mapping = config.USER_INPUT_MAPPING[p_id]
            for key, action in mapping.items():
                if key in self.pressed and self.pressed[key]:
                    actions[p_id] = action
                if key in self.triggered and self.triggered[key]:
                    self.triggered[key] = False
                    actions[p_id] = action
        return actions

    def players_turn_and_interact(self):
        for player, sprite in self.p_sprites.items():
            sprite.update_image(player.holding, player.facing)
        for counter, sprite in self.c_sprites.items():
            if not counter.new_one_to_dispense:
                sprite.update_image(counter.holding)

    # will move no more than this amount of tiles in one second
    players_moving_speed = 5.0

    def players_moving(self, dt: float):
        # print('moving', dt)
        if dt > 0.02: dt = 0.02
        finished = True
        for player, sprite in self.p_sprites.items():
            x, y = sprite.current_x, sprite.current_y
            dx, dy = player.x - x, player.y - y
            if dx != 0:
                d_ = dt * self.players_moving_speed
                if d_ > abs(dx):
                    x = player.x
                else:
                    finished = False
                    x += d_ if dx > 0 else -d_
                sprite.set_x(x)
            if dy != 0:
                d_ = dt * self.players_moving_speed
                if d_ > abs(dy):
                    y = player.y
                else:
                    finished = False
                    y += d_ if dy > 0 else -d_
                sprite.set_y(y)
        self.is_paused = finished


import time


if __name__ == "__main__":

    game = Game(*config.load('simple/circuit_room'), move_to_axis=True).reset()

    # game = Game(*config.load('big_room'), player_size=(0.6, 0.96)).reset()

    window = GameUI(game)

    while not window.is_closed:
        actions = window.listen()
        if all(a == Action.NOOP for a in actions.values()):
            continue
        game.step(actions)
        window.sync()


