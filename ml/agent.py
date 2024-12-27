import torch
from torch import Tensor
from net import QNet
import numpy as np
import file as f
from replay_buffer import ReplayBuffer

class Agent:
    def __init__(self, id: str):
        self.gamma = 0.98
        self.lr = 0.0005
        self.epsilon = 0.1
        self.buffer_size = 10000
        self.batch_size = 32
        self.action_size = 4
        self.id = id
        state_size = 605
        
        self.replay_buffer = ReplayBuffer(buffer_size=self.buffer_size, batch_size=self.batch_size)
        self.qnet = QNet(action_size=self.action_size, state_size=state_size)
        self.qnet_target = QNet(action_size=self.action_size, state_size=state_size)
        self.optimizer = torch.optim.Adam(self.qnet.parameters(), lr=self.lr)
        # self.optimizer.add_param_group({'params': self.qnet.parameters()})

    def sync_target(self):
        self.qnet_target.load_state_dict(self.qnet.state_dict())
    
    def get_action(self, state: Tensor):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_size)
        else:
            state = state[np.newaxis, :]
            qs = self.qnet(state)
            return torch.argmax(qs).item()
    
    def update(self, state: Tensor, action: int, reward: float, next_state: Tensor, done: bool):
        self.replay_buffer.add(state, action, reward, next_state, done)
        if len(self.replay_buffer) < self.batch_size:
            return
    
        state, action, reward, next_state, done = self.replay_buffer.get_batch()
        qs = self.qnet(state)
        q = qs.gather(1, action[:, np.newaxis]).squeeze(1)
        
        next_qs = self.qnet_target(next_state)
        next_q = torch.max(next_qs, dim=1)[0]
        # next_q.unchain() ?
        
        target = reward + self.gamma * next_q * (1 - done)
        loss = torch.nn.functional.mse_loss(q, target)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    def save(self):
        path = f"model/{self.id}_{self.version}.pth"
        torch.save(self.qnet.state_dict(), path)
    
    def load(self):
        dir = "model"
        path, version = f.get_lastest_path(pattern=f"{self.id}_(\d+).pth", dir=dir)
        self.version = version + 1
        
        if path is None:
            return
        
        path = f"{dir}/{path}"
        
        self.qnet.load_state_dict(torch.load(path, weights_only=True))
        self.qnet_target.load_state_dict(torch.load(path, weights_only=True))

