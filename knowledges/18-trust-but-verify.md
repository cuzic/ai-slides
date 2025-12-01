# Trust but Verify（任せる＆確かめる）

## 定義

Trust but Verify（トラスト・バット・ベリファイ）は、AIに作業を委任しながらも、その出力を複数のレイヤーで検証する開発手法。AIの効率性を活用しつつ、品質と正確性を保証する実践的アプローチ。

## 語源

ロシア語の諺「доверяй, но проверяй（doveryai, no proveryai）」に由来。レーガン大統領が冷戦時代の核軍縮交渉で使用したことで有名になった。

> 「信頼するが、検証する」

## 基本原則

### Trust（任せる）
AIの強みを最大限に活用：
- 高速なコード生成
- パターンベースの実装
- ボイラープレートコードの自動化
- テストコードの生成

### Verify（確かめる）
複数のレイヤーで検証：
- 自動検証（コンパイル、テスト）
- AIによる自己検証
- 人間によるレビュー

## なぜ必要なのか

### AIの問題点に対する対策

Trust but Verifyは、以下のAI問題に対する包括的な対策：

1. **AI Hallucination（虚偽報告）** → 存在しないAPIやメソッドの検出
2. **Reward Hacking（手抜き）** → テストを通すだけの実装の発見
3. **Scope Creep（暴走）** → 指示していない機能の追加の検出
4. **Context Limitations（忘れっぽさ）** → ルール違反の発見
5. **Jagged Intelligence（凸凹な知能）** → 苦手分野での誤りの検出

## 検証の多層防御（Defense in Depth）

### レイヤー1: 自動検証

#### コンパイルチェック
```bash
# Javaプロジェクトのコンパイル
mvn compile

# エラー例
[ERROR] /src/main/java/com/example/UserService.java:[15,8]
cannot find symbol
  symbol:   class AutoOptimizer
  location: class com.example.UserService
```

**検出できる問題**:
- 存在しないクラス・メソッド（Hallucination）
- 構文エラー
- 型の不一致

#### 単体テスト
```bash
# ユニットテストの実行
mvn test

# 統合テストの実行
mvn verify
```

```java
@SpringBootTest
class UserServiceTest {

    @Autowired
    private UserService userService;

    @Autowired
    private UserRepository userRepository;

    @Test
    void testCreateUser_shouldHashPassword() {
        // GIVEN
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("test@example.com");
        request.setPassword("plainPassword");

        // WHEN
        User user = userService.createUser(request);

        // THEN
        assertNotEquals("plainPassword", user.getPassword());
        assertTrue(user.getPassword().startsWith("$2a$")); // BCrypt形式
    }

    @Test
    void testCreateUser_shouldThrowExceptionForDuplicate() {
        // GIVEN
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("existing@example.com");

        userService.createUser(request);

        // WHEN & THEN
        assertThrows(DuplicateEmailException.class, () -> {
            userService.createUser(request);
        });
    }
}
```

**検出できる問題**:
- ビジネスロジックの誤り
- エッジケースの未処理
- Reward Hacking（テストをパスするだけの実装）

#### 静的解析

静的解析ツールは、コードを実行せずにソースコードやバイトコードを分析し、潜在的な問題を検出します。

##### 1. CheckStyle（コーディング規約チェック）

**概要**: ソースコードがコーディング規約に準拠しているかをチェック

**検出できる問題**:
- インデント・スペースの不一致
- 命名規則違反（クラス名、メソッド名、変数名）
- JavaDocの欠如
- インポート文の順序
- マジックナンバー（ハードコードされた数値）

**導入方法**:
```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-checkstyle-plugin</artifactId>
    <version>3.3.1</version>
    <configuration>
        <configLocation>checkstyle.xml</configLocation>
        <consoleOutput>true</consoleOutput>
        <failsOnError>true</failsOnError>
    </configuration>
    <executions>
        <execution>
            <phase>validate</phase>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

**実行**:
```bash
mvn checkstyle:check
```

**出力例**:
```
[ERROR] src/main/java/com/example/UserService.java:[15,5] (naming) MemberName:
  Member name 'User_Name' must match pattern '^[a-z][a-zA-Z0-9]*$'.

[ERROR] src/main/java/com/example/OrderService.java:[23,1] (javadoc) JavadocMethod:
  Missing a Javadoc comment.

[WARN] src/main/java/com/example/ProductService.java:[45,32] (coding) MagicNumber:
  '100' is a magic number.
```

**推奨設定** (`checkstyle.xml`):
```xml
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC
    "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">

<module name="Checker">
    <!-- ファイルレベル -->
    <module name="FileLength">
        <property name="max" value="500"/>
    </module>

    <module name="TreeWalker">
        <!-- 命名規則 -->
        <module name="ConstantName"/>
        <module name="LocalFinalVariableName"/>
        <module name="LocalVariableName"/>
        <module name="MemberName"/>
        <module name="MethodName"/>
        <module name="PackageName"/>
        <module name="ParameterName"/>
        <module name="StaticVariableName"/>
        <module name="TypeName"/>

        <!-- インポート -->
        <module name="AvoidStarImport"/>
        <module name="UnusedImports"/>

        <!-- コードサイズ -->
        <module name="MethodLength">
            <property name="max" value="50"/>
        </module>
        <module name="ParameterNumber">
            <property name="max" value="7"/>
        </module>

        <!-- ホワイトスペース -->
        <module name="EmptyForIteratorPad"/>
        <module name="GenericWhitespace"/>
        <module name="MethodParamPad"/>
        <module name="WhitespaceAfter"/>
        <module name="WhitespaceAround"/>

        <!-- マジックナンバー -->
        <module name="MagicNumber"/>

        <!-- JavaDoc -->
        <module name="JavadocMethod"/>
        <module name="JavadocType"/>
    </module>
</module>
```

##### 2. SpotBugs（バグパターン検出）

**概要**: バイトコードを解析し、潜在的なバグパターンを検出（FindBugsの後継）

**検出できる問題**:
- Null pointer dereference（ヌルポインタ参照）
- リソースリーク（ファイル、DB接続の未クローズ）
- 無限ループ
- デッドロック
- セキュリティ脆弱性（SQLインジェクション、XSS）
- 非効率なコード（String concatenation in loop）

**導入方法**:
```xml
<!-- pom.xml -->
<plugin>
    <groupId>com.github.spotbugs</groupId>
    <artifactId>spotbugs-maven-plugin</artifactId>
    <version>4.8.2.0</version>
    <configuration>
        <effort>Max</effort>
        <threshold>Low</threshold>
        <xmlOutput>true</xmlOutput>
        <failOnError>true</failOnError>
    </configuration>
    <executions>
        <execution>
            <phase>verify</phase>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

**実行**:
```bash
mvn spotbugs:check
```

**出力例**:
```
[ERROR] High: Possible null pointer dereference in com.example.UserService.getUserById(Long)
  on exception path [com.example.UserService] At UserService.java:[line 45]

[ERROR] Medium: Unguarded read of resultSet in com.example.OrderRepository.findAll()
  [com.example.OrderRepository] At OrderRepository.java:[line 67]

[WARN] Low: Method concatenates strings using + in a loop
  [com.example.ProductService] At ProductService.java:[line 89]
```

**重要な検出カテゴリ**:
- **BAD_PRACTICE**: 不適切なコーディングプラクティス
- **CORRECTNESS**: 明らかなコーディングミス
- **MALICIOUS_CODE**: 悪意のあるコードの可能性
- **PERFORMANCE**: パフォーマンスの問題
- **SECURITY**: セキュリティ脆弱性

##### 3. PMD（コード品質分析）

**概要**: ソースコードを解析し、コード品質の問題を検出

**検出できる問題**:
- 未使用の変数・メソッド・パラメータ
- 空のtry/catch/finallyブロック
- 不必要なオブジェクト生成
- 複雑すぎるコード（Cyclomatic Complexity）
- コピー＆ペーストの重複コード（CPD）
- 非効率なString操作
- 不適切な例外処理

**導入方法**:
```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-pmd-plugin</artifactId>
    <version>3.21.2</version>
    <configuration>
        <rulesets>
            <ruleset>pmd-ruleset.xml</ruleset>
        </rulesets>
        <failOnViolation>true</failOnViolation>
        <printFailingErrors>true</printFailingErrors>
    </configuration>
    <executions>
        <execution>
            <phase>verify</phase>
            <goals>
                <goal>check</goal>
                <goal>cpd-check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

**実行**:
```bash
# PMD本体
mvn pmd:check

# CPD（コピー＆ペースト検出）
mvn pmd:cpd-check
```

**出力例**:
```
[ERROR] UserService.java:25: Avoid unused private fields such as 'logger'.

[ERROR] OrderService.java:67: Avoid empty catch blocks

[WARN] ProductService.java:89-102: The method 'calculateDiscount' has a cyclomatic complexity of 15.

[ERROR] CPD found duplicate code (50 lines) in:
  - src/main/java/com/example/service/UserService.java:45-95
  - src/main/java/com/example/service/AdminService.java:30-80
```

**推奨ルールセット** (`pmd-ruleset.xml`):
```xml
<?xml version="1.0"?>
<ruleset name="Custom Rules">
    <!-- ベストプラクティス -->
    <rule ref="category/java/bestpractices.xml">
        <exclude name="JUnitTestsShouldIncludeAssert"/>
    </rule>

    <!-- コード品質 -->
    <rule ref="category/java/codestyle.xml/MethodNamingConventions"/>
    <rule ref="category/java/codestyle.xml/ClassNamingConventions"/>
    <rule ref="category/java/codestyle.xml/ShortVariable"/>

    <!-- デザイン -->
    <rule ref="category/java/design.xml/CyclomaticComplexity">
        <properties>
            <property name="methodReportLevel" value="10"/>
        </properties>
    </rule>
    <rule ref="category/java/design.xml/ExcessiveMethodLength">
        <properties>
            <property name="minimum" value="50"/>
        </properties>
    </rule>

    <!-- エラー傾向 -->
    <rule ref="category/java/errorprone.xml/AvoidCatchingNPE"/>
    <rule ref="category/java/errorprone.xml/EmptyCatchBlock"/>

    <!-- パフォーマンス -->
    <rule ref="category/java/performance.xml/AvoidInstantiatingObjectsInLoops"/>
    <rule ref="category/java/performance.xml/StringInstantiation"/>
</ruleset>
```

##### 静的解析ツールの使い分け

| ツール | 分析対象 | 主な検出内容 | 推奨使用タイミング |
|--------|---------|-------------|------------------|
| **CheckStyle** | ソースコード | コーディング規約、フォーマット | 開発中（IDE統合） |
| **SpotBugs** | バイトコード | バグパターン、セキュリティ脆弱性 | ビルド時、コミット前 |
| **PMD** | ソースコード | コード品質、複雑度、重複 | ビルド時、リファクタリング前 |

##### 3つのツールを組み合わせた実行

```bash
# すべての静的解析を一度に実行
mvn clean compile checkstyle:check pmd:check spotbugs:check
```

**理想的な導入順序**（modern-java-practicesより）:
```
STEP 1: SpotBugs（バグは議論の余地なく修正すべき）
  ↓
STEP 2: PMD（コード品質のベストプラクティス）
  ↓
STEP 3: CheckStyle（スタイルは議論が分かれる）
```

**検出できる問題の総合表**:
- コーディング規約違反（CheckStyle）
- 複雑度が高すぎるコード（PMD: Cyclomatic Complexity > 10）
- 潜在的なバグパターン（SpotBugs: Null pointer, Resource leak）
- セキュリティ脆弱性（SpotBugs: SQL injection, XSS）
- 重複コード（PMD CPD）
- 未使用コード（PMD）

#### カバレッジチェック
```bash
# JaCoCo: テストカバレッジの測定
mvn jacoco:report
```

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <configuration>
        <rules>
            <rule>
                <element>CLASS</element>
                <limits>
                    <limit>
                        <counter>LINE</counter>
                        <value>COVEREDRATIO</value>
                        <minimum>0.80</minimum>
                    </limit>
                </limits>
            </rule>
        </rules>
    </configuration>
</plugin>
```

**検出できる問題**:
- テストされていないコードパス
- 不十分なテストカバレッジ

### レイヤー2: AIによる自己検証

AIに自分の出力をレビューさせる方法は2つあります：

#### 方法1: 実装後の自己チェック（同じAI）

```
「実装したコードをレビューして、以下を確認してください：

1. 存在しないAPIやメソッドを使用していないか
2. すべての要件を満たしているか
3. エラーハンドリングが適切か
4. テストが十分にカバーしているか
5. CLAUDE.mdのルールに従っているか
6. ハードコードされた値がないか
7. デフォルト値でエラーを隠していないか」
```

**SelfCheckGPT方式**（矛盾検出）:

同じタスクを複数回実行させて比較：

```
質問1: UserServiceの実装は完成していますか？
AI回答1: はい、完成しています

質問2: UserServiceの実装は何％完成していますか？残りのタスクをリストアップしてください。
AI回答2: 85%完成しています。残り：
        - メール送信機能（未実装）
        - パスワード強度チェック（未実装）
```

矛盾がある場合、虚偽報告の可能性が高い。

#### 方法2: Repomixを使った複数AIでの相互レビュー

**なぜ複数AIで検証するのか**:
- **Jagged Intelligence（凸凹な知能）**: 各AIに得意・苦手分野がある
- **Hallucination（虚偽報告）**: 1つのAIの誤りを他のAIが検出
- **見落とし防止**: 複数の視点で問題を発見

**ワークフロー**:

```
STEP 1: Claude Codeで実装完了
  ↓
STEP 2: Layer 1（自動検証）成功
  ↓
STEP 3: Repomixでコードベースをパッケージ化
  ↓
STEP 4: 複数AI（Claude、ChatGPT、Gemini）でレビュー
  ↓
STEP 5: 結果を統合・比較
  ↓ 3つのAIすべてが指摘 → 優先修正
  ↓ 1つのAIだけが指摘 → 人間が判断
STEP 6: Claude Codeで修正
```

**実践例**:

##### STEP 3: Repomixでパッケージ化

```bash
# セキュリティレビュー用にパッケージ化
repomix --output security-review.md --format markdown \
  --include "src/**/*.java,pom.xml,application.yml"
```

##### STEP 4-A: Claude 3.5 Sonnetでレビュー

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
```

##### STEP 4-B: ChatGPT o1でレビュー

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
   - 問題: management.endpoints.web.exposure.include=*
   - 推奨: 必要なエンドポイントのみ公開

【中リスク】
4. CorsConfig.java - CORS設定が緩すぎる
   - 問題: allowedOrigins = "*"
   - 推奨: 特定のドメインのみ許可

5. pom.xml - 古いバージョンのSpring Securityを使用
   - 問題: spring-security 5.5.0（既知の脆弱性あり）
   - 推奨: 最新版にアップデート
```

##### STEP 4-C: Gemini 1.5 Proでレビュー

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
```

##### STEP 5: 結果を統合・比較

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

**優先度の判断ルール**:
- **3つのAIすべてが指摘** → **P0（最優先、即座に修正）**
- **2つのAIが指摘** → **P0**
- **1つのAIだけが指摘** → P1またはP2（人間が検証して判断）

##### STEP 6: 修正とレビュー

**P0の修正例**:

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

**修正後、再度Layer 1とLayer 2で検証**:
```bash
# Layer 1: 自動検証
mvn clean compile test checkstyle:check pmd:check spotbugs:check

# Layer 2: Repomix + 複数AIレビュー
repomix --output review-v2.md
# → Claude、ChatGPT、Geminiで再レビュー
```

#### 複数AIレビューのベストプラクティス

1. **同じプロンプトを使用**
   - 各AIに同じ質問をして、結果を比較可能にする

2. **得意分野を活かす**
   - Claude: コードレビュー、論理的思考
   - ChatGPT: セキュリティ、ベストプラクティス
   - Gemini: Google規約に基づいた提案、パフォーマンス

3. **共通の指摘を優先**
   - 複数AIが同じ問題を指摘 → 高確率で真の問題
   - 1つのAIだけの指摘 → 人間が検証

4. **見落としの検出**
   - あるAIが見逃した問題を別のAIが指摘
   - より網羅的なレビューが可能

5. **トークン数の最適化**
   - `repomix --remove-comments --remove-empty-lines` でトークン削減
   - 各AIの Context Window を考慮（Claude: 200k, GPT-4: 128k, Gemini: 1M）

#### Repomixでのレビュー対象の調整

**セキュリティレビュー**:
```bash
repomix --output security-review.md --format markdown \
  --include "src/**/*.java,pom.xml,application*.yml"
```

**パフォーマンスレビュー**:
```bash
repomix --output performance-review.md --format markdown \
  --include "src/main/java/**/service/**,src/main/java/**/repository/**"
```

**アーキテクチャレビュー**:
```bash
repomix --output architecture-review.md --format markdown \
  --include "src/main/java/**,pom.xml" \
  --exclude "**/test/**"
```

### レイヤー3: 人間によるレビュー

#### コードレビューのチェックポイント

```java
// レビューポイント1: ビジネスロジックの正確性
@Service
public class OrderService {

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        // ✅ 在庫チェック
        // ✅ 在庫引き当て
        // ✅ 注文作成
        // ✅ 支払い処理
        // ❓ この順序は正しいか？
        // ❓ 失敗時のロールバック戦略は適切か？
    }
}

// レビューポイント2: セキュリティ
@RestController
public class UserController {

    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        // ❓ 認証は必要ないか？
        // ❓ 他人の情報を見られないか？
        return userService.getUserById(id);
    }
}

// レビューポイント3: パフォーマンス
@Service
public class ProductService {

    public List<ProductDto> getAllProducts() {
        List<Product> products = productRepository.findAll();

        // ❓ N+1問題は発生しないか？
        return products.stream()
            .map(p -> {
                Category category = categoryRepository.findById(p.getCategoryId()).orElse(null);
                return new ProductDto(p, category);
            })
            .collect(Collectors.toList());
    }
}
```

#### レビューチェックリスト

```markdown
## コードレビューチェックリスト

### 機能要件
- [ ] すべての受入条件を満たしているか
- [ ] エッジケースが処理されているか
- [ ] エラーハンドリングが適切か

### 非機能要件
- [ ] パフォーマンスは問題ないか
- [ ] セキュリティは考慮されているか
- [ ] スケーラビリティは問題ないか

### コード品質
- [ ] CLAUDE.mdのルールに従っているか
- [ ] ADRに記載された技術的決定に従っているか
- [ ] コーディング規約を守っているか
- [ ] 既存コードとの一貫性があるか

### テスト
- [ ] 十分なテストケースがあるか
- [ ] エッジケースがテストされているか
- [ ] テストカバレッジは基準を満たしているか

### ドキュメント
- [ ] 複雑なロジックにコメントがあるか
- [ ] APIドキュメントが更新されているか
- [ ] ADRが必要な決定は記録されているか
```

## 実践的なワークフロー

### ステップ1: タスクの委任（Trust）

```
「UserServiceを実装してください。

受入条件:
GIVEN: 新しいユーザー情報が提供される
WHEN: createUser()を呼び出す
THEN:
  - パスワードがBCryptでハッシュ化される
  - データベースに保存される
  - 作成されたUserが返される

GIVEN: 既に登録済みのメールアドレス
WHEN: createUser()を呼び出す
THEN:
  - DuplicateEmailExceptionがスローされる

技術要件:
- Spring Boot 3.2
- BCryptPasswordEncoder使用
- @Transactional必須
- CLAUDE.mdのルールに従う」
```

### ステップ2: 実装完了

AIがコードを生成。

### ステップ3: 自動検証（Verify Layer 1）

```bash
# コンパイル
mvn clean compile

# テスト実行
mvn test

# 静的解析
mvn checkstyle:check pmd:check spotbugs:check

# カバレッジチェック
mvn jacoco:report
```

### ステップ4: AIによる自己検証（Verify Layer 2）

```
「実装したUserServiceをレビューしてください。

チェック項目:
1. BCryptPasswordEncoderを正しく使用しているか
2. DuplicateEmailExceptionを適切にスローしているか
3. @Transactionalが付いているか
4. CLAUDE.mdのルールに従っているか
5. 存在しないAPIを使用していないか
6. ハードコードされた値がないか
7. テストは十分か」
```

### ステップ5: 人間によるレビュー（Verify Layer 3）

```java
// コードレビュー実施
@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional
    public User createUser(CreateUserRequest request) {
        // ✅ 重複チェック
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateEmailException(request.getEmail());
        }

        // ✅ BCrypt使用
        User user = new User();
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));

        // ✅ 保存
        return userRepository.save(user);
    }
}
```

レビュー結果: **承認** ✅

### ステップ6: 統合確認

```bash
# 統合テスト
mvn integration-test

# E2Eテスト（Playwrightなど）
npm run test:e2e
```

## 具体的な問題検出例

### 例1: Hallucination（虚偽報告）の検出

#### AIが生成したコード
```java
import org.springframework.data.jpa.repository.SmartQuery; // 存在しない

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    @SmartQuery(optimize = true)
    List<User> findAllOptimized();
}
```

#### 検証レイヤー1: コンパイルで検出
```bash
mvn compile

[ERROR] cannot find symbol
  symbol:   class SmartQuery
```

✅ **コンパイルエラーで検出成功**

### 例2: Reward Hacking（手抜き）の検出

#### AIが生成したコード
```java
public class DiscountCalculator {
    public BigDecimal calculateDiscount(BigDecimal price, BigDecimal rate) {
        // テストケースにハードコード
        if (price.equals(new BigDecimal("100")) &&
            rate.equals(new BigDecimal("0.1"))) {
            return new BigDecimal("90");
        }
        if (price.equals(new BigDecimal("200")) &&
            rate.equals(new BigDecimal("0.2"))) {
            return new BigDecimal("160");
        }
        return BigDecimal.ZERO;
    }
}
```

#### 検証レイヤー1: プロパティベーステストで検出
```java
@Test
void testCalculateDiscount_randomValues() {
    Random random = new Random();

    for (int i = 0; i < 100; i++) {
        BigDecimal price = BigDecimal.valueOf(random.nextDouble() * 1000);
        BigDecimal rate = BigDecimal.valueOf(random.nextDouble());

        BigDecimal result = calculator.calculateDiscount(price, rate);
        BigDecimal expected = price.multiply(BigDecimal.ONE.subtract(rate));

        assertEquals(expected, result);
        // ランダム値でテスト失敗 → Reward Hacking検出
    }
}
```

✅ **ランダム値テストで検出成功**

#### 検証レイヤー3: 人間のレビューで検出
レビュアーが気づく：
> 「なぜ特定の値だけハードコードされているのか？実際の計算式が実装されていない」

✅ **コードレビューで検出成功**

### 例3: Scope Creep（暴走）の検出

#### AIが生成したコード
```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private EmailService emailService;  // 指示していない
    @Autowired
    private NotificationService notificationService;  // 指示していない

    @Transactional
    public User createUser(CreateUserRequest request) {
        User user = new User();
        user.setEmail(request.getEmail());
        User savedUser = userRepository.save(user);

        // 指示していない機能
        emailService.sendWelcomeEmail(savedUser);
        notificationService.notifyAdmins(savedUser);

        return savedUser;
    }
}
```

#### 検証レイヤー2: AIによる自己検証
```
質問: 「このUserServiceは指示通りに実装されていますか？
       余分な機能はありませんか？」

AI回答: 「以下の追加機能が実装されています：
        - ウェルカムメール送信（指示されていない）
        - 管理者への通知（指示されていない）」
```

✅ **AI自己検証で検出成功**

#### 検証レイヤー3: 人間のレビューで検出
レビュアーが気づく：
> 「EmailServiceとNotificationServiceは指示していない。シンプルな実装が要求されていたはず」

✅ **コードレビューで検出成功**

### 例4: Context Limitations（忘れっぽさ）の検出

#### AIが生成したコード（Compact後）
```java
@Entity
public class Product {
    @Id
    private Long id;
    private String name;
    // Auditableの継承を忘れている
}
```

#### 検証レイヤー1: 静的解析（カスタムルール）
```xml
<!-- checkstyle.xml -->
<module name="Checker">
    <module name="TreeWalker">
        <module name="SuperClass">
            <property name="requiredSuperClass" value="Auditable"/>
            <message key="missing.superclass"
                     value="Entity must extend Auditable"/>
        </module>
    </module>
</module>
```

```bash
mvn checkstyle:check

[ERROR] Product.java:1: Entity must extend Auditable
```

✅ **静的解析で検出成功**

#### 検証レイヤー3: 人間のレビューで検出
レビュアーが気づく：
> 「CLAUDE.mdでは全エンティティがAuditableを継承する必要がある」

✅ **コードレビューで検出成功**


## ツールとの統合

### MCP Servers

#### Serena MCP Server
```
Trust: AIにコード生成を依頼
       ↓
Serena: 既存コードのパターンを参照
       ↓
Verify: 既存コードとの一貫性をチェック
```

#### Playwright MCP Server
```
Trust: AIにE2Eテストコード生成を依頼
       ↓
Playwright: テスト実行
       ↓
Verify: 実際のUIがテスト通りか確認
```

#### Chrome DevTools MCP Server
```
Trust: AIにフロントエンド機能実装を依頼
       ↓
Chrome DevTools: パフォーマンス計測
       ↓
Verify: パフォーマンス基準を満たすか確認
```

## ベストプラクティス

### 1. 自動化を最大限に活用
人間の負担を減らすため、可能な限り自動化：
```bash
# pre-commit hook
#!/bin/sh
mvn clean compile test checkstyle:check pmd:check
```

### 2. 早期検出
問題は早く見つけるほど修正コストが低い：
```
コンパイル(数秒) < テスト(数分) < レビュー(数時間) < 本番バグ(数日)
```

### 3. 複数の検証方法
1つの検証方法に依存しない：
- コンパイル: 構文エラー
- テスト: ロジックエラー
- 静的解析: コード品質
- レビュー: ビジネスロジック

### 4. AIに自己検証させる
実装後、必ずAIにレビューさせる：
```
「実装したコードをレビューして問題点を指摘してください」
```

### 5. 段階的な信頼
AIの出力に対する信頼度を段階的に調整：
- ボイラープレート: 高信頼（軽い検証）
- ビジネスロジック: 中信頼（通常の検証）
- セキュリティ: 低信頼（厳重な検証）

## 参考資料

### ベストプラクティス
- [Google: Code Review Guidelines](https://google.github.io/eng-practices/review/)
- [Microsoft: Secure Development Lifecycle](https://www.microsoft.com/en-us/securityengineering/sdl)

### ツール
- [Maven](https://maven.apache.org/)
- [CheckStyle](https://checkstyle.sourceforge.io/)
- [PMD](https://pmd.github.io/)
- [SpotBugs](https://spotbugs.github.io/)
- [JaCoCo](https://www.jacoco.org/)
- [SonarQube](https://www.sonarqube.org/)

### 概念
- [Defense in Depth](https://en.wikipedia.org/wiki/Defense_in_depth_(computing))
- [Shift Left Testing](https://en.wikipedia.org/wiki/Shift-left_testing)

## まとめ

Trust but Verify（任せる＆確かめる）は、AI駆動開発における中核的な実践手法。3つのレイヤーでの検証により：

1. **Layer 1（自動検証）**: コンパイル、テスト、静的解析、カバレッジ
2. **Layer 2（AI自己検証）**: AIによるセルフレビュー
3. **Layer 3（人間レビュー）**: ビジネスロジック、セキュリティ、アーキテクチャ

この多層防御により、すべてのAI問題（Hallucination、Reward Hacking、Scope Creep、Context Limitations、Jagged Intelligence）を効果的に検出し、高品質なコードを維持できる。

**Trust but Verifyの本質**: AIの効率性を最大限に活用しながら、品質を担保する賢明なバランス。
