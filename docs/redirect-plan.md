# リダイレクト計画（2026-08 リニューアル）

## 結論: 新規リダイレクトは不要

`docs/content-migration-map.md` の分析結果を踏襲する。旧サイトのインデックス済みURLは以下の4つのみで、いずれもリニューアル後も**同一URLのまま**内容だけが更新される。

- `/`(内容刷新、URLは不変)
- `/en/`(同上)
- `/terms.html`(据え置き。旧デザインのまま=既知負債)
- `/privacy.html`(同上)

新規に追加した12ページ(`/services/` `/research/` `/research/human-os/` 等、日英計24〜26 URL)は、旧サイトに存在しなかった**まったく新しいURL**であり、リダイレクト元を持たない。

## 旧アンカー深リンクの互換性

旧トップページはアンカーリンク(`#humanos` `#conflictology` `#divisions` `#faq` `#contact` 等)で内部セクションを参照していた。新トップページでも同名の `id` をセクションに残しており(`id="humanos"` は Human OS カード、`id="conflictology"` は対立学カード等)、外部から `/#humanos` のようにブックマークされていた場合も引き続き該当セクションへスクロールする。恒久的な行き先は専用ページ(`/research/human-os/` 等)であり、トップのアンカーは互換性維持の役割に留める。

## 既存 `_redirects` の扱い

現状維持。変更なし。

```
/post/*        /        301   (旧CMS実体の名残)
en.eudaimoniauniverse.com/*   https://eudaimoniauniverse.com/en/:splat   301
```

2つ目のルールは `en.` サブドメインのDNSがNetlifyへ未切替のため現状発火していない(`CLAUDE.md` 記載の既知負債)。DNS切替は本リニューアルのスコープ外。

## 今後リダイレクトが必要になるケース

- `/services/` を将来6領域の個別URL(`/services/organizational-transformation/` 等)へ分割する場合、アンカー(`/services/#transformation`)から新URLへの301が必要になる。現時点(Phase 1)ではハブ1ページのみのため不要。
- `/about/` を将来 `/about/team/` 等へ分割する場合も同様。
