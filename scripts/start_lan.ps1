$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$env:GRADIO_SERVER_NAME = "0.0.0.0"
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

$ipv4 = Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object {
        $_.IPAddress -notlike "169.254.*" -and
        $_.IPAddress -ne "127.0.0.1" -and
        $_.PrefixOrigin -ne "WellKnown"
    } |
    Select-Object -First 1 -ExpandProperty IPAddress

Write-Host "Starting Imaginary Local Media AI for LAN access..." -ForegroundColor Cyan
if ($ipv4) {
    Write-Host "Open this on your Android phone: http://$ipv4:7860" -ForegroundColor Green
} else {
    Write-Host "LAN IP could not be determined automatically. The app will still start on port 7860." -ForegroundColor Yellow
}

& "$root\.venv\Scripts\python.exe" "$root\main.py"
