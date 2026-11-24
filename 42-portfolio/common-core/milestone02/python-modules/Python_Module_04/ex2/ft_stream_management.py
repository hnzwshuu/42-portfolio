#!/usr/bin/env python3

import sys
from typing import IO


def print_error(message: str) -> None:
    sys.stderr.write(f"[STDERR] {message}\n")
    sys.stderr.flush()


def read_file(filename: str) -> str | None:
    try:
        file: IO[str] = open(filename)
    except OSError as e:
        print_error(f"Error opening file '{filename}': {e}")
        return None
    data = file.read()
    file.close()
    print("---")
    print()
    print(data, end="")
    print()
    print("---")
    print(f"File '{filename}' closed.")
    return data


def add_archive_markers(data: str) -> str:
    new_data = ""
    for char in data:
        if char == "\n":
            new_data += "#\n"
        else:
            new_data += char
    if data != "" and data[-1] != "\n":
        new_data += "#"
    return new_data


def save_file(filename: str, data: str) -> bool:
    try:
        file = open(filename, mode='w')
    except OSError as e:
        print_error(f"Error opening file '{filename}': {e}")
        return False
    file.write(data)
    file.close()
    return True


def read_stdin_line() -> str:
    line = sys.stdin.readline()

    if line.endswith("\n"):
        return line[:-1]
    return line


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return
    filename = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file'{filename}'")
    data = read_file(filename)
    if data is None:
        return
    new_data = add_archive_markers(data)
    print()
    print("Transform data:")
    print("---")
    print()
    print(new_data, end="")
    print()
    print("---")
    print("Enter new file name (or empty): ", end="")
    sys.stdout.flush()
    new_filename = read_stdin_line()
    if new_filename == "":
        print("Not saving data.")
        return
    print(f"Saving data to '{new_filename}'")
    if save_file(new_filename, new_data):
        print(f"Data saved in file '{new_filename}'.")
    else:
        print("Data not saved.")
    return


if __name__ == "__main__":
    main()
