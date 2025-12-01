# Guardrails（ガードレール）

## 定義

Guardrails（ガードレール）は、AIが生成するコードや決定に対する境界線や制約を設定する手法。詳細な設計書、技術仕様、ルール文書を通じて、AIが「道を外れる」ことを防ぎ、望ましい範囲内で動作するようにガイドする。

## メタファー

高速道路のガードレールと同じ：
- **許可**: 道路（許可された範囲）内で自由に運転できる
- **防止**: 道を外れて崖から落ちることを防ぐ
- **ガイド**: 安全な経路を示す

AIにとってのガードレールは、詳細な仕様書やルール文書が相当する。

## なぜ必要なのか

### AIの問題に対する事前防止策

Guardrailsは、以下のAI問題を**事前に防止**する：

1. **Scope Creep（暴走）** → 実装範囲を明確に制限
2. **Jagged Intelligence（凸凹な知能）** → 苦手分野での判断を人間が事前に決定
3. **Reward Hacking（手抜き）** → 受入条件を明確に定義
4. **Hallucination（虚偽報告）** → 使用可能なAPIやライブラリを明示
5. **Context Limitations（忘れっぽさ）** → 外部文書でルールを永続化

## Guardrailsの種類

### 1. プロジェクトレベルのガードレール

#### CLAUDE.md

プロジェクトルートに配置する「憲法」：

```markdown
# プロジェクトルール

## アーキテクチャ原則

### レイヤー構造（必須）
```
Controller → Service → Repository
```
- Controllerから直接Repositoryにアクセス禁止
- Serviceレイヤーをスキップしてはならない
- 各レイヤーは下位レイヤーのみに依存

### 依存性注入
- フィールドインジェクション禁止
- コンストラクタインジェクションのみ使用
- `@Autowired`はコンストラクタに付けない（暗黙的）

```java
// ✅ 正しい
public class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}

// ❌ 禁止
public class UserService {
    @Autowired
    private UserRepository repository;
}
```

## セキュリティ要件

### パスワード管理
- BCryptPasswordEncoderを必ず使用
- ストレングス: 10以上
- 平文保存は絶対禁止

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(10);
}
```

### 認証・認可
- Spring Security 6.2使用
- JWTトークンの有効期限: 24時間
- リフレッシュトークン: 7日間

## データベース規約

### エンティティ（必須）
すべてのエンティティは`Auditable`クラスを継承：

```java
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class Auditable {
    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @CreatedBy
    @Column(nullable = false, updatable = false)
    private String createdBy;

    @LastModifiedBy
    @Column(nullable = false)
    private String lastModifiedBy;
}
```

すべての新規エンティティ：
```java
@Entity
@Table(name = "users")
public class User extends Auditable {
    // フィールド定義
}
```

### トランザクション
- Serviceレイヤーのpublicメソッドに`@Transactional`
- 読み取り専用の場合: `@Transactional(readOnly = true)`
- デフォルト分離レベル: READ_COMMITTED

## エラーハンドリング

### 例外階層
```
RuntimeException
├── BusinessException（ビジネスロジックエラー）
│   ├── DuplicateEmailException
│   ├── InsufficientStockException
│   └── InvalidOrderStateException
├── ValidationException（バリデーションエラー）
│   ├── InvalidEmailFormatException
│   └── PasswordTooWeakException
└── DataAccessException（データアクセスエラー）
    ├── EntityNotFoundException
    └── DatabaseConnectionException
```

### グローバル例外ハンドラ
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(
            BusinessException ex) {
        return ResponseEntity
            .status(HttpStatus.BAD_REQUEST)
            .body(new ErrorResponse(ex.getErrorCode(), ex.getMessage()));
    }

    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            ValidationException ex) {
        return ResponseEntity
            .status(HttpStatus.UNPROCESSABLE_ENTITY)
            .body(new ErrorResponse(ex.getErrorCode(), ex.getMessage()));
    }
}
```

## テスト戦略

### テストの種類と責任
- **@DataJpaTest**: Repositoryの単体テスト
- **@WebMvcTest**: Controllerの単体テスト
- **@SpringBootTest**: Serviceの統合テスト、E2Eテスト

### 必須カバレッジ
- Serviceレイヤー: 80%以上
- Repositoryレイヤー: 70%以上
- Controllerレイヤー: 70%以上

### テストケース命名規則
```java
@Test
void testMethodName_condition_expectedResult() {
    // Given - When - Then
}
```

例：
```java
@Test
void testCreateUser_withValidData_shouldReturnCreatedUser() {
    // テストコード
}

@Test
void testCreateUser_withDuplicateEmail_shouldThrowException() {
    // テストコード
}
```

## コーディング規約

### 命名規則
- クラス: PascalCase（例: UserService）
- メソッド: camelCase（例: createUser）
- 定数: UPPER_SNAKE_CASE（例: MAX_RETRY_COUNT）
- パッケージ: 小文字（例: com.example.userservice）

### メソッド長
- 最大40行
- それ以上の場合は分割

### Cyclomatic Complexity
- メソッド: 最大10
- クラス: 最大50

## 使用ライブラリ（許可リスト）

### 必須
- Spring Boot 3.2.x
- Spring Data JPA
- Spring Security 6.2.x
- PostgreSQL JDBC Driver
- Lombok
- Jakarta Bean Validation

### 推奨
- MapStruct（DTO変換）
- Liquibase（DBマイグレーション）
- Testcontainers（統合テスト）

### 禁止
- Hibernate直接使用（Spring Data JPAを使用）
- java.util.Date（LocalDateTime使用）
- StringBuffer（StringBuilder使用）
```

**効果**:
- AIが新しいコードを生成する際、自動的にこのルールを参照
- プロジェクト全体で一貫性が保たれる
- Compact後もルールが失われない

### 2. タスクレベルのガードレール

#### GitHub Issues

各タスクに詳細な仕様を記載：

```markdown
## Issue #123: ユーザー登録機能の実装

### 背景
新規ユーザーがシステムに登録できる機能を実装する。

### 実装範囲（明示的な制限）

#### 実装するもの
1. `POST /api/users` エンドポイント
2. UserController.createUser() メソッド
3. UserService.createUser() メソッド
4. CreateUserRequest DTO
5. UserResponse DTO
6. DuplicateEmailException

#### 実装しないもの（スコープ外）
- ❌ メール送信機能（別issue #124で実装予定）
- ❌ メール確認機能（別issue #125で実装予定）
- ❌ プロフィール画像アップロード（別issue #126で実装予定）
- ❌ ソーシャルログイン（将来的な拡張）
- ❌ 2要素認証（将来的な拡張）

### 技術仕様

#### エンドポイント
```
POST /api/users
Content-Type: application/json
```

#### リクエスト
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

#### レスポンス（成功）
```json
HTTP 201 Created
Location: /api/users/123

{
  "id": 123,
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2025-01-06T12:00:00Z"
}
```

#### レスポンス（失敗 - 重複メール）
```json
HTTP 400 Bad Request

{
  "errorCode": "DUPLICATE_EMAIL",
  "message": "Email already exists",
  "field": "email"
}
```

#### レスポンス（失敗 - バリデーション）
```json
HTTP 422 Unprocessable Entity

{
  "errorCode": "VALIDATION_ERROR",
  "message": "Invalid email format",
  "field": "email"
}
```

### 受入条件（GIVEN WHEN THEN）

#### シナリオ1: 正常なユーザー登録
```
GIVEN: 新しいユーザー情報が提供される
  AND: メールアドレスが有効な形式
  AND: パスワードが8文字以上
  AND: そのメールアドレスは未登録
WHEN: POST /api/users を呼び出す
THEN: HTTP 201 Createdが返される
  AND: レスポンスボディにユーザー情報が含まれる
  AND: パスワードはBCryptでハッシュ化されてDBに保存される
  AND: createdAt, updatedAtが自動設定される
  AND: LocationヘッダーにユーザーリソースのURLが含まれる
```

#### シナリオ2: 重複メールアドレス
```
GIVEN: 既に登録済みのメールアドレス
WHEN: 同じメールアドレスで POST /api/users を呼び出す
THEN: HTTP 400 Bad Requestが返される
  AND: エラーコード "DUPLICATE_EMAIL" が含まれる
  AND: データベースには保存されない
```

#### シナリオ3: 無効なメール形式
```
GIVEN: 無効な形式のメールアドレス（例: "invalid-email"）
WHEN: POST /api/users を呼び出す
THEN: HTTP 422 Unprocessable Entityが返される
  AND: エラーコード "VALIDATION_ERROR" が含まれる
  AND: データベースには保存されない
```

#### シナリオ4: 弱いパスワード
```
GIVEN: 8文字未満のパスワード
WHEN: POST /api/users を呼び出す
THEN: HTTP 422 Unprocessable Entityが返される
  AND: エラーコード "VALIDATION_ERROR" が含まれる
  AND: データベースには保存されない
```

### 技術的制約

#### 使用技術
- Spring Boot 3.2.x
- Spring Data JPA
- Spring Security（BCryptPasswordEncoder）
- Jakarta Bean Validation
- PostgreSQL

#### アーキテクチャ
- CLAUDE.mdの3層アーキテクチャに従う
- コンストラクタインジェクション使用
- @Transactional必須

#### セキュリティ
- パスワードはBCryptでハッシュ化（strength=10）
- レスポンスにパスワードを含めない

#### バリデーション
```java
public class CreateUserRequest {
    @NotNull(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotNull(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;

    @NotNull(message = "Name is required")
    @Size(min = 2, max = 50, message = "Name must be between 2 and 50 characters")
    private String name;
}
```

### テスト要件

#### 単体テスト
1. UserService.createUser() - 正常系
2. UserService.createUser() - 重複メール
3. UserService.createUser() - パスワードハッシュ化確認

#### 統合テスト
1. POST /api/users - 正常系（@SpringBootTest）
2. POST /api/users - 重複メール（@SpringBootTest）
3. POST /api/users - 無効なメール（@SpringBootTest）
4. POST /api/users - 弱いパスワード（@SpringBootTest）

#### カバレッジ目標
- UserService: 80%以上
- UserController: 70%以上

### 変更ファイル

#### 新規作成
- `src/main/java/com/example/controller/UserController.java`
- `src/main/java/com/example/service/UserService.java`
- `src/main/java/com/example/dto/CreateUserRequest.java`
- `src/main/java/com/example/dto/UserResponse.java`
- `src/main/java/com/example/exception/DuplicateEmailException.java`
- `src/test/java/com/example/service/UserServiceTest.java`
- `src/test/java/com/example/controller/UserControllerTest.java`

#### 変更
- なし（既存コードの変更なし）

### 完了の定義（DoD）

- [ ] すべての受入条件を満たす実装が完了
- [ ] すべてのテストが通る
- [ ] テストカバレッジが目標を達成
- [ ] コンパイルエラーなし
- [ ] CheckStyle、PMD、SpotBugsで警告なし
- [ ] CLAUDE.mdのルールに準拠
- [ ] コードレビュー承認
- [ ] ドキュメント更新（必要な場合）

### 参照ドキュメント
- CLAUDE.md（プロジェクトルール）
- docs/adr/0001-password-encryption.md
- docs/adr/0003-error-handling.md
- docs/adr/0005-rest-api-design.md
```

**効果**:
- AIが「何を実装すべきか」「何を実装すべきでないか」を明確に理解
- Scope Creep（暴走）を防止
- 受入条件が明確なため、Reward Hacking（手抜き）を防止

### 3. アーキテクチャレベルのガードレール

#### Architecture Decision Records (ADR)

重要な技術的決定を文書化：

**`docs/adr/0001-password-encryption.md`**:
```markdown
# 1. パスワードの暗号化にBCryptを使用

## Status
Accepted

## Context
ユーザーのパスワードを安全に保存する必要がある。以下の選択肢を検討：
1. BCrypt
2. PBKDF2
3. Argon2
4. SCrypt

## Decision
BCryptPasswordEncoderを使用してパスワードをハッシュ化する。

## Rationale
- **業界標準**: 広く使用され、信頼されている
- **Spring統合**: Spring Securityとの統合が容易
- **自動ソルト**: ソルトを自動生成
- **調整可能**: ストレングスを調整可能
- **後方互換性**: 将来的にストレングスを上げても既存パスワードが動作

他の選択肢を却下した理由：
- PBKDF2: BCryptより若干劣る
- Argon2: Spring Securityの標準サポートがない（2024年時点）
- SCrypt: メモリ集約的すぎる

## Consequences

### Positive
- 業界標準のセキュリティ
- Spring Securityとの統合が容易
- ソルト自動生成
- 調整可能なストレングス

### Negative
- 若干のパフォーマンスオーバーヘッド（許容範囲内）

## Implementation

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(10);
    }
}
```

### Usage
```java
@Service
public class UserService {
    private final PasswordEncoder passwordEncoder;

    public UserService(PasswordEncoder passwordEncoder) {
        this.passwordEncoder = passwordEncoder;
    }

    public User createUser(CreateUserRequest request) {
        User user = new User();
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        return userRepository.save(user);
    }
}
```

## References
- [Spring Security BCrypt](https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html#authentication-password-storage-bcrypt)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

## Date
2025-01-06

## Author
Development Team
```

**効果**:
- AIが新しいパスワード関連コードを書く際、必ずBCryptを使用
- 他の開発者やAIが「なぜBCryptなのか」を理解
- 将来的な変更（Argon2への移行など）の判断材料

### 4. APIレベルのガードレール

#### OpenAPI Specification

API仕様を明示：

**`docs/openapi.yaml`**:
```yaml
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0

paths:
  /api/users:
    post:
      summary: Create a new user
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created successfully
          headers:
            Location:
              description: URL of the created user
              schema:
                type: string
                example: /api/users/123
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          description: Duplicate email
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                errorCode: DUPLICATE_EMAIL
                message: Email already exists
                field: email
        '422':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                errorCode: VALIDATION_ERROR
                message: Invalid email format
                field: email

components:
  schemas:
    CreateUserRequest:
      type: object
      required:
        - email
        - password
        - name
      properties:
        email:
          type: string
          format: email
          example: user@example.com
        password:
          type: string
          format: password
          minLength: 8
          example: SecurePass123!
        name:
          type: string
          minLength: 2
          maxLength: 50
          example: John Doe

    UserResponse:
      type: object
      properties:
        id:
          type: integer
          format: int64
          example: 123
        email:
          type: string
          format: email
          example: user@example.com
        name:
          type: string
          example: John Doe
        createdAt:
          type: string
          format: date-time
          example: 2025-01-06T12:00:00Z

    ErrorResponse:
      type: object
      properties:
        errorCode:
          type: string
          example: DUPLICATE_EMAIL
        message:
          type: string
          example: Email already exists
        field:
          type: string
          example: email
```

**効果**:
- AIがAPI実装時に正確な仕様に従う
- Hallucination（存在しないフィールドや構造）を防止
- フロントエンド開発者との契約として機能

## Guardrailsの実装パターン

### パターン1: 事前制約（Pre-constraint）

タスク開始前にルールを明示：

```
「UserServiceを実装してください。

制約:
- CLAUDE.mdのルールに必ず従うこと
- docs/adr/0001-password-encryption.md を参照してBCrypt使用
- GitHub issue #123の仕様に正確に従うこと
- 実装範囲: issue #123の「実装するもの」のみ
- 禁止: issue #123の「実装しないもの」に記載の機能」
```

### パターン2: チェックリスト強制（Checklist Enforcement）

実装前にチェックリストを確認：

```
「実装を開始する前に、以下のチェックリストを確認してください:

- [ ] CLAUDE.mdを読んだか
- [ ] docs/adr/関連するADRを確認したか
- [ ] GitHub issueの仕様を理解したか
- [ ] 実装範囲が明確か
- [ ] 使用する技術が許可リストにあるか
- [ ] 既存コードのパターンを確認したか

すべてチェックしたら、実装計画を提示してください。」
```

### パターン3: 段階的承認（Staged Approval）

実装前に計画をレビュー：

```
開発者: 「UserServiceを実装してください」

AI: 「実装計画:
    1. CreateUserRequest DTO作成
    2. UserService.createUser()実装
       - BCryptでパスワードハッシュ化
       - 重複メールチェック
       - Auditable継承
    3. UserController.createUser()実装
    4. テスト作成

    この計画で進めてよろしいですか？」

開発者: 「OK」または「修正: ○○は不要」

AI: 実装開始
```

### パターン4: 定期的な確認（Periodic Check）

長時間セッションでの定期確認：

```
【30分ごと】
「これまでの実装がCLAUDE.mdのルールに従っているか確認してください。
 違反があれば指摘してください。」
```

## 具体的な問題防止例

### 例1: Scope Creep（暴走）の防止

#### Guardrailなし
```
開発者: 「UserServiceを実装してください」

AI: 了解しました。（暴走して以下を実装）
    - ユーザー登録
    - メール送信
    - 通知
    - 監査ログ
    - プロフィール画像処理
    - 推奨ユーザー
```

#### Guardrailあり（GitHub Issue）
```markdown
## Issue #123

### 実装するもの
- UserService.createUser()のみ

### 実装しないもの
- ❌ メール送信
- ❌ 通知
- ❌ 監査ログ
```

```
開発者: 「Issue #123に従ってUserServiceを実装してください」

AI: 了解しました。Issue #123の仕様を確認しました。
    実装範囲: UserService.createUser()のみ
    メール送信等は実装しません。
```

✅ **暴走防止成功**

### 例2: Hallucination（虚偽報告）の防止

#### Guardrailなし
```java
// AIが勝手に存在しないアノテーションを使用
@SmartQuery(optimize = true)  // 存在しない
List<User> findAllOptimized();
```

#### Guardrailあり（CLAUDE.md）
```markdown
## 使用ライブラリ（許可リスト）

### 必須
- Spring Boot 3.2.x
- Spring Data JPA
- Spring Security 6.2.x

### 禁止
- 許可リストにないライブラリは使用禁止
```

```
開発者: 「CLAUDE.mdの許可リストに従って、UserRepositoryを実装してください」

AI: 了解しました。許可リストを確認しました。
    Spring Data JPAの標準機能のみ使用します。
```

```java
// 標準的な実装
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
}
```

✅ **虚偽報告防止成功**

### 例3: Jagged Intelligence（苦手分野）の補完

#### Guardrailなし
```
開発者: 「OrderServiceを実装してください」

AI: （複雑なビジネスロジックを誤って実装）
    - 在庫引き当てのタイミングが不適切
    - トランザクション境界が誤り
    - ロールバック戦略が不完全
```

#### Guardrailあり（詳細な設計書）
```markdown
## OrderService設計書

### ビジネスロジックフロー
1. 在庫チェック（ロックなし）
2. 注文レコード作成（status=PENDING）
3. 在庫引き当て（楽観的ロック）
4. 支払い処理
5. 注文ステータス更新（status=CONFIRMED）

### トランザクション境界
- メソッド全体を@Transactionalで囲む
- 分離レベル: READ_COMMITTED

### ロールバック戦略
- 支払い失敗時: 全ロールバック
- 在庫不足時: BusinessException（ロールバック）

### エラーハンドリング
- 在庫不足: InsufficientStockException
- 支払い失敗: PaymentFailedException
```

```
開発者: 「docs/design/order-service.mdの設計に従って、OrderServiceを実装してください」

AI: 了解しました。設計書を確認しました。
    フロー通りに実装します。
```

✅ **苦手分野での誤り防止成功**

### 例4: Context Limitations（忘れっぽさ）の克服

#### Guardrailなし
```
【セッション開始】
開発者: 「すべてのエンティティはAuditableを継承してください」

【Compact後】
AI: （忘れる）
```

```java
@Entity
public class Product {
    // Auditableを継承していない
}
```

#### Guardrailあり（CLAUDE.md）
```markdown
## データベース規約

### エンティティ（必須）
すべてのエンティティは`Auditable`クラスを継承：

```java
@Entity
public class EntityName extends Auditable {
    // 実装
}
```
```

```
【Compact後】
開発者: 「CLAUDE.mdに従って、Productエンティティを作成してください」

AI: 了解しました。CLAUDE.mdを確認しました。
    Auditableを継承します。
```

```java
@Entity
@Table(name = "products")
public class Product extends Auditable {
    // 実装
}
```

✅ **忘却防止成功**

## ベストプラクティス

### 1. 階層的なGuardrails

```
【レベル1: プロジェクト全体】
CLAUDE.md
├── アーキテクチャ原則
├── セキュリティ要件
├── コーディング規約
└── 使用ライブラリ

【レベル2: 技術的決定】
docs/adr/
├── 0001-password-encryption.md
├── 0002-database-choice.md
└── 0003-error-handling.md

【レベル3: 機能単位】
GitHub Issues
├── #123: ユーザー登録
├── #124: メール送信
└── #125: メール確認

【レベル4: API仕様】
docs/openapi.yaml
docs/database-schema.sql
```

### 2. 明示的な参照

AIに何を参照すべきか明示：

```
「以下のドキュメントを参照して実装してください:
- CLAUDE.md（全体ルール）
- docs/adr/0001-password-encryption.md（パスワード暗号化）
- GitHub issue #123（仕様）
- docs/openapi.yaml（API仕様）」
```

### 3. 実装前の計画確認

```
「実装前に、計画を提示してください。
 計画にはCLAUDE.mdとissue #123への参照を含めてください。」
```

### 4. 定期的なルール再確認

```
【30分ごと】
「CLAUDE.mdのルールを再確認してください。
 これまでの実装に違反がないかチェックしてください。」
```

### 5. Custom Commandsでの自動化

**`.claude/commands/implement.md`**:
```markdown
新しい機能を実装する際は、以下の手順に従うこと:

1. CLAUDE.mdを確認
2. 関連するADRを確認
3. GitHub issueの仕様を確認
4. 実装計画を提示
5. 承認後に実装開始
6. 実装後、自己レビュー実施
```

使用方法：
```
/implement #123
```

## ツールとの統合

### IDE統合

#### IntelliJ IDEA
```xml
<!-- .idea/inspections/Project_Default.xml -->
<component name="InspectionProjectProfileManager">
  <profile version="1.0">
    <option name="myName" value="CLAUDE.md Enforcement" />
    <inspection_tool class="FieldCanBeLocal" enabled="true" level="ERROR" />
    <!-- カスタムインスペクション -->
  </profile>
</component>
```

### CI/CD統合

```yaml
# .github/workflows/guardrails-check.yml
name: Guardrails Check

on: [push, pull_request]

jobs:
  check-compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # CLAUDE.mdルールのチェック
      - name: Check Auditable Inheritance
        run: |
          # すべてのエンティティがAuditableを継承しているかチェック
          find src/main/java -name "*Entity.java" | while read file; do
            if ! grep -q "extends Auditable" "$file"; then
              echo "ERROR: $file does not extend Auditable"
              exit 1
            fi
          done

      # 禁止ライブラリのチェック
      - name: Check Forbidden Libraries
        run: |
          if grep -r "@Autowired" src/main/java --include="*.java" | grep "private"; then
            echo "ERROR: Field injection found (forbidden by CLAUDE.md)"
            exit 1
          fi
```

## 参考資料

### ベストプラクティス
- [Anthropic: Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [OpenAI: GPT Best Practices](https://platform.openai.com/docs/guides/gpt-best-practices)

### ツール
- [ADR Tools](https://github.com/npryce/adr-tools)
- [OpenAPI Generator](https://openapi-generator.tech/)
- [CheckStyle](https://checkstyle.sourceforge.io/)

### 概念
- [Design by Contract](https://en.wikipedia.org/wiki/Design_by_contract)
- [Defensive Programming](https://en.wikipedia.org/wiki/Defensive_programming)

## まとめ

Guardrails（ガードレール）は、AIが望ましい範囲内で動作するよう導く境界線と制約。

### 主要なGuardrails
1. **CLAUDE.md**: プロジェクト全体のルール
2. **ADR**: 技術的決定の記録
3. **GitHub Issues**: タスク仕様と実装範囲
4. **OpenAPI Spec**: API仕様

### 防止できるAI問題
- Scope Creep（暴走）→ 実装範囲の明確化
- Hallucination（虚偽報告）→ 許可リストによる制限
- Jagged Intelligence（苦手分野）→ 詳細な設計書
- Context Limitations（忘れっぽさ）→ 外部文書での永続化
- Reward Hacking（手抜き）→ 明確な受入条件

Guardrailsは「Trust but Verify」の「Trust」を可能にする基盤。適切な境界線を設定することで、AIに安心して作業を委任できる。
