# UI編

このプロジェクトは、AIエージェントと対話するためのWebアプリケーションです。FastAPIバックエンドとStreamlitフロントエンドで構成されています。

## プロジェクト構成

```
.
├── app/
│   ├── api/                    # FastAPIバックエンド
│   │   ├── main.py            # メインAPIエンドポイント
│   │   ├── ai_response_generator.py  # AI応答生成ロジック
│   │   └── message_repository.py     # メッセージ保存ロジック
│   └── ui/                    # Streamlitフロントエンド
│       └── ui.py              # UIアプリケーション
├── config.py                  # 設定ファイル
├── requirements.api.txt       # API依存関係
├── requirements.ui.txt        # UI依存関係
├── Dockerfile.api            # API用Dockerfile
├── Dockerfile.ui             # UI用Dockerfile
└── docker-compose.yaml       # Docker Compose設定
```

## セットアップ

### 前提条件

- Docker
- Docker Compose

## セットアップ手順

1. **リポジトリのクローン**
    ```bash
    git clone -b ui-integration https://github.com/dx-junkyard/ai-agent-playground.git
    cd ai-agent-playground
    ```


3. Dockerコンテナのビルドと起動:
```bash
docker-compose build
docker-compose up
```

4. アプリケーションにアクセス:
- UI: http://localhost:8080
- API: http://localhost:8086

## 開発

### バックエンド（FastAPI）

バックエンドはFastAPIを使用して実装されており、以下のエンドポイントを提供します：

- `POST /api/v1/user-message`: ユーザーメッセージを処理し、AI応答を返す
- `GET /api/v1/user-messages`: 過去のメッセージ履歴を取得

### フロントエンド（Streamlit）

フロントエンドはStreamlitを使用して実装されており、以下の機能を提供します：

- ユーザーメッセージの入力
- AI応答の表示
- メッセージ履歴の表示

## 環境変数

必要な環境変数：

- `OPENAI_API_KEY`: OpenAI APIキー
- `DB_HOST`: データベースホスト
- `DB_PORT`: データベースポート
- `DB_USER`: データベースユーザー
- `DB_PASSWORD`: データベースパスワード
- `DB_NAME`: データベース名

