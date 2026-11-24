# Acceptance Test Plan

## How tests were run

- **Automated:** a local unittest suite (`python -m unittest discover -s
  tests`), run headless after every change. It grew from 112 tests
  (10-23) to 224 (11-12), then was cleaned up to 211 by removing
  duplicates and tests of removed features. It is not submitted.
- **Manual:** play sessions in a real MLX window, plus launching the
  packaged build from an extracted archive in another directory.
- **Static:** `make lint` and `make lint-strict` on a clean export of the
  repository.

## Features tested

| Area | Acceptance criteria | Method | Status |
| --- | --- | --- | --- |
| Launch | Exactly one argument; usage and errors without traceback | Automated, manual | Pass |
| Configuration | Comments ignored; unknown keys ignored; invalid fields fall back with a warning; ten default levels | Automated, broken-file matrix | Pass |
| Maze | Assigned package used as-is; fixed seed for level one, random afterwards | Automated | Pass |
| Layout | Pacgums in corridors, super pacgums and ghosts in corners, player in the middle | Automated | Pass |
| Movement | Corridors only; arrows and WASD; queued turns; reversal | Automated, manual | Pass |
| Ghosts | Chase, ambush, flank, flee when edible, respawn after 5 seconds | Automated | Pass |
| Rules | Lives, respawn, level clear, timeout, all clear; score never decreases | Automated | Pass |
| Screens | Home, instructions, ranking, pause, ready, stage clear, game over, all clear | Automated rendering, manual | Pass |
| Highscores | Top ten, name rules, persistence, corrupted and unwritable files | Automated | Pass |
| Cheats | Toggle sequence; next level, freeze, invincibility, lives, time, speed, ×10 | Automated, manual | Pass |
| Robustness | No display, no audio, no Vulkan, generator failure, Ctrl+C | Automated, manual | Pass |
| Package | Runs without Python from another directory; scores stored beside the game | Manual | Pass |

## Bugs found and fixed

| Found | Bug | Fix |
| --- | --- | --- |
| 10-22 | Keys typed as part of the cheat sequence also moved the player or skipped levels. | Keys matching the sequence are consumed before normal controls. |
| 10-23 | Text flickered because MLX drew strings in separate batches. | Text composited into the image; one transfer per frame. |
| 10-23 | About 28 FPS on a 2460×1340 window. | Ghost and player sprites cached as images. |
| 10-27 | Wall-pass cheat could leave the maze because of a missing bounds check. | Bounds check fixed in `Maze.can_move()`. |
| 10-28 | Panels overflowed after switching to the pixel font. | Panel width computed from the widest line. |
| 11-03 | Restarting a game did not reuse the level-one seed. | The configured seed is passed whenever level one is generated. |
| 11-12 | Disabling cheats did not restore the player's speed. | Speed reset with the other cheat effects. |
| 11-12 | The game crashed without an audio device or when started outside the repository. | Audio disabled on errors; asset paths made absolute. |
| 11-12 | `mlx_init()` crashed (segmentation fault) without a reachable display. | Display checked with XCB before `mlx_init()`. |
| 11-12 | Fewer than ten levels when `levels` was missing. | Ten default levels. |
| 11-19 | Ctrl+C during the MLX loop printed a traceback. | Interrupt handled; exit code 130. |
| 11-20 | A generator failure on a level change raised inside the MLX callback. | Failure reported; the game returns to Home. |
| 11-20 | A score file name with a NUL character crashed on save. | Name validated in the configuration; save errors caught. |
