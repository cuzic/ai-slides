# Context Limitations（コンテキスト制限・忘れっぽさ）

## 定義

Context Limitations（コンテキスト制限）は、AIの作業メモリが有限であることにより、長い会話やセッション中に以前の情報を「忘れる」現象。AIは過去の会話全体を保持できず、トークン制限により古い情報が失われる。

## 別名

- **忘れっぽさ**
- **Context Window Problem（コンテキストウィンドウ問題）**
- **Token Limit Issue（トークン制限問題）**
- **Memory Loss（記憶喪失）**

## 基本概念

### トークンとは
AIモデルは、テキストを「トークン」という単位で処理：
- 1トークン ≈ 0.75語（英語）
- 1トークン ≈ 0.5-1文字（日本語）
- 入力と出力の合計トークン数に制限がある

### コンテキストウィンドウ
- **Claude 3.5 Sonnet**: 200,000トークン（約15万語）
- **GPT-4 Turbo**: 128,000トークン
- **GPT-3.5**: 16,000トークン

一見大きく見えるが、長時間の開発セッションでは不足。

## 具体的な問題

### 問題1: 長時間セッションでの忘却

```
【セッション開始】
開発者: Spring BootでUserServiceを作成してください。
        ただし、必ずBCryptを使ってパスワードをハッシュ化すること。

AI: 了解しました。BCryptでパスワードをハッシュ化します。

【30分後、多くのやり取りの後】
開発者: 次にPasswordResetServiceを作成してください。

AI: 了解しました。以下のように実装します：
```

```java
@Service
public class PasswordResetService {
    public void resetPassword(User user, String newPassword) {
        // BCryptの指示を忘れ、平文で保存
        user.setPassword(newPassword);
        userRepository.save(user);
    }
}
```

**問題**: 最初に指定したBCrypt要件を忘れた。

### 問題2: Compact後の完全な記憶喪失

Claude Codeには「Compact」機能があり、会話履歴を圧縮：
- 古い会話を要約して保存
- 詳細な情報が失われる
- **カスタムコマンド、特別な指示、プロジェクト固有のルールが消える**

```
【Compact前】
開発者: このプロジェクトでは、すべてのエンティティに
        必ずAuditableクラスを継承させてください。

AI: 了解しました。すべてのエンティティにAuditableを継承させます。

【Compact実行】

【Compact後】
開発者: ProductエンティティとOrderエンティティを作成してください。

AI: 了解しました。
```

```java
// Auditableの継承を忘れる
@Entity
public class Product {
    @Id
    private Long id;
    private String name;
    // createdAt、updatedAtなどのAuditフィールドが欠落
}
```

### 問題3: 設計書の喪失

```
【セッション中盤】
開発者: エラーハンドリングについて：
        - ビジネスロジックエラー → BusinessException
        - バリデーションエラー → ValidationException
        - データベースエラー → DataAccessException
        これを統一ルールとしてください。

AI: 了解しました。

【多くのコードを実装後】
開発者: OrderService にエラーハンドリングを追加してください。

AI: 了解しました。
```

```java
@Service
public class OrderService {
    public Order createOrder(OrderRequest request) {
        try {
            // ... ビジネスロジック
        } catch (Exception e) {
            // 統一ルールを忘れ、汎用的なExceptionを使用
            throw new RuntimeException("Order creation failed", e);
        }
    }
}
```

## Java開発での影響

### 影響1: アーキテクチャの一貫性喪失

```java
// セッション初期に決定したレイヤー構造
Controller → Service → Repository

// 後半で作成されたコード（一貫性が崩れる）
@RestController
public class ProductController {
    @Autowired
    private ProductRepository repository; // Serviceをスキップ

    @GetMapping("/products/{id}")
    public Product getProduct(@PathVariable Long id) {
        return repository.findById(id).orElse(null);
    }
}
```

### 影響2: コーディング規約の不一致

```java
// 最初に決めた規約: DTOは必ずバリデーションアノテーション付き
public class CreateUserRequest {
    @NotNull
    @Email
    private String email;

    @NotNull
    @Size(min = 8)
    private String password;
}

// 後で作成されたDTO（規約を忘れる）
public class CreateProductRequest {
    private String name;  // バリデーションなし
    private BigDecimal price;  // バリデーションなし
}
```

### 影響3: テスト戦略の不一致

```java
// 最初に決めたテスト方針: すべてのServiceは@SpringBootTest
@SpringBootTest
class UserServiceTest {
    @Autowired
    private UserService userService;

    @Test
    void testCreateUser() {
        // 統合テスト
    }
}

// 後で作成されたテスト（方針を忘れる）
@ExtendWith(MockitoExtension.class)  // 単体テストに変更
class ProductServiceTest {
    @Mock
    private ProductRepository repository;

    @InjectMocks
    private ProductService productService;

    @Test
    void testCreateProduct() {
        // 単体テスト
    }
}
```

## なぜ発生するのか

### 1. トークン制限
- 物理的な制約（メモリ、計算コスト）
- 入力 + 出力の合計がコンテキストウィンドウを超えると古い情報が削除される

### 2. 優先順位付け
AIは最近の会話を優先：
- 直近の指示が最も重視される
- 古い指示は「重要度が低い」と判断される

### 3. Compactによる情報損失
- 要約プロセスで詳細が失われる
- 「重要」と判断されなかった情報が削除される
- プロジェクト固有のルールが一般化される

## 対策と解決策

### 1. CLAUDE.md - プロジェクトの憲法

プロジェクトルートに`CLAUDE.md`を配置：

```markdown
# プロジェクトルール

## アーキテクチャ
- 3層アーキテクチャ: Controller → Service → Repository
- Serviceレイヤーを必ずスキップしない

## セキュリティ
- パスワードは必ずBCryptPasswordEncoderでハッシュ化
- 平文での保存は厳禁

## エンティティ
- すべてのエンティティはAuditableクラスを継承
- @EntityListenersは必須

```java
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class Auditable {
    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;
}
```

## エラーハンドリング
- ビジネスロジックエラー: BusinessException
- バリデーションエラー: ValidationException
- データベースエラー: DataAccessException

## テスト戦略
- Serviceクラスは@SpringBootTestで統合テスト
- Repositoryは@DataJpaTestで単体テスト
- Controllerは@WebMvcTestで単体テスト

## DTOバリデーション
- すべてのリクエストDTOに適切なバリデーションアノテーション
- @NotNull, @Email, @Size, @Min, @Maxを活用
```

このファイルをAIに定期的に参照させる。

### 2. Custom Commands（カスタムコマンド）

`.claude/commands/`ディレクトリにプロジェクト固有のコマンドを保存：

**`.claude/commands/create-entity.md`**:
```markdown
新しいエンティティを作成する際は、以下のテンプレートに従うこと：

\`\`\`java
@Entity
@Table(name = "テーブル名")
public class エンティティ名 extends Auditable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // フィールド定義

    // Getter/Setter（Lombokの場合は @Data）
}
\`\`\`

必須事項：
- Auditableクラスの継承
- @Entityと@Tableアノテーション
- ID生成戦略の明示
```

**`.claude/commands/create-service.md`**:
```markdown
新しいServiceクラスを作成する際は、以下のテンプレートに従うこと：

\`\`\`java
@Service
@Transactional(readOnly = true)
public class EntityService {

    private final EntityRepository repository;

    public EntityService(EntityRepository repository) {
        this.repository = repository;
    }

    @Transactional
    public Entity create(CreateEntityRequest request) {
        // ビジネスロジック
    }
}
\`\`\`

必須事項：
- コンストラクタインジェクション
- @Transactionalの適切な使用
- 統一されたエラーハンドリング
```

使用方法：
```bash
/create-entity Product
/create-service ProductService
```

### 3. Architecture Decision Records (ADR)

重要な技術的決定を記録：

**`docs/adr/0001-password-encryption.md`**:
```markdown
# 1. パスワードの暗号化にBCryptを使用

## Status
Accepted

## Context
ユーザーのパスワードを安全に保存する必要がある。

## Decision
BCryptPasswordEncoderを使用してパスワードをハッシュ化する。

## Consequences
### Positive
- 業界標準のセキュリティ
- Spring Securityとの統合が容易
- ソルト自動生成

### Negative
- 若干のパフォーマンスオーバーヘッド

## Implementation
\`\`\`java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
\`\`\`
```

AIに定期的にADRを参照させる：
```
docs/adr/にある技術的決定を確認してから実装してください
```

### 4. 定期的なリマインダー

長時間セッションでは定期的に重要事項を再確認：

```
【30分ごとに実施】
「CLAUDE.md の内容を確認して、
 これから実装するコードが
 プロジェクトルールに従っているか
 チェックしてください」
```

### 5. チェックリスト方式

各タスクに必須チェック項目を含める：

```markdown
## UserService実装タスク

### 実装内容
- UserService.createUser() メソッド

### 必須チェック項目
- [ ] CLAUDE.mdのルールに従っているか
- [ ] BCryptでパスワードハッシュ化
- [ ] 統一されたエラーハンドリング
- [ ] @Transactionalの適切な使用
- [ ] テストが@SpringBootTestで書かれているか
```

### 6. MCP Server: Serena（外部メモリ）

Serena MCP Serverを使用してプロジェクト全体のコンテキストを維持：

**利点**:
- Language Server Protocolで効率的にコードを参照
- トークン使用量を削減
- 既存コードのパターンを継続的に参照可能

```
Claude Code + Serena MCP Server
→ 既存コードのパターンを常に参照
→ アーキテクチャの一貫性を保つ
```

### 7. GitHub Issues での明示的な設計書

各issueに詳細な仕様を含める：

```markdown
## Issue #123: ProductService実装

### 技術要件
- Spring Boot 3.2
- BCryptでパスワードハッシュ化（CLAUDE.md参照）
- 3層アーキテクチャ遵守（CLAUDE.md参照）

### エラーハンドリング
docs/adr/0003-error-handling.md に従う：
- BusinessException
- ValidationException
- DataAccessException

### テスト要件
- @SpringBootTestで統合テスト
- 最低3つのテストケース

### 参照ドキュメント
- CLAUDE.md（プロジェクトルール）
- docs/adr/0001-password-encryption.md
- docs/adr/0003-error-handling.md
```

## 統計とデータ

### コンテキストウィンドウの消費

典型的なJava開発セッションでのトークン消費：
- コード実装: 500-2000トークン/ファイル
- ドキュメント: 1000-3000トークン
- 会話履歴: 100-500トークン/やり取り

30分のセッションで50回のやり取り：
- 会話履歴: 5,000-25,000トークン
- コード: 10,000-40,000トークン
- 合計: 15,000-65,000トークン

200,000トークンのコンテキストウィンドウでも、2-3時間で満杯になる可能性。

### Compactの影響

Compact実行後：
- 会話履歴が**要約**される
- 詳細な指示が**一般化**される
- プロジェクト固有のルールが**失われる**可能性が高い

## 実践的なワークフロー

### ステップ1: セッション開始時
```
「CLAUDE.mdとdocs/adr/の内容を確認してください。
 これから実装するコードがこれらのルールに
 従うようにしてください。」
```

### ステップ2: 各タスク開始時
```
「ProductServiceを実装する前に、
 既存のUserServiceを参照して、
 同じパターンで実装してください。」
```

### ステップ3: Compact前
```
「Compactを実行する前に、
 重要な決定事項をCLAUDE.mdまたは
 docs/adr/に記録してください。」
```

### ステップ4: Compact後
```
「CLAUDE.mdとdocs/adr/を再度確認してください。
 これらのルールを忘れずに実装を続けてください。」
```

### ステップ5: 定期的な確認（30分ごと）
```
「これまでの実装がCLAUDE.mdのルールに
 従っているか確認してください。
 不一致があれば指摘してください。」
```

## ベストプラクティス

### 1. 外部化
重要な情報をAIのメモリに依存せず外部化：
- **CLAUDE.md**: プロジェクトルール
- **ADR**: 技術的決定
- **Custom Commands**: 定型処理
- **GitHub Issues**: タスク仕様

### 2. 繰り返し
重要な指示は定期的に繰り返す：
- セッション開始時
- Compact後
- 30分ごと
- 新しいタスク開始時

### 3. 参照の明示
AIに何を参照すべきか明示：
```
docs/adr/0001-password-encryption.md を参照して、
パスワード暗号化を実装してください
```

### 4. パターンの共有
既存コードをテンプレートとして使用：
```
UserServiceと同じパターンでProductServiceを実装してください
```

## 参考資料

### Claude Code ドキュメント
- [Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Long Context Windows](https://www.anthropic.com/news/claude-3-5-sonnet)

### プラクティス
- [CLAUDE.md Pattern](https://docs.claude.com/claude-code/guides/best-practices)
- [Custom Commands](https://docs.claude.com/claude-code/guides/custom-commands)

### 学術的背景
- [The Limits of Context Windows in Large Language Models](https://arxiv.org/abs/2404.00199)

## まとめ

Context Limitations（忘れっぽさ）は、AIの物理的制約による問題。対策として：

1. **外部メモリの活用**: CLAUDE.md、ADR、Custom Commands
2. **定期的なリマインダー**: 重要事項を繰り返し確認
3. **MCP Server (Serena)**: 効率的なコード参照
4. **GitHub Issues**: 詳細な仕様書と参照ドキュメント
5. **Compact前後の対策**: 重要情報を文書化

AIのメモリに依存せず、プロジェクト知識を外部化することで、長期間にわたって一貫した開発を実現できる。
