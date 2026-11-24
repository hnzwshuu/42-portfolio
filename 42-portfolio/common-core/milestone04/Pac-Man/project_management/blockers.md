# Blocking Points and Conflicts

| Date | Blocking point or conflict | Resolution |
| --- | --- | --- |
| 10-23 | MLX text drawing flickered and was limited per batch; synchronizing each batch did not fully fix it. | Switched to Pillow text images composited into one frame. |
| 10-26 | The maze generator package had been modified locally to change the "42" shape, which breaks the "use as-is" rule. | Restored the package from the supplied wheel and verified every source file matches. |
| 10-27 | An auto-play prototype was added for testing, then judged out of scope. | Removed on 11-03 with its key, HUD label and tests. |
| 10-28 | The first pixel-art sprite prototype was not ready by the end of the day. | Reverted the same day and reimplemented on 11-07. |
| 10-30 | It was unclear whether the Pixabay audio could be published in the repository. | Kept out of Git at first with download instructions; included with full credits on 11-02. |
| 11-12 | `mypy --strict` failed because `mlx` and `mazegenerator` have no type information. | Added local stub files instead of `# type: ignore`. |
| 11-12 | Tests were committed although the subject does not grade them. | Tests made local-only and removed from the Git history. |
| 11-13 | WSL players saw "Can't initialize gpu": MLX needs a Vulkan driver. | Documented installing Mesa's software Vulkan driver in the package README. |
