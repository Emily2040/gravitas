# Install the skill into Antigravity's global skills directory.
# Workspace .agents/ directories are never scanned, so global is the only option.
$name = (Select-String -Path skill/SKILL.md -Pattern '^name:\s*(.+)$' | Select-Object -First 1).Matches.Groups[1].Value.Trim()
$dest = Join-Path $env:USERPROFILE ".gemini\config\skills\$name"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path skill\* -Destination $dest -Recurse -Force
Write-Output "installed to $dest"
python scripts/check_skills.py
