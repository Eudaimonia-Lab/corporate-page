# GEO/SEO強化 実装ドラフト提案書 — eudaimoniauniverse.com

作成日: 2026-07-17 ／ 対象リポジトリ: `/Users/aya/Project/eulabwebsite/`（Netlify、main push = 本番公開）
本書は「リサーチ結果」「コンテンツ（A）」「テクニカル（B）」「戦略（C）」の3ドラフトを統合したもの。記載の行番号・既存コード・既存コピーはすべて実ファイル（index.html / robots.txt / sitemap.xml）と照合済み。

---

## ① 方針サマリ

1. AIクローラーはJSON-LDを構造として解釈せず「見えるテキスト」を抽出するため、**可視の定義文・FAQが主、スキーマが従**。独自造語（Human OS／対立学）の「一次定義元」ポジションをHTML本文で確保することが最大のレバレッジ。
2. 日本語は静的HTMLで完全に見えているが、**英語は `translations` オブジェクト（JS内）にのみ存在し、JS非実行のAIクローラーには不可視**。英語圏での引用を狙うなら静的 `/en/` 化が唯一の確実な対策。
3. robots.txt は現状の全許可が既に正解。llms.txt は効果を期待しない「安い保険」として最後に置く。
4. AIのナレッジ定着には自社サイト内の反復だけでは不十分。**正準定義の一字一句同一の反復を、サイト外（note・プレス・登壇）で積む**運用をセットにする。

---

## ② 優先度付き施策一覧（効果 × 工数）

| Phase | 施策 | 効果 | 工数 | 本書の該当節 |
|---|---|---|---|---|
| **P1**（30分） | llms.txt 設置 | 低〜中（Perplexity系のみ実効） | 15分 | ⑤ |
| **P1** | robots.txt 明示化 | ほぼゼロ（宣言的価値のみ） | 10分 | ⑥ |
| **P1** | Netlify層のボットブロック監査 | 中（27%のB2Bサイトが意図せずブロックの事故防止） | 15分 | 本節末尾 |
| **P2**（半日） | 可視FAQセクション新設 + JSON-LD全置換 | **高**（独自造語の定義元独占） | 半日 | ③・⑦ |
| **P2** | 既存コピー微修正（定義文の抽出可能化） | 高（工数比で最良） | 1時間 | ④・⑧ |
| **P2** | dateModified / lastmod 運用ルール化 | 中（Perplexityの鮮度重視対応） | 15分 | 本節末尾 |
| **P3**（1〜2日） | 英語静的ページ `/en/` + hreflang + sitemap更新 | **高**（英語圏で現状ゼロ→可視化） | 1〜2日 | 本節「P3スケッチ」 |
| **P3** | Bing Webmaster Tools 登録 | 中（ChatGPTエージェント検索の約92%がBingインデックス依存） | 30分 | — |
| **継続** | サイト外での正準定義の反復（note・プレス・登壇） | 高（AIナレッジ定着の本丸） | 継続 | ⑨ |

### P3 実装スケッチ: `/en/` 静的化

英語対応の選択肢のうち、noscript埋め込み・プリレンダリングサービス・両言語CSS切替はいずれも不採用（理由は⑩）。**静的 `/en/index.html` 生成 + hreflang** を採用する。

1. **生成方式**: en辞書は `index.html` 1334行目〜の `const translations` に完備（`data-i18n` 163箇所）。ビルドスクリプト `scripts/build-en.mjs`（Node + cheerio）で `index.html` を読み、en辞書を適用 → `lang="en"`、title / meta description / OGP（`og:locale` を `en_US`）/ canonical（`/en/` 自己参照）/ JSON-LD（`inLanguage: "en"`、FAQPage英語版）を差し替えて `en/index.html` へ出力。単一ソース維持で翻訳ドリフトを防ぐ。Netlifyビルドコマンドに設定するか、コミット前にローカル実行。
2. **hreflang**（両ページの `<head>` に追加）:
```html
<link rel="alternate" hreflang="ja" href="https://eudaimoniauniverse.com/">
<link rel="alternate" hreflang="en" href="https://eudaimoniauniverse.com/en/">
<link rel="alternate" hreflang="x-default" href="https://eudaimoniauniverse.com/">
```
3. **canonical**: `/en/` は自己参照canonical（ルートに向けると英語ページがインデックスから消える）。
4. **sitemap.xml**: `/en/` を追加し `xhtml:link` で相互参照（`xmlns:xhtml="http://www.w3.org/1999/xhtml"` を urlset に追加）。terms.html / privacy.html は現行のまま。
5. **言語トグル**: JAページの `setLang('en')` ボタンは `/en/` への通常リンクに変更（JSトグルは廃止が最も安全）。`navigator.language` による自動リダイレクトはしない（クローラーとの齟齬の温床）。案内バナー程度に留める。
6. `/en/` 完成までの暫定措置は llms.txt の英語定義（⑤）でカバー。

### 運用ルール2点（P1/P2で導入）

- **Netlifyボット監査**（デプロイ後にライブURLで実行、全て200を確認。403/429ならNetlifyのFirewall / Traffic Rules / AI bot設定を解除）:
```bash
for UA in "GPTBot" "OAI-SearchBot" "ChatGPT-User" "ClaudeBot" "Claude-SearchBot" "PerplexityBot" "Perplexity-User" "CCBot"; do
  printf "%-18s -> " "$UA"
  curl -s -o /dev/null -w "%{http_code}\n" -A "$UA" https://eudaimoniauniverse.com/
done
```
- **dateModified / lastmod の同期3点セット**: ①JSON-LD `WebPage.dateModified`、②`sitemap.xml` の `<lastmod>`、③（P3後）`/en/` 側。**実際に内容を更新した時だけ**日付を上げる（無変更の日付更新はスパムシグナル）。CLAUDE.md に「コンテンツ変更を含む push 前に dateModified / lastmod を当日日付に更新」と1行追記する。

### 完了条件（`.claude/rules/frontend-verify.md` 準拠）

- `curl -s https://eudaimoniauniverse.com/llms.txt | head -3` と `curl -s https://eudaimoniauniverse.com/robots.txt` がライブで新内容を返す
- `curl -s https://eudaimoniauniverse.com/ | grep -c 'faq-q'` でFAQが**生HTML**に存在（JSレンダリング後でなく）
- JSON-LD: validator.schema.org でエラーゼロ、Google Rich Results Test で FAQPage / Organization 認識
- UA別curlが全て200
- P3後: `curl -s https://eudaimoniauniverse.com/en/ | grep -i '<html lang="en"'` と hreflang相互参照をGSCで確認
- 視覚的変更（FAQ追加・言語トグルのリンク化）はheadlessスクリーンショットで前後比較してから完了報告

### デプロイ運用

main への push = Netlify 自動デプロイ = 本番公開。P2以降（見た目が変わる変更）は staging ブランチで確認してから main へ。P1（txt 2ファイル）は main 直でも可、ただし push 前確認は維持。

---

## ③ FAQセクション完成ドラフト（全文・8問）

**設置位置**: About セクション（1126行目〜）の直後、Newsletter セクション（1165行目〜）の前。会社情報を読んだ直後にFAQが来る流れが自然なためこの位置とする。**回答は質問見出し `<h3>` の直後に `<p>` で完結させる**（AI抽出の要件）。ナビへの追加は任意。

**多言語対応**: `translations` の ja / en 双方に `faq-title`, `faq-q1`〜`faq-a8` のキーを追加（ja辞書の値は下記HTMLと同一文言にする）。

```html
<!-- ==================== FAQ ==================== -->
<section class="section section-bordered" id="faq" style="z-index:1; position:relative;">
  <div class="container">
    <div class="fi" style="margin-bottom:40px;">
      <p class="section-label">FAQ</p>
      <h2 class="section-title" data-i18n="faq-title">よくあるご質問</h2>
    </div>
    <div class="fi">
      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="faq-q1">Eudaimonia Universe（ユーダイモニアユニバース）はどのような会社ですか？</h3>
        <p data-i18n="faq-a1">Eudaimonia Universe, Inc.（株式会社ユーダイモニアユニバース）は、組織や社会に生じる対立を構造から診断し、新しい合意・意思決定・関係性の設計を支援するThink &amp; Do Tankです。独自開発した理論「Human OS」と「対立学」を基盤に、研究（Think Tank）・実装（Produce）・資産化（Asset）の3部門が循環する体制をとっています。Founder &amp; CEOはTakayuki Mizuno（水野 貴之）です。</p>
      </div>
      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="faq-q2">Human OSとは何ですか？</h3>
        <p data-i18n="faq-a2">Human OSとは、人間の内的構造をBody（身体）・Emotion（感情）・Mind（思考）・Meaning（意味）・Relationship（関係性）の5層で捉える、Eudaimonia Universeが独自開発したモデルです。対立の診断では「どの層で何が起きているのか」を読み解く共通言語として使います。</p>
      </div>
      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="faq-q3">対立学（Conflictology）とは何ですか？</h3>
        <p data-i18n="faq-a3">対立学（Conflictology）とは、対立を「価値」「構造」「認知」「存在」の4タイプに分類して診断する、Eudaimonia Universeが独自開発したフレームワークです。どのタイプの対立が・どこで起きているのかを診断してから打ち手を選ぶことで、的外れな介入を避けます。</p>
      </div>
      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="faq-q4">組織の対立は、なぜ話し合いだけでは解決しないのですか？</h3>
        <p data-i18n="faq-a4">対立は単一の原因ではなく、複数の要因が同時に絡んで発生する構造的な現象だからです。原因のタイプを特定しないまま話し合いを重ねても、打ち手が原因と噛み合わず空振りします。だからこそ、私たちは対立をいきなり解決しようとせず、まず診断を行います。</p>
      </div>
      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="faq-q5">「介入」とは具体的に何をするのですか？</h3>
        <p data-i18n="faq-a5">介入とは、対立の構造に働きかける具体的な打ち手のことです。論点を捉え直す問いの設計（視点の再構成）、会議体や合意形成プロセスの組み直し（意思決定の再設計）、役割や対話の場のつくり直し（関係性の再定義）などが含まれます。唯一の正解を押しつけるのではなく、診断結果に基づいて、その組織にとっての最適解を設計します。</p>
      </div>
      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="faq-q6">支援はどのようなプロセスで進みますか？</h3>
        <p data-i18n="faq-a6">支援は「構造理解 → 診断 → 介入設計 → 創発」の4ステップで進みます。まずHuman OSの5層で関わる人々の内的構造を把握し、次に対立学の4タイプで対立がどこで・なぜ起きているのかを診断します。診断に基づきAIの分析を活用しながら介入を設計し、対立を起点に新しい関係性・意味・これまでなかった選択肢が立ち上がる状態（創発）を目指します。</p>
      </div>
      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="faq-q7">AIはどのように活用されていますか？</h3>
        <p data-i18n="faq-a7">介入を設計するのは私たち人間であり、AIはその分析を支援する役割を担います。Human OSと対立学にAIによる分析を組み合わせて対立の構造を読み解くことで、介入設計をより速く、より精緻にします。また、対立の診断から介入プランの提示までを支援するAIプロダクトの開発も進めています。</p>
      </div>
      <div class="card">
        <h3 data-i18n="faq-q8">どのような相談ができますか？</h3>
        <p data-i18n="faq-a8">組織変容・事業開発の実装プロジェクトのほか、Human OS・対立学の共同研究、投資・パートナーシップ、取材・講演のご相談をお受けしています。新規事業開発部門、組織開発部門、人事部門、経営管理室等の皆さまが主な想定窓口で、課題の整理段階からご一緒します。ご連絡は info@eudaimonialab.org へ（日本語・英語対応）。</p>
      </div>
    </div>
  </div>
</section>
```

**同期ルール**: 可視FAQテキスト・FAQPage JSON-LD（⑦）・llms.txt（⑤）の文言を変えるときは必ず同時に更新する（不一致はスパムシグナル）。

---

## ④ 引用可能な定義文 5本

いずれも「〜とは、…である」形式で、文単体で切り取られても主語・帰属が保たれる。既存コピーと用語・内容を照合済み。

| 用語 | 定義文 | 設置位置 |
|---|---|---|
| Human OS | Human OSとは、人間の内的構造を身体・感情・思考・意味・関係性の5層で捉える、Eudaimonia Universeの独自モデルであり、対立の診断と介入設計の土台となる。 | FAQ Q2 ＋ Human OSセクション（⑧-②で反映） |
| 対立学 | 対立学（Conflictology）とは、対立を価値・構造・認知・存在の4タイプに分類して診断する、Eudaimonia Universeの独自フレームワークである。 | FAQ Q3 ＋ Conflictologyセクション冒頭（⑧-③で反映） |
| 創発 | 創発とは、既存の要素の単なる統合ではなく、新しい関係性や意味が立ち上がる現象である。 | 既存の purpose-quote（740行目）と同旨。FAQ Q6の補足として機能 |
| 介入 | 介入とは、対立の構造に働きかける具体的な打ち手であり、問いの設計、会議体・合意形成プロセスの組み直し、対話の場のつくり直しなどを指す。 | FAQ Q5冒頭。既存の approach-desc・hero-desc のダッシュ挿入型定義と整合 |
| Think & Do Tank | Think & Do Tankとは、研究と現場実装を一体で担う組織形態で、Eudaimonia Universeは研究・実装・資産化の3部門の循環で実践している。 | FAQ Q1 ＋ Aboutセクション（既存文がほぼこの形。修正不要） |

**正準表記の運用ルール**（全媒体共通・サイト外発信にも適用）:
- 「対立学」は常にこの3文字。英語定訳は「Conflictology」に固定。「Human OS」は半角・大文字OS固定（「ヒューマンOS」等のカナ表記は使わない）。
- 初出時は必ず「Eudaimonia Universeの独自理論『Human OS』」のように**提唱主体を冠する**（一般語との曖昧性解消。「対立学」も同様）。
- 上記の一文定義を、サイト・note・プレスリリース・登壇プロフィール・書籍紹介文・SNS bioで**一字一句同じ形で**反復する。AIの引用は「複数ソースで一致する定義文」に強く寄る。
- 「Human OS」「対立学」は造語のため定義文に必ず帰属語（独自／Eudaimonia Universe）を残す。「創発」「介入」「Think & Do Tank」は一般語のため帰属は文脈側で補う。

---

## ⑤ llms.txt 完成ドラフト（全文）

設置先: `/Users/aya/Project/eulabwebsite/llms.txt`（→ `https://eudaimoniauniverse.com/llms.txt`）。Netlifyは静的ファイルをそのまま配信するので追加設定不要。

**設計判断**: 本文は英語主体＋日本語併記。英語コンテンツが現状HTMLから不可視なため、`/en/` 完成までは llms.txt が英語定義の唯一の静的置き場を兼ねる。記載事実はすべてサイト掲載情報のみ。

```markdown
# Eudaimonia Universe, Inc.

> Eudaimonia Universe, Inc. (株式会社ユーダイモニアユニバース) is a Japanese "Think & Do Tank" founded and led by Takayuki Mizuno (水野貴之). It diagnoses the structure of social and organizational conflict — dualisms and clashes of competing values and justices — and helps organizations redesign agreements, decision-making, and relationships. Mission: "Transforming Conflict into Emergence"（社会の対立を、創発へと変換する）.

## Core concepts (original frameworks defined by Eudaimonia Universe)

- **Human OS**: An original model that views human inner structure as five layers — Body, Emotion, Mind, Meaning, and Relationship（身体・感情・思考・意味・関係性）. Used to locate where a conflict actually lives within and between people.
- **Conflictology（対立学）**: An original framework that classifies conflict into four types — Value（価値）, Structure（構造）, Cognition（認知）, and Existence（存在） — so a conflict is correctly diagnosed before any intervention is designed.
- **Process**: structural understanding → diagnosis → intervention design → emergence（構造理解→診断→介入設計→創発）. An "intervention" is a concrete move on the structure of a conflict: designing questions, restructuring meeting bodies and consensus-building processes, and redesigning dialogue settings. Humans diagnose and design; AI supports the analysis.

## Organization

- **Think Tank Division** — research on human inner structure and conflict
- **Produce Division** — implementation in organizations; consultation window for client work
- **Asset Division** — turning research and field results into reusable intellectual assets

Typical clients: corporate teams in new business development, organization development, HR, and corporate planning / management offices（新規事業開発・組織開発・人事・経営管理室等）.

## Projects

- **Ikugyo（育業）** — self-initiated social implementation project
- **The Guild** — self-initiated social implementation project
- **Giver research（Giver研究）** — research project

## Books by the founder

- [ikigai経営術 — 自己実現を企業の原動力に変える方法 (Japanese)](https://amzn.asia/d/07vj6FGu): by Takayuki Mizuno（水野貴之）
- [ikigai intelligence — Transforming personal purpose into a growth engine for your organization (English)](https://amzn.asia/d/0hevtcf2): by Takayuki Mizuno

## Key pages

- [Home](https://eudaimoniauniverse.com/): company overview, Human OS, Conflictology, divisions, projects, publications, contact. Japanese; English available via on-page toggle.
- [Human OS](https://eudaimoniauniverse.com/#humanos)
- [Conflictology](https://eudaimoniauniverse.com/#conflictology)
- [FAQ](https://eudaimoniauniverse.com/#faq)
- [Contact](https://eudaimoniauniverse.com/#contact): info@eudaimonialab.org (Japanese / English)

## Optional

- [Terms of Service](https://eudaimoniauniverse.com/terms.html)
- [Privacy Policy](https://eudaimoniauniverse.com/privacy.html)
```

補足: P3で `/en/` を作ったら Key pages に1行追記する。効果は限定的（OpenAI・Google・Anthropicの主要クローラーは取得しない。Perplexityは活用報告あり）と割り切り、HTML本文の改善（③④⑧）を先行させる。

---

## ⑥ robots.txt 改訂案

設置先: `/Users/aya/Project/eulabwebsite/robots.txt`（現行4行を置換）。

**前提の明示**: 現行の `User-agent: * / Allow: /` は「引用されたい」目的には既に機能的に正解で、改訂による実効差は**ゼロ**。改訂の価値は (a) 方針の宣言（後日誰かが安易に Disallow を足す事故の防止）、(b) 監査時のチェックリスト化、の2点のみ。**特定 User-agent グループを持つボットは `*` グループを無視する**ため、明示する各グループに必ず `Allow: /` を書くこと。

```
# robots.txt — eudaimoniauniverse.com
# 方針: AI クローラーを含む全クローラーに全ページの取得を許可（AI回答での引用と将来モデルでの言及を最大化）
# 注意: 個別グループを持つボットは「*」グループを無視するため、各グループに Allow: / を明示すること
# 注意: ここで許可しても CDN/WAF 層（Netlify）でブロックされ得る。デプロイ後にUA別curl監査を実施

# --- 検索エンジン ---
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# --- AI 検索・回答系（ブロックすると引用資格を失う） ---
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

# --- AI 学習用（将来モデルの学習データでの言及機会） ---
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: meta-externalagent
Allow: /

# --- その他すべて ---
User-agent: *
Allow: /

Sitemap: https://eudaimoniauniverse.com/sitemap.xml
```

---

## ⑦ JSON-LD 追加コード（既存ブロックの全置換）

`index.html` 34〜71行目の既存 `<script type="application/ld+json">` ブロック（Organization + WebSite）を以下で**丸ごと置換**する（差分管理より安全）。

変更点: ①founder を `@id` 参照化し Person ノードを独立・強化、②Book×2追加、③WebPage追加（dateModified担当）、④FAQPage追加（③の可視FAQと**全文一致**）。なお `alternateName: "株式会社ユーダイモニアユニバース"` と founder は**既存ブロックに実装済み**であることを確認済み（引き継いで強化する）。

FAQPageの回答テキストは可視FAQと一字一句同一にする（要約版は同期ミスの温床になるため不採用）。以下、FAQ回答は③の文言をそのまま貼り込むこと（`&amp;` は `&` に戻す）。

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://eudaimoniauniverse.com/#organization",
      "name": "Eudaimonia Universe, Inc.",
      "alternateName": "株式会社ユーダイモニアユニバース",
      "url": "https://eudaimoniauniverse.com/",
      "logo": "https://eudaimoniauniverse.com/img/mark-2026-05-14.png",
      "slogan": "Transforming Conflict into Emergence",
      "description": "人々がより善く幸せで在り続けられる社会を目指し、対立の複雑さを構造から診断して新しい合意・意思決定・関係性をつくるThink & Do Tank。",
      "email": "info@eudaimonialab.org",
      "founder": { "@id": "https://eudaimoniauniverse.com/#founder" },
      "knowsAbout": ["Human OS", "対立学", "Conflictology", "組織変容", "意思決定設計", "事業開発支援", "Ikigai"],
      "contactPoint": {
        "@type": "ContactPoint",
        "email": "info@eudaimonialab.org",
        "contactType": "customer support",
        "availableLanguage": ["Japanese", "English"]
      }
    },
    {
      "@type": "Person",
      "@id": "https://eudaimoniauniverse.com/#founder",
      "name": "Takayuki Mizuno",
      "alternateName": "水野 貴之",
      "jobTitle": "Founder & CEO",
      "worksFor": { "@id": "https://eudaimoniauniverse.com/#organization" },
      "knowsAbout": ["Human OS", "対立学 (Conflictology)", "Ikigai", "組織変容", "意思決定設計"]
    },
    {
      "@type": "Book",
      "@id": "https://eudaimoniauniverse.com/#book-ikigai-keiei",
      "name": "ikigai経営術",
      "alternateName": "ikigai経営術 — 自己実現を企業の原動力に変える方法",
      "author": { "@id": "https://eudaimoniauniverse.com/#founder" },
      "inLanguage": "ja",
      "url": "https://amzn.asia/d/07vj6FGu"
    },
    {
      "@type": "Book",
      "@id": "https://eudaimoniauniverse.com/#book-ikigai-intelligence",
      "name": "ikigai intelligence",
      "alternateName": "ikigai intelligence — Transforming personal purpose into a growth engine for your organization",
      "author": { "@id": "https://eudaimoniauniverse.com/#founder" },
      "inLanguage": "en",
      "url": "https://amzn.asia/d/0hevtcf2"
    },
    {
      "@type": "WebSite",
      "@id": "https://eudaimoniauniverse.com/#website",
      "name": "Eudaimonia Universe",
      "url": "https://eudaimoniauniverse.com/",
      "publisher": { "@id": "https://eudaimoniauniverse.com/#organization" },
      "inLanguage": ["ja", "en"]
    },
    {
      "@type": "WebPage",
      "@id": "https://eudaimoniauniverse.com/#webpage",
      "url": "https://eudaimoniauniverse.com/",
      "name": "Eudaimonia Universe — 社会の対立を、創発へと変換する Think & Do Tank",
      "isPartOf": { "@id": "https://eudaimoniauniverse.com/#website" },
      "about": { "@id": "https://eudaimoniauniverse.com/#organization" },
      "inLanguage": "ja",
      "dateModified": "2026-07-17"
    },
    {
      "@type": "FAQPage",
      "@id": "https://eudaimoniauniverse.com/#faq",
      "mainEntity": [
        { "@type": "Question", "name": "Eudaimonia Universe（ユーダイモニアユニバース）はどのような会社ですか？", "acceptedAnswer": { "@type": "Answer", "text": "（③のfaq-a1と同一文言）" } },
        { "@type": "Question", "name": "Human OSとは何ですか？", "acceptedAnswer": { "@type": "Answer", "text": "（③のfaq-a2と同一文言）" } },
        { "@type": "Question", "name": "対立学（Conflictology）とは何ですか？", "acceptedAnswer": { "@type": "Answer", "text": "（③のfaq-a3と同一文言）" } },
        { "@type": "Question", "name": "組織の対立は、なぜ話し合いだけでは解決しないのですか？", "acceptedAnswer": { "@type": "Answer", "text": "（③のfaq-a4と同一文言）" } },
        { "@type": "Question", "name": "「介入」とは具体的に何をするのですか？", "acceptedAnswer": { "@type": "Answer", "text": "（③のfaq-a5と同一文言）" } },
        { "@type": "Question", "name": "支援はどのようなプロセスで進みますか？", "acceptedAnswer": { "@type": "Answer", "text": "（③のfaq-a6と同一文言）" } },
        { "@type": "Question", "name": "AIはどのように活用されていますか？", "acceptedAnswer": { "@type": "Answer", "text": "（③のfaq-a7と同一文言）" } },
        { "@type": "Question", "name": "どのような相談ができますか？", "acceptedAnswer": { "@type": "Answer", "text": "（③のfaq-a8と同一文言）" } }
      ]
    }
  ]
}
</script>
```

**採否メモ**: `Person.sameAs`（Amazon著者ページ・LinkedIn等）は**URLが実在確認できるまで入れない**（捏造禁止）。ISBN・出版社も確認でき次第追加。`dateModified` はデプロイ当日の日付に設定し、以後は⑤②の運用ルールで更新。

---

## ⑧ 既存コピー微修正案（最小限・トーン維持）

**共通注意**: 各微修正は**静的HTML本文と `translations` の ja 辞書（1334行目〜）の両方**に適用すること。ja辞書にも同じ文言が存在するため（例: hero-desc は1347行目）、片方だけ直すと言語トグルの往復で旧文言に戻る。

### ① hero-desc（696行目）— 対立学に英語名を併記
- 変更前: `対立を4つのタイプに分類して診断する「対立学」です。`
- 変更後: `対立を4つのタイプに分類して診断する「対立学（Conflictology）」です。`
- 理由: 造語の日英対応をHTML本文の初出箇所で確立。英語圏クエリ（"What is Conflictology"）との照合手掛かり。ナビとsection-labelには既に「Conflictology」があり文体上の違和感なし。

### ② humanos-desc2（788行目）— 指示語の解消
- 変更前: `Human OS は、その内的構造を5つの層で統合的に捉えるために独自開発したモデルです。`
- 変更後: `Human OS は、人間の内的構造を5つの層で統合的に捉えるために独自開発したモデルです。`
- 理由: 「その」が前段落に依存しており、単体抽出されると意味が通らない。2文字の変更で単体引用可能な定義文になる。

### ③ conflictology-desc（845行目）— 冒頭に定義文を1文追加
- 変更前（冒頭）: `「とにかく話し合いましょう」で解決しない対立には、理由があります。…`
- 変更後（冒頭に1文追加）: `対立学（Conflictology）は、対立を価値・構造・認知・存在の4タイプに分類して診断する、私たちが独自開発したフレームワークです。「とにかく話し合いましょう」で解決しない対立には、理由があります。…`
- 理由: 対立学セクション本文に現在、対立学そのものの定義文がない（定義はページ下部のAssetsセクション1026行目にのみ存在）。セクション見出し直下に定義を置くのはAI抽出の定石。既存文は一切変更しない。

### ④ About情報テーブル（1136〜1137行目）— 実体情報の補完
- 変更前: `<td>Eudaimonia Universe, Inc.</td>` ／ `<td>TAKAYUKI MIZUNO</td>`
- 変更後: `<td>Eudaimonia Universe, Inc.（株式会社ユーダイモニアユニバース）</td>` ／ `<td>Takayuki Mizuno（水野 貴之）</td>`
- 理由: 日本語法人名が現在**可視HTML本文のどこにも存在せず**（JSON-LDの `alternateName` には実装済み）、「ユーダイモニアユニバースとは」系の日本語クエリで可視テキスト側の実体照合ができない。代表者の漢字表記もPublicationsの「水野 貴之 著」にしかないため、About（組織情報の正規位置）に併記する。

### ⑤ 見出し（変更なしの判断）
「対立は問題ではなく、構造である」「人間は構造である」等の既存見出しはブランドの声として機能しており、直下に定義・回答が揃っていれば質問形に変える必要はない。質問形見出しは新設FAQ（③）に集約する。

---

## ⑨ サイト外施策（効果順）

AIが独自概念を「知識」として持つ条件は、(1) 一貫した定義文が (2) 提唱主体と紐づいて (3) **複数の独立ソース**で反復されること。自社サイト内でいくら反復しても独立ソースにはならない。④の正準表記・一文定義ルールを全施策に適用する。

1. **note（等の外部プラットフォーム）での概念解説連載** — 「対立学とは」「Human OSの5層」「対立の4タイプ」を各1本、正準定義を含めて公開し自社サイトへリンク。クロール頻度・被リンク・独立ソース化を同時に満たす、費用対効果最良の一手。
2. **PR TIMES等のプレスリリース配信** — 書籍・プロジェクト（育業／The Guild／Giver研究）・研究発表など事実ベースのニュースを配信。転載経由で「社名×対立学」の独立した共起ソースが一度に増える。
3. **Amazon著者ページ・書籍ページとの連携強化** — 著者プロフィールに正準定義入りの紹介文を整備し、サイト側から Book / Person スキーマの sameAs で連結（URL確認後）。既刊2冊は最も安価に使える外部アンカー。
4. **第三者メディアへの寄稿・登壇・Podcast出演（組織開発・人事領域）** — 自社発でない媒体に「提唱者＋理論名」が載ることがエンティティ定着の本丸。登壇プロフィール文を正準表記で統一し、イベントページを恒久的な言及ソースとして残す。

**共起ルール**: 「水野貴之が提唱する対立学」「Eudaimonia UniverseのHuman OS」という**主語付きの言及**で書く。育業・The Guild・Giver研究の発信時も必ず親エンティティ（会社名・理論名）と紐づける（プロジェクト単独で言及が散るとエンティティ網が育たない）。

**中期の狙うべきクエリ（参考・優先順）**: 短期は指名型（「対立学 とは」「Human OS とは」「ユーダイモニアユニバース 会社」＝本書のP2で対応）、中期は手法型（「合意形成 フレームワーク」「コンフリクトマネジメント 手法 比較」）、長期は課題型（「部門間 対立 解決」「組織 サイロ化 解消」）。手法型・課題型はシングルページでは面が足りず、ページ増設が前提（⑩で保留扱い）。

---

## ⑩ 実装しない／保留とその理由

| 項目 | 判断 | 理由 |
|---|---|---|
| Speakable スキーマ | 実装しない | 対応環境が限定的なまま（Googleはニュース向けベータ）。優先度なし |
| llms-full.txt | 実装しない | 実質1ページのサイトでは llms.txt と差分がない |
| 学習用AIボット（GPTBot等）のブロック | しない（全許可維持） | 認知拡大目的のコーポレートサイト。学習ブロックは将来モデルでの言及機会も削る |
| noscript への英語埋め込み | 不採用 | 大量の非表示コンテンツは不信シグナル。英語専用URLがなければ hreflang も張れず根本解決にならない |
| プリレンダリングサービス | 不採用 | もともと静的サイト。外部依存を増やすだけで、UA判別配信はクローキング認定リスクもある |
| 両言語をHTML本文に埋めCSS切替 | 不採用（次点） | 1URLに2言語混在でチャンク抽出時の言語判定が不安定、hreflang不可。`/en/` 静的化を採用 |
| Service スキーマ | 見送り | 実績数値・料金等の裏付けフィールドがなく薄いノードになる。サービスページ独立URL化の際に再検討 |
| BreadcrumbList | 見送り | 3ページのフラット構成で階層が存在せず、ノイズにしかならない |
| 既存見出しの質問形化 | しない | ブランドの声として機能中。質問形はFAQに集約（トーン毀損リスクの方が大きい） |
| Wikipedia 作成 | 見送り（条件整備を先行） | 特筆性（独立二次資料）が現状不足。本人・関係者作成はCOI・削除リスク。⑨で第三者言及が蓄積した後の選択肢とし、先に Wikidata への基礎項目登録可否を検討 |
| 課題型クエリ向け専用ページ群（/tairitsugaku 等） | 保留 | シングルページの構造的制約への正攻法だが工数大。P3（/en/）完了後に、FAQ・noteの反応を見て優先順位を再判断 |
| IndexNow | 不要 | ページ数が少なく Bing Webmaster Tools の sitemap 送信で十分 |
| 実績数値・顧客事例の記載 | 記載しない | サイトに存在しない事実は書かない。書く場合は「事例」ではなく「アプローチ解説・想定シナリオ」として（捏造禁止の制約と両立する唯一の書き方） |

---

## 付記: 統合時のファクトチェック結果

- 本書のFAQ・定義文・llms.txt の全記述は index.html の既存コピーに存在する情報のみで構成（実績数値・顧客名・新規の主張なし）。主要な主張の典拠: AIプロダクト開発＝assets-ai-desc（1039行目）、介入の3類型＝approach-s3-desc（919行目）、想定窓口4部門＝contact-lead（1201行目）、「唯一の正解を押しつけない」＝approach-desc（905行目）、5層の英語名＝humanos-B〜R-title（795行目〜）、「自社発の社会実装プロジェクト」＝projects-title（980行目）。
- ドラフト間の矛盾解決: (1) FAQ設置位置はA案（About直後・Newsletter前）を採用、(2) FAQPage JSON-LDは可視テキストと全文一致方式（B案）を採用しA案の要約版方式は不採用、(3) A案④の「JSON-LDにalternateName/founder追記」は既存ブロックに実装済みのため削除し、可視HTML側の補完のみ残した、(4) 行番号はすべて実ファイルで再確認済み（hero-desc 696／humanos-desc2 788／conflictology-desc 845／Aboutテーブル 1136-1137／JSON-LD 34／translations 1334）。