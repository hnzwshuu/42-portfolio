"""Load a map, plan drone movements, and display the simulation."""

import argparse
import os
import sys

from models import DroneMap
from parser import MapParseError, MapParser
from pathfinder import PathFinder
from simulator import SimulationError, Simulator


class TerminalView:
    """Print simulation turns with optional destination-based colors."""

    ANSI_COLORS: dict[str, int] = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "gray": 90,
        "grey": 90,
    }

    def __init__(self, use_color: bool) -> None:
        """Enable ANSI coloring when use_color is True.

        Args:
            use_color: Whether movement tokens should include ANSI colors.
        """
        self.use_color = use_color

    def display(
        self, turns: list[list[str]], zone_colors: dict[str, str | None]
    ) -> None:
        """Print each turn as a line of space-separated movement tokens.

        Args:
            turns: Movement tokens grouped by simulation turn.
            zone_colors: Optional color names indexed by zone name.
        """
        for movements in turns:
            rendered: list[str] = []
            for movement in movements:
                rendered.append(self._color_movement(movement, zone_colors))
            print(" ".join(rendered))

    def _color_movement(
        self, movement: str, zone_colors: dict[str, str | None]
    ) -> str:
        """Return a token colored by its destination, if coloring is enabled.

        Unrecognized color names receive a deterministic terminal color.
        Tokens with no destination color are returned unchanged.

        Args:
            movement: Validated arrival or transit token for one drone.
            zone_colors: Optional color names indexed by destination zone.

        Returns:
            The movement token wrapped in ANSI color and reset sequences,
            or the original token if coloring is disabled or no color is set.
        """
        if not self.use_color:
            return movement
        destination = movement.rsplit("-", 1)[1]
        color = zone_colors.get(destination)
        if color is None:
            return movement
        normalized = color.lower()
        if normalized in self.ANSI_COLORS:
            prefix = f"\033[{self.ANSI_COLORS[normalized]}m"
        else:
            character_total = 0
            for character in normalized:
                character_total += ord(character)
            color_number = 16 + character_total % 216
            prefix = f"\033[38;5;{color_number}m"
        return f"{prefix}{movement}\033[0m"


class FlyInApplication:
    """Coordinate parsing, route planning, simulation, and presentation."""

    def run(self, filename: str, use_color: bool, gui: bool = False) -> None:
        """Simulate a map file and display its validated movements.

        Args:
            filename: Path to a UTF-8 map file.
            use_color: Whether terminal tokens use ANSI colors.
            gui: Whether to open the GUI instead of printing turns.

        Raises:
            MapParseError: The map cannot be read or parsed.
            SimulationError: The planned movements violate map rules.
            ValueError: No route exists or the GUI cannot be initialized.
        """
        drone_map = MapParser().parse_file(filename)

        finder = PathFinder(drone_map)
        paths = finder.create_paths()

        simulator = Simulator(drone_map, paths, finder.departures)
        turns = simulator.run()

        if gui:
            self._show_gui(drone_map, turns)
            return

        colors = {}
        for name, zone in drone_map.zones.items():
            colors[name] = zone.color
        view = TerminalView(use_color)
        view.display(turns, colors)

    def _show_gui(self, drone_map: DroneMap, turns: list[list[str]]) -> None:
        """Import pygame on demand and replay validated turns in a window.

        Args:
            drone_map: Map supplying zone coordinates, colors, and links.
            turns: Validated movement tokens grouped in chronological order.
        """
        os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
        try:
            from pygame_view import PygameView
        except ModuleNotFoundError as error:
            if error.name != "pygame":
                raise
            raise ValueError(
                "pygame is not installed; run: "
                "python3 -m pip install -r requirements.txt"
            ) from error
        view = PygameView(drone_map, turns)
        view.run()


def parse_arguments() -> argparse.Namespace:
    """Return command-line options for the map file, colors, and GUI.

    argparse exits on a help request or invalid arguments.

    Returns:
        An argparse.Namespace containing map_file as a path string and
        color and gui as booleans indicating whether each flag was supplied.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("map_file")
    parser.add_argument("--color", action="store_true")
    parser.add_argument("--gui", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Run the CLI and report handled errors on standard error.

    Returns:
        Zero on success or a closed output pipe; one on handled input,
        planning, simulation, or display errors. Argument parsing may exit
        before this function returns.
    """
    try:
        try:
            arguments = parse_arguments()
            FlyInApplication().run(
                arguments.map_file, arguments.color, arguments.gui
            )
        finally:
            sys.stdout.flush()
    except BrokenPipeError:
        with open(os.devnull, "w") as null_output:
            os.dup2(null_output.fileno(), sys.stdout.fileno())
        return 0
    except (MapParseError, SimulationError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
