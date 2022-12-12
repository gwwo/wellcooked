
import gym
from gym import spaces
import numpy as np
from typing import Union
import config
from game import Action, Game
from roles import Ingredient, Server

from game_ui import GameUI

empty_counter = np.array([
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
], dtype=np.float32)

onion_counter = np.array([
    [1, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 1],
], dtype=np.float32)

onion_on_counter = np.array([
    [1, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 1],
], dtype=np.float32)

server_counter = np.array([
    [1, 1, 1, 1],
    [1, 1, 0, 1],
    [1, 0, 1, 1],
    [1, 1, 1, 1],
], dtype=np.float32)

chef_north = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 0, 0, 0],
], dtype=np.float32)


chef_north_with_onion = np.array([
    [0, 1, 1, 0],
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [0, 0, 0, 0],
], dtype=np.float32)


class GameEnv(gym.Env):
    metadata = {'render_modes': ['human', 'ansi'], 'human_mode_move_speed': 4.0}

    def __init__(self, layout_name: str, period=50, truncate_period=False, render_mode=None):
        assert render_mode is None or render_mode in self.metadata['render_modes']
        self.render_mode = render_mode

        assert layout_name.startswith('simple'), 'currently only support simple versions of the game'
        self.game = Game(*config.load(layout_name), move_to_axis=True)
        assert len(self.game._players) == 1, 'currently only support 1 player'
        self.player_id = self.game._players[0].id

        # self.action_space = spaces.Dict({player.id: spaces.Discrete(len(Action)) for player in self.game._players})
        self.action_space = spaces.Discrete(len(Action))

        w, h = self.game.kitchen_w, self.game.kitchen_h
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(h*4, w*4), dtype=np.float32)
        self.window = None

        self.step_count = 0
        self.period = period
        self.truncate_period = truncate_period
        self.rewards_over_period = 0.0

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.game.reset()
        self.step_count = 0
        obs, info = self.observe(), dict()
        if self.render_mode == 'human':
            if self.window == None:
                self.window = GameUI(self.game)
            else:
                self.window.fresh()
        return obs, info


    def step(self, action):

        feedbacks = self.game.step({self.player_id: Action(value=action)})

        reward = sum(feedbacks.values())
        terminated, truncated, info = False, False, dict()
        obs = self.observe()

        self.rewards_over_period += reward
        self.step_count += 1

        if self.step_count % self.period == 0:
            truncated = self.truncate_period
            info['rewards_over_period'] = self.rewards_over_period
            self.rewards_over_period = 0.0

        if self.render_mode == 'human':
            self.window.sync()

        return obs, reward, terminated, truncated, info


    def render(self):
        if self.render_mode == 'ansi':
            obs = self.observe()
            return '\n'.join(
                ''.join('  ' if v == 0.0 else '██' for v in r)
                for r in obs
            )

    def observe(self):
        w, h = self.game.kitchen_w, self.game.kitchen_h
        obs = np.zeros((h*4, w*4), dtype=np.float32)
        for x in range(w):
            for y in range(h):
                counter = self.game.kitchen[x][y]
                if counter != None:
                    if counter.holding == None:
                        pseudo_img = empty_counter
                    elif type(counter.holding) is Ingredient:
                        if counter.new_one_to_dispense:
                            pseudo_img = onion_counter
                        else:
                            pseudo_img = onion_on_counter
                    elif type(counter.holding) is Server:
                        pseudo_img = server_counter
                    x_, y_ = 4*(h-1-y), 4*x
                    obs[x_:x_+4, y_:y_+4] = pseudo_img
        for player in self.game.players:
            x, y, facing, holding = player.x, player.y, player.facing, player.holding
            if holding == None:
                pseudo_img = chef_north
            else:
                pseudo_img = chef_north_with_onion
            if facing == 'south':
                pseudo_img = np.flip(pseudo_img,  0)
            elif facing == 'west':
                pseudo_img = np.transpose(pseudo_img)
            elif facing == 'east':
                pseudo_img = np.flip(np.transpose(pseudo_img), 1)
            x_, y_ = int(4*(h-1-y)), int(4*x)
            obs[x_:x_+4, y_:y_+4] = pseudo_img
        return obs

    def close(self):
        if self.window != None:
            self.window.close()


def make_env():
    def thunk():
        env = GameEnv('simple/circuit_room')
        return env
    return thunk


if __name__ == '__main__':

    env = gym.vector.SyncVectorEnv([make_env() for i in range(5)])

    obs, info = env.reset()

    for _ in range(200):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)

        if 'rewards_over_period' in info:
            print(info['rewards_over_period'], info['_rewards_over_period'])

    for single_env in env.envs:
        print(single_env.action_space, single_env.observation_space)


    print()