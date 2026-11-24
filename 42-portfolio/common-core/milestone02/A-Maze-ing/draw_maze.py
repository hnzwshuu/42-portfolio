#!/usr/bin/env python3
from enum import Enum
import sys


class Directions(int, Enum):
    """Represent wall bit values for the four maze directions."""

    NORTH = 1,
    EAST = 2,
    SOUTH = 4,
    WEST = 8


class DrawMaze:
    """Render a maze map with colors in the terminal."""

    def __init__(self, maze_map: list[list[int]], start: tuple[int, int],
                 goal: tuple[int, int], sh_path: str) -> None:
        """Initialize drawing state.

        Args:
            maze_map: Two-dimensional maze map of wall bit values.
            start: Entry coordinate as (x, y).
            goal: Exit coordinate as (x, y).
            sh_path: Shortest path encoded with N, E, S, and W.
        """
        self._maze_map: list[list[int]] = maze_map
        self._start: tuple[int, int] = start
        self._goal: tuple[int, int] = goal
        self._sh_path: str = sh_path
        self._pixel: str = "  "
        self._clr_dict: dict[str, str] = \
            {
                "white": "\x1b[48;2;255;255;255m",
                "red": "\x1b[48;2;255;0;0m",
                "green": "\x1b[48;2;0;255;0m",
                "blue": "\x1b[48;2;0;0;255m",
                "start": "\x1b[48;2;252;15;192m",
                "goal": "\x1b[48;2;252;194;15m",
                "normal": "\x1b[48;2;0;0;0m",
                "shortest": "\x1b[48;2;255;144;102m",
                "white_pat": "\x1b[48;2;205;205;205m",
                "red_pat": "\x1b[48;2;205;0;0m",
                "green_pat": "\x1b[48;2;0;205;0m",
                "blue_pat": "\x1b[48;2;0;0;205m",
                "default": "\x1b[0m"
             }
        self._clr_set: str = "white"
        self._is_show: bool = True
        return

    def set_maze_map(self, maze_map: list[list[int]]) -> None:
        """Replace the maze map used for drawing.

        Args:
            maze_map: New two-dimensional maze map.
        """
        self._maze_map = maze_map
        return

    def set_sh_path(self, sh_path: str) -> None:
        """Replace the shortest path used for drawing.

        Args:
            sh_path: Shortest path encoded with N, E, S, and W.
        """
        self._sh_path = sh_path
        return

    def set_clr(self) -> None:
        """Rotate the wall color setting."""
        if self._clr_set == "white":
            self._clr_set = "red"
        elif self._clr_set == "red":
            self._clr_set = "blue"
        elif self._clr_set == "blue":
            self._clr_set = "green"
        elif self._clr_set == "green":
            self._clr_set = "white"
        return

    def set_is_show(self) -> None:
        """Toggle whether the shortest path is shown."""
        if self._is_show is True:
            self._is_show = False
        else:
            self._is_show = True
        return

    def regis_sh(self) -> None:
        """Mark shortest-path cells by adding 16 to their map values.

        Raises:
            ValueError: If the shortest path contains an invalid direction.
            Exception: If the path does not reach the goal.
        """
        x: int = self._start[0]
        y: int = self._start[1]
        self._maze_map[y][x] += 16
        for direc in self._sh_path:
            if direc == "E":
                x += 1
            elif direc == "W":
                x -= 1
            elif direc == "S":
                y += 1
            elif direc == "N":
                y -= 1
            else:
                raise \
                    ValueError("detect error in sh_path"
                               "correct directions are 'E', 'W', 'S' and 'N'")
            self._maze_map[y][x] += 16
        if self._maze_map[self._goal[1]][self._goal[0]] >= 16:
            return
        else:
            raise Exception("No Goal !!!")

    def draw_pixel(self, clr_name: str) -> None:
        """Print one colored terminal pixel.

        Args:
            clr_name: Key name in the color dictionary.
        """
        print(self._clr_dict[clr_name], self._pixel, sep="", end="")
        print(self._clr_dict["default"], sep="", end="")
        return

    def slct_clr_path(self, coord: tuple[int, int], direc: int) -> None:
        """Choose and draw the color for a wall or passage between cells.

        Args:
            coord: Coordinate of the current cell as (x, y).
            direc: Direction bit for the wall or passage to draw.
        """
        x: int
        y: int
        x, y = coord
        if self._maze_map[y][x] & direc:
            self.draw_pixel(self._clr_set)
        else:
            if self._is_show is False or self._maze_map[y][x] < 16:
                self.draw_pixel("normal")
            elif direc == Directions.NORTH and self._maze_map[y-1][x] >= 16:
                self.draw_pixel("shortest")
            elif direc == Directions.EAST and self._maze_map[y][x+1] >= 16:
                self.draw_pixel("shortest")
            elif direc == Directions.SOUTH and self._maze_map[y+1][x] >= 16:
                self.draw_pixel("shortest")
            elif direc == Directions.WEST and self._maze_map[y][x-1] >= 16:
                self.draw_pixel("shortest")
            else:
                self.draw_pixel("normal")
        return

    def slct_clr_coord(self, coord: tuple[int, int]) -> None:
        """Choose and draw the color for one cell.

        Args:
            coord: Coordinate of the cell as (x, y).
        """
        x: int
        y: int
        x, y = coord
        if x == self._start[0] and y == self._start[1]:
            self.draw_pixel("start")
        elif x == self._goal[0] and y == self._goal[1]:
            self.draw_pixel("goal")
        elif self._is_show is True and self._maze_map[y][x] >= 16:
            self.draw_pixel("shortest")
        elif self._maze_map[y][x] % 16 == 15:
            self.draw_pixel(f"{self._clr_set}_pat")
        else:
            self.draw_pixel("normal")
        return

    def slct_clr_vert(self, y: int, direc: int) -> None:
        """Draw one horizontal wall separator row.

        Args:
            y: Maze row index to draw.
            direc: Direction bit used for the horizontal wall check.
        """
        for x in range(len(self._maze_map[y])):
            self.draw_pixel(self._clr_set)
            self.slct_clr_path((x, y), direc)
        self.draw_pixel(self._clr_set)
        print()
        return

    def slct_clr_horiz(self, y: int) -> None:
        """Draw one cell row with west and east wall checks.

        Args:
            y: Maze row index to draw.
        """
        for x in range(len(self._maze_map[y])):
            self.slct_clr_path((x, y), Directions.WEST)
            self.slct_clr_coord((x, y))
        self.slct_clr_path((x, y), Directions.EAST)
        print()
        return

    def slct_clr_maze(self) -> None:
        """Draw the whole maze."""
        if self._is_show is True:
            try:
                self.regis_sh()
            except Exception as ex:
                print(f"Rendering Error {ex}")
                sys.exit(0)
        for y in range(len(self._maze_map)):
            self.slct_clr_vert(y, Directions.NORTH)
            self.slct_clr_horiz(y)
        self.slct_clr_vert(len(self._maze_map) - 1, Directions.SOUTH)
        return
