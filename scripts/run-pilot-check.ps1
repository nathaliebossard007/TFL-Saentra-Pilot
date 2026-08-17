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
  "scripts/run-pilot-check.ps1",
  "experiments/TFL-UAS-001A/FROZEN_PROVENANCE.md",
  "experiments/TFL-UAS-001A/FROZEN_MANIFEST.sha256",
  "experiments/TFL-UAS-001B/TFL-UAS-001B_PROTOCOL_v1.0.md",
  "experiments/TFL-UAS-001B/config/tfl_uas_001b_protocol_v1.json",
  "experiments/TFL-UAS-001B/PROTOCOL_FREEZE.md"
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
if ($current -notmatch "Review TFL-UAS-001B exploratory results") {
  throw "Current task is not the exploratory-review gate."
}

$frozenRoot = Join-Path $PSScriptRoot "..\experiments\TFL-UAS-001A"
$manifestPath = Join-Path $frozenRoot "FROZEN_MANIFEST.sha256"
foreach ($line in Get-Content -LiteralPath $manifestPath) {
  if ([string]::IsNullOrWhiteSpace($line)) { continue }
  $parts = $line -split "  ", 2
  if ($parts.Count -ne 2) { throw "Malformed frozen manifest line: $line" }
  $expected = $parts[0].ToLowerInvariant()
  $relative = $parts[1].Replace('/', [IO.Path]::DirectorySeparatorChar)
  $target = Join-Path $frozenRoot $relative
  if (-not (Test-Path -LiteralPath $target -PathType Leaf)) {
    throw "Frozen predecessor file missing: $relative"
  }
  $actual = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($actual -ne $expected) {
    throw "Frozen predecessor hash mismatch: $relative`nExpected: $expected`nActual:   $actual"
  }
}

Write-Output "Pilot structure check passed."
Write-Output "Frozen predecessor manifest check passed."

$protocolPath = Join-Path $PSScriptRoot "..\experiments\TFL-UAS-001B\TFL-UAS-001B_PROTOCOL_v1.0.md"
$configPath = Join-Path $PSScriptRoot "..\experiments\TFL-UAS-001B\config\tfl_uas_001b_protocol_v1.json"
$freezePath = Join-Path $PSScriptRoot "..\experiments\TFL-UAS-001B\PROTOCOL_FREEZE.md"
$freeze = Get-Content -Raw -LiteralPath $freezePath
$protocolExpected = ([regex]::Match($freeze, 'Protocol SHA-256: `([0-9a-fA-F]{64})`')).Groups[1].Value.ToLowerInvariant()
$configExpected = ([regex]::Match($freeze, 'Configuration SHA-256: `([0-9a-fA-F]{64})`')).Groups[1].Value.ToLowerInvariant()
if ([string]::IsNullOrWhiteSpace($protocolExpected) -or [string]::IsNullOrWhiteSpace($configExpected)) {
  throw "Protocol freeze hashes are missing or malformed."
}
$protocolActual = (Get-FileHash -LiteralPath $protocolPath -Algorithm SHA256).Hash.ToLowerInvariant()
$configActual = (Get-FileHash -LiteralPath $configPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($protocolActual -ne $protocolExpected) { throw "001B protocol hash mismatch." }
if ($configActual -ne $configExpected) { throw "001B configuration hash mismatch." }
Write-Output "001B protocol freeze hash check passed."
