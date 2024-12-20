def isAroundHead(my_head: tuple[int, int],
                 enemy_head: tuple[int, int]) -> bool:
    """相手の斜めに自分のheadがあるかどうかを判定
    """
    a = (my_head[0] + 1, my_head[1] + 1) == enemy_head
    b = (my_head[0] + 1, my_head[1] - 1) == enemy_head
    c = (my_head[0] - 1, my_head[1] + 1) == enemy_head
    d = (my_head[0] - 1, my_head[1] - 1) == enemy_head

    if a or b or c or d:
        return True
    return False

def getSafeMoves(head: tuple[int, int]):
    moves = []

    if head[0] != 0:
        moves.append((head[0] - 1 , head[1]))
    if head[0] != 10:
        moves.append((head[0] + 1 , head[1]))
    if head[1] != 0:
        moves.append((head[0] , head[1] - 1))
    if head[1] != 10:
        moves.append((head[0] , head[1] + 1))

    return moves

def getDirection(move: tuple[int,int], my_head: tuple[int, int]):
    if my_head == (move[0] - 1, move[1]):
        return "right"
    elif my_head == (move[0] + 1, move[1]):
        return "left"
    elif my_head == (move[0], move[1] - 1):
        return "up"
    elif my_head == (move[0], move[1] + 1):
        return "down"