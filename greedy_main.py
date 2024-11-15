# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import typing

from greedy_snake.HeatMap import HeatMap


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "PBL7",  # TODO: Your Battlesnake Username
        "color": "#3FA254",  # TODO: Choose color
        "head": "alligator",  # TODO: Choose head
        "tail": "alligator",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    global heat_map
    # initialize HeatMap
    heat_map = HeatMap(
        width=game_state["board"]["width"], height=game_state["board"]["height"]
    )
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    body = game_state["you"]["body"]
    my_head = body[0]
    my_tail = body[-1]

    heat_map.updateMapByMoving(head_x=my_head["x"], head_y=my_head["y"],
                               tail_x=my_tail["x"], tail_y=my_tail["y"],
                               turn=game_state["turn"],
                               foods=game_state["board"]["food"])

    next_move = heat_map.getSafeMove(head_x=my_head["x"], head_y=my_head["y"],
                                     health=game_state["you"]["health"],
                                     foods=game_state["board"]["food"],
                                     turn=game_state["turn"]
                                     )

    if next_move == "":
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        print()
        return {"move": "down"}

    print(f"MOVE {game_state['turn']}: {next_move}")
    print()
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
