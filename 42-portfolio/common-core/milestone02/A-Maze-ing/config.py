from typing import Any


class Config():
    """Store and validate maze settings loaded from a config file."""

    def __init__(self, cmpnts: list[str]) -> None:
        """Initialize a Config object from raw config file lines.

        Args:
            cmpnts: Lines read from the configuration file.

        Raises:
            ValueError: If a line has invalid syntax or an unknown key.
        """
        for line_no, cmpnt in enumerate(cmpnts, start=1):
            try:
                inp: tuple[str, Any] = self.pickup(cmpnt)
            except ValueError as ex:
                raise ValueError(f"line {line_no}: {ex}")
            if inp[0]:
                if inp[0] == "width":
                    self._width: int = inp[1]
                elif inp[0] == "height":
                    self._height: int = inp[1]
                elif inp[0] == "entry":
                    self._entry: tuple[int, int] = inp[1]
                elif inp[0] == "exit":
                    self._exit: tuple[int, int] = inp[1]
                elif inp[0] == "output_file":
                    self._output_file: str = inp[1]
                elif inp[0] == "perfect":
                    self._perfect: bool = inp[1]
                else:
                    raise ValueError(f"line {line_no}: unknown key '{inp[0]}'")
        return

    def pickup(self, cmpnt: str) -> tuple[str, Any]:
        """Parse one configuration line into a key and typed value.

        Args:
            cmpnt: One raw line from the configuration file.

        Returns:
            A tuple containing the normalized key and parsed value.

        Raises:
            ValueError: If the line has an invalid format or value.
        """
        cmpnt = cmpnt.strip()
        if not cmpnt or cmpnt.startswith("#"):
            return ("", "")
        try:
            key, value = cmpnt.split("=", 1)
            key = key.strip()
            value = value.strip()
        except ValueError:
            raise ValueError("configuration line must be KEY=VALUE")
        if not key:
            raise ValueError("configuration key is empty")
        if not value:
            raise ValueError(f"{key} value is empty")
        key = key.lower()
        if key == "width" or key == "height":
            try:
                return (key, int(value))
            except ValueError:
                raise ValueError(f"{key} must be an integer")
        elif key == "entry" or key == "exit":
            try:
                x, y = value.split(",", 1)
                return (key, (int(x), int(y)))
            except ValueError:
                raise ValueError(f"{key} must be coordinates in x,y format")
        elif key == "output_file":
            if not value.endswith(".txt"):
                raise Exception(f"{key}'s name must end with '.txt'")
            return (key, value)
        elif key == "perfect":
            if value == "True":
                return (key, True)
            elif value == "False":
                return (key, False)
            else:
                raise ValueError("perfect must be True or False")
        return (key, value)

    def check(self) -> None:
        """Validate required config fields and coordinate constraints.

        Raises:
            ValueError: If a required key is missing or a value is invalid.
        """
        required_keys: list[str] = [
            "_width", "_height", "_entry", "_exit",
            "_output_file", "_perfect",
        ]
        for key in required_keys:
            if not hasattr(self, key):
                raise ValueError(f"{key[1:].upper()} is required")
        if self._width <= 0:
            raise ValueError("width must be more than zero")
        if self._height <= 0:
            raise ValueError("height must be more than zero")
        x_entry, y_entry = self._entry
        if not (0 <= x_entry < self._width and 0 <= y_entry < self._height):
            raise ValueError("entry must be inside maze")
        x_exit, y_exit = self._exit
        if not (0 <= x_exit < self._width and 0 <= y_exit < self._height):
            raise ValueError("exit must be inside maze")
        if self._entry == self._exit:
            raise ValueError("entry and exit must be different")
        self._output_file
        self._perfect
        return
