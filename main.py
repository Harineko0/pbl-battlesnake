"""
-07班
-Python 3.11.9 を動作確認に使用
-Flask==2.3.2 をインストールしています．
-↑requirements.txtに載せてあります
"""
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

import random
import typing

from AlphaBeta import alpha_beta_action
from BoardState import BoardState
from Helpers import getDirection

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
    global my_snake_number
    global enemy_snake_number
    if game_state["you"]["id"] == game_state["board"]["snakes"][0]["id"]:
        my_snake_number = 0
        enemy_snake_number = 1
    else:
        my_snake_number = 1
        enemy_snake_number = 0
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    snakes = game_state["board"]["snakes"]
    
    if len(snakes) == 1:
        print("Game finished (Only one snake left). Moving down")
        return {"move": "down"}
    
    my_body = [(body["x"], body["y"]) for body in game_state["board"]["snakes"][my_snake_number]["body"]]
    enemy_body = [(body["x"], body["y"]) for body in game_state["board"]["snakes"][enemy_snake_number]["body"]]
    foods = {(food["x"], food["y"]) for food in game_state["board"]["food"]}

    board_state = BoardState(my_body=my_body, 
                             enemy_body=enemy_body, 
                             my_health=game_state["board"]["snakes"][my_snake_number]["health"], 
                             enemy_health=game_state["board"]["snakes"][enemy_snake_number]["health"],
                             foods=foods
                            )
    
    next_move = alpha_beta_action(board_state=board_state)

    next_direction = getDirection(move=next_move, 
                                  my_head=(game_state["board"]["snakes"][my_snake_number]["body"][0]["x"],
                                           game_state["board"]["snakes"][my_snake_number]["body"][0]["y"])
                                  )
    
    if next_move == "":
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        print()
        return {"move": "down"}

    print(f"MOVE {game_state['turn']}: {next_direction}")
    my_head=(game_state["board"]["snakes"][my_snake_number]["body"][0]["x"],
             game_state["board"]["snakes"][my_snake_number]["body"][0]["y"])
    print(f"Head:{my_head}")
    print(f"next_move:{next_move}")
    print()
    return {"move": next_direction}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
