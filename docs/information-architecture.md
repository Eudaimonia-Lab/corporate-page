# 情報設計（2026-07 リニューアル）

方針: 企業課題 → 提供価値 → サービス → 独自研究 → 方法論 → 哲学 の順で提示する。
哲学・理論は削除せず、後段と専用ページへ移す。ポジションは「Human Science for Organizational Transformation（人間科学に基づく組織変革）」。

## サイトマップ（フェーズ1で実装）

```
/                       JAトップ
/services/              私たちの支援（6領域を1ハブに集約。#transformation #leadership #engagement #conflict #value #innovation）
/research/              独自研究ハブ（概要・研究方法・研究とデータの倫理を含む）
/research/human-os/
/research/conflictology/
/research/source-108/
/research/ikigai-management/
/research/crv/
/products/              プロダクト（対象者別グルーピング。トップから移設）
/about/                 私たちについて（定義・歩み・Think/Transform/Scale・創業者・会社概要）
/about/philosophy/      哲学（パーパス・止揚・Aufhebung・Synthese・トーラスの由来。トップから移設）
/contact/               お問い合わせ（Netlifyフォーム＋種別選択）
/contact/thanks.html    送信完了（noindex）
/privacy.html /terms.html  既存を維持
/en/...                 上記すべての英語版（同構成）
```

## フェーズ1で作らないもの（理由つき）

- `/impact/`（導入事例）: 公開承認済みの事例・クライアント名・数値が現時点でゼロ。捏造禁止原則により見送り。素材が揃い次第、最優先で追加。
- `/insights/`: 著者・日付・独自視点を備えた記事が未執筆。汎用記事の量産はGEO/E-E-A-T上むしろ有害なため見送り。
- サービス6領域の個別URL: まずハブ1ページに完全な内容で集約。検索需要と商談動線が確認できた領域から個別URL化。
- `/about/team/`: 公開承認済みのプロフィールが創業者のみ。About内に創業者プロフィールを置き、専用ページは人数が揃ってから。

## トップページのセクション順（日英共通）

1. Hero(eyebrow/h1/lead/CTA×2) 2. Identity strip(研究→実装→テクノロジー＋エンティティ定義) 3. 組織課題 4. 提供価値4領域 5. 独自研究5フレームワーク(id=humanos/conflictology を旧アンカー互換で維持) 6. How we work 5段階 7. 課題から探す(11項目→servicesアンカー) 8. Think/Transform/Scale(id=divisions) 9. Purpose(哲学へのリンク) 10. 最終CTA(ダークセクション) 11. FAQ(6問) 12. Footer

## FAQの再配置（削除せず移設）

- トップ(6問): 会社定義（新）／支援内容／Human OS／対立学／AI活用／問い合わせ方法
- /research/conflictology/(4問): 診断できるとは／なぜ話し合いだけでは解決しないか／介入とは／プロセス
- /about/philosophy/(2問): 止揚とは／Synthese Society とは
- 各ページの FAQPage JSON-LD は可視テキストと全文一致（従来規律を維持）

## ナビゲーション

ヘッダー: 私たちの支援 / 独自研究 / プロダクト / 私たちについて ＋ CTA「組織課題を相談する」＋ JA|EN
（Impact・Insights はページ新設時にナビへ追加する）
フッター: 支援・研究・会社・法務の4列＋エンティティ一行＋言語切替

## エンティティ定義（新・正準文字列）

3箇所（トップ本文 p.def / FAQ第1問回答冒頭 / JSON-LD Organization.description）で一言一句同一。メタ description は検索意図向けの別文（§seo-geo-strategy.md）。

JA: ユーダイモニアユニバース（株式会社ユーダイモニアユニバース）は、人間科学の研究と組織変革を行う、日本発の Think & Do Tank です。価値観、感情、認知、意味、関係性に関する独自研究を、組織で活用できるフレームワーク、診断、テクノロジーへと転換し、人と事業がともに持続的に成長する経営を支援します。

EN: Eudaimonia Universe is a human science research and organizational transformation company based in Japan. We turn original research on values, emotions, cognition, meaning, and relationships into practical frameworks, diagnostics, and technologies that help organizations strengthen culture, leadership, decision-making, and meaningful work.

## 用語の正準表記（継続）

対立学=Conflictology／Human OS（半角・「モデル」を付けない）／止揚の英語は Synthese（Synthesis 禁止）／Omusubi Quest（おむすび表記・全大文字禁止）／操舵室 (Sōdashitsu)・円卓会議 (Entaku Kaigi)
