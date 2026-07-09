**[English](./README.md)** | [简体中文](./README.zh-CN.md)

---ttt

# Allegorize Textbook Content

> A complete workflow that converts technical textbooks and knowledge bases into learning stories for absolute beginners. The output eliminates circular jargon — it never defines a term using other specialized vocabulary.

## What this is

A collection of **12 allegorical chapters** that turn abstract, jargon-heavy AI / agent material into a coherent Ming-Dynasty story about a prince growing up. Each chapter runs 600-1000 lines. The protagonist progresses from a 14-year-old page boy to a 23-year-old crown prince, rotating through six fictional imperial institutions (the Astronomical Bureau, the Hanlin Academy, the Office of Memorials, the Tributary Reception Court, the Ministry of Rites, the Imperial Academy).

**Core methodology**: the first pass explains using concepts the audience already knows; the second pass uses the first-pass explanation to explain new concepts. No "A is explained by A" anywhere.

## Chapter list

Read in order. Each chapter is a self-contained HTML, readable offline.

| # | Chapter | Topic | Allegorical setting |
|---|---------|-------|---------------------|
| 01 | [What is an Agent](第01章-初识智能体.html) | Agent definition | The prince's first tutor |
| 02 | [History of Agents](第02章-智能体发展史-v3.html) | Symbolism to LLMs | Three-school debate at the Daoist Academy |
| 03 | [LLM Foundations](第03章-大语言模型基础-v4.html) | Transformer, attention, training | Type-cutting and book-carving at the Hanlin Academy |
| 04 | [Classic Agent Patterns](第04章-智能体经典范式构建-v1.html) | ReAct, Reflexion, plan-execute | Memorial flow through the Six Ministries |
| 05 | [Low-Code Platform](第05章-低代码平台搭建-v1.html) | Platform building | Jiangnan Weaving Bureau reform with four looms |
| 06 | [Framework Development](第06章-框架开发实践-v1.html) | Framework design, decoupling | Joint investigation of the four capital ministries |
| 07 | [Build an Agent Framework from Scratch](第07章-从零开始造一个智能体框架.html) | Full framework implementation | The Astronomical Bureau builds HelloAgents |
| 08 | [Memory and Retrieval](第08章-记忆与检索-v2.html) | RAG, vector DB, memory tiers | Ledger and archive machines in the Hanlin Academy |
| 09 | [Context Engineering](第09章-上下文工程-v1.html) | Context orchestration, compression, routing | Memorial-orchestrating machine in the Office of Memorials |
| 10 | [Agent Communication Protocols](第10章-智能体通信协议-v1.html) | MCP, agent-to-agent | "Connector" machine in the Tributary Reception Court |
| 11 | [Evaluation and Iteration](第11章-评估与迭代-v1.html) | Evaluation loops, metric design | "Evaluation-cycle" machine in the Ministry of Rites |
| 12 | [Training and Alignment](第12章-训练与对齐-v1.html) | RLHF, DPO, reward modeling | "Training" machine in the Imperial Academy |

## Allegorical methodology (for rewriters)

If you want to apply the same workflow to other textbooks, three rules:

1. **No circular definitions** — never explain "attention mechanism" with "Q/K/V matrices"; use "the emperor sorting memorials into three piles"
2. **Cross-chapter protagonist growth** — same protagonist across chapters (14 → 23), giving continuity rather than re-learning
3. **Antagonists with valid positions** — every villain is a principled opposition, refuted by evidence not by monologue

## Characters

**The Prince**: enters the Astronomical Bureau at 14 as a page boy, rises to 23 as a senior trainee. Grows one year per chapter, rotating through 5 institutions (Hanlin / Memorials / Tributary / Rites / Imperial Academy).

**Prince Liang**: the pro-Western faction. Appears in 7/8/9/10 with four reversals (dismissive → curious → borrowing → convinced). Embodiment of the "villain with valid position" rule.

## Bundled package

- [`fable-skills.zip`](fable-skills.zip) — fully self-contained reproduction package (12-step SOP + regression scripts + checklists + environment guide). Any agent can copy, change 4 names, and render new chapters

## How to read

**Zero-background path** (for complete outsiders): 1 → 2 → 3 → 7 → 8 → 12. Follow the prince from novice to senior trainee.

**Practitioner path** (for those who already know AI): skip-read 4 / 7 / 8 / 10 / 12. Focus on framework design, self-built framework, RAG, MCP, training.

**Authoring path** (for those who want to apply this methodology to other textbooks): start with `fable-skills.zip` → `01-sop/fable-write-sop.md` (12-step SOP), then read chapters 2 and 7 (the v1→v2 fix case studies).

## License

- HTML content: **CC BY-NC-SA 4.0** (attribution, non-commercial, share-alike)
- Code/scripts inside `fable-skills.zip`: **MIT**

## Origin

- Source textbook: datawhalechina/hello-agents
- Allegorization: WellInsight team, from 2026-06
- Last update of bundled package: 2026-06-29
