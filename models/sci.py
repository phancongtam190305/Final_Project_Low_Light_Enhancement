import torch
import torch.nn as nn

class SCI(nn.Module):
    def __init__(self):
        super(SCI, self).__init__()
        # TODO: Implement SCI architecture here (Task assigned to Phuc)
        self.conv = nn.Conv2d(3, 3, kernel_size=3, padding=1)

    def forward(self, x):
        # Placeholder behavior: return input
        return x + self.conv(x) * 0.0
