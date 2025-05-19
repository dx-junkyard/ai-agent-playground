# AI Agent 開発講座（基礎編）

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
│   ├── main.py              # FastAPIアプリケーション（エンドポイント定義）
│   └── ai_response_generator.py  # AI応答生成クラス（LLMとの連携）
├── config.py            # 設定ファイル（AI_MODEL, AI_URLなどの設定）
├── Dockerfile           # Dockerイメージ定義
├── docker-compose.yml   # Docker Compose設定
├── api_test.sh          # APIテスト用スクリプト
└── requirements.txt     # Pythonパッケージ依存関係
```

## 実装のポイント

- `app/main.py`でFastAPIのエンドポイントを定義し、ユーザーからのメッセージを受け取る
- `app/ai_response_generator.py`でOllamaのAPIを呼び出し、AIの応答を生成
- `config.py`でAIモデルやAPIエンドポイントなどの設定を管理

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
# config.pyファイルを編集して必要な設定を行う
# AI_MODEL: 使用するOllamaのモデル名
# AI_URL: OllamaのAPIエンドポイント（デフォルト: http://host.docker.internal:11434）
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

### レスポンス例

```json
"こんにちは！どのようなことでお手伝いできますか？"
```

## 次のステップ

基礎編を完了したら、以下の応用編に進むことができます：

- MySQL連携編: データベースを使った会話履歴の保存と取得
- UI連携編: StreamlitによるWebインターフェースの実装
