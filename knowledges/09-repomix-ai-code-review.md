# 09. Repomix による AI コードレビュー

**最終更新**: 2025-01-07
**カテゴリ**: 開発ツールとユーティリティ
**難易度**: ⭐⭐ (初級〜中級)

## 📋 目次

1. [概要](#概要)
2. [Repomixとは](#repomixとは)
3. [主な機能](#主な機能)
4. [インストールと基本的な使い方](#インストールと基本的な使い方)
5. [出力形式](#出力形式)
6. [AI駆動開発での活用](#ai駆動開発での活用)
7. [複数AIでの相互レビュー](#複数aiでの相互レビュー)
8. [Trust but Verify Layer 2での活用](#trust-but-verify-layer-2での活用)
9. [ベストプラクティス](#ベストプラクティス)
10. [実践例：Java/Spring Bootプロジェクト](#実践例javaspring-bootプロジェクト)
11. [トラブルシューティング](#トラブルシューティング)
12. [まとめ](#まとめ)
13. [参考資料](#参考資料)

---

## 概要

### Repomixとは

**Repomix**（レポミックス）は、コードベース全体を単一のAIフレンドリーなファイルにパッケージ化する強力なツールです。Claude、ChatGPT、DeepSeek、Perplexity、Gemini、Llama、Grokなど、あらゆるLLM（大規模言語モデル）に対応しています。

**公式サイト**: https://repomix.com/

**作者**: yamadashy氏（日本人開発者）

**GitHub**: https://github.com/yamadashy/repomix
- ⭐ 5,000+ スター（2025年1月時点）
- JSNation Open Source Awards 2025「Powered by AI」カテゴリにノミネート

### なぜRepomixが必要か

**問題**: AIにコードレビューを依頼する際の課題
```
従来の方法:
1. ファイルを1つずつコピー＆ペースト
2. ディレクトリ構造が伝わらない
3. ファイル間の関係が分からない
4. 何度も同じファイルを貼り付ける
```

**Repomixの解決策**:
```
Repomixを使用:
1. コマンド1つで全ファイルをパッケージ化
2. ディレクトリ構造を保持
3. ファイル間の依存関係が明確
4. AIが全体像を理解した上でレビュー可能
```

### AI駆動開発における位置づけ

```
要件定義 → 設計 → 実装 → テスト
                           ↓
                    Repomix ← ここで活用
                           ↓
                    AIコードレビュー（Trust but Verify Layer 2）
                           ↓
                    複数AIでの相互検証
```

---

## Repomixとは

### 公式の説明

> "Repomix is a powerful tool that packs your entire repository into a single, AI-friendly file. Perfect for when you need to feed your codebase to Large Language Models (LLMs)."

### 特徴

1. **単一ファイル出力**
   - クリアなセパレータでコードの異なる部分を分離
   - ディレクトリ構造を保持

2. **AI最適化**
   - LLMが理解しやすい形式にフォーマット化
   - ファイルの冒頭にAI理解を向上させる説明を追加

3. **トークンカウント**
   - LLMのコンテキスト制限に対応するためのトークン数を計測
   - Claude（200,000トークン）、GPT-4（128,000トークン）などの上限を確認

4. **Git対応**
   - `.gitignore` および `.git/info/exclude` を自動認識
   - パッケージング対象から除外

5. **セキュリティ重視**
   - Secretlintを使用した機密情報の検出と保護
   - `.env`、`credentials.json` などを自動除外

6. **Model Context Protocol対応**
   - MCPサーバーとして実行可能
   - AIアシスタントがコードベースと直接対話可能

---

## 主な機能

### 1. 複数の出力形式

| 形式 | 特徴 | 推奨用途 |
|------|------|---------|
| **XML** | 構造化データ、パース容易 | Claude、ChatGPT |
| **Markdown** | 読みやすい、コードブロック強調 | GitHub、ドキュメント生成 |
| **Plain Text** | シンプル、互換性高い | 軽量なレビュー |

### 2. ファイルフィルタリング

**include/excludeパターン**:
```bash
# 特定のファイルのみ含める
repomix --include "src/**/*.java"

# 特定のファイルを除外
repomix --exclude "**/*.test.java,**/node_modules/**"
```

### 3. トークン数表示

```bash
repomix --show-tokens
```

**出力例**:
```
Total tokens: 45,234
  - Claude 3.5 Sonnet (200k): 22.6% used
  - GPT-4 Turbo (128k): 35.3% used
  - Gemini 1.5 Pro (1M): 4.5% used
```

### 4. リモートリポジトリ対応

```bash
# GitHubリポジトリを直接パッケージ化
repomix --remote https://github.com/user/repo
```

### 5. カスタムプロンプト追加

**`repomix.config.json`**:
```json
{
  "output": {
    "customInstructions": "このコードベースはSpring Bootで実装されたECサイトです。セキュリティとパフォーマンスの観点からレビューしてください。"
  }
}
```

---

## インストールと基本的な使い方

### インストール

```bash
# npm経由
npm install -g repomix

# バージョン確認
repomix --version
```

### 基本的な使い方

#### 1. デフォルト出力（XML形式）

```bash
# プロジェクトディレクトリで実行
cd /path/to/your/project
repomix

# 出力: repomix-output.xml
```

#### 2. Markdown形式で出力

```bash
repomix --output codebase.md --format markdown
```

#### 3. トークン数を表示

```bash
repomix --show-tokens
```

#### 4. 特定のディレクトリのみ

```bash
repomix --include "src/main/java/**"
```

#### 5. リモートリポジトリ

```bash
repomix --remote https://github.com/spring-projects/spring-boot
```

---

## 出力形式

### XML形式（デフォルト）

**`repomix-output.xml`**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<repository>
  <metadata>
    <name>my-spring-boot-app</name>
    <totalFiles>85</totalFiles>
    <totalTokens>45234</totalTokens>
    <generatedAt>2025-01-07T10:30:00Z</generatedAt>
  </metadata>

  <structure>
    <directory name="src">
      <directory name="main">
        <directory name="java">
          <directory name="com">
            <directory name="example">
              <file name="Application.java" />
              <file name="UserController.java" />
              ...
            </directory>
          </directory>
        </directory>
      </directory>
    </directory>
  </structure>

  <files>
    <file path="src/main/java/com/example/Application.java">
      <content><![CDATA[
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
      ]]></content>
    </file>

    <file path="src/main/java/com/example/UserController.java">
      <content><![CDATA[
package com.example;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    // ...
}
      ]]></content>
    </file>
    ...
  </files>
</repository>
```

### Markdown形式

**`codebase.md`**:
````markdown
# Codebase: my-spring-boot-app

**Generated**: 2025-01-07 10:30:00
**Total Files**: 85
**Total Tokens**: 45,234

## Directory Structure

```
src/
├── main/
│   ├── java/
│   │   └── com/
│   │       └── example/
│   │           ├── Application.java
│   │           ├── UserController.java
│   │           └── UserService.java
│   └── resources/
│       └── application.yml
└── test/
    └── java/
        └── com/
            └── example/
                └── UserControllerTest.java
```

## Files

### src/main/java/com/example/Application.java

```java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### src/main/java/com/example/UserController.java

```java
package com.example;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    // ...
}
```
````

---

## AI駆動開発での活用

### ユースケース1: コードレビュー

**ワークフロー**:
```bash
# 1. Repomixでパッケージ化
repomix --output codebase.md --format markdown

# 2. AIにレビュー依頼
# codebase.mdをClaude Code、ChatGPT、Geminiなどに貼り付け
```

**プロンプト例**:
```
このファイルはリポジトリ内のすべてのファイルを1つにまとめたものです。

以下の観点でコードレビューをお願いします：

1. **セキュリティ**
   - SQLインジェクション、XSS、CSRF脆弱性
   - 認証・認可の実装漏れ
   - 機密情報のハードコード

2. **パフォーマンス**
   - N+1クエリ問題
   - 不要なデータベースアクセス
   - メモリリーク

3. **コード品質**
   - SOLID原則違反
   - コードの重複
   - 命名規則

4. **Spring Bootベストプラクティス**
   - 適切なアノテーション使用
   - DIコンテナの活用
   - 例外ハンドリング

具体的な問題箇所を「ファイル名:行数」の形式で指摘してください。
```

### ユースケース2: リファクタリング提案

**プロンプト例**:
```
このコードベースをリファクタリングしたいです。

優先度の高い改善点を以下の観点から提案してください：

1. **循環的複雑度の削減**
   - 複雑度10以上のメソッドを特定
   - 分割・簡略化の提案

2. **重複コードの削減**
   - 同じロジックが3回以上出現する箇所
   - 共通化の提案

3. **アーキテクチャ改善**
   - レイヤー分離の問題
   - 依存関係の逆転

各提案に対して、具体的なコード例を示してください。
```

### ユースケース3: ドキュメント生成

**プロンプト例**:
```
このコードベースから、以下のドキュメントを生成してください：

1. **README.md**
   - プロジェクト概要
   - セットアップ手順
   - 主要な機能

2. **API仕様書（OpenAPI形式）**
   - 全エンドポイントのリスト
   - リクエスト/レスポンス例

3. **アーキテクチャ図（Mermaid記法）**
   - レイヤー構成
   - 主要なクラスの関係
```

### ユースケース4: 新機能の実装計画

**プロンプト例**:
```
このコードベースに「商品レコメンデーション機能」を追加したいです。

既存のアーキテクチャを踏まえて、以下を提案してください：

1. **実装すべきクラス**
   - Controller、Service、Repository、Entity

2. **変更が必要な既存ファイル**
   - ファイル名と変更内容

3. **タスク分解**
   - 実装順序
   - 各タスクの見積もり時間

4. **考慮すべきリスク**
   - パフォーマンスへの影響
   - 既存機能への影響
```

---

## 複数AIでの相互レビュー

### なぜ複数AIで検証するのか

**1つのAIだけに頼る問題点**:
- AIの**Hallucination**（虚偽報告）: 存在しないAPIを提案
- AIの**Jagged Intelligence**（凸凹な知能）: 得意分野と苦手分野がある
- **見落とし**: 1つのAIが見逃した問題がある

**複数AIで相互検証するメリット**:
- **異なる視点**: Claude、ChatGPT、Geminiで得意分野が異なる
- **見落とし防止**: あるAIが見逃した問題を別のAIが指摘
- **信頼性向上**: 複数AIが同じ問題を指摘 → 高確率で真の問題

### 複数AIレビューのワークフロー

```
STEP 1: Repomixでパッケージ化
  ↓
STEP 2: Claude 3.5 Sonnetでレビュー
  ↓
STEP 3: ChatGPT o1でレビュー
  ↓
STEP 4: Gemini 1.5 Proでレビュー
  ↓
STEP 5: 結果を統合・比較
  ↓
STEP 6: 共通の指摘 → 優先的に修正
  ↓
STEP 7: 1つのAIだけの指摘 → 人間が判断
```

### 実践例: Spring Bootアプリのセキュリティレビュー

#### STEP 1: Repomixでパッケージ化

```bash
# セキュリティレビュー用にパッケージ化
repomix --output security-review.md --format markdown \
  --include "src/**/*.java,pom.xml,application.yml"
```

#### STEP 2: Claude 3.5 Sonnetでレビュー

**プロンプト**:
```
このSpring Bootアプリケーションのセキュリティレビューをお願いします。

以下のOWASP Top 10の脆弱性を重点的にチェックしてください：

1. SQLインジェクション
2. 認証・認可の不備
3. 機密データの露出
4. XMLエンティティ攻撃（XXE）
5. アクセス制御の不備
6. セキュリティ設定ミス
7. XSS（クロスサイトスクリプティング）
8. 安全でないデシリアライゼーション
9. 既知の脆弱性を持つコンポーネント使用
10. ログとモニタリングの不足

具体的な問題箇所を「ファイル名:クラス名:メソッド名」の形式で指摘してください。
```

**Claude 3.5 Sonnetの回答例**:
```
セキュリティレビュー結果：

【高リスク】
1. UserController.java:getUserById() - SQLインジェクションの可能性
   - 問題: String concatenationでSQLを構築
   - 推奨: PreparedStatementまたはJPA使用

2. AuthController.java:login() - パスワードのハッシュ化なし
   - 問題: 平文パスワードをDBに保存
   - 推奨: BCryptPasswordEncoderを使用

3. application.yml - 機密情報のハードコード
   - 問題: database.password=admin123 が平文
   - 推奨: 環境変数またはVaultを使用

【中リスク】
4. FileUploadController.java:upload() - ファイルタイプチェックなし
   - 問題: 任意のファイルをアップロード可能
   - 推奨: Content-Typeと拡張子を検証

...
```

#### STEP 3: ChatGPT o1でレビュー

**同じプロンプトを使用**

**ChatGPT o1の回答例**:
```
セキュリティレビュー結果：

【高リスク】
1. UserController.java:getUserById() - SQLインジェクション
   - Claudeと同じ指摘 ← 信頼性高い

2. AuthController.java:login() - パスワードのハッシュ化なし
   - Claudeと同じ指摘 ← 信頼性高い

3. application.yml - Spring Boot Actuatorのセキュリティ設定不足
   - Claudeが見落とした問題 ← 新しい視点

【中リスク】
4. CorsConfig.java - CORS設定が緩すぎる
   - 問題: allowedOrigins = "*"
   - 推奨: 特定のドメインのみ許可

5. pom.xml - 古いバージョンのSpring Securityを使用
   - 問題: spring-security 5.5.0（既知の脆弱性あり）
   - 推奨: 最新版にアップデート

...
```

#### STEP 4: Gemini 1.5 Proでレビュー

**同じプロンプトを使用**

**Gemini 1.5 Proの回答例**:
```
セキュリティレビュー結果：

【高リスク】
1. UserController.java:getUserById() - SQLインジェクション
   - Claude、ChatGPTと同じ指摘 ← 確実に修正すべき

2. AuthController.java:login() - セッション固定攻撃への脆弱性
   - 問題: ログイン成功時にセッションIDを再生成していない
   - 推奨: sessionRegistry.invalidateSession()を呼び出す

3. application.yml - HTTPSが有効化されていない
   - 問題: server.ssl.enabled = false
   - 推奨: 本番環境ではHTTPSを強制

【中リスク】
4. LoggingAspect.java - 機密情報のログ出力
   - 問題: パスワード、トークンをログに出力
   - 推奨: @SensitiveDataアノテーションでマスク

...
```

#### STEP 5: 結果を統合・比較

**統合シート**:

| 問題 | Claude | ChatGPT | Gemini | 優先度 |
|------|--------|---------|--------|--------|
| SQLインジェクション（UserController） | ✅ | ✅ | ✅ | **P0（即座に修正）** |
| パスワードのハッシュ化なし | ✅ | ✅ | - | **P0（即座に修正）** |
| 機密情報のハードコード（application.yml） | ✅ | - | - | P1（次回リリース） |
| Spring Boot Actuatorのセキュリティ設定不足 | - | ✅ | - | P1 |
| CORS設定が緩すぎる | - | ✅ | - | P1 |
| 古いSpring Securityバージョン | - | ✅ | - | P1 |
| セッション固定攻撃への脆弱性 | - | - | ✅ | P1 |
| HTTPSが無効 | - | - | ✅ | P0（本番環境） |
| 機密情報のログ出力 | - | - | ✅ | P2 |

**優先度の判断**:
- **3つのAIすべてが指摘** → **P0（最優先）**
- **2つのAIが指摘** → **P0**
- **1つのAIだけが指摘** → P1またはP2（人間が検証）

#### STEP 6: 修正とレビュー

**P0の修正**:
```java
// Before（SQLインジェクション脆弱性）
@GetMapping("/{id}")
public User getUserById(@PathVariable String id) {
    String sql = "SELECT * FROM users WHERE id = " + id; // ❌ 危険
    return jdbcTemplate.queryForObject(sql, User.class);
}

// After（修正）
@GetMapping("/{id}")
public User getUserById(@PathVariable Long id) {
    return userRepository.findById(id)
        .orElseThrow(() -> new UserNotFoundException(id)); // ✅ 安全
}
```

```java
// Before（パスワード平文保存）
public void createUser(String email, String password) {
    User user = new User();
    user.setEmail(email);
    user.setPassword(password); // ❌ 平文
    userRepository.save(user);
}

// After（修正）
@Autowired
private PasswordEncoder passwordEncoder;

public void createUser(String email, String password) {
    User user = new User();
    user.setEmail(email);
    user.setPassword(passwordEncoder.encode(password)); // ✅ BCryptでハッシュ化
    userRepository.save(user);
}
```

---

## Trust but Verify Layer 2での活用

### Trust but Verifyの3層構造

```
Layer 1（自動検証）: コンパイル、テスト、静的解析（CheckStyle、SpotBugs、PMD）
  ↓
Layer 2（AI自己検証）: Repomixで複数AIレビュー ← ここで活用
  ↓
Layer 3（人間レビュー）: ビジネスロジック、アーキテクチャレビュー
```

### Layer 2でのRepomix活用フロー

```
STEP 1: Claude Codeで実装
  ↓
STEP 2: Layer 1（自動検証）
  - mvn compile（コンパイルチェック）
  - mvn test（単体テスト）
  - mvn checkstyle:check（CheckStyle）
  - mvn spotbugs:check（SpotBugs）
  - mvn pmd:check（PMD）
  ↓ すべて成功
STEP 3: Repomixでパッケージ化
  ↓
STEP 4: 複数AI（Claude、ChatGPT、Gemini）でレビュー
  ↓ 問題が見つかった場合
STEP 5: Claude Codeに修正依頼
  ↓
STEP 6: 再度Layer 1 + Layer 2で検証
  ↓ 問題なし
STEP 7: Layer 3（人間レビュー）
```

### Layer 2での具体的プロンプト

**セキュリティレビュー**:
```
このコードベースをセキュリティの観点からレビューしてください。

以下のチェック項目に沿って検証してください：

✓ SQLインジェクション、XSS、CSRF脆弱性
✓ 認証・認可の実装漏れ
✓ 機密情報のハードコード（パスワード、APIキー）
✓ 安全でないデシリアライゼーション
✓ ファイルアップロードの脆弱性
✓ CORS設定の妥当性
✓ HTTPSの使用
✓ セッション管理の安全性

問題が見つかった場合、以下の形式で報告してください：
- ファイル名:行数
- 問題の説明
- 修正方法の提案
- リスクレベル（高/中/低）
```

**パフォーマンスレビュー**:
```
このコードベースをパフォーマンスの観点からレビューしてください。

以下の問題を特定してください：

✓ N+1クエリ問題
✓ 不要なデータベースアクセス
✓ メモリリーク
✓ 無駄なループ処理
✓ キャッシュの未使用
✓ インデックスの欠如
✓ 非効率なSQL

問題が見つかった場合、具体的な改善案を提示してください。
```

---

## ベストプラクティス

### 1. 段階的なレビュー

**❌ 悪い例**: 全ファイルを一度にレビュー
```bash
repomix  # すべてのファイル（10,000行以上）
```
→ トークン消費が大きすぎる、レビューが浅くなる

**✅ 良い例**: レイヤーごとにレビュー
```bash
# Controller層のみ
repomix --include "src/main/java/**/controller/**" --output controllers.md

# Service層のみ
repomix --include "src/main/java/**/service/**" --output services.md

# Repository層のみ
repomix --include "src/main/java/**/repository/**" --output repositories.md
```

### 2. セキュリティ重視の設定

**`.repomixignore`**:
```
# 機密情報を含むファイルを除外
.env
*.key
*.pem
credentials.json
application-prod.yml
src/main/resources/keystore.jks

# ビルド成果物を除外
target/
build/
*.class
*.jar

# テストデータを除外
**/test-data/
**/fixtures/
```

### 3. カスタムインストラクション

**`repomix.config.json`**:
```json
{
  "output": {
    "filePath": "ai-review.md",
    "style": "markdown",
    "customInstructions": "このコードベースはSpring Boot 3.2で実装されたECサイトです。\n\n**レビュー観点**:\n1. セキュリティ（OWASP Top 10）\n2. パフォーマンス（N+1クエリ、キャッシュ）\n3. Spring Bootベストプラクティス\n4. RESTful API設計\n\n**技術スタック**:\n- Spring Boot 3.2\n- Spring Security 6.0\n- Spring Data JPA\n- PostgreSQL\n- Thymeleaf"
  },
  "include": [
    "src/main/java/**",
    "src/main/resources/application.yml",
    "pom.xml"
  ],
  "ignore": {
    "customPatterns": [
      "**/test/**",
      "**/*.test.java"
    ]
  }
}
```

### 4. トークン数の最適化

**トークン数が多すぎる場合**:
```bash
# トークン数を確認
repomix --show-tokens

# 結果: Total tokens: 250,000（Claude 3.5 Sonnetの上限200,000を超過）
```

**対策**:
```bash
# 1. コメントを除外
repomix --remove-comments

# 2. 空行を除外
repomix --remove-empty-lines

# 3. 特定のディレクトリのみ
repomix --include "src/main/java/com/example/core/**"

# 結果: Total tokens: 85,000（上限内に収まる）
```

### 5. 定期的なレビュー

**GitHub Actionsでの自動化**:
```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    branches: [main]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Repomix
        run: npm install -g repomix

      - name: Package codebase
        run: repomix --output pr-review.md --format markdown

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: ai-review-package
          path: pr-review.md

      # 人間がダウンロードしてAIにレビュー依頼
```

---

## 実践例：Java/Spring Bootプロジェクト

### プロジェクト構成

```
my-spring-boot-app/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── example/
│   │   │           ├── Application.java
│   │   │           ├── controller/
│   │   │           ├── service/
│   │   │           ├── repository/
│   │   │           └── entity/
│   │   └── resources/
│   │       ├── application.yml
│   │       └── templates/
│   └── test/
├── pom.xml
└── repomix.config.json
```

### repomix.config.json

```json
{
  "output": {
    "filePath": "spring-boot-review.md",
    "style": "markdown",
    "customInstructions": "Spring Boot 3.2アプリケーション\n\n**レビュー観点**:\n1. RESTful API設計\n2. Spring Securityの実装\n3. データベース設計（JPA Entity）\n4. 例外ハンドリング\n5. トランザクション管理"
  },
  "include": [
    "src/main/java/**/*.java",
    "src/main/resources/application*.yml",
    "pom.xml"
  ],
  "ignore": {
    "useGitignore": true,
    "customPatterns": [
      "**/test/**",
      "**/*.class",
      "target/**"
    ]
  },
  "security": {
    "enableSecretDetection": true
  }
}
```

### 実行

```bash
# 1. パッケージ化
repomix

# 2. トークン数を確認
repomix --show-tokens
# 出力: Total tokens: 45,234

# 3. Claude 3.5 Sonnetでレビュー
# spring-boot-review.mdをClaude Codeに貼り付け
```

### レビュープロンプト

```
このSpring Bootアプリケーションをレビューしてください。

**観点**:
1. RESTful API設計
   - HTTPメソッドの適切な使用
   - リソース指向の設計
   - ステータスコードの正確性

2. Spring Securityの実装
   - 認証・認可の実装
   - CSRF対策
   - セッション管理

3. データベース設計
   - Entity設計の妥当性
   - インデックスの設定
   - カスケード設定

4. 例外ハンドリング
   - @ControllerAdviceの使用
   - カスタム例外の定義
   - エラーレスポンスの一貫性

5. トランザクション管理
   - @Transactionalの適切な配置
   - トランザクション境界
   - ロールバック条件

具体的な改善点を、ファイル名と行数とともに指摘してください。
```

---

## トラブルシューティング

### 問題1: トークン数が上限を超える

**症状**:
```bash
repomix --show-tokens
# Total tokens: 350,000（Claude 3.5 Sonnetの上限200,000を超過）
```

**解決策**:
```bash
# 1. コメントと空行を除外
repomix --remove-comments --remove-empty-lines

# 2. テストコードを除外
repomix --exclude "**/test/**"

# 3. 特定のレイヤーのみ
repomix --include "src/main/java/**/controller/**,src/main/java/**/service/**"
```

### 問題2: 機密情報が含まれる

**症状**:
```
repomix-output.xmlに `database.password=admin123` が含まれる
```

**解決策**:
```bash
# 1. .repomixignoreに追加
echo "application-prod.yml" >> .repomixignore
echo ".env" >> .repomixignore

# 2. セキュリティ検出を有効化
# repomix.config.jsonに以下を追加
{
  "security": {
    "enableSecretDetection": true
  }
}
```

### 問題3: 不要なファイルが含まれる

**症状**:
```
target/, node_modules/などのビルド成果物が含まれる
```

**解決策**:
```bash
# 1. .gitignoreを活用
repomix --use-gitignore

# 2. カスタムパターンで除外
repomix --exclude "target/**,node_modules/**,build/**"
```

---

## まとめ

### Repomixの主な利点

1. **効率的なAIレビュー**
   - コードベース全体を1ファイルにパッケージ化
   - ディレクトリ構造を保持
   - トークン数を最適化

2. **複数AIでの相互検証**
   - Claude、ChatGPT、Geminiで異なる視点
   - 見落とし防止
   - 信頼性向上

3. **Trust but Verify Layer 2での活用**
   - 自動検証（Layer 1）後のAIレビュー
   - セキュリティ、パフォーマンス、コード品質の多角的検証
   - 人間レビュー（Layer 3）前の問題発見

4. **開発効率の向上**
   - リファクタリング提案
   - ドキュメント生成
   - 新機能の実装計画

### 推奨ワークフロー

```
実装（Claude Code）
  ↓
Layer 1（自動検証）: mvn test, checkstyle, spotbugs, pmd
  ↓
Repomixでパッケージ化
  ↓
Layer 2（AIレビュー）:
  - Claude 3.5 Sonnet
  - ChatGPT o1
  - Gemini 1.5 Pro
  ↓
結果統合・優先度判定
  ↓
修正（Claude Code）
  ↓
Layer 3（人間レビュー）
  ↓
マージ
```

---

## 参考資料

### 公式ドキュメント

1. **Repomix公式サイト**
   - [Repomix.com](https://repomix.com/)
   - [日本語ガイド](https://repomix.com/ja/guide/)
   - [基本的な使い方](https://repomix.com/ja/guide/usage)
   - [ユースケース](https://repomix.com/guide/use-cases)

2. **GitHub リポジトリ**
   - [yamadashy/repomix](https://github.com/yamadashy/repomix)
   - 5,000+ スター（2025年1月時点）

3. **MCP Server**
   - [Repomix MCP Server - LobeHub](https://lobehub.com/mcp/yamadashy-repomix)

### 技術記事・ブログ

4. **日本語記事**
   - [リポジトリをまるっとAIに食わせるRepomixの話](https://speakerdeck.com/yamadashy/sakura-ai-meetup-repomix-20250318) - Speaker Deck
   - [思いつきで作ったAIツールが5000スターを獲得した話](https://zenn.dev/yamadashy/articles/ai-tool-repomix-5000-star) - Zenn
   - [Repomix活用術：GitHubリポジトリをAIプロンプトに変換して爆速で稼ぐ方法](https://note.com/quiet_gibbon6020/n/n3f3ccbbfa6ab) - note
   - [VibeCodingに必須の便利ツール「repomix」の紹介](https://cryptobox.blog/blog/repomix/)

5. **英語記事**
   - [My LLM codegen workflow atm](https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/) - Harper Reed's Blog
   - [How to Get Automatic Code Review Using LLM Before Committing](https://dev.to/docker/how-to-get-automatic-code-review-using-llm-before-committing-3nkj) - DEV Community

### 学術論文

6. **AI Code Review研究**
   - [AI-powered Code Review with LLMs: Early Results](https://arxiv.org/abs/2404.18496) - arXiv 2024
   - [Evaluating Large Language Models for Code Review](https://arxiv.org/html/2505.20206v1) - arXiv 2025
   - [Rethinking Code Review Workflows with LLM Assistance: An Empirical Study](https://arxiv.org/html/2505.16339v1) - arXiv 2025

### 関連トピック

- [18. Trust but Verify（任せる＆確かめる）](./18-trust-but-verify.md)
- [15. AI Hallucination（虚偽報告）](./15-ai-hallucination.md)
- [14. Jagged Intelligence（凸凹な知能）](./14-jagged-intelligence.md)
- [02. Test Driven Development (TDD)](./02-test-driven-development-tdd.md)

---

**次のトピック**: [10. Rust製開発ツール](./10-rust-based-dev-tools.md)
**前のトピック**: [08. Architecture Decision Records (ADR)](./08-architecture-decision-records-adr.md)

---

**📝 更新履歴**:
- 2025-01-07: Repomix特化版に全面改訂（複数AIレビュー、Trust but Verify Layer 2活用を追加）
- 2025-01-06: 初版作成（code2prompt、files-to-promptとの比較）
