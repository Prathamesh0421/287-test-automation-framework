# Quick Start Guide

Get up and running with the Image Description Testing System in 5 minutes!

## 🚀 Setup (3 steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- OpenAI/Azure libraries
- Sentence transformers (for semantic comparison)
- Other required packages

### Step 2: Configure API

Copy and edit the environment file:

```bash
cp .env.example .env
```

**For OpenAI** (recommended for beginners):
```env
API_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key-here
SIMILARITY_THRESHOLD=0.7
```

Get your OpenAI key: https://platform.openai.com/api-keys

**For Azure Computer Vision**:
```env
API_PROVIDER=azure
AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_VISION_KEY=your-key-here
SIMILARITY_THRESHOLD=0.7
```

### Step 3: Verify Setup

Run the verification script:

```bash
python setup.py
```

This checks:
- All dependencies installed ✓
- .env file configured ✓
- API connection working ✓

## 🎯 Using the Web Interface

### Start the Server

```bash
python app.py
```

Open your browser to: **http://localhost:5000**

### Add Test Cases

1. **Upload Image**: Click the upload area or drag & drop
2. **Enter Description**: What the image should show
3. **Click Add**: Test case is saved

Example:
- Image: A photo of your dog
- Description: "A golden retriever playing in a park"

### Run Tests

1. **Click "Run All Tests"**: System will process all images
2. **Wait**: Progress indicator shows testing in progress
3. **View Results**: Charts and detailed comparison appear

## 📊 Understanding Results

### Success Rate
- Green = Test passed (description matches)
- Red = Test failed (description doesn't match)

### Similarity Score
- **90-100%**: Excellent match
- **70-90%**: Good match (default pass threshold)
- **50-70%**: Moderate match
- **<50%**: Poor match

### Adjusting Threshold

In `.env` file:
```env
SIMILARITY_THRESHOLD=0.7  # 70% required to pass
```

- Lower (0.5): More lenient
- Higher (0.9): More strict

## 🧪 Example Test Cases

Try these to get started:

### Test 1: Simple Object
- **Image**: Coffee cup on a table
- **Description**: "A cup of coffee on a wooden table"

### Test 2: Scene
- **Image**: Beach at sunset
- **Description**: "A beach scene during sunset with waves"

### Test 3: Multiple Objects
- **Image**: Office desk with laptop
- **Description**: "A modern office desk with laptop and notebook"

## 💻 Command Line Usage

For automation/CI/CD:

```bash
# Edit test_cases.json with your test cases
python test_runner.py
```

Output:
```
Running automated image description tests...
============================================================
Test Results Summary
============================================================
Total Tests: 10
Passed: 8
Failed: 2
Success Rate: 80.00%
============================================================

✓ PASS | Test 1: 0.89
  Expected: A dog playing in a park
  Actual:   A golden retriever playing outdoors
```

## 🔍 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Invalid API key"
- Check `.env` file
- Verify key is correct
- For OpenAI: Key starts with "sk-"

### "Connection failed"
- Check internet connection
- Verify API endpoint is correct
- Ensure API has credits/is active

### Low similarity scores
- Make descriptions more general
- Avoid very specific details
- Try lowering threshold in `.env`

## 🎓 Tips for Best Results

### Writing Good Descriptions

**Good** ✓:
- "A cat sitting by a window"
- "People walking in a city street"
- "Food on a plate"

**Too Specific** ✗:
- "A gray tabby cat with green eyes sitting by a bay window on Tuesday"
- "Exactly 5 people walking on Madison Avenue"
- "Spaghetti carbonara with exactly 3 basil leaves"

### Choosing Images

- Use clear, well-lit images
- Avoid very complex scenes
- Focus on main subject
- Standard formats (JPG, PNG)

### API Selection

**Use OpenAI if:**
- Need detailed descriptions
- Complex scenes
- Multiple objects
- Better context understanding

**Use Azure if:**
- Simple object detection
- Lower cost priority
- Faster responses needed
- Basic tagging sufficient

## 📈 Next Steps

1. **Try the examples**: `python example.py`
2. **Read full docs**: See `README.md`
3. **Customize**: Adjust thresholds, try different APIs
4. **Automate**: Integrate into your CI/CD pipeline

## ⚡ Common Workflows

### Testing a New Model
```bash
# Update API_PROVIDER in .env
# Run tests
python test_runner.py
```

### Batch Testing
```bash
# Add 10-20 test cases via web UI
# Click "Run All Tests"
# Download results JSON
```

### CI/CD Integration
```bash
# In your CI pipeline:
export OPENAI_API_KEY=$SECRET_KEY
python test_runner.py
# Check exit code
```

## 🆘 Getting Help

1. Check this guide
2. Read `README.md` for detailed docs
3. Run `python setup.py` to verify setup
4. Check API documentation:
   - OpenAI: https://platform.openai.com/docs
   - Azure: https://docs.microsoft.com/azure/cognitive-services/

---

**You're all set!** Start testing your vision models! 🎉
