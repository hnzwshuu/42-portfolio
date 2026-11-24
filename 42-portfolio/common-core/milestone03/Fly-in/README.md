*This project has been created as part of the 42 curriculum by shanazaw.*

# Fly-in

## Description

Fly-in reads a network of zones and moves every drone from `start_hub` to
`end_hub`. It respects blocked and restricted zones, zone occupancy limits,
and connection capacity limits. The program uses only the Python standard
library for graph operations.

The code is intentionally split into small responsibilities:

- `models.py` contains the simple data objects.
- `parser.py` reads and validates a map.
- `flow.py` finds compatible routes and can revise earlier choices.
- `pathfinder.py` chooses routes and departure turns.
- `schedule.py` stores arrival times and reserves capacity by turn.
- `simulator.py` checks the timetable and builds simultaneous movement tokens.
- `main.py` connects the parts and prints the result.
- `playback.py` applies one validated turn at a time.
- `pygame_view.py` draws the interactive map using pygame.

The implementation uses English docstrings, descriptive names,
and explicit loops to make each step easier to follow. Number validation uses
ordinary string operations rather than regular expressions. Search routines
keep movement rules, exploration, and result reconstruction in separate methods.

## Instructions

Python 3.10 or newer is required.

Run the following commands from the repository root (macOS/Linux):

```sh
python3 -m venv .venv
source .venv/bin/activate
make install
make run
python3 main.py 01_linear_path.txt
python3 main.py 01_linear_path.txt --color
python3 main.py 02_simple_fork.txt --gui
make visualize MAP=02_circular_loop.txt
python3 main.py 03_ultimate_challenge.txt --gui
python3 main.py 01_the_impossible_dream.txt --gui
make lint
make lint-strict
```

Activate the virtual environment again when opening a new terminal. The
Makefile also accepts an explicit interpreter, for example:
`make lint PYTHON=.venv/bin/python`.

`make debug MAP=path/to/map` starts the program with Python's debugger.
`make clean` removes Python cache files.
The ten supplied input maps are stored at the repository root. The default
`MAP` for Makefile commands is `01_linear_path.txt`. Other input files can
be used with `make run MAP="path/to/map.txt"` or
`python3 main.py "path/to/map.txt"`.

If a pipe reader such as `head` closes the output early, the CLI stops
quietly with exit code 0. Invalid maps still report an error and exit with
code 1.

## Algorithm and implementation strategy

`MapParser` loads the file and checks each non-comment line. It rejects empty
metadata blocks, malformed `key=value` tags, duplicate zones or links, invalid
capacities, and links to zones that were not already defined. Missing start/end
declarations report the line immediately after the end of the file. Capacities
use ASCII decimal digits; coordinates also allow a leading `+` or `-`.
As specified, capacity values on start/end zones are ignored.

As an additional input restriction, all zones, including start and end, must
have distinct integer coordinate pairs. Duplicate-coordinate errors identify
the input line and both zone names. This is stricter than the subject, which
does not explicitly require unique coordinates.

### Routes and departure times

Think of a route lane as a path that accepts one new drone per turn. A
capacity-one zone can belong to one lane; a capacity-two zone can belong to two.
Each drone on a lane moves without stopping after leaving the start. Entering
a restricted zone takes two turns, including one turn on the connection.

`RouteFlow` creates a minimum-cost flow network using ordinary Python lists.
Each zone has an entrance and exit joined by its capacity limit. Each
connection costs the number of turns required to enter its destination.
Reverse edges can undo earlier choices, allowing several routes to change
together. Bellman-Ford finds the cheapest next change; it handles the negative
cost of undoing an earlier choice. Priority zones break equal-travel-time ties.

For `k` lanes with total travel time `C`, repeating each lane every turn
delivers `(H + 1) * k - C` drones by turn `H`, provided those lanes fit the
horizon. `PathFinder` compares the required horizon for successive minimum-cost
flows and keeps the best lane set. It assigns drones to the earliest available
arrival slots and stores their corresponding departure times. There is no
32-path candidate cutoff or one-drone-at-a-time local-improvement loop.

This is the temporally repeated flow construction for a single start and end.
The standard flow-over-time model permits waiting, but has a repeated optimal
solution without intermediate waits. Our zone capacity is represented by a
zero-time capacity edge: a non-waiting lane occupies a zone for one turn, so
the resulting timetable also satisfies the stricter zone occupancy limit.
Positive movement costs rule out cycles in a minimum-cost static flow,
including simultaneous use of both directions of an undirected connection.

### Simultaneous movements

The CLI passes both routes and departures to `Simulator`. It reserves and
checks the whole timetable before printing it. Arrivals and departures are
therefore independent of the order in which drone IDs are printed.

An entry into a restricted zone departing on turn `t` is printed as
`D<ID>-source-destination`; arrival at that zone is printed on turn `t+1`.
The arrival frees the connection for another departure that turn. Only the
actual arrival occupies the destination zone. Another drone leaving that zone
in the arrival turn frees a slot for the arriving drone.

For example, two drones using `s -> r(restricted) -> t`, with capacity one,
finish in four turns:

```text
D1-s-r
D1-r D2-s-r
D1-t D2-r
D2-t
```

The CLI uses the flow planner's timetable:

```python
finder = PathFinder(drone_map)
paths = finder.create_paths()
turns = Simulator(drone_map, paths, finder.departures).run()
```

### Complexity and performance

With `V` zones, `E` connections, and `A` augmentations, the main flow search
cost is `O(A * V * E)` using Bellman-Ford. Each augmentation sends a whole
bottleneck batch; it is not repeated once for every possible drone/route swap.
Decomposing flow also copies its lane paths. Assigning `N` drones to `k` lanes
uses `O(N log k)` heap operations. Rendering and reservations scale with the
number of actual route steps, plus drone sorting and the output turn count.
The flow graph uses `O(V + E)` memory; routes, reservations, and output also
require memory proportional to the generated flights and turns.

Completion times for the ten supplied maps are:

| Supplied map | Turns |
| --- | --- |
| `01_linear_path.txt` | 4 |
| `02_simple_fork.txt` | 4 |
| `03_basic_capacity.txt` | 4 |
| `01_dead_end_trap.txt` | 8 |
| `02_circular_loop.txt` | 10 |
| `03_priority_puzzle.txt` | 6 |
| `01_maze_nightmare.txt` | 13 |
| `02_capacity_hell.txt` | 16 |
| `03_ultimate_challenge.txt` | 26 |
| `01_the_impossible_dream.txt` | 43 |

### Shortest-path exercises studied

The following two exercises were used to study graph search. They are separate
from Fly-in and do not use its map-file format.

- **Positive-weight, undirected graph:** Given `N` vertices, `M` edges with
  positive lengths, and source vertex 1, output the minimum total length to
  each vertex, or `-1` when unreachable. In the first answer, an adjacency
  list and a FIFO queue repeatedly relax edges: when a shorter distance is
  found, the vertex is queued again. This can find the correct distances, but
  it is not Dijkstra's algorithm and may repeat much work. The second answer
  uses a min-heap of `(distance, vertex)` pairs. It processes the smallest
  tentative distance first, skips stale entries with
  `cost != dist[vertex]`, and relaxes neighbouring edges. This is Dijkstra's
  algorithm for the exercise's positive edge weights. In the first sample,
  the shortest distance to vertex 6 is 27 via `1 -> 2 -> 5 -> 6`.
- **Unweighted, undirected graph:** Given `N` vertices, `M` edges, and source
  vertex 1, output the minimum number of edges to each vertex, or `-1` when
  unreachable. The answer uses an adjacency list and a FIFO queue for BFS.
  Each vertex is visited when first discovered, and its distance is its
  predecessor's distance plus one. In the first sample, `1 -> 3 -> 2` gives
  vertex 2 a distance of two edges.

The key distinction is what "shortest" measures: BFS counts edges, while
weighted shortest paths minimize the sum of edge lengths. A FIFO queue with
repeated updates is different from a min-heap that always extracts the lowest
tentative distance. These exercises helped establish the graph and relaxation
ideas used in Fly-in. Fly-in does not use Dijkstra for its residual network:
reverse edges can have negative costs, so `RouteFlow` uses Bellman-Ford.

## Visual representation

### Simple Pygame view

Install the dependencies with `make install`, then run:

```sh
python3 main.py 02_simple_fork.txt --gui
```

Press the Right arrow key to advance exactly one turn. Press Escape or close
the window to finish. There is no automatic playback, speed control, mouse
operation, or 3D effect.

Connections are lines and zones are colored circles. Only start and end are
labelled `S` and `E`, avoiding overlapping long zone names. Crowded maps use
smaller circles automatically. Drones are yellow text such as `D1`, so they do
not cover zone colors. Several drones at one position are shown as `x7`.
A restricted entry is shown at the connection midpoint after its first turn
and at the zone after its second turn.

The GUI only replays the output of `Simulator.run()`; it does not calculate
routes. All supplied maps are scaled to fit the window. Pygame is imported
only when `--gui` is used, so normal text output does not require it.

### Terminal colors

The optional `--color` flag applies ANSI colors to movement tokens. Common
names such as `red`, `green`, `blue`, and `yellow` use their standard terminal
color. Any other valid single-word color receives a stable 256-color terminal
value (a consistent label, not an exact interpretation of arbitrary color
names). Transit tokens always use the actual movement direction, so the
destination's color does not depend on the order of endpoints in the input.
Without `--color`, output stays easy to redirect to a log or checker.

## Example

Input (`01_linear_path.txt`, with comments and blank lines omitted):

```text
nb_drones: 2
start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]
connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

Output:

```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

## Resources

Books consulted for algorithm and data-structure fundamentals:

- 米田優峻, *競技プログラミングの鉄則：アルゴリズム力と思考力を高める77の技術*:
  <https://www.amazon.co.jp/dp/483997750X>
- 大槻兼資, *問題解決力を鍛える！アルゴリズムとデータ構造*:
  <https://www.amazon.co.jp/dp/B08PV83L3N>

- Python documentation: <https://docs.python.org/3/>
- Pygame drawing and game-loop documentation: <https://www.pygame.org/docs/>
- `heapq` documentation: <https://docs.python.org/3/library/heapq.html>
- Flows over time and the temporally repeated flow construction (Section 2):
  <https://publications.rwth-aachen.de/record/1014347/files/1014347.pdf>
- PEP 8 style guide: <https://peps.python.org/pep-0008/>
- PEP 484 type hints: <https://peps.python.org/pep-0484/>

AI was used to help interpret the project specification, propose the file
structure, draft the implementation and tests, and review documentation. 
