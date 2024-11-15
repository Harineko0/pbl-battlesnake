import math
import numpy as np
from typing import Optional
from numpy.typing import NDArray
import logging
from logging import getLogger

moves = ["down", "up", "left", "right"]

PROHIBIT_SCORE = -1024
EDGE_SCORE = -10
DEADEND_SCORE = -1024
FOOD_SCORE = 512
FOOD_NEARBY_SCORE = 6
TAIL_SCORE = 256

# logging.basicConfig(filename="", level=logging.DEBUG)
# logger = getLogger(__name__)


# ヒートマップ class. 正の方が好ましい
class HeatMap:
    def __init__(self, width: int, height: int) -> None:
        w = width + 2
        h = height + 2

        # size + 1 の int8 型正方2次元配列を生成
        border_map = np.zeros((w, h), dtype=np.int16)

        # 端はあまり行きたくない
        border_map[1] = EDGE_SCORE
        border_map[-2] = EDGE_SCORE
        border_map[:, 1] = EDGE_SCORE
        border_map[:, -2] = EDGE_SCORE

        # 枠外は行かない
        ## row
        border_map[0] = PROHIBIT_SCORE
        border_map[-1] = PROHIBIT_SCORE
        ## column
        border_map[:, 0] = PROHIBIT_SCORE
        border_map[:, -1] = PROHIBIT_SCORE

        # set maps
        self._border_map = border_map
        self._snake_map = np.zeros((w, h), dtype=np.int16)
        self._food_map = np.zeros((w, h), dtype=np.int16)
        self._deadend_map = np.zeros((w, h), dtype=np.int16)
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
        map += self._deadend_map * DEADEND_SCORE
        print(map)

        maxVal = PROHIBIT_SCORE
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

        snake_map[h_y + 1, h_x + 1] = PROHIBIT_SCORE
        queue.append(head)

        t_x, t_y = tail

        # 最初のみしっぽの位置を設定
        # if len(queue) <= 1:
        #     snake_map[t_y + 1, t_x + 1] = PROHIBIT_SCORE
        #     queue.append(tail)

        # しっぽの位置が変わった (食べ物食べてない)
        if queue[-1] != tail and len(queue) > 2:
            # reset
            snake_map[t_y + 1, t_x + 1] = 0
            # snake_map[t_y + 1, t_x + 1] = TAIL_SCORE
            # old_tail = queue.pop(0)
            # ot_x, ot_y = old_tail
            # snake_map[ot_y + 1, ot_/x + 1] = 0

    def updateMapByFood(
        self,
        foods: list[dict[str, int]],
        head: tuple[int, int],
        health: int,
        # head: dict[str, int],
    ) -> Optional[tuple[int, int]]:
        food_map = self._food_map
        snake_map = self._snake_map
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

            # stop if snake is there
            if snake_map[y, x] < 0:
                return

            old_score = food_map[y, x]
            food_map[y, x] = (
                max(score, old_score) if score > 0 else min(score, old_score)
            )

            # 重要度 (score) が高いなら
            # if abs(score) > abs(cell):
            #     food_map[y, x] = score

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
        nearest_food_dist = getNearbyFoodDist()
        print(f"nearest_food_dist: {nearest_food_dist}, foods: { foods }")
        if health > nearest_food_dist + 2:
            # avoid foods
            for f in foods:
                f_x = f["x"] + 1
                f_y = f["y"] + 1
                updateByNearbyFood(f_x, f_y, -FOOD_NEARBY_SCORE)
                food_map[f_y, f_x] = -FOOD_SCORE
        # elif health > nearest_food_dist:
        #     # wander around food
        #     for f in foods:
        #         f_x = f["x"] + 1
        #         f_y = f["y"] + 1
        #         updateByNearbyFood(f_x, f_y, FOOD_NEARBY_SCORE)
        #         food_map[f_y, f_x] = -FOOD_SCORE

        else:
            # go to foods
            for f in foods:
                f_x = f["x"] + 1
                f_y = f["y"] + 1
                updateByNearbyFood(f_x, f_y, FOOD_NEARBY_SCORE)
                food_map[f_y, f_x] = FOOD_SCORE

        # print(f"food_map: \n{food_map}")

    def updateMapByDeadend(self, head: tuple[int, int]):
        prohibit_map = np.zeros_like(self._border_map)
        prohibit_map += self._border_map
        prohibit_map += self._snake_map
        prohibit_map += self._food_map

        all_area_map = np.zeros_like(prohibit_map)
        area_array_maps = {
            "up": np.zeros_like(prohibit_map),
            "down": np.zeros_like(prohibit_map),
            "left": np.zeros_like(prohibit_map),
            "right": np.zeros_like(prohibit_map),
        }

        width = len(prohibit_map[0])
        height = len(prohibit_map)

        def search(x: int, y: int, area_map: NDArray) -> int:
            # out of board
            if (
                x < 0
                or y < 0
                or x >= width
                or y >= height
                or prohibit_map[y, x] <= PROHIBIT_SCORE
            ):
                return 0

            # 探索済み
            if all_area_map[y, x] != 0:
                return 0

            area_map[y, x] = 1
            all_area_map[y, x] = 1

            return (
                search(x, y - 1, area_map)
                + search(x, y + 1, area_map)
                + search(x - 1, y, area_map)
                + search(x + 1, y, area_map)
            ) + 1

        h_x = head[0] + 1
        h_y = head[1] + 1
        area_map = {
            "up": search(h_x, h_y + 1, area_array_maps["up"]),
            "down": search(h_x, h_y - 1, area_array_maps["down"]),
            "left": search(h_x - 1, h_y, area_array_maps["left"]),
            "right": search(h_x + 1, h_y, area_array_maps["right"]),
        }
        print(f"head: {head}")
        # print(f"all_area_map: \n{all_area_map}")
        # print(f"prohibit_map: \n{prohibit_map}")
        # print(f"area_count_map: {area_map}")
        # print(
        #     f"up: \n{area_array_maps['up']}, \ndown: \n{area_array_maps['down']}, \nleft: \n{area_array_maps['left']}, \nright: \n{area_array_maps['right']}"
        # )

        # 最小面積の方向を探す
        min_area = math.inf
        area_count = 0
        dir = ""

        for key, area in area_map.items():
            if area > 0:
                area_count += 1

                if area < min_area:
                    min_area = area
                    dir = key

        # print("min_area: ", min_area, "dir: ", dir)
        # 最小面積の方向には行かない
        if dir != "" and area_count > 1:
            self._deadend_map = area_array_maps[dir]
