#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C1 · CS146S 课程资料翻译流水线（可复跑、确定性）

子命令：
  python3 pipeline.py extract     从源 zip 抽取 31 个 HTML 页面 → 干净 Markdown（可翻译文本）
  python3 pipeline.py coverage    统计翻译覆盖度（源页数/词数 vs translated/ 完成情况）
  python3 pipeline.py glossary    校验 translated/ 中术语是否遵循 glossary/术语表.md

目录约定（相对本仓库根）：
  src/CS146S_offline/          源材料（解压后的 zip）
  src/CS146S_offline/markdown/  extract 生成的干净 Markdown
  glossary/术语表.md            术语表（译文一致性锚点）
  translated/                  翻译后的 Markdown（每页一个 .md，文件名与源 stem 一致）
"""
import os, re, sys, html, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIP_FILE = "/Users/xiaowo/Desktop/我的挑战/C1 课程资料获取与翻译/materials/CS146S_offline.zip"
MD_DIR = ROOT / "src" / "CS146S_offline" / "markdown"
TRANS_DIR = ROOT / "translated"
GLOSSARY = ROOT / "glossary" / "术语表.md"


def read_zip():
    return zipfile.ZipFile(ZIP_FILE)


def pages(z):
    return sorted(n for n in z.namelist() if n.endswith('.html') and '/pages/' in n)


def html_to_md(data):
    data = re.sub(r'<script.*?</script>', '', data, flags=re.S | re.I)
    data = re.sub(r'<style.*?</style>', '', data, flags=re.S | re.I)
    # 去掉导航/页眉/页脚/侧栏/表单等每页重复的样板
    for tag in ('nav', 'header', 'footer', 'aside', 'form'):
        data = re.sub(r'<%s\b.*?</%s>' % (tag, tag), ' ', data, flags=re.S | re.I)
    # 优先取主内容区
    m = re.search(r'<main\b.*?</main>', data, flags=re.S | re.I)
    if m:
        data = m.group(0)
    else:
        m = re.search(r'<article\b.*?</article>', data, flags=re.S | re.I)
        if m:
            data = m.group(0)
    # 标题 h1-h6
    data = re.sub(
        r'<h([1-6])[^>]*>(.*?)</h\1>',
        lambda m: '\n' + '#' * int(m.group(1)) + ' ' + html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip() + '\n',
        data, flags=re.S | re.I)
    # 段落
    data = re.sub(
        r'<p[^>]*>(.*?)</p>',
        lambda m: '\n' + html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() + '\n',
        data, flags=re.S | re.I)
    # 列表项
    data = re.sub(
        r'<li[^>]*>(.*?)</li>',
        lambda m: '- ' + html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() + '\n',
        data, flags=re.S | re.I)
    # 代码块
    data = re.sub(
        r'<pre[^>]*>(.*?)</pre>',
        lambda m: '\n```\n' + html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() + '\n```\n',
        data, flags=re.S | re.I)
    data = re.sub(r'<[^>]+>', ' ', data)
    data = html.unescape(data)
    data = re.sub(r'[ \t]+', ' ', data)
    data = re.sub(r'\n{3,}', '\n\n', data)
    return data.strip()


def cmd_extract():
    z = read_zip()
    MD_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for name in pages(z):
        md = html_to_md(z.read(name).decode('utf-8', errors='ignore'))
        (MD_DIR / (Path(name).stem + '.md')).write_text(md, encoding='utf-8')
        n += 1
    print("extract 完成：%d 页 → %s" % (n, MD_DIR))


def wordcount(text):
    return len(re.findall(r"[A-Za-z][A-Za-z'-]+", text))


def cmd_coverage():
    z = read_zip()
    src = {Path(n).stem: n for n in pages(z)}
    md_files = sorted(MD_DIR.glob('*.md'))
    src_words = sum(wordcount(p.read_text(encoding='utf-8')) for p in md_files)
    done = sorted(TRANS_DIR.glob('*.md')) if TRANS_DIR.exists() else []
    done_stems = {p.stem for p in done}
    done_src = [s for s in src if s in done_stems]
    zh = sum(len(re.findall(r'[\u4e00-\u9fff]', p.read_text(encoding='utf-8'))) for p in done)
    print("源页面：%d  已完成翻译：%d/%d" % (len(src), len(done_src), len(src)))
    print("源英文词数：%d  已完成译文中文字符数：%d" % (src_words, zh))
    print("页数覆盖度：%.1f%%" % (len(done_src) / len(src) * 100))
    missing = sorted(set(src) - done_stems)
    if missing:
        print("未翻译页（%d）：" % len(missing))
        for s in missing:
            print("  -", s)


def cmd_glossary():
    if not GLOSSARY.exists():
        print("缺少 glossary/术语表.md")
        return
    pairs = []
    for line in GLOSSARY.read_text(encoding='utf-8').splitlines():
        m = re.match(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|', line)
        if m and m.group(1).strip() not in ('英文', 'English') and not m.group(1).startswith('-'):
            en, zh = m.group(1).strip(), m.group(2).strip()
            if en:
                pairs.append((en, zh))
    trans = sorted(TRANS_DIR.glob('*.md'))
    print("术语表 %d 条，translated/ %d 个文件" % (len(pairs), len(trans)))
    issues = 0
    for en, zh in pairs:
        for p in trans:
            body = p.read_text(encoding='utf-8')
            # 标准译名未出现，且英文裸出现（可能漏译或不一致）
            if zh not in body and en in body:
                print("  [!] %s：未出现标准译名「%s」，英文「%s」裸出现" % (p.name, zh, en))
                issues += 1
    print("术语一致性检查完成，%d 处待人工复核" % issues)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'coverage'
    {'extract': cmd_extract, 'coverage': cmd_coverage, 'glossary': cmd_glossary}.get(
        cmd, lambda: print("未知子命令：%s" % cmd))()
