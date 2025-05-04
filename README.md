# AI Agent 開発講座

このリポジトリは、AI Agentの開発を学ぶための教材（基礎編）です。


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
│   └── ai_response_generator.py  # AI応答生成クラス
├── config.py            # 設定ファイル
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 環境構築

### 必要条件
- Docker Desktop
- Ollama（ローカルLLM実行環境）
※　詳細は[環境設定](https://github.com/dx-junkyard/ai-agent-playground/wiki/%E7%92%B0%E5%A2%83%E8%A8%AD%E5%AE%9A)を参照

### セットアップ

1. リポジトリのクローン
```bash
git clone -b basic-course https://github.com/dx-junkyard/ai-agent-playground.git
cd ai-agent-playground
```

2. 環境変数の設定
```bash
# ./app/config.pyファイルを編集して必要な設定を行う
```

3. コンテナの起動
```bash
docker compose up
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
