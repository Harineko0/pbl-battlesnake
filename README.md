# Battlesnake Python Starter Project

Git の使い方
```bash
# リポジトリをローカルにクローン
git clone https://github.com/Harineko0/pbl-battlesnake

# リポジトリに変更を加える
git checkout -b feat/変更したい内容を端的に表した言葉 ## 例: git checkout -b feat/customize-snake

# ファイルを追加した後
git add -A

# 変更を確定するとき
git commit -am "コミットメッセージ" # 例: git commit -am "MODIFY :ヘビの色を緑に変更"

# 変更を GitHub にアップロードするとき
git push origin HEAD

# 1. https://github.com/Harineko0/pbl-battlesnake/pulls の New pull request ボタンをクリックし, Pull Request を作成する
# 2. Slack で誰かにレビューを依頼する
# 3. Pull Request のページ下部からマージする
```

```bash
# setup venv
python3 -m venv "battlesnake"
./battlesnake/Scripts/activate
pip install -r .\requirements.txt
python main.py

# Copy battlesnake.exe to this directory
./battlesnake.exe play -W 11 -H 11 --name 'PBL 7' --url http://localhost:8000 -g solo --browser
```

## Getting Started

An official Battlesnake template written in Python. Get started at [play.battlesnake.com](https://play.battlesnake.com).

![Battlesnake Logo](https://media.battlesnake.com/social/StarterSnakeGitHubRepos_Python.png)

This project is a great starting point for anyone wanting to program their first Battlesnake in Python. It can be run locally or easily deployed to a cloud provider of your choosing. See the [Battlesnake API Docs](https://docs.battlesnake.com/api) for more detail. 

[![Run on Replit](https://repl.it/badge/github/BattlesnakeOfficial/starter-snake-python)](https://replit.com/@Battlesnake/starter-snake-python)

## Technologies Used

This project uses [Python 3](https://www.python.org/) and [Flask](https://flask.palletsprojects.com/). It also comes with an optional [Dockerfile](https://docs.docker.com/engine/reference/builder/) to help with deployment.

## Run Your Battlesnake

Install dependencies using pip

```sh
pip install -r requirements.txt
```

Start your Battlesnake

```sh
python main.py
```

You should see the following output once it is running

```sh
Running your Battlesnake at http://0.0.0.0:8000
 * Serving Flask app 'My Battlesnake'
 * Debug mode: off
```

Open [localhost:8000](http://localhost:8000) in your browser and you should see

```json
{"apiversion":"1","author":"","color":"#888888","head":"default","tail":"default"}
```

## Play a Game Locally

Install the [Battlesnake CLI](https://github.com/BattlesnakeOfficial/rules/tree/main/cli)
* You can [download compiled binaries here](https://github.com/BattlesnakeOfficial/rules/releases)
* or [install as a go package](https://github.com/BattlesnakeOfficial/rules/tree/main/cli#installation) (requires Go 1.18 or higher)

Command to run a local game

```sh
battlesnake play -W 11 -H 11 --name 'Python Starter Project' --url http://localhost:8000 -g solo --browser
```

## Next Steps

Continue with the [Battlesnake Quickstart Guide](https://docs.battlesnake.com/quickstart) to customize and improve your Battlesnake's behavior.

**Note:** To play games on [play.battlesnake.com](https://play.battlesnake.com) you'll need to deploy your Battlesnake to a live web server OR use a port forwarding tool like [ngrok](https://ngrok.com/) to access your server locally.
