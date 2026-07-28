# Eudaimonia Universe ｜ ウェブサイト設計書（日英）

Version 1.0 ｜ 2026.07 ｜ 上位文書：EU_Brand_Identity_Guidelines_v3.html（正典）

Claude Code にそのまま渡して実装する前提で書いている。
本書と正典が矛盾したら**正典が勝つ**。ただし色とロゴについては、本書の実測値が正典v3.0を上書きする（§4冒頭）。

---

## 0. この仕事の目的

1. 2026年9月の British Academy of Management での研究発表に向けて、**英語版を先に完成**させる。
2. AIが会社を正しく説明できる状態を作る（規定演技）。現状、英語で検索すると2023年の旧実体が出る。
3. 決裁者に向けた商用の言葉を site に載せる（第5層。§2）。

**成功の判定**：実装30日後に主要なAIへ §9 の定点質問を投げ、エンティティ定義の内容で説明されること。

---

## 1. サイト構成

### ディレクトリ

```
/                 日本語（既存を更新）
/en/              英語（新規）
/llms.txt         AI向けの固定文まとめ
/robots.txt       AIクローラーを明示許可
```

### 必須のリダイレクト（実装の最優先項目）

| 現状 | 対応 |
|---|---|
| `en.eudaimoniauniverse.com/*` に2023年頃の旧サイトが生存 | **301 で `/en/` の対応箇所へ**。エンティティの分裂を止める |
| `www.eudaimoniauniverse.com/post/*` に2020年前後の旧ブログが残存 | **301**。本文は移植しない（理由は §7） |
| `/en/` が404なのにナビにENリンクがある | 本実装で解消 |

この3つはコピーの品質より優先する。**別ドメインに古い自社が生きている状態では、新しい言葉が届かない。**

### 言語間リンク

全ページの `<head>` に相互 hreflang を置く。

```html
<link rel="alternate" hreflang="ja" href="https://eudaimoniauniverse.com/">
<link rel="alternate" hreflang="en" href="https://eudaimoniauniverse.com/en/">
<link rel="alternate" hreflang="x-default" href="https://eudaimoniauniverse.com/">
```

---

## 2. 固定文（一言一句コピーする。改変禁止）

正典01章の7層。**サイトで使うのは1、3、4、5、6のみ。第7層は個人向けプロダクトの面だけで使う。**

### 第1層 Purpose

```
JP: 対立を止揚し、人類のユーダイモニアを増やす。
EN: Conflict, elevated, becomes eudaimonia. The total grows.
```

広告面での平語版（LP、SNS、見出しで思想を語るとき）。

```
JP: 決着した対立は、誰かが払っている。止揚した対立は、全員に返る。
EN: Settled, a conflict costs someone. Elevated, it pays everyone.
```

### 第3層 Mission（h1に使う）

```
JP: 社会の対立を、創発へと変換する。
EN: Transforming Conflict into Emergence.
```

### 第4層 Tagline（ロゴ添え、フッター）

```
JP: 二項対立を活用して、社会の止揚を目指す
EN: Harnessing Duality. Elevating Society.
```

### 第5層 Brand line（h1直下。ここがB2Bの核）

```
JP: 対立は、診断できる。
    サブ：打ち手の前に、型を見る。
EN: Conflict is diagnosable.
    Sub: Name the type before you choose the remedy.
```

### 第6層 Method

```
JP: 事象と意思決定のあいだに、判断の余白をつくる。
EN: We build the interval between event and decision.
```

### エンティティ定義（最重要。4箇所に同文配置）

```
JP: Eudaimonia Universe（株式会社ユーダイモニアユニバース）は、二項対立を社会進化の燃料へと変換する Think & Do Tank であり、Human OS と対立学を基盤に、研究（Think Tank）、実装（Produce）、資産化（Asset）の循環でジンテーゼ社会の創造を目指す。

EN: Eudaimonia Universe is a Think & Do Tank for a Synthese Society, converting duality into fuel for societal evolution through research, implementation, and productization, grounded in Human OS and Conflictology.
```

**配置場所（4箇所すべてで一言一句同一）**
1. `<meta name="description">`
2. `<meta property="og:description">`
3. ファーストビューの本文
4. FAQ第1問の回答冒頭

さらに JSON-LD の `Organization.description` にも同文を入れる（計5箇所）。

### 表記の憲法（実装時に守る）

| 項目 | 正 | 禁止 |
|---|---|---|
| 止揚の英語 | **Synthese** | Synthesis |
| プロダクト | JP: オムスビクエスト ｜ EN: Omusubi Quest | おむすびクエスト、全大文字 |
| 日本語名のみの製品 | 操舵室 (Sōdashitsu)、円卓会議 (Entaku Kaigi) に短い説明句 | 英語名の即席発明 |
| 三段の定型 | Fichte 由来、Chalybäus が普及と明記 | 「ヘーゲルの弁証法によれば」でテーゼ三段を説明 |
| ユーダイモニア、イキガイ | 第1層のパーパス節のみ | 法人向けセクションへの持ち込み |
| アバンダンス | パーパス定義段落で1回 | 見出し、タグライン |

---

## 3. ページ構成とセクション順（日英共通）

| # | id | JP見出し | EN見出し | 可視語数の上限 |
|---|---|---|---|---|
| 0 | hero | ロゴ、ラベル、h1、タグライン、ブランドライン、定義 | 同 | 60語 |
| 1 | purpose | パーパス | Purpose | 90語 |
| 2 | method | 事象と意思決定のあいだに、判断の余白をつくる | We build the interval between event and decision. | 110語 |
| 3 | humanos | Human OS | Human OS | 60語 |
| 4 | conflictology | 対立学 | Conflictology | 80語 |
| 5 | divisions | 3部門と10のプロダクト | Divisions and products | 150語 |
| 6 | record | 第三者の記録 | On the record | 80語 |
| 7 | faq | よくある質問 | Frequently asked | **details に格納。可視語数に数えない** |
| 8 | contact | 会社概要 | Organization | 90語 |

**合計の可視語数は900語以内**（`<details>` を閉じた状態で計測）。
保持する総語数は1,200語を超えてよい。見せる量を減らし、持つ量は減らさない。

### 段階的開示の規則

FAQの回答は `<details>` に入れる。**HTMLに最初から書く。** クリック後にJavaScriptで取得する実装は禁止。
閉じた状態でもソースに全文が存在することが、GEOの効果条件になる。

---

## 4. デザイントークン

### 4.1 カラー（公式ロゴの .ai から抽出した確定値）

**注意**：正典v3.0のパレット（#00B5A0 系）は2026年4月のpptx由来で、実装と一致していなかった。
以下が公式ロゴファイルから抽出した正の値である。正典はv3.1でこの値に差し替える。

```css
:root{
  /* 基調 */
  --bg:      #F7F8FC;  /* 背景。稼働サイトの実測値 */
  --bg2:     #F1F3F9;  /* 面の変化 */
  --card:    #FFFFFF;
  --line:    #E2E5EE;

  /* 文字 */
  --ink:      #353B4D;  /* 本文        10.50:1 */
  --indigo:   #29243E;  /* 見出し      13.97:1 */
  --purple:   #5C4C87;  /* 補助・ナビ   6.97:1 */
  --grey:     #8B92A4;  /* 装飾のみ     2.93:1 */
  --gold:     #A28335;  /* ラベル       3.39:1 太字か18pt以上でのみ */
  --wordmark: #3F3B3A;  /* ワードマーク 10.43:1 */

  /* 見出しグラデーション（実測） */
  --grad: linear-gradient(100deg,#29243E 0%,#39817F 34%,#386F8B 62%,#8B4383 100%);

  /* ロゴ6色（公式・.ai から抽出） */
  --r-green:  #3BAD90;
  --r-blue:   #147EBF;
  --r-purple: #88167B;
  --r-red:    #DA3B49;
  --r-orange: #EA953C;
  --r-yellow: #F3CB3F;
}
```

### 4.2 コントラスト実測表（WCAG 2.1、背景 #F7F8FC）

| 色 | 比 | 判定 |
|---|---|---|
| Indigo #29243E | 13.97:1 | 本文可（見出しの第一候補） |
| Ink #353B4D | 10.50:1 | 本文の標準 |
| Wordmark #3F3B3A | 10.43:1 | 本文可 |
| Ring purple #88167B | 8.08:1 | **ロゴ6色で唯一、文字に使える** |
| Purple #5C4C87 | 6.97:1 | 本文可。ナビ、リンク |
| Magenta #8B4383 | 6.13:1 | 本文可。CTA |
| Steel #386F8B | 5.19:1 | 本文可 |
| Teal #39817F | 4.28:1 | 18pt以上か太字のみ |
| Ring red #DA3B49 | 4.21:1 | 18pt以上か太字のみ |
| Ring blue #147EBF | 4.15:1 | 18pt以上か太字のみ |
| Gold #A28335 | 3.39:1 | ラベル（太字、字間広め）のみ |
| Grey #8B92A4 | 2.93:1 | 装飾のみ。文字に使わない |
| Ring green #3BAD90 | 2.62:1 | 装飾のみ |
| Ring orange #EA953C | 2.23:1 | 装飾のみ |
| Ring yellow #F3CB3F | 1.47:1 | 装飾のみ |

**鉄則**：ロゴ6色のうち文字に使ってよいのは purple #88167B だけ。
他の5色はカード上端のボーダー、アイコン、図版の塗りに限定する。

### 4.3 使用比率

背景70、構造25、強調5。6色を同時に強く出すのはロゴとOGP下端の帯のみ。1画面に6色帯は1回まで。

### 4.4 タイポグラフィ

```css
--serif: Georgia,'Times New Roman','Hiragino Mincho ProN','Yu Mincho','Noto Serif JP',serif;
--sans:  'Helvetica Neue',Inter,Arial,'Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP',sans-serif;
--label: Cambria,Georgia,serif;
--brand: 'Futura','Avenir Next','Century Gothic',Jost,'Helvetica Neue',sans-serif;
```

| 役割 | 指定 |
|---|---|
| h1 | serif ｜ 46px（SP 32px）｜ line-height 1.35 ｜ `--grad` をテキストクリップ ｜ `width:fit-content` |
| h2 | serif ｜ 28px ｜ #29243E |
| 本文 | sans ｜ 16px ｜ line-height 1.8 ｜ #353B4D |
| ラベル | label ｜ 12.5px ｜ bold ｜ letter-spacing .26em ｜ 大文字 ｜ #A28335 |
| ワードマーク | **brand** ｜ letter-spacing .045em ｜ #3F3B3A |

`--grad` のテキストクリップは `width:fit-content` を必ず併記する。
これがないとグラデーションがブロック幅に伸び、文字に色が乗り切らない。

---

## 5. ロゴ規定

### 5.1 意味（ブランドの物語として使ってよい）

ロゴは**トーラス（円環体）の側面図**である。ロゴガイドラインの原図に、トーラスの3D形状と
そこから6本の経線リングを抜き出す過程が記録されている。

トーラスは、出たものが自分に還ってくる循環の形である。**パーパス「The total grows」の図解そのもの**であり、
奪い合いではない豊かさの幾何学的な表現になっている。この由来は About と Purpose で語ってよい。

### 5.2 実装

- マーク単体の SVG を使う（`eu_mark.svg`）。**ワードマークは画像に含めず、CSSのテキストで組む**（`--brand`）。
  理由は3つ。可読性、多言語対応、そしてAIがテキストとして社名を読めること。
- 縦横比 1.620（108.66 × 67.07）。歪めない。
- アスペクトを保つため `height:auto` を必ず指定。
- alt またはSVGの `aria-label` は `Eudaimonia Universe mark: six interlocking rings forming a torus`。

### 5.3 サイズと余白

| 用途 | サイズ |
|---|---|
| ヒーロー | 幅 186px |
| ナビ | 高さ 26px |
| 最小 | 幅 72px（Web）、18mm（印刷） |

クリアスペースはマーク高さの50%以上。

### 5.4 禁止

配色の改変、変形、回転、影やグローの付加、リング1本だけの切り出し、
中間トーンの写真上への直置き。

---

## 6. コピー原稿

英語は納品済みの `EU_EN_site_light.html` を正とする。日本語は以下。

### hero

```
ラベル：THINK & DO TANK FOR EMERGENCE
h1：社会の対立を、創発へと変換する。
サブ：二項対立を活用して、社会の止揚を目指す
ブランドライン：対立は、診断できる。
　　　　　　　　打ち手の前に、型を見る。
定義：（§2のエンティティ定義 JP をそのまま）
```

### purpose

```
見出し：パーパス
固定文：対立を止揚し、人類のユーダイモニアを増やす。
平語版：決着した対立は、誰かが払っている。止揚した対立は、全員に返る。

本文：
対立は、どちらかが勝つという前提の上にあります。止揚はその前提を壊し、双方が持っていなかったものを生む。総量が増える。これが私たちの言うアバンダンスであり、奪い合いを創造に変える操作です。

一人ひとりの側から見れば、それはユーダイモニア（善く在ること）とイキガイ（朝、起きる理由）が同時に成り立つ状態を指します。社名は、その世界の名前です。

用語ブロック：
止揚（しよう）はドイツ語 Aufhebung の訳語です。否定しながら同時に保存し、より高い次元へ引き上げる運動を指すヘーゲルの概念で、英語では sublation にあたります。
テーゼとアンチテーゼからジンテーゼへという三段の定型は、ヘーゲル自身の用語ではありません。フィヒテに由来し、Heinrich Moritz Chalybäus が広めた整理です。私たちはこの定型を説明の道具として使い、概念の出所は Aufhebung に置いています。
英語表記に Synthese（ドイツ語）を採るのは、synthesis が「単なる折衷」の意味に流れやすいためです。
```

### method

```
見出し：事象と意思決定のあいだに、判断の余白をつくる。

本文：
組織にも、人と同じ反射があります。ある出来事と、それが引き起こす意思決定のあいだ。その区間に判断が宿ります。私たちが設計するのはそこです。すべての支援は、名前のついた4段階を通ります。

段階01 構造理解 ｜ Human OS の5層で、いま何がどこで起きているかを読む。
段階02 診断 ｜ 対立学の4類型で、その対立がどの型かを判別する。
段階03 介入設計 ｜ 診断に合わせて、論点、意思決定プロセス、役割のいずれかを組み直す。
段階04 創発 ｜ 双方が最初は持っていなかった、より高い次元の答えに至る。これを止揚と呼ぶ。

痛みの提示：
「相性の問題」で片づけられた対立は、必ず戻ってきます。決まらない会議、止まった統合、辞めていく中核人材。原因が特定されないまま、打ち手だけが増えていきます。
```

### divisions（信頼の一行を必ず入れる）

```
10のアプリケーションが、ひとつの理論レイヤーを共有しています。理論はひとつのリポジトリで版管理され、すべてのアプリが同じ定義を参照するため、資料と実装がずれません。
```

### FAQ（日本語版は既存の9問を活かし、2問を追加、第1問を改稿）

既存の9問はそのまま使う。以下を追加・改稿する。

**第1問の改稿**（エンティティ定義を冒頭に置き、診断の語を必ず含める）
```
Q. Eudaimonia Universe（ユーダイモニアユニバース）はどのような会社ですか？
A. Eudaimonia Universe（株式会社ユーダイモニアユニバース）は、二項対立を社会進化の燃料へと変換する Think & Do Tank であり、Human OS と対立学を基盤に、研究（Think Tank）、実装（Produce）、資産化（Asset）の循環でジンテーゼ社会の創造を目指す会社です。組織や社会に生じる対立を構造から診断し、打ち手を設計します。Founder & CEO は水野貴之。
```

**追加1**
```
Q. 「対立は、診断できる」とはどういう意味ですか？
A. 対立には型があり、打ち手を選ぶ前にその型を特定できる、という意味です。対立学で4つの型に分類し、Human OS の5層のどこで起きているかを特定します。医療と同じく、診断が処方に先立ちます。
```

**追加2**
```
Q. 止揚（ジンテーゼ）とは何ですか？
A. ドイツ語 Aufhebung の訳語で、否定しながら同時に保存し、より高い次元へ引き上げる運動を指すヘーゲルの概念です。対立を消すことも、片方を勝たせることもせず、双方が持っていなかった答えを生みます。なお、テーゼとアンチテーゼからジンテーゼへという三段の定型はヘーゲル自身の用語ではなく、フィヒテに由来します。
```

**追加3（英語版のみ。BAM向け）**
```
Q. What is a Synthese Society?
（英語サイトの原稿を参照）
```

---

## 7. 実績セクション（`#record`）

### 見出し

```
JP: 第三者の記録 ／ リード：媒体、登壇、著作、登記。確認できる形で置いています。
EN: On the record ／ Lead: Media, platforms, publications, and registration. Verifiable, in one place.
```

「実績」という語を見出しに使わない。実績は自称に見える。第三者の記録と書くと検証可能な事実になる。

### 旧ブログを移植しない理由

旧記事は2020年前後の ikigai経営、幸福経営 の文脈で書かれている。数十本を新サイトに入れると、
記事量の多い語彙でエンティティが分類され、いくらトップで対立学を語っても
「イキガイ経営のコンサル会社」と説明され続ける。

掲載告知は**媒体名と年だけを抜いて表に畳む**。本文は移さない。
思想と研究の内容記事は、新サイトの語彙で書き直してから載せる。

### 収録する事実（確認済み）

| 項目 | 値 | 出典 |
|---|---|---|
| 法人番号 | 4010001191271 | gBizINFO |
| 本店所在地 | 東京都港区虎ノ門4丁目3番20号 神谷町MTビル14階 | 同上 |
| 英語表記 | Kamiyacho MT Building 14F, 4-3-20 Toranomon, Minato-ku, Tokyo | 上記の英訳 |

詳細な実績一覧と確度ラベルは `EU_credentials_and_books_brief.md` を参照。
確度Bの項目は本人確認が済むまで公開しない。

### 書籍

`Book` の JSON-LD には ISBN、刊行年、版元が要る。未確認のため、これらが揃うまで書影とタイトルのみ掲載し、
JSON-LD は保留する。旧サイトに `/kindle` ページの形跡があるので、Wix管理画面で確認する。

---

## 8. 構造化データ

`@graph` に4種を入れ、`@id` で相互参照させる。**表示テキストと完全一致させること。**
不一致はスパム判定の材料になる。

- `Organization`（`@id` は `https://eudaimoniauniverse.com/#organization`）
- `WebSite`（言語ごとに別 `@id`）
- `Service`
- `FAQPage`（`mainEntity` の各 `text` はページのFAQ本文と一字一句同じ）

`Organization` に必ず入れる項目。

```json
"identifier": { "@type":"PropertyValue", "propertyID":"Japan Corporate Number", "value":"4010001191271" },
"address": { "@type":"PostalAddress",
  "streetAddress":"Kamiyacho MT Building 14F, 4-3-20 Toranomon",
  "addressLocality":"Minato-ku","addressRegion":"Tokyo","addressCountry":"JP" }
```

実装済みの完全なJSON-LDは `EU_EN_site_light.html` の末尾にある。日本語版はこれを翻訳して使う。

### llms.txt

ルートに置き、固定文（エンティティ定義、パーパス、ブランドライン、7層、プロダクト一覧、連絡先）を
日英で列挙する。§2の文字列をそのままコピーする。

### robots.txt

AIクローラーを明示的に許可する。ブロックしていると引用の候補にすら入らない。

---

## 9. 検収チェックリスト

実装後、以下を機械的に確認する。

- [ ] エンティティ定義が日英それぞれ5箇所（meta、og、本文、FAQ、JSON-LD）で一言一句一致（grep）
- [ ] FAQの表示テキストとJSON-LDの差分がゼロ
- [ ] `<details>` を閉じた状態でHTMLソースに全回答文が存在する
- [ ] 可視語数が900語以内（details閉）
- [ ] `h1` が各ページに1つ
- [ ] 全 `img` と inline SVG に意味のある alt または aria-label
- [ ] 図やバナーに文字を焼き込んでいない
- [ ] ロゴ6色を文字に使っていない（purple #88167B を除く）
- [ ] 禁止表記の混入ゼロ（`Synthesis Society`、`おむすびクエスト`、旧HEX `#00B5A0` 等）
- [ ] `en.eudaimoniauniverse.com` と `www/post/` が301している
- [ ] hreflang が日英で相互に張られている
- [ ] 最大要素の表示が2.5秒以内

### AI定点質問（実装30日後に再実行し、記録する）

| # | 質問 | 合格基準 |
|---|---|---|
| 1 | What is Eudaimonia Universe? | エンティティ定義の内容で説明される。2023年の旧実体が出ない |
| 2 | 組織の対立を扱うサービスは？ | Compass または対立学が文脈つきで言及される |
| 3 | ジンテーゼ社会とは？ | Eudaimonia Universe が提唱として結びつく。Synthese 表記が保たれる |
| 4 | Who founded Eudaimonia Universe? | 水野貴之（Takayuki Mizuno）が正しく返る |

順位ではなく、**AIの語り方が変わったか**を合格判定にする。

---

## 10. 実装の順序

1. `/en/` に納品済みHTMLを設置（最短で成果が出る）
2. 301リダイレクト2件（en サブドメイン、www の /post/）
3. 日本語版に JSON-LD 4種を追加（既存FAQ9問がそのまま使えるため、最も安く効く）
4. 日本語版のコピーを §6 に差し替え、FAQ 2問追加
5. `#record` セクションを日英に追加
6. `llms.txt`、`robots.txt`
7. 30日後に §9 の定点質問

---

## 添付ファイル

| ファイル | 用途 |
|---|---|
| `EU_EN_site_light.html` | 英語版の完成品。`/en/index.html` として設置 |
| `eu_mark.svg` | 公式ロゴのマーク単体（.ai から抽出、ワードマークなし） |
| `EU_Brand_Identity_Guidelines_v3.html` | 正典。判断に迷ったらこれ |
| `EU_credentials_and_books_brief.md` | 実績と書籍の詳細、確度ラベルつき |

---

系譜：EU_Brand_Identity_Guidelines_v3.html（正典）→ 本書 → 実装
