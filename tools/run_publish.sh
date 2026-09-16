#!/bin/bash
# C1 发布一键入口：优先使用令牌文件，其次退回终端输入。
# 用法：bash tools/run_publish.sh
cd "$(dirname "$0")/.." || exit 1

TOK="/Users/xiaowo/.cogseed-dev/userWorkSpace/我的挑战有哪些/gh_token.txt"

if grep -Eq 'gh[pousr]_[A-Za-z0-9]{16,}' "$TOK" 2>/dev/null; then
  echo "== 已检测到令牌文件，开始推送 =="
  exec python3 tools/publish_with_prompt.py --repo cs146s-vibe-coding-zh --token-file "$TOK"
fi

echo "== 未检测到令牌文件，改为终端输入 =="
echo "== （提示：也可以把令牌粘到 $TOK 里再跑本脚本）=="
exec python3 tools/publish_with_prompt.py --repo cs146s-vibe-coding-zh
