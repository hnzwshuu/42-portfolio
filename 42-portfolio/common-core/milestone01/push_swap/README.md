*This project has been created as part of the 42 curriculum by soarai, shanazaw.*

# push_swap

## Description

`push_swap` は、2つのスタック `a` と `b` と、限られた操作だけを使って整数列を昇順に並べ替えるプログラムです。

初期状態では、すべての整数がスタック `a` に入り、スタック `b` は空です。プログラムは入力された整数列を解析し、スタック `a` が小さい順にソートされるように、以下の操作列を標準出力へ表示します。

- `sa`, `sb`, `ss`
- `pa`, `pb`
- `ra`, `rb`, `rr`
- `rra`, `rrb`, `rrr`

このプロジェクトでは、単に正しくソートするだけでなく、出力する操作数をできるだけ少なくすることを目標にしています。

## Instructions

### Compile

```sh
make
```


### Clean

```sh
make clean
make fclean
make re
```

### Usage

```sh
./push_swap 3 2 1
```

戦略を指定しない場合は、`--adaptive` と同じ挙動になります。

```sh
./push_swap 3 2 1
./push_swap --adaptive 3 2 1
```

戦略を明示的に指定することもできます。

```sh
./push_swap --simple 3 2 1
./push_swap --medium 3 2 1
./push_swap --complex 3 2 1
```


### Error Handling

以下のような入力はエラーとして扱います。

- 整数ではない引数
- `int` の範囲外の値
- 重複した値
- 不正なオプション

エラー時は標準エラー出力に `Error` と改行を表示します。

## Algorithms

このプロジェクトでは、4つのソート戦略を実装しています。

### Simple Strategy: O(n^2)

`--simple` では、最小値を探してスタック `a` の先頭へ移動し、`pb` でスタック `b` に退避する方法を使います。

すべての要素について、残っているスタックの中から最小値の位置を探索するため、Push_swap の操作モデルでは上限を O(n^2) として扱います。

### Medium Strategy: O(n sqrt(n))

`--medium` では、値の順位を使ったチャンクベースのソートを使います。

入力サイズ `n` に対して、おおよそ `sqrt(n)` の幅を持つチャンクを作り、順位が現在のチャンク範囲に入る要素をスタック `b` に移します。その後、スタック `b` から最大値を順にスタック `a` へ戻します。

チャンク数と各チャンク内の探索・回転のバランスから、Push_swap の操作モデルでは O(n sqrt(n)) の戦略として扱います。

### Complex Strategy: O(n log n)

`--complex` では、順位に基づく radix sort を使います。

元の値を直接ビットで見るのではなく、各値を順位として扱います。例えば、500個の入力であれば順位は `0` から `499` になり、必要なビット数を抑えることができます。

各ビットについて、対象ビットの値に応じて `pb` または `ra` を行い、その後 `pa` でスタック `a` に戻します。必要なビット数は `log n` なので、Push_swap の操作モデルでは O(n log n) の戦略として扱います。

### Adaptive Strategy

`--adaptive` は入力の disorder を計算し、その値に応じて内部で使う戦略を切り替えます。戦略を指定しない場合も、この adaptive strategy を使用します。

disorder は、スタック `a` 内のすべてのペアについて、前にある値が後ろの値より大きい組み合わせを数えることで計算します。

```text
disorder = number_of_inverted_pairs / number_of_all_pairs
```


adaptive strategy の閾値は以下の通りです。

- `disorder < 0.2`: simple strategy, O(n^2)
- `0.2 <= disorder < 0.5`: medium strategy, O(n sqrt(n))
- `disorder >= 0.5`: complex strategy, O(n log n)

低い disorder の入力では、すでにかなり整列に近いため、単純な最小値抽出でも十分に扱いやすいと判断しました。中程度の disorder では、チャンク分割によって操作数を抑えます。高い disorder の入力では、入力順に強く依存しにくい rank-based radix sort を使い、O(n log n) の上限を保つ設計にしています。

## Benchmark Mode

`--bench` を指定した場合、ソート後にベンチマーク情報を標準エラー出力へ表示します。

表示する情報は以下です。

- 計算した disorder
- 使用した戦略名
- 操作数の合計
- 各操作の回数

例:

```sh
./push_swap --bench --adaptive 3 2 1 2> bench.txt
```

## Contributions

このプロジェクトは `soarai` と `shanazaw` の2人で作成しました。

`soarai` は、コマンドライン引数からスタック構造を作成する部分、ベンチマークモード、ヘッダファイル、Makefile を担当しました。

`shanazaw` は、4つのソートアルゴリズム、Push_swap 操作関数、README の作成を担当しました。

## Resources

以下の資料や考え方を参考にしました。

- 42 subject: Push_swap

### AI Usage

AI は、実装をそのまま生成して貼り付ける目的ではなく、設計の整理、テストコマンドの作成、README の文章整理に利用しました。

具体的には、以下の用途で利用しました。

- adaptive strategy と disorder の仕様解釈
- benchmark 表示の形式確認
- README に必要な項目の整理
