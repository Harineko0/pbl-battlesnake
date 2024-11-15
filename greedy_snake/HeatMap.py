"""greedysnakeに用いるヒートマップ用のファイル
"""

import numpy as np

from greedy_snake.Greedy import updateMapByCanEatFood
from greedy_snake.Greedy import canReachTail
from greedy_snake.Helper import getBestDirection
from greedy_snake.Helper import getBestFood
from greedy_snake.Helper import getCoordinateAround
from greedy_snake.Helper import printMap
from greedy_snake.Settings import FOOD_VALUE
from greedy_snake.Settings import NEG_INF
from greedy_snake.Settings import OUTSIDE_THE_FRAME_VALUE


# ヒートマップ class. 正の方が好ましい
class HeatMap:
    def __init__(self, width: int, height: int) -> None:
        # size + 1 の int8 型正方2次元配列を生成
        map = np.zeros((width + 2, height + 2), dtype=np.int8)

        # 端は負の無限
        ## row
        map[0] = OUTSIDE_THE_FRAME_VALUE
        map[height + 1] = OUTSIDE_THE_FRAME_VALUE
        ## column
        map[:, 0] = OUTSIDE_THE_FRAME_VALUE
        map[:, width + 1] = OUTSIDE_THE_FRAME_VALUE

        # set members
        self._map = map
        self._width = width + 2
        self._height = height + 2
        # ヘビが動いた座標のキュー
        self._snake_queue = []
        self._old_snake_queue = []
        # snakeがfoodを食べたかを判定するためのtuple.後で代入する.
        self._last_food = ()

        pass


    def getSafeMove(self, head_y: int, head_x: int, health: int, turn: int,
                    foods: list[dict["x" : int, "y" : int]],
                    ) -> str:
        x = head_x + 1
        y = head_y + 1

        # 範囲外
        if x == 0 or y == 0 or x == self._width - 1 or y == self._height - 1:
            return ""
        
        temporary_map = self._map.copy()
        best_food = getBestFood(map=temporary_map,foods=foods)

        strat_finding_food_turn = self._height + self._width + len(self._snake_queue)

        if strat_finding_food_turn > 36:
            strat_finding_food_turn = 36

        # foodを食べられるかどうかでmapを更新
        # healthが一定以下ならheadからfoodを経由してtailに向かう経路を探索する
        if (health <= strat_finding_food_turn) or (len(self._snake_queue) <= 3):
            updateMapByCanEatFood(map=temporary_map,snake_que=self._snake_queue,
                                best_food=best_food, health=health
                                )
        else:
            # healthが一定以上ならtailを追いかける
            next_path = canReachTail(map=temporary_map,start=(y,x),snake_que=self._old_snake_queue)
            if next_path != False:
                temporary_map[next_path] += 10
            # 途中で餌を食べざるを得ない場合は途中で餌を食べる経路も探索する
            else:
                next_path = canReachTail(map=temporary_map,start=(y,x),snake_que=self._old_snake_queue,pass_through_val=FOOD_VALUE)
                temporary_map[next_path] += 10

        # headの周りにFOOD_VALUE未満の値のマスしかなかった場合、tailを追いかける
        num_of_dead_space = 0
        for  next_y,next_x in (getCoordinateAround(y=y,x=x)):
            if temporary_map[next_y,next_x] < FOOD_VALUE:
                num_of_dead_space += 1

        if num_of_dead_space == 4:
            next_path = canReachTail(map=self._map,start=(y,x),snake_que=self._old_snake_queue)
            if next_path != False:
                temporary_map[next_path] = 10
            else:
                next_path = canReachTail(map=self._map,start=(y,x),snake_que=self._old_snake_queue,pass_through_val=FOOD_VALUE)
                temporary_map[next_path] = 10

        #そのターンの最終的なhotmapを表示
        print(f"head:{y,x}")
        print(f"snake_queue{self._old_snake_queue}")
        printMap(map=temporary_map)

        # 隣接するマスで最も大きいvalの方向へ行く
        # 大きさが同じならmovesの順で選ぶ
        return getBestDirection(map=temporary_map, head_y=y, head_x=x)


    def updateMapByMoving(self, head_y: int, head_x: int,
                          tail_y: int, tail_x: int, turn: int,
                          foods: list[dict["x" : int, "y" : int]]
                          ):
        heatmap_head = (head_y + 1, head_x + 1)
        heatmap_tail = (tail_y + 1, tail_x + 1)

        self._snake_queue.append(heatmap_head)
        self._old_snake_queue = self._snake_queue.copy()
        self._map[*heatmap_head] = NEG_INF

        if turn == 0:
            for food in foods:
                self._map[food["y"] + 1, food["x"] + 1] = FOOD_VALUE
        elif turn == 1:
            self._last_food = (foods[-1]["y"] + 1, foods[-1]["x"] + 1)

            for food in foods:
                self._map[food["y"] + 1, food["x"] + 1] = FOOD_VALUE
        elif self._last_food != (foods[-1]["y"] + 1, foods[-1]["x"] + 1):
            self._last_food = (foods[-1]["y"] + 1, foods[-1]["x"] + 1)

            self._map[self._last_food] = FOOD_VALUE
            
            self._map[*heatmap_tail] = NEG_INF
        elif self._snake_queue[0] == heatmap_tail:
            self._map[*heatmap_tail] = 0
            self._snake_queue.pop(0)
        else:
            self._map[*heatmap_tail] = NEG_INF
