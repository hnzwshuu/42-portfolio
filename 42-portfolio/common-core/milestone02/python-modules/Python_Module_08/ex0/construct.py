import sys
import os
import site


def is_virtual_environment() -> bool:
    return sys.prefix != sys.base_prefix


def environment_name() -> str:
    return os.path.basename(sys.prefix)


def print_construct_instructions() -> None:
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows")
    print()
    print("Then run this program again.")


def main() -> None:
    print()
    if is_virtual_environment():
        print("MATRIX STATUS: Welcome to the construct")
    else:
        print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")

    if is_virtual_environment():
        print(f"Virtual Environment: {environment_name()}")
        print(f"Environment Path: {sys.prefix}")
        print()
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print()
        print("Package installation path:")
        paths = site.getsitepackages()
        print(paths[0])
    else:
        print("Virtual Environment: None detected")
        print()
        print_construct_instructions()


if __name__ == "__main__":
    main()
