#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把本项目推送/更新到 GitHub —— 纯标准库，无需 git / gh / Xcode CLT。

流程：建仓(或复用) -> 空仓库先做初始化提交 -> 逐文件建 blob -> 建 tree -> 建 commit -> 更新 ref
特性：限速保护、失败自动重试(含 403/429/5xx)、blob 本地缓存可续跑、失败时打印响应体。

用法：
    python3 tools/publish_github.py --repo cs146s-vibe-coding-zh            # 交互输入 token
    GITHUB_TOKEN=xxx python3 tools/publish_github.py --repo xxx --dry-run   # 只读预演
    python3 tools/publish_github.py --repo xxx --collect-only               # 离线清点文件
"""

import argparse
import base64
import getpass
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://api.github.com"
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".scratch", ".cache", "out"}
SKIP_NAMES = {".DS_Store", ".publish_cache.json"}
SKIP_EXT = {".pyc", ".zip"}
RETRY_CODES = (403, 429, 500, 502, 503, 504)
PACE = 0.8  # 相邻"写内容"请求的最小间隔(秒) => 约 75 次/分钟，避开二次限流


class Api:
    """带限速与重试的 GitHub REST 客户端。"""

    def __init__(self, token):
        self.token = token
        self._lock = threading.Lock()
        self._last = 0.0

    def raw(self, method, path, payload=None, timeout=90):
        url = path if path.startswith("http") else API + path
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", "Bearer " + self.token)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "c1-publisher")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read().decode("utf-8", "replace")
                return r.status, (json.loads(body) if body.strip() else {}), dict(r.headers)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            try:
                return e.code, json.loads(body), dict(e.headers)
            except Exception:
                return e.code, {"message": body[:400]}, dict(e.headers)
        except urllib.error.URLError as e:
            return 0, {"message": "network: {}".format(e.reason)}, {}

    def call(self, method, path, payload=None, pace=0.0, tries=5, label=""):
        delay, code, body = 2.0, 0, {}
        for i in range(tries):
            if pace:
                with self._lock:
                    gap = self._last + pace - time.time()
                    if gap > 0:
                        time.sleep(gap)
                    self._last = time.time()
            code, body, hdr = self.raw(method, path, payload)
            if code != 0 and code not in RETRY_CODES:
                return code, body
            if i == tries - 1:
                return code, body
            ra = str(hdr.get("Retry-After", ""))
            wait = float(ra) if ra.isdigit() else delay
            print("    · 重试 {}/{} {} {} -> HTTP {} {}（等 {:.0f}s）".format(
                i + 1, tries - 1, method, label or path, code,
                str(body.get("message"))[:80], wait))
            time.sleep(wait)
            delay *= 2
        return code, body


def collect(root):
    """收集待上传文件 -> [(仓库内相对路径, 本地绝对路径)]，已排序。"""
    files = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn in SKIP_NAMES or os.path.splitext(fn)[1] in SKIP_EXT:
                continue
            ap = os.path.join(dp, fn)
            files.append((os.path.relpath(ap, root).replace(os.sep, "/"), ap))
    files.sort()
    return files


def load_cache(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="仓库名，例如 cs146s-vibe-coding-zh")
    ap.add_argument("--dir", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="要发布的目录，默认本项目根目录")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--description",
                    default="Stanford CS146S Vibe Coding 课程资料中文翻译与可复跑流水线")
    ap.add_argument("--private", action="store_true", help="建为私有仓库")
    ap.add_argument("--message",
                    default="docs: Stanford CS146S 课程资料中文翻译（31/31 页，覆盖度 100%）")
    ap.add_argument("--dry-run", action="store_true", help="只读预演，不写入任何东西")
    ap.add_argument("--collect-only", action="store_true", help="离线清点文件，不联网")
    args = ap.parse_args()

    root = os.path.abspath(args.dir)
    files = collect(root)
    total = sum(os.path.getsize(p) for _, p in files)
    print("待发布：{} 个文件，合计 {:.1f} MB".format(len(files), total / 1048576.0))
    big = [(rp, os.path.getsize(p)) for rp, p in files if os.path.getsize(p) > 100 * 1048576]
    if big:
        raise SystemExit("以下文件超过 GitHub 单文件 100MB 上限：{}".format(big))
    if args.collect_only:
        for rp, _ in files[:5]:
            print("   ·", rp)
        print("   …（共 {} 个）".format(len(files)))
        return 0

    if args.dry_run:
        print("[dry-run] 只读预演：不联网、不写入、无需令牌。")
        print("[dry-run] 目标仓库：<你的用户名>/{}（不校验令牌）".format(args.repo))
        print("[dry-run] 待推送 {} 个文件，合计 {:.1f} MB。".format(len(files), total / 1048576.0))
        return 0

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("请粘贴 GitHub Personal Access Token（输入不回显，不写入任何文件）：")
        token = getpass.getpass("GitHub Token（输入时不显示，回车确认）: ").strip()
    if not token:
        raise SystemExit(3)

    api = Api(token)
    code, me = api.call("GET", "/user", tries=2)
    if code != 200:
        raise SystemExit("令牌校验失败：HTTP {} {}".format(code, json.dumps(me)[:200]))
    owner = me["login"]
    print("身份校验通过：{}".format(owner))
    full = "{}/{}".format(owner, args.repo)

    if args.dry_run:
        print("[dry-run] 不做任何写入。目标：{}".format(full))
        return 0

    # 1) 建仓（已存在则复用）
    code, repo = api.call("POST", "/user/repos", {
        "name": args.repo,
        "description": args.description,
        "private": bool(args.private),
        "auto_init": False,
    }, tries=1)
    if code == 201:
        print("已创建仓库：{}".format(repo.get("html_url")))
    elif code in (409, 422):
        print("仓库已存在，将继续推送：{}".format(full))
    elif code == 403:
        c2, _ = api.call("GET", "/repos/" + full, tries=1)
        if c2 == 200:
            print("令牌无建仓权限，但仓库已存在，继续推送到：{}".format(full))
        else:
            print("")
            print("！当前令牌没有创建仓库的权限（GitHub 返回 403 Resource not accessible）。")
            print("  两种解法：① 用带 repo 权限的经典令牌（ghp_ 开头）；")
            print("            ② 先手动建空仓库：https://github.com/new")
            print("               名称 {}，选 Public，不要勾 README/.gitignore/license，".format(args.repo))
            print("               建好后用同一个令牌重跑本脚本，会自动检测到该仓库。")
            print("")
            raise SystemExit(3)
    else:
        raise SystemExit("建仓失败：HTTP {} {}".format(code, json.dumps(repo)[:300]))

    # 2) 空仓库必须先做一次初始化提交，否则 Git Data API 写入会被拒
    code, ref = api.call("GET", "/repos/{}/git/ref/heads/{}".format(full, args.branch), tries=2)
    parent = ref.get("object", {}).get("sha") if code == 200 else None
    if not parent:
        name = ".gitignore" if os.path.isfile(os.path.join(root, ".gitignore")) else ".gitkeep"
        src = os.path.join(root, name)
        raw = open(src, "rb").read() if os.path.isfile(src) else b"# init\n"
        code, o = api.call("PUT", "/repos/{}/contents/{}".format(full, name), {
            "message": "chore: 初始化仓库",
            "content": base64.b64encode(raw).decode("ascii"),
            "branch": args.branch,
        }, tries=2)
        if code not in (200, 201):
            raise SystemExit("初始化提交失败：HTTP {} {}".format(code, json.dumps(o)[:300]))
        parent = o.get("commit", {}).get("sha")
        print("已初始化首个提交（{}），父提交 {}".format(name, (parent or "?")[:10]))
    else:
        print("已有分支 {}，父提交 {}".format(args.branch, parent[:10]))

    # 3) 逐文件建 blob（限速 + 本地缓存，中断可续跑）
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".publish_cache.json")
    cache = load_cache(cache_path)

    def blob_of(item):
        rp, ap = item
        st = os.stat(ap)
        hit = cache.get(rp) or {}
        if hit.get("sha") and hit.get("size") == st.st_size and hit.get("mtime") == int(st.st_mtime):
            return rp, hit["sha"]
        with open(ap, "rb") as fh:
            content = base64.b64encode(fh.read()).decode("ascii")
        code, o = api.call("POST", "/repos/{}/git/blobs".format(full),
                           {"content": content, "encoding": "base64"},
                           pace=PACE, label=rp)
        if code not in (200, 201) or "sha" not in o:
            raise RuntimeError("blob 创建失败 {} -> HTTP {} {}".format(
                rp, code, json.dumps(o)[:200]))
        cache[rp] = {"sha": o["sha"], "size": st.st_size, "mtime": int(st.st_mtime)}
        return rp, o["sha"]

    entries = []
    done = 0
    try:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for rp, sha in pool.map(blob_of, files):
                entries.append({"path": rp, "mode": "100644", "type": "blob", "sha": sha})
                done += 1
                if done % 20 == 0 or done == len(files):
                    print("  blob {}/{}".format(done, len(files)))
    finally:
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache, f)
        except Exception:
            pass
    print("blob 完成：{}".format(len(entries)))

    # 4) tree -> commit -> 更新 ref
    code, tree = api.call("POST", "/repos/{}/git/trees".format(full), {"tree": entries}, tries=3)
    if code not in (200, 201) or "sha" not in tree:
        raise SystemExit("建 tree 失败：HTTP {} {}".format(code, json.dumps(tree)[:300]))

    code, commit = api.call("POST", "/repos/{}/git/commits".format(full),
                            {"message": args.message, "tree": tree["sha"], "parents": [parent]},
                            tries=3)
    if code not in (200, 201) or "sha" not in commit:
        raise SystemExit("建 commit 失败：HTTP {} {}".format(code, json.dumps(commit)[:300]))

    code, upd = api.call("PATCH", "/repos/{}/git/refs/heads/{}".format(full, args.branch),
                         {"sha": commit["sha"], "force": False}, tries=3)
    if code not in (200, 201):
        raise SystemExit("更新分支失败：HTTP {} {}".format(code, json.dumps(upd)[:300]))

    print("")
    print("推送完成：{} 个文件 / {:.1f} MB".format(len(entries), total / 1048576.0))
    print("仓库地址（提交用）：https://github.com/{}".format(full))
    print("提交记录：https://github.com/{}/commit/{}".format(full, commit["sha"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
