# Gravitas update check for Antigravity on Windows (SessionStart hook; runs in the plugin folder).
#
# At most once a day it asks GitHub for the latest Gravitas release: one request to
# api.github.com, carrying only a User-Agent with this plugin's version. The answer is
# cached in ~/.gemini/gravitas/update-check.json. When a newer release is out, it prints
# a system message that has the agent say so once, with the step to update; otherwise it
# prints {}. Any failure prints {} and exits 0, so a session never waits on this.
#
# Turn it off: create the file ~/.gemini/gravitas/update-check-off, or set the
# environment variable GRAVITAS_UPDATE_CHECK=off.
$ErrorActionPreference = 'Stop'
# Not Windows (PowerShell on a Mac or Linux): leave it to update-check.sh, which the hook runs next.
if (-not $env:USERPROFILE) { exit 1 }
$none = '{}'
try {
    $dir = Join-Path $env:USERPROFILE '.gemini\gravitas'
    if ($env:GRAVITAS_UPDATE_CHECK -eq 'off' -or (Test-Path -LiteralPath (Join-Path $dir 'update-check-off'))) { Write-Output $none; exit 0 }
    $current = (Get-Content -Raw -LiteralPath 'plugin.json' | ConvertFrom-Json).version
    if (-not ($current -match '^\d+\.\d+\.\d+$')) { Write-Output $none; exit 0 }
    $file = Join-Path $dir 'update-check.json'
    $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $state = $null
    if (Test-Path -LiteralPath $file) { try { $state = Get-Content -Raw -LiteralPath $file | ConvertFrom-Json } catch { $state = $null } }
    $checked = if ($state) { $state.checkedAt -as [long] } else { $null }
    $fresh = ($null -ne $checked) -and ($now -ge $checked) -and ($now - $checked -lt 86400)
    if (-not $fresh) {
        $latest = if ($state) { $state.latest } else { $null }
        $url = if ($state) { $state.url } else { $null }
        try {
            [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
            $r = Invoke-RestMethod -Uri 'https://api.github.com/repos/Emily2040/gravitas/releases/latest' -TimeoutSec 4 -UseBasicParsing `
                -Headers @{ 'Accept' = 'application/vnd.github+json'; 'User-Agent' = "gravitas-antigravity/$current" }
            if ($r.tag_name -match '^v?(\d+\.\d+\.\d+)$') {
                $latest = $Matches[1]
                $url = if ("$($r.html_url)".StartsWith('https://github.com/')) { "$($r.html_url)" } else { 'https://github.com/Emily2040/gravitas/releases/latest' }
            }
        } catch { }
        $state = [ordered]@{ checkedAt = $now; latest = $latest; url = $url }
        try {
            New-Item -ItemType Directory -Force -Path $dir | Out-Null
            ($state | ConvertTo-Json -Compress) | Set-Content -Encoding ASCII -LiteralPath $file
        } catch { }
    }
    if (-not $state.latest -or -not ([version]$state.latest -gt [version]$current)) { Write-Output $none; exit 0 }
    $page = if ($state.url) { $state.url } else { 'https://github.com/Emily2040/gravitas/releases/latest' }
    $text = "Gravitas update: version $($state.latest) is out; this computer has $current ($page). " +
        "In your first reply in this conversation, after everything else, add one short line in the user's language saying so, with how to update: " +
        "download Gravitas.zip from that page, unzip it, and double-click Install Gravitas (Windows).cmd. " +
        "Say it once: not in later replies, and not if one of your replies above already said it. Do not change or shorten the answer for it, and do not run the update yourself."
    $out = @{ injectSteps = @(@{ systemMessage = @{ systemMessage = $text } }) }
    Write-Output ($out | ConvertTo-Json -Depth 6 -Compress)
} catch {
    Write-Output $none
}
exit 0
