from collections import deque
import numpy as np
from environment import Cause

class CauseCounter:
    def __init__(self, buffer_size: int, episode_size: int, scale: int = 100):
        self.buffer_size = buffer_size
        self.scale = scale
        self.enum_size = len(Cause)
        self.deque = deque(maxlen=buffer_size)
        self.average = np.zeros(self.enum_size)
        self.history = np.zeros((episode_size, self.enum_size))
    
    def append(self, cause: Cause, index: int):
        if len(self.deque) == self.buffer_size:
            old = self.deque.popleft()
            self.average[old.value] -= self.scale / self.buffer_size

        self.deque.append(cause)
        self.average[cause.value] += self.scale / self.buffer_size

        if index >= self.buffer_size:
            self.history[index] = self.average
    
    def get_averages(self):
        return self.history