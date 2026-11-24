def secure_archive(
    filename: str,
    action: str = "read",
    content: str = ""
) -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename) as file:
                return (True, file.read())
        if action == "write":
            with open(filename, 'w') as file:
                file.write(content)
            return (True, "Content successfully written to file")
        return (False, "Unknown archive action")
    except OSError as e:
        return (False, str(e))


def main() -> None:
    print("=== Cyber Archives Security ===")
    print()
    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/non/existing/file"))
    print()
    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))
    print()
    print("Using 'secure_archive' to read from a regular file:")
    success, data = secure_archive("ancient_fragment.txt")
    print((success, data))
    print()
    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("secure_fragment.txt", "write", data))


if __name__ == "__main__":
    main()
