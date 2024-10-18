import numpy as np
import math

moves = ["up", "down", "left", "right"]


# ヒートマップ class. 正の方が好ましい
class HeatMap:
    def __init__(self, width: int, height: int) -> None:
        # size + 1 の int8 型正方2次元配列を生成
        map = np.zeros((width + 2, height + 2), dtype=np.int8)

        # 端は負の無限
        ## row
        map[0] = -math.inf
        map[height + 1] = -math.inf
        ## column
        map[:0] = -math.inf
        map[: width + 1] = -math.inf

        # set members
        self._map = map
        self._width = width + 2
        self._height = height + 2
        # ヘビが動いた座標のキュー
        self._snake_queue = []

        pass

    """
    x, y の上下左右で最良な方向を返す
    """

    def getSafeMove(self, coord: tuple[int, int]) -> str:
        x = coord[0] + 1
        y = coord[1] + 1

        # 範囲外
        if x == 0 or y == 0 or x == self._width - 1 or y == self._height - 1:
            return ""

        map = self._map
        maxVal = -math.inf
        dir = ""

        for val, i in enumerate(
            # up, down, left, right
            [map[x + 1, y], map[x - 1, y], map[x, y - 1], map[x, y + 1]]
        ):
            if val > maxVal:
                maxVal = val
                dir = moves[i]

        return dir

    def updateValuesByMoving(self, head: tuple[int, int], tail: tuple[int, int]):
        queue = self._snake_queue
        queue.append(head)
        self._map[head[0], head[1]] = -math.inf

        # しっぽの位置が変わった
        if queue[-1] != tail:
            # 初期化. TODO: 0 ではなく正しいスコアを設定
            self._map[tail[0], tail[1]] = 0
            queue.pop(0)
