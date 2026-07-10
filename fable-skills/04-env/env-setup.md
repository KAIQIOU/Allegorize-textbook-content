# Fable Skills 环境搭建指南

> **目标**: 让其他 agent 在**没有任何已有环境**的情况下,从零搭出可跑寓言渲染的环境。

---

## 1. 操作系统 & Python

### 1.1 操作系统
- **Windows 10/11** (已验证)
- macOS / Linux: 渲染脚本跨平台, 但 `bat` 启动器需改成 `.sh`

### 1.2 Python 版本
- **Python 3.11+** (已用 3.11 验证)
- 安装: <https://www.python.org/downloads/windows/>
- ⚠️ 安装时勾选 "Add Python to PATH"

### 1.3 验证
```bash
python --version
# 应输出: Python 3.11.x
```

---

## 2. 第三方依赖

**寓言渲染脚本只用 Python 标准库**(`pathlib`, `re`, `string`),**不需要 pip install 任何包**。

唯一可能需要的依赖:

| 依赖 | 何时需要 | 安装命令 |
|------|---------|---------|
| 无 | 渲染脚本只读 stdlib | — |
| playwright | 截图验证(可选) | `pip install playwright && playwright install chromium` |
| markdownify | 反向解析(可选) | `pip install markdownify` |

---

## 3. 字体 (HTML 内嵌, 无需本地装)

寓言 HTML 输出**内嵌 CSS** 定义了所有字体:
- 中文字体: `'Noto Serif SC', 'Source Han Serif SC', 'Songti SC', serif`
- 等宽字体: `'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace`

如果用户在浏览器看到中文乱码,需:
1. Windows 安装 Noto Serif SC: <https://fonts.google.com/noto/specimen/Noto+Serif+SC>
2. 或系统自带"宋体"/"思源宋体"

---

## 4. 文件编码

⚠️ **核心**: 所有 `.py` 和 `.md` 文件必须用 **UTF-8 with BOM** 或 **UTF-8**。

Windows 默认 GBK 会导致:
- 中文报错 `SyntaxError: Non-UTF-8 code`
- HTML 输出中文乱码

### 解决方案
```bash
# 方法 1: 运行时强制 UTF-8
python -X utf8 scripts/rewrite_ch12_v1.py

# 方法 2: 文件头声明 (脚本已加)
# -*- coding: utf-8 -*-
```

---

## 5. 目录结构

```
fable-skills/                 # 本 skills 包
├── README.md                  # 总入口
├── 01-sop/                    # 3 个 SOP 文档
├── 02-scripts/                # 渲染脚本 + 回归
├── 03-reference/              # ch11/ch12 源+输出样本
├── 04-env/                    # 本文件 + requirements.txt
└── 05-checklist/              # 写前/写后/回归清单
```

---

## 6. 跑通验证 (Smoke Test)

```bash
# 1. 进入目录
cd fable-skills/

# 2. 看 SOP 总览
type 01-sop\fable-write-sop.md        # Windows
# cat 01-sop/fable-write-sop.md       # macOS/Linux

# 3. 跑渲染脚本(用 ch12 样本, 应生成 chapter12-output.html 副本)
python -X utf8 02-scripts/rewrite_ch12_v1.py

# 4. 跑回归(应全部通过)
python -X utf8 02-scripts/fable_regression_check.py

# 5. 双击打开 HTML 看效果
start 03-reference/chapter12-output.html        # Windows
open 03-reference/chapter12-output.html         # macOS
```

---

## 7. 跨平台注意

| 操作 | Windows | macOS/Linux |
|------|---------|-------------|
| 跑脚本 | `python -X utf8 ...` | `python3 -X utf8 ...` |
| 看文件 | `type file.md` | `cat file.md` |
| 打开 HTML | `start file.html` | `open file.html` (Mac) / `xdg-open file.html` (Linux) |
| 路径分隔 | `\` 或 `/` 都可 | `/` |

`run_pipeline.bat` 仅 Windows, 跨平台需改成 `run_pipeline.sh`:
```bash
#!/bin/bash
python3 -X utf8 02-scripts/rewrite_chXX_v1.py
python3 -X utf8 02-scripts/fable_regression_check.py
```

---

## 8. 故障排查

| 问题 | 排查 |
|------|------|
| `ModuleNotFoundError: No module named 'xxx'` | 寓言渲染只用 stdlib, 不需要 pip; 检查 PYTHONPATH |
| 中文乱码 | 强制 `python -X utf8 ...` |
| `SyntaxError: Non-UTF-8 code` | 文件保存为 UTF-8 with BOM |
| HTML 打开空白 | 检查浏览器控制台 (F12); CSS 用内联 |
| 回归脚本 glob 不匹配 | Python 3.11 glob 支持中文, 旧版需 `glob.glob(..., encoding='utf-8')` |