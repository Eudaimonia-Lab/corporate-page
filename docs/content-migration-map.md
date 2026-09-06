# コンテンツ移設マップ（旧1ページ構成 → 新構成）

凡例: keep=そのまま維持 / rewrite=新ポジションで書き直し / move=移設 / merge=統合。削除は0件（すべて行き先あり）。

| 旧位置（/ と /en/ のアンカー） | 旧見出し | 処置 | 新しい行き先 | 検証 |
|---|---|---|---|---|
| hero | 社会の対立を、創発へと変換する。/ Transforming Conflict into Emergence. | rewrite | トップhero（新h1「人間の内面を、組織変革の技術へ。」）。旧ミッション文は /about/philosophy/ に move | 新旧両文がサイト内に存在すること |
| hero .claim | 対立は、診断できる。 | move | /research/conflictology/（ブランドラインとして） | conflictologyページに存在 |
| hero .def | 旧エンティティ定義 | rewrite | 新エンティティ定義（3箇所一致）。旧定義文は廃止（新定義が正） | verify-geo.py |
| #purpose 固定文 | 対立を止揚し、人類のユーダイモニアを増やす。＋平語版 | move | /about/philosophy/ ＋トップ Purpose セクションに要約 | philosophy に全文 |
| #purpose 用語ブロック | 止揚・Aufhebung・Fichte・Chalybäus・Synthese | move | /about/philosophy/（全文維持） | 同上 |
| #method | 事象と意思決定のあいだに〜 4段階 | move+merge | /services/（支援プロセスとして詳細化）＋ /research/conflictology/ に4段階を維持 | services に5段階、conflictology に4段階 |
| #humanos | Human OS 5層 | move+expand | /research/human-os/（専用ページ化）。トップは要約カード（id=humanos 維持） | 専用ページ存在 |
| #conflictology | 対立学 4類型 | move+expand | /research/conflictology/（専用ページ化）。トップは要約カード（id=conflictology 維持） | 同上 |
| #divisions 3部門 | Think Tank / Produce / Asset | rewrite | トップ Think/Transform/Scale（id=divisions 維持）＋ /about/ に公式部門名の対応注記 | about に注記 |
| #divisions 10プロダクト表 | ポートフォリオ | move | /products/（対象者別グルーピングに再編。全10件・状況ラベル維持） | 10件全掲載 |
| 自社発プロジェクト注記 | 育業・The Guild・Giver研究 | move | /about/ | about に存在 |
| #faq 10問 | よくあるご質問 | move+split | トップ6問（第1問は新定義で改稿）／conflictology 4問／philosophy 2問。JSON-LD同期 | verify-geo.py FAQ同期 |
| #contact 会社概要 | 第三者の記録 | move | /about/（会社概要表）＋ /contact/（問い合わせ動線） | about に法人番号・所在地 |
| 著書2冊 | ikigai経営術 / ikigai intelligence | move | /about/（創業者プロフィール）＋ /research/ikigai-management/（関連文献） | 両ページにリンク |
| footer | タグライン | rewrite | 新フッター（エンティティ一行）。旧タグラインは philosophy に維持 | — |
| terms.html / privacy.html | 法務 | keep | 据え置き（旧デザインのまま。負債として記録） | リンク切れなし |
| llms.txt | AI向け固定文 | rewrite | 新定義・新ページ一覧で全面更新 | verify |
| sitemap.xml | 4 URL | rewrite | 全ページ＋hreflang対 | verify |

## リダイレクト要否

旧URLは `/`・`/en/`・`/terms.html`・`/privacy.html` のみで、すべて同一URLのまま内容更新。**新規リダイレクト不要**。
旧アンカー深リンク（/#humanos 等）はトップに同名 id を残して互換維持。既存 `_redirects`（/post/*、en.サブドメイン）は据え置き。
