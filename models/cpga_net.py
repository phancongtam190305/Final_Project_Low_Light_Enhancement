import torch
import torch.nn as nn

class CPGA_Base(nn.Module):
    def __init__(self):
        super(CPGA_Base, self).__init__()
        # TODO: Implement CPGA-Net baseline here (Task assigned to Ben)
        self.conv = nn.Conv2d(3, 3, kernel_size=3, padding=1)

    def forward(self, x):
        # Placeholder behavior
        return x + self.conv(x) * 0.0

class CPGA_DS_Both(nn.Module):
    def __init__(self):
        super(CPGA_DS_Both, self).__init__()
        # TODO: Implement CPGA-DS-Both here (Task assigned to Ben)
        self.conv = nn.Conv2d(3, 3, kernel_size=3, padding=1)

    def forward(self, x):
        return x + self.conv(x) * 0.0

class CPGA_HVI_T(nn.Module):
    def __init__(self):
        super(CPGA_HVI_T, self).__init__()
        # TODO: Implement CPGA-HVI-T here (Task assigned to Ben)
        self.conv = nn.Conv2d(3, 3, kernel_size=3, padding=1)

    def forward(self, x):
        return x + self.conv(x) * 0.0

class CPGA_IAAF_SC(nn.Module):
    def __init__(self):
        super(CPGA_IAAF_SC, self).__init__()
        # TODO: Implement CPGA-IAAF-SC here (Task assigned to Phuc / Ben)
        self.conv = nn.Conv2d(3, 3, kernel_size=3, padding=1)

    def forward(self, x):
        return x + self.conv(x) * 0.0
