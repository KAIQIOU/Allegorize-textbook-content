"""
fable_regression_check.py
寓言章节 HTML 一键回归校验脚本

用法:
    python scripts/fable_regression_check.py

校验内容(基于内容特征,不依赖注释命名):
    - ** 残留数(应为 0)              ← 事故 1
    - .correct 类残留数(应为 0)        ← 事故 2
    - <strong> 标签总数
    - <aside class="annotation"> 块数
    - <details> 折叠数
    - 必填分节齐全(基于 DOM 特征)    ← 不依赖注释命名
    - chars / 行数

退出码:
    0 = 全部通过
    1 = 有残留或缺分节
"""
import re
import sys
import os
from pathlib import Path

# 输出目录:env 变量优先,默认 reports/ (包内 smoke test 用)
DEFAULT_REPORT_DIR = Path(r"reports")
REPORT_DIR = Path(os.environ.get('FABLE_REPORT_DIR', str(DEFAULT_REPORT_DIR)))

def has_sticky_toc(c: str) -> bool:
    """检查是否有 sticky-toc(基于 DOM class 名,不是注释)"""
    return 'class="sticky-toc"' in c

def has_hero(c: str) -> bool:
    """检查是否有 hero 区(基于 DOM class 名)"""
    return 'class="hero"' in c

def has_opening_hook(c: str) -> bool:
    """检查是否有开篇钩子(基于 hero-desc 或第一个 h2)"""
    return 'hero-desc' in c or 'chapter-tag' in c

def has_finale(c: str) -> bool:
    """检查是否有终章(基于 chapter-tag 含'终章'或 h2 含数字 06)"""
    return '终章' in c or re.search(r'<h2><span class="num">0[56]</span>', c) is not None

def has_summary(c: str) -> bool:
    """检查是否有一句话总结(基于 summary-box DOM 类)"""
    return 'class="summary-box"' in c or '一句话总结' in c

def has_coverage(c: str) -> bool:
    """检查是否有概念地图(基于 coverage 或 doctors-grid DOM 类)"""
    return 'class="coverage"' in c or 'class="doctors-grid"' in c or '概念地图' in c

def check_file(fn: Path) -> dict:
    c = fn.read_text(encoding='utf-8')

    md_bold = len(re.findall(r'\*\*[^*\n]+\*\*', c))
    correct_class = c.count('class="correct"')
    strong = c.count('<strong>')
    annotation = c.count('<aside class="annotation">')
    details = c.count('<details')
    lines = c.count('\n')
    chars = len(c)

    # 分节检查(基于 DOM 特征,容忍注释命名差异)
    section_checks = {
        'Sticky TOC': has_sticky_toc(c),
        'Hero': has_hero(c),
        'Opening Hook': has_opening_hook(c),
        '终章': has_finale(c),
        'Summary': has_summary(c),
        'Coverage/概念地图': has_coverage(c),
    }
    missing = [k for k, v in section_checks.items() if not v]

    return {
        'fn': fn.name,
        'md_bold': md_bold,
        'correct_class': correct_class,
        'strong': strong,
        'annotation': annotation,
        'details': details,
        'lines': lines,
        'chars': chars,
        'missing': missing,
        'pass': md_bold == 0 and correct_class == 0 and not missing,
    }

def main():
    files = sorted(set(REPORT_DIR.glob('第0[1-9]章*.html')) | set(REPORT_DIR.glob('第1[0-6]章*.html')))
    if not files:
        print(f'❌ 没找到寓言 HTML(检查 {REPORT_DIR})')
        sys.exit(1)

    print(f'=== 寓言章节 HTML 回归校验 ===')
    print(f'扫描目录:{REPORT_DIR}')
    print(f'共 {len(files)} 个文件\n')

    print(f'{"状态":2s} {"文件":52s} {"**":4s} {"correct":8s} {"<strong>":9s} {"annot":6s} {"detail":7s} {"行":5s} {"chars":6s}')
    print('-' * 120)

    fail_count = 0
    warn_files = []

    for fn in files:
        r = check_file(fn)
        status = '✅' if r['pass'] else '❌'
        if not r['pass']:
            fail_count += 1
            warn_files.append((r['fn'], r['missing']))

        print(f'{status:2s} {r["fn"]:52s} {r["md_bold"]:4d} {r["correct_class"]:8d} {r["strong"]:9d} {r["annotation"]:6d} {r["details"]:7d} {r["lines"]:5d} {r["chars"]:6d}')

        if r['missing']:
            print(f'      ⚠️ 缺失分节:{r["missing"]}')

    print('-' * 120)

    if fail_count == 0:
        print(f'\n✅ 全部通过({len(files)} 个文件)')
        print(f'   - ** 残留:0')
        print(f'   - .correct 暴露答案:0')
        print(f'   - 必填分节齐全')
        sys.exit(0)
    else:
        print(f'\n❌ {fail_count} 个文件不通过:')
        for fn, miss in warn_files:
            print(f'   - {fn}:缺失 {miss}')
        print(f'\n修复指引:')
        print(f'   1. ** 残留 → Python 正则批量替换:`re.sub(r"\\*\\*([^*\\n]+)\\*\\*", r"<strong>\\1</strong>", content)`')
        print(f'   2. .correct → 替换 `<li class="correct">` 为 `<li>`,并删除对应 CSS')
        print(f'   3. 缺分节 → 用 DOM class 名确认(sticky-toc / hero / summary-box / coverage / doctors-grid)')
        sys.exit(1)

if __name__ == '__main__':
    main()