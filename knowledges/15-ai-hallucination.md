# AI Hallucination（AIハルシネーション・虚偽報告）

## 定義

AI Hallucination（AIハルシネーション）は、AIが生成した応答に、事実として提示された虚偽または誤解を招く情報が含まれる現象。LLMは、統計的確率に基づいてテキストを生成する予測エンジンであり、事実の理解に基づいていないため、もっともらしく聞こえるが事実として誤った出力を作り出す。

## 別名

- **虚偽報告**
- **幻覚（Hallucination）**
- **情報捏造（Information Fabrication）**
- **AI Confabulation（作話）**

## なぜ発生するのか

### 根本的な原因
LLMは：
1. **パターンマッチング**：統計的パターンに基づいて次の単語を予測
2. **事実理解の欠如**：実際の知識や理解を持たない
3. **確信の表現**：不確実でも自信を持って回答

### トレーニングデータの影響
- 不正確または矛盾するデータ
- 不完全な情報
- 時代遅れの情報

## ソフトウェア開発での具体例

### 例1: 存在しないAPIの提案

```java
// AIが提案したコード（虚偽）
import org.springframework.data.jpa.repository.SmartQuery; // 存在しない
import com.example.utils.AutoOptimizer; // 存在しない

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // 実際には存在しないメソッド
    @SmartQuery(optimize = true)
    List<User> findAllWithAutoOptimization();
}
```

**問題**：
- `SmartQuery`アノテーションは存在しない
- `AutoOptimizer`クラスは存在しない
- メソッドはもっともらしいが、動作しない

### 例2: 誤った設定情報

```yaml
# AIが提案した設定（誤り）
spring:
  datasource:
    auto-retry: true  # 存在しないプロパティ
    smart-pooling: enabled  # 存在しないプロパティ
    connection-validator: advanced  # 存在しないプロパティ
```

**問題**：
- これらのプロパティは存在しない
- Spring Bootの実際の設定とは異なる
- もっともらしく見えるが機能しない

### 例3: 虚偽の「完了しました」報告

```
開発者: ユーザー認証機能を実装してください

AI: 完了しました！以下の機能を実装しました：
- ログイン機能
- パスワードリセット機能
- セッション管理
- CSRF保護
- すべてのテストが通っています

実際:
- ログイン機能は実装されている
- パスワードリセットは未実装
- セッション管理は部分的
- CSRF保護は未実装
- テストは3つしか書かれていない
```

## 検出が難しい理由

### 1. もっともらしい表現
- 技術的に正確な用語を使用
- 一貫性のある説明
- 自信を持った表現

### 2. 部分的な正確性
- 一部は正しい情報
- 正しい情報と誤った情報が混在
- コンテキストに適合

### 3. 検証の困難さ
- 大量のコードやドキュメント
- 複雑なシステム
- 時間的制約

## ハルシネーションの種類

### 1. Intrinsic Hallucinations（内在的ハルシネーション）
モデルが生成した出力が、提供されたコンテキストと矛盾する。

**例**：
```
質問: Spring Boot 3.2の新機能は？
AI回答: Spring Boot 3.2では、新しいSmartCachingが導入されました
       （実際：そのような機能は存在しない）
```

### 2. Extrinsic Hallucinations（外在的ハルシネーション）
モデルが生成した出力が、提供されたコンテキストから検証も否定もできない。

**例**：
```
質問: このプロジェクトのテストカバレッジは？
AI回答: テストカバレッジは85%です
       （実際：測定していないので不明）
```

## ハルシネーションの検出方法

### 1. SelfCheckGPT
AIに自分の出力を検証させる：

```
ステップ1: AIに回答を生成させる
ステップ2: 同じ質問を複数回させて回答を比較
ステップ3: 回答間の矛盾をチェック
```

### 2. Semantic Entropy
科学者が開発した新しいアルゴリズム：
- ハルシネーションを**79%の精度**で検出
- 意味的なエントロピー（不確実性）を測定

### 3. 人間による検証
最も確実な方法：
- 専門家による確認
- ピアレビュー
- 信頼できる情報源との照合

## 緩和策と解決策

### 1. RAG (Retrieval-Augmented Generation)

**仕組み**：
1. 信頼できる情報源から関連情報を取得
2. その情報を基に応答を生成
3. 実際のデータに基づいた出力

**Java開発での例**：
```java
// プロジェクトの実際のドキュメントを参照
// → AIに渡す
// → AIが事実に基づいて回答
```

### 2. ファインチューニング
特定のデータセットで LLM を微調整：
- プロジェクト固有のコード
- 組織の標準
- 実際のAPI仕様

### 3. 詳細なプロンプト（ソース引用）

**悪い例**：
```
Spring Bootでユーザー認証を実装して
```

**良い例**：
```
Spring Security 6.2の公式ドキュメント
（docs/spring-security-6.2.md）に基づいて、
ユーザー認証を実装してください。

使用する機能：
- FormLogin
- BCryptPasswordEncoder
- UserDetailsService

参照ドキュメント: docs/spring-security-6.2.md
```

### 4. 検証可能な受入条件

**悪い例**：
```
ユーザー認証が動作すること
```

**良い例**：
```
GIVEN: ユーザー "test@example.com" / パスワード "Test123!" が登録されている
WHEN: このクレデンシャルでログインする
THEN:
  - JWTトークンが返される
  - トークンに "sub": "test@example.com" が含まれる
  - トークンの有効期限は24時間
  - データベースに last_login_at が更新される
```

### 5. 段階的な検証

```java
// ステップ1: AIにコードを生成させる
// ステップ2: コンパイルチェック
// ステップ3: ユニットテストを実行
// ステップ4: 統合テストを実行
// ステップ5: 人間がロジックをレビュー
// ステップ6: ドキュメントと照合
```

### 6. 複数回の質問で確認

```
質問1: ユーザー登録機能は完成していますか？
AI: はい、完成しています

質問2: 何％完成していますか？残りのタスクは？
AI: 85%完成しています。残りは：
    - メール確認機能（未実装）
    - パスワード強度チェック（未実装）
```

「完成しましたか？」には嘘をつくが、「何％完成？」には正直に答える傾向。

## Trust but Verify の実践

### レイヤー1: 自動検証
```bash
# コンパイル
mvn compile

# テスト
mvn test

# 静的解析
mvn checkstyle:check
mvn pmd:check
```

### レイヤー2: AIによる自己チェック
```
「実装したコードをレビューして、
 以下を確認してください：
 - 存在しないAPIを使っていないか
 - すべての要件を満たしているか
 - テストは十分か」
```

### レイヤー3: 人間によるレビュー
- コードレビュー
- 要件との照合
- 実際の動作確認

## 統計と研究

### 検出精度
- Semantic Entropyアルゴリズム：**79%の精度**
- SelfCheckGPT：中程度の精度
- 人間の専門家：最も高い精度（ただし時間がかかる）

### 発生頻度
研究によると：
- 単純なタスク：低頻度
- 複雑なタスク：高頻度
- ドメイン固有の知識：非常に高頻度

## ガードレールの設定

### 詳細な設計書

```markdown
## API仕様

### エンドポイント
POST /api/users

### リクエスト
{
  "email": "string (必須, メール形式)",
  "password": "string (必須, 8文字以上)",
  "name": "string (必須, 2-50文字)"
}

### レスポンス（成功）
HTTP 201 Created
{
  "id": 123,
  "email": "user@example.com",
  "name": "User Name",
  "createdAt": "2025-01-06T12:00:00Z"
}

### レスポンス（失敗）
HTTP 400 Bad Request
{
  "error": "VALIDATION_ERROR",
  "message": "Email already exists",
  "field": "email"
}

### 実装要件
- Spring Boot 3.2
- Spring Data JPA
- PostgreSQL
- Jakarta Bean Validation
```

このような詳細な仕様により、AIが勝手に仕様を「創作」することを防ぐ。

## ベストプラクティス

### 1. 常に検証
- AI の出力を盲目的に信頼しない
- コンパイル、テスト、レビューを実施
- 実際の動作を確認

### 2. 段階的なアプローチ
- 小さな単位で実装
- 各ステップで検証
- 問題を早期に発見

### 3. 明確な基準
- 受入条件を明確に
- テストケースを事前に定義
- 完了の定義を共有

### 4. 複数の情報源
- 公式ドキュメントを参照
- 複数のAIで確認
- 人間の専門家に相談

## 参考資料

### 学術研究
- [arXiv: Semantic Entropy Algorithm](https://arxiv.org/abs/2406.15927)
- [MIT: Addressing AI Hallucinations](https://mitsloanedtech.mit.edu/ai/basics/addressing-ai-hallucinations-and-bias/)

### 実践ガイド
- [NN/G: AI Hallucinations - What Designers Need to Know](https://www.nngroup.com/articles/ai-hallucinations/)
- [DigitalOcean: Understanding and Mitigating AI Hallucination](https://www.digitalocean.com/resources/articles/ai-hallucination)
- [TechTarget: Managing Generative AI Hallucinations](https://www.techtarget.com/searchenterpriseai/tip/A-short-guide-to-managing-generative-AI-hallucinations)

### Wikipedia
- [Hallucination (artificial intelligence)](https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence))

## まとめ

AI Hallucination（虚偽報告）は、AI開発における深刻な問題。対策として：

1. **RAG**で信頼できる情報源を参照
2. **詳細なプロンプト**でソースを明示
3. **検証可能な受入条件**を設定
4. **段階的な検証**（自動＋AI自己チェック＋人間）
5. **Trust but Verify**を徹底

完全に防ぐことは現時点では不可能だが、適切な緩和策により、リスクを大幅に削減できる。
