# 写脚本后 · 5 项自检清单

> **目的**: 渲染完成后,**跑这 5 项 grep**, 全部 0 才算 v1 渲染成功。

## 自检 1: `.correct` 类

```bash
grep -c 'class="correct"' reports/第<NUM>章-*-v1.html
```

**应为 0**。如果 > 0: 看哪个 quiz 漏改。

## 自检 2: `text-align: justify`

```bash
grep -cE 'text-align:.*justify' reports/第<NUM>章-*-v1.html
```

**应为 0**。

## 自检 3: `**...**` markdown 残留

```bash
grep -cE '\*\*[^*]+\*\*' reports/第<NUM>章-*-v1.html
```

**应为 0**。

## 自检 4: quiz-options 内 `<strong>`

```bash
grep -cE '<ul class="quiz-options">.*<strong>' reports/第<NUM>章-*-v1.html
```

**应为 0**。quiz 选项不能加粗(否则一眼看出正确答案)。

## 自检 5: 正文英文术语泄漏

```bash
grep -ciE '\b(RL|Training|Alignment|Reward Model|Fine-tuning|PPO|DPO|SFT|RLAIF|RLHF|Constitutional AI|Memory|RAG|MCP|Agent)\b' reports/第<NUM>章-*-v1.html
```

**允许 ≤ 6**(全部在 `<aside class="annotation">` 块内,正文必须 0)。
- annotation 内可以保留英文(读者查档用)
- quiz 解析 / coverage 表 / 正文 → 必须朝代化

### 自检 5 详细: 英文泄漏排查脚本

```python
import re
html = open(f'reports/第{NUM}章-...v1.html').read()

# 去掉 annotation 块(允许英文)
no_anno = re.sub(r'<aside class="annotation">.*?</aside>', '', html, flags=re.S)
# 去掉 style/script
no_anno = re.sub(r'<(style|script).*?</\1>', '', no_anno, flags=re.S)

# 查英文术语
TERMS = ['RL', 'Training', 'Alignment', 'Reward Model', 'Fine-tuning',
         'PPO', 'DPO', 'SFT', 'RLAIF', 'RLHF', 'Constitutional AI',
         'Memory', 'RAG', 'MCP', 'Agent', 'LLM', 'Prompt', 'Tokenizer']
for term in TERMS:
    if re.search(rf'\b{re.escape(term)}\b', no_anno, re.I):
        print(f'❌ 英文泄漏: {term}')
print('✓ 全部朝代化' if all checks pass else '⚠️ 需修复')
```

---

## 5 项全 0 才算 v1 成功

```bash
# 一键跑完
python -X utf8 -c "
import re
f = r'reports/第<NUM>章-...v1.html'
html = open(f, encoding='utf-8').read()
checks = {
    '.correct': len(re.findall(r'class=\"correct\"', html)),
    'justify': len(re.findall(r'text-align:.*justify', html)),
    '**残留': len(re.findall(r'\*\*[^*]+\*\*', html)),
    'quiz-strong': len(re.findall(r'<ul class=\"quiz-options\">.*<strong>', html, re.S)),
    '英文泄漏': len(re.findall(r'\bRL\b|\bTraining\b|\bAlignment\b', html)) - 6,
}
for k, v in checks.items():
    print(f'{k}: {v} {\"✓\" if v == 0 else \"❌\"}')"
```