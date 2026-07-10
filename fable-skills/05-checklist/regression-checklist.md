# 回归测试清单

> **目的**: 每章 v1 渲染后,**跑回归脚本**确保所有已渲染章节都符合规范。

## 跑法

```bash
python -X utf8 02-scripts/fable_regression_check.py
```

## 预期输出

```
=== Fable Regression Check v2 ===
Scanning 28 HTML files...

[01/28] 第01章-*.html ✓
[02/28] 第02章-*.html ✓
...
[28/28] 第28章-*.html ✓

=== Summary ===
Files: 28 / 28 passed
Issues: 0 critical, 0 warning
```

## 回归脚本检测的 8 项

| # | 检测项 | 期望 |
|---|--------|------|
| 1 | `.correct` 类 | 0 |
| 2 | `text-align: justify` | 0 |
| 3 | `**残留` | 0 |
| 4 | quiz-options `<strong>` | 0 |
| 5 | 正文英文术语 | ≤ 6 (annotation 内) |
| 6 | annotation 数量 | ≥ 6 |
| 7 | TOC 项数 | ≥ 8 |
| 8 | HERO 含主角年龄 | True |

## 扩展 glob 支持 2 位数章节

```python
# 关键代码 (fable_regression_check.py 内)
files = sorted(REPORT_DIR.glob('第*章-*.html'))
# glob 支持 '第01章' 到 '第99章', 旧脚本只支持 '第1章' 到 '第9章'
# ch10+ 必须用 2 位 glob 模式
```

## 故障排查

| 失败项 | 修复 |
|--------|------|
| Files: 27 / 28 | 看哪个文件 0 critical, 单独跑那章的 5 项自检 |
| glob 0 文件 | 检查 REPORT_DIR 路径, 检查章节文件名格式 |
| 中文乱码 | `python -X utf8 ...` |