import os
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms.functional as TF
import torchvision.models as models
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

class LOLDataset(Dataset):
    def __init__(self, root_dir, split='train', transform=None):
        """
        root_dir: Đường dẫn tới thư mục chứa dataset LOL-v1 (ví dụ: ./data)
        split: 'train' (sẽ đọc trong our485) hoặc 'val'/'test' (sẽ đọc trong eval15)
        """
        self.root_dir = root_dir
        self.split = split
        self.transform = transform
        
        folder_name = 'our485' if split == 'train' else 'eval15'
        self.low_dir = os.path.join(root_dir, folder_name, 'low')
        self.high_dir = os.path.join(root_dir, folder_name, 'high')
        
        if not os.path.exists(self.low_dir) or not os.path.exists(self.high_dir):
            raise FileNotFoundError(
                f"Không tìm thấy thư mục Low/High tại: {self.low_dir} hoặc {self.high_dir}. "
                "Vui lòng kiểm tra lại cấu trúc dataset."
            )
            
        self.file_names = sorted([f for f in os.listdir(self.low_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])

    def __len__(self):
        return len(self.file_names)

    def __getitem__(self, idx):
        file_name = self.file_names[idx]
        low_path = os.path.join(self.low_dir, file_name)
        high_path = os.path.join(self.high_dir, file_name)
        
        low_img = Image.open(low_path).convert('RGB')
        high_img = Image.open(high_path).convert('RGB')
        
        # Chuyển đổi thành Tensor trong khoảng [0, 1] trước tiên
        low_tensor = TF.to_tensor(low_img)
        high_tensor = TF.to_tensor(high_img)
        
        # Thực hiện đồng bộ Augmentation cho cả Low và High (chỉ dùng cho tập train)
        if self.split == 'train':
            # Random Horizontal Flip
            if random.random() > 0.5:
                low_tensor = TF.hflip(low_tensor)
                high_tensor = TF.hflip(high_tensor)
                
            # Random Vertical Flip
            if random.random() > 0.5:
                low_tensor = TF.vflip(low_tensor)
                high_tensor = TF.vflip(high_tensor)
                
        return low_tensor, high_tensor

class VGGPerceptualLoss(nn.Module):
    def __init__(self):
        super(VGGPerceptualLoss, self).__init__()
        # Load VGG16 pretrained
        vgg = models.vgg16(weights=models.VGG16_Weights.DEFAULT)
        # Sử dụng các layers đến relu3_3 (index 16)
        self.features = nn.Sequential(*list(vgg.features.children())[:16]).eval()
        
        # Đóng băng parameters
        for param in self.features.parameters():
            param.requires_grad = False
            
        # Các hằng số chuẩn hóa ImageNet
        self.register_buffer("mean", torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1))
        self.register_buffer("std", torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1))

    def forward(self, input_tensor, target_tensor):
        # Đưa input/target về khoảng chuẩn hóa của ImageNet
        input_norm = (input_tensor - self.mean) / self.std
        target_norm = (target_tensor - self.mean) / self.std
        
        # Trích xuất đặc trưng
        input_feats = self.features(input_norm)
        target_feats = self.features(target_norm)
        
        # Tính Mean Squared Error giữa các bản đồ đặc trưng
        loss = F.mse_loss(input_feats, target_feats)
        return loss

def calculate_metrics_numpy(output_tensor, target_tensor):
    """
    Tính PSNR và SSIM chính xác bằng skimage.
    output_tensor: Tensor shape (B, C, H, W) hoặc (C, H, W), range [0, 1] trên GPU/CPU
    target_tensor: Tensor shape (B, C, H, W) hoặc (C, H, W), range [0, 1] trên GPU/CPU
    """
    # Chuyển về numpy array dạng HWC và range [0, 255]
    if len(output_tensor.shape) == 4:
        # Nếu là batch, tính trung bình của batch
        psnrs, ssims = [], []
        for i in range(output_tensor.shape[0]):
            out_np = output_tensor[i].detach().cpu().numpy().transpose(1, 2, 0)
            tgt_np = target_tensor[i].detach().cpu().numpy().transpose(1, 2, 0)
            
            # Cắt về [0, 1] để an toàn trước khi tính metric
            out_np = np.clip(out_np, 0, 1)
            tgt_np = np.clip(tgt_np, 0, 1)
            
            psnr = peak_signal_noise_ratio(tgt_np, out_np, data_range=1.0)
            ssim = structural_similarity(tgt_np, out_np, data_range=1.0, channel_axis=2)
            psnrs.append(psnr)
            ssims.append(ssim)
        return np.mean(psnrs), np.mean(ssims)
    else:
        out_np = output_tensor.detach().cpu().numpy().transpose(1, 2, 0)
        tgt_np = target_tensor.detach().cpu().numpy().transpose(1, 2, 0)
        out_np = np.clip(out_np, 0, 1)
        tgt_np = np.clip(tgt_np, 0, 1)
        
        psnr = peak_signal_noise_ratio(tgt_np, out_np, data_range=1.0)
        ssim = structural_similarity(tgt_np, out_np, data_range=1.0, channel_axis=2)
        return psnr, ssim
