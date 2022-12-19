

With `python="^3.9"` `pyglet="^2.0.0"` installed, 

Play with GameUI

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

Interact with GameEnv

```py
from game_env import GameEnv
from game_env.observe import show

env = GameEnv("circuit_room_2", render_mode="human")

obs, info = env.reset()

while not env.window.is_closed:
    action = env.window.listen_until()
    obs, reward, terminated, truncated, info = env.step(action)
    for player_id, ob in obs.items():
        print('\n', player_id)
        print(show(ob))  # print ascii map for pseudo-pixel observation
```

After certain steps, the environment state is rendered as the following frame in the ui window:


Meanwhile, the ascii representation of the two players' observations is printed as below:

```
 1
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
GG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GG
GG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GG
GG      GGGG      GGGG      GGGGGG  GGGGGGGG  GGGGGG      GGGG      GGGG      GG
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
GGGGGGGGGG                                                            GGGGGGGGGG
GG      GG                    GG      GG                              GG      GG
GG      GG                    GG      GG                              GG      GG
GG      GG                      GG  GG                                GG      GG
GGGGGGGGGG                        GG                                  GGGGGGGGGG
GGGGGGGGGG          GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG          GGGGGGGGGG
GG      GG          GG      GGGG      GGGG      GGGG      GG          GG  GG  GG
GGGGGGGGGG          GG      GGGG      GGGG      GGGG      GG          GGGG  GGGG
GG      GG          GG      GGGG      GGGG      GGGG      GG          GG  GG  GG
GGGGGGGGGG          GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG          GGGGGGGGGG
GGGGGGGGGG              ████                                          GGGGGGGGGG
GG      GG            ██                                              GG      GG
GG      GG          ██████                                            GG      GG
GG      GG            ██                                              GG      GG
GGGGGGGGGG              ████                                          GGGGGGGGGG
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
GG      GGGG      GGGG      GGGGGGGGGGGGGGGGGGGGGGGG      GGGG      GGGG      GG
GG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GG
GG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GG
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG

 2
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
GG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GG
GG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GG
GG      GGGG      GGGG      GGGGGG  GGGGGGGG  GGGGGG      GGGG      GGGG      GG
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
GGGGGGGGGG                                                            GGGGGGGGGG
GG      GG                    ██      ██                              GG      GG
GG      GG                    ██      ██                              GG      GG
GG      GG                      ██  ██                                GG      GG
GGGGGGGGGG                        ██                                  GGGGGGGGGG
GGGGGGGGGG          GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG          GGGGGGGGGG
GG      GG          GG      GGGG      GGGG      GGGG      GG          GG  GG  GG
GGGGGGGGGG          GG      GGGG      GGGG      GGGG      GG          GGGG  GGGG
GG      GG          GG      GGGG      GGGG      GGGG      GG          GG  GG  GG
GGGGGGGGGG          GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG          GGGGGGGGGG
GGGGGGGGGG              GGGG                                          GGGGGGGGGG
GG      GG            GG                                              GG      GG
GG      GG          GGGGGG                                            GG      GG
GG      GG            GG                                              GG      GG
GGGGGGGGGG              GGGG                                          GGGGGGGGGG
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
GG      GGGG      GGGG      GGGGGGGGGGGGGGGGGGGGGGGG      GGGG      GGGG      GG
GG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GG
GG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GGGG      GG
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
```