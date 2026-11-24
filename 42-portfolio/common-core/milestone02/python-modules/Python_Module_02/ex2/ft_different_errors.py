#!/usr/bin/env python3

def garden_operations(operation_number: int) -> None:
    result = 1
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        result = result // 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        result = "hello" + 42


def test_error(operation_number: int) -> None:
    print(f"Testing operation: {operation_number}...")
    try:
        garden_operations(operation_number)
    except ValueError as e:
        print(f"Caught ValueError: {e}")
    except ZeroDivisionError as e:
        print(f"Caught ZeroDivisionError: {e}")
    except FileNotFoundError as e:
        print(f"Caught FileNotFoundError: {e}")
    except TypeError as e:
        print(f"Caught TypeError: {e}")
    else:
        print("Operation completed successfully")


def test_error_types() -> None:
    test_error(0)
    test_error(1)
    test_error(2)
    test_error(3)
    test_error(4)
    print()
    print("All error types tested successfully!")


def main() -> None:
    print("=== Garden Error Types Demo ===")
    test_error_types()


if __name__ == "__main__":
    main()
