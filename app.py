"""
Flask Web Application for Image Description Testing
Provides REST API and serves frontend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import logging
import traceback
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv
from test_runner import (
    TestCase,
    ImageTestRunner,
    AzureComputerVisionClient,
    OpenAIVisionClient
)

# Load environment variables from .env file
load_dotenv()
logger_init = logging.getLogger('init')
logger_init.info("Environment variables loaded from .env")
logger_init.info(f"API_PROVIDER: {os.getenv('API_PROVIDER', 'not set')}")
logger_init.info(f"SIMILARITY_THRESHOLD: {os.getenv('SIMILARITY_THRESHOLD', 'not set')}")

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Global test cases storage
test_cases = []
test_case_counter = 1


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_vision_client():
    """Initialize and return the appropriate vision client"""
    api_provider = os.getenv("API_PROVIDER", "openai")
    
    if api_provider == "azure":
        endpoint = os.getenv("AZURE_VISION_ENDPOINT")
        api_key = os.getenv("AZURE_VISION_KEY")
        if not endpoint or not api_key:
            raise ValueError("Azure credentials not configured")
        return AzureComputerVisionClient(endpoint, api_key)
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not configured")
        return OpenAIVisionClient(api_key)


@app.route('/')
def index():
    """Serve the React app"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current API configuration"""
    api_provider = os.getenv("API_PROVIDER", "openai")
    return jsonify({
        'api_provider': api_provider,
        'similarity_threshold': float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    })


@app.route('/api/test-cases', methods=['GET'])
def get_test_cases():
    """Get all test cases"""
    return jsonify({
        'test_cases': [
            {
                'id': tc.id,
                'image_path': os.path.basename(tc.image_path),
                'expected_description': tc.expected_description
            }
            for tc in test_cases
        ],
        'count': len(test_cases)
    })


@app.route('/api/test-cases', methods=['POST'])
def add_test_case():
    """Add a new test case"""
    global test_case_counter

    logger.info("POST /api/test-cases - Adding new test case")

    # Check if image file is present
    if 'image' not in request.files:
        logger.warning("No image file in request")
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    description = request.form.get('description', '')

    logger.info(f"File: {file.filename}, Description length: {len(description)}")

    if file.filename == '':
        logger.warning("Empty filename")
        return jsonify({'error': 'No file selected'}), 400

    if not description:
        logger.warning("No description provided")
        return jsonify({'error': 'Description is required'}), 400

    if file and allowed_file(file.filename):
        # Save file with unique name
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{test_case_counter}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        logger.info(f"Saving file to: {filepath}")
        file.save(filepath)

        # Create test case
        test_case = TestCase(
            id=test_case_counter,
            image_path=filepath,
            expected_description=description
        )
        test_cases.append(test_case)
        logger.info(f"Test case #{test_case_counter} added successfully")
        test_case_counter += 1

        return jsonify({
            'message': 'Test case added successfully',
            'test_case': {
                'id': test_case.id,
                'image_path': unique_filename,
                'expected_description': test_case.expected_description
            }
        }), 201

    logger.warning(f"Invalid file type: {file.filename}")
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/api/test-cases/<int:test_id>', methods=['DELETE'])
def delete_test_case(test_id):
    """Delete a test case"""
    global test_cases
    
    test_case = next((tc for tc in test_cases if tc.id == test_id), None)
    if not test_case:
        return jsonify({'error': 'Test case not found'}), 404
    
    # Delete image file
    try:
        if os.path.exists(test_case.image_path):
            os.remove(test_case.image_path)
    except Exception as e:
        print(f"Error deleting file: {e}")
    
    # Remove from list
    test_cases = [tc for tc in test_cases if tc.id != test_id]
    
    return jsonify({'message': 'Test case deleted successfully'}), 200


@app.route('/api/test-cases/clear', methods=['POST'])
def clear_test_cases():
    """Clear all test cases"""
    global test_cases, test_case_counter
    
    # Delete all uploaded files
    for test_case in test_cases:
        try:
            if os.path.exists(test_case.image_path):
                os.remove(test_case.image_path)
        except Exception as e:
            print(f"Error deleting file: {e}")
    
    test_cases = []
    test_case_counter = 1
    
    return jsonify({'message': 'All test cases cleared'}), 200


@app.route('/api/run-tests', methods=['POST'])
def run_tests():
    """Run all tests and return results"""
    logger.info("=" * 60)
    logger.info("POST /api/run-tests - Starting test execution")
    logger.info(f"Number of test cases: {len(test_cases)}")

    if not test_cases:
        logger.warning("No test cases available")
        return jsonify({'error': 'No test cases available'}), 400

    try:
        # Get similarity threshold from request or use default
        # Use silent=True to handle empty body gracefully
        data = request.get_json(silent=True) or {}
        similarity_threshold = data.get('similarity_threshold', 0.7)
        logger.info(f"Similarity threshold: {similarity_threshold}")

        # Get environment configuration
        api_provider = os.getenv("API_PROVIDER", "openai")
        logger.info(f"API Provider: {api_provider}")

        # Initialize vision client and test runner
        logger.info("Initializing vision client...")
        vision_client = get_vision_client()
        logger.info(f"Vision client initialized: {type(vision_client).__name__}")

        logger.info("Initializing test runner...")
        test_runner = ImageTestRunner(vision_client, similarity_threshold)
        logger.info("Test runner initialized successfully")

        # Log test cases
        for tc in test_cases:
            logger.info(f"Test Case #{tc.id}: {tc.image_path}")

        # Run tests
        logger.info("Running tests...")
        results = test_runner.run_all_tests(test_cases.copy())
        logger.info(f"Tests completed. Results: {results.get('passed', 0)}/{results.get('total_tests', 0)} passed")

        # Save results
        result_filename = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
        logger.info(f"Saving results to: {result_path}")
        with open(result_path, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info("Results saved successfully")

        logger.info("=" * 60)
        return jsonify(results), 200

    except ValueError as e:
        logger.error(f"ValueError in run_tests: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Exception in run_tests: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Test execution failed: {str(e)}'}), 500


@app.route('/api/test-single', methods=['POST'])
def test_single_image():
    """Test a single image without saving it"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    try:
        # Save temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
        file.save(temp_path)
        
        # Get description
        vision_client = get_vision_client()
        description = vision_client.describe_image(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({'description': description}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/results/history', methods=['GET'])
def get_results_history():
    """Get list of all saved test results"""
    try:
        result_files = [
            f for f in os.listdir(app.config['RESULTS_FOLDER'])
            if f.startswith('results_') and f.endswith('.json')
        ]
        result_files.sort(reverse=True)  # Most recent first
        
        return jsonify({
            'results': result_files[:10]  # Return last 10 results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/results/<filename>', methods=['GET'])
def get_result(filename):
    """Get specific test result"""
    try:
        result_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
        with open(result_path, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'Result not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    print("=" * 60)
    print("Image Description Testing System")
    print("=" * 60)
    print(f"API Provider: {os.getenv('API_PROVIDER', 'openai')}")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Results folder: {RESULTS_FOLDER}")
    print("=" * 60)
    print("\nStarting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
