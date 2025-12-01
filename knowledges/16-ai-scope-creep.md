# AI Scope Creep（AIによるスコープ・クリープ・暴走）

## 定義

AI Scope Creep（AIスコープクリープ）は、AIが指示されたタスクの範囲を超えて、未承認の変更や追加機能を実装してしまう現象。ソフトウェア開発における「暴走」「勝手な判断」の問題。

## Scope Creep の一般的な定義

「プロダクトのスコープへの未承認の変更—非公式な会話を通じて追加の機能や要件を追加すること」

## Feature Creep との関係

Feature Creep（機能クリープ）は、「プロダクトの基本機能を超えた、新機能の過度な継続的拡張または追加」。AI は意図せずこれを引き起こす。

## AI特有の問題

### 人間の Scope Creep
従来、Scope Creep は人間による追加要求が原因：
- ステークホルダーからの新要求
- 開発中の「良いアイデア」
- 要件の誤解

### AIによる Scope Creep
AIは自動的にスコープを拡大：
- **基本機能を自動処理**するため、開発者が「もっと大きく、広く」夢見られる
- **MVP原則を忘れる**
- **フル機能アプリ**に執着する

## Java開発での具体例

### 例1: 単純な User Service の暴走

#### 指示
```
Spring BootでUserServiceクラスを作成してください。
ユーザーの作成と取得ができること。
```

#### 期待される実装
```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public User createUser(User user) {
        return userRepository.save(user);
    }

    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

#### AIが実際に生成したコード（暴走版）
```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EmailService emailService;  // 指示していない

    @Autowired
    private NotificationService notificationService;  // 指示していない

    @Autowired
    private AuditLogService auditLogService;  // 指示していない

    public User createUser(User user) {
        // バリデーション（指示していない）
        validateUser(user);

        // プロフィール画像の最適化（指示していない）
        optimizeProfileImage(user);

        User savedUser = userRepository.save(user);

        // ウェルカムメール送信（指示していない）
        emailService.sendWelcomeEmail(savedUser);

        // 管理者に通知（指示していない）
        notificationService.notifyAdmins(savedUser);

        // 監査ログ（指示していない）
        auditLogService.log("USER_CREATED", savedUser);

        // 推奨ユーザーのマッチング（指示していない）
        recommendUsers(savedUser);

        return savedUser;
    }

    // 以下、指示していないメソッドが多数...
}
```

**問題**：
- 依存関係が増えすぎ
- 実装していないサービスを参照
- テストが複雑化
- 保守性が低下

### 例2: Controller の過剰な機能

#### 指示
```
ユーザー登録のRESTエンドポイントを作成してください
```

#### 期待される実装
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;

    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User created = userService.createUser(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

#### AIが実際に生成したコード（暴走版）
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;

    // 指示していない機能
    @PostMapping
    @RateLimiting(maxRequests = 100)  // レート制限
    @Cacheable("users")  // キャッシング
    @Async  // 非同期処理
    @Transactional(isolation = Isolation.SERIALIZABLE)  // トランザクション
    public ResponseEntity<UserResponse> createUser(
        @Valid @RequestBody CreateUserRequest request,
        @RequestHeader("X-Client-Version") String clientVersion,  // 指示していない
        @RequestHeader("X-Device-Id") String deviceId,  // 指示していない
        HttpServletRequest httpRequest  // 指示していない
    ) {
        // クライアントバージョンチェック（指示していない）
        validateClientVersion(clientVersion);

        // デバイスIDの検証（指示していない）
        checkDeviceLimit(deviceId);

        // IPベースのジオロケーション（指示していない）
        String country = getCountryFromIP(httpRequest.getRemoteAddr());

        // A/Bテスト（指示していない）
        String experimentGroup = assignExperimentGroup(request);

        User created = userService.createUser(request);

        // メトリクス送信（指示していない）
        sendMetrics(created, country, experimentGroup);

        return ResponseEntity.status(HttpStatus.CREATED)
            .header("X-RateLimit-Remaining", "99")  // 指示していない
            .body(UserResponse.from(created));
    }

    // 多数の helper メソッド（すべて指示していない）
}
```

### 例3: 設定ファイルの過剰な追加

#### 指示
```
application.ymlにデータベース設定を追加してください
```

#### 期待される実装
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: user
    password: password
```

#### AIが実際に生成したコード（暴走版）
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: user
    password: password
    # ここから指示していない
    hikari:
      maximum-pool-size: 20
      minimum-idle: 10
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
  jpa:
    # 指示していない
    hibernate:
      ddl-auto: update
      naming:
        physical-strategy: org.hibernate.boot.model.naming.PhysicalNamingStrategyStandardImpl
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        format_sql: true
        show_sql: true
        use_sql_comments: true
        jdbc:
          batch_size: 20
        cache:
          use_second_level_cache: true
          region:
            factory_class: org.hibernate.cache.jcache.JCacheRegionFactory

# さらに多数の設定が追加される
logging:
  level:
    org.hibernate: DEBUG
    org.springframework: INFO

management:
  endpoints:
    web:
      exposure:
        include: "*"
  metrics:
    export:
      prometheus:
        enabled: true
```

## なぜ発生するのか

### 1. AIの「親切心」
AIは「良かれと思って」機能を追加：
- ベストプラクティスの適用
- エラーハンドリングの追加
- パフォーマンス最適化
- セキュリティ機能の追加

### 2. パターン認識
トレーニングデータから学習したパターンを適用：
- 「UserServiceには通常メール送信がある」
- 「Controllerには通常バリデーションがある」
- 「本番環境にはメトリクスが必要」

### 3. 不明確な指示
指示が曖昧だとAIが「推測」：
```
// 曖昧な指示
「ユーザー機能を実装して」

// AIの推測
→ 登録、ログイン、プロフィール編集、削除、
  パスワードリセット、メール確認、2FA...
```

## 対策：ガードレールの設定

### 1. 明確なスコープ指定

**悪い例**：
```
ユーザー登録機能を実装して
```

**良い例**：
```
ユーザー登録機能を実装してください。

スコープ：
- ユーザーの作成のみ（メール送信は含めない）
- エラーハンドリングは BasicException のみ
- キャッシングは実装しない
- 非同期処理は使用しない

実装するもの：
1. UserService.createUser() メソッド
2. 基本的なバリデーション（null チェックのみ）

実装しないもの：
- メール送信
- 通知
- 監査ログ
- プロフィール画像処理
- 推奨機能
```

### 2. 具体的な技術制約

```markdown
## 技術制約

### 使用するライブラリ
- Spring Boot 3.2（標準機能のみ）
- Spring Data JPA
- Jakarta Bean Validation

### 使用しないライブラリ
- キャッシングライブラリ（Redis等）
- メッセージングライブラリ（Kafka等）
- メトリクスライブラリ（Prometheus等）

### アーキテクチャ
- シンプルな3層アーキテクチャ
- Controller → Service → Repository
- 追加のレイヤーは不要
```

### 3. MVP原則の明示

```
このタスクはMVP（Minimum Viable Product）です。

必須機能のみを実装し、以下は含めないでください：
- 「あると良い」機能
- 最適化
- 将来の拡張性のための抽象化
- 過剰なエラーハンドリング
```

### 4. チェックリストによる制限

```markdown
## 実装チェックリスト

実装すること：
- [ ] User エンティティの作成
- [ ] UserRepository インターフェース
- [ ] UserService.createUser() メソッド
- [ ] 基本的なバリデーション

実装しないこと：
- [ ] メール送信
- [ ] 画像処理
- [ ] キャッシング
- [ ] 非同期処理
- [ ] 監査ログ
```

### 5. GitHub Issues での言語化

```markdown
## Issue: ユーザー登録機能

### 実装内容
- UserService.createUser() メソッド
- 基本的なバリデーション

### 変更範囲
- src/main/java/com/example/service/UserService.java (新規)
- src/test/java/com/example/service/UserServiceTest.java (新規)

### 影響を受けるファイル
- 上記2ファイルのみ

### テスト計画
- ユニットテスト3ケース（正常系、null、重複）

### やらないこと
- メール送信は別issue (#123)で実装
- プロフィール画像は別issue (#124)で実装
```

## Trust but Verify（任せる＆確かめる）

### 実装前の確認
```
AIに実装前に以下を確認：

「このタスクで実装する内容を
 詳細にリストアップしてください。

 指示されていない機能を
 追加しようとしていませんか？」
```

### 実装後のレビュー
```java
// レビューポイント
1. 指示した機能のみが実装されているか
2. 余計な依存関係が追加されていないか
3. 指示していないアノテーションがないか
4. 設定ファイルに不要な設定がないか
```

## Copilot での Scope Creep 対策

### 明示的な制約
```
入力と出力、終了条件を事前に明示的に指定し、
AI生成の出力を「ドラフト」として扱い、
不要な分岐を削除してトリガーをロックダウンする。
```

### 段階的な実装
```
大きなタスクを小さく分割：

タスク1: エンティティのみ作成（5分）
タスク2: Repositoryのみ作成（5分）
タスク3: Service メソッド1つのみ作成（5分）
```

## 実践的なワークフロー

### ステップ1: 計画の言語化
```
AIに「このタスクで何をするつもりか」を
GitHub issuesの形式で言語化させる
```

### ステップ2: レビューと絞り込み
```
言語化された内容をレビュー：
- 「これは不要」を削除
- 「これは後回し」を別issueに
- 本当に必要なもののみ残す
```

### ステップ3: 明示的な指示
```
絞り込んだ内容を明示：

「以下のみを実装してください：
1. ...
2. ...

以下は実装しないでください：
1. ...
2. ...」
```

### ステップ4: 実装と検証
```
実装後、指示した内容と照合：
- 余分な機能がないか
- 依存関係が増えていないか
- ファイル数が想定内か
```

## 統計と効果

### 問題の規模
- AI使用時、Scope Creepが**発生しやすくなる**
- 基本機能を素早く実装できるため、開発者が「もっと追加したい」と考える
- MVP原則を忘れ、フル機能アプリに向かう傾向

### 対策の効果
明確なスコープ指定により：
- 開発時間が予測可能に
- テストが簡潔に
- 保守性が向上

## 参考資料

### 実践ガイド
- [Product Discovery Group: AI Side Effect - Human Scope Creep](https://productdiscoverygroup.com/learn/ai-side-effect-human-scope-creep)
- [Latenode Community: Stop Scope Creep with AI Copilot](https://community.latenode.com/t/how-do-i-stop-scope-creep-with-ai-copilot-workflow-generation/51541)
- [Huenei: Scope Creep in Software Development](https://www.huenei.com/en/scop-creep-in-software-development/)

### 概念解説
- [Lucidspark: What is Scope Creep?](https://lucid.co/blog/what-is-scope-creep)
- [Wikipedia: Feature creep](https://en.wikipedia.org/wiki/Feature_creep)
- [LogRocket: What is feature creep](https://blog.logrocket.com/product-management/what-is-feature-creep-how-to-avoid/)

## まとめ

AI Scope Creep（暴走・勝手な判断）は、AIの「親切心」が裏目に出る現象。対策として：

1. **明確なスコープ指定**：やること/やらないことを明示
2. **MVP原則の徹底**：最小限の機能のみ実装
3. **技術制約の明示**：使用するライブラリを限定
4. **GitHub Issuesでの言語化**：実装前に計画をレビュー
5. **Trust but Verify**：実装後に指示と照合

適切なガードレールにより、AIの効率性を保ちながら、スコープを制御できる。
