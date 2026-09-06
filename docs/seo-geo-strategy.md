# SEO / GEO 戦略（2026-08 リニューアル）

## エンティティ定義(GEO引用対象)の正本

3箇所で一言一句同一(2026-08に5箇所→3箇所へ方針変更。理由は下記「meta description の分離」参照)。

- ファーストビュー本文 `<p class="def">`(トップページのみ)
- FAQ 第1問の回答冒頭(トップページのみ)
- JSON-LD `Organization.description`(全ページ、`@id: https://eudaimoniauniverse.com/#organization` を参照)

**JA**: ユーダイモニアユニバース（株式会社ユーダイモニアユニバース）は、人間科学の研究と組織変革を行う、日本発の Think & Do Tank です。価値観、感情、認知、意味、関係性に関する独自研究を、組織で活用できるフレームワーク、診断、テクノロジーへと転換し、人と事業がともに持続的に成長する経営を支援します。

**EN**: Eudaimonia Universe is a human science research and organizational transformation company based in Japan. We turn original research on values, emotions, cognition, meaning, and relationships into practical frameworks, diagnostics, and technologies that help organizations strengthen culture, leadership, decision-making, and meaningful work.

研究ページ(`/research/*/`)では、上記トップページ定義の代わりに各フレームワーク固有の `DefinedTerm.description` を正本として使う(例: Human OSの定義、対立学の定義)。ページ内では `.answer .q`(質問)+`.answer p`(回答)のAnswer-First形式と、JSON-LD `DefinedTerm.description` を一致させる。

## meta description の分離(2026-08 の方針変更)

旧サイトは meta description / og:description もエンティティ定義と一言一句同一にする「5箇所一致」ルールだった。リニューアルではこれを廃止し、**meta description は検索意図に最適化した独立の要約文**とした。

**理由**: 指示書 §18 が「全ページでユニークな title/description」を要求しており、かつ GEO用の長い定義文(155字超)をそのまま meta description に使うと検索結果で末尾が切れ、クリック率最適化の機能を果たさない。エンティティ定義(引用されるための正確な定義)と meta description(クリックを誘導する要約)は目的が異なるため、意図的に分離した。

**維持する制約**: `verify-geo.py` は meta description と og:description の2つが**互いに**一致すること、および両方が空でないことを検査する(OGP表示の一貫性のため)。GEO側の3箇所一致とは別軸の検査。

## 検索意図マッピング(ページ単位で1意図)

指示書 §17 のキーワード群を、ページごとに主たる意図1つへ割り当てた(キーワードの水増しをしない指示書の方針に従う)。

| ページ | 主たる検索意図 |
|---|---|
| `/` | Eudaimonia Universe とは何か(エンティティクエリ) |
| `/services/` | 組織変革・組織開発コンサルティング(商用クエリ) |
| `/research/` | 独自研究の全体像(調査クエリ) |
| `/research/human-os/` | Human OS とは(定義クエリ) |
| `/research/conflictology/` | 対立学 / Conflictology とは(定義クエリ) |
| `/research/source-108/` | Source 108 とは(定義クエリ) |
| `/research/ikigai-management/` | Ikigai Management とは(定義クエリ) |
| `/research/crv/` | CRV とは(定義クエリ) |
| `/products/` | Eudaimonia Universe のプロダクト一覧(ナビゲーショナルクエリ) |
| `/about/` | 会社概要・創業者(ナビゲーショナル/エンティティクエリ) |
| `/about/philosophy/` | 止揚・Synthese Society とは(定義クエリ) |
| `/contact/` | 問い合わせ(トランザクショナルクエリ) |

## GEO運用ルール(継続、`CLAUDE.md` と重複しないよう要点のみ)

- FAQを持つページ(トップ6問、`/research/conflictology/` 4問、`/about/philosophy/` 2問)は、可視 `<details>` テキストと `FAQPage` JSON-LD を全文一致させる。`verify-geo.py` はトップページのみ自動検査(下記「既知の限界」参照)。
- 研究ページは Answer-First(定義→概要→構造→開発経緯・根拠状態→限界→引用)の順を崩さない。根拠の状態(evidence status)は誇張しない: 「検証中」「実務を通じて開発」であって「実証済み」ではない。
- 用語の正準表記(対立学=Conflictology固定、Human OS、止揚の英語はSynthese等)は `CLAUDE.md` を正本とする。

## 既知の限界(次フェーズで対応)

- `scripts/verify-geo.py` は `index.html` / `en/index.html` の2ファイルのみを検査する設計(旧サイトが2ページ構成だった名残)。新設した12ページ×2言語には自動検査が及んでいない。今回のQAは目視+個別 `python3 -c` チェックで代替した。将来的に `PAGES` 辞書を全ページへ拡張し、ページ種別ごとに検査項目(FAQ同期はFAQ保有ページのみ、エンティティ定義3箇所一致はトップと各研究ページのみ等)を出し分ける改修が必要。
- `/impact/` `/insights/` は本リニューアルのスコープ外(`docs/information-architecture.md` 参照)。将来追加する際は、追加ページ分のURLをこのファイルの検索意図マッピングと `sitemap.xml` に追記すること。
