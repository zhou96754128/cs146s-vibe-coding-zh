#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全发布入口：获取 GitHub Token（不回显、不进聊天记录），再调用同目录的
publish_github.py 完成「建仓/复用 + 推送」。

Token 来源（按优先级）：
1) --token-file <路径>  从本地文件读取（文件由用户自行创建，用完请删除）
2) 环境变量 GITHUB_TOKEN
3) 终端交互输入（getpass，输入不显示）

设计要点：
- Token 只存在于本次进程的内存环境变量中，不写入任何文件、不打印。
- 其余参数（--repo / --branch / --private / --dry-run 等）原样透传给 publish_github.py。

用法：
    python3 tools/publish_with_prompt.py --repo cs146s-vibe-coding-zh
    python3 tools/publish_with_prompt.py --repo cs146s-vibe-coding-zh --token-file /path/gh_token.txt
    python3 tools/publish_with_prompt.py --repo cs146s-vibe-coding-zh --dry-run
"""

import getpass
import os
import re
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "publish_github.py")

# 只匹配 GitHub 官方令牌形态，避免把说明文字/URL 误当成令牌。
TOKEN_RE = re.compile(r"(github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{16,})")


def _read_token_file(path: str) -> str:
    """从令牌文件中提取令牌：优先匹配官方前缀，其次回退到首个非注释非空行。

    这样可以容忍用户在文件里写了说明文字（例如本脚本生成的提示模板）。
    """
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    hit = TOKEN_RE.search(raw)
    if hit:
        return hit.group(1).strip()
    for line in raw.splitlines():
        line = line.strip().lstrip("\ufeff")
        if line and not line.startswith("#"):
            return line
    return ""


def main() -> int:
    if not os.path.exists(TARGET):
        sys.stderr.write("找不到 %s，无法继续。\n" % TARGET)
        return 2

    argv = sys.argv[1:]
    token = ""
    passthrough = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--token-file":
            if i + 1 >= len(argv):
                sys.stderr.write("--token-file 后面缺少文件路径，已中止，未做任何改动。\n")
                return 3
            path, i = argv[i + 1], i + 2
        elif a.startswith("--token-file="):
            path, i = a.split("=", 1)[1], i + 1
        else:
            passthrough.append(a)
            i += 1
            continue

        try:
            token = _read_token_file(path)
        except OSError as exc:
            sys.stderr.write("读取令牌文件失败：%s\n已中止，未做任何改动。\n" % exc)
            return 3
        if not token:
            sys.stderr.write("令牌文件为空：%s\n已中止，未做任何改动。\n" % path)
            return 3
    else:
        path = None

    if not token:
        token = (os.environ.get("GITHUB_TOKEN") or "").strip()
    if not token:
        token = (getpass.getpass("GitHub Token（输入时不显示，回车确认）: ") or "").strip()
        if not token:
            sys.stderr.write("未输入 Token，已中止，未做任何改动。\n")
            return 3

    os.environ["GITHUB_TOKEN"] = token
    print("Token 已读入内存（长度 %d），开始处理……" % len(token))
    if path:
        print("提示：推送结束后请删除令牌文件 %s" % path)

    sys.argv = [TARGET] + passthrough
    try:
        runpy.run_path(TARGET, run_name="__main__")
    finally:
        # 尽力擦除内存中的凭据
        os.environ.pop("GITHUB_TOKEN", None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
