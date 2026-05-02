#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$BinDir = "$env:USERPROFILE\.local\bin"
$CodexDir = "$env:USERPROFILE\.codex"
$TargetScript = "$BinDir\codex_api"
$TargetBat = "$BinDir\codex_api.bat"
$TargetAuthList = "$CodexDir\auth_list.json"
$TargetConfig = "$CodexDir\config.toml"

function Backup-IfExists($path) {
    if (Test-Path $path) {
        $ts = Get-Date -Format "yyyyMMddHHmmss"
        Copy-Item $path "$path.bak.$ts" -Force
    }
}

Write-Host "==> Installing codex_api (Windows)"

if (-not (Test-Path $CodexDir)) {
    Write-Error "Missing directory: $CodexDir — install Codex first."
    exit 1
}

New-Item -ItemType Directory -Force -Path $BinDir | Out-Null

Backup-IfExists $TargetScript
Backup-IfExists $TargetBat
Backup-IfExists $TargetAuthList
Backup-IfExists $TargetConfig

Copy-Item "$RepoRoot\bin\codex_api" $TargetScript -Force
Copy-Item "$RepoRoot\bin\codex_api.bat" $TargetBat -Force
python "$RepoRoot\lib\merge_json_template.py" $TargetAuthList "$RepoRoot\templates\codex\auth_list.json"

python "$RepoRoot\lib\merge_codex_config.py" $TargetConfig "$RepoRoot\templates\codex\config.providers.toml"

Write-Host "Installed: $TargetScript"
Write-Host "Installed: $TargetBat"
Write-Host "Merged auth keys into: $TargetAuthList"
Write-Host "Note: existing API keys were preserved; new entries use placeholder values"
Write-Host "Merged helper-managed providers into: $TargetConfig"

if ($env:PATH -notlike "*$BinDir*") {
    Write-Warning "$BinDir is not in PATH. Add it to your user PATH to use codex_api from any directory."
}
