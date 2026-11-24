#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    x = int(temp_str)
    if x > 40:
        raise ValueError(f"{x}°C is too hot for plants (max 40°C)")
    elif x < 0:
        raise ValueError(f"{x}°C is too cold for plants (min 0°C)")
    else:
        return x


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
    print("Input data is '100'")
    try:
        x = input_temperature("100")
    except Exception as e:
        print(f"Caught input_temperature error: {e}")
    else:
        print(f"Temperature is now {x}°C")
    print()
    print("Input data is '-50'")
    try:
        x = input_temperature("-50")
    except Exception as e:
        print(f"Caught input_temperature error: {e}")
    else:
        print(f"Temperature is now {x}°C")
    print()
    print("All tests completed - program didn't crash!")


def main() -> None:
    print("=== Garden Temperature Checker ===")
    print()
    test_temperature()


if __name__ == "__main__":
    main()
