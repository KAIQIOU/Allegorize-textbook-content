# 写脚本前 · 3 必跑清单

> **目的**: 防止前章 bug 带到新章。**写脚本前** 在 `reports/` 目录跑这 3 个 grep。

## 必跑 1: 查 `.correct` 类

```bash
grep -c 'class="correct"' reports/第<前NUM>章-*.html
```

**应为 0**。如果 > 0:
- 说明前章有 quiz `.correct` class 名(选项直接暴露答案)
- 看哪一章漏了 `.correct` 修复
- 把前章脚本里 `class="correct"` 改成 `class="quiz-answer"`(藏在 `<details>` 里)

## 必跑 2: 查 `text-align: justify`

```bash
grep -cE 'text-align:.*justify' reports/第<前NUM>章-*.html
```

**应为 0**。v5 规范要求 `text-align: left`。
- justify 在中文长行会拉大间距,不自然
- 全部 `justify` 改 `left`

## 必跑 3: 查 `**...**` markdown 加粗残留

```bash
grep -cE '\*\*[^*]+\*\*' reports/第<前NUM>章-*.html
```

**应为 0**。fable 渲染全部用 `<strong>...</strong>`, 不能用 markdown `**`。
- 如果发现残留, Python 批量替换:
  ```python
  import re
  html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
  ```

## Why 这 3 项

| Bug | 历史出现章节 | 教训 |
|-----|------------|------|
| `.correct` class | ch06/07/08 | quiz 选项暴露答案, 用户能直接看出 |
| `text-align: justify` | ch05/06 | 中文长行间距过大, 不自然 |
| `**残留` | ch05/06/10 | markdown 语法在 HTML 里不渲染 |

**3 项全 0 才开始写新章脚本**。

---

## 跨章验证记录

| 章节 | .correct | justify | **残留 | 是否阻塞 |
|------|---------|---------|-------|---------|
| ch11 | 0 ✓ | 0 ✓ | 0 ✓ | 否 |
| ch12 | 0 ✓ | 0 ✓ | 0 ✓ | 否 |
| ch13+ | 待验证 | 待验证 | 待验证 | 0 阻塞才开写 |