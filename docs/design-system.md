# デザインシステム（2026-08 リニューアル）

正本は `assets/site.css`。ここではその設計意図とコンポーネント規約を文書化する。旧サイトは各ページにインラインCSSを重複させていたが、リニューアルで単一の外部スタイルシートに統合した（全ページ `<link rel="stylesheet" href="/assets/site.css">` を参照）。

## デザインコンセプト

洗練された知性・安心感・わかりやすさ。マッキンゼー水準の情報量規律（1画面あたりの主張は1つ、装飾より余白）を採用しつつ、既存ブランドの色彩・書体資産（公式ロゴ由来のトークン）は変更しない。

## カラートークン

`assets/site.css` の `:root` で定義。**日英で完全同一**。

| 変数 | 値 | 用途 |
|---|---|---|
| `--bg` / `--bg2` / `--card` / `--line` | #F7F8FC / #F1F3F9 / #FFFFFF / #E2E5EE | 背景・面・罫線 |
| `--ink` | #353B4D | 本文 |
| `--indigo` | #29243E | 見出し |
| `--purple` | #5C4C87 | 補助・ナビリンク |
| `--gold` | #A28335 | ラベル(klabel)。太字か18pt以上でのみ使用 |
| `--grey` | #8B92A4 | 装飾専用。文字色に使わない |
| `--wordmark` | #3F3B3A | ワードマーク |
| `--teal` / `--steel` / `--magenta` | #39817F / #386F8B / #8B4383 | CTA・リンクアクセント |
| `--r-green/blue/purple/red/orange/yellow` | #3BAD90 / #147EBF / #88167B / #DA3B49 / #EA953C / #F3CB3F | 公式ロゴ6色。カード上端ボーダー・図版塗りに限定 |
| `--ink-on-dark` / `--sub-on-dark` / `--line-on-dark` | #EDEFF6 / #B9BDD0 / rgba(241,243,249,.18) | `.sec-dark` セクション内の文字色 |

**鉄則（`verify-geo.py` が機械チェック）**: ロゴ6色のうち文字色に使ってよいのは `--r-purple` #88167B のみ(コントラスト比8.08:1)。他の5色はカード上端ボーダー・アイコン・図版の塗りに限定する。

## タイポグラフィ

- `--serif`: Georgia系(見出し・引用)
- `--sans`: Helvetica Neue/Inter系(本文)
- `--label`: Cambria/Georgia系(ラベル・小見出し)
- `--brand`: Futura/Avenir Next系(ロゴワードマーク専用)

日本語本文の行間は `body{line-height:1.9}`、英語ページは `html[lang="en"] body{line-height:1.65}` で上書き(言語ごとに可読性を最適化する指示書 §5・§14 に対応)。

## グリッドとレイアウト

- `.wrap{max-width:1000px;margin:0 auto;padding:0 30px}` を全セクション共通のコンテナとして使用
- `.grid.g2` / `.g3` / `.g5` — `repeat(auto-fit,minmax(...))` によるレスポンシブグリッド(2/3/5カラム)
- カードは真にモジュール的な内容(研究フレームワーク、サービス領域、プロダクト)にのみ使用。サービス詳細・プロセス説明は `.numsec`(番号付きリスト)や `.svc`(2カラム分割)を優先し、指示書 §14 の「SaaSカードグリッドの多用を避ける」方針に従う

## 共通コンポーネント(ページテンプレート)

全下層ページで再利用しているパターン:

1. `<nav class="top">` — ロゴ・4項目ナビ・CTA・言語切替。`aria-current="page"` で現在地を示す
2. `.crumbs` — パンくずリスト
3. `.pagehead` — h1 + `.answer`(Answer-First定義ブロック、GEO対応)
4. `<section>` の繰り返し — 各節先頭に `.klabel`(英語ラベル)+ `<h2>`
5. 研究ページ専用: `.meta`(著者・公開日・最終確認日)、`.evidence`(根拠の状態を明示するボックス)、`.citebox`(推奨引用)
6. `.sec-dark` — 各ページ末尾のCTAセクション。`--ink-on-dark` 系トークンで反転
7. `<footer>` — 社名・言語切替・メール・利用規約/プライバシーポリシーへのリンクを1行で統一(全ページ共通パターン。研究サブページ10ファイルは2026-08-09に本パターンへ統一済み)
8. JSON-LD `<script type="application/ld+json">` — ページ種別ごとに `WebPage`/`AboutPage`/`ContactPage` + `BreadcrumbList` を最小限含む。トップページのみ `Organization`/`Person`/`WebSite`/`Service`/`FAQPage` のフル `@graph` を持つ

## フォーム(Contact)

`/contact/` `/en/contact/` のみ、ページ内 `<style>` でフォーム専用スタイル(`.formgrid` 等)を追加している。他ページへの汎用化はまだ行っておらず、今後フォームを増やす場合は `assets/site.css` へ昇格を検討する。

## モーション

`prefers-reduced-motion: reduce` を `assets/site.css` の先頭で無効化(`scroll-behavior:auto` + アニメーション全停止)。装飾的な常時アニメーションは使用していない。
