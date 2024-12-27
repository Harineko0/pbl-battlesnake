import random
import typing
from environment import RemoteEnv
from agent import Agent

env = RemoteEnv(ally_id="ally", opponent_id="opponent")
agent = Agent(id="ally")
actions = ["up", "down", "left", "right"]
direction = ['←', '→', '↑', '↓']

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "PBL7",
        "color": "#3FA254",
        "head": "alligator",
        "tail": "alligator",
    }


def start(game_state: typing.Dict):
    print("GAME START")
    env.reset()

def end(game_state: typing.Dict):
    print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:
    env.set(game_state)
    state = env.get_state()
    action = agent.get_action(state)
    next_move = actions[action]
    env.render()

    print(f"MOVE {game_state['turn']}: {next_move} ({direction[action]})")
    return {"move": next_move}


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
