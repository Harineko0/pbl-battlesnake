import torch

def get_device() -> torch.device:
    # return torch.device("mps")
    return torch.device("cpu")
    # torch.device("mps" if torch.backends.mps.is_available() else "cpu")

device = get_device()
