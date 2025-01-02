map_score=[
    [10, 9, 8, 7, 6, 5, 6, 7, 8, 9, 10],
    [9 , 8, 7, 6, 5, 4, 5, 6, 7, 8,  9],
    [8 , 7, 6, 5, 4, 3, 4, 5, 6, 7,  8],
    [7 , 6, 5, 4, 3, 2, 3, 4, 5, 6,  7],
    [6 , 5, 4, 3, 2, 1, 2, 3, 4, 5,  6],
    [5 , 4, 3, 2, 1, 0, 1, 2, 3, 4,  5],
    [6 , 5, 4, 3, 2, 1, 2, 3, 4, 5,  6],
    [7 , 6, 5, 4, 3, 2, 3, 4, 5, 6,  7],
    [8 , 7, 6, 5, 4, 3, 4, 5, 6, 7,  8],
    [9 , 8, 7, 6, 5, 4, 5, 6, 7, 8,  9],
    [10, 9, 8, 7, 6, 5, 6, 7, 8, 9, 10]
]

"""
Buta Modified
#Note that this procedure makes the entire process of this program redundant.#
#Use this when you want to change map score quickly.#

<Note>
Isn't declaring map_score ehnever BoardScore.py is called a bit pointless?
I did not write the original code, but to me declaring map_socore at AlphaBeta.py
(whatever file that only activate once as a battlesnake run) seems more reasonable.
--Buhi

"""
for y in range(11):
    for x in range(11):
        map_score[y][x]=abs(5-x)+abs(5-y)


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

        self.score += coefficient * map_score[head[0]][head[1]]
        

    def updateScoreByLength(self, 
                            my_body: list[tuple[int, int]],
                            enemy_body: list[tuple[int, int]]
                            ):
        """
        自分の長さ - 相手の長さを加点
        相手より長ければ10点加点
        """
        if((length_difference := len(my_body) - len(enemy_body)) > 0):
             self.score += 10

        self.score += length_difference
