# AI Agent 開発講座

このリポジトリは、AI Agentの開発を学ぶための教材です。基礎編から応用編まで、段階的に学習できる構成になっています。

## 目次

- [学習コース](#学習コース)
- [環境構築](#環境構築)
- [使い方](#使い方)
- [ライセンス](#ライセンス)

## 学習コース

このリポジトリでは、以下の学習コースを提供しています。各コースは独立したブランチとして管理されています。

### [基礎編（basic-course）](https://github.com/dx-junkyard/ai-agent-playground/tree/basic-course)

基礎編では、FastAPIを使用したシンプルなAI Agentの実装方法を学びます。

#### 学習内容

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

#### プロジェクト構成

```
.
├── app/
│   ├── main.py        # FastAPIアプリケーション
│   └── ai.py          # AIクライアントクラス
├── config.py          # 設定ファイル
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

### [データベース連携編（mysql-integration）](https://github.com/dx-junkyard/ai-agent-playground/tree/mysql-integration)

データベース連携編では、MySQLを使用した会話履歴の保存と管理を学びます。

#### 学習内容

1. **データベース連携**
   - MySQLを使用した会話履歴の保存
   - ユーザー情報の管理
   - 会話コンテキストの保持

2. **データアクセスレイヤーの実装**
   - DBClientクラスの設計と実装
   - クエリの作成と実行
   - エラーハンドリング

3. **APIエンドポイントの拡張**
   - 会話履歴取得APIの実装
   - データベースとの連携処理
   - レスポンスフォーマットの設計

#### プロジェクト構成

```
.
├── app/
│   ├── main.py        # FastAPIアプリケーション
│   ├── ai.py          # AIクライアントクラス
│   └── db.py          # データベースクライアントクラス
├── config.py          # 設定ファイル
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

### [UI連携編（ui-integration）](https://github.com/dx-junkyard/ai-agent-playground/tree/ui-integration)

UI連携編では、StreamlitによるWebフロントエンドの実装と、FastAPIバックエンドとの連携を学びます。

#### 学習内容

1. **Streamlitによるフロントエンド開発**
   - インタラクティブなUIの構築
   - ユーザー入力の処理
   - レスポンスの表示

2. **バックエンドとの連携**
   - APIリクエストの送信
   - レスポンスの処理
   - エラーハンドリング

3. **マルチコンテナ環境の構築**
   - フロントエンドとバックエンドの分離
   - コンテナ間通信の設定
   - 環境変数の管理

#### プロジェクト構成

```
.
├── app/
│   ├── api/                    # FastAPIバックエンド
│   │   ├── main.py            # メインAPIエンドポイント
│   │   ├── ai.py              # AIクライアントクラス
│   │   └── db.py              # データベースクライアントクラス
│   └── ui/                     # Streamlitフロントエンド
│       └── ui.py              # フロントエンドアプリケーション
├── config.py                   # 設定ファイル
├── Dockerfile.api              # バックエンド用Dockerfile
├── Dockerfile.ui               # フロントエンド用Dockerfile
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
git clone https://github.com/dx-junkyard/ai-agent-playground.git
cd ai-agent-playground
```

2. 学習コースの選択
```bash
# 基礎編
git checkout basic-course

# データベース連携編
git checkout mysql-integration

# UI連携編
git checkout ui-integration
```

3. 環境変数の設定
```bash
# ./config.pyファイルを編集して必要な設定を行う
```

4. コンテナの起動
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

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
