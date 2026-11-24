"""Read command-line paths and save generated function calls as JSON."""

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from src.schema import load_functions, load_prompts


def parser() -> argparse.ArgumentParser:
    """Return a command-line parser for input and output file paths.

    Returns:
        Configured argument parser for the application's file paths.
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--functions_definition',
        type=Path,
        default=Path('data/input/functions_definition.json'),
    )
    argument_parser.add_argument(
        '--input',
        type=Path,
        default=Path('data/input/function_calling_tests.json'),
    )
    argument_parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/output/function_calling_results.json'),
    )
    return argument_parser


def write_results(path: Path, results: list[dict[str, Any]]) -> None:
    """Write function calls as indented JSON, overwriting the target file.

    Args:
        path: Output file path. Missing parent directories are created.
        results: Function calls to serialize.

    Raises:
        OSError: If the directory or file cannot be created or written.
        TypeError: If a value cannot be serialized as JSON.
        ValueError: If a value contains a non-finite number.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as output_file:
        json.dump(
            results,
            output_file,
            ensure_ascii=True,
            allow_nan=False,
            indent=2,
        )
        output_file.write('\n')


def main() -> int:
    """Validate inputs, generate function calls, and save the results.

    Report processing errors to stderr and completion to stdout.

    Returns:
        Exit status: 0 on success, or 1 on failure or user interruption.

    Raises:
        SystemExit: If argument parsing handles help or invalid arguments.
    """
    arguments = parser().parse_args()
    try:
        output_path = arguments.output.resolve()
        input_path = arguments.input.resolve()
        definitions_path = arguments.functions_definition.resolve()
        if output_path == input_path or output_path == definitions_path:
            raise ValueError('The output path must differ from input paths.')

        functions = load_functions(arguments.functions_definition)
        prompts = load_prompts(arguments.input)

        from src.pipeline import run

        results = run(functions, prompts)
        write_results(arguments.output, results)
        print(f'Wrote {len(results)} function calls to {arguments.output}')
        return 0
    except KeyboardInterrupt:
        print('Error: execution cancelled by user.', file=sys.stderr)
        return 1
    except Exception as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
