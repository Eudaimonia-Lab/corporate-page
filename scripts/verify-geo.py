#!/usr/bin/env python3
"""EU_website_spec.md §9 の検収チェックリストを機械的に回す。

    python3 scripts/verify-geo.py            # ローカルファイルを検査
    python3 scripts/verify-geo.py --live     # ライブ URL を取得して同じ検査

FAQ の可視テキストと FAQPage JSON-LD の一致、エンティティ定義の5箇所一致、
hreflang の相互参照、禁止表記、ロゴ6色の文字利用などを見る。
"""
import argparse
import html
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = {
    "ja": {
        "file": ROOT / "index.html",
        "live": "https://eudaimoniauniverse.com/",
        "definition": "Eudaimonia Universe（株式会社ユーダイモニアユニバース）は、二項対立を社会進化の燃料へと変換する Think & Do Tank であり、Human OS と対立学を基盤に、研究（Think Tank）、実装（Produce）、資産化（Asset）の循環でジンテーゼ社会の創造を目指す。",
        "lang": "ja",
        "alt": "https://eudaimoniauniverse.com/en/",
    },
    "en": {
        "file": ROOT / "en" / "index.html",
        "live": "https://eudaimoniauniverse.com/en/",
        "definition": "Eudaimonia Universe is a Think & Do Tank for a Synthese Society, converting duality into fuel for societal evolution through research, implementation, and productization, grounded in Human OS and Conflictology.",
        "lang": "en",
        "alt": "https://eudaimoniauniverse.com/",
    },
}

BANNED = ["Synthesis Society", "おむすびクエスト", "#00B5A0", "OMUSUBI QUEST"]
# ロゴ6色のうち文字に使ってよいのは purple #88167B だけ (spec §4.2)
DECOR_ONLY = ["#3BAD90", "#147EBF", "#DA3B49", "#EA953C", "#F3CB3F"]

failures: list[str] = []
notes: list[str] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        failures.append(f"{label}{(' — ' + detail) if detail else ''}")


class VisibleText(HTMLParser):
    """<script>/<style> と、details 内の回答本文 (.a) を除いた可視テキスト。"""

    def __init__(self) -> None:
        super().__init__()
        self.skip_depth = 0
        self.answer_depth = 0
        self.depth_stack: list[bool] = []
        self.out: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip_depth += 1
        is_answer = tag == "div" and a.get("class") == "a"
        if is_answer:
            self.answer_depth += 1
        self.depth_stack.append(is_answer)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip_depth:
            self.skip_depth -= 1
        while self.depth_stack:
            was_answer = self.depth_stack.pop()
            if was_answer:
                self.answer_depth -= 1
                break
            break

    def handle_data(self, data):
        if self.skip_depth == 0 and self.answer_depth == 0:
            self.out.append(data)

    def text(self) -> str:
        return " ".join(" ".join(self.out).split())


def strip_tags(fragment: str) -> str:
    txt = re.sub(r"<[^>]+>", "", fragment)
    return " ".join(html.unescape(txt).split())


def count_words(text: str) -> tuple[int, int]:
    cjk = len(re.findall(r"[぀-ゟ゠-ヿ一-鿿]", text))
    latin = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'&./-]*", text))
    return latin, cjk


def ld_graph(src: str):
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
    if len(blocks) != 1:
        return None, f"ld+json ブロックが {len(blocks)} 個"
    try:
        return json.loads(blocks[0]), None
    except json.JSONDecodeError as exc:
        return None, f"JSON パース失敗: {exc}"


def verify(key: str, src: str) -> None:
    cfg = PAGES[key]
    print(f"\n=== {key.upper()} ({cfg['live']}) ===")

    # --- JSON-LD ---
    data, err = ld_graph(src)
    check(data is not None, "JSON-LD が単一ブロックで valid", err or "")
    graph = data.get("@graph", []) if data else []
    types = [n.get("@type") for n in graph]
    for required in ("Organization", "WebSite", "Service", "FAQPage"):
        check(required in types, f"JSON-LD に {required}")
    org = next((n for n in graph if n.get("@type") == "Organization"), {})
    check(
        org.get("identifier", {}).get("value") == "4010001191271",
        "Organization.identifier = 法人番号 4010001191271",
    )
    check("address" in org, "Organization.address あり")

    # --- FAQ: 可視テキストと JSON-LD の一致 ---
    pairs = re.findall(
        r"<details><summary>(.*?)</summary>\s*<div class=\"a\">(.*?)</div></details>", src, re.S
    )
    faq_node = next((n for n in graph if n.get("@type") == "FAQPage"), {})
    ld_qa = [
        (q.get("name", ""), q.get("acceptedAnswer", {}).get("text", ""))
        for q in faq_node.get("mainEntity", [])
    ]
    check(len(pairs) > 0, "可視 FAQ が <details> で存在", f"{len(pairs)} 問")
    check(
        len(pairs) == len(ld_qa),
        "可視 FAQ と FAQPage の件数一致",
        f"可視 {len(pairs)} / LD {len(ld_qa)}",
    )
    mismatch = []
    for i, ((vq, va), (lq, la)) in enumerate(zip(pairs, ld_qa), 1):
        if strip_tags(vq) != lq:
            mismatch.append(f"Q{i} 質問文")
        if strip_tags(va) != la:
            mismatch.append(f"Q{i} 回答文")
    check(not mismatch, "FAQ 可視テキスト = JSON-LD 全文一致", ", ".join(mismatch))

    # --- エンティティ定義 5箇所 ---
    definition = cfg["definition"]
    esc = definition.replace("&", "&amp;")
    spots = {
        "meta description": f'<meta name="description" content="{esc}">' in src,
        "og:description": f'<meta property="og:description" content="{esc}">' in src,
        "ファーストビュー本文": f'<p class="def">{esc}</p>' in src,
        "FAQ 第1問の冒頭": bool(ld_qa)
        and ld_qa[0][1].startswith(definition.rstrip("。").rstrip(".")),
        "JSON-LD Organization.description": org.get("description") == definition,
    }
    for name, ok in spots.items():
        check(ok, f"エンティティ定義 一言一句一致: {name}")

    # --- hreflang 相互参照 ---
    for hl, href in (("ja", "https://eudaimoniauniverse.com/"), ("en", "https://eudaimoniauniverse.com/en/"), ("x-default", "https://eudaimoniauniverse.com/")):
        check(
            f'hreflang="{hl}" href="{href}"' in src,
            f"hreflang {hl}",
        )
    check(f'<link rel="canonical" href="{cfg["live"]}">' in src, "canonical 自己参照")

    # --- h1 / 代替テキスト / 禁止表記 / ロゴ6色 ---
    check(len(re.findall(r"<h1", src)) == 1, "h1 はページに1つ")
    imgs = re.findall(r"<img\b[^>]*>", src)
    check(all("alt=" in t for t in imgs), "全 img に alt", f"img {len(imgs)} 件")
    svgs = re.findall(r"<svg\b[^>]*>", src)
    check(all("aria-label=" in t for t in svgs), "全 inline SVG に aria-label", f"svg {len(svgs)} 件")
    hit = [b for b in BANNED if b in src]
    check(not hit, "禁止表記の混入ゼロ", ", ".join(hit))
    text_colored = [c for c in DECOR_ONLY if re.search(r"color:\s*" + c, src, re.I)]
    check(not text_colored, "ロゴ6色を文字色に使っていない (purple #88167B を除く)", ", ".join(text_colored))

    # --- 可視語数 (details 閉じ) ---
    vt = VisibleText()
    vt.feed(src)
    latin, cjk = count_words(vt.text())
    if cfg["lang"] == "en":
        check(latin <= 900, "可視語数 900 語以内 (details 閉)", f"{latin} 語")
    else:
        notes.append(f"JA 可視量 (details 閉): 英数 {latin} 語 / 和文 {cjk} 字")
        print(f"  INFO  JA 可視量 (details 閉): 英数 {latin} 語 / 和文 {cjk} 字")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="ライブ URL を取得して検査")
    args = ap.parse_args()

    for key, cfg in PAGES.items():
        if args.live:
            req = urllib.request.Request(cfg["live"], headers={"User-Agent": "verify-geo"})
            src = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
        else:
            src = cfg["file"].read_text(encoding="utf-8")
        verify(key, src)

    print("\n" + ("=" * 60))
    if failures:
        print(f"FAILED: {len(failures)} 件")
        for f in failures:
            print("  - " + f)
        return 1
    print("すべて PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
