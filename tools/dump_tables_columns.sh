#!/bin/bash
#
# dump_tables_columns.sh
#
# Dump all tables and columns (public schema) from a PostgreSQL DB using psql.
#
# Usage examples:
#   # use env var DATABASE_URL
#   export DATABASE_URL='postgresql://user:pass@host:5432/dbname'
#   ./dump_tables_columns.sh
#
#   # pass connection string explicitly
#   ./dump_tables_columns.sh 'postgresql://user:pass@host:5432/dbname?sslmode=require'
#
#   # also write JSON and CSV
#   ./dump_tables_columns.sh "$DATABASE_URL" tables_columns.json tables_columns.csv
#
# Parameters:
#   $1 : DB URL (optional if DATABASE_URL env var is set)
#   $2 : optional path to write JSON output
#   $3 : optional path to write CSV output

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Function to print colored output
print_error() { echo -e "${RED}Error: $1${NC}" >&2; }
print_success() { echo -e "${GREEN}$1${NC}"; }
print_warning() { echo -e "${YELLOW}$1${NC}"; }
print_info() { echo -e "${CYAN}$1${NC}"; }
print_gray() { echo -e "${GRAY}$1${NC}"; }

# Function to fail with error message
fail() {
    print_error "$1"
    exit 1
}

# Parse arguments
CONNECTION_STRING="${1:-${DATABASE_URL:-}}"
OUT_JSON="${2:-}"
OUT_CSV="${3:-}"

# Validate connection string
if [[ -z "$CONNECTION_STRING" ]]; then
    fail "No connection string provided. Set DATABASE_URL env var or pass as first argument."
fi

# Ensure sslmode is present (common for Supabase)
if [[ ! "$CONNECTION_STRING" =~ sslmode= ]]; then
    if [[ "$CONNECTION_STRING" =~ \? ]]; then
        CONNECTION_STRING="${CONNECTION_STRING}&sslmode=require"
    else
        CONNECTION_STRING="${CONNECTION_STRING}?sslmode=require"
    fi
fi

# Check if psql is available
if ! command -v psql &> /dev/null; then
    fail "psql not found on PATH. Please install the PostgreSQL client (psql)."
fi

# Mask password in connection string for display
MASKED_CONNECTION=$(echo "$CONNECTION_STRING" | sed 's|://[^:]*:[^@]*@|://user:REDACTED@|g')
print_gray "Using connection: $MASKED_CONNECTION"

# SQL query to get table and column information
SQL="SELECT table_schema, table_name, column_name, data_type, is_nullable, column_default, ordinal_position
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_schema, table_name, ordinal_position;"

# Execute psql and get pipe-delimited output
echo "Querying database..."
if ! RAW_OUTPUT=$(psql "$CONNECTION_STRING" -t -A -F '|' -c "$SQL" 2>/dev/null); then
    fail "psql failed. Check connection string and credentials."
fi

# Create temporary files for processing
TEMP_DIR=$(mktemp -d)
TEMP_FILE="$TEMP_DIR/raw_output.txt"
JSON_TEMP="$TEMP_DIR/tables.json"
CSV_TEMP="$TEMP_DIR/tables.csv"

# Clean up temp directory on exit
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Save raw output to temp file
echo "$RAW_OUTPUT" > "$TEMP_FILE"

# Process the output and build table structure
declare -A TABLES
declare -A TABLE_COLUMNS

while IFS='|' read -r schema table_name column_name data_type is_nullable column_default ordinal_position; do
    # Skip empty lines
    [[ -n "$schema" ]] || continue
    
    # Create table key
    table_key="${schema}.${table_name}"
    
    # Initialize table if not exists
    if [[ -z "${TABLES[$table_key]:-}" ]]; then
        TABLES[$table_key]="$table_key"
        TABLE_COLUMNS[$table_key]=""
    fi
    
    # Add column info
    TABLE_COLUMNS[$table_key]+="$ordinal_position|$column_name|$data_type|$is_nullable|$column_default"$'\n'
    
done < "$TEMP_FILE"

# Print readable report
print_info "\n=== TABLES AND COLUMNS (public schema) ===\n"

# Sort table keys and display
for table_key in $(printf '%s\n' "${!TABLES[@]}" | sort); do
    print_warning "Table: $table_key"
    
    # Sort columns by ordinal position and display
    echo "${TABLE_COLUMNS[$table_key]}" | sort -t'|' -k1,1n | while IFS='|' read -r pos col_name data_type nullable default_val; do
        [[ -n "$pos" ]] || continue
        
        # Format default value
        if [[ -n "$default_val" && "$default_val" != " " ]]; then
            default_display=" default=$default_val"
        else
            default_display=""
        fi
        
        # Format and print column info
        printf "  [%2d] %-30s %-15s %-8s%s\n" "$pos" "$col_name" "$data_type" "$nullable" "$default_display"
    done
    echo
done

# Export to JSON if requested
if [[ -n "$OUT_JSON" ]]; then
    echo "Generating JSON output..."
    
    # Start JSON structure
    echo '[' > "$JSON_TEMP"
    
    first_table=true
    for table_key in $(printf '%s\n' "${!TABLES[@]}" | sort); do
        # Add comma separator for subsequent tables
        if [[ "$first_table" == "true" ]]; then
            first_table=false
        else
            echo ',' >> "$JSON_TEMP"
        fi
        
        echo "  {" >> "$JSON_TEMP"
        echo "    \"table\": \"$table_key\"," >> "$JSON_TEMP"
        echo "    \"columns\": [" >> "$JSON_TEMP"
        
        # Process columns for this table
        first_column=true
        echo "${TABLE_COLUMNS[$table_key]}" | sort -t'|' -k1,1n | while IFS='|' read -r pos col_name data_type nullable default_val; do
            [[ -n "$pos" ]] || continue
            
            # Add comma separator for subsequent columns
            if [[ "$first_column" == "true" ]]; then
                first_column=false
            else
                echo ',' >> "$JSON_TEMP"
            fi
            
            # Escape JSON strings
            col_name_escaped=$(echo "$col_name" | sed 's/"/\\"/g')
            data_type_escaped=$(echo "$data_type" | sed 's/"/\\"/g')
            nullable_escaped=$(echo "$nullable" | sed 's/"/\\"/g')
            default_escaped=$(echo "$default_val" | sed 's/"/\\"/g')
            
            echo "      {" >> "$JSON_TEMP"
            echo "        \"table_schema\": \"public\"," >> "$JSON_TEMP"
            echo "        \"table_name\": \"$(echo "$table_key" | cut -d'.' -f2)\"," >> "$JSON_TEMP"
            echo "        \"column_name\": \"$col_name_escaped\"," >> "$JSON_TEMP"
            echo "        \"data_type\": \"$data_type_escaped\"," >> "$JSON_TEMP"
            echo "        \"is_nullable\": \"$nullable_escaped\"," >> "$JSON_TEMP"
            echo "        \"column_default\": \"$default_escaped\"," >> "$JSON_TEMP"
            echo "        \"ordinal_position\": $pos" >> "$JSON_TEMP"
            echo "      }" >> "$JSON_TEMP"
        done
        
        echo "    ]" >> "$JSON_TEMP"
        echo "  }" >> "$JSON_TEMP"
    done
    
    echo ']' >> "$JSON_TEMP"
    
    # Copy to output file
    cp "$JSON_TEMP" "$OUT_JSON"
    print_success "Wrote JSON to $OUT_JSON"
fi

# Export to CSV if requested
if [[ -n "$OUT_CSV" ]]; then
    echo "Generating CSV output..."
    
    # CSV header
    echo "table,ordinal_position,column_name,data_type,is_nullable,column_default" > "$CSV_TEMP"
    
    # Process all tables and columns
    for table_key in $(printf '%s\n' "${!TABLES[@]}" | sort); do
        echo "${TABLE_COLUMNS[$table_key]}" | sort -t'|' -k1,1n | while IFS='|' read -r pos col_name data_type nullable default_val; do
            [[ -n "$pos" ]] || continue
            
            # Escape CSV fields (quote fields containing commas, quotes, or newlines)
            escape_csv() {
                local field="$1"
                if [[ "$field" =~ [,\"$'\n'] ]]; then
                    # Escape quotes by doubling them and wrap in quotes
                    echo "\"$(echo "$field" | sed 's/"/"""/g')\""
                else
                    echo "$field"
                fi
            }
            
            table_escaped=$(escape_csv "$table_key")
            col_name_escaped=$(escape_csv "$col_name")
            data_type_escaped=$(escape_csv "$data_type")
            nullable_escaped=$(escape_csv "$nullable")
            default_escaped=$(escape_csv "$default_val")
            
            echo "$table_escaped,$pos,$col_name_escaped,$data_type_escaped,$nullable_escaped,$default_escaped" >> "$CSV_TEMP"
        done
    done
    
    # Copy to output file
    cp "$CSV_TEMP" "$OUT_CSV"
    print_success "Wrote CSV to $OUT_CSV"
fi

print_info "\nDone."