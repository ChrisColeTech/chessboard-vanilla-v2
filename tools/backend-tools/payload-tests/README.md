# Focused Endpoint Tests

This directory contains a specialized test suite designed to troubleshoot the 8 failing API endpoints that are preventing 100% test success.

## Purpose

After achieving 87.7% success rate (57/65 endpoints) with the main test suite, 8 endpoints remain failing. This focused test suite isolates these problematic endpoints to identify the root causes.

## Failing Endpoints Being Tested

1. **POST /api/content/** - 400 Bad Request (invalid JSON syntax)
2. **PUT /api/content/** - 400 Bad Request (invalid JSON syntax)  
3. **POST /api/puzzles/** - 400 Bad Request (invalid JSON syntax)
4. **GET /api/puzzles/** - 400 Bad Request (JSON parse error)
5. **PUT /api/puzzles/** - 400 Bad Request (invalid JSON syntax)
6. **GET /api/puzzles/** - 400 Bad Request (JSON parse error)
7. **POST /api/user-achievements/** - 400 Bad Request (foreign key constraint)
8. **DELETE /api/users/** - 400 Bad Request (foreign key constraint)

## Usage

```bash
# Run the focused tests
cd /mnt/c/Projects/chessboard-vanilla-v2/tools/backend-tools/payload-tests
python3 focused_endpoint_tests.py

# Generate debug payloads first (optional)
cd ../mini-payload-generator
python3 mini_payload_generator.py
```

## Features

- **Isolated Testing**: Tests only the failing endpoints for focused debugging
- **Detailed Error Analysis**: Captures full error responses and payloads
- **Real Database IDs**: Uses actual IDs from the database for foreign key relationships
- **JSON Debugging**: Specifically addresses JSON formatting issues
- **Verbose Logging**: Shows exact payloads being sent and responses received

## Expected Outcomes

This test suite will help identify:
- Specific JSON formatting issues in content and puzzle payloads
- Foreign key constraint violations in user-achievements and user deletion
- Parameter parsing issues in GET requests
- Exact error messages and response codes

## Files

- `focused_endpoint_tests.py` - Main test runner
- `focused_test_results.json` - Generated test results (after running)
- `README.md` - This documentation