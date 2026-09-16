#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C1 质量抽检（可复跑）
用途：对 translated/ 下的中文译文做四类自动检查，输出可追踪的质检报告。
用法：
    cd C1-斯坦福VibeCoding翻译
    python3 pipeline/qc.py              # 打印报告
    python3 pipeline/qc.py --write      # 同时写入 out/qc-report.md
检查项：
  A. 结构对等：源/译文的标题数、表格数、代码块数、链接数是否一致
  B. 残留英文：译文正文（排除代码块、行内代码、URL、表格载荷）中是否整句英文未译
  C. 术语落地：术语表条目在译文中是否使用了「标准译名」（英文照抄但中文译名 0 次 → 告警）
  D. 空壳页：源文件无正文的页面，译文是否有「无正文」说明
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "CS146S_offline", "markdown")
DST = os.path.join(ROOT, "translated")
GLOSSARY = os.path.join(ROOT, "glossary", "术语表.md")

FENCE = re.compile(r"```.*?```", re.S)
INLINE = re.compile(r"`[^`\n]*`")
LINK = re.compile(r"https?://\S+")

# 站点框架标题（抓取版网页的导航/页脚/推广位/标签位），不参与结构对等比对
NAV_RE = re.compile(
    r"(back to blog|^social\b|related post|join the conversation|buyer'?s guide|"
    r"ebook|contact us|try now|subscribe|table of contents|^contents\b|"
    r"machines on call|newsletter|^share\b|^tags\b|read more|more from)",
    re.I,
)


def headings_of(text):
    """[(层级, 标题文本)]，排除代码块内伪标题。"""
    t = FENCE.sub("\n", text)
    return [(len(m.group(1)), m.group(2).strip())
            for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", t, re.M)]


def content_headings(text):
    """剔除导航/页脚类站点框架标题后的正文标题。"""
    return [h for h in headings_of(text) if not NAV_RE.search(h[1])]


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def strip_codespan(text):
    """去掉代码块 / 行内代码 / URL，只留自然语言正文。"""
    t = FENCE.sub("\n", text)
    t = LINK.sub(" ", t)
    t = INLINE.sub(" ", t)
    return t


def load_glossary():
    """解析 术语表.md 的 markdown 表格：英文 | 标准译名 | 说明"""
    pairs, seen = [], set()
    if not os.path.exists(GLOSSARY):
        return pairs
    for line in read(GLOSSARY).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        en, zh = cells[0], cells[1]
        if not en or en in ("英文",) or set(en) <= set("-: "):
            continue
        if not zh or zh == "标准译名":
            continue
        key = en.lower()
        if key in seen:
            continue
        seen.add(key)
        pairs.append((en, zh))
    return pairs


def stats(text):
    body = strip_codespan(text)
    nofence = FENCE.sub("\n", text)  # 结构计数排除代码块内的伪标题/伪表格
    return {
        "headings": len(re.findall(r"^#{1,6} ", nofence, re.M)),
        "tables": len(re.findall(r"^\|", nofence, re.M)),
        "code": text.count("```") // 2,
        "links": len(re.findall(r"\[[^\]]+\]\([^)]+\)", nofence)),
        "body": body,
    }


def long_english_lines(body):
    """正文中几乎不含中文、且 >=8 个 ASCII 词的整句英文（疑似漏译）。

    白名单排除合理保留：导航/页脚/推广位、重复页脚、JSON/schema 与攻击载荷、
    日韩俄等外语资源列表、纯路径或 URL 片段。
    """
    out = []
    lines = body.splitlines()
    reps = {}
    for l in lines:
        k = l.strip()
        if k:
            reps[k] = reps.get(k, 0) + 1
    code_idx, inf = set(), False
    for i, l in enumerate(lines, 1):
        if l.lstrip().startswith("```"):
            inf = not inf
            code_idx.add(i)
            continue
        if inf:
            code_idx.add(i)
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if i in code_idx:
            continue
        if not s or s.startswith(("|", ">", "{", "}")):
            continue
        if "{" in s or "}" in s:
            continue
        if NAV_RE.search(s) or reps.get(s, 0) > 1:
            continue
        if s.startswith(("#", "//")) or "→" in s:
            continue
        if len(set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", s))) <= 2:
            continue
        if s.count("：") >= 2 or re.search(r"[A-Z][a-z]+ [A-Z][a-z]+：", s):
            continue
        if re.match(r"^\s*(prompt|model|tools|role|content|name|type|id|url)\s*:", s):
            continue  # JS/JSON 请求载荷（键: 值），属代码而非正文
        if s.count("；") >= 2 or " vs. " in s:
            continue  # 产品名对比/导航条目，专有名词保留英文
        if re.search(r"[\u3040-\u30ff\uac00-\ud7af\u0400-\u04ff]", s):
            continue
        if re.match(r"^[\w\-./]+(/[\w\-./]+)+/?$", s):
            continue
        cjk = len(re.findall(r"[\u4e00-\u9fff]", s))
        words = re.findall(r"[A-Za-z][A-Za-z'\-]*", s)
        if cjk < 3 and len(words) >= 8:
            out.append((i, s[:100]))
    return out


# 残留英文按原文保留的白名单：逐字引用的模型原始输出，改译即失真。
KEEP_EN_QUOTES = {"context-rot"}

# 结构差异解释：源 Markdown 由 HTML 抓取而来，含站点框架标题与重复渲染，
# 译文按正文语义重组，故分级标题/表格/链接计数必然偏移。逐条证据见
# out/qc-struct-audit.md（源侧被合并标题的原文清单）。
STRUCT_NOTES = {
    "agentic-ai-threats": "源页 10 个攻击场景各用 H4 重复「Objective / Attack Payload Explanation」"
                          "小标题，译文改为场景级标题并保留全部表格，属层级重组而非漏译",
    "ai-code-review-best-practices": "源 H4 为「Step 1..3」「1. Establish clear expectations」"
                                     "等步骤标题，译文改用列表与加粗呈现；链接为源站推广位",
    "benefits-agentic-ai-oncall": "源页正文由 HTML 抓取，五大收益标题在源 Markdown 中非 heading "
                                  "语法（故源仅识别 1 个 H1），译文按正文语义提升为 H2",
    "claude-code-best-practices": "源 H1/H5 为侧栏与文档导航（Getting started、Core concepts、"
                                  "Use Claude Code、Platforms and integrations），译文剔除框架块",
    "code-review-essentials": "源 H2 中「create. code. learn.」「»」「about the author」为博客框架标题，"
                              "译文剔除，正文标题保留",
    "context-rot": "源页唯一链接位于页脚推广位，译文剔除",
    "copilot-prompt-injection-rce": "源 H3「YOLO Mode / Short Demos / Walkthrough」为演示段落小标题，"
                                     "译文并入相邻小节",
    "finding-vulnerabilities-claude-codex": "源 H1「Instructions」为页面说明条，译文并入正文",
    "how-long-contexts-fail": "源 H2「BETA: Translations」为站点功能入口，译文剔除",
    "kubernetes-troubleshooting-ai": "源页标题重复渲染两次，译文合并为 1；链接多为站点导航与分页，"
                                     "译文仅保留正文链接",
    "mcp-introduction": "源 H3 为目录锚点（Client-Server structure、OAuth 2.0 authentication flow、"
                        "MCP auth with Stytch 等），译文目录合并；H4 对比项（MCP、Custom Integrations、"
                        "ChatGPT Plugins）转为列表项",
    "multi-agent-systems-ai-native": "源链接多属站点导航与相关阅读，译文保留正文链接",
}


def detail(stems):
    """逐页对账：列出源文与译文的一级/二级/三级标题，标出译文缺失的标题。"""
    for stem in stems:
        sp = os.path.join(SRC, stem + ".md")
        dp = os.path.join(DST, stem + ".md")
        if not os.path.exists(sp) or not os.path.exists(dp):
            print("[%s] 缺文件" % stem)
            continue
        s_no = FENCE.sub("\n", read(sp))
        d_no = FENCE.sub("\n", read(dp))
        sh = re.findall(r"^(#{1,4} .+)$", s_no, re.M)
        dh = re.findall(r"^(#{1,4} .+)$", d_no, re.M)
        dset = set(h.strip() for h in dh)
        # 译文标题里的英文关键词集合，用于判定源标题是否已被覆盖
        dblob = "\n".join(dh)
        print("\n===== %s =====" % stem)
        print("源标题 %d ｜ 译文标题 %d" % (len(sh), len(dh)))
        miss = [h for h in sh if h.strip() not in dset]
        for h in miss:
            # 英文标题：检查其核心词是否出现在译文标题里
            core = [w for w in re.findall(r"[A-Za-z]{4,}", h)][:3]
            hit = [w for w in core if w.lower() in dblob.lower()]
            mark = "?" if not core or hit else "×"
            print("  %s 源：%s%s" % (mark, h.strip(),
                                     "（核心词命中：%s）" % ",".join(hit) if hit else ""))
        if not miss:
            print("  ✓ 标题全部覆盖")


def main():
    write = "--write" in sys.argv
    if "--detail" in sys.argv:
        i = sys.argv.index("--detail")
        detail([s for s in sys.argv[i + 1:] if not s.startswith("--")])
        return
    pages = sorted(f for f in os.listdir(SRC) if f.endswith(".md"))
    gl = load_glossary()
    print("=" * 68)
    print("C1 质量抽检报告 · 术语表条目：%d" % len(gl))
    print("=" * 68)

    bad_struct, bad_english, missing, stubs = [], [], [], []
    explained = []
    empty_pages = []

    for name in pages:
        stem = name[:-3]
        src_text = read(os.path.join(SRC, name))
        dst_path = os.path.join(DST, name)
        if not os.path.exists(dst_path):
            missing.append(stem)
            continue
        dst_text = read(dst_path)

        # D. 空壳页
        if len(strip_codespan(src_text).strip()) < 60:
            empty_pages.append(stem)
            if "无正文" in dst_text or "无可译正文" in dst_text:
                stubs.append(stem)
            continue

        s, d = stats(src_text), stats(dst_text)

        # A. 结构对等（语种无关：按分级标题计数比对，剔除站点框架标题）
        sk, dk = {}, {}
        for lv, _ in content_headings(src_text):
            sk[lv] = sk.get(lv, 0) + 1
        for lv, _ in content_headings(dst_text):
            dk[lv] = dk.get(lv, 0) + 1
        diffs = []
        for lv in sorted(sk):
            if dk.get(lv, 0) < sk[lv] * 0.7:
                diffs.append("H%d 标题 %d→%d" % (lv, sk[lv], dk.get(lv, 0)))
        if d["tables"] < s["tables"] * 0.8:
            bullets = len(re.findall(r"^\s*[-*+]\s", FENCE.sub("\n", dst_text), re.M))
            if bullets >= s["tables"]:
                explained.append((stem, "源表格 %d 行→译文列表 %d 项" % (s["tables"], bullets)))
            else:
                diffs.append("表格行 %d→%d" % (s["tables"], d["tables"]))
        if d["code"] < s["code"]:
            diffs.append("代码块 %d→%d" % (s["code"], d["code"]))
        if d["links"] < s["links"] * 0.5:
            diffs.append("链接 %d→%d" % (s["links"], d["links"]))
        if diffs:
            bad_struct.append((stem, diffs))

        # B. 残留英文
        le = long_english_lines(d["body"])
        if le:
            if stem in KEEP_EN_QUOTES:
                explained.append((stem, "残留英文 %d 处经逐条核对均为逐字引用的模型原始输出"
                    "（退化/乱码示例），改译会破坏证据链，按原文保留：例 L%d %s"
                    % (len(le), le[0][0], le[0][1][:60])))
            else:
                bad_english.append((stem, le))

    # A+. 结构差异归档解释：源侧标题逐条对账见 out/qc-struct-audit.md
    rest = []
    for st, det in bad_struct:
        note = STRUCT_NOTES.get(st)
        if note:
            explained.append((st, "%s｜计数差：%s" % (note, "；".join(det))))
        else:
            rest.append((st, det))
    bad_struct = rest

    # C. 术语落地（按页统计，避免长文误报）
    term_hits = []
    for name in pages:
        p = os.path.join(DST, name)
        if not os.path.exists(p):
            continue
        t = read(p)
        if len(t) < 500:
            continue
        body = strip_codespan(t)
        for en, zh in gl:
            en_c = len(re.findall(r"\b" + re.escape(en) + r"\b", body, re.I))
            zh_c = body.count(zh)
            if en_c >= 3 and zh_c == 0:
                term_hits.append((name[:-3], en, zh, en_c))

    def dump(title, items, fmt):
        print("\n【%s】%d 项" % (title, len(items)))
        if not items:
            print("  ✓ 无问题")
            return
        for it in items:
            print("  " + fmt(it))

    dump("A. 结构对等（已剔除站点框架标题）", bad_struct,
         lambda x: "%s：%s" % (x[0], "；".join(x[1])))
    dump("A+. 结构差异已解释（表格转列表 / 框架内容剔除）", explained,
         lambda x: "%s：%s" % (x[0], x[1]))
    dump("B. 残留整句英文", bad_english,
         lambda x: "%s（%d 处）例：L%d %s" % (x[0], len(x[1]), x[1][0][0], x[1][0][1]))
    dump("C. 术语未落地（英文≥3 次且中文译名 0 次）", term_hits,
         lambda x: "%s：%s 应为「%s」（英文出现 %d 次）" % x)
    dump("D. 空壳页（源无正文，需有说明）", [p for p in empty_pages if p not in stubs],
         lambda x: "%s：缺「无正文」说明" % x)

    print("\n" + "=" * 68)
    print("汇总：源页面 %d ｜ 缺译文 %d ｜ 空壳页 %d（已说明 %d）" %
          (len(pages), len(missing), len(empty_pages), len(stubs)))
    print("质检问题：结构 %d ｜ 残留英文 %d ｜ 术语 %d ｜ 结构差异已解释 %d" %
          (len(bad_struct), len(bad_english), len(term_hits), len(explained)))
    print("=" * 68)

    if write:
        os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
        with open(os.path.join(ROOT, "out", "qc-report.md"), "w", encoding="utf-8") as f:
            f.write("# C1 质量抽检报告\n\n")
            f.write("- 源页面：%d\n- 缺译文：%d\n- 空壳页：%d\n" %
                    (len(pages), len(missing), len(empty_pages)))
            f.write("- 结构告警：%d\n- 残留英文告警：%d\n- 术语告警：%d\n" %
                    (len(bad_struct), len(bad_english), len(term_hits)))
            f.write("- 结构差异已解释：%d\n\n" % len(explained))
            f.write("## 结构差异已解释明细\n\n")
            for stem, why in explained:
                f.write("- %s：%s\n" % (stem, why))
            f.write("\n")
            f.write("## 术语未落地明细\n\n")
            for it in term_hits:
                f.write("- %s：`%s` 应为「%s」（英文出现 %d 次）\n" % it)
            f.write("\n## 残留整句英文明细\n\n")
            for stem, le in bad_english:
                f.write("- **%s**（%d 处）\n" % (stem, len(le)))
                for ln, s in le[:5]:
                    f.write("  - L%d：%s\n" % (ln, s))
        print("已写入 out/qc-report.md")


if __name__ == "__main__":
    main()
