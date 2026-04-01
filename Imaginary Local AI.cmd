@echo off
setlocal
cd /d "%~dp0"

set "START_SCRIPT=start-local.cmd"
if exist "start-local-private.cmd" set "START_SCRIPT=start-local-private.cmd"

echo Starting Imaginary Local Media AI...
start "Imaginary Local Media AI" cmd /k call "%~dp0%START_SCRIPT%"

powershell -NoProfile -Command "$deadline=(Get-Date).AddSeconds(60); do { try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:7860' -UseBasicParsing -TimeoutSec 2; if ($r.StatusCode -ge 200) { exit 0 } } catch {}; Start-Sleep -Seconds 1 } while ((Get-Date) -lt $deadline); exit 1"
if errorlevel 1 (
  echo Server did not answer within 60 seconds. Leave the server window open and try http://127.0.0.1:7860 manually.
) else (
  start "" "http://127.0.0.1:7860"
  echo Browser opened.
)
endlocal
