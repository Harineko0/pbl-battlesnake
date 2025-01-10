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


tmp_map_score=[
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

for y in range(11):
    for x in range(11):
        map_score[x][y]=abs(5-x)+abs(5-y)
        tmp_map_score[x][y]=abs(5-x)+abs(5-y)


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
        
    def updateScoreByGate(self, my_body: list[tuple[int, int]],
                          enemy_body: list[tuple[int, int]]):
        """
        Buhi
        We can make this def funt a bit more smoothly and thoroughly done.
        If we change map_score with my_body and enemy_body and then change it by checking every space.
        But I did not write this that way as I thought it is timetaking (NOT to write but to run).


        I am not familiar with how αβ search works, but I believe that not reducing score when my head is in between 
        enemy body and the wall (by enemy body I mean body that is not tail) does not effect the overall result. Opinions?
        """


        
        if(enemy_body[len(enemy_body)-1][0]==1):
            if(my_body[1][1]!=enemy_body[len(enemy_body)-2][1] and my_body[1][1]!=my_body[2][1] ):
                tmp_map_score[0][enemy_body[len(enemy_body)-1][1]]=-100
                self.score += map_score[my_body[0][0]][my_body[0][1]]
        if(enemy_body[len(enemy_body)-1][0]==9):
            if(my_body[1][1]!=enemy_body[len(enemy_body)-2][1] and my_body[1][1]!=my_body[2][1] ):
                tmp_map_score[10][enemy_body[len(enemy_body)-1][1]]=-100
                self.score += map_score[my_body[0][0]][my_body[0][1]]
        if(enemy_body[len(enemy_body)-1][1]==1):
            if(my_body[1][0]!=enemy_body[len(enemy_body)-2][0] and my_body[1][0]!=my_body[2][0] ):
                tmp_map_score[enemy_body[len(enemy_body)-1][0]][0]=-100
                self.score += map_score[my_body[0][0]][my_body[0][1]]
        if(enemy_body[len(enemy_body)-1][1]==9):
            if(my_body[1][0]!=enemy_body[len(enemy_body)-2][0] and my_body[1][0]!=my_body[2][0] ):
                tmp_map_score[enemy_body[len(enemy_body)-1][0]][10]=-100     
                self.score += map_score[my_body[0][0]][my_body[0][1]]

    def updateScoreByNumOfWays(self, head:tuple[int,int],
                               my_body: list[tuple[int, int]],
                               enemy_body: list[tuple[int, int]]):
        WayofAble = 0
        if head[0] != 0:
            num_f = 0
            for bodyme in my_body:
                if((head[0]-1 == bodyme[0]) and (head[1] == bodyme[1])):
                    num_f = num_f + 1
        
            for bodyene in enemy_body:
                if((head[0]-1 == bodyene[0]) and (head[1] == bodyene[1])):
                    num_f = num_f + 1
            
            if(num_f == 0):
                WayofAble = WayofAble + 1

        if head[0] != 10:
            num_f = 0
            for bodyme in my_body:
                if((head[0]+1 == bodyme[0] and head[1] == bodyme[1])):
                    num_f = num_f + 1
            for bodyene in enemy_body:
                if(head[0]+1 == bodyene[0] and head[1] == bodyene[1]):
                    num_f = num_f + 1
            
            if(num_f == 0):
                WayofAble = WayofAble + 1
            
        if head[1] != 0:
            num_f = 0
            for bodyme in my_body:
                if((head[0] == bodyme[0]) and (head[1]-1 == bodyme[1])):
                    num_f = num_f + 1
            for bodyene in enemy_body:
                if((head[0] == bodyene[0]) and(head[1]-1 == bodyene[1])):
                    num_f = num_f + 1
            
            if(num_f == 0):
                WayofAble = WayofAble + 1

        if head[1] != 10:
            num_f = 0
            for bodyme in my_body:
                if((head[0] == bodyme[0]) and (head[1]+1 == bodyme[1])):
                    num_f = num_f + 1
            
            for bodyene in enemy_body:
                if((head[0] == bodyene[0]) and (head[1]+11 == bodyene[1])):
                    num_f = num_f + 1
            if(num_f == 0):
                WayofAble = WayofAble + 1
        self.score += WayofAble * WayofAble
    def updateScoreByLength(self, 
                            my_body: list[tuple[int, int]],
                            enemy_body: list[tuple[int, int]]
                            ):
        """
        自分の長さ - 相手の長さを加点
        相手より長ければ10点加点
        """
        """
        HIHIHIHI
        """
        if((length_difference := len(my_body) - len(enemy_body)) > 0):
             self.score += 10

        self.score += length_difference
