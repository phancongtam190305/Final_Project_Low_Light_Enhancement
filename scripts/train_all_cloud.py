import argparse
import subprocess
import sys
import time
from pathlib import Path


MODELS = [
    "Zero_DCE",
    "Zero_DCE_PP",
    "ZDCE_ResBlock_Small",
    "ZDCE_DenseBlock_Small",
]


def stream_command(command, log_path):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"\nRunning: {' '.join(command)}")
    print(f"Log: {log_path}")

    with log_path.open("w", encoding="utf-8") as log_file:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        assert process.stdout is not None
        for line in process.stdout:
            print(line, end="")
            log_file.write(line)

        return process.wait()


def main():
    parser = argparse.ArgumentParser(description="Train all Zero-DCE variants on a cloud GPU.")
    parser.add_argument("--data_dir", default="./data")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--weight_decay", type=float, default=1e-4)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--num_workers", type=int, default=2)
    parser.add_argument("--no_resume", action="store_true", help="Start fresh instead of --resume auto.")
    parser.add_argument("--no_amp", action="store_true")
    parser.add_argument("--only", nargs="*", choices=MODELS, help="Train only selected model names.")
    parser.add_argument("--log_dir", default="./cloud_logs")
    args = parser.parse_args()

    models = args.only if args.only else MODELS
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    for model_name in models:
        command = [
            sys.executable,
            "train.py",
            "--model",
            model_name,
            "--data_dir",
            args.data_dir,
            "--epochs",
            str(args.epochs),
            "--batch_size",
            str(args.batch_size),
            "--lr",
            str(args.lr),
            "--weight_decay",
            str(args.weight_decay),
            "--device",
            args.device,
            "--num_workers",
            str(args.num_workers),
        ]

        if not args.no_resume:
            command.extend(["--resume", "auto"])
        if args.no_amp:
            command.append("--no_amp")

        log_path = Path(args.log_dir) / f"{timestamp}_{model_name}.log"
        return_code = stream_command(command, log_path)
        if return_code != 0:
            print(f"Training failed for {model_name} with exit code {return_code}.")
            raise SystemExit(return_code)

    print("\nAll requested models finished training.")


if __name__ == "__main__":
    main()
