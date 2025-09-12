param(
    [string]$ConnectionString = $env:DATABASE_URL
)

function Fail($msg) { Write-Error $msg; exit 1 }

if (-not $ConnectionString -or $ConnectionString -eq '') {
    Fail "No connection string provided. Set env:DATABASE_URL or pass -ConnectionString."
}

# Ensure sslmode is present for Supabase / cloud DBs
if ($ConnectionString -notmatch "sslmode=") {
    if ($ConnectionString.Contains('?')) { $ConnectionString = "$ConnectionString&sslmode=require" }
    else { $ConnectionString = "$ConnectionString?sslmode=require" }
}

# Masked display for logs
$masked = $ConnectionString -replace '\/\/([^:]+):([^@]+)@','//$1:REDACTED@'
Write-Host ("Using connection: {0}" -f $masked) -ForegroundColor DarkGray

# Require psql
if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
    Fail "psql not found on PATH. Install the PostgreSQL client (psql) before running."
}

# quick connectivity test
Write-Host "`nTesting DB connectivity..." -ForegroundColor Cyan
& psql $ConnectionString -c "SELECT 1;" > $null 2>&1
if ($LASTEXITCODE -ne 0) { Fail "psql failed to connect using that connection string. Check credentials/network." }
Write-Host "Connection OK." -ForegroundColor Green

# timestamp for backups
$ts = Get-Date -Format "yyyyMMddHHmmss"

# helper that runs SQL and fails nicely if psql returns error code
function RunSql($sql) {
    Write-Host ("SQL> {0}" -f $sql) -ForegroundColor DarkGray
    & psql $ConnectionString -v ON_ERROR_STOP=1 -c $sql
    if ($LASTEXITCODE -ne 0) {
        Fail ("psql returned exit code $LASTEXITCODE for SQL: $sql")
    }
}

# helper to check whether column exists
function ColumnExists($table, $col) {
    $q = "SELECT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_schema='public' AND table_name = '$table' AND column_name = '$col'
         )::text;"
    $res = & psql $ConnectionString -t -A -c $q
    return ($res.Trim() -eq 't')
}

# helper to check whether column is nullable = NO
function IsNotNullable($table, $col) {
    $q = "SELECT is_nullable FROM information_schema.columns
          WHERE table_schema='public' AND table_name = '$table' AND column_name = '$col';"
    $res = (& psql $ConnectionString -t -A -c $q).Trim()
    return ($res -eq 'NO')
}

# Tables we will operate on (targeted)
$targets = @('games','user_study_plans','user_sessions','subscriptions','user_analytics')

Write-Host "`nCreating backups (per-table)..." -ForegroundColor Cyan
foreach ($t in $targets) {
    $backup = "${t}_backup_$ts"
    $sqlBackup = "CREATE TABLE IF NOT EXISTS $backup AS TABLE $t;"
    try {
        RunSql $sqlBackup
        Write-Host ("Backed up {0} -> {1}" -f $t, $backup) -ForegroundColor Green
    } catch {
        Write-Host ("Warning: backup failed for {0}. Skipping further actions for that table." -f $t) -ForegroundColor Yellow
    }
}

# 1) Make games.user_id nullable (drop NOT NULL) to stop null-insert errors
Write-Host "`n--- Fix: games.user_id nullability ---" -ForegroundColor Cyan
if (ColumnExists 'games' 'user_id') {
    if (IsNotNullable 'games' 'user_id') {
        Write-Host "Dropping NOT NULL constraint on games.user_id..."
        RunSql "ALTER TABLE games ALTER COLUMN user_id DROP NOT NULL;"
        Write-Host "OK: games.user_id is now nullable." -ForegroundColor Green
    } else {
        Write-Host "games.user_id already nullable." -ForegroundColor DarkGray
    }
} else {
    Write-Host "games.user_id does not exist — adding a nullable user_id (uuid) column..."
    RunSql "ALTER TABLE games ADD COLUMN IF NOT EXISTS user_id uuid;"
    Write-Host "OK: added games.user_id (nullable uuid)." -ForegroundColor Green
}

# 2) Make user_study_plans.user_id nullable
Write-Host "`n--- Fix: user_study_plans.user_id nullability ---" -ForegroundColor Cyan
if (ColumnExists 'user_study_plans' 'user_id') {
    if (IsNotNullable 'user_study_plans' 'user_id') {
        Write-Host "Dropping NOT NULL constraint on user_study_plans.user_id..."
        RunSql "ALTER TABLE user_study_plans ALTER COLUMN user_id DROP NOT NULL;"
        Write-Host "OK: user_study_plans.user_id is now nullable." -ForegroundColor Green
    } else {
        Write-Host "user_study_plans.user_id already nullable." -ForegroundColor DarkGray
    }
} else {
    Write-Host "user_study_plans.user_id does not exist — adding a nullable user_id (uuid) column..."
    RunSql "ALTER TABLE user_study_plans ADD COLUMN IF NOT EXISTS user_id uuid;"
    Write-Host "OK: added user_study_plans.user_id (nullable uuid)." -ForegroundColor Green
}

# 3) Ensure user_sessions.updated_at exists (NOT NULL DEFAULT now())
Write-Host "`n--- Fix: user_sessions.updated_at ---" -ForegroundColor Cyan
if (-not (ColumnExists 'user_sessions' 'updated_at')) {
    Write-Host "Adding user_sessions.updated_at (timestamptz NOT NULL DEFAULT now())..."
    RunSql "ALTER TABLE user_sessions ADD COLUMN IF NOT EXISTS updated_at timestamptz NOT NULL DEFAULT now();"
    Write-Host "OK: user_sessions.updated_at added." -ForegroundColor Green
} else {
    Write-Host "user_sessions.updated_at already exists." -ForegroundColor DarkGray
}

# 4) Ensure subscriptions.updated_at exists (NOT NULL DEFAULT now())
Write-Host "`n--- Fix: subscriptions.updated_at ---" -ForegroundColor Cyan
if (-not (ColumnExists 'subscriptions' 'updated_at')) {
    Write-Host "Adding subscriptions.updated_at (timestamptz NOT NULL DEFAULT now())..."
    RunSql "ALTER TABLE subscriptions ADD COLUMN IF NOT EXISTS updated_at timestamptz NOT NULL DEFAULT now();"
    Write-Host "OK: subscriptions.updated_at added." -ForegroundColor Green
} else {
    Write-Host "subscriptions.updated_at already exists." -ForegroundColor DarkGray
}

# 5) Ensure user_analytics.created_at exists (NOT NULL DEFAULT now())
Write-Host "`n--- Fix: user_analytics.created_at ---" -ForegroundColor Cyan
if (-not (ColumnExists 'user_analytics' 'created_at')) {
    Write-Host "Adding user_analytics.created_at (timestamptz NOT NULL DEFAULT now())..."
    RunSql "ALTER TABLE user_analytics ADD COLUMN IF NOT EXISTS created_at timestamptz NOT NULL DEFAULT now();"
    Write-Host "OK: user_analytics.created_at added." -ForegroundColor Green
} else {
    Write-Host "user_analytics.created_at already exists." -ForegroundColor DarkGray
}

# Final verification: list columns for the target tables
Write-Host "`nVerification: columns for target tables" -ForegroundColor Cyan
foreach ($t in $targets) {
    Write-Host ("`n-- {0} --" -f $t) -ForegroundColor Yellow
    RunSql "SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_schema='public' AND table_name='$t' ORDER BY ordinal_position;"
}

Write-Host "`nDone. Restart your backend and re-test the failing endpoints (POST /api/games, enroll, sessions, subscriptions, analytics events)." -ForegroundColor Green
Write-Host "NOTE: These are pragmatic, fast fixes to stop errors. For long-term health, convert them to tracked migrations and fix the app to supply user_id where appropriate." -ForegroundColor Yellow
