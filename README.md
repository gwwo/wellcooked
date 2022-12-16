

With `python="^3.9"` `pyglet="^2.0.0"` installed, 

play with GameUI

```py
from game_ui import GameUI
from game import Game
from config import load

game = Game(*load("simple/circuit_room"), move_to_axis=True, player_size=(1, 1))
game = Game(*load("big_room"), move_stride=0.08, player_size=(0.6, 0.96))
window = GameUI(game.reset())

while not window.is_closed:
    actions = window.listen_until()
    feedbacks = game.step(actions)
    for player_id, reward in feedbacks.items():
        if reward > 0:
            print(f"player_{player_id} just contributed {reward} point!")
    window.sync(speed=6.0)
```

interact with GameEnv

```py
from game_env import GameEnv
from game_env.observe import show

env = GameEnv("circuit_room_single", render_mode="human")

obs, info = env.reset()
while not env.window.is_closed:
    actions = env.window.listen_until()
    action = actions[env.player_id].value
    obs, reward, terminated, truncated, info = env.step(action)
    print(show(obs))  # print boolean map for pseudo-pixel observation
```