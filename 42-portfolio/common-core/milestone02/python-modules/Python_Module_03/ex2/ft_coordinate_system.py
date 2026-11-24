#!/usr/bin/env python3
import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw_value = input("Enter new coordinate as floats in format 'x,y,z': ")
        parts = raw_value.split(",")
        try:
            raw_x, raw_y, raw_z = parts
        except ValueError:
            print("Invalid syntax")
            continue
        try:
            x_pos = float(raw_x.strip())
            y_pos = float(raw_y.strip())
            z_pos = float(raw_z.strip())
            return (x_pos, y_pos, z_pos)
        except ValueError as e:
            bad_value = find_bad_value(parts)
            print(f"Error on parameter '{bad_value}': {e}")


def find_bad_value(parts: list[str]) -> str:
    i = 0
    try:
        while i < 3:
            float(parts[i].strip())
            i += 1
    except ValueError:
        return parts[i].strip()
    return ""


def distance_between(first_pos: tuple[float, float, float],
                     second_pos: tuple[float, float, float]) -> float:
    return math.sqrt(
        (second_pos[0] - first_pos[0]) ** 2
        + (second_pos[1] - first_pos[1]) ** 2
        + (second_pos[2] - first_pos[2]) ** 2
    )


def main() -> None:
    print("=== Game Coordinate System ===")
    print()
    print("Get a first set of coordinates")
    first_tuple = get_player_pos()
    print(f"Got a first tuple: {first_tuple}")
    print(f"It includes: \
X={first_tuple[0]}, Y={first_tuple[1]}, Z={first_tuple[2]}")
    print(f"Distance to center: \
{round(distance_between((0.0, 0.0, 0.0), first_tuple), 4)}")
    print()
    print("Get a second set of coordinates")
    second_tuple = get_player_pos()
    print(f"Distance between the 2 sets of coordinates: \
{round(distance_between(first_tuple, second_tuple), 4)}")


if __name__ == "__main__":
    main()
