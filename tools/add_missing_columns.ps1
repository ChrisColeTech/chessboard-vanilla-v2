<#
add_missing_columns.ps1

Usage:
  # Option A: set env var and run
  $env:DATABASE_URL = 'postgresql://user:pass@host:5432/dbname'
  .\add_missing_columns.ps1

  # Option B: pass connection string explicitly (recommended in your workflow)
  .\add_missing_columns.ps1 -ConnectionString 'postgresql://user:pass@host:5432/dbname?sslmode=require'

What it does:
  1) ensures sslmode=require on the connection string
  2) checks psql exists and tests connectivity
  3) creates timestamped backups of learning_modules, tutorial_steps, game_reviews
  4) runs ALTER TABLE ... ADD COLUMN IF NOT EXISTS for missing columns:
       - learning_modules.created_at timestamptz NOT NULL DEFAULT now()
       - tutorial_steps.created_at timestamptz NOT NULL DEFAULT now()
       - game_reviews.status text NOT NULL DEFAULT 'published'
  5) prints verification of the column lists afterwards

Notes:
  - This script runs destructive-looking SQL only for backups (CREATE TABLE AS SELECT) and non-destructive ALTER TABLE ... ADD COLUMN IF NOT EXISTS.
  - Adjust or remove the backup lines if you prefer a different backup strategy or a migration tool.
#>

param(
    [string]$ConnectionString = $env:DATABASE_URL
)

function Fail([string]$msg, [int]$code=1) {
    Write-Error $msg
    exit $code
}

if (-not $ConnectionString -or $ConnectionString -eq '') {
    Fail "No connection string provided. Set env var DATABASE_URL or pass -ConnectionString."
}

# Ensure sslmode parameter for Supabase
if ($ConnectionString -notmatch "sslmode=") {
    if ($ConnectionString.Contains('?')) { $ConnectionString = "$ConnectionString&sslmode=require" }
    else { $ConnectionString = "$ConnectionString?sslmode=require" }
}

# Masked display for logs
$displayConn = $ConnectionString -replace '\/\/([^:]+):([^@]+)@','//$1:REDACTED@'
Write-Host ("Using connection: {0}" -f $displayConn) -ForegroundColor DarkGray

# Ensure psql command exists
if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
    Fail "psql not found on PATH. Install PostgreSQL client (psql) first."
}

# Quick connectivity test
Write-Host "`nTesting DB connectivity..." -ForegroundColor Cyan
& psql $ConnectionString -c "SELECT 1;" > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Fail "psql failed to connect using that connection string. Check network/credentials and try again."
}
Write-Host "Connection OK." -ForegroundColor Green

# Timestamp suffix for backups
$ts = Get-Date -Format "yyyyMMddHHmmss"

# Tables to backup and alter
$tablesToBackup = @('learning_modules','tutorial_steps','game_reviews')

# BACKUP - create simple table copies (safe, idempotent)
Write-Host "`nCreating backups (one-row-copy if huge tables not desired)..." -ForegroundColor Cyan
foreach ($t in $tablesToBackup) {
    $backupName = "${t}_backup_$ts"
    $sqlBackup = "CREATE TABLE IF NOT EXISTS $backupName AS TABLE $t;"
    Write-Host ("Backing up {0} -> {1}" -f $t, $backupName)
    & psql $ConnectionString -c $sqlBackup
    if ($LASTEXITCODE -ne 0) {
        Write-Host ("Warning: backup for {0} failed (exit {1}). Continuing..." -f $t, $LASTEXITCODE) -ForegroundColor Yellow
    } else {
        Write-Host ("Backed up {0} -> {1}" -f $t, $backupName) -ForegroundColor Green
    }
}

# ALTERS - idempotent
Write-Host "`nApplying ALTER TABLE statements (IF NOT EXISTS)..." -ForegroundColor Cyan

# 1) learning_modules.created_at
$sql1 = "ALTER TABLE learning_modules ADD COLUMN IF NOT EXISTS created_at timestamptz NOT NULL DEFAULT now();"
Write-Host "-> Adding learning_modules.created_at (if missing)"
& psql $ConnectionString -c $sql1
if ($LASTEXITCODE -eq 0) { Write-Host "OK: learning_modules.created_at ensured." -ForegroundColor Green } else { Write-Host "FAILED: learning_modules.created_at (exit $LASTEXITCODE)" -ForegroundColor Red }

# 2) tutorial_steps.created_at
$sql2 = "ALTER TABLE tutorial_steps ADD COLUMN IF NOT EXISTS created_at timestamptz NOT NULL DEFAULT now();"
Write-Host "-> Adding tutorial_steps.created_at (if missing)"
& psql $ConnectionString -c $sql2
if ($LASTEXITCODE -eq 0) { Write-Host "OK: tutorial_steps.created_at ensured." -ForegroundColor Green } else { Write-Host "FAILED: tutorial_steps.created_at (exit $LASTEXITCODE)" -ForegroundColor Red }

# 3) game_reviews.status
$sql3 = "ALTER TABLE game_reviews ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'published';"
Write-Host "-> Adding game_reviews.status (if missing)"
& psql $ConnectionString -c $sql3
if ($LASTEXITCODE -eq 0) { Write-Host "OK: game_reviews.status ensured." -ForegroundColor Green } else { Write-Host "FAILED: game_reviews.status (exit $LASTEXITCODE)" -ForegroundColor Red }

# OPTIONAL: create indexes for created_at if you expect ORDER BY created_at frequently
# Uncomment the following lines if you want indexes (safe to run IF NOT EXISTS)
# Write-Host "-> Creating index on learning_modules.created_at (optional)"
# & psql $ConnectionString -c "CREATE INDEX IF NOT EXISTS idx_learning_modules_created_at ON learning_modules (created_at);"
# Write-Host "-> Creating index on tutorial_steps.created_at (optional)"
# & psql $ConnectionString -c "C
