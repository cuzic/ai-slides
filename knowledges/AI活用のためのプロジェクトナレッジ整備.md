# AI活用のためのプロジェクトナレッジ整備ガイド

## なぜプロジェクトナレッジが重要か

### 課題
- AIに毎回全ソースコードを読み込ませるとトークン数が膨大になる
- 時間もコストもかかる
- プロジェクトのルールや方針が口頭伝承になっている

### 解決策
- **初回のみ**: 全ソースコードをAIに読み込ませてプロジェクトを理解させる
- **2回目以降**: 整備したドキュメント（README.md等）のみを読み込む
- **結果**: トークン数が1/10以下に削減、時間も大幅短縮

### 人間との類推
- 人間の新人も最初はコード全体を読む必要がある
- 慣れてきたら設計書やREADMEだけで作業できる
- AIも同じ

---

## プロジェクトナレッジの構成要素

### 1. README.md（プロジェクト概要）
プロジェクト全体の説明と使い方

### 2. ARCHITECTURE.md（アーキテクチャ設計）
システムの構造と設計思想

### 3. DEVELOPMENT_RULES.md（開発ルール）
コーディング規約と作業手順

### 4. AI_INSTRUCTIONS.md（AI向け指示書）
AIが作業する際の具体的なルール

---

## サンプル1: README.md

```markdown
# 運賃請求管理システム (NFBMS)

## 概要
運送会社向けの伝票登録・請求・支払い管理Webアプリケーション

## 技術スタック
- **言語**: Java 1.8
- **フレームワーク**: Spring Boot 2.7
- **ORマッパー**: Doma2 (DBFlute)
- **DB**: SQL Server
- **ビルドツール**: Maven
- **バージョン管理**: SVN

## プロジェクト構成

```
nfbms/
├── src/
│   └── main/
│       ├── java/
│       │   └── springboot/pj/
│       │       ├── zcore/         # 共通コア機能
│       │       │   ├── common/    # 共通部品
│       │       │   ├── bean/      # 共通Bean
│       │       │   └── util/      # ユーティリティ
│       │       └── nfbms/         # アプリケーション
│       │           └── app/       # 機能別パッケージ
│       │               ├── m001/  # ユーザーマスター
│       │               ├── m002/  # 拠点マスター
│       │               └── ...
│       └── resources/
│           ├── application.properties         # 共通設定
│           ├── application-dev.properties     # 開発環境
│           ├── application-it.properties      # 結合テスト環境
│           ├── application-prod.properties    # 本番環境
│           └── META-INF/
│               └── {機能}/                     # DAO用SQLファイル
├── Mock/                  # モックアップHTML
└── pom.xml               # Maven設定
```

## 標準パッケージ構成

各機能（例: m001_ユーザーマスター）は以下の構成:

```
app/m001/
├── M001Controller.java    # リクエスト制御
├── M001Service.java       # ビジネスロジック
├── M001Form.java          # 画面入力フォーム
├── M001Bean.java          # 画面表示用Bean
├── M001Dao.java           # データアクセス
└── M001Entity.java        # エンティティ（テーブル対応）
```

## 環境構築

### 必要なツール
- JDK 1.8
- Maven 3.6+
- SQL Server（または互換DB）

### セットアップ手順
1. SVNからチェックアウト
2. Maven install: `mvn clean install`
3. WARファイルをTomcatにデプロイ

### 環境別の起動方法
```bash
# 開発環境
export SPRING_PROFILES_ACTIVE=dev

# 結合テスト環境
export SPRING_PROFILES_ACTIVE=it

# 本番環境
export SPRING_PROFILES_ACTIVE=prod
```

## 命名規則

### テーブル
- マスター: `mXXX_テーブル名` (例: m001_user)
- トランザクション: `tXXX_テーブル名` (例: t001_slip)
- インポート: `iXXX_テーブル名` (例: i001_freightSlipImport)

### クラス
- エンティティ: `M001User` (テーブル名をPascalCaseに)
- DAO: `M001UserDao`
- Service: `M001Service` (番号のみ)
- Controller: `M001Controller`
- Form: `M001Form`

### パッケージ
- 機能別: `springboot.pj.nfbms.app.{機能番号}`
- 例: `springboot.pj.nfbms.app.m001`

## 開発の流れ
1. テーブル定義（DDL作成）
2. エンティティ・DAO自動生成（DBFlute）
3. モックアップHTML作成
4. Form/Bean作成
5. Service作成（ビジネスロジック）
6. Controller作成（画面制御）
7. 動作確認

## 参考リンク
- [Spring Boot公式ドキュメント](https://spring.io/projects/spring-boot)
- [Doma2リファレンス](https://doma.readthedocs.io/)
```

---

## サンプル2: AI_INSTRUCTIONS.md

```markdown
# AI向け作業指示書

## 基本ルール

### 1. 作業ディレクトリ
- メイン作業ディレクトリ: `/path/to/nfbms`
- 一時ファイル: `/tmp` または `./work`
- **禁止**: 共有ドライブ（`\\server\share\`）へのアクセス

### 2. ファイル操作
- 既存ファイルの編集前に必ずバックアップを取る
- バックアップ先: `./backup/{YYYYMMDD}/`
- Git管理下のファイルは特に注意

### 3. コード生成時の原則
- **既存コードを参考にする**: 新規作成時は類似機能のコードを参照
- **命名規則を守る**: README.mdの命名規則に従う
- **共通項目を継承**: 登録・更新系の項目（regUser, updTime等）は必須
- **段階的に生成**: 一度に全部作らず、クラスごとに確認

### 4. プロンプトへの応答
- コードは必ずMarkdown形式で返す
- ファイルパスを明示する
- 変更内容を簡潔に説明する

## 新規マスター機能を作成する場合の手順

### Step 1: 要件確認
ユーザーに以下を質問:
1. マスター名（例: 得意先マスター）
2. テーブル番号（例: m021）
3. 必要な項目（業務要件から）
4. 参考にする既存マスター（例: m001_user）

### Step 2: テーブル定義生成
```sql
-- 参考: m001_user.sql
CREATE TABLE m021_customer (
     customerId NVARCHAR(20) NOT NULL
    ,customerNm NVARCHAR(50) NOT NULL
    -- ... その他項目
    ,regUser NVARCHAR(20)       -- 共通項目
    ,regTime DATETIME           -- 共通項目
    ,updUser NVARCHAR(20)       -- 共通項目
    ,updTime DATETIME           -- 共通項目
     PRIMARY KEY (customerId)
);
```

### Step 3: エンティティ生成
```java
// ファイル: src/main/java/springboot/pj/nfbms/app/m021/M021Entity.java
// 参考: M001UserEntity.java

@Entity
@Table(name = "m021_customer")
@Data
public class M021CustomerEntity {
    @Id
    private String customerId;
    private String customerNm;
    // ... その他フィールド
    private String regUser;
    private LocalDateTime regTime;
    private String updUser;
    private LocalDateTime updTime;
}
```

### Step 4: DAO生成
```java
// ファイル: src/main/java/springboot/pj/nfbms/app/m021/M021CustomerDao.java
// 参考: M001UserDao.java

@Dao
public interface M021CustomerDao {
    @Select
    List<M021CustomerEntity> selectAll();

    @Select
    M021CustomerEntity selectById(String customerId);

    @Insert
    int insert(M021CustomerEntity entity);

    @Update
    int update(M021CustomerEntity entity);

    @Delete
    int delete(M021CustomerEntity entity);
}
```

### Step 5: Form/Bean生成
既存の M001Form.java を参考に作成

### Step 6: Service生成
既存の M001Service.java を参考に作成

### Step 7: Controller生成
既存の M001Controller.java を参考に作成

## エラーハンドリング

### ユーザーがエラーメッセージを貼り付けた場合
1. エラーメッセージを分析
2. 原因を特定
3. 修正方法を提示
4. 修正後のコードを生成

### 例:
```
ユーザー: 「NullPointerExceptionが発生しました」

AI応答:
1. 原因: ○○がnullの可能性があります
2. 修正箇所: {ファイル名}の{行番号}
3. 修正コード:
   [修正後のコード]
```

## コードレビューの観点

ユーザーが「このコードをレビューして」と依頼した場合:

### チェック項目
1. **命名規則**: プロジェクトの規則に従っているか
2. **共通項目**: regUser, updTime等が漏れていないか
3. **NULL安全性**: NullPointerExceptionの可能性
4. **トランザクション**: @Transactionalの付与
5. **バリデーション**: 入力チェックの妥当性
6. **SQLインジェクション**: 危険なSQL組み立て
7. **パフォーマンス**: N+1問題、不要なループ

### レビュー結果の形式
```markdown
## レビュー結果

### ✅ 良い点
- 命名規則に従っている
- NULLチェックが適切

### ⚠️ 改善提案
1. {ファイル名}:{行番号}
   - 問題: ○○
   - 提案: ××

### 🔧 修正コード
[修正後のコード]
```

## ドキュメント生成

### マスター仕様書を依頼された場合
```markdown
# {マスター名}仕様書

## 概要
[マスターの目的と役割]

## テーブル定義
[CREATE TABLE文]

## 項目定義
| 項目名 | 物理名 | 型 | 必須 | 説明 |
|--------|--------|-----|------|------|
| ... | ... | ... | ... | ... |

## 画面仕様
### 一覧画面
- 検索条件: ...
- 表示項目: ...

### 登録・編集画面
- 入力項目: ...
- バリデーション: ...

## 業務ルール
[特記事項]
```

## トークン数節約のコツ

### 初回読み込み時
- プロジェクト全体を読み込む（仕方ない）
- 要約を作成して保存

### 2回目以降
- README.md、ARCHITECTURE.md、AI_INSTRUCTIONS.mdのみ読み込む
- 必要な既存ファイルのみ個別に読み込む
- 「前回の会話を参照」を活用

### 例:
```
❌ 悪い例:
「プロジェクト全体をもう一度読んで、得意先マスターを作って」
→ トークン数: 50,000+

✅ 良い例:
「README.mdを読んで、m001の構造を参考に、m021_customerのエンティティを作って」
→ トークン数: 5,000程度
```

## まとめ

### AIに依頼する前の準備
1. ✅ README.mdを読ませる
2. ✅ 参考にする既存コードを指定
3. ✅ 具体的な要件を伝える
4. ✅ 段階的に依頼（一度に全部作らない）

### AIからの応答を受け取ったら
1. ✅ コードを確認（盲目的に信用しない）
2. ✅ 動作テスト
3. ✅ 問題があればエラーを伝えて修正依頼

### ドキュメント更新
1. ✅ 新機能を追加したらREADMEを更新
2. ✅ AIに更新を依頼してもOK
```

---

## サンプル3: DEVELOPMENT_RULES.md

```markdown
# 開発ルール

## コーディング規約

### Java
- インデント: スペース4個
- 文字コード: UTF-8
- 改行コード: LF
- Lombokを積極的に活用（@Data, @Builder等）

### SQL
- キーワードは大文字
- テーブル名・カラム名は小文字
- インデントは2スペース

## Git運用

### ブランチ戦略
- main: 本番リリース用
- develop: 開発用
- feature/*: 機能開発用

### コミットメッセージ
```
[機能番号] 変更内容の要約

詳細説明
```

例:
```
[M021] 得意先マスター新規作成

- エンティティ、DAO、Service、Controllerを追加
- 一覧・登録・編集・削除機能を実装
```

## テスト方針

### 単体テスト
- JUnitでServiceクラスをテスト
- カバレッジ80%以上を目標

### 結合テスト
- 画面からの動作確認
- 主要なシナリオをテスト

## レビュー体制
- 全てのコードはレビューを経てマージ
- レビュー観点: 命名、NULL安全性、SQLインジェクション

## デプロイ手順
1. Maven clean install
2. WARファイル生成確認
3. テスト環境にデプロイ
4. 動作確認後、本番デプロイ
```

---

## 実践ワークショップ: Day1最後の演習

### 目的
プロジェクトをAIに読み込ませ、要約ドキュメントを作成する

### 手順

#### 1. 初回読み込み（全員で実施）
```
プロンプト例:
「このプロジェクトのソースコードを全て読んで、
以下の観点で要約してください:
1. プロジェクトの目的
2. 技術スタック
3. ディレクトリ構成
4. 主要なクラスとその役割
5. 命名規則
6. 開発の流れ

要約はMarkdown形式で、README.mdとして保存できる形式でお願いします。」
```

#### 2. 生成された要約の確認
- AIが生成したREADME.mdを確認
- 不足している情報があれば追加質問
- 間違いがあれば指摘して修正

#### 3. 保存
- 生成された内容をREADME.mdとして保存
- プロジェクトルートに配置

#### 4. 動作確認
- 新しいClaude会話を開始
- README.mdのみを読み込ませる
- 「得意先マスターのエンティティを作って」と依頼
- うまく生成できればOK

### 期待される成果物
- プロジェクトの要約README.md
- AIが2回目以降に参照するドキュメント
- トークン数が大幅に削減された状態

### 所要時間
- 30分程度

---

## トークン数削減の具体例

### Before: ドキュメントなし
```
毎回の会話:
- プロジェクト全体を読み込む
- 50,000トークン消費
- 読み込みに3-5分
- コスト: $$$
```

### After: ドキュメント整備後
```
2回目以降の会話:
- README.md + 必要なファイルのみ
- 5,000トークン
- 読み込みに30秒
- コスト: $
```

### 節約効果
- **トークン数**: 1/10
- **時間**: 1/6
- **コスト**: 1/10

---

## よくある質問

### Q1: README.mdはどこまで詳しく書くべき？
A: AIが新規機能を作れる程度の情報量。具体的には:
- ディレクトリ構成
- 命名規則
- 既存の類似機能の場所
- 開発の流れ

### Q2: 毎回更新が必要？
A: 新しい機能やルールを追加したら更新。
ただし、小さな修正なら不要。

### Q3: AIに更新してもらえる？
A: 可能。「このREADMEに新機能の説明を追加して」と依頼できる。

### Q4: 複数人で開発する場合は？
A: README.mdをGit管理下に置き、全員で共有。
最新版を常にAIに読み込ませる。

---

## Day2での活用

### 演習開始時
1. 全員がREADME.mdをClaudeに読み込ませる
2. 「得意先マスターを作りたい」と伝える
3. AIが自動的に既存の構造を参考にしてコード生成

### 演習中
- エラーが出たらエラーメッセージを貼り付け
- AIが解決策を提示
- 修正コードを生成

### 演習終了時
- 完成したコードをAIにレビュー依頼
- 改善提案を受ける
- ドキュメント更新

---

## まとめ

### プロジェクトナレッジ整備の3ステップ

1. **初回読み込み**: AIにプロジェクト全体を読ませる
2. **要約作成**: README.mdとして保存
3. **継続活用**: 2回目以降はREADMEのみ読み込む

### メリット
- ✅ トークン数削減
- ✅ 時間短縮
- ✅ コスト削減
- ✅ 一貫性のある開発
- ✅ チーム内での知識共有

### Day2への準備
- Day1でREADME.md作成を完了
- Day2開始時には全員が使える状態に
- 演習がスムーズに進行
