# Unified Logging Integration Demo

The mobile-pages-v2 tool now uses the centralized unified logger! Here's how to use it:

## CLI Configuration

### Basic Usage (Minimal Mode - Default)
```bash
python main.py analyze
# Shows: info, warnings, errors with emojis
```

### Verbose Mode
```bash
python main.py --verbose parent TestPage
python main.py -v analyze
# Shows: all messages including verbose operation details
```

### Silent Mode  
```bash
python main.py --silent validate
python main.py -s analyze
# Shows: only warnings and errors
```

### File Logging
```bash
python main.py --log-file ./logs/generator.log parent TestPage
# Logs to file with timestamps while showing console output
```

### Combined Options
```bash
python main.py --verbose --log-file ./logs/debug.log parent TestPage
# Verbose console output + complete file log

python main.py --silent --log-file ./logs/errors.log validate  
# Silent console + complete file log
```

## What Changed

### Before (Direct Print Statements)
```python
print(f"🚀 Creating parent page: {name}")
print(f"✅ Parent page creation completed")
print(f"❌ Error creating parent page: {e}")
```

### After (Unified Logger)
```python
self.logger.operation(f"Creating parent page: {name}")
self.logger.success("Parent page creation completed") 
self.logger.error(f"Error creating parent page: {e}")
```

## Log Levels in Action

| Level | Console (Minimal) | Console (Verbose) | Console (Silent) | File |
|-------|-------------------|-------------------|------------------|------|
| `verbose()` | ❌ | ✅ | ❌ | ✅ |
| `debug()` | ❌ | ✅ | ❌ | ✅ |
| `info()` | ✅ | ✅ | ❌ | ✅ |
| `success()` | ✅ | ✅ | ❌ | ✅ |
| `operation()` | ✅ | ✅ | ❌ | ✅ |
| `warning()` | ✅ | ✅ | ✅ | ✅ |
| `error()` | ✅ | ✅ | ✅ | ✅ |

## Examples

### Minimal Mode (Default)
```bash
$ python main.py analyze
ℹ️ Analyzing project structure...
⚠️  Project Structure Issues found
✅ Analysis completed
```

### Verbose Mode  
```bash
$ python main.py --verbose analyze
ℹ️ Analyzing project structure...
🔍 Scanning src/components directory
🔍 Checking for existing hook files  
🐛 Found 12 existing components
⚠️  Project Structure Issues found
✅ Analysis completed
```

### Silent Mode
```bash
$ python main.py --silent analyze  
⚠️  Project Structure Issues found
```

### File Output Example
```
2025-09-16 08:35:50 - unified_logger.page_generator - INFO - Analyzing project structure...
2025-09-16 08:35:50 - unified_logger.page_generator - Level 5 - Scanning src/components directory
2025-09-16 08:35:50 - unified_logger.page_generator - DEBUG - Found 12 existing components
2025-09-16 08:35:51 - unified_logger.page_generator - WARNING - Project Structure Issues found
2025-09-16 08:35:51 - unified_logger.page_generator - INFO - Analysis completed
```

## Benefits

1. **Consistent Logging**: All tools can use the same logging framework
2. **Flexible Output**: Choose verbosity based on use case
3. **File Logging**: Debug issues with persistent logs
4. **User-Friendly**: Maintains emoji-based console output
5. **No Breaking Changes**: Same user experience with better control
6. **Production Ready**: Proper log levels and timestamps for production use

## Next Steps

Other tools in the frontend-tools suite can be upgraded to use the same unified logger by:

1. Importing `from unified_logger import create_logger`
2. Adding CLI flags for `--verbose`, `--silent`, `--log-file`  
3. Replacing print statements with appropriate log levels
4. Passing logger to components that need it