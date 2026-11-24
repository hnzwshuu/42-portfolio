*This project has been created as part of the 42 curriculum by shanazaw.*

# libft

42 Tokyo の課題で作った、自分用の C 言語ライブラリです。
よく使う標準関数を自分で実装したり、リスト構造を扱う関数を作ったりしています。

## Description / 説明

この課題では、C 言語で使える静的ライブラリを作ります。

標準関数をそのまま使うのではなく、自分で書いてみることで、
文字列、メモリ、ポインタ、malloc、リスト構造などの理解を深めることが目的です。

完成すると `libft.a` というライブラリができます。

## Instructions / 使い方

この課題では `Makefile` を使います。

```sh
make
```

`.c` ファイルをコンパイルして、`libft.a` を作ります。

```sh
make clean
```

オブジェクトファイルを削除します。

```sh
make fclean
```

オブジェクトファイルと `libft.a` を削除します。

```sh
make re
```

一度全部消してから、もう一度作り直します。

## ファイル

- `Makefile`
- `libft.h`
- `ft_*.c`
- `README.md`

`libft.h` には、関数のプロトタイプとリスト構造体を書いています。

## Part 1

Part 1 では、基本的な標準関数を作ります。

### is 系

`ft_isalpha` や `ft_isdigit` などは、渡された文字コードが条件に合っているかを判定します。

例:

- `ft_isalpha`
- `ft_isdigit`
- `ft_isalnum`
- `ft_isascii`
- `ft_isprint`

### mem 系

`mem` 系の関数では、`void *` を使ってメモリを扱います。
`void *` のままだと中身を直接操作しにくいので、必要な型にキャストして使います。

例:

- `ft_memset`
- `ft_bzero`
- `ft_memcpy`
- `ft_memmove`
- `ft_memchr`
- `ft_memcmp`

### str 系

文字列を扱う関数です。
`const` が付いている引数は、中身を書き換えないように注意します。

例:

- `ft_strlen`
- `ft_strlcpy`
- `ft_strlcat`
- `ft_strchr`
- `ft_strrchr`
- `ft_strncmp`
- `ft_strnstr`
- `ft_strdup`

### malloc を使う関数

`malloc` でメモリを確保する関数では、失敗したときに `NULL` を返すようにします。

例:

- `ft_calloc`
- `ft_strdup`

## Part 2

Part 2 では、Part 1 より少し複雑な関数を作ります。

例:

- `ft_substr`
- `ft_strjoin`
- `ft_strtrim`
- `ft_split`
- `ft_itoa`
- `ft_strmapi`
- `ft_striteri`
- `ft_putchar_fd`
- `ft_putstr_fd`
- `ft_putendl_fd`
- `ft_putnbr_fd`

ここでも `malloc` に失敗したら `NULL` を返します。

特に `ft_split` は何回も `malloc` を使うので、
途中で失敗した場合は、それまでに確保したメモリを全部 `free` する必要があります。

## Part 3

Part 3 ではリスト構造を扱います。

`libft.h` には次の構造体を書いています。

```c
typedef struct s_list
{
	void			*content;
	struct s_list	*next;
}	t_list;
```

作った関数:

- `ft_lstnew`
- `ft_lstadd_front`
- `ft_lstsize`
- `ft_lstlast`
- `ft_lstadd_back`
- `ft_lstdelone`
- `ft_lstclear`
- `ft_lstiter`
- `ft_lstmap`

`ft_lstdelone` は、1つのノードを削除する関数です。
前後のノードをつなげ直す処理はしないので、それは関数の外で行う必要があります。

## Resources / 参考

- 課題 PDF
- `man` コマンド
- リスト構造についての記事
  https://daedaeu.com/list-structure/
- 矢沢 久雄『コンピュータはなぜ動くのか 第2版 知っておきたいハードウエア＆ソフトウエアの基礎知識』日経BP社，2022年．

AI は、関数の挙動が正しいかを確認したり、自分の理解が曖昧だった部分を深掘りしたりするために使いました。
実装そのものを自動生成する目的では使っていません。
