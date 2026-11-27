# Project Management

This directory documents how the Pac-Man project was planned, tracked,
tested and delivered. A Japanese version of each document is available
See the [project README](../README.md) for setup,
gameplay and the technical overview.

| Document | Contents |
| --- | --- |
| [team.md](team.md) | Who did what, how decisions were made, and how AI assistance was used. |
| [decisions.md](decisions.md) | Project analysis and the main technical choices, with the reasons and the alternatives rejected. |
| [risks.md](risks.md) | Risk analysis and the mitigation in place for each risk. |
| [acceptance_tests.md](acceptance_tests.md) | Acceptance test plan, how it was run, and the bugs found and fixed. |
| [blockers.md](blockers.md) | Blocking points and conflicts met during the project, and how each was resolved. |

## Method

Work was organized as a small Kanban flow kept in a running progress log
(development notes) rather than a fixed upfront schedule:

1. At the end of each session the log recorded what was done, how it was
   verified, and the **next step** to resume with.
2. The next session started from that step: inspect the affected code,
   implement or refactor it, verify it, then update the log.
3. Each finished step became one Git commit with a descriptive message, so
   `git log` is the detailed change history.

The project went through four phases: building the playable game
(October 13–31), restructuring the code into the `pacman/` package and
loading the configuration (November 2–4), reading and clarifying every
module (November 4–12), then checking the subject requirements and
delivering (November 12–20). 

## Board at submission

| Done | Open (accepted or deferred) |
| --- | --- |
| Movement, maze integration, ten levels, timers | Showing top scores directly on the home screen (ranking is one menu entry away) |
| Pacgums, power-ups, four ghost strategies, lives | A congratulatory line on the victory screen beyond "All Clear!" |
| Home, instructions, ranking, pause, result and name entry screens | Clamping out-of-range numbers instead of resetting them to defaults |
| Cheat mode, highscores, audio | Clean message when started with a system Python older than 3.14 |
| Configuration with per-field fallback and comments | Windows and macOS builds (MLX is Linux/X11 only) |
| Crash handling: no display, no audio, generator failure, invalid score paths | |
| flake8 and mypy (`lint` and `lint-strict`) clean | |
| PyInstaller build, itch.io upload, English README | |

## Verification and change tracking

Local headless regression tests covered movement, placement, collisions,
level changes, configuration recovery, highscores, controls and rendering.
Manual play checks covered the window and interaction flow. The tests are
kept locally and excluded from the submitted repository; see
[acceptance_tests.md](acceptance_tests.md) for the plan and results.

`make lint` and `make lint-strict` check style and types. Packaging was
checked by launching an extracted build from another directory. Use
`git log` and `git show` to follow individual changes.
