import argparse
import csv
import json
import os
import time
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

from models import Zero_DCE, Zero_DCE_PP, ZDCE_ResBlock_Small, ZDCE_DenseBlock_Small
from utils import LOLDataset, calculate_metrics_numpy


MODEL_CLASSES = {
    "Zero_DCE": Zero_DCE,
    "Zero_DCE_PP": Zero_DCE_PP,
    "ZDCE_ResBlock_Small": ZDCE_ResBlock_Small,
    "ZDCE_DenseBlock_Small": ZDCE_DenseBlock_Small,
}


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def estimate_flops(model, device):
    """
    Estimate FLOPs with thop if it is installed.
    """
    try:
        from thop import profile

        dummy_input = torch.randn(1, 3, 400, 600).to(device)
        flops, _ = profile(model, inputs=(dummy_input,), verbose=False)
        return f"{flops / 1e9:.3f} GFLOPs"
    except ImportError:
        return "N/A (install thop)"


def evaluate_model(model_name, data_dir, device, checkpoint_dir, results_dir):
    print(f"\n--- Evaluating model: {model_name} ---")

    if model_name not in MODEL_CLASSES:
        raise ValueError(f"Unknown model name: {model_name}")

    model = MODEL_CLASSES[model_name]().to(device)

    params_count = count_parameters(model)
    flops_str = estimate_flops(model, device)

    print(f"Trainable parameters: {params_count:,}")
    print(f"Estimated FLOPs (400x600 image): {flops_str}")

    checkpoint_path = checkpoint_dir / f"best_{model_name}.pth"
    if not checkpoint_path.exists():
        print(f"Warning: checkpoint not found at {checkpoint_path}. Train this model first.")
        return None

    print(f"Loading checkpoint: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    print(
        f"Checkpoint epoch {checkpoint['epoch']} "
        f"(PSNR: {checkpoint['psnr']:.4f} dB, SSIM: {checkpoint['ssim']:.4f})"
    )

    try:
        val_dataset = LOLDataset(data_dir, split="val")
    except Exception as exc:
        print(f"Dataset load error: {exc}")
        return None

    use_cuda = device.type == "cuda"
    val_loader = DataLoader(
        val_dataset,
        batch_size=1,
        shuffle=False,
        num_workers=0,
        pin_memory=use_cuda,
    )

    model.eval()
    psnrs = []
    ssims = []
    inference_times = []

    output_img_dir = results_dir / model_name
    output_img_dir.mkdir(parents=True, exist_ok=True)

    with torch.no_grad():
        for idx, (low_img, high_img) in enumerate(val_loader):
            low_img = low_img.to(device, non_blocking=use_cuda)
            high_img = high_img.to(device, non_blocking=use_cuda)

            if use_cuda:
                torch.cuda.synchronize()
            start_time = time.time()
            enhanced_img = model(low_img)
            if use_cuda:
                torch.cuda.synchronize()
            infer_time = time.time() - start_time
            inference_times.append(infer_time)

            psnr, ssim = calculate_metrics_numpy(enhanced_img, high_img)
            psnrs.append(psnr)
            ssims.append(ssim)

            if idx < 3:
                enhanced_np = enhanced_img[0].detach().cpu().numpy().transpose(1, 2, 0)
                enhanced_np = np.clip(enhanced_np * 255.0, 0, 255).astype(np.uint8)

                from PIL import Image

                img = Image.fromarray(enhanced_np)
                img.save(output_img_dir / f"val_enhanced_{idx + 1}.png")

    mean_psnr = float(np.mean(psnrs))
    mean_ssim = float(np.mean(ssims))
    mean_time = float(np.mean(inference_times))

    print("\n--- Evaluation results ---")
    print(f"Average PSNR: {mean_psnr:.4f} dB")
    print(f"Average SSIM: {mean_ssim:.4f}")
    print(f"Average inference time/image: {mean_time * 1000:.2f} ms")
    print(f"Saved sample enhanced images to: {output_img_dir}")

    return {
        "model_name": model_name,
        "params": params_count,
        "flops": flops_str,
        "psnr": mean_psnr,
        "ssim": mean_ssim,
        "infer_time_ms": mean_time * 1000,
    }


def write_results(results, csv_path, json_path):
    if csv_path:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["model_name", "params", "flops", "psnr", "ssim", "infer_time_ms"],
            )
            writer.writeheader()
            writer.writerows(results)
        print(f"Saved CSV metrics to: {csv_path}")

    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Saved JSON metrics to: {json_path}")


def main():
    parser = argparse.ArgumentParser(description="Danh gia mo hinh Low-Light Enhancement tren tap test")
    parser.add_argument(
        "--model",
        type=str,
        default="Zero_DCE",
        choices=list(MODEL_CLASSES.keys()) + ["all"],
        help="Ten mo hinh can danh gia hoac 'all' de danh gia toan bo",
    )
    parser.add_argument("--data_dir", type=str, default="./data", help="Duong dan den thu muc LOL-v1")
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Thiet bi chay (cuda/cpu)",
    )
    parser.add_argument("--checkpoint_dir", type=str, default="./checkpoints", help="Thu muc checkpoint")
    parser.add_argument("--results_dir", type=str, default="./results", help="Thu muc luu anh va metrics")
    parser.add_argument("--csv_path", type=str, default="", help="Duong dan xuat metrics CSV")
    parser.add_argument("--json_path", type=str, default="", help="Duong dan xuat metrics JSON")

    args = parser.parse_args()
    device = torch.device(args.device)

    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but torch.cuda.is_available() is False.")

    checkpoint_dir = Path(args.checkpoint_dir)
    results_dir = Path(args.results_dir)

    models_to_eval = list(MODEL_CLASSES.keys()) if args.model == "all" else [args.model]

    results = []
    for model_name in models_to_eval:
        result = evaluate_model(model_name, args.data_dir, device, checkpoint_dir, results_dir)
        if result:
            results.append(result)

    if results:
        print("\n" + "=" * 100)
        print(" ZERO-DCE VARIANT COMPARISON ".center(100, "="))
        print("=" * 100)
        print(
            f"{'Model':30s} | {'Params':12s} | {'FLOPs':15s} | "
            f"{'PSNR (dB)':10s} | {'SSIM':8s} | {'Infer ms':9s}"
        )
        print("-" * 100)
        for row in results:
            print(
                f"{row['model_name']:30s} | {row['params']:12,d} | {row['flops']:15s} | "
                f"{row['psnr']:10.4f} | {row['ssim']:8.4f} | {row['infer_time_ms']:9.2f}"
            )
        print("=" * 100)

    csv_path = Path(args.csv_path) if args.csv_path else None
    json_path = Path(args.json_path) if args.json_path else None
    write_results(results, csv_path, json_path)


if __name__ == "__main__":
    main()
