# Troubleshooting Guide

## Common Issues and Solutions

### Issue: Getting 500 Error when clicking "Run All Tests"

#### Root Cause
The 500 error typically occurs due to one of these reasons:
1. **API credentials not configured properly**
2. **Azure endpoint is a placeholder**
3. **Missing or incorrect API keys**
4. **Network/API connectivity issues**

#### Solution Steps

**Step 1: Check Your Configuration**

Run the diagnostic tool:
```bash
source venv/bin/activate
python diagnose.py
```

This will check:
- All dependencies are installed
- API provider is set correctly
- API credentials are configured
- Required directories exist

**Step 2: Configure Your API Provider**

You need to choose ONE of the following:

#### Option A: Using Azure Computer Vision

1. Open [.env](.env) file
2. Update these lines:
   ```bash
   API_PROVIDER=azure
   AZURE_VISION_ENDPOINT=https://YOUR-RESOURCE-NAME.cognitiveservices.azure.com/
   AZURE_VISION_KEY=YOUR-ACTUAL-AZURE-KEY
   ```

   **Important:**
   - Replace `YOUR-RESOURCE-NAME` with your actual Azure resource name
   - Replace `YOUR-ACTUAL-AZURE-KEY` with your Azure Computer Vision API key
   - Get these from Azure Portal → Your Computer Vision resource → Keys and Endpoint

#### Option B: Using OpenAI GPT-4 Vision

1. Open [.env](.env) file
2. Update these lines:
   ```bash
   API_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-your-actual-openai-key-here
   ```

   **Important:**
   - Replace with your actual OpenAI API key
   - Get your key from: https://platform.openai.com/api-keys

**Step 3: Check the Logs**

After configuring, run the app and check logs:

```bash
# Start the app
source venv/bin/activate
python app.py

# In another terminal, check logs
tail -f app.log
```

Look for error messages when you click "Run All Tests". The logs will show:
- Which API provider is being used
- API calls being made
- Any error messages
- Detailed stack traces

**Step 4: Test with a Single Test Case**

1. Add just ONE test case first
2. Click "Run All Tests"
3. Check the logs for specific error messages

### Common Error Messages

#### "OpenAI API key not configured"
- **Cause**: OPENAI_API_KEY is missing or set to placeholder
- **Fix**: Update .env with your actual OpenAI API key

#### "Azure credentials not configured"
- **Cause**: AZURE_VISION_ENDPOINT or AZURE_VISION_KEY is missing/placeholder
- **Fix**: Update .env with your actual Azure credentials

#### "Failed to initialize SentenceTransformer"
- **Cause**: Model download issue or insufficient disk space
- **Fix**:
  ```bash
  source venv/bin/activate
  python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
  ```

#### "OpenAI API Error: 401"
- **Cause**: Invalid OpenAI API key
- **Fix**: Verify your API key is correct and active

#### "OpenAI API Error: 429"
- **Cause**: Rate limit exceeded or insufficient credits
- **Fix**: Check your OpenAI account billing and rate limits

#### "Azure API Error: 401"
- **Cause**: Invalid Azure API key
- **Fix**: Verify your key from Azure Portal

#### "Azure API Error: 404"
- **Cause**: Incorrect Azure endpoint URL
- **Fix**: Verify endpoint URL from Azure Portal

### Checking Your Current Configuration

Run this command to see what's actually loaded:

```bash
source venv/bin/activate
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print(f'API Provider: {os.getenv(\"API_PROVIDER\", \"not set\")}')
print(f'Has OpenAI Key: {\"yes\" if os.getenv(\"OPENAI_API_KEY\") and not os.getenv(\"OPENAI_API_KEY\").startswith(\"your-\") else \"no\"}')
print(f'Has Azure Endpoint: {\"yes\" if os.getenv(\"AZURE_VISION_ENDPOINT\") and not \"your-resource\" in os.getenv(\"AZURE_VISION_ENDPOINT\") else \"no\"}')
print(f'Has Azure Key: {\"yes\" if os.getenv(\"AZURE_VISION_KEY\") else \"no\"}')
"
```

### Still Having Issues?

1. **Check app.log** - The detailed logs will show exactly what's failing
   ```bash
   cat app.log | grep -i error
   ```

2. **Test API connectivity**
   ```bash
   # For OpenAI
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR-API-KEY"

   # For Azure
   curl -H "Ocp-Apim-Subscription-Key: YOUR-KEY" \
     "YOUR-ENDPOINT/vision/v3.2/analyze?visualFeatures=Description"
   ```

3. **Check Python environment**
   ```bash
   source venv/bin/activate
   which python  # Should point to venv/bin/python
   pip list | grep -i "flask\|torch\|sentence"
   ```

4. **Restart the application**
   - Stop the Flask server (Ctrl+C)
   - Clear the log: `rm app.log`
   - Start again: `python app.py`
   - Try running tests
   - Check the new log: `cat app.log`

## Quick Fix Checklist

- [ ] `.env` file exists in the project root
- [ ] API_PROVIDER is set to either "azure" or "openai"
- [ ] Corresponding API credentials are configured (not placeholders)
- [ ] Virtual environment is activated (`source venv/bin/activate`)
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] Application is running (`python app.py`)
- [ ] Check logs for specific error messages (`tail -f app.log`)

## Example Working Configurations

### Working .env for Azure
```bash
API_PROVIDER=azure
AZURE_VISION_ENDPOINT=https://myresource.cognitiveservices.azure.com/
AZURE_VISION_KEY=abc123def456...
SIMILARITY_THRESHOLD=0.7
```

### Working .env for OpenAI
```bash
API_PROVIDER=openai
OPENAI_API_KEY=sk-proj-abc123def456...
SIMILARITY_THRESHOLD=0.7
```
