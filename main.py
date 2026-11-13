#!/usr/bin/env python3
"""news-image-13nov-entry-2: copy the repo-held front-page image to /output/entry.png.

Deterministic, stdlib-only, no network, no randomness: running twice
produces byte-identical output.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "/output"))
DST = OUTPUT_DIR / "entry.png"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
