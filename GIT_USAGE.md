# Git / GitHub Usage
## 初回のみ
```bash
# リポジトリをローカルにクローン
git clone https://github.com/Harineko0/pbl-battlesnake
```

## 変更を加えるとき
```bash
# ブランチを切る
git checkout -b feat/変更したい内容を端的に表した言葉 # 例: git checkout -b feat/customize-snake

# ファイルを追加した場合に実行
git add -A

# 変更を確定する
git commit -am "コミットメッセージ" # 例: git commit -am "MODIFY :ヘビの色を緑に変更"

# 変更を GitHub に push (アップロード) する
git push origin HEAD
```
