class BoardScore:
    """
    初期値0のscoreをupdateして返すクラス
    scoreは-9999から9999の範囲とする
    """
    def __init__(self):
        self.score = 0

    def updateScoreByHead(self, head: tuple[int, int], enemy = False):
        """
        自分が盤面の真ん中から遠いほど減点
        相手が盤面の真ん中から遠いほど加点
        """
        if enemy:
            coefficient = 1
        else:
            coefficient = -1

        # TODO 11 * 11 のリストで場所に対応した値を宣言しておいて、それとheadの位置で決定? 
        self.score += coefficient * abs(5 - head[0])
        self.score += coefficient * abs(5 - head[1])
        

    def updateScoreByLength(self, 
                            my_body: list[tuple[int, int]],
                            enemy_body: list[tuple[int, int]]
                            ):
        """
        自分の長さ - 相手の長さを加点
        相手より長ければ10点加点
        """
        if(len(my_body) > len(enemy_body)):
             self.score += 10

        self.score += len(my_body) - len(enemy_body)
