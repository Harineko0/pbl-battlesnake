from BoardScore import BoardScore
from Helpers import getSafeMoves

class BoardState:
    def __init__(self, 
                 my_body: list[tuple[int, int]],
                 enemy_body: list[tuple[int, int]],
                 my_health: int,
                 enemy_health: int,
                 foods: list[tuple[int, int]]
                 ):
        
        # set members
        self._my_body = my_body
        self._enemy_body = enemy_body
        self._my_health = my_health
        self._enemy_health = enemy_health
        self._foods = foods

    def getScore(self) -> int:
        board_score = BoardScore()

        # 端にいるかどうかで更新
        board_score.updateScoreByEdge(head=self._my_body[0], enemy=False)
        board_score.updateScoreByEdge(head=self._enemy_body[0], enemy=True)

        # 相手のheadとの位置で更新
        board_score.updateScoreByHead(my_body=self._my_body, enemy_body=self._enemy_body)
        board_score.updateScoreByLength(my_body=self._my_body, enemy_body=self._enemy_body)

        return board_score.score
        
    
    def youWin(self) -> bool:
        a = self._enemy_body[0] in self._my_body[1:]
        b = self._enemy_body[0] in self._enemy_body[1:]
        c = self._enemy_health <= 0
        d = len(self._my_body) > len(self._enemy_body) and self._my_body[0] == self._enemy_body[0]

        if a or b or c or d:
            return True
        
        return False

    def youLose(self) -> bool:
        a = self._my_body[0] in self._enemy_body[1:]
        b = self._my_body[0] in self._my_body[1:]
        c = self._my_health <= 0
        d = len(self._my_body) <= len(self._enemy_body) and self._my_body[0] == self._enemy_body[0]
        
        if a or b or c or d:
            # print("You Lose")
            # print(f"Your Head: {self._my_body[0]}")
            # print(f"Your body: {self._my_body[1:]}")
            return True

        return False


    def getLegalMoves(self, depth) -> list[tuple[int, int]]:
        """
        depthが偶数なら自分のターン、奇数なら相手のターンとして合法手を返す
        """
        if (depth % 2 == 0):
            moves = getSafeMoves(head=self._my_body[0])
        else:
            moves = getSafeMoves(head=self._enemy_body[0])
        
        return moves
    
    def next(self, move: tuple[int, int], depth: int):
        if (depth % 2 == 1):
            # print(f"current_my_body:{self._my_body}")
            my_body = self._my_body.copy()
            my_body.insert(0, move)
            foods = self._foods.copy()
            if move in self._foods:
                foods.remove(move)
            else:
                my_body.pop()
            my_health =  self._my_health -1

            enemy_body =  self._enemy_body.copy()
            enemy_health = self._enemy_health
            # print(f"next_my_body:{self._my_body}")
        else:
            enemy_body = self._enemy_body.copy()
            enemy_body.insert(0, move)
            foods = self._foods.copy()
            if move in self._foods:
                foods.remove(move)
            else:
                enemy_body.pop()
            enemy_health =  self._enemy_health -1

            my_body =  self._my_body.copy()
            my_health = self._my_health
        
        return BoardState(my_body=my_body, 
                          enemy_body=enemy_body,
                          my_health=my_health,
                          enemy_health=enemy_health,
                          foods=foods)