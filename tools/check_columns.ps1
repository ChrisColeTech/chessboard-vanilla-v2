<#
check_columns_phased_fixed.ps1

Phased column verifier for Postgres (PowerShell)

Phases:
  1) List tables in public schema
  2) List columns for selected tables
  3) Compare actual columns to expected variants and print report + suggested ALTERs

Usage:
  # set DATABASE_URL in session (recommended)
  $env:DATABASE_URL = 'postgresql://user:pass@host:5432/dbname'
  .\check_columns_phased_fixed.ps1

  # or pass connection string:
  .\check_columns_phased_fixed.ps1 -ConnectionString 'postgresql://user:pass@host:5432/dbname?sslmode=require'

Options:
  -AllTables : inspect all tables in public schema (not just defaults)
  -Verbose   : show data_type/is_nullable/ordinal positions
#>

param(
    [string]$ConnectionString = $env:DATABASE_URL,
    [switch]$AllTables = $false,
    [switch]$Verbose = $false
)

if (-not $ConnectionString -or $ConnectionString -eq '') {
    Write-Error "No connection string provided. Set env var DATABASE_URL or pass -ConnectionString."
    exit 2
}

# ensure sslmode present
if ($ConnectionString -notmatch "sslmode=") {
    if ($ConnectionString.Contains('?')) { $ConnectionString = "$ConnectionString&sslmode=require" }
    else { $ConnectionString = "$ConnectionString?sslmode=require" }
}

# Default tables to inspect (the ones that caused errors)
$defaultTables = @('learning_modules','tutorial_steps','game_reviews')

# Expected columns mapping (variants we will check)
$expectedMap = @{
    'learning_modules' = @('created_at','createdAt')
    'tutorial_steps'   = @('created_at','createdAt')
    'game_reviews'     = @('status')
}

function Phase([int]$n, [string]$desc) {
    # use -f formatting to avoid interpolation parsing issues
    Write-Host ("`n===== Phase {0}: {1} =====`n" -f $n, $desc) -ForegroundColor Cyan
}

# Mask connection display for logging
$displayConn = $ConnectionString -replace '\/\/([^:]+):([^@]+)@','//$1:REDACTED@'
Write-Host ("Using connection: {0}" -f $displayConn) -ForegroundColor DarkGray

# ---------- PHASE 1: list tables ----------
Phase 1 "List tables in public schema"
$sqlTables = "SELECT table_name
              FROM information_schema.tables
              WHERE table_schema='public'
              ORDER BY table_name;"
$tablesRaw = & psql $ConnectionString -t -A -c $sqlTables
if ($LASTEXITCODE -ne 0) { Write-Error "psql exited with code $LASTEXITCODE"; exit 3 }

$tables = @()
foreach ($line in $tablesRaw -split "`n") {
    $trim = $line.Trim()
    if ($trim -ne '') { $tables += $trim }
}

if ($AllTables) {
    Write-Host ("Inspecting ALL tables in public schema (count={0})" -f $tables.Count) -ForegroundColor Yellow
    $inspectTables = $tables
} else {
    $inspectTables = @()
    foreach ($t in $defaultTables) {
        if ($tables -contains $t) { $inspectTables += $t }
        else { Write-Host ("Warning: default table '{0}' NOT found in schema." -f $t) -ForegroundColor DarkYellow }
    }
    if ($inspectTables.Count -eq 0) {
        Write-Host "No default tables found -- switching to the first 10 tables from DB." -ForegroundColor Yellow
        $endIndex = [math]::Min(9, $tables.Count - 1)
        if ($endIndex -ge 0) { $inspectTables = $tables[0..$endIndex] }
    }
}

Write-Host "`nTables to inspect:" -ForegroundColor Green
$inspectTables | ForEach-Object { Write-Host "- $_" }

# ---------- PHASE 2: list columns for each table ----------
Phase 2 "List columns for each inspected table"

$columnsMap = @{}

foreach ($table in $inspectTables) {
    Write-Host ("`nColumns for table: {0}" -f $table) -ForegroundColor Yellow
    $sqlCols = "SELECT column_name, data_type, is_nullable, ordinal_position
                FROM information_schema.columns
                WHERE table_schema='public' AND table_name='$table'
                ORDER BY ordinal_position;"
    # use -F '|' to keep output parseable
    $raw = & psql $ConnectionString -t -A -F '|' -c $sqlCols
    if ($LASTEXITCODE -ne 0) {
        Write-Host ("Error running psql for table {0} (exit {1})" -f $table, $LASTEXITCODE) -ForegroundColor Red
        continue
    }
    $cols = @()
    foreach ($rline in $raw -split "`n") {
        $r = $rline.Trim()
        if ($r -eq '') { continue }
        $parts = $r -split '\|'
        $colName = $parts[0].Trim()
        $cols += $colName
        if ($Verbose) {
            $datatype = $parts[1]; $nullable = $parts[2]; $ord = $parts[3]
            Write-Host ("  {0,-30} {1,-20} {2,-8} pos={3}" -f $colName, $datatype, $nullable, $ord)
        } else {
            Write-Host ("  {0}" -f $colName)
        }
    }
    $columnsMap[$table] = $cols
}

# ---------- PHASE 3: verify expected columns ----------
Phase 3 "Verify expected columns vs actual"

foreach ($kv in $expectedMap.GetEnumerator()) {
    $table = $kv.Key
    $expectedList = $kv.Value
    $actual = @()
    if ($columnsMap.ContainsKey($table)) { $actual = $columnsMap[$table] } else { $actual = @() }
    Write-Host ("`n--- Table: {0} ---" -f $table) -ForegroundColor Cyan
    Write-Host ("Actual columns count: {0}" -f $actual.Count) -ForegroundColor DarkGray
    if ($actual.Count -gt 0) {
        Write-Host ("Actual columns: {0}" -f ($actual -join ', ')) -ForegroundColor White
    } else {
        Write-Host "Actual columns: (none)" -ForegroundColor White
    }

    foreach ($expected in $expectedList) {
        $exists = $false
        $note = $null
        if ($actual -contains $expected) {
            $exists = $true
            $note = "found exact"
        } else {
            # check camel/snake swaps for created variants
            if ($expected -eq 'created_at' -and ($actual -contains 'createdAt')) { $exists = $true; $note = "found as createdAt (camelCase)" }
            elseif ($expected -eq 'createdAt' -and ($actual -contains 'created_at')) { $exists = $true; $note = "found as created_at (snake_case)" }
        }

        if ($exists) {
            Write-Host ("✔ Expected '{0}' => PRESENT ({1})" -f $expected, $note) -ForegroundColor Green
        } else {
            Write-Host ("✖ Expected '{0}' => MISSING" -f $expected) -ForegroundColor Red
            if ($expected -match 'created') {
                $alter = "ALTER TABLE $table ADD COLUMN IF NOT EXISTS ""createdAt"" timestamptz NOT NULL DEFAULT now();"
            } elseif ($expected -eq 'status') {
                $alter = "ALTER TABLE $table ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'published';"
            } else {
                $alter = ("-- ALTER TABLE {0} ADD COLUMN IF NOT EXISTS {1} <type>;" -f $table, $expected)
            }
            Write-Host ("  Suggested: {0}" -f $alter) -ForegroundColor DarkYellow
        }
    }
}

Write-Host "`nSummary: inspection complete." -ForegroundColor Cyan
Write-Host "If you want a migration or to run suggested ALTERs, tell me which ones to generate." -ForegroundColor Cyan
