# Install the skill into Antigravity's global skills directory.
# Workspace .agents/ directories are never scanned, so global is the only option.
#
#   pwsh scripts/install.ps1            # English (default)
#   pwsh scripts/install.ps1 zh-CN      # 简体中文
#   pwsh scripts/install.ps1 ja         # 日本語
#   pwsh scripts/install.ps1 ko         # 한국어
#
# Only one language can be installed at a time, because every version uses the
# same skill name. Re-run with a different language to switch.
param([string]$Language = "en")

$src = switch ($Language) {
  "en"    { "skill" }
  "zh"    { "locales/zh-CN" }
  "zh-CN" { "locales/zh-CN" }
  "ja"    { "locales/ja" }
  "ko"    { "locales/ko" }
  default { Write-Error "unknown language: $Language (use en, zh-CN, ja or ko)"; exit 2 }
}

if (-not (Test-Path "$src/SKILL.md")) { Write-Error "missing $src/SKILL.md"; exit 1 }

$name = (Select-String -Path "$src/SKILL.md" -Pattern '^name:\s*(.+)$' | Select-Object -First 1).Matches.Groups[1].Value.Trim()
$dest = Join-Path $env:USERPROFILE ".gemini\config\skills\$name"

if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path "$src\*" -Destination $dest -Recurse -Force

Write-Output "installed $Language to $dest"
python scripts/check_skills.py
Write-Output "Restart Antigravity to pick up the change."
