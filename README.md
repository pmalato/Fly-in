*This project has been created as part of the 42 curriculum by pecoelho.*

# Fly-in


## Description

**Fly-in** is a Multiple Agent Path Finding (MAPF) simulator. Given a map of
interconnected zones and a fleet of drones, the program computes conflict-free
routes from a single **start** zone to a single **end** zone and simulates the
fleet moving turn by turn, respecting zone capacities, connection capacities,
and per-zone movement costs, while trying to minimize the total number of
simulation turns.

The project is split into four responsibilities:

- **Parsing** (`src/parser.py`) — reads and validates the custom map file
  format, turning it into raw hub/connection data.
- **Modeling** (`src/map.py`, `src/drone.py`) — builds the zone/connection
  graph (`Zone`, `Connection`, `Map`) and the drone state machine (`Drone`).
- **Scheduling** (`src/path_finder.py`, `src/scheduler.py`, `src/tracker.py`)
  — computes shortest/least-congested paths with a load-aware Dijkstra,
  reserves/releases paths, locks zone and connection capacity per turn, and
  drives the turn-by-turn simulation, replanning drones that wait too long.
- **Visualization** (`src/visualizer.py`) — a `pygame`-based graphical display
  (Genshin Impact–themed assets) that renders hubs, connections and drones,
  and lets you step through the simulation turn by turn.

The entry point is `fly-in.py`, which wires the parser, map, tracker,
scheduler and visualizer together.

## Instructions

### Requirements

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) as the package/dependency manager
  (see `pyproject.toml`)
- Dependencies: `pygame-ce`, plus `flake8` / `flake8-pyproject` / `mypy` for
  linting

### Install

```sh
make install
```

This runs `uv sync` and installs all dependencies declared in
`pyproject.toml` into a local virtual environment.

### Run

```sh
make run ARGS="path/to/map.txt"
```

This runs `uv run python3 fly-in.py path/to/map.txt`, i.e. the map file must
be passed as the first command-line argument. A graphical window opens;
press **SPACE** or **RIGHT** to advance the simulation one turn at a time,
**F11** to toggle fullscreen, and **ESC** (or close the window) to quit. When
the simulation finishes, the total turn count is printed to the terminal.

### Debug

```sh
make debug
```

Runs the program under Python's built-in debugger (`pdb`).

### Lint

```sh
make lint
make lint-strict
```

### Clean

```sh
make clean
make fclean
```

## Map file format

```text
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]
connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```

- `nb_drones: <positive int>` — number of drones to route.
- `start_hub:`/`end_hub:`/`hub: <name> <x> <y> [metadata]` — zone
  definitions. `max_drones` is ignored (unlimited) on `start_hub`/`end_hub`.
- `zone` metadata: `normal` (cost 1, default), `restricted` (cost 2),
  `priority` (cost 1, preferred by the scheduler), `blocked` (impassable).
- `connection: <name1>-<name2> [max_link_capacity=<int>]` — bidirectional
  edge between two previously defined zones (zone names cannot contain `-`
  or spaces).
- Lines starting with `#` and blank lines are ignored.
- Any malformed line raises a descriptive `FlyInError` (see `src/errors.py`)
  naming the offending line.

## Algorithm & implementation strategy

- **Graph model** — `Map` builds an adjacency list (`Zone -> [(Zone, link
  capacity)]`) and a per-edge base cost table from the parsed hubs and
  connections (no external graph library is used, per the subject's
  constraints).
- **Pathfinding** — `PathFinder.dijkstra_algo` is a hand-rolled Dijkstra over
  a binary heap (`heapq`). Each drone is routed independently, but the edge
  cost is **load-aware**: `edge_cost` adds extra wait turns proportional to
  how many drones already occupy the destination zone (`zone_load`) or are
  scheduled on the same connection (`link_load`), so later drones are
  naturally steered around congestion instead of all piling onto the
  shortest raw path. `priority` zones are given heap priority (a secondary
  sort key) so the algorithm favors them when costs tie.
- **Reservation** — `reserve_path`/`release_path` increment/decrement the
  `zone_load`/`link_load` counters for every edge on a computed path, so
  subsequent Dijkstra calls "see" the congestion created by drones already
  routed.
- **Turn-by-turn simulation** — `Tracker` enforces the hard constraints at
  runtime: `can_enter_zone`/`can_use_connection` check `max_drones` and
  `max_link_capacity`; `lock_zone`/`unlock_zone` and
  `lock_connection`/`unlock_connection` track exactly which drone occupies
  which zone/connection and until which turn. `advance_turn` resolves
  drones whose transit time has elapsed.
- **Scheduler** — `Scheduler.waiting_drones` is called once per turn: for
  every drone it checks whether the next hop is currently free; if not, the
  drone waits (`Drone.wait`) and, after `MAX_WAIT` (3) consecutive waited
  turns, is **replanned** (`Scheduler.replan`) — its remaining reservation is
  released and a fresh Dijkstra path is computed from its current position,
  which naturally routes it around whatever caused the deadlock/congestion.
  A hard `MAX_TURNS` (500) cap guards against genuine deadlocks and raises
  `UnsolveableMapError`.
- **Complexity** — each `dijkstra_algo` call is `O((V + E) log V)` with the
  binary heap. Paths are **not cached** across drones since congestion
  changes the effective cost of each edge between calls; they are however
  only recomputed for a given drone when it is first scheduled or when it
  is replanned after waiting too long, not on every turn. Memory usage is
  `O(V + E)` for the graph plus `O(drones)` for path/state tracking.
- **Output** — every turn, `Scheduler.waiting_drones` prints one
  space-separated line of `D<id>-<zone_or_connection>` tokens for every
  drone that moved that turn (drones that stay put are omitted), matching
  the format required by the subject. The final printed line is the total
  turn count.

## Visual representation

`src/visualizer.py` renders the simulation with `pygame`:

- Hubs are drawn as colored circles (using each hub's `color` metadata, or
  purple when no color/an unrecognized `rainbow`/`none` value is given),
  labeled with their zone name.
- Connections are drawn as white lines between the hubs they link.
- Each drone is displayed as a small themed sprite (randomly, but
  deterministically per drone id, chosen among three Genshin Impact–styled
  icons) positioned at its current zone.
- The simulation is advanced step-by-step by the user (SPACE/RIGHT arrow),
  which makes it easy to visually follow congestion, waiting, and
  replanning decisions turn by turn rather than only reading the text log.

## Example

Given the map file shown above (`nb_drones: 5`, `hub → corridorA →
tunnelB → goal`, plus a `roof1/roof2` branch), the terminal log looks like:

```text
Turn 1: D1-corridorA D2-roof1
Turn 2: D1-tunnelB D2-roof2
Turn 3: D1-goal D2-goal
...
Turn count: 3
```

(Exact drone assignment and turn count depend on capacities and congestion
on the actual map used.)

## Resources

- [Dijkstra's algorithm — overview](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)
- [`mypy` documentation](https://mypy.readthedocs.io/)
- [`flake8` documentation](https://flake8.pycqa.org/)
- [`pygame-ce` documentation](https://pyga.me/docs/)
- [`uv` documentation](https://docs.astral.sh/uv/)

### AI usage

AI assistance was used during this project as a support tool, not as a
replacement for understanding:

- Clarifying design questions about implementing Dijkstra's algorithm with a
  custom priority queue (`heapq`) without external graph libraries.
- Discussing strategies for congestion-aware pathfinding (how to make edge
  costs reflect current zone/connection load) and for detecting/breaking
  potential deadlocks through waiting thresholds and replanning.
- Reviewing error-handling and parser edge cases (duplicate keys, duplicate
  hubs/coordinates/connections, invalid metadata) against the subject's
  parser constraints.
- Helping draft and structure this README and the project's docstrings.

All AI-suggested approaches were reviewed, tested, and adapted by hand; no
generated code was used without being fully understood, in line with the
subject's AI usage guidelines.