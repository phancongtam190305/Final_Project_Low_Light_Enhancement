import argparse
import subprocess
import sys
import time
import zipfile
from pathlib import Path


def run_eval(args):
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "eval.py",
        "--model",
        "all",
        "--data_dir",
        args.data_dir,
        "--device",
        args.device,
        "--checkpoint_dir",
        args.checkpoint_dir,
        "--results_dir",
        args.results_dir,
        "--csv_path",
        str(results_dir / "metrics.csv"),
        "--json_path",
        str(results_dir / "metrics.json"),
    ]
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True)


def add_dir_to_zip(zip_file, directory):
    directory = Path(directory)
    if not directory.exists():
        return

    for path in directory.rglob("*"):
        if path.is_file():
            zip_file.write(path, path)


def pack_artifacts(args):
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        add_dir_to_zip(zf, args.results_dir)
        add_dir_to_zip(zf, args.checkpoint_dir)
        add_dir_to_zip(zf, args.log_dir)
        if args.include_runs:
            add_dir_to_zip(zf, args.runs_dir)

    print(f"Packed artifacts to: {output}")


def main():
    parser = argparse.ArgumentParser(description="Run eval.py for all models and zip cloud artifacts.")
    parser.add_argument("--data_dir", default="./data")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--checkpoint_dir", default="./checkpoints")
    parser.add_argument("--results_dir", default="./results")
    parser.add_argument("--log_dir", default="./cloud_logs")
    parser.add_argument("--runs_dir", default="./runs")
    parser.add_argument("--include_runs", action="store_true", help="Include TensorBoard event files in the zip.")
    parser.add_argument(
        "--output",
        default=f"./artifacts/zero_dce_cloud_artifacts_{time.strftime('%Y%m%d_%H%M%S')}.zip",
    )
    args = parser.parse_args()

    run_eval(args)
    pack_artifacts(args)


if __name__ == "__main__":
    main()
