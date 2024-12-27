from collections import deque
import random
import numpy as np
from torch import Tensor
import torch

class ReplayBuffer:
    def __init__(self, buffer_size: int, batch_size: int):
        self.buffer= deque(maxlen=buffer_size)
        self.batch_size = batch_size
    
    def add(self, state: Tensor, action: int, reward: float, next_state: Tensor, done: bool):
        data = (state, action, reward, next_state, done)
        self.buffer.append(data)
    
    def __len__(self):
        return len(self.buffer)
    
    """
    Returns:
        state: 状態のテンソルの ndarray (ndarray[tensor, tensor, ...])
        action: 行動のインデックス
        reward: 報酬
        next_state: 次の状態のテンソル
        done: ゲームが終了したかどうか
    """
    def get_batch(self) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
        data = random.sample(self.buffer, self.batch_size)
        
        state = torch.stack([d[0] for d in data])
        action = torch.tensor([d[1] for d in data])
        reward = torch.tensor([d[2] for d in data])
        next_state = torch.stack([d[3] for d in data])
        done = torch.tensor([1 if d[4] == True else 0 for d in data])
        
        return state, action, reward, next_state, done