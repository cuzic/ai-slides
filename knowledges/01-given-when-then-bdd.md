# GIVEN WHEN THEN - BDD形式の受入条件

## 概要

Given-When-Thenは、BDD（Behavior-Driven Development）から借用された受入条件を作成するフォーマットで、ユーザーストーリーの望ましい動作をより構造的で理解しやすい方法で表現する。

## 3つのコンポーネント

基本原則：

- **GIVEN（前提条件）**: この特定のシナリオに関連する前提条件、状態、パラメータ（シーンの設定）
- **WHEN（操作）**: トリガー、または状態の変化、テストされるもの
- **THEN（期待される結果）**: 前提条件のコンテキストを考慮した、トリガーの期待される結果

## 主な利点

1. **明確性と構造**: 明確で簡潔、かつ構造化された方法で受入条件を定義
2. **共通理解**: 開発プロセスに関わる全員（開発者、テスター、プロダクトオーナー）が達成すべきことと成功の測定方法を理解できる
3. **テストケースへの自然な変換**: 各コンポーネントを特定のテストシナリオに変換できる
4. **自動化の容易さ**: Cucumber、SpecFlow、JBehaveなどのツールで自動テストスクリプトに直接変換可能

## 実装例

```gherkin
Given ユーザーが未登録の状態で
When 有効なメールアドレスとパスワードを入力して登録ボタンを押したら
Then ユーザーが登録され、確認メールが送信される
```

## 自動化ツール

- **Cucumber**: Ruby、Java、JavaScript対応
- **SpecFlow**: .NET向け
- **JBehave**: Java向け
- **Behave**: Python向け

## ベストプラクティス

1. **シンプルに保つ**: 各シナリオは1つの動作に焦点を当てる
2. **具体的に**: 曖昧な表現を避け、具体的な値や状態を記述
3. **テスト可能**: 各THENは検証可能な結果でなければならない
4. **ユーザー視点**: ユーザーの視点から記述し、実装の詳細を避ける

## 参考資料

- [Visual Paradigm: Given-When-Then Guide](https://guides.visual-paradigm.com/give-when-then-acceptance-criteria-for-user-stories-in-agile-development/)
- [Thoughtworks: Applying BDD acceptance criteria](https://www.thoughtworks.com/insights/blog/applying-bdd-acceptance-criteria-user-stories)
- [ProductMonk: Given-When-Then Acceptance Criteria](https://www.productmonk.io/p/given-when-then-acceptance-criteria)

## 2024-2025年の状況

GWT形式は現在でもアジャイルソフトウェア開発における現行かつ関連性の高いプラクティスとして継続している。
