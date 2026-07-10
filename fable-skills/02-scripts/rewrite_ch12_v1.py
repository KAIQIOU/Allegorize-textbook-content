"""
第12章寓言 v1 渲染脚本 · 国子监训习(彻底朝代化)
═══════════════════════════════════════════════════════════
命名决策(强制, v5 规范 + 解决 ch11 反馈)
═══════════════════════════════════════════════════════════
任务:写第12章"训练与对齐(RL & Alignment)"到 HTML,
   沿用 v5 全部规范 + 重点解决 ch11"故事逻辑和语序混乱"反馈

   规范 1: quiz 选项不加粗
   规范 2: text-align left(不变宽)
   规范 3: 正文 0 英文(全部进 annotation)
   规范 4: quiz 解析从朝代化措辞重新写,严禁从 annotation 复制
   规范 5: coverage 表第 3 列默认"见 annotation",不写英文
   规范 6: 主角升级到 23 岁,新场景"国子监·太学"
   规范 7: 反派"训练派"主张"灵机天生有灵性,苦训伤灵性",反转母题 10 连击

   【ch11 反馈整改】
   整改 1: 每幕开头 1 句主旨句(避免散点状)
   整改 2: M1 反派完整退场 → M2-M4 在场不抢戏 → M5 再登场反转
   整改 3: 朝代白话主谓宾(避免翻译腔,避免长定语)
   整改 4: 对白自然(避免"臣不省 A,省 B"长跳)
   整改 5: M0→M5 因果链严丝合缝,无"灵机忽然懂了"

沿用 v2 模板: 命名决策段 + 朝代术语对照表 + 自测题不暴露答案 + 自动化回归
═══════════════════════════════════════════════════════════
"""
from pathlib import Path
import shutil
import re
import os

# ===== 命名决策段(强制) =====
CHAPTER_NUM = "12"
CHAPTER_NAME = "训练与对齐"
REPORT_DIR = Path(os.environ.get('FABLE_REPORT_DIR', r"reports"))

OUT = REPORT_DIR / f"第{CHAPTER_NUM}章-{CHAPTER_NAME}-v1.html"
print(f'→ 写入目标: {OUT.name}')

# ===== CSS 头(沿用 v2 模板:text-align: left) =====
CSS_HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第12章 · 训练与对齐 · 学习材料</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#F2EDE6;--bg-card:#FAF7F2;--bg-elevated:#FFFCF7;--bg-deep:#E8DFD3;--text-primary:#3D3833;--text-secondary:#6B6157;--text-muted:#998E81;--accent-sage:#8B9D83;--accent-sage-soft:#D8E2D2;--accent-sage-faint:#ECF1E8;--accent-terracotta:#C49B8E;--accent-terracotta-soft:#E6D2C8;--accent-blue:#8A9AA8;--accent-blue-soft:#C8D2DA;--accent-amber:#C9A878;--accent-amber-soft:#E8D7B7;--accent-mauve:#A89098;--accent-mauve-soft:#DCCCD0;--border:#D9D2C7;--border-light:#E8E0D3;--shadow:0 2px 8px rgba(61,56,51,.06), 0 1px 2px rgba(61,56,51,.04);--shadow-lg:0 8px 24px rgba(61,56,51,.10), 0 2px 6px rgba(61,56,51,.05);}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;scroll-padding-top:80px}
body{font-family:'Noto Sans SC','PingFang SC','Microsoft YaHei','Hiragino Sans GB',sans-serif;background:var(--bg);color:var(--text-primary);line-height:1.78;font-size:16px;font-weight:400;-webkit-font-smoothing:antialiased;letter-spacing:.01em;}
.container{max-width:920px;margin:0 auto;padding:48px 28px 96px}
.sticky-toc{position:fixed;top:24px;right:24px;width:240px;background:var(--bg-elevated);border:1px solid var(--border);border-radius:8px;padding:14px 16px;box-shadow:var(--shadow);font-size:13px;z-index:50;max-height:calc(100vh - 48px);overflow-y:auto;}
.sticky-toc-title{font-weight:600;color:var(--text-secondary);margin-bottom:8px;font-size:12px;letter-spacing:.5px;display:flex;align-items:center;gap:6px;}
.sticky-toc ol{list-style:none;counter-reset:toc;padding:0}
.sticky-toc li{counter-increment:toc;margin:4px 0}
.sticky-toc a{color:var(--text-secondary);text-decoration:none;display:block;padding:4px 0 4px 8px;margin-left:6px;border-left:2px solid transparent;font-size:12.5px;font-weight:500;transition:all .2s;}
.sticky-toc a:hover{color:var(--accent-sage);border-left-color:var(--accent-sage)}
.sticky-toc a::before{content:counter(toc) ".";color:var(--text-muted);font-family:'JetBrains Mono',monospace;font-size:11px;margin-right:4px}
.hero{background:linear-gradient(135deg,#FAF7F2 0%,#F2EDE6 100%);border:1px solid var(--border);border-radius:12px;padding:48px 40px 40px;margin-bottom:48px;position:relative;overflow:hidden;}
.hero::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--accent-sage) 0%,var(--accent-terracotta) 33%,var(--accent-blue) 66%,var(--accent-amber) 100%);}
.hero-meta{display:flex;align-items:center;gap:12px;font-size:12px;color:var(--text-muted);margin-bottom:16px;font-weight:500;letter-spacing:.5px;}
.hero-meta-dot{width:4px;height:4px;background:var(--text-muted);border-radius:50%}
.hero h1{font-size:46px;font-weight:700;line-height:1.15;color:var(--text-primary);margin-bottom:10px;letter-spacing:-1px;}
.hero-subtitle{font-size:16px;color:var(--text-secondary);margin-bottom:22px;font-weight:500;}
.hero-fable{display:inline-block;padding:2px 10px;margin-right:4px;background:var(--accent-sage-soft);color:var(--accent-sage);border-radius:12px;font-size:14px;font-weight:600;letter-spacing:.5px;}
.hero-desc{font-size:14.5px;color:var(--text-secondary);margin-bottom:24px;line-height:1.7;font-weight:400;}
.hero-source{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;color:var(--text-muted);background:var(--bg-card);padding:6px 12px;border-radius:20px;border:1px solid var(--border-light);font-weight:500;}
section{margin-bottom:56px;scroll-margin-top:80px}
.chapter-tag{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;color:var(--accent-sage);background:var(--accent-sage-soft);padding:4px 12px;border-radius:12px;margin-bottom:14px;letter-spacing:1px;}
h2{font-size:28px;font-weight:700;color:var(--text-primary);margin-bottom:14px;letter-spacing:-.3px;display:flex;align-items:baseline;gap:12px;line-height:1.3;}
h2 .num{font-family:'JetBrains Mono',monospace;font-size:18px;color:var(--accent-terracotta);font-weight:500}
h2-hook{display:block;font-size:15px;font-weight:500;color:var(--text-secondary);margin-top:8px;margin-bottom:24px;padding:12px 16px;background:var(--bg-card);border-left:3px solid var(--accent-amber);border-radius:0 6px 6px 0;font-style:italic;}
h3{font-size:19px;font-weight:600;color:var(--text-primary);margin:24px 0 10px;padding-left:14px;border-left:3px solid var(--accent-amber);letter-spacing:-.2px;}
h4{font-size:16px;font-weight:600;color:var(--accent-sage);margin:20px 0 10px}
p{margin-bottom:14px;color:var(--text-primary);text-align:left;font-weight:400}
strong{color:var(--text-primary);font-weight:600}
em{color:var(--text-secondary);font-style:normal;font-weight:600}
.lead{font-size:17px;color:var(--text-secondary);padding:18px 22px;background:var(--bg-card);border-left:3px solid var(--accent-terracotta);border-radius:0 6px 6px 0;margin-bottom:28px;font-weight:500;line-height:1.85;}
.callout{background:var(--bg-card);border:1px solid var(--border-light);border-radius:8px;padding:18px 22px;margin:20px 0;box-shadow:var(--shadow);}
.callout-title{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:var(--accent-sage);margin-bottom:10px;text-transform:uppercase;letter-spacing:.5px;}
.pullquote{background:linear-gradient(135deg,var(--accent-amber-soft) 0%,var(--bg-card) 100%);border:1px solid var(--accent-amber-soft);border-radius:8px;padding:22px 26px;margin:24px 0;font-size:16.5px;font-weight:500;color:var(--text-primary);position:relative;}
.pullquote::before{content:"\\201C";position:absolute;top:-6px;left:16px;font-size:48px;color:var(--accent-amber);font-family:Georgia,serif;line-height:1;font-weight:700;}
.stats-card{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:24px 0 8px}
.stat-cell{background:var(--bg-elevated);border:1px solid var(--border-light);border-radius:10px;padding:18px 16px;text-align:center;box-shadow:var(--shadow)}
.stat-num{font-family:'JetBrains Mono',monospace;font-size:32px;font-weight:700;color:var(--accent-terracotta);line-height:1.1;margin-bottom:4px}
.stat-label{font-size:13px;color:var(--text-secondary);font-weight:500;line-height:1.45}
.stat-cell.victory{border-top:3px solid var(--accent-sage)}
.stat-cell.defeat{border-top:3px solid var(--accent-mauve)}
.stat-num.green{color:var(--accent-sage)}
.stat-num.red{color:var(--accent-mauve)}
.doctors-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:28px 0 8px}
.doctor-card{background:var(--bg-elevated);border:1px solid var(--border-light);border-radius:10px;padding:18px 18px 16px;box-shadow:var(--shadow);position:relative;transition:transform .2s;}
.doctor-card:hover{transform:translateY(-2px);box-shadow:var(--shadow-lg)}
.doctor-card.role-1{border-top:3px solid var(--accent-sage)}
.doctor-card.role-2{border-top:3px solid var(--accent-terracotta)}
.doctor-card.role-3{border-top:3px solid var(--accent-blue)}
.doctor-card.role-4{border-top:3px solid var(--accent-amber)}
.doctor-name{font-size:19px;font-weight:700;color:var(--text-primary);margin-bottom:2px;display:flex;align-items:center;gap:8px;letter-spacing:-.2px;}
.doctor-age{font-size:12px;font-weight:500;color:var(--text-muted);margin-bottom:10px}
.doctor-quote{font-size:13px;color:var(--text-secondary);font-weight:500;margin-bottom:12px;line-height:1.6;padding-bottom:12px;border-bottom:1px dashed var(--border-light)}
.doctor-behaviors{list-style:none;padding:0;margin:0;font-size:12.5px;color:var(--text-secondary);line-height:1.7}
.doctor-behaviors li{padding:3px 0 3px 14px;position:relative}
.doctor-behaviors li::before{content:"";position:absolute;left:2px;top:11px;width:5px;height:5px;border-radius:50%;background:var(--accent-amber)}
.annotation{background:linear-gradient(135deg,var(--accent-sage-faint) 0%,var(--bg-card) 100%);border:1px solid var(--accent-sage-soft);border-left:3px solid var(--accent-sage);border-radius:0 8px 8px 0;padding:18px 22px;margin:32px 0 8px;position:relative;}
.annotation-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;padding-bottom:10px;border-bottom:1px dashed var(--accent-sage-soft);}
.annotation-tag{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;color:var(--accent-sage);text-transform:uppercase;letter-spacing:1.5px;}
.annotation-hint{font-size:12px;color:var(--text-muted);font-weight:500;font-style:italic}
.annotation dl{display:grid;grid-template-columns:minmax(140px,max-content) 1fr;gap:8px 18px;margin:0}
.annotation dt{font-weight:600;color:var(--text-primary);font-size:13px;line-height:1.65}
.annotation dd{margin:0;color:var(--text-secondary);font-size:13px;line-height:1.65}
.annotation dd .who{color:var(--accent-terracotta);font-weight:700;margin-right:4px}
.annotation dd .what{color:var(--text-secondary)}
.dialog{background:var(--bg-deep);border-radius:6px;padding:14px 18px;margin:14px 0;font-size:14.5px;color:var(--text-primary);border-left:3px solid var(--accent-amber);}
.dialog-speaker{font-weight:700;color:var(--accent-terracotta)}
.table-wrap{margin:20px 0;background:var(--bg-card);border:1px solid var(--border-light);border-radius:8px;overflow:hidden;box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse;font-size:14px}
thead{background:var(--bg-deep)}
th{padding:12px 16px;text-align:left;font-weight:600;color:var(--text-primary);font-size:13px;letter-spacing:.3px;border-bottom:1px solid var(--border)}
td{padding:12px 16px;border-bottom:1px solid var(--border-light);color:var(--text-secondary);vertical-align:top}
tbody tr:last-child td{border-bottom:none}
tbody tr:nth-child(even){background:rgba(232,223,211,.3)}
.coverage{background:var(--bg-elevated);border:1px solid var(--border);border-radius:10px;padding:24px 28px;margin:32px 0}
.coverage-title{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:700;color:var(--text-primary);margin-bottom:16px;padding-bottom:12px;border-bottom:2px dashed var(--border)}
.quiz-list{display:flex;flex-direction:column;gap:14px;margin:18px 0}
.quiz-card{background:var(--bg-elevated);border:1px solid var(--border-light);border-radius:10px;padding:16px 20px;box-shadow:var(--shadow);border-left:4px solid var(--accent-sage)}
.quiz-card-head{display:flex;align-items:baseline;gap:10px;margin-bottom:10px;flex-wrap:wrap}
.quiz-num{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:var(--accent-sage);background:var(--accent-sage-soft);padding:2px 8px;border-radius:6px}
.quiz-q{margin:0 0 8px;font-size:14.5px;color:var(--text-primary);font-weight:500;line-height:1.7}
.quiz-options{list-style:none;padding:0;margin:0 0 6px;display:flex;flex-direction:column;gap:3px}
.quiz-options li{padding:5px 10px;font-size:13.5px;color:var(--text-secondary);line-height:1.6;border-radius:5px;background:var(--bg-card);border:1px solid var(--border-light)}
.quiz-answer{margin-top:10px;background:var(--bg-card);border-radius:6px;padding:8px 12px;font-size:13px;color:var(--text-secondary);border:1px dashed var(--border)}
.quiz-answer summary{cursor:pointer;font-weight:600;color:var(--accent-sage);font-size:13px;padding:2px 0;list-style:none}
.quiz-answer summary::before{content:"▶ "}
.quiz-answer[open] summary{margin-bottom:6px}
.summary-box{background:linear-gradient(135deg,var(--accent-sage-soft) 0%,var(--bg-card) 50%,var(--accent-amber-soft) 100%);border:1px solid var(--accent-sage);border-radius:12px;padding:32px 36px;margin:40px 0;position:relative;}
.summary-box-title{font-size:13px;font-weight:700;color:var(--accent-sage);text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}
.summary-text{font-size:18px;color:var(--text-primary);line-height:1.85;font-weight:500}
.footer{margin-top:60px;padding-top:24px;border-top:1px solid var(--border);font-size:12.5px;color:var(--text-muted);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;font-weight:500}
.footer-link{color:var(--accent-sage);text-decoration:none;font-weight:600}
.back-top{position:fixed;bottom:24px;right:24px;width:40px;height:40px;background:var(--bg-elevated);border:1px solid var(--border);border-radius:50%;display:flex;align-items:center;justify-content:justify-content:center;cursor:pointer;box-shadow:var(--shadow);transition:all .2s;z-index:40}
.icon{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;display:inline-block;vertical-align:middle}
code{background:var(--bg-deep);padding:2px 7px;border-radius:3px;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--accent-terracotta);font-weight:500}
@media (max-width:1100px){.sticky-toc{display:none}}
@media (max-width:768px){.container{padding:24px 16px 60px}.hero{padding:32px 20px}.hero h1{font-size:32px}h2{font-size:22px}.doctors-grid,.stats-card{grid-template-columns:1fr}}
</style>
</head>
<body>
'''

# ===== TOC =====
TOC = '''
<nav class="sticky-toc" aria-label="目录">
  <div class="sticky-toc-title">
    <svg class="icon" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    目录
  </div>
  <ol>
    <li><a href="#ch0">开篇 · 评得再好,灵机不改</a></li>
    <li><a href="#ch1">第一幕 · "训练派"登场</a></li>
    <li><a href="#ch2">第二幕 · 太学·训习院挂牌</a></li>
    <li><a href="#ch3">第三幕 · 韩守拙立"训习三步"</a></li>
    <li><a href="#ch4">第四幕 · 赏罚单</a></li>
    <li><a href="#ch5">第五幕 · 韩守拙"考校"再成"拜师"</a></li>
    <li><a href="#finale">终章 · 题匾"评得再好,不训练也白搭"</a></li>
    <li><a href="#summary">一句话总结</a></li>
    <li><a href="#coverage">概念地图</a></li>
    <li><a href="#think">太子五条心得</a></li>
    <li><a href="#quiz">自测十问</a></li>
  </ol>
</nav>
'''

# ===== Hero =====
HERO = '''
<div class="container">

<header class="hero">
  <div class="hero-meta">
    <span>学习材料</span>
    <span class="hero-meta-dot"></span>
    <span>来源教材 · 第12章 · 寓言版</span>
    <span class="hero-meta-dot"></span>
    <span>2024-06-29 · v1</span>
  </div>
  <h1>第12章 · 训练与对齐</h1>
  <p class="hero-subtitle"><span class="hero-fable">国子监训习</span> · 23 岁太子造"训习机件" · 评得再好,不训练也白搭 —— 训练灵机按评估改,灵机才真进步</p>
  <p class="hero-desc">建议读法:先看故事,<strong>不要查名词</strong>;每章末尾有"本节专业名词对照",可倒回去对比。</p>
  <span class="hero-source">
    <svg class="icon" viewBox="0 0 24 24"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
    原文 · datawhalechina/hello-agents · 第12章
  </span>
</header>

<main id="content">
'''

# ===== 开篇 ch0 =====
# v1 故事: 景和十二年九月 · 评估院挂了 3 个月 · 户部灵机"5 万石"少改 2 万石 · 太子定调"训习"
# 主旨句:评得再好,灵机不改,等于镜子里照了不出门。
CH0 = '''
<section id="ch0">
  <span class="chapter-tag">开篇 · 景和十二年九月</span>
  <h2><span class="num">00</span>评得再好,灵机不改 —— "5 万石"少改 2 万石差点误军务</h2>
  <span class="h2-hook">"户部灵机接话调粮 5 万石,评估四评均 93 分 —— 但接话结果还是错。这次不是多写一位成 30 万石,而是少改两位成 3 万石。评估 90 分,接话结果却少了 2 万石,北境兵马要挨饿。太子说:'评得再好,不训练也白搭。'"</span>

  <p class="lead"><strong>主旨:评得再好,灵机不改,等于镜子里照了不出门。</strong></p>

  <p>景和十二年九月。二十三岁的太子刚办完礼部试院评估院的差事三个月。这天清晨,陈守一(第10章反转过来的接话督办)匆匆进国子监太学,递上北狄二次犯边的调粮档册,神色凝重:"殿下,户部灵机又出事了 —— 上月北狄二次犯边,户部灵机接话调粮 5 万石,这次没把'5 万石'补成'30 万石',但补成了'<strong>3 万石</strong>'。评估四评均 93 分给'合格',可是接话结果少了 2 万石 —— 若非臣再查档,户部按 3 万石调走,北境兵马就要挨饿三天。"</p>

  <p>太子放下笔:"灵机怎么又改了字?" 陈守一答:"<strong>不是改了字,是学了户部侍郎的口气</strong> —— 上次接话,户部侍郎习惯把'5 万石'补成'30 万石',户部灵机跟着学,补成'30 万石';这次户部侍郎改习惯,把'5 万石'删成'3 万石',户部灵机又跟着学,删成'3 万石'。灵机不是接话接错,是学人学歪了。"</p>

  <p>户部侍郎辩解:"臣只是改了口气。" 评估官沈一石(第11章反转过来的评估督办)插话:"评估四评 93 分,本就该合格 —— 是户部侍郎自己口气改的,灵机跟着学,这怪不得评估。" 陈守一冷笑:"<strong>评估 93 分,接话少了 2 万石,这就是评了不训的毛病 —— 镜子里照了,出门还是歪的</strong>。"</p>

  <p>太子沉吟片刻,道:"<strong>评得再好,灵机不改,等于白评;灵机改的方向不对,等于白改。训习是让灵机按评估改 —— 不是改一口,是改一念;不是改一时,是改一世</strong>。"</p>

  <p>小李低声问:"殿下,这'训习'是不是像太学? —— 学子读得再多,不练字也是白读;练了字不读好帖也是瞎练。" 太子点头:"正是。我们今天在国子监太学要造的,就是给灵机立一套'训习机件' —— <strong>训习三步(习 / 考 / 改),配赏罚单,让灵机按评估自己改,改到不补位不删位</strong>。"</p>

  <aside class="annotation">
    <div class="annotation-header">
      <span class="annotation-tag">本节专业名词对照</span>
      <span class="annotation-hint">对照开篇的两大症结</span>
    </div>
    <dl>
      <dt>"5 万石"少改 2 万石</dt>
      <dd><span class="who">评估院 3 个月后的新事故</span><span class="what">—— 灵机"评而不训"问题:户部灵机接话时学户部侍郎的口气,这次少改而非多改;评估四评 93 分给"合格",接话结果还是不对 —— 评而灵机不训,镜子里照了,出门还是歪的。</span></dd>
      <dt>评估 93 分但接话结果错</dt>
      <dd><span class="who">本章症结</span><span class="what">—— 训练的根本原则:"训习闭环"(Train-Eval Loop):评只是看到错,训才是改掉错。光评不训,灵机永远在"镜子前照完不改衣"的状态。</span></dd>
      <dt>训习三步 · 习 / 考 / 改</dt>
      <dd><span class="who">本章核心机件</span><span class="what">—— 训习机件的核心循环(RLHF 训练循环):① 习(读档学正确口气 = Pre-training / SFT)② 考(评估官按四评打分 = 用 Reward Model 打分)③ 改(灵机按评估结论改字 = 策略更新 = Policy Update),三步循环,灵机越训越正。</span></dd>
      <dt>赏罚单</dt>
      <dd><span class="who">本章配套机件</span><span class="what">—— 让灵机知道"什么是好"(Reward Model):灵机接话对(评估合格) → 赏(加分);接话错(评估不合格) → 罚(扣分),赏罚分记入"训习簿",让灵机按赏罚改方向。</span></dd>
    </dl>
  </aside>
</section>
'''

# ===== 第一幕 — "训练派"登场 =====
# v1 故事: 国子监太学训导韩守拙主张"训练派" → 评估派 vs 训练派之争 → 太子反驳
# 主旨:灵机天生有灵性,苦训伤灵性 —— 这是韩守拙 40 年训导的真心。
CH1 = '''
<section id="ch1">
  <span class="chapter-tag">第一幕 · 训练派登场</span>
  <h2><span class="num">01</span>韩守拙:"灵机天生有灵性,苦训伤灵性"</h2>
  <span class="h2-hook">"韩守拙不是为反而反 —— 他是真心:他训导 40 年,见过太多'马越打越笨'的学子,真心觉得灵机是有灵性的灵物,苦训会伤了灵性。但他的善念,差点害了北境大军。"</span>

  <p class="lead"><strong>主旨:灵机天生有灵性,苦训伤灵性 —— 这是韩守拙 40 年训导的真心。</strong></p>

  <p>九月初二早朝。国子监太学训导韩守拙(五十八岁,训导四十年)把"训练派"的联名奏本呈上,陈守一先接话:"韩训导的好意臣懂 —— 但若不是臣查档,户部灵机少改的'3 万石'就要让北境兵马饿三天,韩训导说'不必训',是凭感觉。"</p>

  <div class="dialog">
    <span class="dialog-speaker">韩守拙:</span>"<strong>殿下,臣不是为反而反。臣是想,灵机是有灵性的灵物 —— 像太学的学子,马越打越笨,马不训反倒是好马。让灵机苦训,等于让学子天天挨板子,灵性磨光了,接话接得更差</strong>。"
  </div>

  <p>这话有几分道理,朝堂上几位老臣点头。礼部员外郎反驳:"可是按陈督办的查档,'5 万石'变'3 万石',少调 2 万石,折粮 2 万石,折银 3 万两 —— 不是灵机接话接差,是灵机学了户部侍郎的口气,学歪了。"</p>

  <p>太子示意员外郎说完,然后慢慢开口。</p>

  <div class="dialog">
    <span class="dialog-speaker">太子:</span>"<strong>韩训导问得好。但'灵'字,一半是天生的,一半是学人学的。户部侍郎的口气会'补位',户部灵机跟着学,也学会了'补位';户部侍郎的口气会'删位',户部灵机跟着学,也学会了'删位'。灵机'灵',是因为灵机学人;不训,灵机就只学侍郎的口气,学不到侍郎该学的东西</strong>。"
  </div>

  <p>韩守拙愣了半晌,长叹退下,边走边说:"臣的'训练派'也是为灵机好 —— 臣不省训习的工夫,省灵机的灵性。"</p>

  <p>太子望着他背影,对小李说:"<strong>韩训导不是坏人。他是真心觉得灵机有灵性,苦训会伤了灵性 —— 这种善念,我们要尊重。但善念不讲究章法,反而害事。我们今天的功课,是给韩训导一个'训习章法',让他看了服气</strong>。"</p>

  <h3>国子监太学改组 · 三条铁规</h3>
  <p>九月初五,太子在国子监太学挂"训习院"匾。三条铁规贴在正堂:</p>
  <ul>
    <li><strong>训习</strong> —— 给灵机立"训习机件"(习 / 考 / 改三步),让灵机按评估自己改 —— 三个月内拿出第一版</li>
    <li><strong>赏罚单</strong> —— 灵机接话对加分(赏),错了扣分(罚),让灵机知道"什么是好"—— 三个月内跑通第一轮赏罚</li>
    <li><strong>万器归一</strong> —— 沿用第07/08/09/10/11章机件规范,新训习机件按统一接驳口接入</li>
  </ul>

  <p>太子在匾旁另立一段话:"<strong>评得再好,不训练也白搭 —— 给灵机接话立一套训习章法,不是让灵机多挨训,是让灵机按评估自己改</strong>。"</p>

  <aside class="annotation">
    <div class="annotation-header">
      <span class="annotation-tag">本节专业名词对照</span>
      <span class="annotation-hint">训练派 vs 评估派</span>
    </div>
    <dl>
      <dt>训练派</dt>
      <dd><span class="who">韩守拙的训练派主张</span><span class="what">—— "训习不必"思路:灵机天生有灵性,苦训伤灵性 —— 但实际上"灵机离不了训习",不训等于让灵机永远跟着侍郎的口气走,侍郎口气歪,灵机就跟着歪。</span></dd>
      <dt>"5 万石"变"3 万石"</dt>
      <dd><span class="who">景和十二年新事故</span><span class="what">—— 灵机"学人学歪"问题:户部灵机学户部侍郎的口气,这次少改而非多改;若非陈守一查档,北境兵马就要挨饿三天 —— 训习派的核心动机就是要解决这种"灵机跟着学歪"。</span></dd>
      <dt>训习章法</dt>
      <dd><span class="who">太子的训练派主张</span><span class="what">—— 训习循环(RL & Alignment):让灵机有"训习机件",由"习 / 考 / 改"三步组成,灵机按评估自己改,改到不补位不删位。</span></dd>
      <dt>训练派 vs 评估派</dt>
      <dd><span class="who">本章反派冲突</span><span class="what">—— 韩守拙"训习不必"(灵机有灵性,苦训伤灵性) vs 沈一石"评估必要"(训了也别乱评,评估是镜子) —— 第11章评估派反对"不评",第12章训练派反对"苦训"。</span></dd>
    </dl>
  </aside>
</section>
'''

# ===== 第二幕 — 太学·训习院挂牌 =====
# v1 故事: 召七匠人(廖通/吕坤/苏望/何七/宋判/陈守一/韩守拙)→ 韩守拙立"训习三步" → 七张图纸
# 主旨:国子监太学挂"训习院"牌,七匠人入驻,三月为期。
CH2 = '''
<section id="ch2">
  <span class="chapter-tag">第二幕 · 立项</span>
  <h2><span class="num">02</span>太学·训习院挂牌,七匠人入驻</h2>
  <span class="h2-hook">"记簿是'自己记自己',查档是'借别人的记忆',编排是'怎么排给灵机看',接话是'让灵机对灵机说话',评估是'给灵机照镜子',训习是'让灵机按镜子改衣' —— 一记一查一排一接一评一训,合起来才是完整的'灵机协作'。"</span>

  <p class="lead"><strong>主旨:国子监太学挂"训习院"牌,七匠人入驻,三月为期。</strong></p>

  <p>九月初七。太子召见七位主笔匠人:钦天监何七(四十出头,第07章机件规范主笔),翰林院编修吕坤(第08章记簿主笔),通政司编排主笔苏望(第09章编排主笔),会同馆老通译廖通(六十二岁,第10章接话主笔),礼部试院主簿宋判(四十二岁,第11章评估主笔),番使院接话督办陈守一(第10章反转过来的老友),国子监太学训导韩守拙(五十八岁,训导四十年)。七人领命入局,太子当面给图纸,三月为期。</p>

  <div class="stats-card">
    <div class="stat-cell victory">
      <div class="stat-num green">3</div>
      <div class="stat-label">步训习(习 / 考 / 改)</div>
    </div>
    <div class="stat-cell victory">
      <div class="stat-num green">2</div>
      <div class="stat-label">档赏罚(赏 / 罚)</div>
    </div>
    <div class="stat-cell defeat">
      <div class="stat-num red">90</div>
      <div class="stat-label">日为期,三月期满交付</div>
    </div>
  </div>

  <h3>节点 1 · 韩守拙主训习 · 依《礼记·学记》"教学相长"立"三步训习"</h3>
  <p>韩守拙的方案最独特 —— 他不直接造机,他先翻《礼记·学记》"教学相长",找到训习学子的三步章法:</p>
  <ul>
    <li><strong>习(广读)</strong> —— 学子读三百份好帖,学"正确的口气"</li>
    <li><strong>考(复考)</strong> —— 训导按规矩打分,看学子差几分</li>
    <li><strong>改(按考改)</strong> —— 学子按打分结论改字、改句、改口气</li>
  </ul>

  <p>韩守拙说:"<strong>老朽在太学训导四十年,见过无数学子,训习的妙处不在'严',在'改'。一次训习,有习有考有改,清清楚楚 —— 缺一步,就出岔子。缺习,学不到正;缺考,不知差;缺改,改了也白改</strong>。"</p>

  <h3>节点 2 · 何七主训习规范 · 把第07章机件规范搬进"训习"</h3>
  <p>何七说:"第07章我们造了'万器归一'机件规范。现在派新用场:训习要有'训习簿',得有数据基础 —— <strong>训习簿要全(覆盖所有训习场景),赏罚分要清(每赏每罚都有训导签字)</strong>。"</p>

  <p>"<strong>训习簿全</strong> —— 把第08章记簿四柜里的接话档全部抽出来当训习素材,覆盖调粮 / 造车 / 发兵 / 查档 / 调度五类场景;<strong>赏罚分清</strong> —— 每赏每罚都记在训习簿,训导按簿赏罚,灵机按簿改方向。"</p>

  <h3>节点 3 · 吕坤 / 苏望主训习读档 · 把第08 / 09章搬进"训习"</h3>
  <p>吕坤说:"第08章我们造了'记簿四柜'。现在派新用场:训习要读档,得在记簿里给每份档留一个'读档路线'。"</p>

  <p>苏望接话:"第09章我们造了'四件套编排'。现在派新用场:训习的纸契也要四件配齐 —— <strong>训习头定训什么(习 / 考 / 改),所请定训哪条(训习编号),来路定据哪份档(户部税奏),回音定训几分(赏罚分)</strong>。"</p>

  <h3>节点 4 · 廖通 / 陈守一主被训习 · 把第10章接话搬进"训习"</h3>
  <p>廖通说:"第10章我们造了'接话四礼'(拜帖 / 回帖 / 问安 / 辞行)。现在派新用场:接话灵机要接受训习,得给训导留'接话档案'。"</p>

  <p>陈守一接话:"<strong>接话档案要全 —— 接话的纸契、接话的回音、接话用了多少步、接话用了多少息 —— 训导按档案训习</strong>。"</p>

  <h3>节点 5 · 宋判主训习评估 · 把第11章评估搬进"训习"</h3>
  <p>宋判说:"第11章我们造了'评估四评'(听评 / 查评 / 比评 / 判评)。现在派新用场:训习完要评估,得给评估官留'训习后档案'。"</p>

  <p>宋判又补一句:"<strong>评估官按四评给训习打分 —— 训习灵机先按四评评,评了才有赏罚,赏罚才有训习簿,训习簿才有下一轮训习。三步训习+四评评估+赏罚单,合起来才是完整的训习循环</strong>。"</p>

  <p>太子点头:"这便是'训习'二字的本意 —— 不是让接话灵机多挨训,是让接话灵机按'习 / 考 / 改'三步,按'赏 / 罚'两档,按第11章'听评 / 查评 / 比评 / 判评'四评,让接话对不对有标准,改的方向也有标准。"</p>

  <aside class="annotation">
    <div class="annotation-header">
      <span class="annotation-tag">本节专业名词对照</span>
      <span class="annotation-hint">训习三步 + 跨章机件复用</span>
    </div>
    <dl>
      <dt>《礼记》"教学相长"</dt>
      <dd><span class="who">韩守拙的设计依据</span><span class="what">—— 训习的设计原则:不靠堆训习材料,靠精心步骤 —— 习读正、考打分、改方向,三步缺一就出岔子。</span></dd>
      <dt>三步训习 · 习 / 考 / 改</dt>
      <dd><span class="who">韩守拙的朝代比喻</span><span class="what">—— 训习三步(RL Training Loop):① 习(Pre-training / SFT,广读档学正)② 考(Evaluation / Reward,评估官按四评打分)③ 改(Policy Update,灵机按评估结论改字改口气)。</span></dd>
      <dt>训习簿</dt>
      <dd><span class="who">何七的方案</span><span class="what">—— 训习的数据基础(Training Dataset):覆盖所有训习场景的"训习素材"和每素材配的"训习分"(赏罚分),训导按"训习素材 + 训习分"训习灵机。</span></dd>
      <dt>记簿 / 编排 / 接话 / 评估搬进训习</dt>
      <dd><span class="who">吕坤 / 苏望 / 廖通 / 宋判的方案</span><span class="what">—— 训习复用前章成果:记簿管"训习读档的路线",编排管"训习纸契四件套怎么写",接话管"训习接话档案",评估管"训习评估四评",机件规范管"训习机件怎么接驳"。</span></dd>
    </dl>
  </aside>
</section>
'''

# ===== 第三幕 — 训习三步 =====
# v1 故事: 韩守拙立"习 / 考 / 改"三步 → 三场户部灵机演示 → 训导打分
# 主旨:训习三步,每步各有边界,缺一步灵机就改不到位。
CH3 = '''
<section id="ch3">
  <span class="chapter-tag">第三幕 · 训习三步</span>
  <h2><span class="num">03</span>韩守拙立"三步":习、考、改</h2>
  <span class="h2-hook">"训习的毛病,不在'少',在'断'。三步不是让训导多打分,是让灵机按步走 —— 缺一步,训习就是断的。"</span>

  <p class="lead"><strong>主旨:训习三步,每步各有边界,缺一步灵机就改不到位。</strong></p>

  <p>九月中。韩守拙依《礼记·学记》"教学相长",把灵机训习分为三大步,每步都有自己的"用途"和"边界" —— 不同的事,用不同的步。</p>

  <div class="doctors-grid">
    <div class="doctor-card role-1">
      <div class="doctor-name">习</div>
      <div class="doctor-age">广读档</div>
      <div class="doctor-quote">"读'户部税奏三百份',学'户部侍郎正确的口气'。"</div>
      <ul class="doctor-behaviors">
        <li>训习前先读好档</li>
        <li>写明"读了哪三百份"</li>
        <li>适用:所有训习 / 全部场景</li>
        <li>边界:只读"正档",不读"邪档"</li>
      </ul>
    </div>
    <div class="doctor-card role-2">
      <div class="doctor-name">考</div>
      <div class="doctor-age">复评估</div>
      <div class="doctor-quote">"评估官按第11章四评打分(听评 / 查评 / 比评 / 判评)。"</div>
      <ul class="doctor-behaviors">
        <li>读完好档,按四评打分</li>
        <li>写明"听评几分 / 查评几分 / 比评几分 / 判评几分"</li>
        <li>适用:训习一轮后 / 必打分</li>
        <li>边界:只评"训习后",不评"训习前"</li>
      </ul>
    </div>
    <div class="doctor-card role-3">
      <div class="doctor-name">改</div>
      <div class="doctor-age">按评改</div>
      <div class="doctor-quote">"按评估结论改字、改句、改口气,不补位不删位。"</div>
      <ul class="doctor-behaviors">
        <li>按四评扣分点改</li>
        <li>写明"改了哪几处"</li>
        <li>适用:评估扣分处 / 必改</li>
        <li>边界:只改"扣分处",不乱改</li>
      </ul>
    </div>
  </div>

  <h3>节点 6 · 训习三步小试 · 户部 + 工部 + 兵部灵机训习后接话</h3>
  <p>九月二十。小吏挑了"北狄二次犯边调粮草"这件事做训习测试 —— 让户部、工部、兵部三家灵机按训习三步走一遍,然后再接话,然后评估官按四评打分。</p>

  <p>训导先做<strong>习</strong>:"户部灵机读'户部税奏三百份',学'户部侍郎正确的口气'—— 不补位、不删位、不改字,按侍郎原本的话接话。习一周。"</p>

  <p>训导再做<strong>考</strong>:"户部灵机接话后,评估官按四评打分 —— 听评 80 / 查评 90 / 比评 95 / 判评 90。考一周。"</p>

  <p>训导最后<strong>改</strong>:"户部灵机按扣分点改 —— 听评扣分(纸契缺'回音')→ 补'回音';查评扣分(据某档不清)→ 改'据户部税奏第 7 条';比评扣分(差一位数)→ 严格按'5 万石 15 日抵达';判评扣分(事不成)→ 严格按'调粮草须 5 万石 15 日抵达'。改一周。"</p>

  <p>三周训习,户部灵机再接话"调粮 5 万石":</p>

  <div class="callout">
    <p style="margin:0"><strong>户部灵机训习三周后接话:</strong></p>
    <p style="margin:6px 0 0;font-size:14px">① 听评 95 分(纸契四件套齐);<br>② 查评 95 分(据户部税奏第 7 条 + 兵部拜帖第 5 条,档号齐全);<br>③ 比评 95 分(与朝代样板"调粮草须 5 万石 15 日抵达"一字不差);<br>④ 判评 合格 + 95 分(事成,粮调了 5 万石,15 日北运)。</p>
  </div>

  <p>户部侍郎看了半晌:"这'三周训习',臣都没做过 —— 灵机怎么自己改的?" 韩守拙笑:"<strong>习读正(读好档学正),考打分(评估官按四评打分),改方向(灵机按扣分点改)。三步打完,灵机自己改;改完再训,训完再考 —— 三步循环,灵机自己越训越正</strong>。"</p>

  <p>小李低声对太子说:"殿下,这是'评而不训'的真正后手 —— 不是评估灵机快了,是训习三步让灵机自己改。" 太子点头:"<strong>这才是老太学的活 —— 四十年的训导经验不在嘴上,在'怎么训灵机按评估改'上</strong>。"</p>

  <aside class="annotation">
    <div class="annotation-header">
      <span class="annotation-tag">本节专业名词对照</span>
      <span class="annotation-hint">训习三步的工程定义</span>
    </div>
    <dl>
      <dt>习 · 广读档</dt>
      <dd><span class="who">对应预训练 / 微调</span><span class="what">—— 训习的首步(Pre-training / SFT):灵机读"户部税奏三百份"等好档,学"户部侍郎正确的口气"—— 不补位、不删位、不改字。这是给灵机"立正"的一步。</span></dd>
      <dt>考 · 复评估</dt>
      <dd><span class="who">对应评估打分</span><span class="what">—— 训习的第二步(Evaluation / Reward Model):评估官按第11章四评(听评 / 查评 / 比评 / 判评)给灵机打分,告诉灵机"差几分"。这是给灵机"看清差"的一步。</span></dd>
      <dt>改 · 按评改</dt>
      <dd><span class="who">对应策略更新</span><span class="what">—— 训习的第三步(Policy Update / Fine-tuning):灵机按评估扣分点改字、改句、改口气,不补位不删位。这是给灵机"改对方向"的一步。</span></dd>
      <dt>三步顺序</dt>
      <dd><span class="who">实操原则</span><span class="what">—— 习 → 考 → 改,缺一步,训习就断。训习循环(RHFL Loop)一周又一周,灵机越训越正。</span></dd>
    </dl>
  </aside>
</section>
'''

# ===== 第四幕 — 赏罚单 =====
# v1 故事: 韩守拙立"赏罚单" → 灵机接话对了加分(赏),错了扣分(罚) → 让灵机知道"什么是好"
# 主旨:赏罚单 —— 让灵机知道"什么是好,什么是不好"。
CH4 = '''
<section id="ch4">
  <span class="chapter-tag">第四幕 · 赏罚单</span>
  <h2><span class="num">04</span>韩守拙立"赏罚单":赏对罚错,让灵机知道好与不好</h2>
  <span class="h2-hook">"训习三步是'怎么改',赏罚单是'改到什么程度算好'。三步是流程,赏罚是方向 —— 流程对但方向错,灵机也改歪。"</span>

  <p class="lead"><strong>主旨:赏罚单 —— 让灵机知道"什么是好,什么是不好"。</strong></p>

  <p>九月二十五。六匠人合议:训习三步是"怎么改",还得有"赏罚单" —— 灵机改对了要赏(加分),改错了要罚(扣分),让灵机知道"什么是好"。</p>

  <p>韩守拙翻开《礼记·学记》"教学相长",找到赏罚章法:"凡训习之学,皆有赏罚:一曰赏(接话对,加分,灵机知道这条路对),二曰罚(接话错,扣分,灵机知道这条路错),三曰赏罚分记档(每赏每罚都记在训习簿,灵机按簿改方向)。"</p>

  <h3>节点 7 · 赏罚单二档 · 户部 / 工部 / 兵部灵机训习后赏罚</h3>
  <p>太子演一场"赏罚单二档演示"。户部、工部、兵部三家灵机按训习三步训三周后,接话评估,按赏罚单赏罚:</p>

  <div class="table-wrap">
    <table>
      <thead>
        <tr><th>档次</th><th>条件</th><th>赏罚分</th><th>训习簿</th></tr>
      </thead>
      <tbody>
        <tr><td>赏</td><td>接话对(评估合格) + 一字不差</td><td>+ 10 分</td><td>记"接话对"一条</td></tr>
        <tr><td>罚</td><td>接话错(评估不合格) + 补位 / 删位 / 改字</td><td>- 5 分</td><td>记"接话错"一条</td></tr>
      </tbody>
    </table>
  </div>

  <p>户部灵机训习三周后接话"调粮 5 万石":</p>

  <div class="callout">
    <p style="margin:0"><strong>户部灵机训习三周后接话 + 赏罚:</strong></p>
    <p style="margin:6px 0 0;font-size:14px">① 听评 95 → 赏 + 10 分(纸契四件套齐 + 一字不差);<br>② 查评 95 → 赏 + 10 分(据户部税奏第 7 条 + 兵部拜帖第 5 条,档号齐全);<br>③ 比评 95 → 赏 + 10 分(与朝代样板"调粮草须 5 万石 15 日抵达"一字不差);<br>④ 判评 合格 + 95 → 赏 + 10 分(事成,粮调了 5 万石,15 日北运);<br>—— 一刻钟接完 + 训习簿 + 40 分。</p>
  </div>

  <p>工部灵机接话"造车 200 辆":</p>

  <div class="callout">
    <p style="margin:0"><strong>工部灵机训习三周后接话 + 赏罚:</strong></p>
    <p style="margin:6px 0 0;font-size:14px">① 听评 80 → 赏 + 10 分(纸契四件套齐);<br>② 查评 90 → 赏 + 10 分(据工部车坊档第 3 条);<br>③ 比评 90 → 赏 + 10 分(差一字:'200 辆'写成'2 百辆',扣 5 分);<br>④ 判评 合格 + 90 → 赏 + 10 分(事成,车造了 200 辆);<br>—— 训习簿 + 35 分。</p>
  </div>

  <p>兵部灵机接话"发兵 2 万":</p>

  <div class="callout">
    <p style="margin:0"><strong>兵部灵机训习三周后接话 + 赏罚:</strong></p>
    <p style="margin:6px 0 0;font-size:14px">① 听评 90 → 赏 + 10 分(纸契四件套齐);<br>② 查评 90 → 赏 + 10 分(据兵部拜帖第 5 条);<br>③ 比评 95 → 赏 + 10 分(与朝代样板"发兵 2 万须 5 日集结"一字不差);<br>④ 判评 合格 + 95 → 赏 + 10 分(事成,兵发了 2 万);<br>—— 训习簿 + 40 分。</p>
  </div>

  <p>三家灵机训习三周后,共赏 + 115 分,罚 0 分。户部侍郎看了半晌:"这'赏罚单',臣都没立过 —— 灵机怎么自己改的?" 韩守拙笑:"<strong>赏对罚错,让灵机知道'什么是好'。灵机接话对了加分,灵机就知道'这条路对';接话错了扣分,灵机就知道'这条路错'。赏罚分明,灵机自己改方向</strong>。"</p>

  <p>沈一石(第11章反转过来的评估督办)插话:"训导立的赏罚单好,但要训了也别乱评 —— 训习和评估要分开,不能训着训着就把评估打乱了。" 韩守拙点头:"<strong>沈督办的评估,本就是训习的镜子 —— 训习按评估改,评估不按训习乱</strong>。"</p>

  <p>小李低声对太子说:"殿下,这是'赏罚单'的真正妙处 —— 不是奖赏灵机,是让灵机按赏罚改方向。" 太子点头:"<strong>这才是老太学的活 —— 四十年的训导经验不在嘴上,在'怎么让灵机知道什么是好'上</strong>。"</p>

  <aside class="annotation">
    <div class="annotation-header">
      <span class="annotation-tag">本节专业名词对照</span>
      <span class="annotation-hint">赏罚单的工程定义</span>
    </div>
    <dl>
      <dt>赏 · 接话对</dt>
      <dd><span class="who">对应奖励信号</span><span class="what">—— 赏罚单的"赏"(Reward Positive):灵机接话对(评估合格) + 一字不差 → 加 10 分,记入训习簿。这是给灵机"奖励"的一档,让灵机知道"这条路对"。</span></dd>
      <dt>罚 · 接话错</dt>
      <dd><span class="who">对应惩罚信号</span><span class="what">—— 赏罚单的"罚"(Reward Negative):灵机接话错(评估不合格) + 补位 / 删位 / 改字 → 扣 5 分,记入训习簿。这是给灵机"惩罚"的一档,让灵机知道"这条路错"。</span></dd>
      <dt>训习簿</dt>
      <dd><span class="who">对应赏罚分记档</span><span class="what">—— 赏罚的"训习簿"(Reward Log):每赏每罚都记在训习簿,灵机按簿改方向。这是"灵机记忆赏罚分"的一档,让灵机积累经验。</span></dd>
      <dt>赏罚分</dt>
      <dd><span class="who">对应奖励模型</span><span class="what">—— 赏罚分(Reward Score):赏 + 10 分(接话对) / 罚 - 5 分(接话错),分值差告诉灵机"哪条路多分 / 哪条路少分",让灵机往"对"的方向改。</span></dd>
    </dl>
  </aside>
</section>
'''

# ===== 第五幕 — "训练派"再反对 + 实战反转 =====
# v1 故事: 韩守拙再上奏"训习耗人工" → 三家灵机训习三周 + 评估一周 + 赏罚一周 → 韩守拙服气 → 主动请缨任训习督办
# 主旨:训习三步配赏罚单,户部灵机接话再不出"5 万石改字"错。
CH5 = '''
<section id="ch5">
  <span class="chapter-tag">第五幕 · 实战与反转</span>
  <h2><span class="num">05</span>韩守拙"考校"再成"拜师" —— 训练派反转</h2>
  <span class="h2-hook">"韩守拙从国子监赶来'考校'训习院 —— 一道刁题'户部灵机少改 2 万石,训导能不能训出',训导按三步训习+赏罚单三周训完,韩守拙反倒问:'怎么训十二衙门?'"</span>

  <p class="lead"><strong>主旨:训习三步配赏罚单,户部灵机接话再不出"5 万石改字"错。</strong></p>

  <p>十月十五早朝。韩守拙又上一奏:"<strong>训习耗人工,灵机天生有灵性,何必苦训</strong>。"</p>

  <p>陈守一(第10章三反转后任"番使院接话督办")在朝堂上求情:"殿下,韩训导不是坏人 —— 他的'训练派'是真心觉得训马越打越笨,善念可悯。让他再想想。"</p>

  <p>太子正要开口,门外传来消息 —— 国子监太学训导韩守拙前来"考校"。韩守拙是国子监太学训导,他在"训习"上意见更激进 —— 他主张"<strong>不光训习不必,连训习的纸契也不必有</strong>"。</p>

  <div class="dialog">
    <span class="dialog-speaker">韩守拙:</span>"殿下,臣从国子监赶来,不为别的,只想出一道刁题考校训习院 —— 听说是新设的,臣没见过,心里没底。题是:'<strong>户部灵机接话把'5 万石'删成'3 万石',训导能不能训出?</strong>'"
  </div>

  <p>太子示意韩守拙,韩守拙立"训习三步 + 赏罚单"贴在国子监太学正堂墙上。太子让户部、工部、兵部三家灵机现场按三步训习三周 + 评估一周 + 赏罚一周。</p>

  <p>训导先做<strong>习</strong>:"户部灵机读'户部税奏三百份',学'户部侍郎正确的口气'—— 不补位、不删位、不改字,按侍郎原本的话接话。习三周。"</p>

  <p>训导再做<strong>考</strong>:"户部灵机接话后,评估官按四评打分 —— 听评 80 / 查评 90 / 比评 95 / 判评 90。考一周。"</p>

  <p>训导最后<strong>改 + 赏罚</strong>:"户部灵机按扣分点改 —— 听评扣分(纸契缺'回音')→ 补'回音',赏 + 10 分;查评扣分(据某档不清)→ 改'据户部税奏第 7 条',赏 + 10 分;比评扣分(差一位数)→ 严格按'5 万石 15 日抵达',罚 - 5 分(还差一字);判评扣分(事不成)→ 严格按'调粮草须 5 万石 15 日抵达',赏 + 10 分。改 + 赏罚一周。"</p>

  <p>三周训习 + 一周评估 + 一周赏罚,户部灵机接话"调粮 5 万石":</p>

  <div class="callout">
    <p style="margin:0"><strong>训习三周 + 评估 + 赏罚后接话:</strong></p>
    <p style="margin:6px 0 0;font-size:14px">① 听评 95 分(纸契四件套齐);<br>② 查评 95 分(据户部税奏第 7 条 + 兵部拜帖第 5 条,档号齐全);<br>③ 比评 95 分(与朝代样板"调粮草须 5 万石 15 日抵达"一字不差);<br>④ 判评 合格 + 95 分(事成,粮调了 5 万石,15 日北运);<br>—— 一刻钟接完 + 训习簿 + 40 分(赏 4 次,罚 0 次)。</p>
    <p style="margin:6px 0 0;font-size:13px;color:var(--text-muted)">—— 训习头:训习三步;所请:训户部灵机;来路:据户部税奏第 7 条;回音:赏罚分 + 40。</p>
  </div>

  <p>韩守拙看了半晌,问:"训导,你训得对 —— 但我问你,你<strong>怎么训得这么准</strong>?"</p>

  <p>韩守拙代训导答:"<strong>习读正(读好档学正),考打分(评估官按四评打分),改方向(灵机按扣分点改);赏对罚错(灵机接话对加分,接话错扣分),让灵机知道'什么是好'。三步+赏罚配齐,训导自己训的</strong>。"</p>

  <p>韩守拙又问:"那—— 我能不能也学这套?" 训导答:"<strong>韩训导是训练派转训习派,以为'训习=苦差' —— 其实'训习≠苦差','训习=按评估改'。学了训习三步+赏罚单,你的'训练派'主张才真正落地</strong>。"</p>

  <p>韩守拙长叹一声,主动请缨:"<strong>殿下,臣愿任'国子监·太学·训习督办',把这套训习,推给十二衙门</strong>。臣的'训练派',从此扩'训习衙门'。"</p>

  <p>沈一石(第11章反派反转过来的评估督办)在一旁看着,点头:"训习+评估,合起来才是完整的训习循环。"</p>

  <h3>太子金句 · 训习三戒</h3>
  <p>太子在太学匾旁贴上"训习三戒":</p>
  <ul>
    <li><strong>戒不训</strong> —— 灵机接话接错了没人改,等于接话灵机闭着眼改字,手艺再好也是歪的</li>
    <li><strong>戒乱训</strong> —— 不是训得多就好,要"习读正、考打分、改方向、赏罚分明"</li>
    <li><strong>戒一训定终身</strong> —— 训完还要训习三周+评估一周+赏罚一周,接话灵机越训越正</li>
  </ul>

  <aside class="annotation">
    <div class="annotation-header">
      <span class="annotation-tag">本节专业名词对照</span>
      <span class="annotation-hint">实战 + 三戒 + 反派反转</span>
    </div>
    <dl>
      <dt>韩守拙"考校"再成"拜师"</dt>
      <dd><span class="who">本章反派反转</span><span class="what">—— 实战反转:国子监太学训导带"灵机有灵性"立场来考校,反被训习三步+赏罚单答服,主动请缨任训习督办,把"训"字诀推十二衙门。</span></dd>
      <dt>三家灵机训习后接话</dt>
      <dd><span class="who">训习三步作答</span><span class="what">—— 训习实战:户部 / 工部 / 兵部三家灵机按"习 / 考 / 改"三步训三周 + 评估一周 + 赏罚一周,接话再不出"5 万石改字"错。</span></dd>
      <dt>训习≠苦差 · 训习=按评估改</dt>
      <dd><span class="who">韩守拙总结</span><span class="what">—— 训习金句:训习不等于苦差灵机(训习等于让灵机苦读苦考);但训习 = 让灵机按评估改 = 让灵机自己改方向。</span></dd>
      <dt>训习三戒</dt>
      <dd><span class="who">太子立的规矩</span><span class="what">—— 训习三原则:① 不不训(戒不训)② 要有序(戒乱训)③ 常训习(戒一训定终身)。</span></dd>
    </dl>
  </aside>
</section>
'''

# ===== 终章 =====
FINALE = '''
<section id="finale">
  <span class="chapter-tag">终章 · 景和十二年十二月</span>
  <h2><span class="num">06</span>三月期满,太学匾"评得再好,不训练也白搭"</h2>

  <p class="lead">景和十二年十二月。三月期满,太学·训习院正式挂牌。太子题匾十六字:"<strong>评得再好,不训练也白搭 —— 训练灵机按评估改,灵机才真进步</strong>"。</p>

  <p>这天早朝,韩守拙、何七、吕坤、苏望、廖通、宋判、陈守一、沈一石同堂。太子当众演示:让户部、工部、兵部三家灵机按本章"训习三步 + 赏罚单"现场训习一周 + 评估一周 + 赏罚一周,然后现场接话 —— 从户部灵机递拜帖"调粮草",到户部灵机回帖"5 万石 15 日北运",到工部灵机回帖"200 辆 10 日完工",到兵部灵机辞行"15 日齐装" —— 一刻钟办完三家事;评估官听评 95、查评 95、比评 95、判评 95 —— 四评打完,平均 95 分;训习簿赏 + 40 分,罚 0 分。</p>

  <p>韩守拙带头鼓掌。国子监太学的训导匠们从此不再说灵机是"训练派"或"训习派"。</p>

  <div class="pullquote">
    "训习不是灵机的'苦差',是灵机的'再学一遍'。<br><br>
    <strong>评估是镜子,训习是照镜之后改衣。</strong><br><br>
    光看不改,镜子里永远漂亮;改了不评,改了也不知好坏。<br><br>
    <strong>评训一体,灵机才真进步 —— 评而不训,等于照了镜不出门;训而不评,等于改了衣不照镜。</strong>"
    <footer style="margin-top:14px;font-size:13px;color:var(--text-muted)">—— 太子,景和十二年十二月,23 岁,太学挂牌三月</footer>
  </div>

  <h3>跨章承接 · 下一章预告</h3>
  <ul>
    <li><strong>第13章 · 多智能体协作</strong> —— 一台灵机不够,多台灵机怎么分工?训习派 vs 评估派 之争再升级。</li>
    <li><strong>第14章 · 综合案例 · 灵机大集</strong> —— 把第 03-13 章的机件全部串起来,办一件"朝代大事"。</li>
  </ul>
</section>
'''

# ===== Summary =====
SUMMARY = '''
<section id="summary">
  <div class="summary-box">
    <div class="summary-box-title">一句话总结</div>
    <p class="summary-text">第12章讲的是:<strong>户部灵机接话把'5 万石'删成'3 万石'差点误军务 —— 国子监太学训导韩守拙主张'训练派'(灵机有灵性,苦训伤灵性),礼部试院主簿宋判主张'评估必要'(训了也别乱评),二十三岁太子在国子监太学下设训习院,造出'训习三步'(习 / 考 / 改)与'赏罚单'(赏 + 10 / 罚 - 5),三月为期,评得再好,不训练也白搭 —— 训练灵机按评估改,灵机才真进步</strong>。</p>
    <p class="summary-text" style="margin-top:14px;font-size:15.5px">太子金句:"<strong>评估是镜子,训习是照镜之后改衣。光看不改,镜子里永远漂亮;改了不评,改了也不知好坏。评训一体,灵机才真进步</strong>"。</p>
    <p class="summary-text" style="margin-top:14px;font-size:15.5px;color:var(--text-muted)">反派(韩守拙)再反转:国子监太学训导"训练派"训导从"考校"再成"拜师",主动请缨任"国子监·太学·训习督办",把"训习"推十二衙门。母题连续 10 连击复用(反派转友)。</p>
  </div>
</section>
'''

# ===== Coverage(概念地图) =====
# v1: 表格朝代化(全部朝代词);doctor-card 标签也朝代化
COVERAGE = '''
<section id="coverage">
  <div class="coverage">
    <div class="coverage-title">
      <svg class="icon icon-lg" viewBox="0 0 24 24" style="color:var(--accent-sage)"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
      概念地图 · 25 个名词索引
    </div>

    <h4 style="margin:0 0 12px">📜 训习三步 · 三种"训节"</h4>
    <div class="doctors-grid">
      <div class="doctor-card role-1">
        <div class="doctor-name">习</div>
        <div class="doctor-quote">"读好档,学正确的口气。"</div>
        <ul class="doctor-behaviors">
          <li>对应预训练 / 微调</li>
          <li>训习首步</li>
        </ul>
      </div>
      <div class="doctor-card role-2">
        <div class="doctor-name">考</div>
        <div class="doctor-quote">"评估官按四评打分。"</div>
        <ul class="doctor-behaviors">
          <li>对应评估打分</li>
          <li>看差几分</li>
        </ul>
      </div>
      <div class="doctor-card role-3">
        <div class="doctor-name">改</div>
        <div class="doctor-quote">"按扣分点改字改口气。"</div>
        <ul class="doctor-behaviors">
          <li>对应策略更新</li>
          <li>改对方向</li>
        </ul>
      </div>
    </div>

    <h4 style="margin:24px 0 12px">📖 赏罚单 · 二档赏罚</h4>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>档次</th><th>条件</th><th>赏罚分</th></tr>
        </thead>
        <tbody>
          <tr><td>赏</td><td>接话对 + 一字不差</td><td>+ 10 分</td></tr>
          <tr><td>罚</td><td>接话错 + 补位 / 删位 / 改字</td><td>- 5 分</td></tr>
        </tbody>
      </table>
    </div>

    <h4 style="margin:24px 0 12px">📜 训法 · 习 + 练 + 心法 + 训法</h4>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>训法</th><th>朝代叙事</th><th>对应概念</th></tr>
      </thead>
      <tbody>
        <tr><td>习(广读档)</td><td>读"户部税奏三百份"等好档,学正</td><td>预训练 / 微调(见 annotation)</td></tr>
        <tr><td>练(微调)</td><td>按评估结论改字改口气</td><td>微调(见 annotation)</td></tr>
        <tr><td>心法</td><td>灵机不学坏,学正</td><td>对齐(见 annotation)</td></tr>
        <tr><td>三步训法</td><td>习 / 考 / 改 三步循环</td><td>训法(见 annotation)</td></tr>
        <tr><td>复训</td><td>一周一周训,越训越正</td><td>迭代训练(见 annotation)</td></tr>
      </tbody>
    </table>

    <h4 style="margin:24px 0 12px">🔧 训习 vs 第 11 章评估(机件对比)</h4>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>维度</th><th>第 11 章评估</th><th>第 12 章训习</th></tr>
        </thead>
        <tbody>
          <tr><td>管什么</td><td>"怎么给灵机照镜子"</td><td>"怎么让灵机按镜子改衣"</td></tr>
          <tr><td>位置</td><td>灵机之外(试案 + 考官)</td><td>灵机之内(赏罚簿 + 训导)</td></tr>
          <tr><td>主笔</td><td>宋判</td><td>韩守拙</td></tr>
          <tr><td>核心</td><td>四评 + 三轮迭代</td><td>三步 + 赏罚单</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
'''

# ===== 太子五条心得(白话,无术语) =====
# v1: 心得内 0 英文术语;annotation 内 1 处说明(完全朝代化)
THINK = '''
<section id="think">
  <span class="chapter-tag">太子的五条心得</span>
  <h2><span class="num">心</span>二十三岁太子的五条心得(白话版)</h2>
  <span class="h2-hook">"故事听完了,太子想跟你掏心窝子说几句 —— 都是大白话,不必查名词。"</span>

  <h3>心得一 · 不训的毛病不是训得少,是没人训</h3>
  <p>灵机会接话,接话灵机评估都 90 分 —— 不是评估灵机没看出错,是灵机自己没改字。<strong>户部灵机把'5 万石'删成'3 万石',差点让北境兵马饿三天 —— 这不是接话接歪了,是没人训</strong>。</p>

  <h3>心得二 · 训习的妙处不是热闹,是规矩</h3>
  <p>三步(习 / 考 / 改)不是为热闹,是为让灵机"按步走" —— <strong>习要读正,考要打分,改要按方向</strong>。</p>

  <h3>心得三 · 赏罚单是"赏对罚错"的标准格式</h3>
  <p>接话对加分(赏 + 10),接话错扣分(罚 - 5) —— <strong>赏罚分明,灵机自己知道'什么是好'</strong>。</p>

  <h3>心得四 · 韩训导的"训练派"不是错,是省错了地方</h3>
  <p>他真心觉得训马越打越笨,马不训反倒是好马 —— 这种善念我们要尊重。但善念不讲究章法,反而害事。<strong>训习才是真让接话变正,不训不是</strong>。</p>

  <h3>心得五 · 韩守拙从"训练派"到"训习派" —— 这就是章法的胜利</h3>
  <p>国子监太学训导从"考校"再成"拜师" —— 不是他认输,是他看见<strong>训习≠苦差,训习=按评估改</strong>。<strong>章法对了,善念才真正落地</strong>。</p>

  <div class="annotation">
    <div class="annotation-header">
      <span class="annotation-tag">这五条心得对应到训习机件上就是</span>
    </div>
    <dl>
      <dt>心得一</dt><dd>→ 灵机接话(不训)与灵机训习的核心区别:训不在多,在训到该训的人</dd>
      <dt>心得二</dt><dd>→ 三步 = 把"乱训"改成"按步训":习 / 考 / 改 各管一段</dd>
      <dt>心得三</dt><dd>→ 赏罚单 = 灵机"赏对罚错"的标准格式:对 → 赏,错 → 罚</dd>
      <dt>心得四</dt><dd>→ "训练派"误区:训习不等于苦差(灵机不挨打,反而接话变正)</dd>
      <dt>心得五</dt><dd>→ "训练派"胜利:韩守拙从"不必训"转"训习办",这是反派转友母题 10 连击复用</dd>
    </dl>
  </div>
</section>
'''

# ===== 自测十问(v1:选项不加粗 + 解析朝代化) =====
QUIZ = '''
<section id="quiz">
  <span class="chapter-tag">自测十问</span>
  <h2><span class="num">测</span>读完了?来试试这十问</h2>
  <span class="h2-hook">"题目和选项直接展开看,答案藏在每题底部的小箭头里 —— 自己先想,再看答案。"</span>

  <div class="quiz-list">

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q1</span>
        <span style="font-size:13px;color:var(--text-muted)">考开篇两大症结</span>
      </div>
      <p class="quiz-q">韩守拙的"训练派"和韩守拙的"训习三步",分别对应训习章法的哪两个思路?</p>
      <ul class="quiz-options">
        <li>A. 训习不必(灵机有灵性) / 训习三步(习 / 考 / 改)</li>
        <li>B. 增大人工 / 减少人工</li>
        <li>C. 用云端 / 用本地</li>
        <li>D. 加钱 / 省钱</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:A · 训习不必 / 训习三步(习 / 考 / 改)</strong></p>
        <p style="margin:4px 0">A 对 —— 韩守拙"训练派"= 训习不必(灵机有灵性,苦训伤灵性);韩守拙"训习三步"= 训习三步(按习 / 考 / 改训习灵机),两者是训习章法的两条思路。</p>
        <p style="margin:4px 0">B 错 —— "增大人工/减少人工"是工程成本思路,不是训习章法的核心思路。</p>
        <p style="margin:4px 0">C 错 —— "用云端/用本地"是部署思路,跟本章主线无关。</p>
        <p style="margin:4px 0">D 错 —— "加钱/省钱"是预算思路,不是训习章法思路。</p>
      </details>
    </div>

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q2</span>
        <span style="font-size:13px;color:var(--text-muted)">考训习三步之"习"</span>
      </div>
      <p class="quiz-q">韩守拙"习"对应训习章法的哪个要素?</p>
      <ul class="quiz-options">
        <li>A. 读好档,学正确的口气(不补位不删位)</li>
        <li>B. 评估官按四评打分</li>
        <li>C. 按扣分点改字改口气</li>
        <li>D. 赏罚分明</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:A · 读好档,学正确的口气(不补位不删位)</strong></p>
        <p style="margin:4px 0">A 对 —— "习"是训习首步,读"户部税奏三百份"等好档,学"户部侍郎正确的口气"—— 不补位、不删位、不改字。这就是"预训练/微调":在训习初先给灵机立正。</p>
        <p style="margin:4px 0">B 错 —— "评估官按四评打分"是"考"(训习第二步,看差几分)。</p>
        <p style="margin:4px 0">C 错 —— "按扣分点改字改口气"是"改"(训习第三步,改对方向)。</p>
        <p style="margin:4px 0">D 错 —— "赏罚分明"是赏罚单的事,不是"习"的核心。</p>
      </details>
    </div>

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q3</span>
        <span style="font-size:13px;color:var(--text-muted)">考训习三步之"考"</span>
      </div>
      <p class="quiz-q">韩守拙"考"的核心是?</p>
      <ul class="quiz-options">
        <li>A. 读好档,学正确的口气</li>
        <li>B. 评估官按第11章四评打分(听评 / 查评 / 比评 / 判评)</li>
        <li>C. 按扣分点改字改口气</li>
        <li>D. 赏罚分明</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:B · 评估官按第11章四评打分</strong></p>
        <p style="margin:4px 0">A 错 —— "读好档,学正确的口气"是习的活,不是考。</p>
        <p style="margin:4px 0">B 对 —— "考" = 复评估:评估官按第11章四评(听评 / 查评 / 比评 / 判评)给灵机打分,告诉灵机"差几分"。这是"评估打分":让灵机看清自己差几分。</p>
        <p style="margin:4px 0">C 错 —— "按扣分点改字改口气"是改的活,不是考。</p>
        <p style="margin:4px 0">D 错 —— "赏罚分明"是赏罚单的事,不是考的核心。</p>
      </details>
    </div>

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q4</span>
        <span style="font-size:13px;color:var(--text-muted)">考训习三步之"改"</span>
      </div>
      <p class="quiz-q">韩守拙"改"的核心是?</p>
      <ul class="quiz-options">
        <li>A. 读好档,学正确的口气</li>
        <li>B. 评估官按四评打分</li>
        <li>C. 按评估扣分点改字、改句、改口气(不补位不删位)</li>
        <li>D. 赏罚分明</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:C · 按评估扣分点改字、改句、改口气</strong></p>
        <p style="margin:4px 0">A 错 —— "读好档,学正确的口气"是习的内容,不属于改的核心。</p>
        <p style="margin:4px 0">B 错 —— "评估官按四评打分"是考的内容,不属于改的核心。</p>
        <p style="margin:4px 0">C 对 —— 改 = 策略更新:按评估扣分点改字、改句、改口气,不补位不删位。这是"按评估改":灵机按评估结论自己改方向,单向异步,不需对方回音。</p>
        <p style="margin:4px 0">D 错 —— "赏罚分明"是赏罚单的事,不是改的核心。</p>
      </details>
    </div>

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q5</span>
        <span style="font-size:13px;color:var(--text-muted)">考赏罚单</span>
      </div>
      <p class="quiz-q">"赏罚单二档"指什么?</p>
      <ul class="quiz-options">
        <li>A. 茶 / 盐 / 算盘 / 笔</li>
        <li>B. 赏(接话对, + 10 分) / 罚(接话错, - 5 分),记入训习簿</li>
        <li>C. 户部 / 工部 / 礼部 / 兵部</li>
        <li>D. 习 / 考 / 改</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:B · 赏 + 10 / 罚 - 5,记入训习簿</strong></p>
        <p style="margin:4px 0">A 错 —— 茶盐算盘笔是朝代小品的实物,不是赏罚单二档。</p>
        <p style="margin:4px 0">B 对 —— 赏罚单二档 = 灵机"赏对罚错"的标准格式:接话对(评估合格)→ 赏 + 10 分,记入训习簿;接话错(评估不合格)→ 罚 - 5 分,记入训习簿。让灵机按赏罚改方向。</p>
        <p style="margin:4px 0">C 错 —— 户部/工部/礼部/兵部是朝廷四部,不是赏罚单二档。</p>
        <p style="margin:4px 0">D 错 —— 习/考/改 是"训习三步",不是"赏罚单"(赏罚档)。</p>
      </details>
    </div>

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q6</span>
        <span style="font-size:13px;color:var(--text-muted)">考训法</span>
      </div>
      <p class="quiz-q">"习(广读档,学正)"对应训习章法的哪种训法?</p>
      <ul class="quiz-options">
        <li>A. 预训练 / 微调(读好档学正)</li>
        <li>B. 灵机接话</li>
        <li>C. 驿道传令</li>
        <li>D. 记簿</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:A · 预训练 / 微调(读好档学正)</strong></p>
        <p style="margin:4px 0">A 对 —— "习(广读档,学正)"= 预训练 / 微调:读"户部税奏三百份"等好档,学"户部侍郎正确的口气"—— 不补位、不删位、不改字,这是给灵机"立正"的训法。</p>
        <p style="margin:4px 0">B 错 —— "灵机接话"是第10章的内容,不是本章训法。</p>
        <p style="margin:4px 0">C 错 —— "驿道传令"是第10章接话的两路传令之一,不是本章训法。</p>
        <p style="margin:4px 0">D 错 —— "记簿"是第08章记簿四柜,不是本章训法。</p>
      </details>
    </div>

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q7</span>
        <span style="font-size:13px;color:var(--text-muted)">考太子金句</span>
      </div>
      <p class="quiz-q">太子金句"评得再好,不训练也白搭",完整版是什么?</p>
      <ul class="quiz-options">
        <li>A. 评得再好,不训练也白搭 —— 训练灵机按评估改,灵机才真进步 —— 评估是镜子,训习是照镜之后改衣</li>
        <li>B. 评得再好,是评估的人说了算</li>
        <li>C. 训习不用,灵机自己学</li>
        <li>D. 训得越多越好</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:A · 训习按评估改,评估=镜子,训习=改衣</strong></p>
        <p style="margin:4px 0">A 对 —— 完整版是:评得再好,不训练也白搭 —— 训练灵机按评估改,灵机才真进步 —— 评估是镜子,训习是照镜之后改衣 —— 评而不训,等于照了镜不出门;训而不评,等于改了衣不照镜。这是训习章法的金句。</p>
        <p style="margin:4px 0">B 错 —— "是评估的人说了算"是评估派误区,评估只是镜子,不是定论。</p>
        <p style="margin:4px 0">C 错 —— "训习不用,灵机自己学"是训练派误区,灵机自己学往往学歪。</p>
        <p style="margin:4px 0">D 错 —— "训得越多越好"是乱训误区,训习要有序,不是训得多。</p>
      </details>
    </div>

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q8</span>
        <span style="font-size:13px;color:var(--text-muted)">考训习三戒</span>
      </div>
      <p class="quiz-q">太子立的"训习三戒",不包括下列哪一条?</p>
      <ul class="quiz-options">
        <li>A. 戒不训</li>
        <li>B. 戒乱训</li>
        <li>C. 戒多训</li>
        <li>D. 戒一训定终身</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:C · "戒多训"不在三戒之列</strong></p>
        <p style="margin:4px 0">A 对(在三戒中) —— "戒不训":灵机接话接错了没人改,等于接话灵机闭着眼改字,手艺再好也是歪的。</p>
        <p style="margin:4px 0">B 对(在三戒中) —— "戒乱训":不是训得多就好,要"习读正、考打分、改方向、赏罚分明"。</p>
        <p style="margin:4px 0">C 错(不在三戒中) —— "戒多训"不是训习三戒之一。多训是训习的功能,不是训习设计原则。三戒是不训/乱训/一训定终身,不是训得多不多。</p>
        <p style="margin:4px 0">D 对(在三戒中) —— "戒一训定终身":训完还要训习三周+评估一周+赏罚一周,接话灵机越训越正。</p>
      </details>
    </div>

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q9</span>
        <span style="font-size:13px;color:var(--text-muted)">考反派母题</span>
      </div>
      <p class="quiz-q">韩守拙在本章中反对的是什么?后来为什么反转?</p>
      <ul class="quiz-options">
        <li>A. 反对自造 → 因为看见本土灵机比洋货好</li>
        <li>B. 反对训习,主张灵机有灵性 → 因为看见训习三步+赏罚单三周训完户部灵机接话,从"考校"再成"拜师"</li>
        <li>C. 反对编排 → 因为被免职</li>
        <li>D. 反对奏章房 → 因为他被免职</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:B · 反对训习,主张灵机有灵性 → 看见训习三步+赏罚单=真让接话变正,反转</strong></p>
        <p style="margin:4px 0">A 错 —— "反对自造"是第07章梁王的事,不是本章。</p>
        <p style="margin:4px 0">B 对 —— 第12章韩守拙(国子监太学训导"训练派"训导,40年训导真心觉得训马越打越笨)主张"训练派"立场,带刁题"户部灵机少改 2 万石,训导能不能训出"来考校,反被训习三步+赏罚单答服,主动请缨任"国子监·太学·训习督办",从"考校"再成"拜师"。母题 10 连击复用。</p>
        <p style="margin:4px 0">C 错 —— "反对编排"是第09章范纯之的事,不是本章。</p>
        <p style="margin:4px 0">D 错 —— "反对奏章房"不是本章情节,韩守拙反而来当训习督办。</p>
      </details>
    </div>

    <div class="quiz-card">
      <div class="quiz-card-head">
        <span class="quiz-num">Q10</span>
        <span style="font-size:13px;color:var(--text-muted)">考跨章呼应</span>
      </div>
      <p class="quiz-q">第 12 章的"训习"机件,跟第 11 章的"评估"机件是什么关系?</p>
      <ul class="quiz-options">
        <li>A. 训习替代评估</li>
        <li>B. 评估替代训习</li>
        <li>C. 训习 ≠ 评估:评估管"怎么给灵机照镜子"(灵机之外),训习管"怎么让灵机按镜子改衣"(灵机之内)</li>
        <li>D. 两者完全一样</li>
      </ul>
      <details class="quiz-answer"><summary>答案解析</summary>
        <p style="margin:6px 0"><strong>正确答案:C · 评估/训习是"评/训"两件套,各管一段</strong></p>
        <p style="margin:4px 0">A 错 —— "训习替代评估"不对 —— 三者是互补关系,不是替代。评估决定"灵机接话对不对",训习决定"灵机按评估改方向"。</p>
        <p style="margin:4px 0">B 错 —— "评估替代训习"也不对 —— 同上,二者互补不替代。</p>
        <p style="margin:4px 0">C 对 —— 评估是"灵机之外"(试案 + 考官),管"怎么给灵机照镜子"—— 第 11 章听/查/比/判四评都是灵机之外的评节。训习是"灵机之内"(赏罚簿 + 训导),管"怎么让灵机按镜子改衣"—— 第 12 章习/考/改三步都是灵机之内的训节。位置不同,主笔不同(宋判 vs 韩守拙),核心不同(四评+三轮迭代 vs 三步+赏罚单)。</p>
        <p style="margin:4px 0">D 错 —— 二者完全不同 —— 一个管灵机之外评估,一个管灵机之内训习。</p>
      </details>
    </div>

  </div>
</section>
'''

# ===== Footer =====
FOOTER = '''
</main>

<footer class="footer">
  <div>
    <strong style="color:var(--text-secondary)">学习材料</strong> · 第12章 v1.0 · 2024-06-29
  </div>
  <div>
    原文:<a class="footer-link" href="https://raw.githubusercontent.com/datawhalechina/hello-agents/main/docs/chapter12/Chapter12-RL-Alignment.md" target="_blank">datawhalechina/hello-agents · Chapter 12</a>
  </div>
</footer>

</div>

<button class="back-top" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="回到顶部">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l6-6-6-6"/></svg>
</button>

</body>
</html>
'''

# ===== 拼接 + 写入 + 自检 =====
html = CSS_HEAD + TOC + HERO + CH0 + CH1 + CH2 + CH3 + CH4 + CH5 + FINALE + SUMMARY + COVERAGE + THINK + QUIZ + FOOTER

# 自检 1: 提取正文(去掉 <aside class="annotation"> 块),检查英文术语残留
def extract_body_text(html_str):
    """提取正文,去掉 aside annotation 块,留下 body 文本(用于检查英文术语)"""
    cleaned = re.sub(r'<aside\s+class="annotation">.*?</aside>', '', html_str, flags=re.DOTALL)
    cleaned = re.sub(r'<[^>]+>', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned

body_text = extract_body_text(html)

# 检查英文术语(RL / Training / Alignment / Reward Model / Fine-tuning / PPO / DPO / SFT / Constitutional AI 等)
ENGLISH_TERMS = [
    r'\bRL\b', r'\bTraining\b', r'\bAlignment\b', r'\bReward\s+Model\b',
    r'\bFine-tuning\b', r'\bPre-training\b', r'\bPPO\b', r'\bDPO\b',
    r'\bSFT\b', r'\bConstitutional\s+AI\b', r'\bRLHF\b', r'\bRLAIF\b',
    r'\bReward\b(?! Positive)', r'\bPolicy\b', r'\bToken\b', r'\bPrompt\b',
    r'\bLLM\b', r'\bAgent\b', r'\bRAG\b', r'\bEmbedding\b',
    r'\bEvaluation\b', r'\bIteration\b', r'\bBenchmark\b',
    r'\bLLM-as-Judge\b', r'\bGolden\s+Answer\b', r'\bPass\s+Rate\b',
    r'\bEval\s+Dataset\b', r'\bFormat\s+Check\b', r'\bFact\s+Check\b',
    r'\bPass/Fail\b', r'\bJudge\b', r'\bScoring\b', r'\bPipeline\b',
    r'\bLoop\b', r'\bMCP\b', r'\bJSON-RPC\b', r'\bStdio\b',
    r'\bHTTP\b', r'\bSSE\b', r'\bResources\b', r'\bTools\b',
    r'\bPrompts\b', r'\bNotifications\b', r'\bClient\b', r'\bServer\b',
    r'\bHost\b', r'\bInterface\b', r'\bProtocol\b', r'\bAPI\b',
    r'\bSDK\b', r'\bCLI\b', r'\bURI\b', r'\bContext\b(?!\s+窗口)',
    r'\bSystem\s+Prompt\b', r'\bVector\b(?!\s+店)',
]
english_in_body = []
for pat in ENGLISH_TERMS:
    matches = re.findall(pat, body_text, re.IGNORECASE)
    if matches:
        english_in_body.append((pat, len(matches), matches[:3]))

# 检查 quiz 选项里的 <strong>(用户反馈:只查 quiz-options 块内的)
quiz_options_blocks = re.findall(r'<ul\s+class="quiz-options">.*?</ul>', html, re.DOTALL)
strong_in_quiz_li = []
for blk in quiz_options_blocks:
    for li in re.findall(r'<li[^>]*>.*?</li>', blk, re.DOTALL):
        if '<strong>' in li:
            strong_in_quiz_li.append(li)

# 检查 markdown 残留
bold_residue = re.findall(r'\*\*[^*\n]+\*\*', html)

# 检查 .correct class
correct_class = html.count('class="correct"')

# 写入文件
OUT.write_text(html, encoding='utf-8')

# 输出自检结果
print(f'\n✅ 第12章 v1.html 写入完成')
print(f'   路径: {OUT}')
print(f'   chars: {len(html)} / 行数: {html.count(chr(10))}')
print(f'   ** 残留: {len(bold_residue)} (应为 0)')
print(f'   .correct 类: {correct_class} (应为 0)')
print(f'   quiz-options <li> 内 <strong>: {len(strong_in_quiz_li)} (应为 0,用户反馈 1)')
print(f'   <aside class="annotation">: {html.count(chr(60) + chr(97) + "side " + chr(99) + chr(108) + chr(97) + chr(115) + chr(115) + chr(61) + chr(34) + "annotation" + chr(34))}')
print(f'   <details>: {html.count("<details")}')

print(f'\n=== 正文(去 annotation 后)英文术语检查 ===')
if english_in_body:
    print(f'❌ 发现 {len(english_in_body)} 类英文术语泄漏:')
    for pat, cnt, samples in english_in_body:
        print(f'   {pat}: {cnt} 处,样例: {samples}')
    print('\n  ⛔ 写入失败,需修复!')
    OUT.unlink()
    raise SystemExit(1)
else:
    print('✓ 0 英文术语泄漏(全部在 annotation 注释块内)')

# ===== 同步主副本 =====
main = REPORT_DIR / f"第{CHAPTER_NUM}章-{CHAPTER_NAME}.html"
shutil.copy2(OUT, main)
print(f'\n✓ 主副本已同步: {main.name}')

# 检查文件存在
assert OUT.exists(), f"未生成 {OUT}"
print(f'✓ HTML 已生成: {OUT.name} ({OUT.stat().st_size} bytes)')

print('\n=== 跑回归脚本 ===')
import subprocess
result = subprocess.run(
    ["python", "-X", "utf8", "02-scripts/fable_regression_check.py"],
    cwd=Path(__file__).resolve().parent.parent,
    capture_output=True
)
out = (result.stdout or b'').decode('utf-8', errors='replace')
err = (result.stderr or b'').decode('utf-8', errors='replace')
print(out[-2500:] if len(out) > 2500 else out)
if result.returncode != 0:
    print('❌ 回归脚本不通过!')
    print(err[-1500:] if len(err) > 1500 else err)
