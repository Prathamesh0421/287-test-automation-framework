# 🖼️ Image Description Testing System

An automated testing framework for evaluating image description APIs using semantic similarity comparison. Features a web interface for managing test cases and visualizing results.

## 📋 Features

- **Multiple API Support**: 
  - OpenAI GPT-4 Vision
  - Azure Computer Vision
- **Semantic Comparison**: Uses sentence transformers for contextual matching
- **Web Interface**: Upload images, manage test cases, and visualize results
- **Automated Testing**: Run batch tests with detailed reporting
- **Visual Analytics**: Charts and graphs showing test performance
- **REST API**: Full API for programmatic access

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- API keys for either OpenAI or Azure Computer Vision

### Installation

1. **Clone or download the repository**

```bash
cd image_test_automation
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API credentials:

**For OpenAI:**
```env
API_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key-here
SIMILARITY_THRESHOLD=0.7
```

**For Azure Computer Vision:**
```env
API_PROVIDER=azure
AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_VISION_KEY=your-azure-api-key-here
SIMILARITY_THRESHOLD=0.7
```

### Running the Application

**Start the web server:**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🎯 Usage

### Web Interface

1. **Add Test Cases**
   - Upload an image (PNG, JPG, GIF, WEBP)
   - Enter the expected description
   - Click "Add Test Case"

2. **Run Tests**
   - Click "Run All Tests" to execute all test cases
   - View real-time progress indicator
   - See detailed results with charts

3. **View Results**
   - Success/failure statistics
   - Pie chart showing pass/fail distribution
   - Bar chart showing similarity scores
   - Detailed table with comparisons

### Command Line Interface

Run tests from command line:

```bash
python test_runner.py
```

This will:
1. Load test cases from `test_cases.json`
2. Call the vision API for each image
3. Compare results semantically
4. Save results to `test_results.json`
5. Print summary to console

### Using the Python API

```python
from test_runner import (
    TestCase,
    ImageTestRunner,
    OpenAIVisionClient
)

# Initialize client
client = OpenAIVisionClient("your-api-key")
runner = ImageTestRunner(client, similarity_threshold=0.7)

# Create test case
test_case = TestCase(
    id=1,
    image_path="path/to/image.jpg",
    expected_description="A cat sitting on a mat"
)

# Run test
result = runner.run_test_case(test_case)
print(f"Status: {'PASS' if result.passed else 'FAIL'}")
print(f"Similarity: {result.similarity_score:.2f}")
print(f"Actual: {result.actual_description}")
```

## 🔧 Configuration

### Similarity Threshold

The `SIMILARITY_THRESHOLD` determines how close the actual description must be to the expected description:

- `0.5` - Lenient (50% similarity required)
- `0.7` - Moderate (default, 70% similarity)
- `0.9` - Strict (90% similarity required)

### Choosing an API Provider

**OpenAI GPT-4 Vision:**
- Pros: More detailed descriptions, better context understanding
- Cons: Higher cost per request
- Best for: Complex scenes, detailed analysis

**Azure Computer Vision:**
- Pros: Lower cost, faster responses
- Cons: Simpler descriptions
- Best for: Basic object detection, tags

## 📊 API Endpoints

### Test Cases Management

**Get all test cases:**
```http
GET /api/test-cases
```

**Add test case:**
```http
POST /api/test-cases
Content-Type: multipart/form-data

image: [file]
description: "Expected description"
```

**Delete test case:**
```http
DELETE /api/test-cases/{id}
```

**Clear all test cases:**
```http
POST /api/test-cases/clear
```

### Testing

**Run all tests:**
```http
POST /api/run-tests
Content-Type: application/json

{
  "similarity_threshold": 0.7
}
```

**Test single image:**
```http
POST /api/test-single
Content-Type: multipart/form-data

image: [file]
```

### Results

**Get results history:**
```http
GET /api/results/history
```

**Get specific result:**
```http
GET /api/results/{filename}
```

## 📁 Project Structure

```
image_test_automation/
├── app.py                  # Flask web application
├── test_runner.py          # Core testing logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── test_cases.json        # Example test cases
├── templates/
│   └── index.html         # Web interface
├── uploads/               # Uploaded test images
├── results/               # Test result JSON files
└── README.md             # This file
```

## 🧪 Test Case Format

Test cases in `test_cases.json`:

```json
{
  "test_cases": [
    {
      "id": 1,
      "image_path": "test_images/example.jpg",
      "expected_description": "A dog playing in a park"
    }
  ]
}
```

## 📈 Understanding Results

### Similarity Scores

The system uses cosine similarity between sentence embeddings:

- **1.0** - Perfect match (identical meaning)
- **0.9+** - Very high similarity
- **0.7-0.9** - Good semantic match
- **0.5-0.7** - Moderate similarity
- **< 0.5** - Low similarity

### Result Files

Results are saved in JSON format with timestamp:

```json
{
  "test_cases": [
    {
      "id": 1,
      "image_path": "uploads/image.jpg",
      "expected_description": "A cat on a mat",
      "actual_description": "A feline sitting on a rug",
      "similarity_score": 0.85,
      "passed": true,
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "total_tests": 10,
  "passed": 8,
  "failed": 2,
  "success_rate": 80.0,
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🔍 How It Works

1. **Image Upload**: User uploads test images with expected descriptions
2. **API Call**: Image sent to chosen vision API (OpenAI/Azure)
3. **Description Generation**: API returns image description
4. **Semantic Comparison**: 
   - Both descriptions converted to embeddings
   - Cosine similarity calculated
   - Score compared against threshold
5. **Result Recording**: Pass/fail status and metrics saved
6. **Visualization**: Results displayed in charts and tables

## 🛠️ Customization

### Adding New Vision APIs

Extend the `VisionAPIClient` class:

```python
class CustomVisionClient(VisionAPIClient):
    def __init__(self, api_key):
        self.api_key = api_key
    
    def describe_image(self, image_path: str) -> str:
        # Your API implementation
        return description
```

### Custom Similarity Models

Use different sentence transformer models:

```python
comparator = SemanticComparator(model_name='all-mpnet-base-v2')
```

Popular models:
- `all-MiniLM-L6-v2` - Fast, lightweight (default)
- `all-mpnet-base-v2` - Higher quality
- `paraphrase-multilingual-mpnet-base-v2` - Multi-language

## 🚨 Troubleshooting

**API Connection Errors:**
- Verify API keys in `.env`
- Check internet connectivity
- Ensure API endpoints are correct

**Import Errors:**
- Run `pip install -r requirements.txt`
- Verify Python version (3.8+)

**File Upload Fails:**
- Check file size (< 16MB)
- Verify file format (PNG, JPG, GIF, WEBP)
- Ensure `uploads/` directory exists

**Low Similarity Scores:**
- Adjust `SIMILARITY_THRESHOLD` in `.env`
- Make expected descriptions more general
- Try different vision API provider

## 📝 API Key Setup

### OpenAI API Key

1. Visit https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env` as `OPENAI_API_KEY`

### Azure Computer Vision

1. Create Azure account
2. Create Computer Vision resource
3. Get endpoint and key from Azure Portal
4. Add to `.env`

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional vision API integrations
- More semantic comparison models
- Advanced visualization options
- Batch testing optimizations
- Export formats (PDF, CSV)

## 📄 License

MIT License - feel free to use in your projects!

## 🙏 Acknowledgments

- OpenAI GPT-4 Vision API
- Azure Computer Vision API
- Sentence Transformers library
- Flask web framework
- Chart.js for visualizations

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review API documentation
3. Open an issue on GitHub

---

Built with ❤️ for automated vision testing
