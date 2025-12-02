# Quick Start Guide

## 🚀 Get Running in 3 Steps

### 1. Configure API Credentials

Edit [.env](.env) file:

**Option A - Using OpenAI:**
```bash
API_PROVIDER=openai
OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY-HERE
```

**Option B - Using Azure:**
```bash
API_PROVIDER=azure
AZURE_VISION_ENDPOINT=https://YOUR-RESOURCE.cognitiveservices.azure.com/
AZURE_VISION_KEY=YOUR-ACTUAL-KEY-HERE
```

### 2. Start the Application

```bash
source venv/bin/activate
python app.py
```

### 3. Open Browser

Visit: **http://localhost:5000**

---

## ✅ Verify Everything Works

```bash
source venv/bin/activate
python diagnose.py
```

Should show: **"✓ All checks passed!"**

---

## 📝 Use the Application

1. **Add Test Case**
   - Drag & drop an image (or click to upload)
   - Enter expected description
   - Click "Add Test Case"

2. **Run Tests**
   - Click "Run All Tests"
   - View results with charts and detailed table

3. **Check Logs** (if issues)
   ```bash
   ./check_logs.sh
   # or
   tail -f app.log
   ```

---

## 🔧 Troubleshooting

### Getting 500 Error?
✅ **FIXED!** - If you still see it, restart the server:
```bash
# Ctrl+C to stop
python app.py
```

### Tests Failing?
Check your API configuration:
```bash
python diagnose.py
```

### Need More Help?
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed troubleshooting
- [LOGGING_GUIDE.md](LOGGING_GUIDE.md) - How to read logs
- [FIX_SUMMARY.md](FIX_SUMMARY.md) - What was fixed

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Project overview |
| [QUICKSTART.md](QUICKSTART.md) | Original quick start |
| [QUICK_START.md](QUICK_START.md) | This file - simplified start |
| [REACT_UI_GUIDE.md](REACT_UI_GUIDE.md) | React UI documentation |
| [LOGGING_GUIDE.md](LOGGING_GUIDE.md) | Logging system guide |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Troubleshooting guide |
| [FIX_SUMMARY.md](FIX_SUMMARY.md) | Recent fixes summary |

---

## 🎯 Common Commands

```bash
# Start server
python app.py

# Check configuration
python diagnose.py

# View logs
tail -f app.log

# Check for errors
grep ERROR app.log

# Rebuild React UI (after frontend changes)
cd frontend && npm run build
```

---

## ⚡ Quick Tips

- **Always use venv**: `source venv/bin/activate`
- **Monitor logs in real-time**: `tail -f app.log`
- **Check API status first**: `python diagnose.py`
- **Restart after .env changes**: Stop server (Ctrl+C) and restart

---

## 🎨 React UI Features

- **Drag & Drop** - Upload images easily
- **Live Preview** - See images before upload
- **Animated Charts** - Doughnut & Bar charts
- **Real-time Results** - Watch tests run
- **Mobile Responsive** - Works on all devices

---

## 🔐 API Configuration Tips

### OpenAI
- Get key from: https://platform.openai.com/api-keys
- Format: `sk-proj-...`
- Model used: `gpt-4o`

### Azure Computer Vision
- Get from: Azure Portal → Your Vision Resource
- Need both endpoint AND key
- Format: `https://YOUR-RESOURCE.cognitiveservices.azure.com/`

---

**Need help?** Check the logs first: `cat app.log | grep ERROR`
