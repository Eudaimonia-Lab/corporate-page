# Eudaimonia Universe コーポレートサイト

## 概要

Eudaimonia Universe の企業サイト。静的HTMLサイト。

- **テーマ**: "Transforming Conflict into Emergence"
- **デザイン**: Cosmos × Lavender テーマ、ライトUI（白基調。2026-07 にダークからリニューアル）

## 構成

```
index.html          # 日本語ページ（CSS インライン、シングルページ構成、JS なし）
en/index.html       # 英語ページ（日本語版と同じ構成・同じ順序）
news/index.html     # お知らせ一覧（日）／ en/news/index.html（英）。JS なし方針のため HTML 直書き
llms.txt            # AI 向けの固定文まとめ（日英併記）
robots.txt          # AI クローラーを含む全許可
sitemap.xml         # / と /en/ を xhtml:link で相互参照
_redirects          # Netlify: /post/* → / 、en. サブドメイン → /en/
assets/
  eu_mark.svg       # 公式マーク（.ai 由来。ワードマークは含まない）
  site.css          # 全ページ共通のスタイルシート（CSS は 2026-08 に各ページのインラインから集約済み）
img/
  og-2026b-ja.png   # OGP 画像（日）1200x630。og-2026b-en.png が英。両者でコピーが異なる。
                    # 2026-09-07 に英国式つづりへ差し替え（旧 og-2026-*.png は SNS キャッシュ向けに残置）
  og-image.png      # 旧 OGP。2026-09 に上記へ差し替え済みで、どのページからも参照していない。
                    # 古いSNSキャッシュ向けにファイルだけ残している
scripts/
  verify-geo.py     # EU_website_spec.md §9 の検収チェックを機械実行
```

**設計書**: `EU_website_spec.md`（v1.0 / 2026.07、上位文書は EU_Brand_Identity_Guidelines_v3.html）。
サイトの構成・固定文・トークンはこの設計書が正。迷ったら正典 → 設計書 → 実装の順で参照する。

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

## サービス構成（2026-09 リニューアル）

組織向けの**主力3サービス**を先出しし、その下に既存の6領域を「対応する経営・組織課題」として畳む構成。

| サービス | ステータス表記 | 対応する課題 |
|---|---|---|
| 組織文化診断 / Culture Diagnostics | 稼働・実測済 | 組織変革・持続的な企業価値 |
| おかげさま / Okagesama | 稼働・自社 | 働きがい・エンゲージメント・部門間連携 |
| Compass | 本番稼働 | 組織内対立・リーダーシップ・意思決定 |

個人向けの「心豊かに生きる支援」は Source / Omusubi Quest / 操舵室 が担い、`/products/#personal` へ誘導する。
プロダクト10種は `/products/` に全部残し、主力を先出しするだけにとどめる（削除しない）。

**掲載してはいけない情報**（2026-09 の企画で確定）: 学会名・開催日／提携社名（個社固有の連携スキーム）／
測定項目提供者の実名／組織文化診断の実測数値。ステータスは上表のラベルのみで表し、数値は出さない。

**対立学の恒久レッドライン**（2026-09-07 追加）: 鎧の7分類（離脱／転嫁／依存／融解／置換／軽蔑／滅私）の
名称・定義／認知バイアス31種の一覧と4機能軸の詳細分類／軸別の具体的介入手法・禁忌・誤介入の罠（TRAP）は
**サイトに一切載せない**（Compass 等のサービス実装に直結する中核メソッド＝知財のため）。
対立学の説明は常に「構造・認知・価値・存在の4類型で診断する」という概要レベルに留める。
「鎧」「（対立学の文脈での）バイアス」という語そのものも出さない。
なお **Human OS ページの「バイアス」は別**（そちらはフレームワークの横断軸そのもので、掲載可）。

## Human OS の構造（2026-09-07 に全面更新）

旧「5層モデル」（body / emotion / mind / meaning / relationships）は**廃止**。現行モデルは次のとおりで、
サイト上の Human OS の説明はすべてこれに従う。

- **共通の源**: 価値観地図 / Value Map — 何を大切にするか。すべての判断がここから始まる
- **並列する2つの機能**: 認知の窓 / Cognitive Window（世界がどう見えるか）と
  コンピテンシー / Competency（何を発揮できるか）。**上下関係ではなく対等な並列**
- **横断する2つの軸**: バイアス / Bias（曲がる側）と 安定性 / Stability（折れる側）。両機能を横断し、対で働く
- 認知の窓の測定が、法人向けサービス **Compass** の理論的な裏付け

本体ページは `/research/human-os/`（日英）。`/research/` の `#consistency` は
**構造の再説明をせず**、問いのストーリーと Human OS ページへのリンクに留める（重複を避けるため）。
図解の CSS は `assets/site.css` の `.hosdiag`。研究セクション側で図を作り込まない。

## デザイントークン（CSS変数）

公式ロゴ（.ai）から抽出した確定値。2026年4月 pptx 由来の旧パレットは使わない（設計書 §4.1）。
両ページの `:root` で定義済みで、**日英で同一**。

| 変数 | 値 | 用途 |
|------|------|------|
| `--bg` / `--bg2` / `--card` / `--line` | #F7F8FC / #F1F3F9 / #FFFFFF / #E2E5EE | 背景・面・罫 |
| `--ink` | #353B4D | 本文 |
| `--indigo` | #29243E | 見出し |
| `--purple` | #5C4C87 | 補助・ナビ |
| `--gold` | #A28335 | ラベル（太字か18pt以上でのみ） |
| `--grey` | #8B92A4 | 装飾のみ。文字に使わない |
| `--wordmark` | #3F3B3A | ワードマーク |
| `--r-*` | #3BAD90 / #147EBF / #88167B / #DA3B49 / #EA953C / #F3CB3F | ロゴ6色 |

**鉄則**: ロゴ6色のうち文字に使ってよいのは `--r-purple` #88167B だけ（コントラスト 8.08:1）。
他の5色はカード上端のボーダー・アイコン・図版の塗りに限定する。`verify-geo.py` が機械チェックする。

## 開発

ローカルで確認する場合:

```bash
npx serve .
```

## SEO / GEO 運用ルール

**編集したら必ず `python3 scripts/verify-geo.py` を通す**（設計書 §9 の検収チェックリストを機械実行する）。
全 PASS を確認してから commit する。デプロイ後は `python3 scripts/verify-geo.py --live` でライブを再確認。
staging を検査するときは `--live --base https://<staging のオリジン>`。取得先だけが変わり、
canonical / hreflang の期待値は本番 URL のまま照合する（staging でも本番向け絶対 URL が入るのが正）。

**検査対象はトップの日英2ページだけ**（`PAGES` 定数）。`/news/` `/services/` `/products/` `/research/`
`/about/` `/contact/` は対象外なので、これらを触ったときは手で確認する。対象拡張は未対応の宿題。
`terms.html` / `privacy.html` は hreflang も JSON-LD も持っていない（旧デザインのまま）。

- **エンティティ定義は3箇所で一言一句同一**（2026-08 リニューアルで5箇所→3箇所に方針変更）: ファーストビュー本文
  (`p.def`) / FAQ 第1問の回答冒頭 / JSON-LD `Organization.description`。日英それぞれで揃える。
  meta description・og:description はこの3箇所とは独立した検索意図向けの要約文としてよい
  （GEOの引用対象＝エンティティ定義と、SEOのクリック誘導文＝メタディスクリプションを分離した。
  経緯は `docs/seo-geo-strategy.md`）。ただし meta description と og:description の2つは互いに一致させる。
  **この一致を verify-geo.py が検査するのはトップの日英だけ**で、下層ページは og を短い変化形にする運用が
  既存の実態になっている（2026-09 時点で一致しているのは4ページのみ）
- **例外: 日本語トップの `p.def` だけ主語が違う（2026-09 決定）**。ファーストビュー本文は
  「**私たちは、**人間科学の研究と…」で始め、FAQ 第1問と JSON-LD `Organization.description` は
  「ユーダイモニアユニバース（株式会社ユーダイモニアユニバース）は、…」のまま残す。
  読み口を軽くしつつ、LLM が引用する側（FAQ・JSON-LD）には社名と定義の結びつきを残すため。
  verify-geo.py は `lede_subject` の置換で変化形を**導出**して照合するので、定義本体を書き換えれば
  ファーストビューの検査も自動で追従する。主語以外が1文字でもずれれば FAIL する。
  **英語トップは社名のまま**（英語圏では社名と定義の結びつきがより重要なため、日英で主語の扱いが分かれる）
- **FAQ の同期**: 可視FAQ（`<details>`）・FAQPage JSON-LD・llms.txt を必ず同時に更新する。
  可視テキストと JSON-LD の全文一致は verify-geo.py が検査するので、要約版を書かない
- **FAQ は必ず HTML に最初から書く**。クリック後に JS で取得する実装は禁止（閉じた状態でもソースに全文
  あることが GEO の効果条件）
- **日英は必ず対で更新する**: 一方だけ直すと hreflang の相互参照と構成の対応が崩れる。セクションの順序も
  日英で同じに保つ
- **dateModified / lastmod の同期**: コンテンツ変更を含む push の前に、両ページ JSON-LD の
  `WebPage.dateModified` と sitemap.xml の `<lastmod>` を当日日付に更新する。
  無変更での日付更新はしない（スパムシグナルになるため）
- **可視語数**: 英語ページは `<details>` を閉じた状態で900語以内（設計書 §3）。verify-geo.py が検査する。
  持つ量は減らさず、見せる量を減らす（詳細は `<details>` に入れる）
- **用語の正準表記**: 「対立学」（英語は Conflictology 固定）／「Human OS」（半角・「モデル」を付けない）／
  対立学は「4タイプ」／プロセス表記は「構造理解→診断→介入設計→創発」／
  止揚の英語は **Synthese**（Synthesis は禁止）／プロダクトは Omusubi Quest（全大文字・「おむすび」表記は禁止）
- **英語は英国式つづりに統一（2026-09-07 決定）**: `organisation` / `organisational` / `centre` /
  `judgement` / `behaviour` / `programme` / `towards` / `catalogue` / `-ise` 系（formalise, organise,
  popularise, analyse）。**noun の practice は英国式でもそのまま**（動詞なら practise）。
  ポジショニングの固定文も **Human Science for Organisational Transformation** に変更済み
  （上位の EU_Brand_Identity_Guidelines_v3 側も要追随）。
  **変換してはいけない例外**: JSON-LD の `"@type": "Organization"` と `@id` の `#organization`、
  アンカー ID `id="organizations"`（`/products/#organizations` の参照先）、CSS の `center`。
  `verify-geo.py` の英語エンティティ定義文も英国式に更新済み
- **止揚に英語の等価語を当てない（2026-09 決定）**: 英語ページでは **Aufhebung** をそのまま使い、
  **sublation は使わない**。Synthese を synthesis より優先するのと同じ理由（英語語彙に置くと意味が流れる）。
  日本語版 `/about/philosophy/` からも「英語では sublation にあたります」を削除済み
- **OGP 画像は日英で別**（`img/og-2026b-ja.png` / `og-2026b-en.png`）。差し替えるときはファイル名を変えて
  SNS 側のキャッシュを切る。`og:image:width` / `height` も併記する
- **NEWS の構造化データは記事2件目から**。1件だけの間は `NewsArticle` / `ItemList` を入れない
- **robots.txt**: AIクローラーを含む全許可方針。Disallow を足す変更は要相談
- **お問い合わせは現在メール方式（2026-09、暫定）**: Netlify の Form detection が未有効で、
  フォームを POST すると 404 になり送信が消えていた（GET は 200 なのに POST だけ 404 になるのが
  この症状の見分け方）。`/contact/` `/en/contact/` は `mailto:` ボタンに差し替えてある。
  **復旧手順**: ① Netlify UI で Site configuration → Forms → Form detection を有効化
  ② 再デプロイする（フォーム登録はデプロイ時の HTML 解析で行われるため、①だけでは直らない）
  ③ Forms → Form notifications に info@eudaimonialab.org を追加
  ④ コミット `1d56731` の `<form>` ブロックを `/contact/` `/en/contact/` に復元する。
  `contact/thanks.html` / `en/contact/thanks.html` はその復元先として残してある（noindex・sitemap 未収録）
- **リダイレクト**: `_redirects` に旧実体の 301 を置いている。en.eudaimoniauniverse.com は現在 Wix 上で
  別サイトが生きており、DNS を Netlify に向けるまでこの行は発火しない（要対応。設計書 §1）

## 注意事項

- CSS は各ページにインラインで含まれている。**JS は使っていない**（言語切替は `/en/` への通常リンク。
  JS 依存の言語トグルは AI クローラーに英語が見えないため 2026-07-28 に廃止した）
- 画像追加時は `assets/` ディレクトリに配置
- `terms.html` / `privacy.html` は旧デザインのまま。新パレットへの追随は未対応
- OGP 画像は 2026-09 に日英別で作り直し済み（→ 構成の `img/`）。なお旧 `og-image.png` も
  マーク・ワードマークは現行ブランドのままだった。不足していたのはポジショニングの一行と背景色で、
  「旧デザインの画像」という以前の記述は実物と食い違っていた
