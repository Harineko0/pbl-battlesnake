"""helper関数用のファイル
"""

from greedy_snake.Settings import MOVES
from greedy_snake.Settings import NEG_INF

def neededDirection():
    """探索する必要のあるmovesの取り方を返す関数

    多分これで十分だと思います
    """
    yield ["up", "right", "down", "left"]
    yield ["left", "down", "right", "up"]


def heuristic(head_x: int,head_y: int,goal_x: int, goal_y: int) -> int:
    """headとgoalの到達距離を返す関数
    """
    return abs(head_x - goal_x) + abs(head_y - goal_y)

def getBestFood(map: list[list[int]], foods: list[dict["x" : int, "y" : int]]) -> tuple[int, int]:
    """best_boodを返す関数

    基本は最も下で、その中で最も右のfoodを返す
    そのfoodが枠やほかのfoodで包囲されている場合、包囲されていないfoodを返す
    """
    sorted_food = sorted(foods, key=lambda food: (food["y"], food["x"]))

    for food in sorted_food:
         i = 0
         for y,x in getCoordinateAround(food["y"] + 1, food["x"] + 1):
            if (map[(y,x)] >= 0) or (map[(y,x)] == NEG_INF):
                i += 1
            
            if i > 1:
                return (food["y"] + 1, food["x"] + 1)
    
    return (sorted_food[0]["y"] + 1, sorted_food["x"] + 1)


def getBestDirection(map: list[list[int]], head_y: int, head_x: int) -> str:
    """mapの最も大きいvalへのdirecyionを返す関数
    """
    maxVal = -128
    dir = ""
    
    for i, list in enumerate(getCoordinateAround(y=head_y,x=head_x)):
        y,x = list
        if  map[y,x] > maxVal:
                maxVal = map[y,x]
                dir = MOVES[i]

    return dir


def printMap(map: list[list[int]]):
    """マップを正しい座標の取り方で出力する関数
    """
    for i in range(len(map) - 1, -1, -1):
        print(map[i])


def getCoordinateAround(y: int, x: int, moves = MOVES) -> list[int]:
    """(y, x) の周りの座標を MOVES の順で返す関数
    """

    dir_dict = {"down" : (y - 1, x), "up" : (y + 1, x), 
                "left" : (y, x - 1), "right" : (y, x + 1)}

    return [dir_dict[dir] for dir in moves]
