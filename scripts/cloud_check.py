import argparse
import platform
import subprocess
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from models import Zero_DCE, Zero_DCE_PP, ZDCE_ResBlock_Small, ZDCE_DenseBlock_Small
from utils import VGGPerceptualLoss


MODEL_CLASSES = {
    "Zero_DCE": Zero_DCE,
    "Zero_DCE_PP": Zero_DCE_PP,
    "ZDCE_ResBlock_Small": ZDCE_ResBlock_Small,
    "ZDCE_DenseBlock_Small": ZDCE_DenseBlock_Small,
}


def run_optional_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20, check=False)
    except FileNotFoundError:
        print(f"{command[0]} not found.")
        return
    except subprocess.TimeoutExpired:
        print(f"{' '.join(command)} timed out.")
        return

    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())


def count_images(path):
    exts = {".png", ".jpg", ".jpeg"}
    if not path.exists():
        return 0
    return sum(1 for item in path.iterdir() if item.suffix.lower() in exts)


def check_data(data_dir):
    data_dir = Path(data_dir)
    required = [
        data_dir / "our485" / "low",
        data_dir / "our485" / "high",
        data_dir / "eval15" / "low",
        data_dir / "eval15" / "high",
    ]

    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print("Dataset check: FAILED")
        for path in missing:
            print(f"Missing: {path}")
        return False

    print("Dataset check: OK")
    print(f"our485/low:  {count_images(data_dir / 'our485' / 'low')} images")
    print(f"our485/high: {count_images(data_dir / 'our485' / 'high')} images")
    print(f"eval15/low:  {count_images(data_dir / 'eval15' / 'low')} images")
    print(f"eval15/high: {count_images(data_dir / 'eval15' / 'high')} images")
    return True


def check_models(device):
    print("\nModel forward checks:")
    dummy = torch.rand(1, 3, 64, 64, device=device)
    with torch.no_grad():
        for name, model_cls in MODEL_CLASSES.items():
            model = model_cls().to(device).eval()
            output = model(dummy)
            param_count = sum(p.numel() for p in model.parameters() if p.requires_grad)
            print(f"{name:24s} params={param_count:8,d} output_shape={tuple(output.shape)}")


def warmup_vgg(device):
    print("\nVGG16 perceptual loss warmup. First run may download pretrained weights...")
    loss_fn = VGGPerceptualLoss().to(device)
    x = torch.rand(1, 3, 64, 64, device=device)
    y = torch.rand(1, 3, 64, 64, device=device)
    with torch.no_grad():
        loss = loss_fn(x, y)
    print(f"VGG16 perceptual loss ready. Test loss={float(loss):.6f}")


def main():
    parser = argparse.ArgumentParser(description="Check molab/cloud GPU readiness for this project.")
    parser.add_argument("--data_dir", default="./data", help="Path to LOL-v1 dataset root.")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--skip_data", action="store_true", help="Skip LOL-v1 folder checks.")
    parser.add_argument("--skip_vgg", action="store_true", help="Skip VGG16 weight warmup.")
    args = parser.parse_args()

    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but torch.cuda.is_available() is False.")

    print("Environment")
    print(f"Python:   {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    print(f"Torch:    {torch.__version__}")
    print(f"CUDA OK:  {torch.cuda.is_available()}")
    print(f"Device:   {device}")
    if torch.cuda.is_available():
        print(f"CUDA:     {torch.version.cuda}")
        print(f"GPU:      {torch.cuda.get_device_name(0)}")
        props = torch.cuda.get_device_properties(0)
        print(f"VRAM:     {props.total_memory / (1024 ** 3):.2f} GB")

    print("\nnvidia-smi")
    run_optional_command(["nvidia-smi"])

    data_ok = True if args.skip_data else check_data(args.data_dir)
    check_models(device)
    if not args.skip_vgg:
        warmup_vgg(device)

    if not data_ok:
        raise SystemExit(2)

    print("\nCloud readiness check finished.")


if __name__ == "__main__":
    main()
