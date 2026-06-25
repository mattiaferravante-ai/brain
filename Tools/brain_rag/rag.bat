@echo off
setlocal
set PYTHONIOENCODING=utf-8
set HF_HUB_DISABLE_SYMLINKS_WARNING=1

if "%~1"=="" (
    echo Uso: rag "la tua domanda" [--top N] [--filter key=value] [--context]
    echo.
    echo Esempi:
    echo   rag "modulo contratti TEA"
    echo   rag "odoo 19 breaking changes" --top 10
    echo   rag "dealer website" --context
    echo   rag "fatturazione" --filter section=Work
    exit /b 1
)

C:\rag\Scripts\python.exe "%~dp0query.py" %*
