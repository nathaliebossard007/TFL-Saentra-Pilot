Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$required = @(
  "AGENTS.md",
  "STATUS.md",
  "README.md",
  "docs/pilot-brief.md",
  "docs/research-baseline.md",
  "docs/decisions.md",
  "docs/falsification-rules.md",
  "docs/chat-context.md",
  "experiments/TFL-UAS-001A/README.md",
  "experiments/TFL-UAS-001B/README.md",
  "tasks/backlog.md",
  "tasks/current-task.md",
  "scripts/run-pilot-check.ps1"
)

foreach ($path in $required) {
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    throw "Missing required project-memory file: $path"
  }
}

$status = Get-Content -Raw "STATUS.md"
$current = Get-Content -Raw "tasks/current-task.md"
if ($status -notmatch "No 001B implementation has started") {
  throw "STATUS.md does not preserve the no-implementation gate."
}
if ($current -notmatch "Import and verify the frozen predecessor") {
  throw "Current task is not the predecessor import gate."
}

Write-Output "Pilot structure check passed."
