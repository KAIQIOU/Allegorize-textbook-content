@echo off
REM ===============================================
REM Fable Skills 一键渲染 + 回归
REM 使用: run_pipeline.bat <CHAPTER_NUM> <CHAPTER_NAME>
REM 示例: run_pipeline.bat 12 训练与对齐
REM ===============================================

set CHAPTER_NUM=%1
set CHAPTER_NAME=%2

if "%CHAPTER_NUM%"=="" goto :usage
if "%CHAPTER_NAME%"=="" goto :usage

echo.
echo === Fable Pipeline v1 ===
echo Chapter: 第%CHAPTER_NUM%章-%CHAPTER_NAME%
echo.

REM Step 1: 3 必跑
echo [Step 1] 3 必跑 (grep 前章 bug)...
python -X utf8 -c "
import re, pathlib
files = sorted(pathlib.Path(r'..\reports').glob('第*章-*.html'))
for f in files:
    html = f.read_text(encoding='utf-8')
    checks = {
        '.correct': len(re.findall(r'class=\"correct\"', html)),
        'justify': len(re.findall(r'text-align:.*justify', html)),
        '**残留': len(re.findall(r'\*\*[^*]+\*\*', html)),
    }
    for k, v in checks.items():
        if v > 0:
            print(f'  ❌ {f.name}: {k}={v}')
print('  ✓ 3 必跑全过')
"

REM Step 2: 渲染
echo.
echo [Step 2] 渲染第%CHAPTER_NUM%章...
REM 默认输出到 ..\reports\,可用 FABLE_REPORT_DIR 环境变量覆盖
if "%FABLE_REPORT_DIR%"=="" set FABLE_REPORT_DIR=..\reports
python -X utf8 rewrite_ch%CHAPTER_NUM%_v1.py
if errorlevel 1 (
    echo ❌ 渲染失败
    exit /b 1
)

REM Step 3: 5 项自检
echo.
echo [Step 3] 5 项自检...
python -X utf8 -c "
import re
f = open(r'..\reports\第%CHAPTER_NUM%章-%CHAPTER_NAME%-v1.html', encoding='utf-8').read()
checks = {
    '.correct': len(re.findall(r'class=\"correct\"', f)),
    'justify': len(re.findall(r'text-align:.*justify', f)),
    '**残留': len(re.findall(r'\*\*[^*]+\*\*', f)),
    'quiz-strong': len(re.findall(r'<ul class=\"quiz-options\">.*<strong>', f, re.S)),
}
all_zero = True
for k, v in checks.items():
    status = '✓' if v == 0 else '❌'
    if v > 0: all_zero = False
    print(f'  {k}: {v} {status}')
if all_zero:
    print('  ✓ 5 项自检全过')
else:
    print('  ❌ 需修复')
    exit(1)
"

REM Step 4: 回归
echo.
echo [Step 4] 跑回归...
python -X utf8 fable_regression_check.py

echo.
echo === Done ===
echo Output: reports\第%CHAPTER_NUM%章-%CHAPTER_NAME%-v1.html
goto :eof

:usage
echo Usage: run_pipeline.bat ^<CHAPTER_NUM^> ^<CHAPTER_NAME^>
echo Example: run_pipeline.bat 12 训练与对齐
exit /b 1