# 📋 Context.md — Final Project: Low-Light Image Enhancement

> **Người thực hiện (task Dô):** Huấn luyện & đánh giá 4 biến thể mô hình họ Zero-DCE trên tập LOL-v1.
> **Ngày cập nhật:** 2026-06-04

---

## 1. Tổng Quan Dự Án

Dự án so sánh hiệu năng (PSNR, SSIM, FLOPs, Params) của nhiều mô hình Low-Light Image Enhancement trên tập **LOL-v1**.

### Phân công nhóm
| Thành viên | Task                                          | Trạng thái |
|------------|-----------------------------------------------|------------|
| **Dô**    | 4 biến thể Zero-DCE (Baseline, ++, ResBlock, DenseBlock) | 🔧 Đang làm |
| **Phuc**  | SCI                                            | ⏳ Chưa hiện thực |
| **Ben**   | CPGA-Net (Base, DS-Both, HVI-T, IAAF-SC)      | ⏳ Chưa hiện thực |

### 4 Mô hình của Dô
1. **Zero_DCE** — Baseline gốc (7 Conv layers, skip connections kiểu U-Net, 8 alpha maps)
2. **Zero_DCE_PP** — Lightweight: thay Conv bằng DepthwiseSeparableConv
3. **ZDCE_ResBlock_Small** — Chèn 2 ResBlock giữa Conv3 và Conv4
4. **ZDCE_DenseBlock_Small** — Chèn 2 DenseBlock giữa Conv3 và Conv4

---

## 2. Cấu Trúc Thư Mục

```
Final_Project_Low_Light_Enhancement/
├── data/                          # Dataset LOL-v1 (đã tải sẵn)
│   ├── our485/                    # Tập train: 485 cặp ảnh (low/ + high/)
│   │   ├── low/
│   │   └── high/
│   └── eval15/                    # Tập val/test: 15 cặp ảnh (low/ + high/)
│       ├── low/
│       └── high/
├── models/
│   ├── __init__.py                # Re-export tất cả models
│   ├── sci.py                     # Placeholder SCI (TODO: Phuc)
│   ├── cpga_net.py                # Placeholder CPGA variants (TODO: Ben)
│   └── zero_dce/                  # === GÓI MÔ HÌNH CỦA DÔ ===
│       ├── __init__.py            # Export 4 classes
│       ├── blocks.py              # DepthwiseSeparableConv, ResBlock, DenseBlock
│       ├── zero_dce.py            # Zero_DCE baseline
│       ├── zero_dce_pp.py         # Zero_DCE_PP (Depthwise Separable)
│       ├── zdce_resblock_small.py # ZDCE_ResBlock_Small
│       └── zdce_denseblock_small.py # ZDCE_DenseBlock_Small
├── utils.py                       # LOLDataset, VGGPerceptualLoss, calculate_metrics_numpy
├── train.py                       # Script CLI huấn luyện (chạy qua terminal)
├── eval.py                        # Script CLI đánh giá (chạy qua terminal)
├── train_notebook.py              # Marimo Notebook (giao diện web tương tác)
├── requirements.txt               # Dependencies
├── checkpoints/                   # Lưu best checkpoint mỗi model (.pth)
├── runs/                          # TensorBoard logs
└── results/                       # Ảnh enhanced output (sau khi chạy eval.py)
```

---

## 3. Kiến Trúc Mô Hình (Chi tiết)

### Cơ chế chung: Light Enhancement Curve (LE-Curve)
Tất cả 4 mô hình đều xuất **24 channels** ở layer cuối, chia thành **8 alpha maps** (mỗi alpha map 3 channels cho RGB). Ảnh đầu vào được tăng sáng lặp lại 8 lần theo công thức:

```python
enhanced = enhanced + alpha * enhanced * (1.0 - enhanced)
```

### Bảng so sánh kiến trúc

| Model               | Conv Type           | Extra Blocks            | Output Channels |
|----------------------|---------------------|-------------------------|-----------------|
| Zero_DCE             | Standard Conv2d     | Không                   | 24 (8×3)        |
| Zero_DCE_PP          | DepthwiseSeparable  | Không                   | 24 (8×3)        |
| ZDCE_ResBlock_Small  | Standard Conv2d     | 2× ResBlock (giữa C3-C4)| 24 (8×3)       |
| ZDCE_DenseBlock_Small| Standard Conv2d     | 2× DenseBlock (giữa C3-C4)| 24 (8×3)     |

### Blocks dùng chung (`blocks.py`)

- **DepthwiseSeparableConv**: Depthwise conv (groups=in_channels) → Pointwise conv (1×1) → ReLU
- **ResBlock**: Conv3×3 → ReLU → Conv3×3 + skip connection (identity shortcut)
- **DenseBlock**: Conv3×3 → ReLU → Concat(input, output) → Conv3×3 → ReLU

---

## 4. Chiến Lược Huấn Luyện

### Loss Function (Supervised)
Mặc dù Zero-DCE gốc được huấn luyện **không giám sát** (unsupervised), dự án này sử dụng **huấn luyện có giám sát** (supervised) để so sánh công bằng với các mô hình khác:

```
Total Loss = L1_Loss(enhanced, ground_truth) + 0.01 × VGG_Perceptual_Loss(enhanced, ground_truth)
```

- **L1 Loss**: So sánh trực tiếp pixel-to-pixel giữa ảnh tăng sáng và ảnh Ground Truth
- **VGG Perceptual Loss**: Sử dụng features đến relu3_3 (index 16) của VGG16 pretrained ImageNet, tính MSE giữa feature maps → giữ chi tiết & texture tự nhiên

### Hyperparameters mặc định
| Parameter      | Giá trị     |
|----------------|-------------|
| Optimizer      | AdamW       |
| Learning Rate  | 1e-4        |
| Weight Decay   | 1e-4        |
| Scheduler      | CosineAnnealingLR (T_max=epochs) |
| Epochs         | 50          |
| Batch Size     | 16          |
| AMP            | Enabled (FP16 trên CUDA) |
| Gradient Clip  | max_norm=1.0 |

### Data Augmentation (chỉ tập train)
- Random Horizontal Flip (p=0.5)
- Random Vertical Flip (p=0.5)

---

## 5. Dataset: LOL-v1

- **Nguồn**: Tải từ mirror Hugging Face (tránh giới hạn quota Google Drive)
- **Cấu trúc**: `our485/` (485 cặp train) + `eval15/` (15 cặp val/test)
- **Định dạng ảnh**: PNG, RGB
- **Tiền xử lý**: ToTensor (normalize [0, 1])

---

## 6. Cách Chạy

### Cách 1: CLI (Terminal)
```bash
# Huấn luyện
python train.py --model Zero_DCE --epochs 50 --batch_size 16 --lr 1e-4

# Đánh giá 1 model
python eval.py --model Zero_DCE

# Đánh giá tất cả
python eval.py --model all
```

### Cách 2: Marimo Notebook (Giao diện Web)
```bash
# Mở ở chế độ edit (code + app)
marimo edit train_notebook.py

# Mở ở chế độ app (chỉ giao diện, giấu code)
marimo run train_notebook.py
```
Trong giao diện Marimo:
1. Chọn mô hình, thiết lập tham số
2. Nhấn nút **"🚀 Bắt đầu Huấn luyện"**
3. Theo dõi progress bar + ảnh so sánh real-time
4. Khi xong: xem biểu đồ Loss/PSNR + checkpoint được lưu tự động

### TensorBoard
```bash
tensorboard --logdir ./runs
```

---

## 7. Metrics Đánh Giá

| Metric | Ý nghĩa |
|--------|---------|
| **PSNR** (Peak Signal-to-Noise Ratio) | Chất lượng ảnh pixel-level (càng cao càng tốt, đơn vị dB) |
| **SSIM** (Structural Similarity Index) | Độ tương đồng cấu trúc với Ground Truth (0-1, càng cao càng tốt) |
| **Params** | Tổng số trainable parameters (phản ánh kích thước model) |
| **FLOPs** | Floating Point Operations (phản ánh chi phí tính toán, cần `pip install thop`) |
| **Inference Time** | Thời gian xử lý 1 ảnh (ms) |

---

## 8. Dependencies

```
torch
torchvision
marimo
opencv-python
matplotlib
pillow
scikit-image
tensorboard
```

Cài đặt: `pip install -r requirements.txt`

---

## 9. Vấn Đề Đã Biết & Lưu Ý

### ⚠️ Quick Test chưa hoàn thành
- Tiến trình chạy thử 1 epoch (`python train.py --epochs 1 --model Zero_DCE`) bị treo sau bước khởi tạo — có thể do **VGG16 weights chưa được cache** (cần tải ~528MB lần đầu) hoặc do xung đột tài nguyên GPU.
- **Cần chạy lại quick test** ở session mới để xác nhận pipeline hoạt động trước khi train chính thức.

### ⚠️ Deprecation Warnings (không ảnh hưởng)
```
FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated.
    → Nên đổi thành `torch.amp.GradScaler('cuda', args...)`
FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated.
    → Nên đổi thành `torch.amp.autocast('cuda', args...)`
```

### ⚠️ Windows Unicode
- Tất cả print trong `train.py` và `eval.py` đã dùng **tiếng Việt không dấu** để tránh `UnicodeEncodeError` trên Windows (mặc định cp1252).
- `utils.py` và `train_notebook.py` (chạy qua Marimo web) vẫn dùng tiếng Việt có dấu bình thường.

### ⚠️ Marimo Syntax
- Không dùng `return` thoát sớm trong cell Marimo (gây `SyntaxError: return outside function`).
- Cell chỉ return biến xuất ở cuối cùng.

---

## 10. Việc Cần Làm Tiếp (Next Steps)

1. **Sửa deprecation warnings**: Cập nhật `torch.cuda.amp` → `torch.amp` trong `train.py`, `train_notebook.py`
2. **Chạy lại quick test 1 epoch** để xác nhận pipeline OK
3. **Huấn luyện chính thức 4 mô hình** (50 epochs mỗi model):
   - Zero_DCE
   - Zero_DCE_PP
   - ZDCE_ResBlock_Small
   - ZDCE_DenseBlock_Small
4. **Chạy eval.py --model all** để tạo bảng so sánh tổng hợp
5. **Xuất kết quả** (bảng metrics, ảnh enhanced mẫu) cho báo cáo

---

## 11. Tóm Tắt File Quan Trọng

| File | Mô tả |
|------|--------|
| `models/zero_dce/blocks.py` | Các building blocks dùng chung (DSConv, ResBlock, DenseBlock) |
| `models/zero_dce/zero_dce.py` | Kiến trúc Zero-DCE baseline |
| `models/zero_dce/zero_dce_pp.py` | Kiến trúc Zero-DCE++ (lightweight) |
| `models/zero_dce/zdce_resblock_small.py` | Biến thể với 2 ResBlocks |
| `models/zero_dce/zdce_denseblock_small.py` | Biến thể với 2 DenseBlocks |
| `utils.py` | LOLDataset, VGGPerceptualLoss, calculate_metrics_numpy |
| `train.py` | Script huấn luyện CLI |
| `eval.py` | Script đánh giá CLI (PSNR/SSIM/FLOPs/Params/InferenceTime) |
| `train_notebook.py` | Marimo notebook tương tác (web UI) |
| `requirements.txt` | Danh sách thư viện |
