import gym
from gym import spaces
import numpy as np

import config

from game import Action, Game


from game_ui import GameUI

from .observe import observe, PIXELS_PER_UNIT


class GameEnv(gym.Env):
    metadata = {"render_modes": ["human"], "animation_speed_for_human": 6.0}

    def __init__(
        self, layout_name: str, period=50, truncate_period=False, render_mode=None
    ):
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.game = Game(*config.load(layout_name), move_to_axis=True)
        w, h = self.game.kitchen_w, self.game.kitchen_h

        self.player_ids = [p.id for p in self.game._players]
        self.player_N = len(self.player_ids)
        self.single_player_action_space = spaces.Discrete(len(Action))
        self.action_space = spaces.Dict(
            {p_id: self.single_player_action_space for p_id in self.player_ids}
        )
        self.single_player_observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(h * PIXELS_PER_UNIT, w * PIXELS_PER_UNIT),
            dtype=np.float32,
        )
        self.observation_space = spaces.Dict(
            {p_id: self.single_player_observation_space for p_id in self.player_ids}
        )

        self.window = None

        self.step_count = 0
        self.period = period
        self.truncate_period = truncate_period
        self.rewards_over_period = 0.0

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.game.reset()
        self.step_count = 0
        obs, info = observe(self.game), dict()
        if self.render_mode == "human":
            if self.window == None:
                self.window = GameUI(self.game)
            else:
                self.window.fresh()
        return obs, info

    def step(self, action: dict[str, int]):
        actions = {p_id: Action(value=index) for p_id, index in action.items()}

        feedbacks = self.game.step(actions)
        reward = sum(feedbacks.values())
        terminated, truncated, info = False, False, dict()

        obs = observe(self.game)
        self.rewards_over_period += reward
        self.step_count += 1

        if self.step_count % self.period == 0:
            truncated = self.truncate_period
            info["rewards_over_period"] = self.rewards_over_period
            self.rewards_over_period = 0.0

        if self.render_mode == "human":
            self.window.sync(self.metadata["animation_speed_for_human"])

        return obs, reward, terminated, truncated, info

    def close(self):
        if self.window != None and not self.window.is_closed:
            self.window.close()
