

import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical

import numpy as np

from game_env import GameEnv
from game_env.serialize import SerializeWrapper


# model_name = "circuit_room_2__1671437407"
model_name = "circuit_room_8__1671546995"

layout_name = model_name.split("__")[0]

layout_name = "circuit_room_10"

def layer_init(layer, std=np.sqrt(2), bias_const=0.0):
    torch.nn.init.orthogonal_(layer.weight, std)
    torch.nn.init.constant_(layer.bias, bias_const)
    return layer


class Agent(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            layer_init(nn.Conv2d(1, 16, 5, stride=1)), # 25
            nn.ReLU(),
            layer_init(nn.Conv2d(16, 32, 3, stride=3)), # 12
            nn.ReLU(),
            layer_init(nn.Conv2d(32, 32, 2, stride=1)), # 8
            nn.ReLU(),
            nn.Flatten(),
            layer_init(nn.Linear(32 * 11 * 6, 512)),
            nn.ReLU(),
        )
        self.actor = layer_init(nn.Linear(512, 6), std=0.01)
        self.critic = layer_init(nn.Linear(512, 1), std=1)

    def get_value(self, x):
        return self.critic(self.network(torch.unsqueeze(x, 1)))

    def get_action_and_value(self, x, action=None):
        x = torch.unsqueeze(x, 1)
        hidden = self.network(x)
        logits = self.actor(hidden)
        probs = Categorical(logits=logits)
        if action is None:
            action = probs.sample()
        return action, probs.log_prob(action), probs.entropy(), self.critic(hidden)




if __name__ == "__main__":

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    env = GameEnv(layout_name, render_mode="human", window_caption=model_name)
    env = SerializeWrapper(env)

    agent = Agent().to(device)
    agent.load_state_dict(torch.load(f"./trained/{model_name}.pth"))
    agent.eval()

    obs, info = env.reset()
    frozen = True
    while not env.unwrapped.window.is_closed:
        if frozen:
            env.unwrapped.window.listen_until()
            frozen = False
        obs = torch.Tensor(obs).to(device)
        action, logprob, _, value = agent.get_action_and_value(obs)
        obs, reward, done, truncated, info = env.step(action.cpu().numpy())








