import sys
from config import Config
from mazegen import MazeGenerator


def set_config() -> Config:
    """Read, parse, and validate the config file from command-line arguments.

    Returns:
        A validated Config object.
    """
    if len(sys.argv) != 2:
        print("usage example: python3 a_maze_ing.py config.txt")
        sys.exit(0)
    args = sys.argv[1]
    try:
        with open(args, mode="r") as f:
            config_input: list[str] = f.readlines()
    except Exception as ex:
        print(f"failed to read config file: {ex}")
        sys.exit(0)
    try:
        config: Config = Config(config_input)
    except Exception as ex:
        print(ex)
        sys.exit(0)
    try:
        config.check()
    except Exception as ex:
        print(ex)
        sys.exit(0)
    return config


def make_output_file(config: Config, gen_maze: MazeGenerator) -> None:
    """Write the generated maze, coordinates, and shortest path to a file.

    Args:
        config: Validated configuration containing the output file path.
        gen_maze: Generated maze object containing map and shortest path data.
    """
    try:
        with open(config._output_file, "w") as f:
            for row in gen_maze.get_map():
                line = ""
                for value in row:
                    line += format(value % 16, "X")
                f.write(f"{line}\n")
            f.write("\n")
            x, y = config._entry
            f.write(f"{str(x)},{str(y)}\n")
            x, y = config._exit
            f.write(f"{str(x)},{str(y)}\n")
            f.write(f"{gen_maze.get_sh_path()}\n")
    except Exception as ex:
        print(f"failed to write output file: {ex}")
        sys.exit(0)
    return
