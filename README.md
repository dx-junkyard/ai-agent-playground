# AI Agent 開発講座

このリポジトリは、AI Agentの開発を学ぶための教材です。基礎編から応用編まで、段階的に学習できる構成になっています。

## 目次

- [基礎編](#基礎編)
- [応用編（予定）](#応用編予定)
- [環境構築](#環境構築)
- [使い方](#使い方)
- [ライセンス](#ライセンス)

## 基礎編

基礎編では、FastAPIを使用したシンプルなAI Agentの実装方法を学びます。

### 学習内容

1. **FastAPIの基本**
   - エンドポイントの作成
   - リクエスト/レスポンスの処理
   - エラーハンドリング

2. **AIモデルの統合**
   - Ollamaを使用したローカルLLMの活用
   - プロンプトエンジニアリングの基礎
   - レスポンス生成の実装

3. **Docker環境の構築**
   - コンテナ化の基本
   - マルチコンテナ環境の構築
   - 環境変数の管理

### プロジェクト構成

```
.
├── app/
│   ├── main.py              # FastAPIアプリケーション
│   └── interest_response_generator.py  # AI応答生成クラス
├── config.py            # 設定ファイル
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 応用編（予定）

応用編では、以下の機能を追加予定です：

1. **データベース連携**
   - MySQLを使用した会話履歴の保存
   - ユーザー情報の管理
   - 会話コンテキストの保持

2. **LINE Messaging API連携**
   - Webhookの実装
   - メッセージの送受信
   - リッチメニューの活用

3. **高度なAI機能**
   - 会話履歴を考慮した応答生成
   - 感情分析の統合
   - マルチモーダル対応

## 環境構築

### 必要条件
- Docker Desktop
- Ollama（ローカルLLM実行環境）
※　詳細は[環境設定](https://github.com/dx-junkyard/ai-agent-playground/wiki/%E7%92%B0%E5%A2%83%E8%A8%AD%E5%AE%9A)を参照

### セットアップ

1. リポジトリのクローン
```bash
git clone https://github.com/dx-junkyard/ai-agent-playground.git
cd ai-agent-playground
```

2. 環境変数の設定
```bash
# ./app/config.pyvファイルを編集して必要な設定を行う
```

3. コンテナの起動
```bash
docker compose up -d
```

## 使い方

### APIのテスト

```bash
curl http://localhost:8086/api/v1/user-message \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "message": "あなたのメッセージ"
  }'
```
