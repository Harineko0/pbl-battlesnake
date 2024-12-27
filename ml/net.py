import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

class QNet(nn.Module):
    def __init__(self, state_size: int, action_size: int):
        super(QNet, self).__init__()
        
        self.l1 = nn.Linear(state_size, 128)
        self.l2 = nn.Linear(128, 64)
        self.l3 = nn.Linear(64, action_size)
    
    """
    Args:
      x: 
    """
    def forward(self, x: Tensor) -> Tensor:
        h = F.relu(self.l1(x))
        h = F.relu(self.l2(h))
        return self.l3(h)
