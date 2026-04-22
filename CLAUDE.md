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
- ホスティング: GitHub Pages（予定）

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

## 注意事項

- CSS/JS は index.html にインラインで含まれている。将来的にファイル分離を検討
- 画像追加時は `assets/` ディレクトリに配置
