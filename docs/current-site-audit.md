# 現状サイト監査（2026-07-30 リニューアル前）

対象: https://eudaimoniauniverse.com/ ｜ リポジトリ: Eudaimonia-Lab/corporate-page（ローカル ~/Project/eulabwebsite）

## 技術スタック

| 項目 | 現状 |
|---|---|
| フレームワーク | なし（手書き静的HTML、CSSは各ページにインライン、JSなし） |
| ルーティング | ファイルベース（`/index.html`、`/en/index.html` の2ページ＋terms/privacy） |
| レンダリング | 完全静的。SSR/CSRなし |
| ローカライズ | 日英を別ファイルで手動維持。hreflang相互参照あり |
| スタイル | インライン `<style>`（ページごとに重複） |
| CMS | なし。HTMLが正 |
| メタデータ | 手書き。title/description/OG/Twitter/canonical/hreflang 完備 |
| 構造化データ | JSON-LD `@graph`（Organization/Person/WebSite/WebPage/Service/FAQPage） |
| sitemap | `/sitemap.xml`（4 URL、xhtml:link 相互参照つき） |
| robots.txt | AIクローラー含む全許可（UAごとに明示 Allow） |
| アナリティクス | なし（サイトにトラッキングスクリプトなし） |
| フォーム | なし。mailto: info@eudaimonialab.org のみ |
| メール送信 | なし |
| ホスティング | Netlify。main push = 本番自動デプロイ。リモートに staging ブランチあり |
| リダイレクト | `_redirects`: `/post/*`→`/` 301、en.サブドメイン→`/en/`（DNS未切替のため未発火） |
| フォント | システムスタック（Georgia系serif / Helvetica系sans）。Webフォント読込なし |
| 画像 | ロゴSVG（インライン重複）、favicon群、旧デザインの og-image.png |
| アクセシビリティ | セマンティックHTML、SVGにaria-label。スキップリンク・フォーカス表示は未整備 |
| パフォーマンス | 軽量（2ページ、JSゼロ）。serve.json はローカル確認用 |
| 検収スクリプト | `scripts/verify-geo.py`（エンティティ定義5箇所一致・FAQ同期・禁止表記・ロゴ色を機械検査） |
| サードパーティ | なし |
| セキュリティ | 静的サイト。環境変数・秘密情報なし |

## インデックス済みURL（把握分）

- `/`、`/en/`、`/terms.html`、`/privacy.html`
- 旧実体: `www.eudaimoniauniverse.com/post/*`（301済）、`en.eudaimoniauniverse.com`（Wix上に残存、DNS未切替）

## コンテンツ構造（リニューアル前）

日英とも1ページ構成: hero → purpose → method → humanos → conflictology → divisions(＋10プロダクト表) → faq(10問) → contact(会社概要)。

## 課題（今回のリニューアルの根拠）

1. **哲学が先、提供価値が後**: ファーストビューが「対立の止揚」の思想説明で、企業向けの提供価値・サービスが後段。
2. **プロダクト一覧がトップに露出**: 10製品の表がトップの中心を占める。
3. **サービスの受け皿ページがない**: 組織変革・リーダーシップ・エンゲージメント等の商用検索意図に対応するURLが存在しない。
4. **研究資産の個別ページがない**: Human OS・対立学等が深掘りできず、引用可能性（GEO）が1ページに集中。
5. **問い合わせ動線が mailto のみ**: 種別選択・フォームがない。
6. **既知の負債**: terms/privacy が旧デザイン、og-image.png が旧ブランド、en.サブドメインDNS未切替。

## 維持すべき強み

- エンティティ定義の複数箇所一致・FAQ同期・llms.txt などのGEO規律と verify-geo.py の機械検査
- JSなし・軽量・全文がHTMLに存在するクローラビリティ
- 公式ロゴ由来のデザイントークンとコントラスト実測表（EU_website_spec.md §4）
- FAQ 10問×2言語の蓄積、確認済みの会社事実（法人番号・所在地・著書）
