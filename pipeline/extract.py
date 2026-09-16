#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 src/CS146S_offline/pages/*.html 抽取为 Markdown（仅用标准库，可复跑）。

背景：原始镜像里部分页面的 Markdown 转换失败（HTML 正文完整，.md 却只有 0~426 字节）。
本脚本用 html.parser 重新抽取这些页面，保留标题层级、列表、代码块、链接与段落边界。

用法:
    python3 extract.py                # 只重抽「已知转换失败」的页面
    python3 extract.py --all          # 重抽全部页面
    python3 extract.py a.html b.html  # 重抽指定页面
"""
import argparse
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGES_DIR = os.path.join(ROOT, "src", "CS146S_offline", "pages")
OUT_DIR = os.path.join(ROOT, "src", "CS146S_offline", "markdown")

SKIP_TAGS = {"script", "style", "noscript", "svg", "head", "nav", "footer",
             "form", "iframe", "template", "button", "select", "option"}
BLOCK_TAGS = {"p", "div", "section", "article", "tr", "table", "ul", "ol",
              "dl", "dd", "dt", "figure", "figcaption", "main", "body", "aside"}

# 已知转换失败的页面（HTML 有正文、Markdown 近乎为空）
BROKEN = [
    "benefits-agentic-ai-oncall.html",
    "kubernetes-troubleshooting-ai.html",
    "multi-agent-systems-ai-native.html",
    "prompt-engineering-guide.html",
    "good-context-good-code.html",
    "how-warp-uses-warp.html",
]

NOISE = re.compile(r"^(skip to .*|toggle navigation|menu|search|sign in|sign up|"
                   r"cookie.*|accept all|subscribe|share this|table of contents)$", re.I)


class MarkdownExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0
        self.block = None
        self.buf = []
        self.in_pre = False
        self.link_href = None
        self.link_text = None
        self.title = None
        self.in_title = False

    def _flush(self):
        text = "".join(self.buf)
        self.buf = []
        block = self.block
        self.block = None
        if self.in_pre:
            if text.strip():
                self.parts.append(text.rstrip("\n") + "\n")
            return
        text = re.sub(r"[ \t\r\f\v\u00a0]+", " ", text)
        text = re.sub(r"\n+", " ", text).strip()
        if not text or NOISE.match(text):
            return
        if block and block.startswith("#"):
            self.parts.append(block + " " + text + "\n")
        elif block == "-":
            self.parts.append("- " + text + "\n")
        elif block == ">":
            self.parts.append("> " + text + "\n")
        else:
            self.parts.append(text + "\n")

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in SKIP_TAGS:
            self.skip += 1
            return
        if tag == "title":
            self.in_title = True
            return
        if self.skip:
            return
        if tag == "pre":
            self._flush()
            self.parts.append("\n```\n")
            self.in_pre = True
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush()
            self.block = "#" * int(tag[1])
            return
        if tag == "li":
            self._flush()
            self.block = "-"
            return
        if tag == "blockquote":
            self._flush()
            self.block = ">"
            return
        if tag == "a":
            self.link_href = (attrs.get("href") or "").strip()
            self.link_text = []
            return
        if tag == "hr":
            self._flush()
            self.parts.append("\n---\n")
            return
        if tag in BLOCK_TAGS or tag == "br":
            self._flush()

    def handle_startendtag(self, tag, attrs):
        if self.skip:
            return
        if tag == "br":
            self._flush()
        elif tag == "hr":
            self._flush()
            self.parts.append("\n---\n")

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            if self.skip:
                self.skip -= 1
            return
        if tag == "title":
            self.in_title = False
            return
        if self.skip:
            return
        if tag == "pre":
            self._flush()
            self.in_pre = False
            self.parts.append("```\n")
            return
        if tag == "a":
            if self.link_text is not None:
                text = re.sub(r"\s+", " ", "".join(self.link_text)).strip()
                href = self.link_href or ""
                self.link_text = None
                self.link_href = None
                if text:
                    self.buf.append("[%s](%s)" % (text, href) if href else text)
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote") \
                or tag in BLOCK_TAGS:
            self._flush()

    def handle_data(self, data):
        if self.in_title:
            self.title = (self.title or "") + data
            return
        if self.skip:
            return
        if self.link_text is not None:
            self.link_text.append(data)
        else:
            self.buf.append(data)

    def result(self):
        self._flush()
        text = "\n".join(self.parts)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def extract_one(name):
    src = os.path.join(PAGES_DIR, name)
    if not os.path.isfile(src):
        return None, "HTML 不存在"
    raw = open(src, encoding="utf-8", errors="ignore").read()
    if not raw.strip():
        return None, "HTML 为空（0 字节），无可抽取内容"
    p = MarkdownExtractor()
    try:
        p.feed(raw)
        p.close()
    except Exception as exc:  # noqa: BLE001
        return None, "解析失败: %s" % exc
    md = p.result()
    stem = os.path.splitext(name)[0]
    out = os.path.join(OUT_DIR, stem + ".md")
    old = os.path.getsize(out) if os.path.exists(out) else 0
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(md)
    return (old, len(md.encode("utf-8")), out), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="*", help="指定 html 文件名")
    ap.add_argument("--all", action="store_true", help="抽取全部页面")
    args = ap.parse_args()

    if args.all:
        targets = sorted(f for f in os.listdir(PAGES_DIR) if f.endswith(".html"))
    elif args.pages:
        targets = args.pages
    else:
        targets = BROKEN

    ok = 0
    for name in targets:
        info, err = extract_one(name)
        if err:
            print("SKIP  %-46s %s" % (name, err))
            continue
        old, new, out = info
        print("OK    %-46s %7d -> %7d bytes" % (name, old, new))
        ok += 1
    print("\n完成：%d/%d 页。" % (ok, len(targets)))


if __name__ == "__main__":
    main()
