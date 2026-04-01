$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$env:GRADIO_SERVER_NAME = "127.0.0.1"
$env:GRADIO_SERVER_PORT = "7860"
$env:HF_HUB_OFFLINE = "1"
$env:IMAGINARY_LOCAL_FILES_ONLY = "1"
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:ALL_PROXY = ""
$env:GIT_HTTP_PROXY = ""
$env:GIT_HTTPS_PROXY = ""
if (Test-Path "$root\.env") {
    Get-Content "$root\.env" | ForEach-Object {
        if ($_ -match '^\s*HF_TOKEN\s*=\s*(.+?)\s*$') {
            $env:HF_TOKEN = $matches[1]
        }
    }
}

Write-Host "Starting Imaginary Local Media AI on http://127.0.0.1:7860" -ForegroundColor Cyan
& "$root\.venv\Scripts\python.exe" "$root\main.py"
