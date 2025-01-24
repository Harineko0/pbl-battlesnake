from BoardScore import BoardScore
from Helpers import getSafeMoves

class BoardState:
    def __init__(self, 
                 my_body: list[tuple[int, int]],
                 enemy_body: list[tuple[int, int]],
                 my_health: int,
                 enemy_health: int,
                 foods: set[tuple[int, int]],
                 my_eat_food: tuple[int, int] = None
                 ):
        
        # set members
        self._my_body = my_body
        self._enemy_body = enemy_body
        self._my_health = my_health
        self._enemy_health = enemy_health
        self._foods = foods
        self._my_eat_food = my_eat_food


    def getScore(self) -> int:
        """
        盤面の評価を入手
        """
        board_score = BoardScore()

        # 自分と相手の頭の位置でどうかで更新
        board_score.updateScoreByHead(head=self._my_body[0], enemy=False)
        board_score.updateScoreByHead(head=self._enemy_body[0], enemy=True)
        board_score.updateScoreByGate(my_body=self._my_body, enemy_body=self._enemy_body)
        board_score.updateScoreByNumOfWays(head=self._my_body[0],my_body=self._my_body,enemy_body=self._enemy_body)
        # 蛇の長さで更新
        board_score.updateScoreByLength(my_body=self._my_body, enemy_body=self._enemy_body)
        
        # board_score.updateScoreByFood(my_body=self._my_body, enemy_body=self._enemy_body, foods=self._foods)
        board_score.updateScoreByDist(my_body=self._my_body, enemy_body=self._enemy_body)

        return board_score.score
        
    
    def youWin(self) -> bool:
        """
        勝ちを判定
        """
        return any([
            self._enemy_health <= 0,
            self._enemy_body[0] in self._enemy_body[1:],
            self._enemy_body[0] in self._my_body[1:],
            len(self._my_body) > len(self._enemy_body) and self._my_body[0] == self._enemy_body[0],
        ])
    

    def youLose(self) -> bool:
        """
        負け、引き分けを判定
        """
        return any([
            self._my_health <= 0,
            self._my_body[0] in self._my_body[1:],
            self._my_body[0] in self._enemy_body[1:],
            len(self._my_body) <= len(self._enemy_body) and self._my_body[0] == self._enemy_body[0],
        ])


    def getLegalMoves(self, depth) -> list[tuple[int, int]]:
        """
        depthが偶数なら自分のターン、奇数なら相手のターンとして合法手を返す
        """
        if (depth % 2 == 0):
            moves = getSafeMoves(head=self._my_body[0], neck = self._my_body[1])
        else:
            moves = getSafeMoves(head=self._enemy_body[0], neck = self._enemy_body[1])
        
        return moves


    def next(self, move: tuple[int, int], depth: int):
        """
        次の盤面を取得
        """
        if (depth % 2 == 1):
            my_body = self._my_body.copy()
            my_body.insert(0, move)
            my_eat_food = None
            if move in self._foods:
                my_eat_food = move
                my_health = 100
            else:
                my_body.pop()
                my_health =  self._my_health -1

            return BoardState(my_body=my_body, 
                              enemy_body=self._enemy_body,
                              my_health=my_health,
                              enemy_health=self._enemy_health,
                              foods=self._foods,
                              my_eat_food=my_eat_food
                              )
        else:
            enemy_body = self._enemy_body.copy()
            enemy_body.insert(0, move)
            foods = self._foods.copy()
            if move in self._foods:
                foods.remove(move)
                enemy_health = 100
            else:
                enemy_body.pop()
                enemy_health =  self._enemy_health -1

            my_eat_food = self._my_eat_food
            if my_eat_food in foods:
                foods.remove(my_eat_food)
        
            return BoardState(my_body=self._my_body, 
                              enemy_body=enemy_body,
                              my_health=self._my_health,
                              enemy_health=enemy_health,
                              foods=foods,
                              my_eat_food=my_eat_food
                              )