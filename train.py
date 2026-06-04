import argparse
import os
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from models import Zero_DCE, Zero_DCE_PP, ZDCE_ResBlock_Small, ZDCE_DenseBlock_Small
from utils import LOLDataset, VGGPerceptualLoss, calculate_metrics_numpy


MODEL_CLASSES = {
    "Zero_DCE": Zero_DCE,
    "Zero_DCE_PP": Zero_DCE_PP,
    "ZDCE_ResBlock_Small": ZDCE_ResBlock_Small,
    "ZDCE_DenseBlock_Small": ZDCE_DenseBlock_Small,
}


def resolve_resume_path(resume_arg, model_name):
    if not resume_arg:
        return None
    if resume_arg.lower() == "auto":
        return Path("checkpoints") / f"last_{model_name}.pth"
    return Path(resume_arg)


def save_checkpoint(path, epoch, model, optimizer, scheduler, psnr, ssim, best_psnr, args):
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "psnr": psnr,
            "ssim": ssim,
            "best_psnr": best_psnr,
            "args": vars(args),
        },
        path,
    )


def maybe_resume(resume_path, model, optimizer, scheduler, device, required=False):
    if resume_path is None:
        return 0, -1.0

    if not resume_path.exists():
        if required:
            raise FileNotFoundError(f"Resume checkpoint not found: {resume_path}")
        print(f"No auto-resume checkpoint found at {resume_path}; starting fresh.")
        return 0, -1.0

    print(f"Loading resume checkpoint: {resume_path}")
    checkpoint = torch.load(resume_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])

    if "optimizer_state_dict" in checkpoint:
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    if "scheduler_state_dict" in checkpoint:
        scheduler.load_state_dict(checkpoint["scheduler_state_dict"])

    start_epoch = int(checkpoint.get("epoch", 0))
    best_psnr = float(checkpoint.get("best_psnr", checkpoint.get("psnr", -1.0)))
    print(f"Resumed after epoch {start_epoch}; best PSNR so far: {best_psnr:.2f} dB")
    return start_epoch, best_psnr


def main():
    parser = argparse.ArgumentParser(description="Huan luyen mo hinh Low-Light Enhancement (Zero-DCE)")
    parser.add_argument(
        "--model",
        type=str,
        default="Zero_DCE",
        choices=list(MODEL_CLASSES.keys()),
        help="Ten mo hinh muon huan luyen",
    )
    parser.add_argument("--data_dir", type=str, default="./data", help="Duong dan den thu muc LOL-v1")
    parser.add_argument("--epochs", type=int, default=50, help="Tong so epochs can dat")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--weight_decay", type=float, default=1e-4, help="Weight decay")
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Thiet bi huan luyen (cuda hoac cpu)",
    )
    parser.add_argument("--num_workers", type=int, default=0, help="So worker cho DataLoader")
    parser.add_argument("--resume", type=str, default="", help="Checkpoint de tiep tuc; dung 'auto' cho last_<model>.pth")
    parser.add_argument("--no_amp", action="store_true", help="Tat mixed precision AMP")

    args = parser.parse_args()
    device = torch.device(args.device)
    use_cuda = device.type == "cuda"
    use_amp = use_cuda and not args.no_amp

    if use_cuda and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but torch.cuda.is_available() is False.")
    if use_cuda:
        torch.backends.cudnn.benchmark = True

    print("\n" + "=" * 60)
    print(f" TRAINING MODEL: {args.model} ".center(60, "="))
    print("=" * 60)
    print(f"Dataset path:  {args.data_dir}")
    print(f"Target epochs: {args.epochs}")
    print(f"Batch size:    {args.batch_size}")
    print(f"Learning rate: {args.lr}")
    print(f"Device:        {device}")
    if use_cuda:
        print(f"GPU:           {torch.cuda.get_device_name(device)}")
    print(f"AMP enabled:   {use_amp}")
    print("=" * 60 + "\n")

    try:
        train_dataset = LOLDataset(args.data_dir, split="train")
        val_dataset = LOLDataset(args.data_dir, split="val")
    except Exception as exc:
        print(f"Data load error: {exc}")
        print("Check that ./data/our485 and ./data/eval15 exist with low/ and high/ folders.")
        return

    print(f"Train images: {len(train_dataset)} | Val images: {len(val_dataset)}")
    loader_kwargs = {
        "num_workers": args.num_workers,
        "pin_memory": use_cuda,
    }
    if args.num_workers > 0:
        loader_kwargs["persistent_workers"] = True

    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        **loader_kwargs,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=1,
        shuffle=False,
        **loader_kwargs,
    )

    model = MODEL_CLASSES[args.model]().to(device)
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    resume_path = resolve_resume_path(args.resume, args.model)
    start_epoch, best_psnr = maybe_resume(
        resume_path,
        model,
        optimizer,
        scheduler,
        device,
        required=bool(args.resume and args.resume.lower() != "auto"),
    )

    if start_epoch >= args.epochs:
        print(f"Checkpoint is already at epoch {start_epoch}; target epochs is {args.epochs}. Nothing to do.")
        return

    print("Loading VGG16 perceptual loss. First run may download pretrained weights...")
    l1_loss_fn = nn.L1Loss()
    perceptual_loss_fn = VGGPerceptualLoss().to(device)
    print("VGG16 perceptual loss ready.")

    scaler = torch.amp.GradScaler(device.type, enabled=use_amp)

    checkpoints_dir = Path("checkpoints")
    runs_dir = Path("runs")
    checkpoints_dir.mkdir(exist_ok=True)
    runs_dir.mkdir(exist_ok=True)

    from torch.utils.tensorboard import SummaryWriter

    writer = SummaryWriter(log_dir=str(runs_dir / f"{args.model}_{time.strftime('%m%d_%H%M%S')}"))

    start_time_total = time.time()
    last_checkpoint_path = checkpoints_dir / f"last_{args.model}.pth"
    best_checkpoint_path = checkpoints_dir / f"best_{args.model}.pth"

    for epoch in range(start_epoch, args.epochs):
        epoch_start_time = time.time()
        model.train()
        epoch_loss = 0.0

        for low_img, high_img in train_loader:
            low_img = low_img.to(device, non_blocking=use_cuda)
            high_img = high_img.to(device, non_blocking=use_cuda)

            optimizer.zero_grad(set_to_none=True)

            with torch.amp.autocast(device_type=device.type, enabled=use_amp):
                enhanced_img = model(low_img)
                loss_l1 = l1_loss_fn(enhanced_img, high_img)
                loss_vgg = perceptual_loss_fn(enhanced_img, high_img)
                loss = loss_l1 + 0.01 * loss_vgg

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()

            epoch_loss += loss.item() * low_img.size(0)

        epoch_loss /= len(train_dataset)
        scheduler.step()

        model.eval()
        epoch_psnrs = []
        epoch_ssims = []

        with torch.no_grad():
            for low_img_val, high_img_val in val_loader:
                low_img_val = low_img_val.to(device, non_blocking=use_cuda)
                high_img_val = high_img_val.to(device, non_blocking=use_cuda)

                enhanced_val = model(low_img_val)
                psnr, ssim = calculate_metrics_numpy(enhanced_val, high_img_val)
                epoch_psnrs.append(psnr)
                epoch_ssims.append(ssim)

        mean_psnr = float(np.mean(epoch_psnrs))
        mean_ssim = float(np.mean(epoch_ssims))
        epoch_time = time.time() - epoch_start_time
        completed_epoch = epoch + 1

        writer.add_scalar("Loss/Train", epoch_loss, completed_epoch)
        writer.add_scalar("Metrics/Val_PSNR", mean_psnr, completed_epoch)
        writer.add_scalar("Metrics/Val_SSIM", mean_ssim, completed_epoch)

        print(
            f"Epoch [{completed_epoch:2d}/{args.epochs:2d}] | "
            f"Loss: {epoch_loss:.5f} | "
            f"Val PSNR: {mean_psnr:.2f} dB | "
            f"Val SSIM: {mean_ssim:.4f} | "
            f"Time: {epoch_time:.1f}s"
        )

        if mean_psnr > best_psnr:
            best_psnr = mean_psnr
            save_checkpoint(
                best_checkpoint_path,
                completed_epoch,
                model,
                optimizer,
                scheduler,
                mean_psnr,
                mean_ssim,
                best_psnr,
                args,
            )
            print(f"   --> Saved new best checkpoint: {best_checkpoint_path} (PSNR {best_psnr:.2f} dB)")

        save_checkpoint(
            last_checkpoint_path,
            completed_epoch,
            model,
            optimizer,
            scheduler,
            mean_psnr,
            mean_ssim,
            best_psnr,
            args,
        )
        print(f"   --> Saved resume checkpoint: {last_checkpoint_path}")

    writer.close()
    total_time = time.time() - start_time_total
    print("\n" + "=" * 60)
    print(" TRAINING FINISHED ".center(60, "="))
    print("=" * 60)
    print(f"Total time:       {total_time / 60:.2f} minutes")
    print(f"Best PSNR:        {best_psnr:.2f} dB")
    print(f"Best checkpoint:  {best_checkpoint_path}")
    print(f"Resume checkpoint:{last_checkpoint_path}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
