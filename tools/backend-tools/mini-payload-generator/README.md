# Mini Payload Generator for Debugging

This is a focused payload generator specifically designed to troubleshoot the 8 failing API endpoints.

## Purpose

The main payload generator achieved 87.7% success rate (57/65 endpoints), but 8 endpoints are still failing with JSON formatting and foreign key constraint issues. This mini generator creates isolated, debuggable payloads for those specific endpoints.

## Failing Endpoints

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
# Generate debug payloads
python3 mini_payload_generator.py

# Run focused tests
python3 ../payload-tests/focused_endpoint_tests.py
```

## Features

- Uses real database IDs from `real_test_ids.json`
- Proper JSON formatting for API payloads (not database storage)
- Focused on the specific failure patterns
- Includes payload analysis and validation
- Generates minimal, debuggable test cases