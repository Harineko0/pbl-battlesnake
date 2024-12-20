from typing import Tuple
import numpy as np
from numpy.typing import NDArray
import torch
from torch.types import Tensor
from enum import Enum


class Cause(Enum):
    WALL = 0
    OUT_OF_HEALTH = 1
    HIT_OPPONENT = 2
    HIT_MYSELF = 3
    NONE = 4


class Battlesnake:
    """
    Args:
        health: 体力
        seed: 乱数のシード
        size: ボードのサイズ
        opponent: 対戦相手の Battlesnake
    """
    def __init__(self, seed: int, health: int = 100, size: int = 11, opponent = None):
        if seed is not None:
            np.random.seed(seed)
        
        head = None
        # opponent と重ならないようにランダムな位置を選択
        while head is None or (isinstance(opponent, Battlesnake) and np.any(np.all(opponent.body == head, axis=1))):
            head = np.random.randint(0, size, 2)
        
        tail = None
        while tail is None or (isinstance(opponent, Battlesnake) and np.any(np.all(opponent.body == tail, axis=1))):
            tail = head + [[-1, 0], [1, 0], [0, -1], [0, 1]][np.random.randint(0, 3, 1)[0]]
        
        self.head = head
        self.body = np.array([head, tail])
        self.health = health
        self.size = size
        self.oppoent = opponent
        
        print(self.body)
    
    def __len__(self):
        return self.body.shape[0]

    """
    自身の位置と食べ物を更新する
    
    Args:
        action: 0 ~ 3 の整数で進む方向を指定する. 0: 上, 1: 下, 2: 左, 3: 右
        foods: 食べ物の位置を表す行列
        
    Returns:
        done: ゲームが終了したかどうか
    """
    def move(self, action: int, foods: NDArray) -> Tuple[bool, Cause]:
        # 動かす
        if action == 0:
            self.head[0] -= 1
        elif action == 1:
            self.head[0] += 1
        elif action == 2:
            self.head[1] -= 1
        elif action == 3:
            self.head[1] += 1
        
        # 範囲外ならゲーム終了
        if self.head[0] < 0 or self.head[0] >= self.size or self.head[1] < 0 or self.head[1] >= self.size:
            return True, Cause.WALL
        
        # 自分の体にぶつかったらゲーム終了
        if np.any(np.all(self.body == self.head, axis=1)):
            return True, Cause.HIT_MYSELF
        
        # 相手の体にぶつかったらゲーム終了
        if np.any(np.all(self.oppoent.body == self.head, axis=1)):
            return True, Cause.HIT_OPPONENT

        # 体力が尽きたらゲーム終了
        if self.health <= 0:
            return True, Cause.OUT_OF_HEALTH
        
        np.append(self.body, [self.head], axis=0)
        
        # food を食べる
        if foods[self.head[0], self.head[1]] == 1:
            self.health = 100
            foods[self.head[0], self.head[1]] = 0
        else:
            self.health -= 1
            np.delete(self.body, -1)
            
        return False, Cause.NONE

    """
    Returns:
        h_mat: ヘッドの位置を表す行列
        b_mat: ボディの位置を表す行列
    """
    def get_state(self) -> Tuple[NDArray, NDArray]:
        h_mat = np.zeros((self.size, self.size), dtype=int)
        h_mat[self.head[0], self.head[1]] = 1
        
        b_mat = np.zeros((self.size, self.size), dtype=int)
        b_mat[self.body[:, 0], self.body[:, 1]] = 1
        
        return h_mat, b_mat


class Foods:
    def __init__(self, snakes: list[Battlesnake], size: int = 11, amount: int = 3, seed: int = None):
        if seed is not None:
            np.random.seed(seed)
        
        self.food = self._get_random_position(np.concatenate([snake.body for snake in snakes], axis=0), size=amount)
        self.size = size
        self.snakes = snakes

    def exists(self, position: NDArray) -> bool:
        return np.all(self.food == position)

    def consume(self, position: NDArray):
        index = np.where(np.all(self.food == position, axis=1))
        self.food = np.delete(self.food, index, axis=0)
        new_food = self._get_random_position(np.concatenate([snake.body for snake in self.snakes], axis=0), size=1)
        self.food = np.append(self.food, new_food, axis=0)
        
    def get_state(self) -> NDArray:
        food_mat = np.zeros((self.size, self.size), dtype=int)
        food_mat[self.food[:, 0], self.food[:, 1]] = 1
        
        return food_mat
    
    """
    constraints 以外の位置の候補からランダムに size 個の位置を NDArray[Tuple[int, int]] で返す
    Args:
        constraints: NDArray[Tuple[int, int]]: 位置の候補の制約
        size: 返却する位置の数
    """ 
    def _get_random_position(self, constraints: NDArray, size: int = 3) -> NDArray:
        all_possible_vectors = np.array(np.meshgrid(np.arange(size), np.arange(size))).T.reshape(-1, 2)
        mask = np.ones(len(all_possible_vectors), dtype=bool)
            
        for con in constraints:
            mask &= np.any(all_possible_vectors != con, axis=1)
        
        possible_cells = all_possible_vectors[mask]
        
        return possible_cells[np.random.randint(len(possible_cells), size=size + 1)]


class LocalBattlesnakeEnv:
    def __init__(self, size: int = 11, seed: int = None):
        self.size = size
        self.seed = seed
        
    
    """
    Args:
        action: 0 ~ 3 の整数で進む方向を指定する. 0: 上, 1: 下, 2: 左, 3: 右
    
    Returns:
        state: 環境の状態を表す情報
        reward: 報酬
        done: ゲームが終了したかどうか
    """
    def step(self, action: int) -> tuple[NDArray, float, bool]:
        foods = self.foods.get_state()
        
        if self.turn == 0:
            done, cause = self.me.move(action, foods)
            self.turn = 1
        else:
            done, cause = self.you.move(action, foods)
            self.turn = 0
            
        state = self.get_state()
        reward = self.get_reward(me=self.me, you=self.you, foods=foods, done=done, cause=cause)
        
        return state, reward, done
    
    
    def get_reward(self, me: Battlesnake, you: Battlesnake, foods: Foods, done: bool, cause: Cause) -> float:
        if not done:
            return 0

        match cause:
            case Cause.WALL:
                return -2 # 壁にぶつかったら多めに減点
            case Cause.OUT_OF_HEALTH:
                return -1
            case Cause.HIT_OPPONENT:
                # 体力が多い方が勝ち
                if len(me) > len(you):
                    return 1
                else:
                    return -1
                
            case Cause.HIT_MYSELF:
                return -2 # 自分にぶつかったら多めに減点
        
        return 0


    """
    Returns:
        state: 環境の状態を表す情報
    """
    def reset(self) -> tuple[NDArray]:
        if self.seed is not None:
            np.random.seed(self.seed)
                
        self.me         = Battlesnake(seed=self.seed)
        self.you        = Battlesnake(seed=self.seed, opponent=self.me)
        self.me.oppoent = self.you
        self.foods      = Foods([self.me, self.you], seed=self.seed, amount=3)
        self.turn       = 0 # 0 for me, 1 for you
        
        return self.get_state()


    """
    Returns:
        state: 環境の状態を表す Tensor
    """
    def get_state(self) -> Tensor:
        me_h_mat, me_b_mat = self.me.get_state()
        you_h_mat, you_b_mat = self.you.get_state()
        foods_mat = self.foods.get_state()
        
        return torch.stack([
            torch.tensor(me_h_mat, dtype=torch.float32),
            torch.tensor(me_b_mat, dtype=torch.float32),
            torch.tensor(you_h_mat, dtype=torch.float32),
            torch.tensor(you_b_mat, dtype=torch.float32),
            torch.tensor(foods_mat, dtype=torch.float32)
        ], dim=0)
    
    def render(self):
        m_head, m_body = self.me.get_state()
        y_head, y_body = self.you.get_state()
        f = self.foods.get_state()
        
        print('-----------')
        print(self.turn)
        print(m_body)
        print(y_body)
        print(f) 
