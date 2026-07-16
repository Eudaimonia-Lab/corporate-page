# Eudaimonia Universe コーポレートサイト

## 概要

Eudaimonia Universe の企業サイト。静的HTMLサイト。

- **テーマ**: "Transforming Conflict into Emergence"
- **デザイン**: Cosmos × Lavender テーマ、ダークUI

## 構成

```
index.html          # メインページ（CSS/JS インライン、シングルページ構成）
assets/
  logo-mark.png     # ロゴ画像
```

## 技術スタック

- 静的HTML/CSS/JS（フレームワークなし）
- フォント: Google Fonts（Noto Sans JP, Inter）
- ホスティング: **Netlify**（リポジトリ: `Eudaimonia-Lab/corporate-page`）

## デプロイとロールバック

- **main への push = Netlify 自動デプロイ = 本番公開**。push 前に必ず確認を取る
- リモートに `staging` ブランチあり。大きめの変更は staging で確認してから main へ
- ロールバック: ① `git revert` して push、または ② Netlify UI の Deploys 履歴から
  以前のデプロイを "Publish deploy" で復元（緊急時はこちらが速い）
- 視覚的変更の完了条件は `.claude/rules/frontend-verify.md` に従う

## Git 運用

- `git config user.email` はこのリポジトリでは `aya.mizuno@gmail.com`
- コミットは conventional commits（feat/fix/docs/chore）＋日本語説明可

## デザイントークン（CSS変数）

主要カラーは `:root` で定義済み:

| 変数 | 用途 |
|------|------|
| `--teal` (#00B5A0) | アクセント / CTA |
| `--blue` (#4A70B5) | メインカラー |
| `--purple` (#7B50A3) | サブカラー |
| `--magenta` (#D64A8C) | ハイライト |
| `--yellow` (#E8C830) | ゴールド / 強調 |
| `--bg` (#06080F) | 背景色 |

## 開発

ローカルで確認する場合:

```bash
npx serve .
```

## SEO / GEO 運用ルール

- **dateModified / lastmod の同期**: コンテンツ変更を含む push の前に、index.html 内 JSON-LD の
  `WebPage.dateModified` と sitemap.xml の `<lastmod>` を当日日付に更新する。
  無変更での日付更新はしない（スパムシグナルになるため）
- **FAQ の同期**: 可視FAQセクション・FAQPage JSON-LD・llms.txt の文言を変えるときは必ず3箇所同時に更新する
- **用語の正準表記**: 「対立学」（英語は Conflictology 固定）／「Human OS」（半角・「モデル」を付けない）／
  対立学は「4タイプ」・Human OSは「5層」／プロセス表記は「構造理解→診断→介入設計→創発」
- **robots.txt**: AIクローラーを含む全許可方針。Disallow を足す変更は要相談

## 注意事項

- CSS/JS は index.html にインラインで含まれている。将来的にファイル分離を検討
- 画像追加時は `assets/` ディレクトリに配置
