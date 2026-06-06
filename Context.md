# Context.md - Final Project: Low-Light Image Enhancement

> Nhiem vu hien tai: huan luyen, danh gia va chuan bi bao cao cho 4 bien the Zero-DCE tren LOL-v1.  
> Cap nhat gan nhat: 2026-06-06.

---

## 1. Muc Tieu Va Pham Vi

Du an so sanh hieu nang Low-Light Image Enhancement tren tap LOL-v1 bang cac chi so PSNR, SSIM, FLOPs, Params va inference time.

Phan cua Do gom 4 model:

| Model | Mo ta |
|---|---|
| `Zero_DCE` | Baseline goc, Conv2d thuong, 8 alpha maps |
| `Zero_DCE_PP` | Ban nhe, dung DepthwiseSeparableConv |
| `ZDCE_ResBlock_Small` | Chen 2 ResBlock giua Conv3 va Conv4 |
| `ZDCE_DenseBlock_Small` | Chen 2 DenseBlock giua Conv3 va Conv4 |

Phan cua nhom:

| Thanh vien | Task | Trang thai |
|---|---|---|
| Do | 4 bien the Zero-DCE | Da train/eval cloud, can tong hop bao cao |
| Phuc | SCI | Placeholder |
| Ben | CPGA-Net variants | Placeholder |

---

## 2. Kien Truc Va Training Config

Tat ca Zero-DCE variants output 24 channels, tach thanh 8 alpha maps RGB. Moi lan tang sang dung:

```python
enhanced = enhanced + alpha * enhanced * (1.0 - enhanced)
```

Training dang dung supervised loss:

```text
Total Loss = L1(enhanced, ground_truth) + 0.01 * VGGPerceptualLoss(enhanced, ground_truth)
```

Config chuan can giu de so sanh cong bang:

| Parameter | Gia tri |
|---|---|
| Dataset | LOL-v1: `our485` train, `eval15` val/test |
| Optimizer | AdamW |
| LR | `1e-4` |
| Weight decay | `1e-4` |
| Scheduler | CosineAnnealingLR, `T_max=epochs` |
| Epochs | `50` |
| Batch size | `16` neu can khop config ban dau |
| AMP | Bat tren CUDA bang `torch.amp` |
| Grad clip | `max_norm=1.0` |
| Augmentation | random horizontal flip + vertical flip chi tren train |

Luu y: tren molab co GPU lon nen co the chay batch size cao hon, nhung neu Ben/nhom yeu cau cung config thi dung `batch_size=16`.

---

## 3. Repo Va GitHub

Remote:

```text
https://github.com/phancongtam190305/Final_Project_Low_Light_Enhancement.git
```

Nhanh dang dung cho cloud workflow:

```text
codex/cloud-gpu-setup
```

Draft PR:

```text
https://github.com/phancongtam190305/Final_Project_Low_Light_Enhancement/pull/1
```

Khong push dataset/checkpoint/log len Git. Cac thu muc `data/`, `checkpoints/`, `runs/`, `results/`, `artifacts/`, `cloud_logs/` duoc ignore.

---

## 4. File Va Script Quan Trong

| File | Vai tro |
|---|---|
| `train.py` | CLI train 1 model, co AMP moi, `best_*.pth`, `last_*.pth`, auto-resume an toan |
| `eval.py` | Eval PSNR/SSIM/FLOPs/Params/inference time, xuat CSV/JSON |
| `scripts/cloud_check.py` | Check CUDA, GPU, dataset, forward 4 model, warmup VGG16 |
| `scripts/prepare_lol_v1.py` | Chuan hoa dataset tu zip/source URL/Google Drive |
| `scripts/train_all_cloud.py` | Train lan luot 4 Zero-DCE variants, mac dinh `--resume auto` |
| `scripts/eval_and_pack.py` | Eval all model va zip artifacts |
| `requirements-cloud.txt` | Them `thop` va `gdown` cho cloud |
| `MOLAB_GPU_GUIDE.md` | Huong dan molab + Google Drive dataset |
| `train_notebook.py` | Marimo UI training, nhung full train nen uu tien CLI |

Auto-resume trong `train.py` da duoc guard: checkpoint smoke test `epochs=1` se khong bi resume nham cho run chinh thuc `epochs=50`.

---

## 5. Cloud/Molab Trang Thai

Da chay tren marimo/molab GPU:

| Muc | Gia tri |
|---|---|
| GPU | NVIDIA RTX PRO 6000 Blackwell Server Edition |
| VRAM | ~94.97 GB |
| CUDA | 13.0 |
| Torch | 2.12.0+cu130 |
| Python | 3.13.11 |
| Dataset check | OK: train 485 cap, eval 15 cap |
| VGG16 warmup | OK |

Dataset duoc dua len Google Drive dang zip, molab tai bang:

```bash
python scripts/prepare_lol_v1.py --gdrive_url "GOOGLE_DRIVE_SHARE_LINK"
```

---

## 6. Ket Qua Eval Cloud Hien Co

Da chay `scripts/eval_and_pack.py` va dong goi artifact:

```text
Final_Project_Low_Light_Enhancement/artifacts/zero_dce_cloud_artifacts_20260604_031456.zip
```

Bang ket qua tren best checkpoints:

| Model | Best epoch | Params | FLOPs | PSNR | SSIM | Infer ms/img |
|---|---:|---:|---:|---:|---:|---:|
| `Zero_DCE` | 7 | 79,416 | 19.008 GFLOPs | 18.6844 | 0.5678 | 1.31 |
| `Zero_DCE_PP` | 3 | 23,574 | 5.551 GFLOPs | 18.7440 | 0.5688 | 1.38 |
| `ZDCE_ResBlock_Small` | 5 | 116,408 | 27.855 GFLOPs | 18.5516 | 0.5708 | 1.87 |
| `ZDCE_DenseBlock_Small` | 8 | 134,840 | 32.279 GFLOPs | 18.5280 | 0.5691 | 2.06 |

Nhan xet nhanh:

- PSNR cao nhat hien tai: `Zero_DCE_PP` (`18.7440 dB`).
- SSIM cao nhat hien tai: `ZDCE_ResBlock_Small` (`0.5708`).
- FLOPs/params thap nhat: `Zero_DCE_PP`.
- Can kiem tra log train neu muon xac nhan full run da dat dung `epochs=50`; best checkpoint co the nam som hon epoch cuoi.

---

## 7. Lenh Molab Can Nho

Cap nhat code:

```bash
cd Final_Project_Low_Light_Enhancement
git pull
python -m pip install -r requirements-cloud.txt
```

Check cloud:

```bash
python scripts/cloud_check.py
```

Train dung config chuan:

```bash
python scripts/train_all_cloud.py --epochs 50 --batch_size 16 --lr 1e-4 --weight_decay 1e-4 --device cuda --num_workers 2
```

Eval va dong goi:

```bash
python scripts/eval_and_pack.py --device cuda --include_runs
```

Neu molab file panel kho tai artifact, tao nut download:

```python
from pathlib import Path
import marimo as mo

zip_path = Path("Final_Project_Low_Light_Enhancement/artifacts/zero_dce_cloud_artifacts_20260604_031456.zip")
mo.download(data=zip_path.read_bytes(), filename=zip_path.name)
```

---

## 8. Next Steps

1. Tai artifact zip ve may local va luu lai de khong mat khi molab session tat.
2. Mo `results/metrics.csv` va anh trong `results/<model>/` de dua vao bao cao.
3. Neu can xem chat luong anh theo checkpoint:
   - Hien co san `best_*.pth` va `last_*.pth`.
   - Chua co checkpoint tung epoch tru khi sua them `--save_every` va train lai/continue.
   - Nen them script `scripts/infer_checkpoints.py` de tao grid `Low | Enhanced(best) | Enhanced(last) | GT` cho moi model.
4. Neu can ket qua cong bang tuyet doi voi config cua Ben/nhom, xac nhan lai batch size/epochs/log full train truoc khi chot bang.
