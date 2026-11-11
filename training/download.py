"""Download and extract the HWRT database (https://zenodo.org/records/50022)."""

import argparse
import hashlib
import tarfile
import urllib.request
from pathlib import Path

URL = "https://zenodo.org/api/records/50022/files/2015-01-28-data.tar/content"
MD5 = "2bf1d089ce65c0a39e57064516f1bd1c"  # from the Zenodo record
NAME = "2015-01-28-data.tar"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "data")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    tar_path = args.out / NAME
    if not tar_path.exists():
        print(f"Downloading {URL} ...")
        tmp = tar_path.with_suffix(".part")
        urllib.request.urlretrieve(URL, tmp)
        tmp.rename(tar_path)
    md5 = hashlib.md5(tar_path.read_bytes()).hexdigest()
    if md5 != MD5:
        raise SystemExit(f"{tar_path}: md5 {md5} != expected {MD5}; delete it and retry")
    with tarfile.open(tar_path) as tar:
        tar.extractall(args.out, filter="data")
    for p in sorted(args.out.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(args.out)} ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
