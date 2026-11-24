*This project has been created as part of the 42 curriculum by soarai, shanazaw.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and terminal viewer written in Python.

The program reads a configuration file, generates a maze from that configuration,
calculates a shortest path from the entry to the exit, writes the generated data
to an output file, and displays the maze in the terminal with colors.

This project also includes a reusable standalone module named `mazegen.py`.
The module exposes the `MazeGenerator` class, which can be imported by another
Python project. It can also be built as a standard Python package named
`mazegen`.

Main features:

- Random maze generation
- Optional perfect maze mode
- Shortest path calculation
- Colored terminal display for walls, entry, exit, and solution path
- Interactive menu for regeneration, solution display, wall color rotation, and
  seed input
- Reusable `MazeGenerator` class in a standalone module
- Pip-installable package named `mazegen`

## Instructions

### Requirements

This project targets Python 3.10 or later.

The runtime program only uses the Python standard library. The development and
packaging commands use:

- `flake8`
- `mypy`
- `build`
- `setuptools`
- `wheel`

### Install Development Tools

```sh
make install
```

This installs the tools used for linting, type checking, and package building.

### Run

```sh
python3 a_maze_ing.py config.txt
```

or:

```sh
make run
```

The program expects exactly one command-line argument: the path to the config
file.

### Interactive Menu

After the first maze is generated, the program displays this menu:

```text
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colors
4. Set seed
5. Quit
```

### Lint and Type Check

```sh
make lint
```

This command runs `flake8` and `mypy`.

### Build the Reusable Package

```sh
make build
```

This command runs:

```sh
python3 -m build --no-isolation
```

`python3 -m build` reads `pyproject.toml`, packages `mazegen.py` as a
single-file module, and creates standard Python package files under `dist/`.

Generated package file examples:

```text
mazegen-1.0.0.tar.gz
mazegen-1.0.0-py3-none-any.whl
```

The submission root also contains `mazegen-*` package files, as required by the
subject.

### Clean

```sh
make clean
```

This removes local Python caches and package build directories.

## Config File Format

The config file is a text file made of `KEY=VALUE` lines.
Blank lines and lines starting with `#` are ignored.

Complete format:

```text
WIDTH=<positive integer>
HEIGHT=<positive integer>
ENTRY=<x>,<y>
EXIT=<x>,<y>
OUTPUT_FILE=<file path>
PERFECT=<True|False>
```

Example:

```text
WIDTH=15
HEIGHT=12
ENTRY=0,0
EXIT=13,11
OUTPUT_FILE=maze.txt
PERFECT=True
```

Meaning of each key:

- `WIDTH`: maze width
- `HEIGHT`: maze height
- `ENTRY`: start coordinate
- `EXIT`: goal coordinate
- `OUTPUT_FILE`: output file path
- `PERFECT`: whether the maze should remain perfect

Rules:

- `WIDTH` and `HEIGHT` must be integers greater than zero.
- `ENTRY` and `EXIT` must use the `x,y` format.
- `ENTRY` and `EXIT` must be inside the maze.
- `ENTRY` and `EXIT` must be different coordinates.
- `PERFECT` must be exactly `True` or `False`.
- `OUTPUT_FILE` is where the generated maze data is written.

## Output File Format

The output file is written in this order:

```text
<maze row 0 as hexadecimal characters>
<maze row 1 as hexadecimal characters>
...

<entry x>,<entry y>
<exit x>,<exit y>
<solution path>
```

Each maze cell is stored as one hexadecimal character. The value is a bit mask
that represents which walls are still present:

```text
North = 1
East  = 2
South = 4
West  = 8
```

For example, `F` is hexadecimal for `15`, so all four walls are present.
When the east wall is removed, the `East = 2` bit is removed from the cell.
The neighboring cell is updated at the same time so that shared wall data stays
consistent.

The solution path is a string made from:

```text
N E S W
```

## Maze Generation Algorithm

The maze is generated with the digging method, implemented as randomized
depth-first search / recursive backtracking.

At the beginning, every cell has all four walls. From the current cell, the
algorithm randomly chooses an unvisited neighboring cell, removes the wall
between the two cells, and moves to that neighbor. The same process repeats
recursively. When there is no unvisited neighbor left, the recursion backtracks.

When `PERFECT=True`, this produces a connected maze where there is exactly one
path between any two open cells.

When `PERFECT=False`, the generator first creates a perfect maze, then detects
dead ends and opens extra walls when possible. This adds loops and produces a
non-perfect maze.

The shortest path from `ENTRY` to `EXIT` is calculated with breadth-first search
(BFS). BFS is appropriate here because every movement in the maze has the same
cost.

The required 42 pattern is handled by temporarily blocking the pattern cells
before carving the maze, then restoring them as closed pattern cells after
generation.

## Why This Algorithm Was Chosen

Recursive backtracking was chosen because it is simple, explainable during
evaluation, and naturally creates a perfect maze when no extra walls are opened.

It also fits this project's wall-bit representation. Moving from one cell to
another only requires removing the matching wall bit from the current cell and
from the neighboring cell.

BFS was chosen for the solution because all moves have the same cost, so BFS can
directly find one shortest path from `ENTRY` to `EXIT`.

## Reusable Module

The reusable part of this project is `mazegen.py`.

`mazegen.py` is a standalone Python module that exposes the `MazeGenerator`
class.

```python
from mazegen import MazeGenerator
```

Basic usage:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=15, seed=42, perfect=True)
generator.generate()

maze = generator.get_map()
solution = generator.get_solution()
```

Custom parameter example:

```python
generator = MazeGenerator(
    width=25,
    height=17,
    entry=(0, 0),
    exit=(24, 16),
    perfect=False,
    seed=1234,
)
generator.generate()
```

Accessing generated data:

- `get_map()` returns the generated maze structure as `maze[y][x]`.
- `get_solution()` returns one shortest path as a string using `N`, `E`, `S`,
  and `W`.

This internal maze structure is meant for reuse and does not have to be exactly
the same format as the output file.

### Package Installation Example

After building the package, or by using the package file located at the
submission root:

```sh
python3 -m pip install ./mazegen-1.0.0.tar.gz
```

or:

```sh
python3 -m pip install ./mazegen-1.0.0-py3-none-any.whl
```

Then another project can use:

```python
from mazegen import MazeGenerator
```

## Project Structure

```text
a_maze_ing.py          Main interactive program
config.py              Config parser and validator
details.py             Config loading and output-file writing
draw_maze.py           Terminal maze renderer
mazegen.py             Reusable maze generation module
pyproject.toml         Python package build configuration
LICENSE.md             License for reuse and distribution
README.md              Project documentation
config.txt             Example config file
Makefile               Common commands
```

## Team and Project Management

### Roles

- `soarai`: maze generation logic, wall-bit representation, package integration
  review
- `shanazaw`: terminal rendering, shortest-path display, output file handling,
  README, and reusable module documentation

Both members reviewed the final connection between config parsing, maze
generation, drawing, output, and packaging.

### Planning

Initial plan:

1. Read and validate the config file.
2. Represent the maze as a wall-bit grid.
3. Generate the maze.
4. Calculate the shortest path.
5. Draw the maze in the terminal.
6. Write the output file.
7. Add documentation and packaging.

How the plan evolved:

- The maze generation logic was separated into `mazegen.py` for reuse.
- `a_maze_ing.py` was updated to use `MazeGenerator` instead of a project-only
  generator file.
- Packaging files were added so the reusable module can be installed with pip.
- README and docstrings were expanded to explain reuse and package building.

### What Worked Well

- The wall-bit representation kept the output compact and made wall checks
  direct.
- Separating config, generation, output, and drawing made the project easier to
  check.
- Seed support made it possible to reproduce the same maze while debugging.

### What Could Be Improved

- The reusable module could have been separated earlier.
- More automated tests could be added for small mazes and invalid config files.
- The terminal renderer and interactive input could be separated further.

### Tools Used

- Python standard library: `random`, `collections.deque`, `sys`
- Makefile
- `flake8`
- `mypy`
- Python packaging tools: `build`, `setuptools`, `wheel`
- Git
- AI assistant support

AI was used for:

- Translating and checking subject requirements
- Reviewing whether the repository structure matched the reusability
  requirements
- Separating the reusable generator into `mazegen.py`
- Updating imports to use `MazeGenerator`
- Writing and checking docstrings and README sections
- Creating packaging files and verifying build/install commands
- Running final review checks such as lint, type check, package install, and
  output-file validation

The final code, behavior, and evaluation explanations remain the responsibility
of the team members.

## Resources

- Python `random` documentation:
  https://docs.python.org/3/library/random.html
- Python `collections.deque` documentation:
  https://docs.python.org/3/library/collections.html#collections.deque
- Python Packaging User Guide:
  https://packaging.python.org/en/latest/tutorials/packaging-projects/
- Setuptools `pyproject.toml` configuration:
  https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html
- Maze generation algorithms:
  https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Breadth-first search:
  https://en.wikipedia.org/wiki/Breadth-first_search

## License

This project includes `LICENSE.md` at the submission root. The maze generation
module is licensed under the MIT License, which allows reuse, modification, and
distribution in later projects.

## 日本語版

### Description

A-Maze-ing は、Python で実装した迷路生成プログラムです。

このプログラムは、設定ファイルを読み込み、その内容に従って迷路を生成します。
その後、開始地点から終了地点までの最短経路を求め、迷路データを出力ファイルに
書き込み、ターミナル上に色付きで迷路を表示します。

また、このプロジェクトには、後続プロジェクトから再利用できる
`mazegen.py` という単独モジュールが含まれています。このモジュールは
`MazeGenerator` クラスを公開しており、Python package として build して
pip で install できる形にもなっています。

主な機能:

- ランダムな迷路生成
- 完全迷路モードの切り替え
- 最短経路の計算
- 壁、開始地点、終了地点、最短経路を色付きでターミナルに表示
- メニューから迷路の再生成、最短経路の表示/非表示、壁色の変更、seed の指定
- 単独で import できる `MazeGenerator` クラス
- `mazegen` という名前の Python package として build 可能

### Instructions

#### 必要な環境

このプロジェクトは Python 3.10 以上を想定しています。

実行時に使うのは Python 標準ライブラリのみです。
開発、静的解析、package build には以下のツールを使います。

- `flake8`
- `mypy`
- `build`
- `setuptools`
- `wheel`

#### 開発用ツールのインストール

```sh
make install
```

このコマンドで、lint、型チェック、package build に必要なツールを
インストールします。

#### 実行方法

```sh
python3 a_maze_ing.py config.txt
```

または:

```sh
make run
```

このプログラムは、実行時引数として config file のパスを1つだけ受け取ります。

#### 実行中のメニュー

最初の迷路生成後、以下のメニューが表示されます。

```text
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colors
4. Set seed
5. Quit
```

#### Lint と型チェック

```sh
make lint
```

このコマンドは `flake8` と `mypy` を実行します。

#### 再利用 package の build

```sh
make build
```

このコマンドは内部で以下を実行します。

```sh
python3 -m build --no-isolation
```

`python3 -m build` は `pyproject.toml` を読み、`mazegen.py` を
単独モジュール package としてまとめます。その結果、標準的な Python package
file が `dist/` の中に生成されます。

生成される package file の例:

```text
mazegen-1.0.0.tar.gz
mazegen-1.0.0-py3-none-any.whl
```

subject の要求に合わせて、この提出root直下にも `mazegen-*` という名前の
package file を置いています。

#### Clean

```sh
make clean
```

Python の cache や package build 時に生成される directory を削除します。

### Config File Format

config file は `KEY=VALUE` 形式の text file です。
空行と `#` から始まる行は無視されます。

完全な形式:

```text
WIDTH=<positive integer>
HEIGHT=<positive integer>
ENTRY=<x>,<y>
EXIT=<x>,<y>
OUTPUT_FILE=<file path>
PERFECT=<True|False>
```

例:

```text
WIDTH=15
HEIGHT=12
ENTRY=0,0
EXIT=13,11
OUTPUT_FILE=maze.txt
PERFECT=True
```

各項目の意味:

- `WIDTH`: 迷路の横幅
- `HEIGHT`: 迷路の縦幅
- `ENTRY`: 開始地点の座標
- `EXIT`: 終了地点の座標
- `OUTPUT_FILE`: 生成結果を書き込むファイル名
- `PERFECT`: 完全迷路にするかどうか

制約:

- `WIDTH` と `HEIGHT` は 0 より大きい整数である必要があります。
- `ENTRY` と `EXIT` は `x,y` 形式で指定します。
- `ENTRY` と `EXIT` は迷路の範囲内である必要があります。
- `ENTRY` と `EXIT` は同じ座標にできません。
- `PERFECT` は `True` または `False` のどちらかです。
- `OUTPUT_FILE` は生成された迷路データを書き込むファイルです。

### Output File Format

出力ファイルには、以下の順番で情報が書き込まれます。

```text
<maze row 0 as hexadecimal characters>
<maze row 1 as hexadecimal characters>
...

<entry x>,<entry y>
<exit x>,<exit y>
<solution path>
```

迷路の各マスは、1文字の16進数で表されます。
その値は、どの方向に壁が残っているかを表す bit mask です。

```text
North = 1
East  = 2
South = 4
West  = 8
```

例えば `F` は16進数で `15` なので、4方向すべてに壁がある状態です。
東の壁を壊す場合は、`East = 2` の bit を落とします。
隣のマス側の対応する壁も同時に更新することで、壁情報の整合性を保ちます。

最短経路は以下の文字を使った文字列です。

```text
N E S W
```

### Maze Generation Algorithm

迷路生成には、穴掘り法を使っています。
実装上は randomized depth-first search / recursive backtracking です。

最初に、全てのマスを4方向すべて壁ありの状態にします。
現在地から未訪問の隣接マスをランダムに選び、そのマスとの間の壁を壊して移動します。
移動先でも同じ処理を繰り返し、進める未訪問マスがなくなったら前のマスに戻ります。

`PERFECT=True` の場合、この方法により、全体がつながっていて、任意の2点間に
経路が1つだけ存在する完全迷路になります。

`PERFECT=False` の場合、まず完全迷路を作り、その後、行き止まりを検出して
可能な場所の壁を追加で壊します。これによりループが増え、完全迷路ではない
迷路になります。

`ENTRY` から `EXIT` までの最短経路は breadth-first search、つまり BFS で
求めています。迷路の移動コストはどの方向も同じなので、BFS を使うと最短経路を
求めることができます。

また、subject で要求されている 42 pattern は、迷路生成前に該当セルを
一時的に塞ぎ、迷路生成後に閉じた pattern cell として戻すことで扱っています。

### Why This Algorithm Was Chosen

recursive backtracking を選んだ理由は、実装が比較的シンプルで、評価時にも
説明しやすく、追加で壁を壊さなければ自然に完全迷路を作れるからです。

この project では各マスの壁を bit で管理しています。
そのため、隣のマスへ移動するときは、現在のマスと隣のマスの対応する wall bit を
落とすだけで壁を壊せます。この表現と recursive backtracking は相性が良いです。

最短経路には BFS を選びました。
この迷路では各移動のコストが同じなので、BFS は `ENTRY` から `EXIT` までの
最短経路を直接求めるのに適しています。

### Reusable Module

この project で再利用可能な部分は `mazegen.py` です。

`mazegen.py` は単独で import できる Python module で、`MazeGenerator`
クラスを公開しています。

```python
from mazegen import MazeGenerator
```

基本的な使い方:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=15, seed=42, perfect=True)
generator.generate()

maze = generator.get_map()
solution = generator.get_solution()
```

custom parameter の指定例:

```python
generator = MazeGenerator(
    width=25,
    height=17,
    entry=(0, 0),
    exit=(24, 16),
    perfect=False,
    seed=1234,
)
generator.generate()
```

生成結果へのアクセス:

- `get_map()` は生成された迷路構造を `maze[y][x]` の2次元 list として返します。
- `get_solution()` は `N`, `E`, `S`, `W` で表した最短経路文字列を返します。

この maze structure は再利用用の内部表現であり、必ずしも出力ファイルと
完全に同じ形式である必要はありません。

#### Package Installation Example

build 済み、または提出rootに置いてある package file を使って install できます。

```sh
python3 -m pip install ./mazegen-1.0.0.tar.gz
```

または:

```sh
python3 -m pip install ./mazegen-1.0.0-py3-none-any.whl
```

install 後、別の project から以下のように使えます。

```python
from mazegen import MazeGenerator
```

### Project Structure

```text
a_maze_ing.py          メインの対話型プログラム
config.py              config file の parse と validation
details.py             config 読み込みと output file 書き込み
draw_maze.py           ターミナルへの迷路描画
mazegen.py             再利用可能な迷路生成 module
pyproject.toml         Python package build 設定
LICENSE.md             再利用と配布のための license
README.md              project documentation
config.txt             config file の例
Makefile               よく使う command
```

### Team and Project Management

#### Roles

- `soarai`: 迷路生成ロジック、wall-bit 表現、package 統合の確認
- `shanazaw`: ターミナル描画、最短経路表示、output file 処理、
  README と reusable module documentation

最終的には、config parsing、maze generation、drawing、output、packaging の
つながりを2人で確認しました。

#### Planning

最初の計画:

1. config file を読み取り、validation する。
2. 迷路を wall-bit の grid として表現する。
3. 迷路を生成する。
4. 最短経路を求める。
5. ターミナルに迷路を描画する。
6. output file を作成する。
7. documentation と packaging を追加する。

計画が変化した点:

- `a_maze_ing.py` は project 専用の generator file ではなく
  `MazeGenerator` を使う形に変更しました。
- pip install 可能にするために packaging file を追加しました。
- README と docstring に、再利用方法と package build 方法を追記しました。

#### What Worked Well

- wall-bit 表現により、出力形式がコンパクトになり、壁判定も直接書けました。
- config、generation、output、drawing を分けたことで、確認しやすくなりました。
- seed を使えるようにしたことで、同じ迷路を再現しながら debug できました。

#### What Could Be Improved

- 再利用 module への分離を、もっと早い段階で行うべきでした。
- 小さい迷路や不正な config file に対する自動テストを増やせます。
- terminal renderer と interactive input は、さらに分離できます。

#### Tools Used

- Python standard library: `random`, `collections.deque`, `sys`
- Makefile
- `flake8`
- `mypy`
- Python Packaging tools: `build`, `setuptools`, `wheel`
- Git
- AI assistant support

AI を使った部分:

- subject の要求の翻訳と確認
- repository structure が再利用要件に合っているかの review
- reusable generator を `mazegen.py` に分離する作業
- `MazeGenerator` を使うための import 整理
- docstring と README の作成、確認
- packaging file の作成と build/install command の確認
- lint、type check、package install、output file validation などの最終確認

最終的な code、挙動、評価での説明は team member の責任です。

### Resources

- Python `random` documentation:
  https://docs.python.org/3/library/random.html
- Python `collections.deque` documentation:
  https://docs.python.org/3/library/collections.html#collections.deque
- Python Packaging User Guide:
  https://packaging.python.org/en/latest/tutorials/packaging-projects/
- Setuptools `pyproject.toml` configuration:
  https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html
- Maze generation algorithms:
  https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Breadth-first search:
  https://en.wikipedia.org/wiki/Breadth-first_search

### License

この project には、提出rootに `LICENSE.md` を含めています。
迷路生成 module は MIT License のもとで提供されており、後続 project での
再利用、変更、配布を許可しています。
