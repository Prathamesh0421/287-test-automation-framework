# Logging Guide

## Overview

Comprehensive logging has been added to the application to help debug issues and monitor system behavior.

## Log Files

### app.log
- Location: Project root directory
- Contains: All application logs including API calls, errors, and debugging information
- Format: `timestamp - logger_name - level - message`

Example:
```
2025-12-02 00:12:16,123 - __main__ - INFO - POST /api/run-tests - Starting test execution
2025-12-02 00:12:16,124 - __main__ - INFO - Number of test cases: 3
2025-12-02 00:12:16,125 - __main__ - INFO - Similarity threshold: 0.7
```

## Log Levels

- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General information about application flow
- **WARNING**: Warning messages for unusual situations
- **ERROR**: Error messages when something fails

## What Gets Logged

### Application Startup
- Environment variables loaded
- API provider configuration
- Upload/results folder paths

### Test Case Upload
- File information (name, size)
- Description length
- Save location
- Success/failure status

### Test Execution (`/api/run-tests`)
- Number of test cases
- Similarity threshold
- API provider being used
- Vision client initialization
- Test runner initialization
- Each test case execution:
  - Test ID and image path
  - API call to get description
  - Description received
  - Similarity comparison
  - Test result (PASS/FAIL)
- Overall results summary
- Results file save location

### API Client Calls

#### OpenAI Vision Client
- Image file reading
- Image encoding (base64)
- API request sending
- Response status code
- Description received
- Any errors with full stack traces

#### Azure Computer Vision Client
- Image file reading
- API request sending
- Response parsing
- Any errors with full stack traces

### Semantic Comparison
- Model initialization
- Text comparison details
- Similarity scores
- Any errors

## Viewing Logs

### View all logs
```bash
cat app.log
```

### View last 50 lines
```bash
tail -50 app.log
```

### Follow logs in real-time
```bash
tail -f app.log
```

### View only errors
```bash
grep -i "error\|exception" app.log
```

### View specific test execution
```bash
grep "POST /api/run-tests" app.log -A 50
```

## Using the Check Logs Script

A convenience script is provided:

```bash
./check_logs.sh
```

This will display:
- Last 50 lines of the log
- All errors and exceptions
- Environment configuration status

## Common Log Patterns

### Successful Test Run
```
INFO - POST /api/run-tests - Starting test execution
INFO - Number of test cases: 2
INFO - Similarity threshold: 0.7
INFO - API Provider: openai
INFO - Initializing vision client...
INFO - Vision client initialized: OpenAIVisionClient
INFO - Initializing test runner...
INFO - ImageTestRunner initialized successfully
INFO - Running test case #1: uploads/image1.jpg
INFO - Getting description from API for test #1
INFO - OpenAI: Describing image uploads/image1.jpg
INFO - Sending request to OpenAI API...
INFO - OpenAI API response status: 200
INFO - OpenAI description received: A cat sitting on a windowsill...
INFO - Comparing descriptions for test #1
INFO - Similarity score for test #1: 0.8542
INFO - Test #1 PASSED
INFO - Test run completed: 2/2 passed (100.00%)
```

### Failed API Call (OpenAI)
```
ERROR - OpenAI API Error: 401
ERROR - Response: {"error": {"message": "Incorrect API key provided"}}
ERROR - Exception in run_tests: OpenAI API Error: 401 - ...
ERROR - Traceback (most recent call last):
...
```

### Failed API Call (Azure)
```
ERROR - Azure API Error: 404
ERROR - Response: {"error": {"code": "ResourceNotFound"}}
```

### Configuration Error
```
ERROR - ValueError in run_tests: OpenAI API key not configured
ERROR - ValueError in run_tests: Azure credentials not configured
```

### Missing Image File
```
ERROR - Error in test case #1: Image file not found: uploads/missing.jpg
```

## Debugging Steps

1. **Run the application**
   ```bash
   python app.py
   ```

2. **In another terminal, monitor logs**
   ```bash
   tail -f app.log
   ```

3. **Perform the action that's failing**
   - Upload test case
   - Run tests
   - etc.

4. **Check the logs** for the exact error message and stack trace

5. **Use the information** to:
   - Fix configuration issues
   - Verify API credentials
   - Check file paths
   - Debug code issues

## Log Rotation

For production use, consider implementing log rotation:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

## Disabling Debug Logs

If you want less verbose logging, edit [app.py](app.py:31):

```python
# Change this:
logging.basicConfig(level=logging.DEBUG, ...)

# To this:
logging.basicConfig(level=logging.INFO, ...)
```

## Troubleshooting Common Issues

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed troubleshooting steps based on log messages.
