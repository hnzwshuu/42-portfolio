*This project has been created as part of the 42 curriculum by shanazaw.*

# Born2beRoot

## Description（概要）

Born2beRootは、仮想マシン上にLinuxサーバーを構築し、Linuxのシステム管理、ユーザー管理、権限管理、ネットワーク、ファイアウォール、SSH、パスワードポリシー、LVM、シェルスクリプト、cronなどの基礎を学ぶプロジェクトである。

単にDebianをインストールすることが目的ではなく、

* なぜ仮想マシンを利用するのか
* rootと一般ユーザーは何が違うのか
* sudoによってどのように権限を管理するのか
* SSHによってどのように別のコンピュータから接続するのか
* ファイアウォールがなぜ必要なのか
* 強いパスワードポリシーをなぜ設定するのか
* LVMやディスク暗号化が何をしているのか
* Linuxの情報をどのようにコマンドから取得するのか
* cronを使って処理を自動化する方法

などを理解することが重要である。

このプロジェクトではGUIを使用せず、基本的にCLIからサーバーを管理する。

---

# 使用した環境

* 仮想化ソフトウェア: VirtualBox
* OS: Debian
* ファイアウォール: UFW
* 強制アクセス制御: AppArmor
* リモート接続: OpenSSH
* 権限管理: sudo
* ストレージ管理: LVM
* 定期実行: cron
* 監視スクリプト: Bash

---

# Debianを選択した理由

Born2beRootではDebianまたはRocky Linuxを選択できる。

今回はDebianを選択した。

主な理由は、

* システム管理初心者でも比較的扱いやすい
* `apt`によるパッケージ管理が分かりやすい
* Debianに関する資料が多い
* AppArmorやUFWなど、この課題で使用する機能を比較的簡単に設定できる
* Born2beRootの課題でも初心者にはDebianが推奨されている

ためである。

---

# DebianとRocky Linuxの比較

## Debian

Debianはコミュニティによって開発されているLinuxディストリビューションである。

パッケージ管理には主に

```bash
apt
```

を使用する。

### 長所

* 安定性を重視している
* パッケージ数が多い
* 情報やドキュメントが豊富
* 初心者でも比較的扱いやすい
* UFWやAppArmorとの組み合わせが分かりやすい

### 短所

* 安定性を優先するため、ソフトウェアのバージョンが最新ではない場合がある
* RHEL系Linuxとは管理方法が異なる

---

## Rocky Linux

Rocky LinuxはRHEL互換を目指して開発されているLinuxディストリビューションである。

主に

```bash
dnf
```

を使用してパッケージを管理する。

### 長所

* RHEL系サーバーの知識を学べる
* エンタープライズ環境に近い構成を経験できる
* SELinuxなど、より詳細なセキュリティ機構を学べる

### 短所

* Debianより設定が複雑になりやすい
* SELinuxやfirewalldについて理解する必要がある

---

# AppArmorとSELinuxの比較

どちらもLinuxの通常のファイル権限とは別に、プログラムが行える操作を制限する仕組みである。

これは「強制アクセス制御」と呼ばれる。

通常のLinux権限だけでは、

```text
このユーザーはこのファイルを読める
```

といった制御を行う。

AppArmorやSELinuxを利用すると、さらに

```text
このプログラムはこのファイルにアクセスしてよい
```

という制御を追加できる。

## AppArmor

DebianではAppArmorを利用する。

AppArmorは主にファイルのパスを基準としてアクセスを制御する。

例:

```text
/usr/sbin/example
```

というプログラムについて、

```text
/etc/example.conf は読んでよい
/important/file は読んではいけない
```

などのルールをプロファイルとして設定できる。

### 特徴

* 比較的設定が分かりやすい
* ファイルパスを基準に考えやすい
* DebianやUbuntuなどで広く利用されている

---

## SELinux

Rocky LinuxではSELinuxを利用する。

SELinuxではファイルやプロセス（実行中のプログラム）に付けられたセキュリティラベル（SELinux が「これは何者か」「何をしてよい対象か」を判断するために、ファイルやプロセスに付ける分類情報）を利用してアクセスを判断する。

例として、Web サーバーのプロセスには「Web サーバーとして動いている」というラベルが付き、Web 用のファイルには「Web が読んでよいファイル」というラベルが付きます。

AppArmor が「このプログラムはこのパスにアクセスしてよいか」を見るのに対して、SELinux は「このラベルのプロセスが、このラベルの対象にアクセスしてよいか」を見ます。

### 特徴

* 非常に細かいアクセス制御ができる
* 大規模なサーバー環境でも使用される
* AppArmorより概念や設定が複雑

---

# UFWとfirewalldの比較

どちらもLinuxでファイアウォールを管理しやすくするための仕組みである。

## UFW

DebianではUFWを使用する。

UFWは

```text
Uncomplicated Firewall
```

の略で、複雑なファイアウォール設定を比較的簡単なコマンドで操作できる。

例えば、

```bash
ufw allow 4242
```

だけで4242番ポートへの通信を許可できる。

Born2beRootのように、

```text
基本的に通信を禁止する
↓
SSH用の4242番ポートだけ許可する
```

という単純な構成に向いている。

---

## firewalld

Rocky Linuxではfirewalldを使用する。

firewalldでは、

```text
public
internal
trusted
```

などの「zone」という単位で通信ルールを管理できる。

UFWより柔軟なネットワーク構成を管理しやすい一方、設定項目も多い。

---

# VirtualBoxとUTMの比較

## VirtualBox

VirtualBoxは仮想マシンを作成・実行するためのソフトウェアである。

ホストOS上に、

```text
仮想CPU
仮想RAM
仮想ディスク
仮想ネットワーク
```

などを作り、その中で別のOSを動作させる。

### 長所

* 多くの環境で利用されている
* GUIからVMの設定を行いやすい
* 仮想ネットワークやポートフォワーディングを設定できる
* `.vdi`形式の仮想ディスクを扱える

---

## UTM

UTMも仮想マシンを実行するためのソフトウェアであり、特にmacOS環境で使用される。

Apple Siliconなど、VirtualBoxを利用できない・利用しにくい環境ではUTMを使用できる。

UTMでは仮想ディスクとして`.qcow2`などが利用される。

---

# Instructions（構築手順）

# 1. DebianのISOを準備する

DebianのISOイメージをダウンロードする。

ISOとは、CDやDVDなどのディスクの内容を1つのファイルとして保存した「ディスクイメージ」である。

今回は、このISOを仮想マシンに仮想的なインストールディスクとして接続し、そこからDebianをインストールする。

---

# 2. VirtualBoxで仮想マシンを作成する

VirtualBoxを起動し、新しい仮想マシンを作成する。

仮想マシンを作成する際には、

* 仮想マシン名
* OSの種類
* メモリ
* 仮想ディスク

などを指定する。

## なぜ仮想マシンを使用するのか

仮想マシンを利用すると、実際のPCのOSを変更せずに、そのPCの中に別のコンピュータを作ることができる。

概念的には、

```text
物理PC
│
├── macOS / Windows / Linux
│
└── VirtualBox
     │
     └── Debian仮想マシン
```

という構造になる。

そのため、Debianの設定を壊してしまっても物理PCそのものへの影響を小さくできる。

---

# 3. ISOをVirtualBoxに接続する

VirtualBoxのStorage設定から、ダウンロードしたDebianのISOファイルを仮想光学ドライブに接続する。

これは実際のPCで、

```text
DebianのインストールDVDをドライブに入れる
```

ことに相当する。

その状態でVMを起動すると、Debianのインストーラーから起動できる。

---

# 4. DebianをGUIなしでインストールする

インストーラーでは

```text
Install
```

を選択する。

`Graphical install`ではなく通常の`Install`を選ぶことで、GUIを必要としないサーバー環境として構築する。

Born2beRootではサーバーを構築するため、X.org、Waylandなどのグラフィカルサーバーをインストールしない。

GUIを入れないことで、

* 使用メモリを減らせる
* 不要なパッケージを減らせる
* 攻撃対象となるソフトウェアを減らせる
* CLIによるLinux管理を学べる

という意味もある。

---

# 5. 言語・地域・キーボードを設定する

Debianインストーラーで、

* 使用言語
* 国・地域
* ロケール
* キーボード配列

を設定する。

ロケールとは、

```text
言語
文字コード
日付表現
数値表現
```

などの地域設定をまとめたものである。

---

# 6. ホスト名を設定する

ホスト名には、

```text
<login>42
```

を設定する。

ホスト名とは、そのコンピュータ自身をネットワーク上で識別するための名前である。

確認する場合は、

```bash
hostname
```

または

```bash
hostnamectl
```

を使用する。

---

# 7. Domain Nameを空欄にする

インストール途中でDomain Nameを聞かれるが、この課題では独自ドメインを構築する必要がないため空欄にする。

ホスト名とドメイン名は別物である。

例えば、

```text
server.example.com
```

なら、

```text
server
```

がホスト名、

```text
example.com
```

がドメイン名に相当する。

---

# 8. rootパスワードを設定する

rootはLinuxにおける最上位権限を持つ管理者ユーザーである。

rootでは、

* ユーザー作成
* パッケージのインストール
* システム設定変更
* サービス管理
* ファイアウォール変更

など、ほぼすべての操作を行える。

そのため、通常作業でrootを使い続けることは危険であり、後ほど一般ユーザーとsudoを利用する。

---

# 9. 一般ユーザーを作成する

rootとは別に、自分のlogin名を持つユーザーを作成する。

通常作業はこの一般ユーザーで行う。

```text
root
↓
システム全体を管理するユーザー

一般ユーザー
↓
普段の作業を行うユーザー
```

と役割を分離することで、誤操作や攻撃による被害を小さくできる。

---

# 10. ディスクをLVMと暗号化を使って構成する

インストール時に、暗号化されたLVMを使用してパーティションを構成する。

## パーティションとは

1つのディスクを論理的に複数の領域へ分割したもの。

例えば、

```text
ディスク
├── /boot
├── /
├── /home
└── swap
```

のように用途を分けることができる。

---

# LVMとは

LVMは

```text
Logical Volume Manager
```

の略である。

通常のパーティションでは、ディスクを直接分割する。

LVMでは、

```text
物理ディスク
↓
Physical Volume
↓
Volume Group
↓
Logical Volume
↓
ファイルシステム
```

という抽象化を行う。

これにより、通常の固定パーティションより柔軟に容量を管理できる。

---

# ディスク暗号化を行う理由

暗号化を行わない場合、仮想ディスクファイルを直接取得されたときに、その中のデータを読み取られる可能性がある。

暗号化しておけば、正しいパスフレーズがなければデータを読み取りにくくできる。

起動時に暗号化パスフレーズを要求されるのはそのためである。

---

# /bootについて

`/boot`には、

* Linuxカーネル
* initramfs
* ブートに必要なファイル

などが置かれる。

OSが暗号化された領域を解除する処理そのものを開始するために必要なファイルが置かれる場所である。

---

# /homeについて

`/home`には一般ユーザーのホームディレクトリが保存される。

例:

```text
/home/<login>
```

システム本体である`/`とユーザーデータである`/home`を分離することで、用途ごとにストレージを管理できる。

---

# swapについて

swapはRAMが不足した場合などに、ディスクの一部を補助的なメモリ領域として利用する仕組みである。

RAMよりディスクは遅いため、RAMそのものの代わりではない。

---

# パーティションを確認する

インストール後に、

```bash
lsblk
```

を実行する。

`lsblk`は

```text
list block devices
```

の意味で、ディスク、パーティション、LVMなどのブロックデバイス構造を表示する。

ここで

```text
disk
part
crypt
lvm
```

などの階層を確認できる。

---

# 11. パッケージマネージャを設定する

DebianではAPTを利用してソフトウェアを管理する。

APTは、

* パッケージの検索
* ダウンロード
* インストール
* 更新
* 依存関係の解決

などを行う。

Debianのミラーサーバーを選択することで、必要なパッケージをネットワーク経由で取得できるようになる。

このプロジェクトでは必要最小限のサーバーを構築するため、不要なデスクトップ環境などはインストールしない。

---

# 12. GRUBをインストールする

GRUB（GRand Unified Bootloader）はブートローダーである。

PCを起動した直後は、まだLinuxカーネルは動いていない。

そこで、

```text
電源ON
↓
ファームウェア
↓
GRUB
↓
Linuxカーネル
↓
Debian
```

という順番でOSを起動する。

GRUBを仮想ディスクへインストールすることで、VirtualBoxがそのディスクからDebianを起動できるようになる。

---

# 13. 初回ログイン

Debianを起動すると、まず暗号化されたディスクを解除するためのパスフレーズを入力する。

その後、

```text
login:
Password:
```

が表示されるので、インストール時に作成した一般ユーザーでログインする。

---

# 14. rootユーザーへ切り替える

必要に応じて、

```bash
su -
```

を使用する。

`su`は

```text
substitute user
```

または

```text
switch user
```

として利用されるコマンドで、別ユーザーへ切り替える。

`-`を付けることで、rootのログイン環境を読み込んだ状態で切り替える。

ただし、最終的には日常的な管理操作を直接rootで行うのではなく、sudoを使用する。（exitで抜けられる）

---

# 15. パッケージ一覧を更新する

```bash
apt update
```

## 意味

`apt update`はソフトウェアそのものを更新するコマンドではない。

APTが参照する

```text
利用可能なパッケージ一覧
```

を最新状態にする。

つまり、

```text
apt update
↓
「現在サーバーにどんなパッケージがあるか」を更新

apt upgrade
↓
実際にインストール済みパッケージを更新
```

という違いがある。

---

# 16. sudoをインストールする

```bash
apt install sudo
```

sudoは、一般ユーザーが一時的に管理者権限でコマンドを実行するための仕組みである。

例えば、

```bash
sudo apt update
```

では、

```text
一般ユーザー
↓
sudoで認証
↓
apt updateだけ管理者権限で実行
↓
一般ユーザーへ戻る
```

という動作になる。

rootでログインし続けるよりも、必要な操作だけ管理者権限にできるため安全性を高められる。

---

# 17. ユーザーを作成し（システムインストール時に自分のユーザーを入力しなかった場合）、user42グループを作成する

```bash
sudo adduser <login>
```

```bash
groupadd user42(addgroup user42)
```

グループとは、複数ユーザーをまとめて権限管理するための仕組みである。

例えば、

```text
user42
├── userA
├── userB
└── userC
```

とすれば、グループ単位でアクセス権を与えることができる。

Born2beRootでは、自分のユーザーを`user42`グループへ所属させる必要がある。

---

# 18. ユーザーをsudoとuser42へ追加する

```bash
usermod -aG sudo,user42 <login>
```

または、

```bash
sudo adduser <username> <groupname>
```

## `usermod`

既存ユーザーの設定を変更するコマンド。

## `-G`

そのユーザーが所属する補助グループを指定する。

## `-a`

append、つまり既存のグループを消さずに追加する。

`-G`だけを不用意に使用すると、現在所属している補助グループが置き換わる可能性があるため、追加する場合は`-aG`を使用する。

---

# グループを確認する

```bash
groups <login>
```

または、

```bash
getent group sudo
getent group user42
```

を使用する。

`getent`（get entries）はシステムが管理しているユーザーやグループなどのデータベースから情報を取得するコマンドである。

---

# 19. SSHをインストールする

```bash
apt install openssh-server
```

SSHは

```text
Secure Shell
```

の略である。

ネットワーク越しに別のコンピュータのシェルへ安全に接続するためのプロトコルである。

例えば、

```text
自分のMac
    │
    │ SSH
    ↓
VirtualBox上のDebian
```

という接続ができる。

通信内容は暗号化される。

確認は以下のコマンド
```bash
sudo service ssh status
```

---

# 20. SSHを4242番ポートへ変更する

SSHサーバーの設定ファイルを開き、次の設定を行う。（VMに入ってくるSSH接続を4242で待つ設定）

```bash
nano /etc/ssh/sshd_config
```

ポート番号を4242に変更
```text
Port 4242
```

SSH経由でのrootログインを無効にする

```text
PermitRootLogin no
```

こちらのファイルも同様にする（VMからどこか別のサーバーへSSH接続するときのデフォルト設定）
```bash
nano /etc/ssh/ssh_config
```

ポート番号を4242に変更
```text
Port 4242
```

SSHサービスを再起動して更新する
```text
sudo service ssh restart
```

サービスの状態を確認する
```text
sudo service ssh status
```

## ポートとは

1台のコンピュータでは複数のネットワークサービスが動作できる。

そこで、

```text
IPアドレス
+
ポート番号
```

によって、どのサービスへ通信するかを区別する。

例えば、

```text
IPアドレス:4242
```

なら、4242番ポートで待機しているサービスへ通信する。

この課題ではSSHを4242番ポートで待ち受けさせる。

---

# 21. SSHによるrootログインを禁止する

`/etc/ssh/sshd_config`で、

```text
PermitRootLogin no
```

を設定する。

rootはシステム上の最高権限を持つ。

SSHからrootへ直接ログインできると、

```text
攻撃者
↓
rootアカウントを直接攻撃
↓
成功した場合、即座に全権限を取得
```

となる。

そこで、

```text
SSH
↓
一般ユーザー
↓
必要な場合だけsudo
```

という構造にする。

suコマンドでrootユーザーに変えることもできるが、攻撃者側からするとrootユーザーだけのパスワードを探せばよかったのが、ユーザーのパスワードとユーザーの名を知る必要が出てくる。さらに、suコマンドでrootに変えるとログが残り、誰が操作したのかが丸わかりになる。

sshd_configとssh_configの関係は以下

sshd_config
= SSHを受け付ける側の設定
= VM内の sshd サーバー設定

ssh_config
= SSHで接続しに行く側の設定
= ssh コマンドのデフォルト設定


---

# 22. SSHサービスを再起動する

設定を変更しただけでは、現在動いているSSHプロセスへ反映されない場合がある。

そのため、

```bash
systemctl restart ssh
```

を実行する。

状態確認は、

```bash
systemctl status ssh
```

で行える。

`systemctl`はsystemdが管理しているサービスを操作するコマンドである。

---

# 23. SSHが4242番ポートで待機していることを確認する

```bash
ss -tulpn
```

などを使用する。

`ss`はソケットの状態を確認するコマンドである。

主なオプションは、

```text
-t  TCP
-u  UDP
-l  LISTEN状態
-p  使用しているプロセス
-n  ポート番号などを数値で表示
```

という意味である。

4242番ポートが`LISTEN`になっていれば、SSHサーバーがそのポートで接続を待っていることを確認できる。

---

# 24. VirtualBoxでポートフォワーディングを設定する

VirtualBoxでNATを利用している場合、ホストPCからゲストVMへSSH接続するためにポートフォワーディングを設定する。（ホストPCの4242番に来た通信を、VMの4242番へ転送する設定をしている。）

ちなみにホストPC、VirtualBox、ゲストVM Debianの関係は以下

```text
ホストPC
└── VirtualBox
    └── ゲストVM Debian
```

例えば、

```text
ホストPCの4242
      ↓
VirtualBox
      ↓
Debian VMの4242
```

という転送を設定する。

これにより、ホスト側から例えば、

```bash
ssh <login>@127.0.0.1 -p 4242
```

のように接続できる。

`-p 4242`は、SSH接続先のポートを4242に指定している。

---

# 25. UFWをインストールする

```bash
apt install ufw
```

ファイアウォールは、

```text
ネットワーク
↓
ファイアウォール
↓
許可された通信だけ通す
↓
サーバー
```

という役割を持つ。

外部から到達できるサービスを必要最小限にすることで、攻撃対象を減らせる。

インストールが完了したら、UFWを有効にする必要がある
```bash
sudo ufw enable
```

---

# 26. SSH用4242番ポートを許可する

```bash
ufw allow 4242/tcp
```

これは、

```text
TCPの4242番ポートへの通信を許可する
```

という意味である。

SSHはTCPを利用する。

---

# 27. UFWを有効化する

```bash
ufw enable
```

ルールを作成しただけではなく、ファイアウォールそのものを有効にする必要がある。

確認する。

```bash
ufw status
```

または、

```bash
ufw status numbered
```

`numbered`を使用するとルール番号も確認できる。

---

# 28. sudoポリシーを設定する

sudoの設定ファイルを作成する。

```bash
touch /etc/sudoers.d/sudo_config
```

`touch`はファイルが存在しなければ新しい空ファイルを作成する。

sudoのログ用ディレクトリも作成する。

```bash
mkdir -p /var/log/sudo
```

`mkdir`はディレクトリを作成するコマンドである。

`-p`を付けると、必要な親ディレクトリも含めて作成でき、既に存在していてもエラーになりにくい。（なくてもできる）

設定ファイルを編集する。

```bash
nano /etc/sudoers.d/sudo_config
```

以下のような設定を行う。

```text
Defaults passwd_tries=3
Defaults badpass_message="Wrong password"
Defaults logfile="/var/log/sudo/sudo_config"
Defaults log_input,log_output
Defaults iolog_dir="/var/log/sudo"
Defaults requiretty
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

---

# passwd_tries=3

```text
Defaults passwd_tries=3
```

sudo実行時にパスワードを間違えられる回数を3回までにする。

無制限に試行できる状態を避けるための設定である。

---

# badpass_message

```text
Defaults badpass_message="Wrong password"
```

sudoのパスワードを間違えた場合に表示するメッセージを指定する。

---

# logfile

```text
Defaults logfile="/var/log/sudo/sudo_config"
```

sudoに関するイベントをログとして保存する場所を指定する。

ログを残すことで、

```text
誰が
いつ
sudoを使ったか
```

などを後から調査しやすくなる。

---

# log_input / log_output

```text
Defaults log_input,log_output
```

sudoで実行された操作について、端末の入力と出力を記録する。

単純に「sudoを使った」という事実だけでなく、操作内容を追跡しやすくする。

---

# iolog_dir

```text
Defaults iolog_dir="/var/log/sudo"
```

sudoの入出力ログを保存するディレクトリを指定する。

---

# requiretty

```text
Defaults requiretty
```

sudoをTTY、つまり端末を通して実行することを要求する。

TTYを必要とすることで、sudoが意図しない非対話的環境から利用される範囲を制限する。

簡単にまとめると以下

TTY = ターミナルとしての入出力口

requiretty = sudo実行時にTTYがあることを要求するsudo設定

目的 = 非対話的・自動的なsudo利用を制限する

---

# secure_path

```text
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

sudo実行時に使用できるコマンド検索パスを限定する。

Linuxでは、

```bash
command
```

を実行すると`PATH`に登録されたディレクトリを順番に検索して実行ファイルを探す。

もし攻撃者が用意した偽のコマンドがPATHの先頭に置かれていると、意図しないプログラムを管理者権限で実行する危険がある。

そこでsudoでは信頼できるディレクトリだけにPATHを制限する。

---

# sudoers設定の確認

sudoersの書式を壊すとsudo自体が利用できなくなる可能性がある。

そのため設定確認には、

```bash
visudo -cf /etc/sudoers.d/sudo_config
```

を利用できる。

`visudo`はsudoersファイルの文法チェックを行うためのコマンドである。

---

# 29. パスワード有効期限を設定する

```bash
nano /etc/login.defs
```

次の値を設定する。

```text
PASS_MAX_DAYS 30
PASS_MIN_DAYS 2
PASS_WARN_AGE 7
```

---

# PASS_MAX_DAYS

```text
PASS_MAX_DAYS 30
```

パスワードを最大30日間使用できる。

30日を超えると変更が必要になる。

---

# PASS_MIN_DAYS

```text
PASS_MIN_DAYS 2
```

パスワード変更後、次の変更まで最低2日必要になる。

例えば、

```text
新しいパスワード
↓
すぐ元のパスワードへ戻す
```

といった方法で履歴ルールを回避しにくくする。

---

# PASS_WARN_AGE

```text
PASS_WARN_AGE 7
```

パスワードの有効期限が切れる7日前から警告する。

---

# 30. libpam-pwqualityをインストールする

```bash
apt install libpam-pwquality
```

`libpam-pwquality`はパスワードの品質を確認するためのPAMモジュールである。

PAMは

```text
Pluggable Authentication Modules
```

の略で、Linuxにおける認証処理を共通化する仕組みである。

---

# 31. パスワード強度を設定する

設定ファイルを開く。

```bash
nano /etc/pam.d/common-password
```

`pam_pwquality.so`に必要なオプションを設定する。

代表的には、

```text
retry=3
minlen=10
ucredit=-1
lcredit=-1
dcredit=-1
maxrepeat=3
reject_username
difok=7
enforce_for_root
```

などを使用する。

---

# minlen=10

```text
minlen=10
```

パスワードを最低10文字にする。

---

# ucredit=-1

```text
ucredit=-1
```

少なくとも1文字の大文字を要求する。

---

# lcredit=-1

```text
lcredit=-1
```

少なくとも1文字の小文字を要求する。

---

# dcredit=-1

```text
dcredit=-1
```

少なくとも1文字の数字を要求する。

---

# maxrepeat=3

```text
maxrepeat=3
```

同じ文字が連続しすぎることを禁止する。

課題では同一文字が3文字を超えて連続しないようにする。

---

# reject_username

```text
reject_username
```

ユーザー名を含むパスワードを拒否する。

例えばユーザー名が、

```text
john
```

なら、

```text
johnPassword123
```

のような推測しやすいパスワードを避けるためである。

---

# difok=7

```text
difok=7
```

以前のパスワードから十分に異なるパスワードを要求する。

Born2beRootでは一般ユーザーについて、以前のパスワードに含まれていなかった文字を少なくとも7文字含めることが要求される。

課題PDFでは、この「前のパスワードとの差」に関する条件はrootには適用されない。

---

# enforce_for_root

```text
enforce_for_root
```

rootについてもパスワード品質チェックを有効にするための設定である。

rootは最も強い権限を持つため、rootのパスワードも強いポリシーに従わせる必要がある。

---

# 32. 既存ユーザーへ有効期限を適用する

`/etc/login.defs`の設定は、既存ユーザーへ自動的にすべて反映されるとは限らない。

そのため`chage`を使用する。

```bash
chage -M 30 -m 2 -W 7 <login>
```

rootについても必要な有効期限を設定する。

```bash
chage -M 30 -m 2 -W 7 root
```

## オプション

```text
-M
```

最大使用日数。

```text
-m
```

最低使用日数。

```text
-W
```

有効期限前の警告日数。

確認する。

```bash
chage -l <login>
```

```bash
chage -l root
```

---

# 33. 設定後にパスワードを変更する

パスワードポリシーを設定した後、既に存在しているアカウントについても新しいルールを満たすパスワードへ変更する。

```bash
passwd <login>
```

rootについては、

```bash
passwd root
```

を使用する。

---

# 34. AppArmorを確認する

DebianではAppArmorが起動時から有効になっている必要がある。

確認には、

```bash
aa-status
```

を使用できる。

また、

```bash
systemctl status apparmor
```

でAppArmorサービスの状態を確認できる。

AppArmorは、通常のLinuxファイル権限だけでは防げない操作について、プログラム単位で追加の制限を与えるために使用する。

---

# 35. monitoring.shを作成する

Bashで、

```text
monitoring.sh
```

というスクリプトを作成する。

このスクリプトではサーバーの状態を取得し、定期的に全端末へ表示する。

表示する情報は、

* OSのアーキテクチャとカーネル
* 物理CPU数
* 仮想CPU数
* RAM使用状況
* ディスク使用状況
* CPU使用率
* 最終起動日時
* LVMの使用状況
* TCP接続数
* ログインユーザー数
* IPv4アドレス
* MACアドレス
* sudo実行回数

である。

---

# monitoring.shで重要な考え方

スクリプトでは、

```bash
command1 | command2
```

のような処理を多く使用する。

`|`はパイプと呼ばれる。

```text
command1の出力
↓
command2の入力
```

として接続する。

例えば、

```bash
grep "processor" /proc/cpuinfo | wc -l
```

なら、

```text
/proc/cpuinfo
↓
processorを含む行だけgrep
↓
wc -lで行数を数える
```

という処理になる。

---

# uname -a

```bash
uname -a
```

OSやカーネルについての情報を取得する。

`-a`は`all`を表し、利用可能な情報をまとめて表示する。

---

# /proc/cpuinfo

```bash
cat /proc/cpuinfo
```

`/proc`は、Linuxカーネルが持つシステム情報をファイルのような形で見せる仮想ファイルシステムである。

`/proc/cpuinfo`にはCPUについての情報が入っている。

例えば、

```bash
grep "processor" /proc/cpuinfo
```

によって仮想CPUの情報を取り出せる。

---

# grep

`grep`は文字列を検索し、条件に一致する行を取り出す。

```bash
grep "processor" /proc/cpuinfo
```

なら、

```text
processor
```

を含む行だけを表示する。

---

# wc -l

```bash
wc -l
```

入力された行数を数える。

そのため、

```bash
grep "processor" /proc/cpuinfo | wc -l
```

とすれば、`processor`に一致した行数から仮想CPU数を数えられる。

---

# free --mega

```bash
free --mega
```

RAMの使用状況を表示する。

`--mega`を付けることでMB系の単位で取得する。

この出力を`awk`で処理して、

```text
使用量
総量
使用率
```

を取り出すことができる。

---

# df

```bash
df
```

ファイルシステムごとのディスク容量や使用量を確認する。

例えば、

```bash
df -m
```

ではMB単位で表示できる。

---

# awk

`awk`は、行を列に分けてデータを加工するのに便利なコマンドである。

例えば、

```bash
free --mega | awk '$1 == "Mem:" {print $2}'
```

では、

1. `free --mega`の結果を取得
2. 先頭列が`Mem:`の行を探す
3. その行の2列目を表示

という処理を行う。

`$1`は1列目、`$2`は2列目を表す。

---

# vmstat

```bash
vmstat
```

CPU、メモリ、プロセス、I/Oなどのシステム統計を確認できる。

CPUのidle値などを利用することでCPU使用率を求められる。

例えば、

```text
CPU使用率 = 100 - idle率
```

という考え方を利用できる。

---

# 最終起動日時

```bash
who -b
```

などでシステムが最後に起動した日時を取得できる。

---

# LVMの確認

```bash
lsblk
```

などからLVMデバイスが存在するかを確認できる。

LVMが使用されていれば、`TYPE`などに`lvm`が表示される。

---

# TCP接続

```bash
ss
```

を利用してネットワーク接続を確認できる。

特に`ESTABLISHED`はTCP接続が確立されている状態を表す。

---

# ログインユーザー

```bash
who
```

や

```bash
users
```

などから現在ログインしているユーザーを確認できる。

---

# IPv4アドレス

```bash
hostname -I
```

などからマシンに割り当てられているIPアドレスを取得できる。

---

# MACアドレス

```bash
ip link
```

などでネットワークインターフェースのMACアドレスを確認できる。

MACアドレスはネットワークインターフェースを識別するためのアドレスである。

---

# sudo実行回数

sudoのログを利用して、sudoが何回実行されたかを数える。

ここでも、

```text
ログを取得
↓
必要な行だけgrep
↓
wc -lで数える
```

というLinuxでよく使用されるパイプ処理を利用できる。

---

# 36. wallで全端末へ送信する

```bash
wall
```

`wall`は

```text
write all
```

に由来するコマンドで、ログインしているユーザーの端末へメッセージを一斉送信する。

例えば、

```bash
echo "hello" | wall
```

なら、

```text
echo
↓
"hello"
↓
パイプ
↓
wall
↓
ログインしている端末へ表示
```

となる。

Born2beRootでは`monitoring.sh`の出力を`wall`へ渡すことで、サーバーの状態を全端末へ表示する。

---

# 37. cronでmonitoring.shを定期実行する

cronはLinuxで処理を指定した時間に自動実行するための仕組みである。

rootのcrontabを編集する場合、

```bash
sudo crontab -e
```

を使用する。

10分ごとに実行する場合は、例えば、

```cron
*/10 * * * * /path/to/monitoring.sh | wall
```

のように設定する。

cronの5つの項目は、

```text
分 時 日 月 曜日
```

を表す。

したがって、

```text
*/10 * * * *
```

は、

```text
分 = 10分ごと
時 = 毎時
日 = 毎日
月 = 毎月
曜日 = 毎曜日
```

という意味になる。

また、課題ではサーバー起動時にも情報を表示する必要があるため、使用している構成に応じて起動時の実行も設定する。

例:

```cron
@reboot /path/to/monitoring.sh | wall
```

---

# cronの確認

```bash
sudo crontab -l
```

を使用すると、現在設定されているrootのcronジョブを確認できる。

---

# monitoring.shを編集せず停止できる理由

monitoring.shそのものに、

```text
10分待つ
↓
実行する
↓
また10分待つ
```

というループが書かれているわけではない。

実行タイミングを管理しているのはcronである。

つまり、

```text
cron
↓
10分ごとにmonitoring.shを起動
```

という構造である。

したがって定期実行を停止したい場合は、スクリプト本体を変更するのではなくcron側を停止・変更すればよい。

---

# 38. signature.txtを作成する

提出前に仮想マシンをシャットダウンする。

仮想ディスクの内容はVMを起動したり変更したりすると変化するため、ハッシュ値も変化する。

VirtualBoxの場合、仮想ディスクは通常、

```text
.vdi
```

ファイルとして保存されている。

macOSでは例えば、

```bash
shasum <machine-name>.vdi
```

を使用する。

Linuxでは、

```bash
sha1sum <machine-name>.vdi
```

を使用できる。

得られたSHA-1値だけを、

```text
signature.txt
```

へ保存する。

---

# SHA-1とは

SHA-1は入力されたデータから固定長の値を計算するハッシュ関数である。

概念的には、

```text
Virtual Disk
      ↓
    SHA-1
      ↓
abcdef1234...
```

となる。

仮想ディスクの中身が少しでも変更されると、基本的に異なるハッシュ値になる。

そのため、

```text
提出時のsignature.txt
```

と

```text
評価時の仮想ディスク
```

が同じものかを確認するために利用される。

---

# signature取得後の注意

signatureを取得した後に元の仮想マシンを起動すると、ログやファイルシステムなどが更新され、`.vdi`の内容が変化する可能性がある。

すると、

```text
signature.txtのSHA-1
≠
現在のVMのSHA-1
```

となる。

評価時にはsignatureが一致している必要があるため注意する。

また、現在の課題では評価開始時に既存のsnapshotが存在してはいけない。

評価用snapshotについては、課題PDFで定められている手順に従う。

---

# 39. 提出物

Gitリポジトリのルートには、

```text
README.md
signature.txt
```

を配置する。

仮想マシン本体や`.vdi`ファイルをGitへアップロードしてはいけない。

---

# セキュリティ設計のまとめ

今回の構成では複数のセキュリティ対策を組み合わせている。

```text
ディスク暗号化
↓
データそのものを保護

強いパスワードポリシー
↓
アカウント認証を強化

一般ユーザー + sudo
↓
root権限の常用を防ぐ

sudoログ
↓
管理者操作を追跡可能にする

SSH rootログイン禁止
↓
ネットワークからrootを直接攻撃できないようにする

SSH 4242番ポート
↓
課題で指定されたSSHサービスの待受設定

UFW
↓
必要な通信以外を制限

AppArmor
↓
プログラム単位のアクセス制御

monitoring.sh
↓
システム状態を可視化

cron
↓
監視処理を自動化
```

1つの対策ですべてを守るのではなく、複数の層でシステムを保護する考え方になっている。

---

# 主な確認コマンド

## OS

```bash
head -n 2 /etc/os-release
```

使用しているLinuxディストリビューションを確認する。

---

## AppArmor

```bash
aa-status
```

AppArmorの状態を確認する。

---

## ホスト名

```bash
hostname
```

または、

```bash
hostnamectl
```

---

## パーティション

```bash
lsblk
```

---

## ユーザー

```bash
getent passwd <login>
```

---

## グループ

```bash
getent group sudo
getent group user42
```

---

## SSH

```bash
systemctl status ssh
```

```bash
ss -tulpn
```

---

## UFW

```bash
ufw status
```

---

## パスワード期限

```bash
chage -l <login>
```

---

## sudoポリシー

```bash
cat /etc/sudoers.d/sudo_config
```

---

## cron

```bash
sudo crontab -l
```

---

# このプロジェクトで理解した重要な概念

Born2beRootを通して、Linuxサーバーは単にOSをインストールすれば完成するものではなく、

```text
OS
+
ユーザー
+
権限
+
ネットワーク
+
ファイアウォール
+
認証
+
ストレージ
+
ログ
+
サービス
+
自動化
```

をそれぞれ適切に設定する必要があることを学んだ。

特に重要なのは、コマンドを暗記するのではなく、

```text
今何を守ろうとしているのか
なぜこの設定が必要なのか
このコマンドはシステムのどこを変更しているのか
```

を理解することである。

---

# Resources（参考資料）

## Born2BeRoot Guide

今回の構築手順を確認する際に使用したガイド。

```text
https://noreply.gitbook.io/born2beroot
```

主に以下の項目を参考にした。

* VirtualBoxの作成
* Debianのインストール
* パーティション設定
* sudo
* ユーザー・グループ管理
* SSH
* UFW
* sudoポリシー
* パスワードポリシー
* monitoring.sh
* cron
* signature.txt

---

## Born2beRoot Subject

42から配布されたBorn2beRootの課題PDFを、最終的な要件確認の基準として使用した。

特に、

* OS
* LVM
* SSH
* UFW
* ユーザー・グループ
* パスワードポリシー
* sudoポリシー
* monitoring.sh
* README
* signature.txt
* snapshot

に関する条件を確認した。

---

## Linuxのマニュアル

コマンドの詳細確認にはLinuxのmanualを利用できる。

例えば、

```bash
man sudo
man sudoers
man ssh
man sshd_config
man ufw
man passwd
man chage
man cron
man crontab
man wall
man lsblk
man free
man df
man grep
man awk
```

`man`はmanualの略で、Linuxコマンドの正式な説明、オプション、設定方法などを確認できる。

---

# Defense / レビュー対策

この章では、Born2beRootのDefenseで確認される内容について、確認方法だけでなく「なぜその設定を行うのか」まで説明する。

---

# 1. Virtual Machine

## 仮想マシンとは何か

仮想マシン（Virtual Machine, VM）とは、物理コンピュータのCPU、RAM、ディスク、ネットワークなどをソフトウェアによって仮想的に再現し、その中で別のOSを動作させる仕組みである。

今回の場合は、

```text
物理PC
│
├── ホストOS
│
├── VirtualBox
│   │
│   └── Debian VM
│       ├── 仮想CPU
│       ├── 仮想RAM
│       ├── 仮想ディスク
│       └── 仮想NIC
```

という構造になっている。

VirtualBoxが物理PCのリソースの一部を仮想ハードウェアとしてDebianに提供し、Debianはそれを通常のコンピュータのハードウェアのように利用する。

---

## 仮想マシンを使用する目的

主な目的は以下である。

* ホストOSとは独立した環境を作れる
* OSを壊しても物理PCへの影響を抑えられる
* 複数のOSを1台のPCで動かせる
* サーバー構築を安全に練習できる
* 同じような環境を再現しやすい
* CPUやRAMなどのリソースをVMごとに分離できる

Born2beRootでは、実際のPCをサーバーへ変更することなく、Linuxサーバー管理を練習するために利用している。

---

# 2. Debianを選んだ理由

今回はDebianを選択した。

理由は、

* 安定性を重視している
* サーバー用途で広く使用されている
* パッケージ管理が比較的分かりやすい
* 情報やドキュメントが多い
* Linuxシステム管理の初心者にも扱いやすい
* Born2beRootでも初心者にはDebianが推奨されている

ためである。

---

# 3. DebianとRocky Linuxの違い

## Debian

Debianはコミュニティ主体で開発されているLinuxディストリビューションである。

主なパッケージ管理:

```bash
apt
```

セキュリティ:

```text
AppArmor
```

ファイアウォール:

```text
UFW
```

---

## Rocky Linux

Rocky LinuxはRHEL互換を目指したLinuxディストリビューションである。

主なパッケージ管理:

```bash
dnf
```

セキュリティ:

```text
SELinux
```

ファイアウォール:

```text
firewalld
```

Debianは比較的扱いやすく、Rocky LinuxはRHEL系サーバーの管理方法を学ぶのに向いている。

---

# 4. apt と aptitude の違い

どちらもDebianでパッケージを管理するためのフロントエンドである。

## apt

例えば、

```bash
sudo apt update
sudo apt install sudo
sudo apt remove package
```

のように使用する。

コマンドラインから簡潔にパッケージ管理を行うことを目的としている。

---

## aptitude

`aptitude`もパッケージ管理を行うツールである。

```bash
aptitude
```

だけで対話型のインターフェースを利用することもできる。

また、依存関係に問題がある場合に複数の解決方法を提示するなど、依存関係の処理に特徴がある。

---

## 簡単に説明すると

レビューでは次のように説明できる。

```text
aptもaptitudeもDebianのパッケージ管理ツールです。

aptは普段のコマンドライン操作に向いたシンプルなツールです。

aptitudeは対話型のインターフェースも持ち、
依存関係の解決方法を提案する機能などがあります。
```

---

# 5. AppArmorとは

AppArmorはLinuxのセキュリティ機能の一つである。

通常のLinuxでは、

```text
ユーザーAはこのファイルを読める
```

というユーザーやグループによる権限制御を行う。

AppArmorではそれに加えて、

```text
このプログラムは
このファイルにはアクセスしてよいが、
こちらのファイルにはアクセスしてはいけない
```

というように、プログラム単位でアクセスを制限できる。

これによって、あるサービスが攻撃された場合でも、そのプログラムがシステム全体へ自由にアクセスすることを防ぎやすくなる。

確認:

```bash
sudo aa-status
```

または、

```bash
systemctl status apparmor
```

---

# 6. GUIが存在しないことを確認する

Born2beRootはサーバー構築課題なのでGUIを使用しない。

GUIを入れない理由は、

* 不要なCPU・RAM消費を減らす
* 不要なパッケージを減らす
* 攻撃対象を減らす
* CLIによるサーバー管理を学ぶ

ためである。

起動時にグラフィカルなデスクトップ環境ではなく、CLIのログイン画面が表示されることを確認する。

---

# 7. OSを確認する

```bash
cat /etc/os-release
```

または、

```bash
head -n 2 /etc/os-release
```

`/etc/os-release`には現在使用しているLinuxディストリビューションの情報が入っている。

---

# 8. User

自分のユーザーが存在することを確認する。

```bash
getent passwd <login>
```

所属グループを確認する。

```bash
groups <login>
```

または、

```bash
id <login>
```

自分のユーザーは、

```text
sudo
user42
```

の両方に所属している必要がある。

---

# 9. 新しいユーザーを作成する

レビューでは新しいユーザーの作成を求められる可能性がある。

```bash
sudo adduser newuser
```

`adduser`は新しいユーザーを作成する。

ユーザー作成時にはBorn2beRootで設定したパスワードポリシーに従ったパスワードを入力する必要がある。

確認:

```bash
getent passwd newuser
```

---

# 10. グループを作成する

例えばレビューで、

```text
evaluating
```

というグループを作るように要求された場合、

```bash
sudo groupadd evaluating
```

を実行する。

確認:

```bash
getent group evaluating
```

---

# 11. ユーザーをグループへ追加する

```bash
sudo usermod -aG evaluating newuser
```

## usermod

既存ユーザーの設定を変更する。

## -G

補助グループを指定する。

## -a

appendの意味で、現在所属しているグループを残したまま追加する。

つまり、

```bash
-aG
```

は、

```text
現在の所属グループを消さずに新しいグループを追加する
```

という意味になる。

確認:

```bash
groups newuser
```

---

# 12. sudoグループへ追加する

```bash
sudo usermod -aG sudo newuser
```

確認:

```bash
groups newuser
```

---

# 13. パスワードポリシー

Born2beRootでは以下のルールを設定している。

```text
最大使用期間: 30日
最低使用期間: 2日
期限切れ警告: 7日前

最低10文字
大文字を含む
小文字を含む
数字を含む
同じ文字を3文字より多く連続させない
ユーザー名を含めない

以前のパスワードと十分に異なるものにする
```

---

# 14. /etc/login.defs

パスワードの有効期限については、

```bash
cat /etc/login.defs
```

で確認できる。

重要な設定:

```text
PASS_MAX_DAYS 30
PASS_MIN_DAYS 2
PASS_WARN_AGE 7
```

## PASS_MAX_DAYS 30

パスワードを最大30日使用できる。

## PASS_MIN_DAYS 2

変更してから最低2日間は再変更できない。

## PASS_WARN_AGE 7

有効期限の7日前から警告する。

---

# 15. PAMによるパスワード強度

パスワードの文字数や複雑さはPAMを利用して制御している。

設定を確認する。

```bash
cat /etc/pam.d/common-password
```

自分の環境で設定した`pam_pwquality`のオプションについて説明できるようにしておく。

代表的には、

```text
minlen
ucredit
lcredit
dcredit
maxrepeat
reject_username
difok
enforce_for_root
```

などを利用する。

---

# 16. 強いパスワードポリシーのメリット

メリット:

* 短いパスワードを防げる
* 単純なパスワードを防げる
* 総当たり攻撃や辞書攻撃への耐性を高められる
* 定期的にパスワードを更新させられる
* ユーザー名など推測しやすいパスワードを防げる

---

# 17. 強いパスワードポリシーのデメリット

デメリット:

* 覚えるのが難しくなる
* 頻繁な変更を要求するとユーザーの負担が増える
* 複雑すぎるルールは、パスワードをメモするなど別の危険な行動につながる可能性がある
* 管理が複雑になる

したがって、

```text
強ければ強いほど常に良い
```

のではなく、安全性と使いやすさのバランスが重要である。

---

# 18. Hostname

現在のhostnameを確認する。

```bash
hostname
```

または、

```bash
hostnamectl
```

Born2beRootでは、

```text
<login>42
```

という形式にする。

---

# 19. hostnameを変更する

例えば、

```text
evaluator42
```

へ変更する場合、

```bash
sudo hostnamectl set-hostname evaluator42
```

を使用できる。

必要に応じて、

```bash
sudo nano /etc/hosts
```

のhostnameに対応している箇所も変更する。

その後、

```bash
sudo reboot
```

する。

再起動後、

```bash
hostname
```

で確認する。

終了後は同じ手順で元のhostnameへ戻す。

---

# 20. Partitionを確認する

```bash
lsblk
```

`lsblk`は、

```text
list block devices
```

の意味で、ディスク、パーティション、暗号化領域、LVMなどを階層構造で表示する。

例えば、

```text
disk
└── part
    └── crypt
        └── lvm
```

のような構造を確認できる。

---

# 21. LVMとは

LVMは、

```text
Logical Volume Manager
```

の略である。

通常の固定パーティションを直接利用する代わりに、

```text
物理ディスク
↓
PV
↓
VG
↓
LV
↓
ファイルシステム
```

という構造で管理する。

---

## PV

```text
Physical Volume
```

LVMで使用する物理ディスクやパーティション。

---

## VG

```text
Volume Group
```

複数のPVをまとめたストレージプール。

---

## LV

```text
Logical Volume
```

VGから必要な容量を切り出して作る論理的なディスク。

---

## LVMのメリット

通常のパーティションより柔軟に、

* 容量を管理できる
* 論理ボリュームを追加できる
* サイズ変更がしやすい

という特徴がある。

簡単に説明するなら、

```text
通常のpartitionはディスクを直接区切ります。

LVMでは一度ストレージをプールとしてまとめ、
そこからLogical Volumeを作ります。

そのため通常の固定partitionより柔軟に容量を管理できます。
```

---

# 22. sudoとは

`sudo`は一般ユーザーが特定のコマンドだけを一時的に管理者権限で実行する仕組みである。

例えば、

```bash
sudo apt update
```

では、

```text
一般ユーザー
↓
sudoで本人確認
↓
apt updateだけroot権限で実行
↓
一般ユーザーへ戻る
```

という動作になる。

---

# 23. rootを常用せずsudoを使う理由

rootではすべての操作が可能である。

そのためrootを常時使用すると、

```text
コマンドを間違える
↓
即座にシステム全体へ影響
```

する可能性がある。

sudoを使用すれば、

* 必要な操作だけroot権限で実行できる
* 誰がsudoを使用したかログを残せる
* rootパスワードを複数人で共有する必要がない
* 誤操作による被害を減らせる

というメリットがある。

---

# 24. sudoがインストールされているか確認する

```bash
which sudo
```

または、

```bash
sudo --version
```

---

# 25. sudo設定を確認する

自分が作成した設定ファイルを確認する。

```bash
cat /etc/sudoers.d/sudo_config
```

主な設定:

```text
passwd_tries=3
badpass_message
logfile
log_input
log_output
requiretty
secure_path
```

---

# 26. sudoの試行回数

```text
Defaults passwd_tries=3
```

パスワードを間違えたときの試行回数を3回までにする。

---

# 27. badpass_message

sudoのパスワードを間違えた場合のメッセージを設定する。

---

# 28. sudoログ

sudoで行った操作は、

```text
/var/log/sudo/
```

へ保存する。

確認:

```bash
sudo ls -la /var/log/sudo/
```

レビューでは、まず現在のログを確認してから、

```bash
sudo ls
```

などを実行する。

その後、

```bash
sudo ls -la /var/log/sudo/
```

をもう一度実行して、ログが更新されていることを確認する。

ログを残す理由は、

```text
誰が
何を
いつ
実行したのか
```

を後から確認できるようにするためである。

---

# 29. requiretty

```text
Defaults requiretty
```

sudoを端末から実行することを要求する。

意図しない非対話的な方法でsudoを利用される可能性を制限する目的がある。

---

# 30. secure_path

sudoで利用するPATHを信頼できるディレクトリだけに制限する。

例えば、

```text
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
/sbin
/bin
```

などである。

PATHを制限することで、攻撃者が用意した偽のコマンドをroot権限で実行してしまう危険を減らす。

---

# 31. UFWとは

UFWは、

```text
Uncomplicated Firewall
```

の略である。

Linuxのファイアウォールを簡単に設定するためのツールである。

ファイアウォールは、

```text
外部ネットワーク
↓
Firewall
↓
許可された通信だけ通す
↓
Server
```

という役割を持つ。

不要なポートを閉じることで、外部から攻撃可能なサービスを減らす。

---

# 32. UFWを確認する

```bash
sudo ufw status
```

詳細に確認する場合、

```bash
sudo ufw status numbered
```

4242番ポートが許可されていることを確認する。

---

# 33. 8080番ポートを追加する

レビューでは新しいルールを追加するよう要求される可能性がある。

```bash
sudo ufw allow 8080
```

確認:

```bash
sudo ufw status numbered
```

---

# 34. 8080番ルールを削除する

```bash
sudo ufw delete allow 8080
```

確認:

```bash
sudo ufw status numbered
```

---

# 35. SSHとは

SSHは、

```text
Secure Shell
```

の略である。

ネットワーク越しに別のコンピュータへ安全にログインし、コマンドを実行するためのプロトコルである。

通信内容は暗号化される。

```text
自分のPC
   │
   │ SSH
   ↓
Debian Server
```

という形で利用できる。

---

# 36. SSHのメリット

SSHを使うことで、

* サーバーへ物理的に移動しなくても操作できる
* 通信内容を暗号化できる
* リモートからサーバーを管理できる
* パスワード認証や公開鍵認証を利用できる

というメリットがある。

---

# 37. SSHサービスを確認する

```bash
systemctl status ssh
```

`active (running)`になっていることを確認する。

---

# 38. SSHが4242番で待機しているか確認する

```bash
sudo ss -tulpn
```

または、

```bash
sudo ss -tulpn | grep 4242
```

4242番ポートが、

```text
LISTEN
```

になっていることを確認する。

---

# 39. ssのオプション

```text
-t : TCP
-u : UDP
-l : LISTEN状態
-p : 使用しているプロセス
-n : ポート番号などを数字で表示
```

---

# 40. SSH設定

```bash
cat /etc/ssh/sshd_config
```

重要な設定:

```text
Port 4242
PermitRootLogin no
```

---

# 41. rootでSSHできない理由

rootはシステム上の最高権限を持つ。

もしrootへSSHで直接ログインできると、

```text
攻撃者
↓
rootアカウントを直接攻撃
↓
成功
↓
即座にシステム全体を操作可能
```

となる。

そこで、

```text
SSH
↓
一般ユーザー
↓
必要な操作だけsudo
```

という構成にしている。

---

# 42. SSHで新しく作ったユーザーへ接続する

接続方法はVirtualBoxのネットワーク設定によって異なる。

例えばホスト側の4242番をVMの4242番へ転送している場合、

```bash
ssh newuser@127.0.0.1 -p 4242
```

のように接続できる。

`-p 4242`は接続先のSSHポートを4242番に指定している。

---

# 43. monitoring.sh

Born2beRootではBashで`monitoring.sh`を作成し、サーバーの状態を定期的に表示する。

表示する情報:

```text
Architecture
Physical CPU
vCPU
Memory Usage
Disk Usage
CPU load
Last boot
LVM use
TCP Connections
User log
Network
Sudo
```

---

# 44. monitoring.shを説明するときの基本

レビューでは、コードを上から、

```text
① 何の情報を取得しているか
② どのコマンドで取得しているか
③ パイプでどう加工しているか
④ 最後にどのように表示しているか
```

の順番で説明する。

---

# 45. uname -a

```bash
uname -a
```

OSのアーキテクチャやカーネルなどの情報を表示する。

`-a`は、

```text
all
```

を意味し、利用可能な情報をまとめて表示する。

---

# 46. /proc/cpuinfo

```bash
cat /proc/cpuinfo
```

CPUについての情報を取得できる。

`/proc`はLinuxカーネルが持っている情報を、ファイルのような形式で参照できる仮想ファイルシステムである。

---

# 47. grep

例えば、

```bash
grep "processor" /proc/cpuinfo
```

は、

```text
processor
```

を含む行だけを抽出する。

---

# 48. wc -l

```bash
wc -l
```

入力された行数を数える。

そのため、

```bash
grep "processor" /proc/cpuinfo | wc -l
```

なら、

```text
processorの行を探す
↓
その行数を数える
```

という処理になる。

---

# 49. Pipe

```text
|
```

はパイプである。

左のコマンドの標準出力を、右のコマンドの標準入力へ渡す。

例えば、

```bash
grep "processor" /proc/cpuinfo | wc -l
```

なら、

```text
grepの結果
↓
pipe
↓
wc -l
```

という処理になる。

Linuxでは複数の小さなコマンドをパイプで組み合わせて、大きな処理を作ることができる。

---

# 50. free

```bash
free --mega
```

RAMの使用状況を表示する。

ここから、

```text
総RAM
使用RAM
使用率
```

を取得できる。

---

# 51. awk

`awk`は文字列を行や列に分けて処理するためのツールである。

例えば、

```bash
free --mega | awk '$1 == "Mem:" {print $2}'
```

なら、

```text
free --megaを実行
↓
1列目がMem:の行を探す
↓
2列目を表示する
```

という処理になる。

`awk`では、

```text
$1 = 1列目
$2 = 2列目
$3 = 3列目
```

を表す。

---

# 52. df

```bash
df
```

ディスクの使用状況を表示する。

ここから、

```text
総容量
使用容量
使用率
```

などを取得する。

---

# 53. CPU Usage

CPU使用率を取得するときには、CPUのidle率などを利用できる。

考え方は、

```text
CPU Usage = 100 - idle
```

である。

idleはCPUが何も処理していない割合である。

---

# 54. Last boot

最後にサーバーが起動した時刻を取得する。

例えば、

```bash
who -b
```

を利用できる。

`-b`は最後のboot時刻を表示する。

---

# 55. LVM use

`lsblk`などを利用して、

```text
lvm
```

として認識されているデバイスが存在するか確認する。

---

# 56. TCP Connections

```bash
ss
```

を利用して現在のTCP接続を確認する。

特に、

```text
ESTABLISHED
```

はTCP接続が確立している状態を意味する。

---

# 57. User log

```bash
who
```

などで現在ログインしているユーザーを確認できる。

---

# 58. IPv4 address

```bash
hostname -I
```

などからIPアドレスを取得できる。

IPアドレスはネットワーク上でコンピュータを識別するためのアドレスである。

---

# 59. MAC address

```bash
ip link
```

などでネットワークインターフェースのMACアドレスを確認できる。

MACアドレスはネットワークインターフェースを識別するアドレスである。

---

# 60. sudo実行回数

sudoに関するログを取得し、

```bash
grep
```

などで必要な行を抽出して、

```bash
wc -l
```

で行数を数えることでsudoの実行回数を求める。

---

# 61. wallとは

`wall`はログインしている端末へメッセージを一斉送信するためのコマンドである。

例えば、

```bash
echo "hello" | wall
```

なら、

```text
echo
↓
hello
↓
pipe
↓
wall
↓
各terminal
```

となる。

monitoring.shの結果も`wall`を利用して端末へ送信する。

---

# 62. cronとは

cronはLinuxで、

```text
決められた時刻
または
一定のスケジュール
```

でコマンドを自動実行する仕組みである。

cronの設定は、

```text
crontab
```

に記述する。

確認:

```bash
sudo crontab -l
```

編集:

```bash
sudo crontab -e
```

---

# 63. crontabの5項目

cronでは、

```text
分 時 日 月 曜日
```

の5つを指定する。

例えば、

```cron
*/10 * * * * command
```

なら、minuteフィールドが10分間隔になっている。

```text
00分
10分
20分
30分
40分
50分
```

に実行される。

---

# 64. 10分ごとにmonitoring.shを実行する

自分の実際のスクリプトの保存場所に合わせて設定する。

例:

```cron
*/10 * * * * /path/to/monitoring.sh | /usr/bin/wall
```

また、起動時にも表示させる構成なら、

```cron
@reboot /path/to/monitoring.sh | /usr/bin/wall
```

を利用できる。

---

# 65. Defense中に1分ごとへ変更する

Correction sheetでは、10分待たずに動作確認するため、Defense中に1分ごとへ変更することがある。

crontabを開く。

```bash
sudo crontab -e
```

例えば、

```cron
*/10 * * * * /path/to/monitoring.sh | /usr/bin/wall
```

を一時的に、

```cron
* * * * * /path/to/monitoring.sh | /usr/bin/wall
```

へ変更する。

これは、

```text
毎分実行
```

という意味である。

確認後は10分ごとの設定へ戻す。

---

# 66. dynamic valuesとは何か

Correction sheetではmonitoring.shの値が動的に変化するか確認される。

例えば、

```text
CPU Usage
Memory Usage
TCP Connections
User log
sudo count
```

などはサーバーの状態によって変わる。

スクリプトの中へ、

```text
CPU Usage = 5%
```

などと固定値を書いてはいけない。

毎回Linuxから現在の状態を取得する必要がある。

---

# 67. monitoring.shを変更せず停止する

monitoring.sh自身が10分ごとに動いているのではない。

実行しているのは、

```text
cron
↓
monitoring.sh
```

という構造である。

そのためスクリプトを編集しなくても、cronを停止すれば定期実行を停止できる。

```bash
sudo systemctl stop cron
```

状態確認:

```bash
systemctl status cron
```

再開:

```bash
sudo systemctl start cron
```

重要なのは、

```text
monitoring.shを変更した
```

のではなく、

```text
monitoring.shを実行しているcron側を停止した
```

という点である。

---

# 68. cronを再起動後にも動作させる

cronがboot時に起動する設定を確認する。

```bash
systemctl is-enabled cron
```

例えば、

```text
enabled
```

なら、システム起動時にcronも起動する。

状態確認:

```bash
systemctl status cron
```

---

# 69. monitoring.shの権限を確認する

```bash
ls -l /path/to/monitoring.sh
```

例えば、

```text
-rwxr-xr-x
```

などが表示される。

`x`は実行権限を表す。

---

# 70. chmodとは

実行権限を付ける場合、

```bash
chmod +x monitoring.sh
```

を利用できる。

`chmod`は、

```text
change mode
```

で、ファイルのpermissionを変更するコマンドである。

---

# 71. reboot後の確認

レビューの最後に再起動した場合、

```bash
sudo reboot
```

再起動後に、

```bash
ls -l /path/to/monitoring.sh
```

を実行する。

ここで、

* monitoring.shが同じ場所にある
* 内容が変更されていない
* permissionが変わっていない
* cronが動作している
* monitoring.shが再び表示される

ことを確認する。

---

# 72. signature.txt

VMを起動する前に、提出した`signature.txt`と仮想ディスクのSHA-1が一致している必要がある。

Linux:

```bash
sha1sum <VM>.vdi
```

macOS:

```bash
shasum <VM>.vdi
```

得られた値と、

```bash
cat signature.txt
```

の値を比較する。

---

# 73. SHA-1を使う理由

仮想ディスクの内容が変更されるとハッシュ値も変化する。

そのため、

```text
提出時の仮想ディスク
```

と、

```text
評価対象の仮想ディスク
```

が同一であるか確認するために利用される。

---

# Defense直前確認用コマンド

以下を順番に実行できるようにしておく。

```bash
# OS
cat /etc/os-release

# AppArmor
sudo aa-status

# hostname
hostname
hostnamectl

# partition
lsblk

# user
id <login>
groups <login>

# group
getent group sudo
getent group user42

# password
sudo cat /etc/login.defs
sudo cat /etc/pam.d/common-password
chage -l <login>

# sudo
which sudo
sudo cat /etc/sudoers.d/sudo_config
sudo ls -la /var/log/sudo/

# UFW
sudo ufw status numbered

# SSH
systemctl status ssh
sudo ss -tulpn | grep 4242

# cron
systemctl status cron
sudo crontab -l

# monitoring
ls -l /path/to/monitoring.sh

# system information
uname -a
```

---

# Defenseで最低限口頭で言えるようにすること

## VM

```text
VirtualBoxが物理PCのCPU、RAM、diskなどを仮想化して、
その仮想hardware上でDebianを動かしています。
ホストOSとは独立した環境を安全に作れるのがメリットです。
```

## Debian

```text
安定していて、サーバー用途に向いており、
aptによるpackage管理も比較的分かりやすいためDebianを選びました。
```

## AppArmor

```text
AppArmorはプログラムごとにアクセスできるresourceを制限する
Linuxのsecurity機能です。
通常のuser permissionに追加して制限できます。
```

## sudo

```text
sudoは一般userが必要なcommandだけ一時的にroot権限で実行する仕組みです。
rootを常用するより安全で、操作をlogに残せるメリットもあります。
```

## UFW

```text
UFWはLinux firewallを簡単に管理するためのtoolです。
不要なportへの通信を遮断し、
このprojectではSSHに必要な4242番portだけを許可しています。
```

## SSH

```text
SSHはnetwork経由で別のcomputerへ安全にloginするprotocolです。
通信は暗号化されます。
このprojectでは4242番portを使用し、rootの直接loginは禁止しています。
```

## LVM

```text
LVMはdiskをPV、VG、LVというlayerで管理する仕組みです。
通常の固定partitionより柔軟にstorage容量を管理できます。
```

## cron

```text
cronは指定したscheduleでcommandを自動実行する仕組みです。
monitoring.sh自身が10分を数えているのではなく、
cronがmonitoring.shを定期的に起動しています。
```

## wall

```text
wallはloginしているterminalへmessageを一斉送信するcommandです。
monitoring.shの結果をwallへ渡して各terminalへ表示しています。
```

## monitoring.sh

```text
monitoring.shはLinuxのcommandから毎回現在のsystem状態を取得し、
grep、awk、wcなどで必要な情報へ加工して、
最後にwallを使って全terminalへ表示します。
値は固定ではなく、その時点のserver状態から取得しています。
```


# AIの使用について

AIは、本READMEを日本語で整理する際に使用した。

主に、

* 各コマンドの役割を文章として整理する
* 「なぜその設定を行うのか」を言語化する
* READMEの構成を整理する
* Debian、Rocky Linux、AppArmor、SELinux、UFW、firewalld、VirtualBox、UTMの違いを整理する
* 説明が不足している箇所を確認する

ために利用した。

一方で、プロジェクトの最終的な要件については42から配布された課題PDFを基準とし、実際の設定については仮想マシン上のコマンドと設定ファイルを確認することを重視した。
