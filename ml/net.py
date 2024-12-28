import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

class QNet(nn.Module):
    def __init__(self, state_size: int, action_size: int):
        super(QNet, self).__init__()
        
        # 畳み込み層
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        
        self.l1 = nn.Linear(32 * state_size, 128)
        self.l2 = nn.Linear(128, action_size)
        # self.l3 = nn.Linear(64, action_size)
    
    """
    Args:
      x: 
    """
    def forward(self, x: Tensor) -> Tensor:
        x = x.unsqueeze(1)  # (batch_size, 1, 121, 5): チャンネル数を追加
        x = F.relu(self.conv1(x))  # 畳み込み層1
        x = F.relu(self.conv2(x))  # 畳み込み層2
        
        # フラット化
        x = x.view(x.size(0), -1)
       
        h = F.relu(self.l1(x))
        # h = F.relu(self.l2(h))
        return self.l2(h)
