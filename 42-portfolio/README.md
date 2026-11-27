# 42 Portfolio

42 TokyoのCommon Coreで取り組んだ課題を、マイルストーンごとに整理したポートフォリオです。

C・Pythonを中心に、ライブラリの実装、アルゴリズム、システム管理、並行処理、ネットワーク、LLM、ゲーム開発を扱っています。各課題へのリンクから、ソースコードやREADMEを確認できます。

## 構成

```text
42-portfolio/
├── common-core/
│   ├── milestone00/
│   │   └── Libft/                  C標準ライブラリの再実装
│   ├── milestone01/
│   │   ├── ft_printf/              printfの基本機能の再実装
│   │   ├── get_next_line/          ファイルを1行ずつ読み取る関数
│   │   └── push_swap/              2つのスタックによるソート
│   ├── milestone02/
│   │   ├── A-Maze-ing/             迷路生成・最短経路探索
│   │   ├── Born2beroot/            Linuxサーバー構築の記録
│   │   └── python-modules/
│   │       └── Python_Module_00/ … Python_Module_10/
│   ├── milestone03/
│   │   ├── Call_Me_Maybe/          LLMによる関数呼び出しの生成
│   │   ├── Codexion/               共有リソースの並行処理
│   │   └── Fly-in/                 複数ドローンの経路計画
│   └── milestone04/
│       ├── NetPractice/            IPv4・サブネット・ルーティング
│       └── Pac-Man/                迷路ゲーム
└── advanced/                       今後の課題の追加先
```

## Milestone 00

| 課題 | 概要 | 主な言語・技術 |
| --- | --- | --- |
| [libft](common-core/milestone00/Libft/) | 文字列・メモリ操作、文字判定、数値変換、出力、単方向リスト操作など43関数を実装したC静的ライブラリ。 | C、Make、動的メモリ管理、連結リスト |

## Milestone 01

| 課題 | 概要 | 主な言語・技術 |
| --- | --- | --- |
| [ft_printf](common-core/milestone01/ft_printf/) | 可変長引数と書式文字列を解析し、文字・文字列・整数・ポインタを出力する `printf` の基本機能の再実装。 | C、Make、`stdarg.h`、`write` |
| [get_next_line](common-core/milestone01/get_next_line/) | ファイルディスクリプタから呼び出しごとに1行を返す関数。読み込み済みの余剰データを静的変数に保持する。 | C、POSIX `read`、動的メモリ管理、static変数 |
| [push_swap](common-core/milestone01/push_swap/) | 2つのスタックを使って整数列をソートする操作列を生成。複数のソート戦略、入力に応じた戦略選択、操作数の計測を実装したチーム課題。 | C、Make、連結リスト、チャンク分割、基数ソート |

## Milestone 02

| 課題 | 概要 | 主な言語・技術 |
| --- | --- | --- |
| [A-Maze-ing](common-core/milestone02/A-Maze-ing/) | 設定ファイルから迷路を生成し、最短経路の計算、ファイル出力、色付きターミナル表示を行うチーム課題。生成器をPythonパッケージとして再利用できる。 | Python、DFS、recursive backtracking、BFS、Python packaging |
| [Born2beroot](common-core/milestone02/Born2beroot/) | Linux仮想サーバーの構築手順とシステム管理の記録。ユーザー・権限管理、SSH、ファイアウォール、ディスク構成、監視処理をREADMEに整理。 | Debian、VirtualBox、LVM、UFW、AppArmor、Bash、cron |
| [Python Modules 00–10](common-core/milestone02/python-modules/) | Pythonの基本構文から、オブジェクト指向、例外処理、データ検証、関数型プログラミングまでを扱う演習。 | Python、OOP、Design Patterns、Pydantic、Functional Programming |

### Python Modules

各モジュールは演習ごとのディレクトリとソースコードで構成しています。

| モジュール | 主な内容 |
| --- | --- |
| [Module 00](common-core/milestone02/python-modules/Python_Module_00/) | 基本的な入出力、条件分岐、反復、再帰 |
| [Module 01](common-core/milestone02/python-modules/Python_Module_01/) | クラス、継承、カプセル化、classmethod・staticmethod |
| [Module 02](common-core/milestone02/python-modules/Python_Module_02/) | 例外の送出・捕捉、独自例外、`try / except / finally` |
| [Module 03](common-core/milestone02/python-modules/Python_Module_03/) | CLI引数、コレクション、内包表記、ジェネレータ |
| [Module 04](common-core/milestone02/python-modules/Python_Module_04/) | ファイル入出力、標準ストリーム、context manager |
| [Module 05](common-core/milestone02/python-modules/Python_Module_05/) | 抽象クラス、ポリモーフィズム、データ処理パイプライン |
| [Module 06](common-core/milestone02/python-modules/Python_Module_06/) | パッケージ構成、import、名前空間、循環依存 |
| [Module 07](common-core/milestone02/python-modules/Python_Module_07/) | Abstract Factory・Strategyによる生成と行動の分離 |
| [Module 08](common-core/milestone02/python-modules/Python_Module_08/) | 仮想環境、依存管理、環境変数、pandas・NumPy・Matplotlib |
| [Module 09](common-core/milestone02/python-modules/Python_Module_09/) | Pydanticによる構造化データとフィールド間の制約の検証 |
| [Module 10](common-core/milestone02/python-modules/Python_Module_10/) | lambda、高階関数、クロージャ、`functools`、デコレータ |

## Milestone 03

| 課題 | 概要 | 主な言語・技術 |
| --- | --- | --- |
| [Call Me Maybe](common-core/milestone03/Call_Me_Maybe/) | ローカルLLMで自然言語の要求から関数名と型付き引数を選び、制約付きデコーディングでJSON形式の関数呼び出しを生成する。 | Python、Qwen3-0.6B、NumPy、Pydantic、constrained decoding |
| [Codexion](common-core/milestone03/Codexion/) | 複数のcoderが共有dongleを取り合う並行シミュレーション。FIFO・EDFによる要求順序、クールダウン、burnout監視を扱う。 | C、POSIX threads、mutex、condition variable、monotonic clock |
| [Fly-in](common-core/milestone03/Fly-in/) | ゾーンと接続の容量制限を考慮して、複数ドローンの経路・出発時刻を計画。移動をテキストまたはGUIで表示する。 | Python、グラフ、minimum-cost flow、Bellman–Ford、pygame |

## Milestone 04

| 課題 | 概要 | 主な言語・技術 |
| --- | --- | --- |
| [NetPractice](common-core/milestone04/NetPractice/) | IPv4アドレス、サブネットマスク、ルーティングを調整するネットワーク演習。全10レベルの設定JSONを収録。 | JSON、IPv4、CIDR、routing、default gateway |
| [Pac-Man](common-core/milestone04/Pac-Man/) | 自動生成された迷路でpacgumを回収し、ghostを回避するチーム課題。レベル進行、スコア保存、メニュー、音声を実装。 | Python、MiniLibX、Pillow、Pydantic、pygame-ce（音声）、maze generator |

## Advanced

[advanced/](advanced/) は、今後取り組む課題の追加先です。

## Author

shanazaw（42 Tokyo）

チーム課題の共同開発者・担当範囲は、各課題のREADMEに記載しています。

## Reference

全体READMEの構成は、[Yonaha88さんの42_subject](https://github.com/Yonaha88/42_subject/tree/main)を参考にしています。課題の説明は、このリポジトリのソースコードと既存READMEに基づいて記載しています。

