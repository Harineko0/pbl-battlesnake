from Helpers import isAroundHead

class BoardScore:
    """
    初期値0のscoreをupdateして返すクラス
    """
    def __init__(self):
        self.score = 0

    def updateScoreByEdge(self, head: tuple[int, int], enemy = False):
        """
        相手が端にいるときに10点加点，自分が端にいるときに10点減点
        """
        if enemy:
            coefficient = 1
        else:
            coefficient = -1
        
        if head[0] == 0:
            self.score += coefficient * 10
        if head[0] == 11:
            self.score += coefficient * 10
        if head[1] == 0:
            self.score += coefficient * 10
        if head[1] == 11:
            self.score += coefficient * 10
        
    def updateScoreByHead(self, 
                       my_body: list[tuple[int, int]],
                       enemy_body: list[tuple[int, int]],):
        """
        相手より大きいとき、相手の斜めにいるなら100点加点.
        相手以下の大きさのとき、相手の斜めにいるなら100点減点.
        """
        if len(my_body) > len(enemy_body):
            if isAroundHead(my_head=my_body[0], enemy_head=enemy_body[0]):
                self.score += 100
        else:
            if isAroundHead(my_head=my_body[0], enemy_head=enemy_body[0]):
                self.score += -100

    # TODO 処理を追加
    def updateScoreByFood():
        pass