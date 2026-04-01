@echo off
setlocal
cd /d "%~dp0"
set "GRADIO_SERVER_NAME=127.0.0.1"
set "GRADIO_SERVER_PORT=7860"
set "HF_HUB_OFFLINE=1"
set "IMAGINARY_LOCAL_FILES_ONLY=1"
set "HTTP_PROXY="
set "HTTPS_PROXY="
set "ALL_PROXY="
set "GIT_HTTP_PROXY="
set "GIT_HTTPS_PROXY="
if exist ".env" (
  for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    if /I "%%A"=="HF_TOKEN" set "HF_TOKEN=%%B"
  )
)
echo Starting Imaginary Local Media AI on http://127.0.0.1:7860
".venv\Scripts\python.exe" main.py
endlocal
