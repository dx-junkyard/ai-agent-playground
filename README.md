# AI Agent 開発講座（UI連携編）

このプロジェクトは、AIエージェントと対話するためのWebアプリケーションです。FastAPIバックエンドとStreamlitフロントエンドで構成されています。

## 学習内容

- Streamlitを使用したWebフロントエンドの構築
- FastAPIバックエンドとの連携
- Webインターフェースの設計と実装
- ユーザーとAIの対話機能の実装
- データベースとの連携

## 主要なコンポーネント

- FastAPIバックエンド: ユーザーメッセージの処理とAI応答の生成
- Streamlitフロントエンド: ユーザーインターフェースの提供
- データベース連携: 会話履歴の保存と取得

## 実装のポイント

### バックエンド（FastAPI）
- APIエンドポイントの定義
- データベース操作の実装
- AI応答生成ロジックの実装

### フロントエンド（Streamlit）
- ユーザーインターフェースの実装
- APIとの通信処理
- セッション状態を使用した会話履歴の管理

## セットアップ

### 前提条件

- Python 3.9以上
- 必要なパッケージ（requirements.txtに記載）

### セットアップ手順

1. **リポジトリのクローン**
    ```bash
    git clone -b ui-integration https://github.com/dx-junkyard/ai-agent-playground.git
    cd ai-agent-playground
    ```

2. **環境構築**
    - 必要な環境変数を設定
    - 依存パッケージのインストール

3. **アプリケーションの起動**
    ```bash
    # Linux/Mac環境
    docker compose up
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

## 拡張アイデア

- ユーザー認証の追加
- 複数のAIモデル切り替え機能
- メッセージの検索機能
- 会話履歴のエクスポート機能
