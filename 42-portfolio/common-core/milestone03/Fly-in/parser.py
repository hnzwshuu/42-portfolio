"""Parse map text and validate its format and references."""

from pathlib import Path
from typing import NoReturn

from models import Connection, DroneMap, Zone


class MapParseError(ValueError):
    """Report invalid map input, including a line number when available."""


class MapParser:
    """Convert validated map text into a DroneMap object."""

    ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}
    ZONE_PREFIXES = {"start_hub", "end_hub", "hub"}

    def parse_file(self, filename: str) -> DroneMap:
        """Read and parse a UTF-8 map file.

        Args:
            filename: Path to the map file.

        Returns:
            A validated map with its neighbour lists populated.

        Raises:
            MapParseError: If the file cannot be read or its input is invalid.
        """
        try:
            with Path(filename).open("r", encoding="utf-8") as map_file:
                lines = map_file.readlines()
        except OSError as error:
            message = f"cannot read '{filename}': {error}"
            raise MapParseError(message) from error
        except UnicodeError as error:
            message = f"cannot read '{filename}': expected UTF-8 text"
            raise MapParseError(message) from error
        return self.parse_lines(lines)

    def parse_lines(self, lines: list[str]) -> DroneMap:
        """Validate map definitions and build their graph.

        Zone names and coordinate pairs must be unique across all zones,
        including the start and end.

        Args:
            lines: Map text split into lines, including any comments.

        Returns:
            A map containing the drone count, zones, and connections.

        Raises:
            MapParseError: If a definition or reference is invalid.
        """
        useful_lines = self._remove_comments(lines)
        if not useful_lines:
            raise MapParseError("line 1: empty input")

        first_number, first_line = useful_lines[0]
        drone_count = self._parse_drone_count(first_number, first_line)
        zones: dict[str, Zone] = {}
        coordinates: dict[tuple[int, int], str] = {}
        connections: dict[str, Connection] = {}
        start: str | None = None
        end: str | None = None

        for line_number, line in useful_lines[1:]:
            prefix, separator, body = line.partition(":")
            if not separator:
                self._error(line_number, "expected '<type>: <value>'")
            prefix = prefix.strip()
            body = body.strip()
            if prefix in self.ZONE_PREFIXES:
                zone = self._parse_zone(line_number, body, prefix)
                if zone.name in zones:
                    self._error(line_number, f"duplicate zone '{zone.name}'")
                position = (zone.x, zone.y)
                if position in coordinates:
                    message = (
                        f"duplicate coordinates {position}: "
                        f"zone '{zone.name}' overlaps "
                        f"zone '{coordinates[position]}'"
                    )
                    self._error(line_number, message)
                zones[zone.name] = zone
                coordinates[position] = zone.name
                if prefix == "start_hub":
                    if start is not None:
                        self._error(line_number, "more than one start_hub")
                    start = zone.name
                elif prefix == "end_hub":
                    if end is not None:
                        self._error(line_number, "more than one end_hub")
                    end = zone.name
            elif prefix == "connection":
                connection = self._parse_connection(line_number, body, zones)
                if connection.key in connections:
                    self._error(line_number, "duplicate connection")
                connections[connection.key] = connection
            else:
                self._error(line_number, f"unknown line type '{prefix}'")

        if start is None:
            self._error(len(lines) + 1, "missing start_hub at end of input")
        if end is None:
            self._error(len(lines) + 1, "missing end_hub at end of input")
        result = DroneMap(drone_count, zones, connections, start, end)
        result.build_neighbours()
        return result

    def _remove_comments(self, lines: list[str]) -> list[tuple[int, str]]:
        """Return nonempty, comment-free lines with original line numbers.

        Args:
            lines: Original input lines, including blank lines and comments.

        Returns:
            A list of (line_number, text) pairs in input order, with one-based
            original line numbers and stripped, nonempty, comment-free text.
        """
        useful_lines: list[tuple[int, str]] = []
        for number, original_line in enumerate(lines, start=1):
            line = original_line.split("#", 1)[0].strip()
            if line:
                useful_lines.append((number, line))
        return useful_lines

    def _parse_drone_count(self, line_number: int, line: str) -> int:
        """Read a positive drone count from the first meaningful line.

        Args:
            line_number: One-based original line number for error reporting.
            line: Stripped, comment-free nb_drones declaration.

        Returns:
            The strictly positive integer declared by nb_drones.
        """
        prefix, separator, number_text = line.partition(":")
        number_text = number_text.strip()
        if (
            prefix != "nb_drones"
            or not separator
            or not self._is_decimal(number_text)
        ):
            self._error(
                line_number,
                "first line must be 'nb_drones: <number>'",
            )
        try:
            count = int(number_text)
        except ValueError:
            self._error(line_number, "number of drones is too large to parse")
        if count <= 0:
            self._error(line_number, "number of drones must be positive")
        return count

    def _split_metadata(
        self, line_number: int, body: str
    ) -> tuple[str, dict[str, str]]:
        """Return the definition body and validated metadata pairs.

        Args:
            line_number: One-based original line number for error reporting.
            body: Stripped text after the definition's colon, optionally
                ending with a bracketed metadata block.

        Returns:
            A (body, metadata) tuple containing the stripped definition text
            without its metadata block and a dictionary of string keys and
            values. The dictionary is empty when no metadata block is given.
        """
        if "[" not in body and "]" not in body:
            return body.strip(), {}
        if body.count("[") != 1 or body.count("]") != 1:
            self._error(line_number, "invalid metadata brackets")
        if not body.endswith("]"):
            self._error(line_number, "invalid metadata brackets")
        main_part, metadata_text = body[:-1].split("[", 1)
        if not metadata_text.strip():
            self._error(line_number, "metadata block cannot be empty")
        metadata: dict[str, str] = {}
        for item in metadata_text.split():
            if item.count("=") != 1:
                self._error(line_number, f"invalid metadata item '{item}'")
            key, value = item.split("=")
            if not key or not value:
                self._error(line_number, f"invalid metadata item '{item}'")
            if key in metadata:
                self._error(line_number, f"duplicate metadata key '{key}'")
            metadata[key] = value
        return main_part.strip(), metadata

    def _parse_zone(self, line_number: int, body: str, prefix: str) -> Zone:
        """Parse a zone's name, coordinates, type, color, and capacity.

        Args:
            line_number: One-based original line number for error reporting.
            body: Zone name, coordinates, and optional metadata after the
                declaration's colon, without the zone prefix.
            prefix: Declaration type: hub, start_hub, or end_hub. The latter
                two cause max_drones metadata to be ignored.

        Returns:
            A Zone object containing the parsed name, integer coordinates,
            zone type, optional color, and capacity after applying defaults.
        """
        main_part, metadata = self._split_metadata(line_number, body)
        parts = main_part.split()
        if len(parts) != 3:
            self._error(line_number, "zone needs a name and two coordinates")
        name, x_text, y_text = parts
        if "-" in name:
            self._error(line_number, "zone names cannot contain dashes")
        x = self._parse_coordinate(line_number, x_text)
        y = self._parse_coordinate(line_number, y_text)

        allowed = {"zone", "color", "max_drones"}
        self._check_metadata_keys(line_number, metadata, allowed)
        zone_type = metadata.get("zone", "normal")
        if zone_type not in self.ZONE_TYPES:
            self._error(line_number, f"invalid zone type '{zone_type}'")
        if prefix in {"start_hub", "end_hub"}:
            max_drones = 1
        else:
            max_drones = self._positive_metadata(
                line_number, metadata, "max_drones", 1
            )
        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=metadata.get("color"),
            max_drones=max_drones,
        )

    def _parse_connection(
        self, line_number: int, body: str, zones: dict[str, Zone]
    ) -> Connection:
        """Parse a connection and require both endpoint zones to exist.

        Args:
            line_number: One-based original line number for error reporting.
            body: Dash-separated endpoint names and optional metadata after
                the connection declaration's colon.
            zones: Previously defined Zone objects indexed by zone name,
                used to check that both endpoints exist.

        Returns:
            A Connection object joining two distinct, existing zones with
            the parsed positive link capacity, defaulting to 1 if omitted.
        """
        main_part, metadata = self._split_metadata(line_number, body)
        if main_part.count("-") != 1:
            self._error(
                line_number,
                "connection must have the form 'zone1-zone2'",
            )
        first, second = main_part.split("-")
        if not first or not second:
            self._error(
                line_number,
                "connection contains an empty zone name",
            )
        if first == second:
            self._error(line_number, "a zone cannot connect to itself")
        if first not in zones or second not in zones:
            self._error(line_number, "connection uses an undefined zone")
        self._check_metadata_keys(
            line_number, metadata, {"max_link_capacity"}
        )
        capacity = self._positive_metadata(
            line_number, metadata, "max_link_capacity", 1
        )
        return Connection(first, second, capacity)

    def _is_decimal(self, text: str) -> bool:
        """Return whether text is nonempty and contains only ASCII digits.

        Args:
            text: Unmodified numeric token to check, without stripping it
                or accepting a leading sign.

        Returns:
            True if text contains one or more ASCII digits and nothing else;
            False if it is empty or contains any other character.
        """
        if not text:
            return False
        for character in text:
            if character not in "0123456789":
                return False
        return True

    def _parse_coordinate(self, line_number: int, text: str) -> int:
        """Parse an integer coordinate with at most one leading sign.

        Args:
            line_number: One-based original line number for error reporting.
            text: Coordinate token containing ASCII digits and optionally
                one leading plus or minus sign.

        Returns:
            The integer coordinate represented by text, preserving its sign.
        """
        digits = text
        if digits.startswith("+") or digits.startswith("-"):
            digits = digits[1:]
        if not self._is_decimal(digits):
            self._error(line_number, "zone coordinates must be integers")
        try:
            return int(text)
        except ValueError:
            self._error(line_number, "zone coordinates must be integers")

    def _positive_metadata(
        self,
        line_number: int,
        metadata: dict[str, str],
        key: str,
        default: int,
    ) -> int:
        """Read positive integer metadata, or return the supplied default.

        Args:
            line_number: One-based original line number for error reporting.
            metadata: Parsed metadata keys mapped to their string values.
            key: Metadata field whose value must be a positive integer.
            default: Value returned without validation when key is absent.

        Returns:
            The strictly positive integer parsed from metadata[key], or
            default unchanged when key is absent.
        """
        if key not in metadata:
            return default
        if not self._is_decimal(metadata[key]):
            self._error(line_number, f"{key} must be a positive integer")
        try:
            value = int(metadata[key])
        except ValueError:
            self._error(line_number, f"{key} must be a positive integer")
        if value <= 0:
            self._error(line_number, f"{key} must be a positive integer")
        return value

    def _check_metadata_keys(
        self,
        line_number: int,
        metadata: dict[str, str],
        allowed: set[str],
    ) -> None:
        """Reject metadata keys outside the allowed set for this definition.

        Args:
            line_number: One-based original line number for error reporting.
            metadata: Parsed metadata dictionary whose keys are checked.
            allowed: Set of metadata keys accepted for this declaration type.
        """
        for key in metadata:
            if key not in allowed:
                self._error(line_number, f"unknown metadata key '{key}'")

    def _error(self, line_number: int, message: str) -> NoReturn:
        """Stop parsing by raising MapParseError with a line number.

        Args:
            line_number: One-based input line number to include in the error.
            message: Description of the error, without a line-number prefix.
        """
        raise MapParseError(f"line {line_number}: {message}")
