#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$BinDir = "$env:USERPROFILE\.local\bin"
$ClaudeDir = "$env:USERPROFILE\.claude"
$TargetScript = "$BinDir\cc_api"
$TargetBat = "$BinDir\cc_api.bat"
$TargetProviderList = "$ClaudeDir\provider_list.json"

function Backup-IfExists($path) {
    if (Test-Path $path) {
        $ts = Get-Date -Format "yyyyMMddHHmmss"
        Copy-Item $path "$path.bak.$ts" -Force
    }
}

Write-Host "==> Installing cc_api (Windows)"

if (-not (Test-Path $ClaudeDir)) {
    Write-Error "Missing directory: $ClaudeDir — install Claude Code first."
    exit 1
}

New-Item -ItemType Directory -Force -Path $BinDir | Out-Null

Backup-IfExists $TargetScript
Backup-IfExists $TargetBat
Backup-IfExists $TargetProviderList

Copy-Item "$RepoRoot\bin\cc_api" $TargetScript -Force
Copy-Item "$RepoRoot\bin\cc_api.bat" $TargetBat -Force
python "$RepoRoot\lib\merge_json_template.py" $TargetProviderList "$RepoRoot\templates\claude\provider_list.json"

Write-Host "Installed: $TargetScript"
Write-Host "Installed: $TargetBat"
Write-Host "Merged providers into: $TargetProviderList"
Write-Host "Note: existing provider tokens were preserved; new entries use placeholder values"
Write-Host "Preserved existing Claude settings in $ClaudeDir\settings.json"

if ($env:PATH -notlike "*$BinDir*") {
    Write-Warning "$BinDir is not in PATH. Add it to your user PATH to use cc_api from any directory."
}
