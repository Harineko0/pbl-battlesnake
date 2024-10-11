![image](https://github.com/user-attachments/assets/a43274bd-7fb0-41a4-b688-756c796d9fc1)# Git / GitHub Usage
## 初回のみ
```bash
# リポジトリをローカルにクローン
git clone https://github.com/Harineko0/pbl-battlesnake
```

## 変更を加えるとき
リポジトリのディレクトリ内で
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

## main ブランチにマージするとき
1. **Pull Request** のタブをクリック > **New pull request** をクリック
   ![image](https://github.com/user-attachments/assets/12f3a275-8c84-470c-b464-ead648a2c448)
2. compare をクリックし, マージしたいブランチを選択 (base がマージする対象のブランチ) > **Create pull request**
   ![image](https://github.com/user-attachments/assets/1e8379ec-e686-4204-b150-ece7c59bfbba)
3. Title, Description を記入して **Create pull request**
   ![image](https://github.com/user-attachments/assets/270874dd-f806-43d4-8671-9130f86f74c1)
4. PR ページのリンクを Slack で共有し, レビューを依頼 (例: https://github.com/Harineko0/pbl-battlesnake/pull/3)
   ![image](https://github.com/user-attachments/assets/26cbe7f8-694d-4b94-b64d-80fc8d71bf7f)
5. レビューが終わったら **Merge pull request** でマージ
