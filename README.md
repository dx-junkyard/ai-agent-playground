# AI Agent 開発講座（MySQL連携編）

この教材では、AI Agentの会話履歴やユーザー情報をデータベースに保存・取得する方法を学びます。

## 学習内容

- データベース連携の基本
- FastAPIからデータベースへの接続
- 会話履歴の保存と取得
- ユーザーごとの履歴管理
- 複数コンテナ環境の構築

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

## 主要なコンポーネント

- FastAPIアプリケーション: ユーザーメッセージの処理とAI応答の生成
- メッセージリポジトリ: データベースとの連携処理
- AI応答生成: LLMを使った応答の生成

## 実装のポイント

- メッセージ保存・取得用クラスでデータベース操作を実装
- 会話ごとにデータベースへメッセージを保存
- ユーザーIDごとに履歴を取得し、AI応答生成に活用
- 環境変数を使用した接続情報の管理

## データベース設計

ユーザーメッセージテーブルには以下の情報が保存されます：
- ID（自動採番）
- ユーザーID
- メッセージ内容
- 作成日時

## セットアップ手順

1. **リポジトリのクローン**
    ```bash
    git clone -b mysql-integration https://github.com/dx-junkyard/ai-agent-playground.git
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
- 送信したメッセージはデータベースに保存されます

### 履歴の取得

```bash
curl 'http://localhost:8086/api/v1/user-messages?user_id=me&limit=10'
```
- ユーザー"me"の発言履歴を最大10件取得します
