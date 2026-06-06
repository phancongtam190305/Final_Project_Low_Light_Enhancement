import torch
import torch.nn as nn
from .blocks import ResBlock

class ZDCE_ResBlock_Small(nn.Module):
    def __init__(self):
        super(ZDCE_ResBlock_Small, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        
        # 2 Residual blocks chèn ở giữa Conv3 và Conv4
        self.res_blocks = nn.Sequential(
            ResBlock(32),
            ResBlock(32)
        )
        
        self.conv4 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(64, 32, kernel_size=3, padding=1)
        self.conv6 = nn.Conv2d(64, 32, kernel_size=3, padding=1)
        self.conv7 = nn.Conv2d(64, 24, kernel_size=3, padding=1)
        
        self.relu = nn.ReLU(inplace=True)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x1 = self.relu(self.conv1(x))
        x2 = self.relu(self.conv2(x1))
        x3 = self.relu(self.conv3(x2))
        
        x3_feat = self.res_blocks(x3)
        
        x4 = self.relu(self.conv4(x3_feat))
        x5 = self.relu(self.conv5(torch.cat([x4, x3_feat], dim=1)))
        x6 = self.relu(self.conv6(torch.cat([x5, x2], dim=1)))
        x7 = self.tanh(self.conv7(torch.cat([x6, x1], dim=1)))
        
        chunks = torch.chunk(x7, 8, dim=1)
        
        enhanced_image = x
        for alpha in chunks:
            enhanced_image = enhanced_image + alpha * enhanced_image * (1.0 - enhanced_image)
            
        return enhanced_image
