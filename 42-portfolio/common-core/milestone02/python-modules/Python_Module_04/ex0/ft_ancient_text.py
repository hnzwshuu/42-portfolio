#!/usr/bin/env python3

import sys
from typing import IO


def read_file(filename: str) -> None:
    try:
        file: IO[str] = open(filename)
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return
    data = file.read()
    file.close()
    print("---")
    print()
    print(data, end="")
    print()
    print("---")
    print(f"File '{filename}' closed.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return
    filename = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file'{filename}'")
    read_file(filename)


if __name__ == "__main__":
    main()
