#!/usr/bin/env python3
"""news-image-13nov-entry-2: copy the repo-held front-page image to /output/entry.png.

Deterministic, stdlib-only, no network, no randomness: running twice
produces byte-identical output. Before copying, the source image is
validated (PNG signature, at most 1024x1024, at most 1 MiB); after
copying, the destination is verified byte-for-byte (SHA-256 and size)
and the run fails loudly if anything differs.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path
from typing import NoReturn

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "/output"))
DST = OUTPUT_DIR / "entry.png"

MAX_DIMENSION = 1024
MAX_BYTES = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_png(path: Path) -> None:
    """Check path is a PNG, at most 1024x1024 and at most 1 MiB."""
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        fail(f"{path} is {len(data)} bytes, over the 1 MiB limit")
    if data[:8] != PNG_SIGNATURE:
        fail(f"{path} does not start with the PNG signature")
    if len(data) < 24:
        fail(f"{path} is too short to contain a PNG IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        fail(f"{path} is {width}x{height}, over the 1024x1024 limit")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    validate_png(SRC)
    src_hash = sha256_of(SRC)
    src_size = SRC.stat().st_size
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)
    if DST.stat().st_size != src_size or sha256_of(DST) != src_hash:
        fail(f"verification failed: {DST} does not match {SRC} byte-for-byte")
    print(f"wrote {DST} ({src_size} bytes, sha256 {src_hash})")


if __name__ == "__main__":
    main()
