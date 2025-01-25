def getSafeMoves(head, neck):
    moves = []

    if head[0] != 0:
        moves.append((head[0] - 1 , head[1]))
    if head[0] != 10:
        moves.append((head[0] + 1 , head[1]))
    if head[1] != 0:
        moves.append((head[0] , head[1] - 1))
    if head[1] != 10:
        moves.append((head[0] , head[1] + 1))
    
    moves.remove(neck)

    return moves

def getDirection(move, my_head):
    if my_head == (move[0] - 1, move[1]):
        return "right"
    elif my_head == (move[0] + 1, move[1]):
        return "left"
    elif my_head == (move[0], move[1] - 1):
        return "up"
    elif my_head == (move[0], move[1] + 1):
        return "down"