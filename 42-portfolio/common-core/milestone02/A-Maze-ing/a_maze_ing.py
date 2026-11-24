#!/usr/bin/env python3
from draw_maze import DrawMaze
from mazegen import MazeGenerator
from config import Config
import details


def input_num() -> int:
    """Prompt the user for one menu command.

    Returns:
        The selected menu number from 1 to 5.
    """
    while 1:
        print(
            "=== A-Maze-ing ===",
            "1. Re-generate a new maze",
            "2. Show / Hide the shortest path",
            "3. Rotate the wall colors",
            "4. Set seed",
            "5. Quit",
            sep="\n"
        )
        try:
            num: int = int(input("Choice? (1-5): "))
            if num < 1 or num > 5:
                raise ValueError("Out of range")
        except Exception as ex:
            print(ex)
        else:
            break
    return num


def main() -> None:
    """Run the interactive maze generation program."""
    config: Config = details.set_config()
    gen_maze = MazeGenerator(config._width, config._height,
                             config._entry, config._exit,
                             config._perfect, None)
    gen_maze.show_pattern_message()
    draw_maze: DrawMaze = \
        DrawMaze(gen_maze.get_map(),
                 config._entry, config._exit,
                 gen_maze.get_sh_path())
    num: int = 1
    while 1:
        if num == 1:
            gen_maze.generate_maze()
            draw_maze.set_maze_map(gen_maze.get_map())
            draw_maze.set_sh_path(gen_maze.get_sh_path())
        elif num == 2:
            draw_maze.set_is_show()
        elif num == 3:
            draw_maze.set_clr()
        elif num == 4:
            while 1:
                try:
                    seed: int = int(input("Set seed value: "))
                except Exception:
                    print("Invalid syntax.")
                else:
                    break
            gen_maze.set_seed(seed)
            gen_maze.generate_maze()
            draw_maze.set_maze_map(gen_maze.get_map())
            draw_maze.set_sh_path(gen_maze.get_sh_path())
        elif num == 5:
            break
        draw_maze.slct_clr_maze()
        details.make_output_file(config, gen_maze)
        num = input_num()
    return


if __name__ == "__main__":
    main()
