#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
& "$RepoRoot\modules\api-switcher\install\install_codex_api_windows.ps1" @args
exit $LASTEXITCODE
