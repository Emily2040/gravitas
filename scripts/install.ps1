# Install Gravitas as an Antigravity plugin. Language: en (default), zh-CN, ja or ko.
#   pwsh scripts/install.ps1 [en|zh-CN|ja|ko]
#   pwsh scripts/install.ps1 --uninstall
$py = (Get-Command python -ErrorAction SilentlyContinue) ?? (Get-Command py -ErrorAction SilentlyContinue)
if (-not $py) { Write-Error "Python 3.8 or later is required"; exit 1 }
Set-Location (Join-Path $PSScriptRoot "..")
& $py.Source scripts/install.py @args
exit $LASTEXITCODE
