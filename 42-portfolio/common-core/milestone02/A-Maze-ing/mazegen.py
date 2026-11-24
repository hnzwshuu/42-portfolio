#!/usr/bin/env python3
"""Reusable maze generator module for the A-Maze-ing project.

Basic example:
    from mazegen import MazeGenerator

    generator = MazeGenerator(width=20, height=15, seed=42, perfect=True)
    generator.generate()

    maze = generator.get_map()
    solution = generator.get_solution()

Custom parameters:
    width and height set the maze size.
    entry and exit set the start and goal coordinates.
    seed makes generation reproducible.
    perfect chooses whether the maze keeps exactly one route.

Accessing generated data:
    get_map() returns the generated wall-bit structure as map[y][x].
    get_solution() returns one shortest path using N, E, S and W.
"""

from collections import deque
from enum import Enum
import random
import sys
X = 0
Y = 1


class Directions(int, Enum):
    """Represent wall bit values for the four maze directions."""

    NORTH = 1,
    EAST = 2,
    SOUTH = 4,
    WEST = 8


class MazeGenerator:
    """Generate a maze and calculate its shortest path."""

    def __init__(self, width: int, height: int,
                 entry: tuple[int, int] = (0, 0),
                 exit: tuple[int, int] | None = None,
                 perfect: bool = False,
                 seed: int | None = None) -> None:
        """Initialize maze state.

        Args:
            width: Maze width.
            height: Maze height.
            entry: Entry coordinate as (x, y).
            exit: Exit coordinate as (x, y). Defaults to the bottom-right cell.
            perfect: Whether to keep the maze perfect.
            seed: Optional random seed for reproducible generation.
        """
        area: tuple[int, int] = (width, height)
        if exit is None:
            goal: tuple[int, int] = (width - 1, height - 1)
        else:
            goal = exit
        self._area: tuple[int, int] = area
        self._map: list[list[int]] = [[15] * area[X] for i in range(area[Y])]
        self._center: tuple[int, int] = self._detect_center_coord()
        self._start: tuple[int, int] = entry
        self._goal: tuple[int, int] = goal
        self._sh_path: str = ""
        self._is_perfect: bool = perfect
        self._seed: int | None = seed
        self._is_pattern: bool = self._check_patten()
        self._is_finish: bool = False
        return

    def generate(self) -> list[list[int]]:
        """Generate a new maze and return its wall-bit structure."""
        self.generate_maze()
        return self.get_map()

    def show(self) -> None:
        """Print the numeric maze map for debugging."""
        for line in self._map:
            for pixel in line:
                if pixel < 10:
                    print("0", end="")
                    print(pixel, end="")
                else:
                    print(pixel, end="")
                print(" ", end="")
            print()

    def get_map(self) -> list[list[int]]:
        """Return the current maze map.

        Returns:
            A two-dimensional list of wall bit values.
        """
        return self._map

    def get_sh_path(self) -> str:
        """Return the shortest path from entry to exit.

        Returns:
            A string made from N, E, S, and W directions.
        """
        return self._sh_path

    def get_solution(self) -> str:
        """Return one shortest path from entry to exit."""
        return self.get_sh_path()

    def show_pattern_message(self) -> None:
        """Print a message if 42 pattern is not present."""
        if self._is_pattern is False:
            print("With this setting, the 42 patterns will not be displayed.")
        return

    def set_seed(self, new: int) -> None:
        """Set the random seed used for the next generation.

        Args:
            new: Seed value passed to the random module.
        """
        self._seed = new
        return

    def _reset_map(self) -> None:
        """Reset every cell to the fully closed wall value."""
        for y in range(self._area[Y]):
            for x in range(self._area[X]):
                self._map[y][x] = 15
        return

    def _detect_seed(self) -> None:
        """Apply the configured random seed when one exists."""
        if self._seed is not None:
            random.seed(self._seed)
        return

    def _detect_center_coord(self) -> tuple[int, int]:
        """Calculate the center coordinate used for the 42 pattern.

        Returns:
            The center coordinate as (x, y).
        """
        if self._area[X] % 2 == 0 and self._area[Y] % 2 == 0:
            return ((self._area[X] - 1) // 2, (self._area[Y] - 1) // 2)
        elif self._area[X] % 2 == 1 and self._area[Y] % 2 == 0:
            return (self._area[X] // 2, (self._area[Y] - 1) // 2)
        elif self._area[X] % 2 == 0 and self._area[Y] % 2 == 1:
            return ((self._area[X] - 1) // 2, self._area[Y] // 2)
        return (self._area[X] // 2, self._area[Y] // 2)

    def _check_patten(self) -> bool:
        """Check whether the 42 pattern fits inside the maze border.

        Returns:
            True if all pattern cells are inside the drawable area.
        """
        pattern: list[tuple[int, int]] = [
            (self._center[X]-3, self._center[Y]-2),
            (self._center[X]-3, self._center[Y]-1),
            (self._center[X]-3, self._center[Y]),
            (self._center[X]-2, self._center[Y]),
            (self._center[X]-1, self._center[Y]),
            (self._center[X]-1, self._center[Y]+1),
            (self._center[X]-1, self._center[Y]+2),
            (self._center[X]+1, self._center[Y]-2),
            (self._center[X]+2, self._center[Y]-2),
            (self._center[X]+3, self._center[Y]-2),
            (self._center[X]+3, self._center[Y]-1),
            (self._center[X]+3, self._center[Y]),
            (self._center[X]+2, self._center[Y]),
            (self._center[X]+1, self._center[Y]),
            (self._center[X]+1, self._center[Y]+1),
            (self._center[X]+1, self._center[Y]+2),
            (self._center[X]+2, self._center[Y]+2),
            (self._center[X]+3, self._center[Y]+2),
        ]
        for i in pattern:
            if i[X] <= 0 or i[X] >= self._area[X] - 1:
                return False
            if i[Y] <= 0 or i[Y] >= self._area[Y] - 1:
                return False
            if i == self._start or i == self._goal:
                return False
        return True

    def _mark_pattern(self, batch_value: int) -> None:
        """Write a temporary or final value into the 42 pattern cells.

        Args:
            batch_value: Cell value to assign to each pattern coordinate.
        """
        pattern: list[tuple[int, int]] = [
            (self._center[X]-3, self._center[Y]-2),
            (self._center[X]-3, self._center[Y]-1),
            (self._center[X]-3, self._center[Y]),
            (self._center[X]-2, self._center[Y]),
            (self._center[X]-1, self._center[Y]),
            (self._center[X]-1, self._center[Y]+1),
            (self._center[X]-1, self._center[Y]+2),
            (self._center[X]+1, self._center[Y]-2),
            (self._center[X]+2, self._center[Y]-2),
            (self._center[X]+3, self._center[Y]-2),
            (self._center[X]+3, self._center[Y]-1),
            (self._center[X]+3, self._center[Y]),
            (self._center[X]+2, self._center[Y]),
            (self._center[X]+1, self._center[Y]),
            (self._center[X]+1, self._center[Y]+1),
            (self._center[X]+1, self._center[Y]+2),
            (self._center[X]+2, self._center[Y]+2),
            (self._center[X]+3, self._center[Y]+2),
        ]
        for i in pattern:
            self._map[i[Y]][i[X]] = batch_value
        return

    def generate_maze(self) -> None:
        """Generate a new maze and store its shortest path.

        Raises:
            RuntimeError: If no valid path from entry to exit can be found.
        """
        sys.setrecursionlimit(self._area[X] * self._area[Y] + 100)
        self._reset_map()
        self._detect_seed()
        if self._is_pattern is True:
            self._mark_pattern(31)
        self._generate_maze_recursive((0, 0))
        if self._is_pattern is True:
            self._mark_pattern(15)
        if self._is_perfect is False:
            self._convert_into_incomplete()
        try:
            self._sh_path = self._solve_sh_path()
        except Exception as ex:
            raise RuntimeError(str(ex)) from ex
        return

    def _is_wall_outside(self, curr_coord: tuple[int, int],
                         direc: int) -> bool:
        """Check whether moving in a direction stays inside the maze.

        Args:
            curr_coord: Current coordinate as (x, y).
            direc: Direction bit to test.

        Returns:
            True if the direction does not leave the maze.
        """
        if direc == Directions.NORTH\
                and curr_coord[Y] == 0:
            return False
        elif direc == Directions.EAST\
                and curr_coord[X] == self._area[X] - 1:
            return False
        elif direc == Directions.SOUTH\
                and curr_coord[Y] == self._area[Y] - 1:
            return False
        elif direc == Directions.WEST\
                and curr_coord[X] == 0:
            return False
        return True

    def _is_wall_inside(self, curr_coord: tuple[int, int],
                        direc: int) -> bool:
        """Check whether the neighbor in a direction is unvisited.

        Args:
            curr_coord: Current coordinate as (x, y).
            direc: Direction bit to test.

        Returns:
            True if the neighbor is still fully closed.
        """
        if direc == Directions.NORTH\
                and self._map[curr_coord[Y]-1][curr_coord[X]] == 15:
            return True
        elif direc == Directions.EAST\
                and self._map[curr_coord[Y]][curr_coord[X]+1] == 15:
            return True
        elif direc == Directions.SOUTH\
                and self._map[curr_coord[Y]+1][curr_coord[X]] == 15:
            return True
        elif direc == Directions.WEST\
                and self._map[curr_coord[Y]][curr_coord[X]-1] == 15:
            return True
        else:
            return False

    def _is_wall(self, curr_coord: tuple[int, int], direc: int) -> bool:
        """Check whether a direction can be carved from the current cell.

        Args:
            curr_coord: Current coordinate as (x, y).
            direc: Direction bit to test.

        Returns:
            True if the move is inside the maze and reaches an unvisited cell.
        """
        if curr_coord[X] == 0 or curr_coord[X] == self._area[X] - 1\
                or curr_coord[Y] == 0 or curr_coord[Y] == self._area[Y] - 1:
            if not self._is_wall_outside(curr_coord, direc):
                return False
        return self._is_wall_inside(curr_coord, direc)

    def _move_next_coord_coord(self, curr_coord: tuple[int, int],
                               direc: int) -> tuple[int, int]:
        """Calculate the neighboring coordinate in one direction.

        Args:
            curr_coord: Current coordinate as (x, y).
            direc: Direction bit to move toward.

        Returns:
            The next coordinate as (x, y).
        """
        if direc == Directions.NORTH:
            return (curr_coord[X], curr_coord[Y]-1)
        elif direc == Directions.EAST:
            return (curr_coord[X]+1, curr_coord[Y])
        elif direc == Directions.SOUTH:
            return (curr_coord[X], curr_coord[Y]+1)
        else:
            return (curr_coord[X]-1, curr_coord[Y])

    def _break_wall(self, curr_coord: tuple[int, int],
                    next_coord: tuple[int, int], direc: int) -> None:
        """Remove the wall between two adjacent cells.

        Args:
            curr_coord: Current coordinate as (x, y).
            next_coord: Neighbor coordinate as (x, y).
            direc: Direction bit from current cell to neighbor.
        """
        self._map[curr_coord[Y]][curr_coord[X]] &= ~direc
        if direc == Directions.NORTH:
            self._map[next_coord[Y]][next_coord[X]] &= ~Directions.SOUTH
        elif direc == Directions.EAST:
            self._map[next_coord[Y]][next_coord[X]] &= ~Directions.WEST
        elif direc == Directions.SOUTH:
            self._map[next_coord[Y]][next_coord[X]] &= ~Directions.NORTH
        elif direc == Directions.WEST:
            self._map[next_coord[Y]][next_coord[X]] &= ~Directions.EAST
        return

    def _generate_maze_recursive(self, curr_coord: tuple[int, int]) -> None:
        """Carve the maze recursively from one cell.

        Args:
            curr_coord: Coordinate currently being expanded.
        """
        cand: list[int] = [Directions.NORTH,
                           Directions.EAST,
                           Directions.SOUTH,
                           Directions.WEST]
        while cand:
            direc: int = random.choice(cand)
            if self._is_wall(curr_coord, direc):
                next_coord: tuple[int, int] = \
                    self._move_next_coord_coord(curr_coord, direc)
                self._break_wall(curr_coord, next_coord, direc)
                self._generate_maze_recursive(next_coord)
            cand.remove(direc)
        return

    def _check_dead_end(self, curr_coord: tuple[int, int]) -> int:
        """Detect whether a cell is a dead end.

        Args:
            curr_coord: Coordinate to inspect.

        Returns:
            The cell value when it is a dead end, otherwise 0.
        """
        cand: list[int] = [7, 11, 13, 14]
        for i in cand:
            if self._map[curr_coord[Y]][curr_coord[X]] == i:
                return i
        return 0

    @staticmethod
    def _detect_cand_direc(path: int) -> list[int]:
        """List wall directions that may be opened from a dead end.

        Args:
            path: Wall bit value of a dead-end cell.

        Returns:
            Candidate direction bits.
        """
        cand: list[int] = [Directions.NORTH,
                           Directions.EAST,
                           Directions.SOUTH,
                           Directions.WEST]
        if path == 7:
            cand.remove(Directions.WEST)
        elif path == 11:
            cand.remove(Directions.SOUTH)
        elif path == 13:
            cand.remove(Directions.EAST)
        elif path == 14:
            cand.remove(Directions.NORTH)
        return cand

    def _detect_connection_direction(self, curr_coord: tuple[int, int],
                                     cand: list[int]) -> int:
        """Choose a valid direction to connect a dead end.

        Args:
            curr_coord: Dead-end coordinate as (x, y).
            cand: Candidate direction bits to test.

        Returns:
            A direction bit to open, or 0 if none is available.
        """
        i: int = 0
        while i < len(cand):
            if not self._is_wall_outside(curr_coord, cand[i]):
                cand.remove(cand[i])
            elif self._is_wall_inside(curr_coord, cand[i]):
                cand.remove(cand[i])
            else:
                i += 1
        if cand:
            return random.choice(cand)
        else:
            return 0

    def _connect_dead_end(self, curr_coord: tuple[int, int],
                          path: int) -> None:
        """Open one extra wall from a dead-end cell when possible.

        Args:
            curr_coord: Dead-end coordinate as (x, y).
            path: Wall bit value of the dead-end cell.
        """
        cand: list[int] = self._detect_cand_direc(path)
        direc: int = self._detect_connection_direction(curr_coord, cand)
        if direc:
            next_coord: tuple[int, int] = \
                self._move_next_coord_coord(curr_coord, direc)
            self._break_wall(curr_coord, next_coord, direc)
        return

    def _convert_into_incomplete(self) -> None:
        """Convert a perfect maze into a less perfect maze."""
        for y in range(self._area[Y]):
            for x in range(self._area[X]):
                path: int = self._check_dead_end((x, y))
                if path:
                    self._connect_dead_end((x, y), path)
        return

    def _can_move(self, x: int, y: int,
                  dx: int, dy: int, wall: int,
                  visited: set[tuple[int, int]]) -> bool:
        """Check whether BFS can move from a cell to a neighbor.

        Args:
            x: Current x coordinate.
            y: Current y coordinate.
            dx: X movement amount.
            dy: Y movement amount.
            wall: Wall bit that blocks this movement.
            visited: Coordinates already visited by BFS.

        Returns:
            True if the neighbor is inside, open, and unvisited.
        """
        nx = x + dx
        ny = y + dy
        if nx < 0 or ny < 0 or nx >= self._area[X] or ny >= self._area[Y]:
            return False
        if self._map[y][x] & wall:
            return False
        if (nx, ny) in visited:
            return False
        return True

    def _solve_sh_path(self) -> str:
        """Find the shortest path from entry to exit with BFS.

        Returns:
            A string made from N, E, S, and W directions.

        Raises:
            Exception: If the exit cannot be reached.
        """
        visited: set[tuple[int, int]] = {self._start}
        queue = deque([self._start])
        parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
        letters: list[str] = []
        directions = [
            ("N", 0, -1, Directions.NORTH),
            ("E", 1, 0, Directions.EAST),
            ("S", 0, 1, Directions.SOUTH),
            ("W", -1, 0, Directions.WEST),
        ]
        while len(queue) > 0:
            x, y = queue.popleft()
            if (x, y) == self._goal:
                current = (x, y)
                while current != self._start:
                    current, letter = parent[current]
                    letters.append(letter)
                letters.reverse()
                return "".join(letters)
            for letter, dx, dy, wall in directions:
                nx = x + dx
                ny = y + dy
                if self._can_move(x, y, dx, dy, wall, visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = ((x, y), letter)
        raise Exception("Can't find goal")
