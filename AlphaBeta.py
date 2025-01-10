import math
import time


# アルファベータ法で状態価値計算
def alpha_beta(board_state, alpha, beta, depth, look_ahead_depth):
    if depth % 2 == 0:
        if board_state.youLose():
            return -(100 - depth) * 10000
        
        if board_state.youWin():
            #return math.inf #<-こっちのほうが早い?
            return (100 - depth) * 10000
    
    if depth >= look_ahead_depth:
        return board_state.getScore()

    # 合法手の状態価値の計算
    for move in board_state.getLegalMoves(depth = depth):
        score = -alpha_beta(board_state=board_state.next(move, depth=depth + 1), 
                            alpha=-beta, 
                            beta=-alpha, 
                            depああth=depth + 1,
                            look_ahead_depth=look_ahead_depth)
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
    start_time = time.time()
    look_ahead_depth = 0
    while True:
        best_move = [0, 0]
        alpha = -math.inf
        string_list = ['','']
        look_ahead_depth += 2

        for move in board_state.getLegalMoves(depth = depth):
            score = -alpha_beta(board_state=board_state.next(move, depth = depth + 1), 
                            alpha=-math.inf, 
                            beta=-alpha,
                            depth=depth + 1,
                            look_ahead_depth=look_ahead_depth)
            if score > alpha:
                best_move = move
                alpha = score
                
            string_list[0] = string_list[0] + f'{move}, '
            string_list[1] = string_list[1] + f'{score}, '
        
        current_time = time.time()
        if current_time - start_time >= 0.080:
            print(f"先読みターン数: {look_ahead_depth//2}")
            print('action:', string_list[0], '\nscore: ', string_list[1], '\n')            

            # 合法手の状態価値の最大値を持つ行動を返す
            return best_move