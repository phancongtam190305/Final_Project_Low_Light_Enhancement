import argparse
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path


def has_lol_structure(path):
    return all(
        (path / split / kind).exists()
        for split in ("our485", "eval15")
        for kind in ("low", "high")
    )


def find_lol_root(search_root):
    search_root = Path(search_root)
    if has_lol_structure(search_root):
        return search_root

    for candidate in search_root.rglob("our485"):
        parent = candidate.parent
        if has_lol_structure(parent):
            return parent

    return None


def download_file(url, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = url.rstrip("/").split("/")[-1] or "lol_v1.zip"
    output_path = output_dir / filename
    print(f"Downloading dataset archive to {output_path}")
    urllib.request.urlretrieve(url, output_path)
    return output_path


def download_gdrive(gdrive_url, gdrive_id, output_dir):
    try:
        import gdown
    except ImportError as exc:
        raise RuntimeError("Google Drive download needs gdown. Install with: pip install gdown") from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "LOL-v1.zip"

    if gdrive_id:
        print(f"Downloading Google Drive file id={gdrive_id} to {output_path}")
        downloaded = gdown.download(id=gdrive_id, output=str(output_path), quiet=False)
    else:
        print(f"Downloading Google Drive URL to {output_path}")
        downloaded = gdown.download(url=gdrive_url, output=str(output_path), quiet=False, fuzzy=True)

    if downloaded is None:
        raise RuntimeError(
            "Google Drive download failed. Make sure the file is shared as 'Anyone with the link can view'."
        )

    return Path(downloaded)


def extract_zip(zip_path, output_dir):
    print(f"Extracting {zip_path} to {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(output_dir)
    return output_dir


def copy_dataset(source_root, target_dir):
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    for split in ("our485", "eval15"):
        src = source_root / split
        dst = target_dir / split
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    print(f"Prepared LOL-v1 dataset at {target_dir}")


def main():
    parser = argparse.ArgumentParser(description="Prepare LOL-v1 folder structure for training.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--zip", dest="zip_path", help="Path to a LOL-v1 zip archive.")
    source.add_argument("--source_dir", help="Path to an extracted LOL-v1 folder.")
    source.add_argument("--url", help="Direct URL to a LOL-v1 zip archive.")
    source.add_argument("--gdrive_url", help="Google Drive share URL to a LOL-v1 zip archive.")
    source.add_argument("--gdrive_id", help="Google Drive file id for a LOL-v1 zip archive.")
    parser.add_argument("--target_dir", default="./data", help="Output dataset root expected by train.py.")
    parser.add_argument("--work_dir", default="./_dataset_tmp", help="Temporary download/extract folder.")
    args = parser.parse_args()

    work_dir = Path(args.work_dir)

    if args.url:
        zip_path = download_file(args.url, work_dir)
        extract_root = extract_zip(zip_path, work_dir / "extracted")
        source_root = find_lol_root(extract_root)
    elif args.gdrive_url or args.gdrive_id:
        zip_path = download_gdrive(args.gdrive_url, args.gdrive_id, work_dir)
        extract_root = extract_zip(zip_path, work_dir / "extracted")
        source_root = find_lol_root(extract_root)
    elif args.zip_path:
        zip_path = Path(args.zip_path)
        if not zip_path.exists():
            raise FileNotFoundError(zip_path)
        extract_root = extract_zip(zip_path, work_dir / "extracted")
        source_root = find_lol_root(extract_root)
    else:
        source_root = find_lol_root(args.source_dir)

    if source_root is None:
        print("Could not find LOL-v1 structure with our485/ and eval15/ folders.", file=sys.stderr)
        raise SystemExit(2)

    copy_dataset(source_root, args.target_dir)
    print("Done. You can now run: python scripts/cloud_check.py")


if __name__ == "__main__":
    main()
