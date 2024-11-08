import numpy as np
from typing import Optional

moves = ["down", "up", "left", "right"]
NEG_INF: int = -128


# ヒートマップ class. 正の方が好ましい
class HeatMap:
    def __init__(self, width: int, height: int) -> None:
        w = width + 2
        h = height + 2

        # size + 1 の int8 型正方2次元配列を生成
        border_map = np.zeros((w, h), dtype=np.int16)

        # 端は負の無限
        ## row
        border_map[0] = NEG_INF
        border_map[-1] = NEG_INF
        ## column
        border_map[:, 0] = NEG_INF
        border_map[:, -1] = NEG_INF

        # set maps
        self._border_map = border_map
        self._snake_map = np.zeros((w, h), dtype=np.int16)
        self._food_map = np.zeros((w, h), dtype=np.int16)
        self._map = np.zeros((w, h), dtype=np.int16)

        # ヘビが動いた座標のキュー
        self._snake_queue = []
        self._food_queue: list[tuple[int, int]] = []

        pass

    """
    x, y の上下左右で最良な方向を返す
    """

    def getSafeMove(self, coord: tuple[int, int]) -> str:
        x = coord[0] + 1
        y = coord[1] + 1

        width = len(self._border_map[0])
        height = len(self._border_map)
        # 範囲外
        if x == 0 or y == 0 or x == width - 1 or y == height - 1:
            return ""

        map = self._map
        map.fill(0)
        map += self._food_map
        map += self._snake_map
        map += self._border_map
        print(map)

        maxVal = NEG_INF
        dir = ""

        for i, val in enumerate(
            # down, up, left, right
            [map[y - 1, x], map[y + 1, x], map[y, x - 1], map[y, x + 1]]
        ):
            if val > maxVal:
                maxVal = val
                dir = moves[i]

        return dir

    def updateMapByMoving(self, head: tuple[int, int], tail: tuple[int, int]):
        queue = self._snake_queue
        snake_map = self._snake_map

        h_x, h_y = head
        t_x, t_y = tail

        snake_map[h_y + 1, h_x + 1] = NEG_INF
        queue.append(head)

        # 最初のみしっぽの位置を設定
        # if len(queue) <= 1:
        #     snake_map[t_y + 1, t_x + 1] = NEG_INF
        #     queue.append(tail)

        # しっぽの位置が変わった
        if queue[-1] != tail and len(queue) > 2:
            t_x, t_y = tail
            # reset
            snake_map[t_y + 1, t_x + 1] = 0
            queue.pop(0)

    def updateMapByFood(
        self,
        foods: list[dict[str, int]],
        head: tuple[int, int],
        health: int,
        # head: dict[str, int],
    ) -> Optional[tuple[int, int]]:
        food_map = self._food_map
        food_queue = self._food_queue

        # initialize
        if not food_queue:
            for f in foods:
                food_queue.append((f["x"], f["y"]))
        else:
            # remove eaten food
            q_head = food_queue[0]
            f_head = foods[0]
            if q_head != (f_head["x"], f_head["y"]):
                food_queue.pop(0)
                print(f"q_head: {q_head}")
                x = q_head[0]
                y = q_head[1]
                food_map[y + 1, x + 1] = 0

            # add new food
            new_foods = []
            q_tail = food_queue[-1]
            for f in reversed(foods):
                if (f["x"], f["y"]) == q_tail:
                    break
                new_foods.append((f["x"], f["y"]))
            new_foods.reverse()
            food_queue.extend(new_foods)

        width = len(food_map[0])
        height = len(food_map)

        def updateByNearbyFood(x: int, y: int, score: int):
            if score == 0 or x == 0 or y == 0 or x == width - 1 or y == height - 1:
                return

            cell = food_map[y, x]

            # 既に設定済みまたは範囲外
            if cell == NEG_INF:
                return

            # 重要度 (score) が高いなら
            if abs(score) > abs(cell):
                food_map[y, x] = score

            next_score = score - 1 if score > 0 else score + 1

            updateByNearbyFood(x - 1, y, next_score)
            updateByNearbyFood(x + 1, y, next_score)
            updateByNearbyFood(x, y - 1, next_score)
            updateByNearbyFood(x, y + 1, next_score)

        def getNearbyFoodDist() -> tuple[int, int]:
            h_x, h_y = head
            max_dist = 0
            for f in foods:
                dist = abs(f["x"] - h_x) + abs(f["y"] - h_y)
                max_dist = max(max_dist, dist)

            return max_dist

        # health が n 以上のときは食べない
        food_map.fill(0)
        f_y = f["y"] + 1
        f_x = f["x"] + 1
        nearest_food_dist = getNearbyFoodDist()
        print(f"nearest_food_dist: {nearest_food_dist}")
        if health > nearest_food_dist:
            for f in foods:
                updateByNearbyFood(f_x, f_y, -6)
                food_map[f_y, f_x] = -6
        else:
            for f in foods:
                updateByNearbyFood(f_x, f_y, 6)
                food_map[f_y, f_x] = 6
