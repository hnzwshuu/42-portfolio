# Team Organization

## Members and responsibilities

| Member | Main responsibilities |
| --- | --- |
| hfujisad | Game implementation: movement, maze integration, ghost strategies, rules, screens, cheats, highscores, maze and player rendering; refactoring; crash handling; static checks; packaging and itch.io delivery. |
| shanazaw | Ghost (monster) rendering; audio (music and sound effects); configuration parsing (the JSON-with-comments format); README rewrite in English; project management documentation. |

## How issues were handled

1. Reproduce the issue, ideally with a local test.
2. Fix it in the smallest affected place.
3. Run the local tests and `make lint`, then record the result and the
   next step in the log.
4. Commit with a message that says what changed and why.

Bugs found this way are listed in [acceptance_tests.md](acceptance_tests.md).

## AI assistance

AI assistance (Claude Code) was used for code explanations, design
discussion, debugging, requested refactors, local regression tests,
static-check fixes, packaging, and documentation drafts. Every change was
reviewed by the developer, who kept ownership of the gameplay design.
