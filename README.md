# AI Agent 開発講座（MySQL連携編 - Windows対応版）

この教材では、AI Agentの会話履歴やユーザー情報をMySQLデータベースに保存・取得する方法を学びます。このブランチはWindows環境での実行に最適化されています。

## 学習内容

- MySQLデータベースのセットアップ
- Python（FastAPI）からMySQLへの接続
- 会話ログの保存・取得
- ユーザーごとの履歴管理
- Docker ComposeによるDBコンテナの統合

## プロジェクト構成

```
.
├── app/
│   ├── main.py                   # FastAPIアプリケーション（エンドポイント定義）
│   ├── message_repository.py     # メッセージ保存・取得用リポジトリクラス
│   └── ai_response_generator.py  # AI応答生成クラス（LLMとの連携）
├── mysql/
│   ├── my.cnf                    # MySQL設定ファイル
│   └── db/user_messages.sql      # テーブル定義(DDL)
├── config.py                     # 設定ファイル（DB接続情報など）
├── Dockerfile                    # Dockerイメージ定義
├── docker-compose.yml            # Docker Compose設定（APIとMySQLコンテナ）
├── api_test.sh                   # APIテスト用スクリプト
├── db_connect.sh                 # DB接続確認用スクリプト
└── requirements.txt              # Pythonパッケージ依存関係
```

## Windows環境での実装ポイント

- `docker-compose.yml`からplatform指定を削除し、Windows環境でも動作するように調整
- コマンド例はWindows環境（コマンドプロンプト/PowerShell）で実行できる形式で記載
- `message_repository.py`でDB接続・クエリ実行を管理
- 会話ごとに`user_messages`テーブルへINSERT
- ユーザーIDごとに履歴を取得し、AI応答生成に活用
- DB接続情報は`config.py`で管理

## データベース設計

```sql
CREATE TABLE user_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## セットアップ手順

1. **リポジトリのクローン**
    ```
    git clone -b mysql-integration-win https://github.com/dx-junkyard/ai-agent-playground.git
    cd ai-agent-playground
    ```

2. **MySQLの初期化**
    - `mysql/db/user_messages.sql`でテーブル作成
    - docker compose起動時に自動で初期化されます

3. **設定ファイルの編集**
    - `config.py`でDB接続情報を確認・必要に応じて修正
    ```python
    # MySQL接続情報
    DB_HOST = "db"  # Dockerコンテナ名
    DB_PORT = 3306
    DB_USER = "me"
    DB_PASSWORD = "me"
    DB_NAME = "mydb"
    ```

4. **コンテナの起動**
    ```
    # Windows環境
    docker compose up -d
    
    # Linux/Mac環境
    docker compose up
    ```

## APIの使い方

### 会話メッセージの送信・保存（コマンドプロンプト）

```
curl http://localhost:8086/api/v1/user-message ^
  -X POST ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"こんにちは！\"}"
```

### 会話メッセージの送信・保存（PowerShell）

```powershell
curl http://localhost:8086/api/v1/user-message `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body "{\"message\":\"こんにちは！\"}"
```

- 送信したメッセージはMySQLの`user_messages`テーブルに保存されます
- AIの応答も同様に保存されます

### 履歴の取得（コマンドプロンプト）

```
curl "http://localhost:8086/api/v1/user-messages?user_id=me&limit=10"
```

### 履歴の取得（PowerShell）

```powershell
curl "http://localhost:8086/api/v1/user-messages?user_id=me&limit=10"
```

- ユーザー"me"の発言履歴を最大10件取得します
- レスポンス例：
```json
[
  {
    "id": 1,
    "user_id": "me",
    "message": "こんにちは！",
    "created_at": "2025-05-19T00:30:00"
  },
  {
    "id": 2,
    "user_id": "ai",
    "message": "こんにちは！どのようにお手伝いできますか？",
    "created_at": "2025-05-19T00:30:01"
  }
]
```

### データベースへの直接接続（Docker経由）

```
docker exec -it my_mysql mysql --default-character-set=utf8 -u me -p mydb
# パスワード: me
```

接続後、以下のコマンドでデータを確認できます：
```sql
show tables;
select * from user_messages;
```

## 次のステップ

MySQL連携編を完了したら、以下の応用編に進むことができます：

- UI連携編: StreamlitによるWebインターフェースの実装
