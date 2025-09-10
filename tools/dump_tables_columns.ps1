<#
dump_tables_columns.ps1

Dump all tables and columns (public schema) from a PostgreSQL DB using psql.

Usage examples:
  # use env var DATABASE_URL
  $env:DATABASE_URL = 'postgresql://user:pass@host:5432/dbname'
  .\dump_tables_columns.ps1

  # pass connection string explicitly
  .\dump_tables_columns.ps1 -ConnectionString 'postgresql://user:pass@host:5432/dbname?sslmode=require'

  # also write JSON and CSV
  .\dump_tables_columns.ps1 -ConnectionString $env:DATABASE_URL -OutJson 'tables_columns.json' -OutCsv 'tables_columns.csv'

Parameters:
  -ConnectionString  : DB URL (optional if $env:DATABASE_URL is set)
  -OutJson           : optional path to write JSON output
  -OutCsv            : optional path to write CSV output
#>

param(
    [string]$ConnectionString = $env:DATABASE_URL,
    [string]$OutJson = $null,
    [string]$OutCsv = $null
)

function Fail([string]$m) { Write-Error $m; exit 1 }

if (-not $ConnectionString -or $ConnectionString -eq '') {
    Fail "No connection string provided. Set env:DATABASE_URL or pass -ConnectionString."
}

# ensure sslmode present (common for Supabase)
if ($ConnectionString -notmatch "sslmode=") {
    if ($ConnectionString.Contains('?')) { $ConnectionString = "$ConnectionString&sslmode=require" }
    else { $ConnectionString = "$ConnectionString?sslmode=require" }
}

# check psql
if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
    Fail "psql not found on PATH. Please install the PostgreSQL client (psql)."
}

# masked display
$masked = $ConnectionString -replace '\/\/([^:]+):([^@]+)@','//$1:REDACTED@'
Write-Host "Using connection: $masked" -ForegroundColor DarkGray

# SQL: select schema.table & columns
$sql = @"
SELECT table_schema, table_name, column_name, data_type, is_nullable, column_default, ordinal_position
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_schema, table_name, ordinal_position;
"@

# run psql, get pipe-delimited rows
$raw = & psql $ConnectionString -t -A -F '|' -c $sql
if ($LASTEXITCODE -ne 0) { Fail "psql failed (exit $LASTEXITCODE). Check connection/credentials." }

# parse into objects grouped by table
$tablesMap = @{}   # key = "schema.table"
$rows = $raw -split "`n" | Where-Object { $_.Trim() -ne '' }

foreach ($line in $rows) {
    $parts = $line -split '\|'
    # defensive: ensure we have 7 columns
    if ($parts.Count -lt 7) { continue }
    $schema = $parts[0].Trim()
    $table  = $parts[1].Trim()
    $col    = $parts[2].Trim()
    $dtype  = $parts[3].Trim()
    $nullable = $parts[4].Trim()
    $default  = $parts[5].Trim()
    $pos      = [int]$parts[6].Trim()

    $key = "$schema.$table"
    if (-not $tablesMap.ContainsKey($key)) {
        $tablesMap[$key] = @()
    }

    $tablesMap[$key] += [PSCustomObject]@{
        table_schema = $schema
        table_name   = $table
        column_name  = $col
        data_type    = $dtype
        is_nullable  = $nullable
        column_default = $default
        ordinal_position = $pos
    }
}

# Print readable report
Write-Host "`n=== TABLES AND COLUMNS (public schema) ===`n" -ForegroundColor Cyan
foreach ($k in ($tablesMap.Keys | Sort-Object)) {
    Write-Host "Table: $k" -ForegroundColor Yellow
    $cols = $tablesMap[$k] | Sort-Object ordinal_position
    foreach ($c in $cols) {
        $def = if ($c.column_default -and $c.column_default -ne '') { " default=$($c.column_default)" } else { "" }
        Write-Host ("  [{0,2}] {1,-30} {2,-15} {3,-8}{4}" -f $c.ordinal_position, $c.column_name, $c.data_type, $c.is_nullable, $def)
    }
    Write-Host ""
}

# Optionally export to JSON
if ($OutJson) {
    $all = @()
    foreach ($k in $tablesMap.Keys) {
        $entry = [PSCustomObject]@{
            table = $k
            columns = $tablesMap[$k] | Sort-Object ordinal_position
        }
        $all += $entry
    }
    $json = $all | ConvertTo-Json -Depth 5
    $json | Out-File -FilePath $OutJson -Encoding utf8
    Write-Host ("Wrote JSON to {0}" -f $OutJson) -ForegroundColor Green
}

# Optionally export to CSV (flattened rows)
if ($OutCsv) {
    $flat = @()
    foreach ($k in $tablesMap.Keys) {
        foreach ($c in $tablesMap[$k]) {
            $flat += [PSCustomObject]@{
                table = $k
                ordinal_position = $c.ordinal_position
                column_name = $c.column_name
                data_type = $c.data_type
                is_nullable = $c.is_nullable
                column_default = $c.column_default
            }
        }
    }
    $flat | Sort-Object table, ordinal_position | Export-Csv -Path $OutCsv -NoTypeInformation -Encoding UTF8
    Write-Host ("Wrote CSV to {0}" -f $OutCsv) -ForegroundColor Green
}

Write-Host "`nDone." -ForegroundColor Cyan
