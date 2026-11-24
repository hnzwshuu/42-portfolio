# Project Analysis and Technical Choices

## Constraints from the subject

- Python with MLX (or an equivalent library), object-oriented and modular.
- The assigned A-Maze-ing package must be used as-is; it is reinstalled
  during the review.
- No crashes and no tracebacks, even when the configuration is changed
  during the defense.
- flake8 and mypy must pass; functions and classes need docstrings.
- The game must be packaged and published on a gaming platform.

## Choices

| Topic | Choice | Reason | Alternative rejected |
| --- | --- | --- | --- |
| Architecture | `Game` owns rules and state; `GameVisualizer` owns MLX, layout, drawing and audio. Input handlers return `WindowAction` requests. | Rules can be tested without a window, and the window code stays small. | One visualizer class doing everything (the original design, split on 10-29 and 11-02). |
| Text and sprites | Draw text and characters as Pillow images, composite them into the MLX image buffer, and send the frame once. | MLX string drawing flickered and was limited to batches of commands; one transfer per frame is stable and fast. | `mlx_string_put` with synchronization (tried on 10-23). |
| Sprite style | 16×16 pixel art scaled with nearest-neighbor, cached per size and direction. | Matches the pixel font and costs almost nothing per frame. | Per-pixel circle drawing every frame (too slow on large windows). |
| Ghost pathfinding | Breadth-first-search distances from every open cell, computed once per maze. | Each decision only looks up four neighbors; no search during play. | Running BFS every time a ghost decides. |
| Ghost behavior | Strategy objects (chase, ambush ahead, ambush behind, flank with red, flee). | Each ghost's personality is replaceable and testable alone. | Hard-coded behavior inside `Ghost`. |
| Configuration | Pydantic models; invalid or missing fields fall back individually with a warning; whole-line `#` comments. | Keeps valid settings and never stops for a single bad value. | Rejecting the whole file on any error. |
| Timeout | Running out of time ends the game. | The subject leaves the choice open; it keeps the rule simple. | Restarting the level. |
| Highscores | JSON file, top ten, validated names, atomic save through a temporary file and `os.replace()`. | Small, readable, and safe against partial writes. | A database or online service. |
| Crash safety | Check the X display before `mlx_init()`; disable audio on failure; report generator failures and return to Home. | `mlx_init()` crashes in C without a display, which Python cannot catch. | Relying on exceptions from MLX. |
| Typing | Local stub files for `mlx` and `mazegenerator`. | They ship no type information; stubs make `--strict` pass without modifying the packages. | `# type: ignore`, which conflicts with `--warn-unused-ignores`. |
| Packaging | PyInstaller one-folder build, `play.sh` launcher, `.itch.toml`, uploaded with butler. | No Python needed by players; butler sends only changed files. | Shipping sources that need uv on the player's machine. |
| Tests | Local unittest suite, not submitted. | The subject says tests are not submitted or graded. | Committing tests to the repository. |
