# COFFEE-API

## 起動手順 (PostgreSQL 前提)
1. PostgreSQL を localhost:5432 で起動し、接続先 DB・ユーザー・パスワードを作成する。
2. 環境変数 `DATABASE_URL` を設定する（例）:
   - PowerShell: `$env:DATABASE_URL="postgresql://<user>:<password>@<host>:<port>/<database>"`
   - cmd.exe: `set DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>`
3. 依存パッケージをインストールする: `pip install -r requirements.txt` (必要に応じて venv を使用)。
4. 初期データ投入: `python seed.py`
5. 開発サーバー起動: `uvicorn main:app --reload`

`DATABASE_URL` を指定しなかった場合は `postgresql://user:password@localhost:5432/coffee` が使われます。実在する DB 名・ユーザー・パスワードに合わせて設定してください。
