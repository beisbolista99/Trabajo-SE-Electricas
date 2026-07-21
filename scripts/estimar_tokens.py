from __future__ import annotations

import argparse
from pathlib import Path

from common import estimate_tokens, read_text


def estimate_file_tokens(path: Path) -> int:
    return estimate_tokens(read_text(path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimar tokens de un archivo de texto.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    print(estimate_file_tokens(args.path))


if __name__ == "__main__":
    main()

