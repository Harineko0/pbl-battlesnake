import math

# アルファベータ法で状態価値計算
def alpha_beta(board_state, alpha, beta, depth):
    if board_state.youLose():
        # 自分のターン
        if depth % 2 == 1:
            return math.inf
        else:
            return -math.inf
    
    if board_state.youWin():
        if depth % 2 == 1:
            return -math.inf
        else:
            return math.inf
    
    if depth >= 14:
        return board_state.getScore()

    # 合法手の状態価値の計算
    for move in board_state.getLegalMoves(depth = depth):
        score = -alpha_beta(board_state=board_state.next(move, depth=depth + 1), 
                            alpha=-beta, 
                            beta=-alpha, 
                            depth=depth + 1)
        if score > alpha:
            alpha = score

        # 現ノードのベストスコアが親ノードを超えたら探索終了
        if alpha >= beta:
            return alpha

    # 合法手の状態価値の最大値を返す
    return alpha

# アルファベータ法で行動選択
def alpha_beta_action(board_state, depth = 0):
    # 合法手の状態価値の計算
    best_move = [0, 0]
    alpha = -math.inf
    string_list = ['','']
    for move in board_state.getLegalMoves(depth = depth): #TODO 本当にこのdepthでいいか？
        score = -alpha_beta(board_state=board_state.next(move, depth = depth + 1), 
                           alpha=-math.inf, 
                           beta=-alpha,
                           depth=depth + 1)
        if score > alpha:
            best_move = move
            alpha = score
            
        string_list[0] = string_list[0] + f'{move}, '
        string_list[1] = string_list[1] + f'{score}, '
    print('action:', string_list[0], '\nscore: ', string_list[1], '\n')            

    # 合法手の状態価値の最大値を持つ行動を返す
    return best_move