# AI Agent 開発講座（MySQL連携編 - Windows対応版）

この教材では、AI Agentの会話履歴やユーザー情報をデータベースに保存・取得する方法を学びます。このブランチはWindows環境での実行に最適化されています。

## 学習内容

- データベース連携の基本
- FastAPIからデータベースへの接続
- 会話履歴の保存と取得
- ユーザーごとの履歴管理
- Windows環境でのコンテナ実行

## 主要なコンポーネント

- FastAPIアプリケーション: ユーザーメッセージの受信と応答の返却
- メッセージリポジトリ: データベースとの連携処理
- AI応答生成: LLMを使った応答の生成

## Windows環境での実装ポイント

- Windows環境でも動作するように設定を最適化
- コマンド例はWindows環境（コマンドプロンプト/PowerShell）で実行できる形式で記載
- メッセージ保存・取得用クラスでデータベース操作を実装
- 会話ごとにデータベースへメッセージを保存
- ユーザーIDごとに履歴を取得し、AI応答生成に活用

## データベース設計

ユーザーメッセージテーブルには以下の情報が保存されます：
- ID（自動採番）
- ユーザーID
- メッセージ内容
- 作成日時

## セットアップ手順

1. **リポジトリのクローン**
    ```
    git clone -b mysql-integration-win https://github.com/dx-junkyard/ai-agent-playground.git
    cd ai-agent-playground
    ```

2. **環境構築**
    - 必要な環境変数を設定
    - 依存パッケージのインストール

3. **アプリケーションの起動**
    ```
    # Windowsコンソールでの起動コマンド
    docker compose up -d
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

### 履歴の取得（コマンドプロンプト）

```
curl "http://localhost:8086/api/v1/user-messages?user_id=me&limit=10"
```

### 履歴の取得（PowerShell）

```powershell
curl "http://localhost:8086/api/v1/user-messages?user_id=me&limit=10"
```

レスポンス例：
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

### データベースへの直接接続（Windows環境）

```
docker exec -it mysql-container mysql --default-character-set=utf8 -u me -p mydb
```

接続後、以下のコマンドでデータを確認できます：
```sql
show tables;
select * from user_messages;
```

## 次のステップ

MySQL連携編を完了したら、以下の応用編に進むことができます：

- UI連携編: StreamlitによるWebインターフェースの実装
