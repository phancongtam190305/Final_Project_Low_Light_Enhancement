# Molab GPU Run Guide

Muc tieu: mo repo tren molab, gan GPU, setup nhanh, train 4 bien the Zero-DCE, eval va tai artifacts ve.

## 1. Dua repo len GitHub

`data/`, `checkpoints/`, `runs/` dang nam trong `.gitignore`, nen repo se khong day dataset/checkpoint/log len GitHub. Day code len GitHub truoc, dataset se chuan bi rieng tren cloud.

## 2. Mo repo tren molab

1. Vao `https://molab.marimo.io/github`.
2. Mo repo GitHub cua du an.
3. Trong molab, bat GPU tu nut cau hinh/specs cua notebook/session.
4. Mo terminal trong molab.

## 3. Cai dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-cloud.txt
```

Neu chua co dataset tren cloud, check moi truong truoc va bo qua data:

```bash
python scripts/cloud_check.py --skip_data
```

## 4. Chuan bi LOL-v1 dataset tu Google Drive

### 4.1. Tao zip dataset tren may local

Dam bao thu muc dataset co cau truc:

```text
data/
  our485/
    low/
    high/
  eval15/
    low/
    high/
```

Nen zip sao cho ben trong file zip co truc tiep `our485/` va `eval15/`, hoac co mot thu muc cha chua hai folder nay. Script se tu tim cau truc dung.

Vi du tren Windows: chuot phai vao folder `data` hoac folder chua `our485/` va `eval15/` -> Send to -> Compressed zipped folder. Dat ten:

```text
LOL-v1.zip
```

### 4.2. Upload zip len Google Drive

1. Vao Google Drive.
2. Upload `LOL-v1.zip`.
3. Chuot phai file -> Share.
4. Doi General access thanh `Anyone with the link`.
5. Role de `Viewer`.
6. Copy link.

Link thuong co dang:

```text
https://drive.google.com/file/d/FILE_ID/view?usp=sharing
```

`FILE_ID` la phan nam giua `/d/` va `/view`.

### 4.3. Tai dataset tren molab tu Google Drive

Dung link share:

```bash
python scripts/prepare_lol_v1.py --gdrive_url "PASTE_GOOGLE_DRIVE_SHARE_LINK_HERE"
```

Hoac dung file id:

```bash
python scripts/prepare_lol_v1.py --gdrive_id "PASTE_FILE_ID_HERE"
```

Sau do kiem tra:

```bash
python scripts/cloud_check.py
```

Lan dau chay co the mat thoi gian vi VGG16 pretrained weights duoc tai ve.

## 5. Chuan bi LOL-v1 dataset bang cach khac

Sau khi co file zip LOL-v1 tren molab:

```bash
python scripts/prepare_lol_v1.py --zip /path/to/LOL-v1.zip
```

Neu co direct URL toi file zip:

```bash
python scripts/prepare_lol_v1.py --url "https://example.com/LOL-v1.zip"
```

Neu da giai nen san vao mot thu muc:

```bash
python scripts/prepare_lol_v1.py --source_dir /path/to/extracted_lol
```

Script se tim cau truc `our485/` va `eval15/`, roi copy ve `./data`.

## 6. Smoke test 1 epoch

```bash
python train.py --model Zero_DCE --epochs 1 --batch_size 4 --device cuda --num_workers 2
```

Neu smoke test OK, se co:

- `checkpoints/best_Zero_DCE.pth`
- `checkpoints/last_Zero_DCE.pth`
- TensorBoard log trong `runs/`

## 7. Train 4 model

```bash
python scripts/train_all_cloud.py --epochs 50 --batch_size 16 --device cuda --num_workers 2
```

Mac dinh script dung `--resume auto`, nen neu molab session bi ngat, chay lai cung lenh tren de tiep tuc tu `checkpoints/last_<model>.pth`.

Co the train rieng model:

```bash
python scripts/train_all_cloud.py --only Zero_DCE_PP --epochs 50 --batch_size 16 --device cuda --num_workers 2
```

Neu gap CUDA OOM, giam `--batch_size` xuong `8`. De bao cao cong bang, nen dung cung batch size cho ca 4 model neu co the.

## 8. Eval va dong goi ket qua

```bash
python scripts/eval_and_pack.py --device cuda --include_runs
```

Ket qua chinh:

- `results/metrics.csv`
- `results/metrics.json`
- `results/<model>/val_enhanced_*.png`
- `artifacts/zero_dce_cloud_artifacts_*.zip`

Neu khong can TensorBoard logs trong zip:

```bash
python scripts/eval_and_pack.py --device cuda
```

## 9. Lenh nhanh voi Google Drive

```bash
python scripts/cloud_check.py --skip_data
python scripts/prepare_lol_v1.py --gdrive_url "PASTE_GOOGLE_DRIVE_SHARE_LINK_HERE"
python scripts/cloud_check.py
python train.py --model Zero_DCE --epochs 1 --batch_size 4 --device cuda --num_workers 2
python scripts/train_all_cloud.py --epochs 50 --batch_size 16 --device cuda --num_workers 2
python scripts/eval_and_pack.py --device cuda --include_runs
```
