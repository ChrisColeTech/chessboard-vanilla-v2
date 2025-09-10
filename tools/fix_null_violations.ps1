<#
fix_null_violations.ps1

Purpose:
  - Stop the "null value violates not-null constraint" and "column does not exist" errors you posted
  - Works idempotently: safe to re-run

Usage:
  .\fix_null_violations.ps1 -ConnectionString 'postgresql://postgres:....?sslmode=require'

Targets:
  - games.user_id            => ensure column exists & DROP NOT NULL if present
  - user_study_plans.user_id => ensure column exists & DROP NOT NULL if present
  - user_sessions.user_id    => ensure column exists & DROP NOT NULL if present
  - subscriptions.tier       => ensure column exists & DROP NOT NULL if present

Notes:
  - This is a pragmatic fix to stop the runtime errors. Ideally you should fix the app so inserts include user_id and tier where required, then convert these quick fixes into tracked DB migrations.
#>

param(
    [string]$ConnectionString = $env:DATABASE_URL
)

function Fail($m) { Write-Error $m; exit 1 }

if (-not $ConnectionString -or $ConnectionString -eq '') {
    Fail "No connection string provided. Set env:DATABASE_URL or pass -ConnectionString."
}

# ensure sslmode param for cloud DB if omitted
if ($ConnectionString -notmatch "sslmode=") {
    if ($ConnectionString.Contains('?')) { $ConnectionString = "$ConnectionString&sslmode=require" }
    else { $ConnectionString = "$ConnectionString?sslmode=require" }
}

# require psql
if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
    Fail "psql not found on PATH. Install the PostgreSQL client (psql) before running."
}

# masked display
$masked = $ConnectionString -replace '\/\/([^:]+):([^@]+)@','//$1:REDACTED@'
Write-Host "Using connection: $masked" -ForegroundColor DarkGray

# small helper to run SQL and fail on error
function RunSql($sql) {
    Write-Host "SQL> $sql" -ForegroundColor DarkGray
    & psql $ConnectionString -v ON_ERROR_STOP=1 -c $sql
    if ($LASTEXITCODE -ne 0) {
        Fail "psql failed (exit $LASTEXITCODE) for: $sql"
    }
}

# helper: returns 't' or 'f' as string
function ColumnExists($table, $col) {
    $q = "SELECT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_schema='public' AND table_name = '$table' AND column_name = '$col'
          )::text;"
    $res = (& psql $ConnectionString -t -A -c $q)
    return $res.Trim() -eq 't'
}

function IsNotNullable($table, $col) {
    $q = "SELECT is_nullable FROM information_schema.columns
          WHERE table_schema='public' AND table_name = '$table' AND column_name = '$col';"
    $res = (& psql $ConnectionString -t -A -c $q).Trim()
    return ($res -eq 'NO')
}

# targets (table -> column)
$operations = @(
    @{ table='games';            column='user_id' },
    @{ table='user_study_plans'; column='user_id' },
    @{ table='user_sessions';    column='user_id' },
    @{ table='subscriptions';    column='tier' }
)

# create backups
$ts = Get-Date -Format "yyyyMMddHHmmss"
Write-Host "`nCreating backups for target tables..." -ForegroundColor Cyan
foreach ($op in $operations) {
    $t = $op.table
    $bk = "${t}_backup_$ts"
    try {
        RunSql "CREATE TABLE IF NOT EXISTS $bk AS TABLE $t;"
        Write-Host ("Backed up {0} -> {1}" -f $t, $bk) -ForegroundColor Green
    } catch {
        Write-Host ("Warning: backup failed for {0}. Error: $_" -f $t) -ForegroundColor Yellow
    }
}

# ensure columns exist, add if missing (character varying), then drop NOT NULL if present
foreach ($op in $operations) {
    $t = $op.table
    $c = $op.column
    Write-Host "`n--- Table: $t / Column: $c ---" -ForegroundColor Cyan

    if (-not (ColumnExists $t $c)) {
        # add column as character varying (matches most of your schema); nullable by default
        Write-Host "Column $c does not exist on $t — adding as character varying (nullable)..."
        RunSql "ALTER TABLE $t ADD COLUMN IF NOT EXISTS $c character varying;"
        Write-Host "Added $t.$c (nullable character varying)." -ForegroundColor Green
    } else {
        Write-Host "Column $c already exists on $t." -ForegroundColor DarkGray
    }

    # If column exists and is NOT NULL, drop the NOT NULL constraint
    if (IsNotNullable $t $c) {
        Write-Host "Column $t.$c is NOT NULL — dropping NOT NULL constraint..."
        RunSql "ALTER TABLE $t ALTER COLUMN $c DROP NOT NULL;"
        Write-Host "Dropped NOT NULL on $t.$c." -ForegroundColor Green
    } else {
        Write-Host "$t.$c already nullable." -ForegroundColor DarkGray
    }
}

# Extra safety: if subscriptions.tier still has many NULLs and you prefer a default value,
# you can set a default and (optionally) update existing NULLs. We won't force that here,
# but show the SQL for your review.
Write-Host "`nIf you want to set a default for subscriptions.tier (recommended long-term), you can run:" -ForegroundColor Yellow
Write-Host "  ALTER TABLE subscriptions ALTER COLUMN tier SET DEFAULT 'free';"
Write-Host "  UPDATE subscriptions SET tier='free' WHERE tier IS NULL;"
Write-Host "  -- then optionally: ALTER TABLE subscriptions ALTER COLUMN tier SET NOT NULL;"

# Final verification: show columns for the modified tables
Write-Host "`nFinal verification of target tables (columns):" -ForegroundColor Cyan
foreach ($op in $operations) {
    $t = $op.table
    Write-Host "`n-- $t --" -ForegroundColor Yellow
    RunSql "SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema='public' AND table_name = '$t'
            ORDER BY ordinal_position;"
}

Write-Host "`nDone. Restart your backend and re-test the failing endpoints (POST /api/games, POST /api/sessions/create, enroll, subscriptions).`n" -ForegroundColor Green
Write-Host "Reminder: these changes allow NULL values to be inserted. For production, prefer adding defaults or fixing the app to always provide required fields and then re-enforce NOT NULL via a proper migration." -ForegroundColor Yellow
