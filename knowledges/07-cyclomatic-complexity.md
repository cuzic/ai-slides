# Cyclomatic Complexity（循環的複雑度）

## 概要

循環的複雑度は、プログラムの複雑さを示すソフトウェアメトリクス。プログラムのソースコードを通る線形独立パスの数を定量的に測定する。

## 歴史

Thomas J. McCabe, Sr.によって1976年に開発された。

## 定義と計算

### 基本的な計算式
```
M = E - N + 2P
```
- E: エッジ（制御フローグラフの辺）の数
- N: ノード（制御フローグラフの頂点）の数
- P: 連結成分の数（通常は1）

### 簡易計算方法
決定ポイント（分岐）の数 + 1
- if文
- while/for/do-while文
- switch/case文
- 三項演算子
- 論理演算子（&&, ||）

## コード品質との関係

### 欠陥密度との相関
- 高い循環的複雑度のコードは、より多くの欠陥を隠す傾向
- 複雑度と欠陥密度の間には強い相関関係
- コードレビューとテストで追加の精査が必要なモジュールを特定するのに有効

### コード行数との組み合わせ
循環的複雑度とコード行数を組み合わせることで、エラーの可能性についてより明確な全体像が得られる。

## 推奨される閾値

### NIST235の推奨
- **10以下**: McCabeが提案した元々の制限値、十分な裏付けあり
- **15以下**: より高い限界値、これも成功裏に使用されている
- 10が良い出発点として推奨

### 一般的な解釈
- **1-10**: シンプル、低リスク
- **11-20**: 中程度の複雑さ、中程度のリスク
- **21-50**: 複雑、高リスク
- **50+**: 非常に複雑、テスト不可能、高リスク

## 重要な制限事項

### 循環的複雑度だけでは不十分
- エラーやバグの数を減らすことが証明されているわけではない
- コード品質の一部の側面のみを示す
- この指標だけに焦点を当てると、誤解を招く結論につながる可能性

### 考慮されない要因
- コードの可読性
- 保守性
- テストカバレッジ
- 命名の品質
- 設計パターンの適用

## 複雑度を減らす戦略

### 1. 小さな関数
- 関数のコード行数が少ないほど、複雑度も低くなる
- インラインコメントなしでも読みやすい
- 目安：1関数20-30行以内

### 2. リファクタリング
- 複雑な関数をより単純な関数に分割
- 決定ポイントの数を減らす

### 3. 早期リターン
- ネストしたif-elseを早期リターンに変換
- ガード節の活用

```javascript
// 複雑度が高い例
function processOrder(order) {
  if (order.status === 'pending') {
    if (order.paymentMethod === 'credit_card') {
      if (order.amount > 1000) {
        // 処理
      } else {
        // 処理
      }
    } else {
      // 処理
    }
  } else {
    // 処理
  }
}

// 複雑度を減らした例
function processOrder(order) {
  if (order.status !== 'pending') {
    return handleNonPendingOrder(order)
  }

  if (order.paymentMethod === 'credit_card') {
    return processCreditCard(order)
  }

  return processOtherPayment(order)
}
```

### 4. 複雑な条件式の抽出
- 複雑な条件を変数に抽出
- 意図を明確化

```javascript
// 前
if (user.age >= 18 && user.hasLicense && !user.isSuspended) {
  // 処理
}

// 後
const canDrive = user.age >= 18 && user.hasLicense && !user.isSuspended
if (canDrive) {
  // 処理
}
```

### 5. パターンの適用
- switch-caseをStrategy Patternに置き換え
- Mapを使用した分岐の置き換え

```javascript
// 前: switch-case (複雑度が高い)
function getPrice(type) {
  switch(type) {
    case 'basic': return 100
    case 'premium': return 200
    case 'enterprise': return 500
    default: return 0
  }
}

// 後: Map (複雑度が低い)
const prices = {
  basic: 100,
  premium: 200,
  enterprise: 500
}
function getPrice(type) {
  return prices[type] || 0
}
```

## ツールとの統合

### Visual Studio
- Code Metrics機能で循環的複雑度を計算
- コードの品質を継続的に監視

### 静的解析ツール
- SonarQube
- CodeClimate
- ESLint (complexity rule)
- Pylint (mccabe plugin)

### CI/CDでの活用
- プルリクエスト時に自動チェック
- 閾値を超えた場合に警告
- コード品質の継続的な改善

## 利点

1. **客観的な測定**: 定量的に複雑さを評価
2. **問題箇所の特定**: 複雑なコードを素早く発見
3. **テスト計画**: 必要なテストケース数の見積もり
4. **優先順位付け**: リファクタリングの優先順位を決定
5. **トレンド分析**: 時間経過によるコード品質の追跡

## 欠点

1. **全体像の欠如**: コード品質の一側面のみ
2. **偽陰性**: 低い複雑度でも悪いコードは存在
3. **偽陽性**: 高い複雑度でも適切なコードは存在
4. **コンテキスト無視**: ビジネスロジックの複雑さを考慮しない

## AIへの指示例

```
循環的複雑度を減らして、この関数をリファクタリングしてください
```

AIは以下のような対応を行う：
- 複雑な関数を小さな関数に分割
- 早期リターンの適用
- 条件式の簡略化
- 適切なデザインパターンの適用

## 参考資料

- [Wikipedia: Cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
- [Microsoft Learn: Code metrics - Cyclomatic complexity](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-cyclomatic-complexity)
- [LinearB: Cyclomatic Complexity explained](https://linearb.io/blog/cyclomatic-complexity)
- [Codacy: Cyclomatic Complexity Complete Guide](https://blog.codacy.com/cyclomatic-complexity)
- [Sonar: What is Cyclomatic Complexity?](https://www.sonarsource.com/learn/cyclomatic-complexity/)

## まとめ

循環的複雑度は有用なメトリクスだが、他のコード品質指標と組み合わせて使用することが重要。閾値を設定し、継続的に監視することで、保守性の高いコードベースを維持できる。
