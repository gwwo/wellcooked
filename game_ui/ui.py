import pyglet
import time

from game import Action, Game, Player
from game.roles import Counter


from config import USER_INPUT_MAPPING

from .sprites import CounterSprite, PlayerSprite, FloorSprite, PIXELS_PER_UNIT


class GameUI:
    def __init__(self, game: Game, caption="wellcooked"):
        w, h = game.kitchen_w, game.kitchen_h
        self.window = pyglet.window.Window(
            w * PIXELS_PER_UNIT, h * PIXELS_PER_UNIT, caption
        )
        # batch needs be initialized after winodw
        batch = pyglet.graphics.Batch()
        c_sprites: dict[Counter, CounterSprite] = dict()
        p_sprites: dict[Player, PlayerSprite] = dict()
        f_sprites: list[FloorSprite] = []
        for x in range(w):
            for y in range(h):
                tile = game.kitchen[x][y]
                if tile == None:
                    f_sprites.append(FloorSprite(x, y, batch))
                elif type(tile) is Counter:
                    c_sprites[tile] = CounterSprite(tile.describe_holding(), x, y, batch)
        for player in game.players:
            p_sprites[player] = PlayerSprite(player.x, player.y, batch)
        self.c_sprites, self.p_sprites, self.f_sprites = c_sprites, p_sprites, f_sprites
        self.game, self.batch = game, batch

        self.clock = None
        self.listen_for_keyboard = False
        self.is_closed = False
        self.window.push_handlers(on_close=self.close)
        self.window.switch_to()
        self.draw()

    def draw(self):
        self.window.clear()
        self.batch.draw()
        self.window.flip()

    def close(self):
        if self.is_closed:
            return
        self.window.pop_handlers()
        if self.listen_for_keyboard:
            self.window.pop_handlers()
        self.window.close()
        self.is_closed = True

    def fresh(self):
        if self.is_closed:
            return
        self.players_turn_and_interact()
        self.players_move()
        self.draw()

    # during animation, players will move no more than `speed` amount of unit tiles in one second
    def sync(self, speed: float = 5.0):
        # print('start syncing')
        if self.is_closed:
            return
        any_update = self.players_turn_and_interact()

        if self.clock == None:
            self.clock = pyglet.clock.Clock()
        moving_finished = False
        first_tick = True

        def moving(dt):
            nonlocal first_tick, moving_finished
            if first_tick and dt > 0.02:
                dt = 0.02
            moving_finished = self.players_moving(dt, speed)
            if first_tick and moving_finished and any_update:
                # make the effect of `turn_and_face` stay for a while, friendly for animation
                # TODO: the playing with continuous Action is lagging
                time.sleep(0.1)

        self.clock.schedule_interval(moving, 1 / 120.0)
        while True:
            self.clock.tick()
            if first_tick:
                first_tick = False
            self.window.dispatch_events()
            if self.is_closed:
                break
            self.draw()
            if moving_finished:
                break
        self.clock.unschedule(moving)
        # print('synced')

    def listen_until(self):
        while True:
            actions = self.listen()
            if self.is_closed or not all(a == Action.NOOP for a in actions.values()):
                return actions

    def listen(self):
        actions = {p.id: Action.NOOP for p in self.game.players}
        if self.is_closed:
            return actions

        if not self.listen_for_keyboard:
            self.setup_keyboard_listener()
            self.listen_for_keyboard = True

        self.window.dispatch_events()
        for p_id in actions:
            if p_id in USER_INPUT_MAPPING:
                mapping = USER_INPUT_MAPPING[p_id]
                for key, action in mapping.items():
                    if key in self.pressed and self.pressed[key]:
                        actions[p_id] = action
                    if key in self.triggered and self.triggered[key]:
                        self.triggered[key] = False
                        actions[p_id] = action
        return actions

    def setup_keyboard_listener(self):
        self.pressed: dict[int, bool] = dict()
        self.triggered: dict[int, bool] = dict()
        for p in self.game.players:
            if p.id in USER_INPUT_MAPPING:
                mapping = USER_INPUT_MAPPING[p.id]
                for key, action in mapping.items():
                    if action == Action.INTERACT:
                        self.triggered[key] = False
                    else:
                        self.pressed[key] = False

        def on_key_press(symbol, modifiers):
            if symbol in self.pressed:
                self.pressed[symbol] = True
            elif symbol in self.triggered:
                self.triggered[symbol] = True

        def on_key_release(symbol, modifiers):
            if symbol in self.pressed:
                self.pressed[symbol] = False

        self.window.push_handlers(on_key_press, on_key_release)

    def players_turn_and_interact(self):
        any_update = False
        for player, sprite in self.p_sprites.items():
            holding, facing = player.describe_holding(), player.facing
            if holding != sprite.holding or facing != sprite.facing:
                sprite.update_image(holding, facing)
                any_update = True
        for counter, sprite in self.c_sprites.items():
            holding = counter.describe_holding()
            if holding != sprite.holding:
                sprite.update_image(holding)
                any_update = True
        return any_update

    def players_move(self):
        for player, sprite in self.p_sprites.items():
            sprite.update_position(player.x, player.y)

    def players_moving(self, dt: float, speed: float):
        # print('moving', dt)
        finished = True
        for player, sprite in self.p_sprites.items():
            x, y = sprite.x, sprite.y
            dx, dy = player.x - x, player.y - y
            if dx != 0:
                d_ = dt * speed
                if d_ > abs(dx):
                    x = player.x
                else:
                    finished = False
                    x += d_ if dx > 0 else -d_
                sprite.update_position(x=x)
            if dy != 0:
                d_ = dt * speed
                if d_ > abs(dy):
                    y = player.y
                else:
                    finished = False
                    y += d_ if dy > 0 else -d_
                sprite.update_position(y=y)
        return finished
