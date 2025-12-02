# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Web Browser (templates/index.html)          │   │
│  │  • Upload images                                     │   │
│  │  • Manage test cases                                │   │
│  │  • View results & charts                            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    WEB APPLICATION (app.py)                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Flask REST API                          │   │
│  │  • /api/test-cases (GET, POST, DELETE)             │   │
│  │  • /api/run-tests (POST)                           │   │
│  │  • /api/results (GET)                              │   │
│  │  • File upload handling                             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              TESTING ENGINE (test_runner.py)                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         ImageTestRunner                              │   │
│  │  • Orchestrates test execution                      │   │
│  │  • Manages test cases                               │   │
│  │  • Generates results                                │   │
│  └─────────────────────────────────────────────────────┘   │
│           │                            │                     │
│           ▼                            ▼                     │
│  ┌──────────────────┐      ┌──────────────────┐           │
│  │  Vision API      │      │   Semantic       │           │
│  │  Clients         │      │   Comparator     │           │
│  │  • OpenAI        │      │  • Embeddings    │           │
│  │  • Azure         │      │  • Cosine Sim    │           │
│  └──────────────────┘      └──────────────────┘           │
└─────────────────────────────────────────────────────────────┘
           │                            │
           ▼                            ▼
┌──────────────────┐          ┌──────────────────┐
│  External APIs   │          │ ML Model         │
│  • OpenAI API    │          │ sentence-        │
│  • Azure API     │          │ transformers     │
└──────────────────┘          └──────────────────┘
```

## Component Breakdown

### 1. Frontend Layer (HTML/JS)

**File**: `templates/index.html`

**Responsibilities:**
- User interaction
- File uploads
- Dynamic UI updates
- Chart rendering
- API communication

**Technologies:**
- Pure JavaScript (no framework)
- Chart.js for visualizations
- Fetch API for HTTP requests
- CSS3 for styling

**Key Functions:**
```javascript
addTestCase()        // Upload and save test case
runAllTests()        // Trigger test execution
displayResults()     // Show results with charts
updatePieChart()     // Visualize pass/fail
updateSimilarityChart() // Show similarity scores
```

### 2. Web Server Layer (Flask)

**File**: `app.py`

**Responsibilities:**
- HTTP request handling
- REST API endpoints
- File management
- Request validation
- Response formatting

**Key Routes:**
```python
GET  /                    # Serve UI
GET  /api/test-cases      # List test cases
POST /api/test-cases      # Add test case
POST /api/run-tests       # Execute tests
GET  /api/results/history # Past results
```

**Data Flow:**
```
Request → Route → Handler → Test Runner → Response
```

### 3. Testing Engine Layer

**File**: `test_runner.py`

**Main Classes:**

#### VisionAPIClient (Abstract Base)
```python
class VisionAPIClient:
    def describe_image(image_path: str) -> str:
        """Get description from vision API"""
```

#### OpenAIVisionClient
```python
class OpenAIVisionClient(VisionAPIClient):
    - Encodes image to base64
    - Calls GPT-4 Vision API
    - Returns text description
```

#### AzureComputerVisionClient
```python
class AzureComputerVisionClient(VisionAPIClient):
    - Sends binary image data
    - Calls Azure Cognitive Services
    - Extracts caption from response
```

#### SemanticComparator
```python
class SemanticComparator:
    - Loads sentence-transformer model
    - Converts text to embeddings
    - Calculates cosine similarity
    - Returns similarity score (0-1)
```

#### ImageTestRunner
```python
class ImageTestRunner:
    - Manages test case execution
    - Coordinates API calls
    - Performs semantic comparison
    - Aggregates results
```

#### TestCase (Data Model)
```python
@dataclass
class TestCase:
    id: int
    image_path: str
    expected_description: str
    actual_description: str
    similarity_score: float
    passed: bool
    timestamp: str
```

## Data Flow Diagrams

### Test Execution Flow

```
┌─────────────┐
│   User      │
│   Clicks    │
│  "Run Tests"│
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Web UI sends       │
│  POST /api/run-tests│
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Flask receives request     │
│  Validates test cases exist │
└──────┬──────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  ImageTestRunner initialized     │
│  With VisionAPIClient            │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  For each test case:             │
│  ┌────────────────────────────┐ │
│  │ 1. Load image              │ │
│  │ 2. Call vision API         │ │
│  │ 3. Get description         │ │
│  │ 4. Compare semantically    │ │
│  │ 5. Record result           │ │
│  └────────────────────────────┘ │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Aggregate results:          │
│  • Total tests               │
│  • Passed/Failed             │
│  • Success rate              │
│  • Individual scores         │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Save to results/            │
│  Return JSON to client       │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Web UI receives results     │
│  • Updates statistics        │
│  • Renders charts            │
│  • Populates table           │
└──────────────────────────────┘
```

### Semantic Comparison Process

```
┌────────────────────────┐
│  Expected Description  │
│  "A cat on a mat"      │
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────────┐
│  Sentence Transformer      │
│  Converts to embedding     │
│  → [0.1, 0.3, ..., 0.5]   │
└──────┬─────────────────────┘
       │
       ├────────────────────┐
       │                    │
       ▼                    ▼
┌────────────┐    ┌────────────────┐
│  Embedding │    │   Embedding    │
│  Vector 1  │    │   Vector 2     │
└──────┬─────┘    └────────┬───────┘
       │                    │
       └──────────┬─────────┘
                  │
                  ▼
      ┌────────────────────────┐
      │  Cosine Similarity     │
      │  cos(θ) = A·B / |A||B| │
      └──────┬─────────────────┘
             │
             ▼
      ┌──────────────────┐
      │  Similarity Score│
      │       0.87       │
      └──────┬───────────┘
             │
             ▼
      ┌──────────────────┐
      │  Compare to      │
      │  Threshold (0.7) │
      └──────┬───────────┘
             │
             ▼
      ┌──────────────────┐
      │   0.87 > 0.7     │
      │   ✓ PASS         │
      └──────────────────┘
```

## Storage Architecture

```
File System Structure:
┌────────────────────────────┐
│  uploads/                  │
│  ├── 20240115_1_dog.jpg   │ ← Test case images
│  ├── 20240115_2_cat.jpg   │
│  └── ...                   │
└────────────────────────────┘

┌────────────────────────────┐
│  results/                  │
│  ├── results_20240115...   │ ← Test run results
│  ├── results_20240116...   │
│  └── ...                   │
└────────────────────────────┘

┌────────────────────────────┐
│  templates/                │
│  └── index.html            │ ← Web interface
└────────────────────────────┘

┌────────────────────────────┐
│  Configuration             │
│  ├── .env                  │ ← API keys, settings
│  └── test_cases.json       │ ← Test definitions
└────────────────────────────┘
```

## API Integration Architecture

### OpenAI Integration

```
┌─────────────────┐
│ Image File      │
│ (JPEG/PNG)      │
└────┬────────────┘
     │
     ▼
┌─────────────────────┐
│ Read & Encode       │
│ Base64 encoding     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ HTTP POST Request           │
│ URL: api.openai.com         │
│ Headers:                    │
│   Authorization: Bearer key │
│ Body:                       │
│   model: gpt-4o            │
│   messages: [{              │
│     content: [              │
│       {type: "text"},       │
│       {type: "image_url"}   │
│     ]                       │
│   }]                        │
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────┐
│ OpenAI API          │
│ Processing...       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────────┐
│ JSON Response           │
│ {                       │
│   choices: [{           │
│     message: {          │
│       content: "..."    │
│     }                   │
│   }]                    │
│ }                       │
└────┬────────────────────┘
     │
     ▼
┌─────────────────────┐
│ Extract Description │
│ Return as string    │
└─────────────────────┘
```

### Azure Integration

```
┌─────────────────┐
│ Image File      │
│ (Binary data)   │
└────┬────────────┘
     │
     ▼
┌─────────────────────┐
│ Read Binary Data    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ HTTP POST Request           │
│ URL: {endpoint}/vision/v3.2 │
│ Headers:                    │
│   Ocp-Apim-Subscription-Key │
│   Content-Type: octet-stream│
│ Params:                     │
│   visualFeatures: Description│
│ Body: Binary image data     │
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────┐
│ Azure Cognitive     │
│ Services Processing │
└────┬────────────────┘
     │
     ▼
┌─────────────────────────┐
│ JSON Response           │
│ {                       │
│   description: {        │
│     captions: [{        │
│       text: "...",      │
│       confidence: 0.95  │
│     }]                  │
│   }                     │
│ }                       │
└────┬────────────────────┘
     │
     ▼
┌─────────────────────┐
│ Extract Caption     │
│ Return as string    │
└─────────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────┐
│  Security Layers                │
│                                 │
│  1. Environment Variables       │
│     • API keys not in code      │
│     • .env file (gitignored)    │
│                                 │
│  2. Input Validation            │
│     • File type checking        │
│     • File size limits          │
│     • Path sanitization         │
│                                 │
│  3. File Handling               │
│     • Secure filename generation│
│     • Isolated storage          │
│     • No directory traversal    │
│                                 │
│  4. API Security                │
│     • HTTPS only               │
│     • API key encryption        │
│     • Rate limiting (TODO)      │
│                                 │
│  5. CORS Configuration          │
│     • Controlled origins        │
│     • Method restrictions       │
└─────────────────────────────────┘
```

## Scalability Considerations

### Current Architecture
- Single-threaded Flask server
- Synchronous API calls
- Local file storage
- In-memory test case storage

### Scaling Strategies

**Horizontal Scaling:**
```
Load Balancer
     │
     ├── Flask Instance 1
     ├── Flask Instance 2
     └── Flask Instance 3
             │
             ▼
     Shared Storage (S3, GCS)
```

**Asynchronous Processing:**
```
Web Server → Task Queue → Worker Processes
     │                          │
     └─────── Results DB ───────┘
```

**Caching:**
```
Request → Cache Check → API Call → Cache Store
              │              │
              └── Cache Hit ─┘
```

## Performance Characteristics

**Bottlenecks:**
1. API call latency (1-3s per image)
2. Large batch processing
3. Semantic model initialization

**Optimizations:**
1. Model caching (done)
2. Concurrent API calls (future)
3. Result caching (future)
4. Connection pooling (future)

## Error Handling Flow

```
API Call
    │
    ├─ Success ──→ Continue
    │
    ├─ Network Error ──→ Retry (3x)
    │                      │
    │                      └─ Log & Report
    │
    ├─ Auth Error ──→ Check credentials
    │                      │
    │                      └─ User notification
    │
    └─ Invalid Response ──→ Parse error
                              │
                              └─ Log & Skip
```

## Monitoring Points

Key metrics to track:
- API response times
- Success/failure rates
- API costs
- Memory usage
- Request queue depth

## Summary

**Architecture Strengths:**
✅ Modular design
✅ Easy to extend
✅ Clear separation of concerns
✅ Well-documented
✅ Production-ready patterns

**Key Design Decisions:**
1. REST API for flexibility
2. Pluggable vision clients
3. Semantic comparison for robustness
4. File-based storage for simplicity
5. Synchronous for clarity

This architecture supports the core use case while remaining extensible for future enhancements.
