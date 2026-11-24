"""Display a map and its drone movements in a two-dimensional pygame view."""

import pygame

from models import DroneMap, Zone
from playback import Playback, Point


Color = tuple[int, int, int]


class PygameView:
    """Replay one simulation turn whenever the Right arrow key is pressed."""

    WIDTH = 900
    HEIGHT = 650
    BACKGROUND = (24, 30, 40)
    TEXT = (235, 240, 245)
    CONNECTION_COLOR = (120, 130, 145)
    DRONE_COLOR = (255, 220, 70)
    ZONE_COLORS = {
        "normal": (70, 150, 220),
        "priority": (70, 200, 140),
        "restricted": (235, 160, 55),
        "blocked": (100, 105, 115),
    }

    def __init__(self, drone_map: DroneMap, turns: list[list[str]]) -> None:
        """Prepare the replay and layout without opening a window.

        Args:
            drone_map: Map supplying zone coordinates, colors, and links.
            turns: Validated movement tokens grouped by simulation turn.

        Raises:
            ValueError: Coordinates overflow the display calculations.
        """
        self.drone_map = drone_map
        self.map_area = pygame.Rect(50, 80, 800, 500)
        self.screen: pygame.Surface
        self.font: pygame.font.Font
        self.small_font: pygame.font.Font
        self.drone_font: pygame.font.Font

        try:
            self.playback = Playback(drone_map, turns)
            self._fit_map()
        except OverflowError as error:
            message = "map coordinates are too large to display"
            raise ValueError(message) from error

    def _fit_map(self) -> None:
        """Set the scale, zone positions, and radius to fit the map area."""
        x_values = [float(zone.x) for zone in self.drone_map.zones.values()]
        y_values = [float(zone.y) for zone in self.drone_map.zones.values()]
        self.min_x = min(x_values)
        self.min_y = min(y_values)

        map_width = max(max(x_values) - self.min_x, 1.0)
        map_height = max(max(y_values) - self.min_y, 1.0)
        horizontal_scale = (self.map_area.width - 60) / map_width
        vertical_scale = (self.map_area.height - 60) / map_height
        self.scale = min(horizontal_scale, vertical_scale)

        self.zone_positions: dict[str, tuple[int, int]] = {}
        for name, zone in self.drone_map.zones.items():
            point = (float(zone.x), float(zone.y))
            self.zone_positions[name] = self._screen_position(point)
        self.zone_radius = self._find_zone_radius()

    def _find_zone_radius(self) -> int:
        """Return a circle radius based on the nearest distinct positions.

        Returns:
            An integer radius from 6 to 18 pixels, based on one third of
            the nearest nonzero zone spacing and clamped to those bounds.
        """
        positions = list(self.zone_positions.values())
        shortest_distance = 60.0

        for index, first in enumerate(positions):
            for second in positions[index + 1:]:
                x_distance = first[0] - second[0]
                y_distance = first[1] - second[1]
                distance = (x_distance ** 2 + y_distance ** 2) ** 0.5
                if 0 < distance < shortest_distance:
                    shortest_distance = distance

        return max(6, min(18, int(shortest_distance / 3)))

    def _screen_position(self, point: Point) -> tuple[int, int]:
        """Return pixel coordinates for a point in map coordinates.

        Args:
            point: Floating-point (x, y) pair in the original map coordinates.

        Returns:
            A rounded integer (x, y) pixel pair after scaling, offsetting,
            and reversing the vertical axis for screen coordinates.
        """
        x, y = point
        screen_x = self.map_area.left + 30 + (x - self.min_x) * self.scale
        screen_y = self.map_area.bottom - 30 - (y - self.min_y) * self.scale
        return (round(screen_x), round(screen_y))

    def run(self) -> None:
        """Open the window and process events until the user exits.

        Always shut down pygame on exit, including keyboard interruption.
        Raise ValueError when pygame reports a display error.
        """
        try:
            self._open_window()
            clock = pygame.time.Clock()
            running = True
            while running:
                for event in pygame.event.get():
                    running = self._handle_event(event)
                    if not running:
                        break

                if not running:
                    break

                self._draw_frame()
                pygame.display.flip()
                clock.tick(30)
        except KeyboardInterrupt:
            pass
        except pygame.error as error:
            raise ValueError(f"cannot open pygame display: {error}") from error
        finally:
            pygame.quit()

    def _open_window(self) -> None:
        """Initialize the pygame display and create the window and fonts."""
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Fly-in")
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        self.drone_font = pygame.font.Font(None, 15)

    def _handle_event(self, event: pygame.event.Event) -> bool:
        """Apply one input event and return whether playback should stay open.

        Right advances one turn; Escape and window-close events return False.

        Args:
            event: Pygame input event to process for replay or window control.

        Returns:
            False for a window-close event or an Escape key press; True for
            all other events, including when the replay has finished.
        """
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_RIGHT:
                self.playback.step()
        return True

    def _zone_color(self, zone: Zone) -> Color:
        """Return the zone's RGB color, falling back to its type's color.

        Args:
            zone: Zone whose optional color and zone type determine its fill.

        Returns:
            An (r, g, b) tuple from the zone's explicit color if pygame
            accepts it, or from its zone type if the color is absent or
            invalid.
        """
        if zone.color is not None:
            try:
                color = pygame.Color(zone.color)
                return (color.r, color.g, color.b)
            except ValueError:
                pass
        return self.ZONE_COLORS[zone.zone_type]

    def _draw_frame(self) -> None:
        """Draw the map, drones, and status onto the display surface."""
        self.screen.fill(self.BACKGROUND)
        self._draw_connections()
        self._draw_zones()
        self._draw_drones()
        self._draw_status()

    def _draw_connections(self) -> None:
        """Draw each connection as a line between its endpoints."""
        for connection in self.drone_map.connections.values():
            start = self.zone_positions[connection.first]
            end = self.zone_positions[connection.second]
            pygame.draw.line(self.screen, self.CONNECTION_COLOR, start, end, 3)

    def _draw_zones(self) -> None:
        """Draw colored zones, blocked markers, and start/end labels."""
        for name, zone in self.drone_map.zones.items():
            position = self.zone_positions[name]
            endpoints = {self.drone_map.start, self.drone_map.end}
            border_width = 3 if name in endpoints else 2
            pygame.draw.circle(
                self.screen, self._zone_color(zone),
                position, self.zone_radius,
            )
            pygame.draw.circle(
                self.screen, self.TEXT,
                position, self.zone_radius, border_width,
            )

            if zone.zone_type == "blocked":
                x, y = position
                cross = self.zone_radius // 2
                pygame.draw.line(
                    self.screen, self.TEXT,
                    (x - cross, y - cross),
                    (x + cross, y + cross), 2,
                )
                pygame.draw.line(
                    self.screen, self.TEXT,
                    (x - cross, y + cross),
                    (x + cross, y - cross), 2,
                )

            if name == self.drone_map.start:
                self._draw_zone_label("S", position)
            elif name == self.drone_map.end:
                self._draw_zone_label("E", position)

    def _draw_zone_label(
        self, text: str, position: tuple[int, int]
    ) -> None:
        """Draw a label below the zone at the supplied pixel position.

        Args:
            text: Label to render, such as S for start or E for end.
            position: Zone center as an (x, y) pair of screen pixels.
        """
        label = self.small_font.render(text, True, self.TEXT)
        label_position = label.get_rect(
            midtop=(position[0], position[1] + self.zone_radius + 5)
        )
        self.screen.blit(label, label_position)

    def _draw_drones(self) -> None:
        """Draw a drone ID or group count at each occupied screen position."""
        groups: dict[tuple[int, int], list[int]] = {}
        for drone_id, point in self.playback.positions.items():
            position = self._screen_position(point)
            groups.setdefault(position, []).append(drone_id)

        for position, drone_ids in groups.items():
            if len(drone_ids) == 1:
                text = f"D{drone_ids[0]}"
            else:
                text = f"x{len(drone_ids)}"

            shadow = self.drone_font.render(text, True, (0, 0, 0))
            label = self.drone_font.render(text, True, self.DRONE_COLOR)
            rectangle = label.get_rect(center=position)
            self.screen.blit(shadow, rectangle.move(1, 1))
            self.screen.blit(label, rectangle)

    def _draw_status(self) -> None:
        """Draw the current turn, completion state, and keyboard controls."""
        status = f"Turn {self.playback.turn} / {len(self.playback.turns)}"
        if self.playback.finished:
            status += "  Finished"
        status_image = self.font.render(status, True, self.TEXT)
        help_image = self.small_font.render(
            "Right: next turn    Esc: close", True, self.TEXT
        )
        self.screen.blit(status_image, (50, 25))
        self.screen.blit(help_image, (50, 610))
