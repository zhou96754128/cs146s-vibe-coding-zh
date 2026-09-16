# CS146S《The Modern Software Developer》课程资料中文翻译包

Stanford University · Fall 2025 · 离线镜像 + 全量中文翻译

> 本仓库是一套**可复跑的信息获取与翻译管线**及其产物：把 Stanford CS146S（The Modern Software Developer，俗称 Stanford Vibe Coding）的全部可下载公开资料抓取归档、抽取为干净 Markdown、按统一术语表翻译为简体中文，并附带自动质量抽检脚本与全部质检报告。
>
> 换一门课的资料，把 `pipeline/pipeline.py` 里的源路径换掉，同样的流程可再次产出——这是本项目的核心目标，而不只是一份译文。

---

## 一、来源与获取方式

| 项目 | 内容 |
|---|---|
| 一手来源 | 课程官网 `https://themodernsoftware.dev/` |
| 课程 | CS146S: The Modern Software Developer（Stanford, Fall 2025） |
| 离线缓存 | `src/CS146S_offline/`，缓存时间 2026-04-02 |
| 原始压缩包 | `materials/CS146S_offline.zip`（挑战平台下发的源材料） |
| 页面清单 | `src/CS146S_offline/all_urls.txt`、`page_map.json`（URL ↔ 本地文件对照） |

**获取流程**：下载平台下发的 `CS146S_offline.zip` → 解压到 `src/` → 运行 `pipeline.py extract` 把 HTML 页面抽成干净 Markdown → 分批翻译 → 自动质检。

## 二、覆盖范围（实测）

| 指标 | 数值 |
|---|---|
| 源讲义页面（HTML） | 31 |
| 已完成中文翻译 | **31 / 31** |
| 页数覆盖度 | **100.0%** |
| 源英文词数 | 65,062 |
| 译文中文字符数 | 97,745 |
| 术语表条目 | 94 条（验收要求 ≥50 条） |
| 附加 PDF 资料 | 3 个（见「已知缺口」） |

> 覆盖度按「有正文的页面」计算。另有 4 个源页面在离线镜像中本身就没有正文（0～341 字节的链接/重定向存根），已在 `translated/_无正文页说明.md` 中逐页登记，不计入分母。

## 三、目录结构

```
C1-斯坦福VibeCoding翻译/
├── README.md                  ← 本文件：资料包说明
├── AI日志/                    ← 每日 AI 协作日志（工具 / prompt / 踩坑）
├── AAR/                       ← 七维 AAR 复盘
├── 拿来说明/                  ← 「拿来说明」：关键决策如何借助 AI 做出
├── src/CS146S_offline/        ← 源材料（离线镜像）
│   ├── pages/*.html           ← 31 个原始 HTML 页面
│   ├── markdown/*.md          ← extract 抽取出的干净英文 Markdown（翻译输入）
│   ├── pdfs/*.pdf             ← 3 个附加 PDF 资料
│   └── ...
├── glossary/术语表.md         ← 94 条术语表（译文一致性锚点）
├── translated/                ← 中文译文（每页一个 .md，文件名与源 stem 一致）
│   └── _parts/                ← 超长页的分片中间产物（可追溯）
├── chunks/                    ← 超长页的源文分片（分片翻译证据链）
├── pipeline/                  ← 可复跑管线
│   ├── extract.py             ← HTML → 干净 Markdown（仅标准库）
│   ├── pipeline.py            ← 主流程：extract / coverage / glossary
│   └── qc.py                  ← 质量抽检：结构对等 / 残留英文 / 术语落地 / 空壳页
└── out/                       ← 质检报告与审计产物
```

## 四、翻译流程（回到本仓库后如何复跑）

前置条件：本机 `python3`（仅用标准库，无需 pip 安装任何依赖）。

```bash
cd C1-斯坦福VibeCoding翻译

# 1) 从源 zip 抽取干净 Markdown（HTML → 可翻译文本，剥离导航/页眉/页脚）
python3 pipeline/pipeline.py extract

# 2) 查看翻译覆盖度（源页数/词数 vs translated/）
python3 pipeline/pipeline.py coverage

# 3) 校验术语是否全文遵循术语表
python3 pipeline/pipeline.py glossary

# 4) 质量抽检（四类自动检查，--write 同时写入 out/qc-report.md）
python3 pipeline/qc.py --write
```

**当前实测输出**（`python3 pipeline/pipeline.py coverage`）：

```
源页面：31  已完成翻译：31/31
源英文词数：65062  已完成译文中文字符数：97745
页数覆盖度：100.0%
```

## 五、翻译约定（术语一致性怎么保证）

1. **一词一译**：`glossary/术语表.md` 是唯一译名基准，共 94 条，分核心范式、安全、工程实践等类目。
2. **产品名/专有名词保留英文**：Claude Code、GitHub Copilot、Kubernetes、OWASP、MCP Registry 等不硬译，首次出现可加中文括注。
3. **技术缩写保留英文**：MCP、SAST、DAST、LLM、SRE、PR、CVE、RCE 等保留原文，首次出现给出中文全称。
4. **机器可校验**：`pipeline.py glossary` 会检查术语表条目在译文中是否用了标准译名（只照抄英文、中文译名 0 次 → 告警）。
5. **代码与引用原样保留**：代码块、行内代码、命令行、URL、以及原文中逐字引用的模型输出（如 context-rot 里演示模型退化的原句）不翻译也不改写。

## 六、质量抽检结果（out/）

- `out/qc-report.md` — 最终质检汇总：**结构告警 0 ｜ 残留英文告警 0 ｜ 术语告警 0 ｜ 缺译文 0**，结构差异 13 项已逐条归档说明。
- `out/qc-struct-audit.md` — 13 项源/译文结构差异逐页对账（为什么差、差在哪、是否漏译）。
- 独立硬伤扫描（32 个译文文件、185,301 字符）：不闭合代码围栏 0 ｜ 未还原 HTML 实体 0 ｜ 真错字 0 ｜ 泄漏的内部标记 0。

**结构差异为什么不是漏译**：差异集中在两类——① 源站抓取时混入的博客/文档框架块（侧栏导航、页脚推广位、「about the author」），译文按资料包用途剔除；② 源页用重复 H4 承载攻击场景（agentic-ai-threats 有 10 个场景），译文改为场景级标题并保留全部表格。逐条证据见 `out/qc-struct-audit.md`。

## 七、使用方法（陌生人怎么用）

1. 只想读译文：直接打开 `translated/` 下的同名 `.md`，或用支持 Markdown 的编辑器/笔记软件批量导入。
2. 想核对原文：`src/CS146S_offline/markdown/` 下同名英文文件，逐页一一对应。
3. 想复跑或换课复用：按第四节四条命令执行；换课时只需替换 `pipeline.py` 中的源路径与 `glossary/术语表.md`。
4. 想看过程与决策：`AI日志/` 看每天用了什么工具和 prompt、踩了什么坑；`AAR/` 看复盘；`拿来说明/` 看关键产出的完整推导。

## 八、已知缺口（诚实清单）

| 缺口 | 说明 | 影响 |
|---|---|---|
| 3 个 PDF 未翻译 | `ai-assisted-code-review-assessment.pdf`、`how-anthropic-uses-claude-code.pdf`、`how-openai-uses-codex.pdf` 为附加阅读材料 | 不影响 31 页讲义覆盖度；后续可扩 |
| 4 个无正文页 | good-context-good-code(217B)、how-warp-uses-warp(1B)、lessons-from-ai-code-reviews(0B)、peeking-under-the-hood-of-claude-code(341B) 在离线镜像中即无正文 | 已登记说明，非漏译 |
| 视频字幕未获取 | 课程视频字幕不在一手来源的可下载范围内 | 覆盖度按讲义计算 |
| 页面框架块已剔除 | 侧栏导航/页脚推广位等非讲义内容未译 | 提高可读性，已在质检备注 |
| 译文未经人工逐句校对 | 采用「机器翻译 + 术语表锚定 + 自动抽检」流程 | 术语与结构已机器校验；文学性润色留待后续 |

## 九、许可与致谢

- 课程内容版权归 Stanford University 及原作者所有，本仓库仅作学习用途的中文翻译与整理，不主张原始内容权利。
- 原始站点：`https://themodernsoftware.dev/`；离线镜像缓存时间 2026-04-02。
