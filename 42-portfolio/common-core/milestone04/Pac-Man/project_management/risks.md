# Risk Analysis

Likelihood and impact are rated Low, Medium or High for the evaluation and
for players of the packaged build.

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| The configuration is edited during the defense with missing, invalid or extreme values. | High | High | Per-field validation with defaults and warnings; malformed files, deep nesting, huge numbers and directories end with `Error:` and exit code 1. Checked with a matrix of broken files. |
| The machine has no display, audio device or Vulkan driver (SSH, containers, WSL). | Medium | High | The display is checked before `mlx_init()`; audio failures disable sound; the package README explains how to install a software Vulkan driver. |
| The reinstalled maze generator fails or behaves differently. | Low | High | Generator calls are guarded: at startup the game exits with a message; on a level change it reports the error and returns to Home. `perfect=False` is passed explicitly. |
| The score file is missing, corrupted, not writable, or its name is invalid. | Medium | Medium | Loading never rewrites the file; saving goes through a temporary file; invalid names fall back to `scores.json`; save errors keep scores in memory. |
| Large windows make rendering slow. | Medium | Medium | Cached sprites and text images; one image transfer per frame. Measured on 10-23 and 10-27. |
| Lint or type checks regress before submission. | Medium | High | `make lint` and `make lint-strict` are run on a clean export of the repository before pushing. |
| The evaluator runs the game with a Python older than 3.14. | Medium | Medium | README and Makefile use the project environment (`make install`, `make run`). Open: the system interpreter still fails with a traceback. |
| The packaged build fails on another Linux machine. | Medium | Medium | Built on Ubuntu 22.04 (glibc 2.35); tested from an extracted archive in another directory; the package README lists required libraries. |
| Asset licenses do not allow redistribution. | Low | Medium | Only CC0, Pixabay Content License and OFL assets; credits in the README and the package. |
| Work is lost or history becomes inconsistent between the two remotes. | Low | Medium | Every change is pushed to both GitHub and the 42 repository; a bundle backup was made before rewriting history. |
