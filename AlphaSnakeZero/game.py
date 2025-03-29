"""
簡易将棋を基にbattlesnakeを実装
"""

# パッケージのインポート
import random
import math
import numpy as np

# ゲームの状態
class State:
    # TODO 処理を変更
    # 初期化
    def __init__(self, 
                 head=None,
                 enemy_head=None,
                 pieces=None, 
                 enemy_pieces=None,
                 health=None,
                 enemy_health=None,
                 foods=None,
                 depth=0
                 ):
        
        # 方向定数
        # down, up, right, left
        self.dxy = ((0, -1), (1, 0), (0, 1), (-1, 0))

        # set members

        self.head = [0] * (121)
        self.head[head["x"] + 11 * head["y"]] = 1

        self.enemy_head = [0] * (121)
        self.enemy_head[enemy_head["x"] + 11 * enemy_head["y"]] = 1

        self.pieces = [0] * 121
        for piece in pieces:
            self.pieces[piece["x"] + 11 * piece["y"]] = 1

        self.enemy_pieces = [0] * 121
        for piece in enemy_pieces:
            self.enemy_pieces[piece["x"] + 11 * piece["y"]] = 1

        self.health = [0] * 121
        self.health[health] = 1

        self.enemy_health = [0] * 121
        self.enemy_health[enemy_health] = 1 

        self.food = [0] * 121
        for food in foods:
            self.food[food["x"] + 11 * food["y"]] = 1
        
        self.depth = depth

    # 負けかどうか
    def is_lose(self):
        # 自分または相手のbodyと衝突(tailとぶつかっただけで負け判定?)
        for i in range(121):
            if self.head[i] == 1 and self.enemy_head[i] == 0 and self.enemy_pieces[i] == 1:
                return True
            
        # 相手より小さい状態でheadと衝突
        for i in range(121):
            if self.head[i] == 1 and self.head[i] == 1 :
                if np.count_nonzero(self.pieces) < np.count_nonzero(self.enemy_pieces):
                    return True
                
        # 場外負けはしないのでパス
        
        return False

    # 引き分けかどうか
    def is_draw(self):
        # 相手と同時にbodyに衝突(tailの場合は?)
        for i in range(121):
            if self.head[i] == 1 and self.enemy_head[i] == 0 and self.enemy_pieces[i] == 1:
                if self.head[i] == 0 and self.enemy_head[i] == 1 and self.pieces[i] == 1:
                    return True
        # 相手と同じ大きさでheadに衝突

        for i in range(121):
            if self.head[i] == 1 and self.head[i] == 1 :
                if np.count_nonzero(self.pieces) == np.count_nonzero(self.enemy_pieces):
                    return True
        # 場外負けはしないのでパス
        return False

    # TODO 処理を追加
    # ゲーム終了かどうか
    def is_done(self):
        pass

    # TODO 処理を変更
    # デュアルネットワークの入力の2次元配列の取得
    def pieces_array(self):
        # プレイヤー毎のデュアルネットワークの入力の2次元配列の取得
        def pieces_array_of(pieces):
            table_list = []
            # 0:自分の蛇の頭, 1:相手の蛇の頭, 
            # 2:自分の蛇の体頭を含(頭を含む), 3:相手の蛇の体(頭を含む),
            # 4:自分の蛇の体力, 5:相手の蛇の体力, 6:餌
            for j in range(1, 8):
                table = [0] * 121
                table_list.append(table)
                for i in range(121):
                    if pieces[i] == j:
                        table[i] = 1

            return table_list

        # デュアルネットワークの入力の2次元配列の取得
        return [pieces_array_of(self.pieces), pieces_array_of(self.enemy_pieces)]
    
    # 駒の移動先と移動元を行動に変換
    def position_to_action(self, position, direction):
        return position * 120 + direction
    
    # 行動を駒の移動先と移動元に変換
    def action_to_position(self, action):
        return (int(action/120), action%120)
    
    # 合法手のリストの取得
    def legal_actions(self):
        actions = []
        for p in range(121):
            # 蛇の移動時
            if self.pieces[p]  != 0 and self.enemy_pieces[p] != 0:
                actions.extend(self.legal_actions_pos(p))

        return actions
    
    # 駒の移動時の合法手のリストの取得
    def legal_actions_pos(self, position_src):
        actions = []

        # 駒の移動可能な方向
        directions = [0, 1, 2, 3]

        # 合法手の取得
        for direction in directions:
            # 駒の移動元
            x = position_src%11 + self.dxy[direction][0]
            y = int(position_src/11) + self.dxy[direction][1]
            p = x + y * 11

            # 移動可能時は合法手として追加
            if 0 <= x and x <= 10 and 0<= y and y <= 10 and self.pieces[p] == 0 and self.enemy_pieces[p] == 0:
                actions.append(self.position_to_action(p, direction))
        return actions
    
    # TODO 処理を変更
    # 次の状態の取得(餌の追加は無視しても問題ないと仮定して更新しない)
    def next(self, action):
        # 次の状態の作成
        state = State(self.head.copy(),
                      self.enemy_head.copy(),
                      self.pieces.copy(), 
                      self.enemy_pieces.copy(),
                      self.health.copy(),
                      self.enemy_health.copy(),
                      self.food.copy(),
                      self.depth+1
                      )

        # 行動を(移動先, 移動元)に変換
        position_dst, position_src = self.action_to_position(action)

        # 駒の移動元
        x = position_dst%11 - self.dxy[position_src][0]
        y = int(position_dst/11) - self.dxy[position_src][1]
        position_src = x + y * 11

        # 駒の移動
        state.pieces[position_dst] = state.pieces[position_src]
        if self.food == 0:
            state.pieces[position_src] = 0


    # 先手かどうか
    def is_first_player(self):
        return self.depth%2 == 0

# ランダムで行動選択
def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0, len(legal_actions)-1)]

# 動作確認
if __name__ == '__main__':
    # 状態の生成
    state = State()

    # ゲーム終了までのループ
    while True:
        # ゲーム終了時
        if state.is_done():
            break

        # 次の状態の取得
        state = state.next(random_action(state))

        # 文字列表示
        print(state)
        print()