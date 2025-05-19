# AI Agent 開発講座（UI連携編）

このプロジェクトは、AIエージェントと対話するためのWebアプリケーションです。FastAPIバックエンドとStreamlitフロントエンドで構成されています。

## 学習内容

- Streamlitを使用したWebフロントエンドの構築
- FastAPIバックエンドとの連携
- マルチコンテナ環境の構築と連携
- ユーザーインターフェースの設計と実装
- MySQLデータベースとの連携

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
├── mysql/                     # MySQLデータベース関連
│   └── db/user_messages.sql   # テーブル定義(DDL)
├── config.py                  # 設定ファイル
├── requirements.api.txt       # API依存関係
├── requirements.ui.txt        # UI依存関係
├── Dockerfile.api             # API用Dockerfile
├── Dockerfile.ui              # UI用Dockerfile
├── docker-compose.yaml        # Docker Compose設定
├── api_test.sh                # APIテスト用スクリプト
└── db_connect.sh              # DB接続確認用スクリプト
```

## 実装のポイント

### バックエンド（FastAPI）
- `app/api/main.py`でAPIエンドポイントを定義
- `app/api/message_repository.py`でデータベース操作を実装
- `app/api/ai_response_generator.py`でAI応答生成ロジックを実装

### フロントエンド（Streamlit）
- `app/ui/ui.py`でユーザーインターフェースを実装
- APIとの通信は`requests`ライブラリを使用
- セッション状態を使用して会話履歴を管理

### データベース（MySQL）
- ユーザーメッセージとAI応答を保存
- 会話履歴の取得と表示

## セットアップ

### 前提条件

- Docker
- Docker Compose

### セットアップ手順

1. **リポジトリのクローン**
    ```bash
    git clone -b ui-integration https://github.com/dx-junkyard/ai-agent-playground.git
    cd ai-agent-playground
    ```

2. **設定ファイルの編集**
    - `config.py`でDB接続情報やAIモデル設定を確認・必要に応じて修正

3. **Dockerコンテナのビルドと起動**
    ```bash
    docker compose build
    docker compose up -d
    ```

4. **アプリケーションにアクセス**
    - UI: http://localhost:8080
    - API: http://localhost:8086

## 使い方

### Webインターフェース

1. ブラウザで http://localhost:8080 にアクセス
2. テキスト入力欄にメッセージを入力
3. 「送信」ボタンをクリックしてAIと対話
4. 会話履歴は画面上に表示されます

### APIの直接利用

#### メッセージの送信

```bash
curl http://localhost:8086/api/v1/user-message \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "message": "こんにちは！"
  }'
```

#### 履歴の取得

```bash
curl 'http://localhost:8086/api/v1/user-messages?user_id=me&limit=10'
```

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

- `AI_MODEL`: 使用するAIモデル名
- `AI_URL`: AIモデルのAPIエンドポイント
- `DB_HOST`: データベースホスト
- `DB_PORT`: データベースポート
- `DB_USER`: データベースユーザー
- `DB_PASSWORD`: データベースパスワード
- `DB_NAME`: データベース名

## 拡張アイデア

- ユーザー認証の追加
- 複数のAIモデル切り替え機能
- メッセージの検索機能
- 会話履歴のエクスポート機能
