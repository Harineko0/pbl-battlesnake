"""greedyなアルゴリズムに使う関数用のファイル
"""
from dataclasses import dataclass, field
import queue
from typing import Any

from greedy_snake.Helper import getCoordinateAround
from greedy_snake.Helper import heuristic
from greedy_snake.Helper import neededDirection
from greedy_snake.Helper import printMap
from greedy_snake.Settings import AROUND_FOOD_VALUE
from greedy_snake.Settings import CANNOT_EAT_FOOD_VALUE
from greedy_snake.Settings import MOVES
from greedy_snake.Settings import NEG_INF


@dataclass(order=True)
class PrioritizedItem:
    """PriorityQueue用のdataclass

    https://docs.python.org/ja/3/library/queue.html#queue.PriorityQueue
    のコードに、
    priorityが同じ場合にサイン後に入れたものから処理するための変数countを足した
    """
    item: Any=field(compare=False)
    priority: int
    count: int=field(compare=True)


def canEatFood(
        map: list[list[int]], 
        snake_que: list[int,int],
        head_y: int, 
        head_x: int, 
        best_food: tuple[int,int], 
        health: int,
        moves: list[str]=MOVES
        ) -> bool:
    """(head_y, head_x)から特定のmovesの取り方でfoodを食べれるか判定する関数

    Greedy best firstを都合のいいように改変したアルゴリズムを用いて、
    そのルートで餌を食べた後死ぬことが確定しているならFalseを、そうでないならTrueを返す

    Greedy best firstについては以下のサイトを参考にした
    https://www.redblobgames.com/pathfinding/a-star/introduction.html
    """
    start = (head_y,head_x)
    goal = best_food

    # frontierにはこれから処理するマスと、その優先順位が入る
    # priorityが同じ場合は、putした順でpopされる
    frontier = queue.PriorityQueue()
    frontier.put(PrioritizedItem(item=start,priority=0,count=10000))
    # came_fromにはそのマスにどこからたどり着いたのかが記録される
    came_from = dict() #パスA->B はcame_from[B] == Aとして保存される
    came_from[start] = None
    # cost_so_farには、そのマスに行くまでにかかったターン数が保存される
    cost_so_far = dict()
    cost_so_far[start] = 0
    
    # 変数の初期化.mapとqueueをコピーして1ターン分進める
    copied_map = map.copy()
    copied_snake_queue = snake_que.copy()
    copied_map[copied_snake_queue[0]] = 0
    copied_snake_queue.pop(0)
    copied_map[start] = NEG_INF
    copied_snake_queue.append(start)

    # PriorityQueueのpriorityが同じ場合に、countの大きさの順で返す
    count = 9999
    # ターン経過後にmapを更新するためのターン経過判定用の変数を初期化
    turn_count = 0

    while not frontier.empty():
        # currentに最もpriorityが高い座標を代入.priorityが同じ場合は入れた順で返される
        current = frontier.get().item
        # 使わなかったfrontierの要素はfeontierとcame_fromから消す
        while not frontier.empty():
            coord = frontier.get().item
            del(came_from[coord])

        if current == goal:
            break

        for  next_y,next_x in (getCoordinateAround(y=current[0],x=current[1],moves=moves)):
            # (next_y,next_x)が探索に値するなら、変数を更新する
            if (next_y,next_x) not in came_from and (copied_map[next_y,next_x] >= 0 or (next_y,next_x) == goal):
                priority = heuristic(head_x=next_x,head_y=next_y,goal_x=goal[1],goal_y=goal[0])
                frontier.put(PrioritizedItem(item=(next_y,next_x),priority=priority,count=count))
                count -= 1
                came_from[next_y,next_x] = current    
        
        # ターンが経過していた場合、mapを更新する
        turn_count += 1
        if copied_snake_queue:
            copied_map[copied_snake_queue[0]] = 0
            copied_snake_queue.pop(0)
        # healthがgoalに到達するためのターン数より少ないならFalseを返す
        if health - turn_count < 0:
            return False

    # goalにたどり着くのが不可能ならFalseを返す
    if goal not in came_from:
        return False

    # 餌に到達した時点のheatmapを再現するために、変数を初期化
    temporary_map = map.copy()
    current = goal
    temporary_snake_queue = snake_que.copy()
    temporary_snake_queue.append(current)
    i = 1

    # 餌に到達した時点のheatmapを再現する
    while current != start and i <= len(snake_que):
        temporary_map[snake_que[i - 1]] = 0
        temporary_snake_queue.pop(0)
        temporary_snake_queue.insert(-i,came_from[current])
        i += 1
        temporary_map[current] = NEG_INF
        current = came_from[current]
    
    temporary_map[current] = NEG_INF

    print(f"temporary_map:{head_y,head_x}")
    print(f"moves:{moves}")
    printMap(map=temporary_map)

    # 再現したheatmapを基に、その後死ぬことが確定しているかを判定し、死ぬならFalseを返す
    if not canReachTail(map=temporary_map,start=goal,snake_que=temporary_snake_queue):
        return False
    
    print("ok")
    return True


def updateMapByCanEatFood(
        map: list[list[int]], 
        snake_que: list[int,int], 
        best_food: tuple[int,int], 
        health: int
        ):
    """CanEatFood()をheadの周囲4マスに適用する関数
    """
    temporary_map = map.copy()
    # headの周囲のマスについてcanEatFood()を適用する
    for list in getCoordinateAround(y=snake_que[-1][0],x=snake_que[-1][1]):
            y,x = list
            # valが0未満ならそもそも行くことはないと思われるので調べない
            if map[y, x] >= 0:
                # canEatfoodをneededDirection()の全movesに対して適用する
                moves = neededDirection()
                for _ in range(0,2):
                    if not canEatFood(map=temporary_map,snake_que=snake_que,
                                      best_food=best_food,health=health - 1,
                                      head_y=y,head_x=x,moves=next(moves)):
                        map[y, x] = CANNOT_EAT_FOOD_VALUE
                    else:
                        map[y,x] = 0

                        # foodの隣に行くと間違って食べかねないので優先度を下げる
                        for next_y,next_x in getCoordinateAround(y,x):
                            if (next_y,next_x) == best_food:
                                map[y,x] += AROUND_FOOD_VALUE

                        break


def canReachTail(map: list[list[int]], 
               start: tuple[int,int],
               snake_que: list[int,int],
               pass_through_val: int = 0
               ) -> bool | tuple[int,int]:
    """mapからtailにたどりつけるかを判定する関数

    Greedy Best Firstでtailにいけるか判定する

    tailに行けるならtailに向かうための次の座標を返す
    
    tailに行けないのならFalseを返す
    """
    # goalはtail
    goal = (snake_que[0][0],snake_que[0][1])
    
    # frontierにはこれから処理するマスと、その優先順位が入る
    # priorityが同じ場合は、putした順でpopされる
    frontier = queue.PriorityQueue()
    frontier.put(PrioritizedItem(item=start,priority=0,count=10000))
    # came_fromにはそのマスにどこからたどり着いたのかが記録される
    came_from = dict() #パスA->B はcame_from[B] == Aとして保存される
    came_from[start] = None
    
    # 変数の初期化.
    copied_map = map.copy()

    # PriorityQueueのpriorityが同じ場合に、countの大きさの順で返す
    count = 9999

    while not frontier.empty():
        # currentに最もpriorityが高い座標を代入.priorityが同じ場合は入れた順で返される
        current = frontier.get().item

        if current == goal:
            break

        for  next_y,next_x in (getCoordinateAround(y=current[0],x=current[1])):
            # (next_y,next_x)が探索に値するなら、変数を更新する
            if (next_y,next_x) not in came_from and (copied_map[next_y,next_x] >= pass_through_val or (next_y,next_x) == goal):
                priority = heuristic(head_x=next_x,head_y=next_y,goal_x=goal[1],goal_y=goal[0])
                frontier.put(PrioritizedItem(item=(next_y,next_x),priority=priority,count=count))
                count -= 1
                came_from[next_y,next_x] = current

    # tailにたどり着くのが不可能ならFalseを返す
    if goal not in came_from:
        return False
    
    # startからtailへの経路をpathに保存する
    current = goal 
    path = []
    while current != start: 
        path.append(current)
        current = came_from[current]
    
    # tailにたどり着ける方向への座標を返す
    return path[-1]
