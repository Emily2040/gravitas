# Install Gravitas as an Antigravity plugin. Language: en (default), zh-CN, ja or ko.
# The Second Opinion is off by default: --review adds it, --no-review leaves it out. Every argument is passed to install.py unchanged.
#   pwsh scripts/install.ps1 [en|zh-CN|ja|ko] [--review|--no-review]
#   pwsh scripts/install.ps1 --uninstall
# The first interpreter that actually runs: on Windows, python and python3 can be the Microsoft Store stub.
$py = $null
foreach ($c in 'python3', 'python', 'py') {
    foreach ($cmd in @(Get-Command $c -CommandType Application -All -ErrorAction SilentlyContinue)) {
        & $cmd.Source -c 'import sys; sys.exit(sys.version_info < (3, 8))' *> $null
        if ($LASTEXITCODE -eq 0) { $py = $cmd.Source; break }
    }
    if ($py) { break }
}
if (-not $py) { Write-Error "Python 3.8 or later is required"; exit 1 }
& $py (Join-Path $PSScriptRoot 'install.py') @args
exit $LASTEXITCODE
