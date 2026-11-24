#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("Input data is '25'")
    try:
        x = input_temperature("25")
    except Exception as e:
        print(f"Caught input_temperature error: {e}")
    else:
        print(f"Temperature is now {x}°C")
    print()
    print("Input data is 'abc'")
    try:
        x = input_temperature("abc")
    except Exception as e:
        print(f"Caught input_temperature error: {e}")
    else:
        print(f"Temperature is now {x}°C")
    print()
    print("All tests completed - program didn't crash!")


def main() -> None:
    print("=== Garden Temperature ===")
    print()

    test_temperature()


if __name__ == "__main__":
    main()
