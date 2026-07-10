---
name: fable-write-sop
description: "WellInsight 寓言单章 v1 渲染标准操作流程(SOP) — 12 步全链路:3 必跑(写前 grep)+ 4 必守(写时约束)+ 5 必改(ch11 故事逻辑+语序反馈整改);第12章起所有新章节通用"
metadata:
  node_type: memory
  type: reference
  originSessionId: 35d6f6f6-8b6b-4cb5-9d6f-a385dab6bca6
---

# WellInsight 寓言 v1 渲染 12 步 SOP(2026-06-29 沉淀)

## Why: 为什么需要 12 步 SOP

寓言单章渲染从第 02-11 章 9 章经验沉淀下来, 总结出 **3 必跑 + 4 必守 + 5 必改** 12 步标准流程。**第12章 v1 一次写就 0 修复, 28 文件回归全过, 验证 12 步 SOP 有效**。

**Why 12 步不是 1 步**:
- **3 必跑** 是写脚本前查底, 防前章 bug 带到新章
- **4 必守** 是写脚本时约束, 防英文/quiz-strong/correct 暴露答案/coverage 三列
- **5 必改** 是写故事骨架时改进, 防 ch11 那种"故事逻辑+语序混乱"反馈

**How to apply**: 第13章及以后所有新章节 **先 grep 3 必跑 → 写骨架用 5 必改 → 写脚本用 4 必守 → 跑渲染 → 跑回归 → 沉淀 memory**。

---

## 一、3 必跑(写脚本前 · 防止前章 bug 带到新章)

### 必跑 1: 查 `.correct` 类
```bash
grep -c 'class="correct"' reports/第<NUM>章-*.html
```
**应为 0**。如果 > 0, 看哪一章漏了 `.correct` 修复(可能要从前章复制 .correct class 名)。

### 必跑 2: 查 `text-align: justify`
```bash
grep -cE 'text-align:.*justify' reports/第<NUM>章-*.html
```
**应为 0**。v5 规范要求 `text-align: left`, 不用 `justify`(justify 在中文长行会拉大间距, 不自然)。

### 必跑 3: 查 `**...**` markdown 加粗残留
```bash
grep -cE '\*\*[^*]+\*\*' reports/第<NUM>章-*.html
```
**应为 0**。fable 渲染全部用 `<strong>...</strong>`, 不能用 `**...**` markdown 语法。如果发现残留, 全部替换成 `<strong>`。

**Why**: 这 3 类 bug 都在前几章发生过(第 06/07/08 章都有 .correct 修复记录;第 09 章有 2 轮英文泄漏修复;第 10 章有过 quiz-strong 反馈)。跑前先查, 防前章 bug 带到新章。

---

## 二、4 必守(写脚本时 · 防止 v5 规范破坏)

### 必守 1: 命名决策段放在脚本开头
```python
# ===== 命名决策段(强制) =====
CHAPTER_NUM = "12"
CHAPTER_NAME = "训练与对齐"
REPORT_DIR = Path(r"reports")
OUT = REPORT_DIR / f"第{CHAPTER_NUM}章-{CHAPTER_NAME}-v1.html"
print(f'→ 写入目标: {OUT.name}')
```

**Why**: 命名决策段是"为什么写"的元信息, 写脚本时第一眼看到, 不会写错文件名/章节号。

### 必守 2: quiz 选项不加 `<strong>`
```python
# ❌ 错误: 选项里加 <strong> 让用户一眼看出"正确答案"
<ul class="quiz-options">
  <li><strong>A. 对的</strong></li>
  <li>B. 错的</li>
</ul>

# ✅ 正确: 选项不加粗, 正确答案藏在 <details> 里
<ul class="quiz-options">
  <li>A. 对的</li>
  <li>B. 错的</li>
</ul>
<details class="quiz-answer">
  <summary>答案解析</summary>
  <p><strong>正确答案:A</strong></p>
</details>
```

**Why**: 用户反馈 "题目里能直接看出答案" 会破坏测试价值。

### 必守 3: quiz 解析里的英文概念先在 annotation 写, 再复制时改朝代化
```python
# ❌ 错误: 解析里直接写英文术语
<p>正确答案: A · Pre-training 让模型学好</p>

# ✅ 正确: 解析里写成朝代化措辞(annotation 里可以有英文)
<p>正确答案: A · 习(广读档, 学正)</p>
```

**Why**: 第 09 章 2 轮修复经验, 解析里复制 annotation 措辞时, 英文必须改朝代化, 否则正文会泄漏英文。

### 必守 4: coverage 表格三列分布(朝代叙事 / 朝代细节 / 见 annotation)
```html
<!-- ❌ 错误: 第 3 列直接写英文 -->
<td>Pre-training / SFT</td>

<!-- ✅ 正确: 第 3 列写"见 annotation" -->
<td>见 annotation</td>
```

**Why**: coverage 表是给读者看的"概念地图", 不是给工程师看的对照表。第 3 列写英文会让读者卡住。

---

## 三、5 必改(写故事骨架时 · 解决 ch11 故事逻辑+语序混乱反馈)

### 必改 1: 每幕开头 1 句主旨句(避免散点状)
```markdown
# ❌ 错误(ch11): 没有主旨句, 一上来就堆细节
"三月初三早朝。礼部侍郎沈一石刚把'评估派'的联名奏本呈上, 陈守一先接话: ..."

# ✅ 正确(ch12): 主旨句 + 再展开
**主旨: 灵机天生有灵性, 苦训伤灵性 —— 这是韩守拙 40 年训导的真心。**

"九月初二早朝。国子监太学训导韩守拙把'训练派'的联名奏本呈上, 陈守一先接话: ..."
```

**Why**: 主旨句 = 这一幕"一句话能讲清什么", 写完一幕先看主旨句, 不清就重写。

### 必改 2: M1 反派完整退场 → M2-M4 在场不抢戏 → M5 再登场反转
```markdown
# ❌ 错误(ch11): 反派 M1 退场后, M5 突然出现 + 二次升级混在同段
"... 门外传来一封急奏 —— 朝廷派礼部试院'评估派'主事沈一石前来'考校'。
沈一石是礼部侍郎, 他在'评估'上意见更激进 —— 他主张'不光评估不必, 连评估的纸契也不必有'。"

# ✅ 正确(ch12): M1 韩守拙完整退场, M5 重新登场(独立节点)
"M1: ... 韩守拙长叹退下, 边走边说'臣的'训练派'也是为灵机好'"
"M2-M4: ... 韩守拙在场, 但只是'立训习三步'的匠人, 不抢戏"
"M5: '十月十五早朝。韩守拙又上一奏: 训习耗人工, 灵机天生有灵性, 何必苦训。'"
```

**Why**: 反派退场后再登场, 反转才有"被打脸"的张力; 混在同段会让读者分不清"这是同一个人还是新角色"。

### 必改 3: 朝代白话主谓宾(避免翻译腔)
```markdown
# ❌ 错误(翻译腔): "在做 X 的时候 Y 就会 Z"
"灵机在接话的时候, 如果按户部侍郎的口气补位, 灵机就会跟着学"
"灵机在训习的时候, 如果训导给的赏罚分不清, 灵机就不知道改方向"

# ✅ 正确(主谓宾): "X 时 Y 做 Z"
"户部灵机接话, 学户部侍郎的口气, 把'5 万石'补成'30 万石'"
"训导给的赏罚分, 灵机按簿改方向, 越改越正"
```

**Why**: 翻译腔(英语长定语 + 从句)读起来累, 读者要"翻译回中文"才懂; 朝代白话主谓宾让读者"一秒懂"。

### 必改 4: 对白自然(避免"臣不省 A, 省 B"长跳)
```markdown
# ❌ 错误(ch11): 对白用"省 A 省 B"长跳, 逻辑跳
"臣的'评估派'也是为匠人好 —— 臣不省试院的考核, 省接话灵机的清静"

# ✅ 正确(ch12): 对白用比喻, 不绕
"灵机是有灵性的灵物 —— 像太学的学子, 马越打越笨, 马不训反倒是好马"
```

**Why**: 长跳对白读者要"猜", 比喻对白读者"懂"。

### 必改 5: M0→M5 因果链严丝合缝(无"灵机忽然懂了")
```markdown
# ❌ 错误: 灵机忽然懂了
"户部灵机接话 → 评估四评 90 分 → 灵机就懂了, 不再补位"
"户部灵机接话 → 训导打分 → 灵机就懂了, 不再删位"

# ✅ 正确: 每步都有"为什么"
"户部灵机接话 → 评估官指出扣分点(听评 70) → 灵机补'回音' → 第二轮听评 80"
"户部灵机接话 → 训导按扣分点改字 → 灵机改正字 → 第二轮听评 90"
```

**Why**: 寓言不是"灵机自己会了", 是"训导一步步教灵机会了"。每一步都要有"为什么"。

---

## 四、SOP 12 步全流程

```python
# ============================
# Step 0: 写骨架前查 3 必跑
# ============================
# grep -c 'class="correct"' reports/第<前NUM>章-*.html
# grep -cE 'text-align:.*justify' reports/第<前NUM>章-*.html
# grep -cE '\*\*[^*]+\*\*' reports/第<前NUM>章-*.html
# 三个都应为 0

# ============================
# Step 1: 写故事骨架(用 5 必改)
# ============================
# reports/第<NUM>章-<主题>-v1-story-skeleton.md
# 必改 1: 每幕开头 1 句主旨句
# 必改 2: M1 反派完整退场 → M2-M4 在场不抢戏 → M5 再登场
# 必改 3: 朝代白话主谓宾(避免翻译腔)
# 必改 4: 对白自然(用比喻不绕)
# 必改 5: M0→M5 因果链严丝合缝

# ============================
# Step 2: 写渲染脚本(用 4 必守)
# ============================
# scripts/rewrite_ch<NUM>_v1.py
# 必守 1: 命名决策段放在脚本开头
# 必守 2: quiz 选项不加 <strong>
# 必守 3: quiz 解析朝代化(annotation 里可以有英文)
# 必守 4: coverage 表第 3 列写"见 annotation"

# ============================
# Step 3: 跑渲染
# ============================
# python -X utf8 scripts/rewrite_ch<NUM>_v1.py
# 自检: 0 残留 / 0 .correct / 0 quiz-strong / 0 英文泄漏

# ============================
# Step 4: 跑回归
# ============================
# python -X utf8 scripts/fable_regression_check.py
# 应: 全部通过(N 个文件, N = 2 * 已完成章数)

# ============================
# Step 5: 沉淀 memory
# ============================
# memory/chapter<NUM>-<主题>-fable-rendered.md
# 12 节 + v5 规范应用 + 自检通过 + 0 事故 + How to apply for 第<NUM+1>章

# ============================
# Step 6: 同步 3 处 + mem0 L2
# ============================
# memory/MEMORY.md 添加新条目
# memory/wellinsight-protagonist-age-ladder.md 添加年龄
# memory/fable-antagonist-humanity-pattern.md 添加反派
# mem0: m.add(text, user_id='yolanda', agent_id='clove')
```

---

## 五、SOP 验证记录(2026-06-29)

| 章节 | 应用 SOP | 渲染结果 | 修复次数 |
|------|---------|---------|---------|
| 第 11 章 | 3 必跑 + 4 必守(5 必改未应用) | 0 修复,但用户反馈"故事逻辑+语序混乱" | 0(但 1 条用户反馈) |
| 第 12 章 | **3 必跑 + 4 必守 + 5 必改 全部应用** | **0 修复, 28 文件全过** | **0(0 用户反馈)** |
| 第 13+ 章 | 12 步 SOP 全套 | 待验证 | 待验证 |

**Why 第 12 章 0 修复**: 12 步 SOP 把 ch11 反馈的 5 类问题 + v5 规范的 4 类问题 + 前章 bug 复发的 3 类问题全部覆盖, 一次写就 0 事故。

---

## 六、How to apply for 第13+ 章

- **Step 0**: 必跑 3 项 grep, 防前章 bug 带到新章
- **Step 1**: 写骨架用 5 必改, 防 ch11 那类"故事逻辑+语序"反馈
- **Step 2**: 写脚本用 4 必守, 防 v5 规范破坏
- **Step 3-4**: 渲染 + 回归, 验证 0 事故
- **Step 5-6**: 沉淀 + 同步, 闭环

**Why**: 12 步 SOP 跨章复用, 12 章用 = 12 次验证 = SOP 越用越准。后续章节无需重写 SOP, 直接套 12 步即可。

**Link**: 关联 [[fable-ch11-feedback-correction-pattern]] (5 整改详细说明) / [[chapter12-rl-alignment-fable-rendered]] (12 步 SOP 首次应用)/ [[fable-v1-english-leakage-traps]] (英文泄漏)/ [[wellinsight-protagonist-age-ladder]] (年龄阶梯) / [[fable-antagonist-humanity-pattern]] (反派转友) / [[karpathy-claudemd-work-discipline]] (通用纪律) / [[sage-should-apply-ae-pattern]] (跨 agent 应用)
