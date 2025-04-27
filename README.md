# MySQL連携編

この教材では、AI Agentの会話履歴やユーザー情報をMySQLデータベースに保存・取得する方法を学びます。

## 学習内容

- MySQLデータベースのセットアップ
- Python（FastAPI）からMySQLへの接続
- 会話ログの保存・取得
- ユーザーごとの履歴管理
- Docker ComposeによるDBコンテナの統合

### プロジェクト構成

```
.
├── app/
│   ├── main.py                   # FastAPIアプリケーション
│   ├── message_repository.py     # FastAPIアプリケーション
│   └── ai_response_generator.py  # AI応答生成クラス
├── mysql/
│   ├── my.cnf                    # MySQL設定ファイル
│   └── db/user_messages.sql      # テーブル定義(DDL)
├── config.py                     # 設定ファイル
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```


## MySQL連携のポイント

- `CuriosityLogRepository.py`でDB接続・クエリ実行を管理
- 会話ごとに`curiosity_log`テーブルへINSERT
- ユーザーIDごとに履歴を取得し、AI応答生成に活用
- DB接続情報は`app/config.py`で管理

## セットアップ手順

1. **リポジトリのクローン**
    ```bash
    git clone https://github.com/dx-junkyard/ai-agent-playground.git
    cd ai-agent-playground
    ```

2. **MySQLの初期化**
    - `mysql/db/curiosity_log.sql`でテーブル作成
    - docker compose起動時に自動で初期化されます

3. **設定ファイルの編集**
    - `app/config.py`でDB接続情報を確認・必要に応じて修正

4. **コンテナの起動**
    ```bash
    docker compose up -d
    ```

## APIの使い方

### 会話メッセージの送信・保存

```bash
curl http://localhost:8086/api/v1/user-message \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "message": "こんにちは！"
  }'
```
- 送信したメッセージはMySQLの`user_messages`テーブルに保存されます

### 履歴の取得（例）

- ユーザーIDごとの履歴取得や、最新メッセージの取得APIも実装例として含まれています（詳細は`message_repository.py`参照）

