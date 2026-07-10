# Fable Skills — 寓言系列 v1 渲染完整复现包

> **项目代号**: Fable-Skills (寓言系列第 02-12 章沉淀的可复用 skills 包)
> **目标受众**: 任何 agent 在**没有原团队环境**的情况下,从零渲染出符合 v5 规范的寓言章节
> **最后更新**: 2024-06-29
> **配套资产**: `01-sop/` (3 份 SOP) + `02-scripts/` (3 个脚本 + 1 个 bat) + `03-reference/` (ch11/ch12 源+输出) + `04-env/` (环境指南) + `05-checklist/` (3 份清单)
> **沉淀经验**: 寓言系列 11 章沉淀(ch02 → ch12)

---

## 0. 这是什么?

一套**自包含的寓言单章渲染 skills 包**。任何 agent 只要:

1. 安装 Python 3.11+ (见 `04-env/env-setup.md`)
2. 阅读本文档 § 1-3 (Quick Start)
3. 复制模板脚本 → 改 4 处命名 → 跑 bat

就能从 0 渲染出符合 v5 规范的寓言章节 HTML,**不依赖原团队环境 / 记忆库 / 项目历史**。

### 0.1 包内沉淀了什么?

寓言项目从第 02 章到第 12 章共 11 章经验沉淀为 3 类 SOP:

| SOP | 章节 | 沉淀内容 |
|-----|------|----------|
| **fable-write-sop** | ch02-12 | 12 步标准操作流程(3 必跑 + 4 必守 + 5 必改) |
| **fable-ch11-feedback-correction** | ch11 反馈 | 用户反馈"故事逻辑+语序混乱"5 整改范式 |
| **fable-antagonist-humanity** | ch04-12 | 反派"加人性"4 步法 + 10 连击统计 |

---

## 1. 5 分钟快速开始 (Quick Start)

### 1.1 验证环境

```bash
# 检查 Python
python --version
# 应: Python 3.11+

# 进入包
cd fable-skills/

# 看 SOP 总入口
type 01-sop\fable-write-sop.md       # Windows
# cat 01-sop/fable-write-sop.md      # macOS/Linux
```

### 1.2 跑通 ch12 样本 (Smoke Test)

```bash
# 1. 渲染 ch12 (用包内现成脚本)
cd 02-scripts/
python -X utf8 rewrite_ch12_v1.py

# 2. 跑回归 (应全部通过)
python -X utf8 fable_regression_check.py

# 3. 双击打开看效果
start ..\03-reference\chapter12-output.html       # Windows
open ../03-reference/chapter12-output.html        # macOS
```

**预期输出**:
- ch12 HTML 生成在 `reports/第12章-训练与对齐-v1.html` (需要 reports/ 目录存在)
- 回归脚本输出 "Files: N / N passed"

### 1.3 自定义输出路径 (其他 agent 复用)

包内脚本默认输出到 `reports/`(默认输出目录, 可用 FABLE_REPORT_DIR 覆盖)。

**其他 agent** 改用自己路径,有 2 种方式:

```bash
# 方式 1: 环境变量(推荐)
export FABLE_REPORT_DIR=/path/to/your/reports       # macOS/Linux
set FABLE_REPORT_DIR=D:\path\to\your\reports        # Windows
python -X utf8 rewrite_ch12_v1.py                   # 自动写到新路径

# 方式 2: 改脚本默认值
# 编辑 rewrite_chXX_v1.py 头部:
# REPORT_DIR = Path(r"D:\your\reports")
```

**Why env 变量**:不改包内代码即可换路径,**保持包的不可变**,其他 agent 升级时不冲突。

### 1.3 想渲染新章节? 4 步搞定

```bash
# 1. 复制模板 (用 ch11 改, ch11 结构最稳定)
cp rewrite_ch11_v1-reference.py rewrite_ch13_v1.py

# 2. 编辑脚本头部 4 处命名决策段 (脚本顶部)
#    CHAPTER_NUM = "13"
#    CHAPTER_NAME = "<新章主题>"
#    OUT = ...第13章-<主题>-v1.html
#    Footer link 改 "上一章/下一章"

# 3. 编辑 TOC 11 项 + HERO + 11 个 section 块 + 6 annotation + 10 quiz

# 4. 跑
python -X utf8 rewrite_ch13_v1.py
python -X utf8 fable_regression_check.py

# 5. 一键(可选)
run_pipeline.bat 13 <新章主题>
```

---

## 2. 包结构详解

```
fable-skills/
├── README.md                              ← 你正在读的(总入口 + 复现指南)
│
├── 01-sop/                                ← 3 份 SOP 文档(先读这)
│   ├── fable-write-sop.md                 ← 12 步 SOP:3 必跑 + 4 必守 + 5 必改
│   ├── fable-ch11-feedback-correction.md  ← ch11 用户反馈 5 整改范式
│   └── fable-antagonist-humanity.md       ← 反派"加人性"4 步法 + 10 连击
│
├── 02-scripts/                            ← 渲染 + 回归 + 启动器
│   ├── rewrite_ch12_v1.py                 ← ch12 实战脚本(改 4 处就能用)
│   ├── rewrite_ch11_v1-reference.py       ← ch11 实战脚本(模板参考)
│   ├── fable_regression_check.py          ← 回归脚本(28 文件全过验证)
│   └── run_pipeline.bat                   ← Windows 一键执行
│
├── 03-reference/                          ← ch11/ch12 源 + 输出样本
│   ├── chapter11-story-skeleton.md        ← ch11 故事骨架(11 节点)
│   ├── chapter11-output.html              ← ch11 输出(925 行参考)
│   ├── chapter12-story-skeleton.md        ← ch12 故事骨架
│   └── chapter12-output.html              ← ch12 输出(925 行 / 0 残留)
│
├── 04-env/                                ← 环境依赖
│   ├── requirements.txt                   ← 依赖声明(实际无第三方依赖)
│   └── env-setup.md                       ← 从零搭建指南
│
└── 05-checklist/                          ← 3 份清单
    ├── pre-render-checklist.md            ← 写脚本前 3 必跑
    ├── post-render-checklist.md           ← 写脚本后 5 项自检
    └── regression-checklist.md            ← 回归测试清单
```

---

## 3. 完整 12 步 SOP 速览

> **详细版** 见 [01-sop/fable-write-sop.md](01-sop/fable-write-sop.md)。这里是极速版。

### Step 0: 写骨架前 · 3 必跑 grep

```bash
# 防前章 bug 带到新章
grep -c 'class="correct"' ../reports/第<前NUM>章-*.html      # 应为 0
grep -cE 'text-align:.*justify' ../reports/第<前NUM>章-*.html  # 应为 0
grep -cE '\*\*[^*]+\*\*' ../reports/第<前NUM>章-*.html         # 应为 0
```

### Step 1: 写故事骨架 · 5 必改

详见 [01-sop/fable-ch11-feedback-correction.md](01-sop/fable-ch11-feedback-correction.md)。

| # | 整改 | 一句话 |
|---|------|--------|
| 1 | 主旨句 | 每幕开头写 "**主旨: X —— Y**" |
| 2 | 反派退场 | M1 退场明确, M5 再登场间隔 1-2 幕 |
| 3 | 朝代白话 | 删"在做 X 的时候" / "如果 X, Y 就会 Z" |
| 4 | 对白比喻 | 用马/学子/镜/衣, 1-3 句 |
| 5 | 因果链 | "动作 → 为什么 → 改了什么 → 提分" |

### Step 2: 写渲染脚本 · 4 必守

| # | 必守 | 一句话 |
|---|------|--------|
| 1 | 命名决策段 | 脚本开头 CHAPTER_NUM/NAME/OUT |
| 2 | quiz 不加粗 | 选项藏 `<details>`, 不让用户一眼看出 |
| 3 | 解析朝代化 | annotation 内可英文, quiz 解析必须朝代化 |
| 4 | coverage 第 3 列 | 写"见 annotation", 不直接写英文 |

### Step 3: 跑渲染

```bash
python -X utf8 rewrite_ch<NUM>_v1.py
```

### Step 4: 5 项自检

详见 [05-checklist/post-render-checklist.md](05-checklist/post-render-checklist.md)。全 0 才算 v1 成功。

### Step 5: 跑回归

```bash
python -X utf8 fable_regression_check.py
```

### Step 6: 同步沉淀

把新章节资料沉淀到自己的 memory 系统(本包内不需要做这步, 包是只读的)。

---

## 4. 渲染脚本结构 (改这 4 处就能用)

```python
# === rewrite_ch13_v1.py 头部 4 处命名决策段 ===
CHAPTER_NUM = "13"                                           # ← 改 1
CHAPTER_NAME = "<新章主题>"                                   # ← 改 2
REPORT_DIR = Path(r"reports")
OUT = REPORT_DIR / f"第{CHAPTER_NUM}章-{CHAPTER_NAME}-v1.html"  # ← 改 3

# 中段 11 个 section 块(每个 section 一段 HTML)
# 必改: HERO 年龄 / TOC 11 项 / 11 section 标题与内容 / 6 annotation
# 必改: 10 quiz 题与 4 选项 / ENGLISH_TERMS 列表 / Footer 上一章下一章链接 ← 改 4
```

---

## 5. HTML 输出结构规范 (v5)

每个章节 HTML 必须包含:

| 元素 | 数量 | 说明 |
|------|------|------|
| `<aside class="annotation">` | ≥ 6 | 英文术语查档块 |
| `<details class="quiz-answer">` | ≥ 10 | 自测题(藏在折叠里) |
| `<ul class="quiz-options">` | ≥ 10 | 4 选项, 不加粗 |
| `<table class="coverage-table">` | 1 | 三列:朝代叙事/朝代细节/见 annotation |
| `<section class="sticky-toc">` | 1 | 240px 宽(改自 200px 防中文截断) |
| `<div class="hero">` | 1 | 含主角年龄 |

详细 HTML 模板见 [03-reference/chapter12-output.html](03-reference/chapter12-output.html) (925 行)。

---

## 6. 环境依赖

**寓言渲染脚本只用 Python 标准库, 不需要 pip install 任何包**。

详细搭建见 [04-env/env-setup.md](04-env/env-setup.md)。

最小环境:
- Python 3.11+
- UTF-8 编码支持(`python -X utf8`)
- 中文字体(浏览器内嵌 CSS 已声明, 系统可选装 Noto Serif SC)

---

## 7. 跨平台

| 操作 | Windows | macOS/Linux |
|------|---------|-------------|
| 跑脚本 | `python -X utf8 ...` | `python3 -X utf8 ...` |
| 看文件 | `type file.md` | `cat file.md` |
| 打开 HTML | `start file.html` | `open file.html` / `xdg-open file.html` |
| 启动器 | `run_pipeline.bat` | `run_pipeline.sh`(本包未提供,需自建) |

---

## 8. 故障排查

| 问题 | 排查 |
|------|------|
| 中文乱码 | 强制 `python -X utf8 ...` |
| `SyntaxError: Non-UTF-8 code` | 文件保存为 UTF-8 with BOM |
| `ModuleNotFoundError` | 寓言渲染只用 stdlib, 不需要 pip; 检查 PYTHONPATH |
| HTML 打开空白 | 检查浏览器控制台 F12 |
| 回归脚本 0 文件 | 检查 REPORT_DIR 路径 / 章节文件名格式 |
| 英文泄漏 > 6 | 跑 `05-checklist/post-render-checklist.md` 自检 5 |

---

## 9. 包内沉淀的设计决策 (供其他 agent 复用)

### 9.1 跨章主角年龄阶梯

```
小书童 14 → 太子 14/15/16/17/18/19/20/21/22/23 岁(第 02-12 章)
```

每章主角升 1 岁,反派的"善"也随之迭代。

### 9.2 跨章场景不重复

| 章 | 场景 | 衙门口 |
|----|------|--------|
| ch02 | 工部 | 营造司 |
| ch03 | 翰林院 | 算法房 |
| ch04 | 工部+翰林院 | 算法房 |
| ch05 | 江南织造局 | 改革督办 |
| ch06 | 京城四部 | 联席 |
| ch07 | 钦天监 | 算法房 |
| ch08 | 翰林院 | 文献阁 |
| ch09 | 通政司 | 奏章房 |
| ch10 | 会同馆 | 番使院 |
| ch11 | 礼部 | 试院 |
| ch12 | 国子监 | 太学 |

新章节必须选**前 11 章没用过的衙门口 + 场景**。

### 9.3 反派"加人性"4 步法

```
1. 善的事业主主张(真心关怀, 不是为反而反)
2. 善与太子路线有真实冲突(价值观撞车)
3. 反派"反转"是被"实证"打脸(数据打脸, 不是嘴炮)
4. 反转后反派"主动请缨"加主角阵营(给"面子")
```

跨章 10 连击:张编修/织造保守派/户部主事/梁王(2 次)/范纯之/郑直/沈一石/韩守拙。

---

## 10. 复现验证记录

| 章节 | 用本包渲染 | 结果 | 修复次数 |
|------|----------|------|---------|
| ch11 | ❌(包未沉淀) | 0 修复但用户反馈 1 条 | 0(但 1 反馈) |
| ch12 | ✅(包内含脚本) | 0 修复, 28 文件全过 | 0 |
| ch13+ | 套 12 步 SOP | 待其他 agent 验证 | 待验证 |

**沉淀有效性证明**:ch12 用本包 12 步 SOP 渲染,一次 0 修复,**证明 SOP 跨章复用有效**。

---

## 11. 协议 & 许可

- **内部沉淀**:本系列项目内部使用,允许修改和分发
- **复用条件**:遵守 `01-sop/` 3 份 SOP 规范,标注本系列项目出处
- **更新触发**:寓言章节 ≥ 1 个新 SOP 增量时,同步更新本包

---

## 12. 索引 & 链接

**包内先读**:
1. [01-sop/fable-write-sop.md](01-sop/fable-write-sop.md) — 12 步 SOP 总入口
2. [01-sop/fable-ch11-feedback-correction.md](01-sop/fable-ch11-feedback-correction.md) — 5 整改范式
3. [04-env/env-setup.md](04-env/env-setup.md) — 环境搭建

**参考样本**:
- [03-reference/chapter11-story-skeleton.md](03-reference/chapter11-story-skeleton.md) — 故事骨架模板
- [03-reference/chapter12-output.html](03-reference/chapter12-output.html) — 输出 HTML 样本

**清单**:
- [05-checklist/pre-render-checklist.md](05-checklist/pre-render-checklist.md) — 写前 3 必跑
- [05-checklist/post-render-checklist.md](05-checklist/post-render-checklist.md) — 写后 5 自检
- [05-checklist/regression-checklist.md](05-checklist/regression-checklist.md) — 回归清单

---

**包版本**: v1.0 (2024-06-29 沉淀, ch12 0 修复验证)
**维护**: 寓言系列作者
**下次更新触发**:ch13+ 新 SOP 沉淀 / 包内文档错误修正