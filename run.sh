#!/bin/bash

# 保存元の作業ディレクトリ（key.jsonのある場所）
ORIGIN_DIR="$(pwd)"

# ディレクトリ作成
[ -d "$HOME/.tools/java2uml" ] || mkdir -p "$HOME/.tools/java2uml"

# .toolsへ移動
cd "$HOME/.tools/"
rm -fr java2uml

# リポジトリをクローン
git clone https://github.com/Courbet14/java2uml.git > /dev/null 2>&1

# key.json をコピー（元のディレクトリから）
#cp "$ORIGIN_DIR/key.json" "$HOME/.tools/java2uml/key.json"
# セットアップ実行
cd java2uml
chmod +x setup.sh
./setup.sh
