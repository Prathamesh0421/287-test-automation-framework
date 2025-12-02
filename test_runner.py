"""
Automated Image Description Testing System
Supports multiple vision APIs: Azure Computer Vision, OpenAI GPT-4 Vision
"""

import os
import json
import base64
import logging
import traceback
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
import requests
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class TestCase:
    """Represents a single test case"""
    id: int
    image_path: str
    expected_description: str
    actual_description: str = ""
    similarity_score: float = 0.0
    passed: bool = False
    timestamp: str = ""


class VisionAPIClient:
    """Base class for Vision API clients"""
    
    def describe_image(self, image_path: str) -> str:
        """Get description of an image"""
        raise NotImplementedError


class AzureComputerVisionClient(VisionAPIClient):
    """Azure Computer Vision API Client"""
    
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
        self.analyze_url = f"{endpoint}/vision/v3.2/analyze"
    
    def describe_image(self, image_path: str) -> str:
        """Get image description from Azure Computer Vision"""
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/octet-stream'
        }
        
        params = {
            'visualFeatures': 'Description,Tags',
            'language': 'en'
        }
        
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        response = requests.post(
            self.analyze_url,
            headers=headers,
            params=params,
            data=image_data
        )
        
        if response.status_code == 200:
            result = response.json()
            # Get the most confident description
            if 'description' in result and 'captions' in result['description']:
                captions = result['description']['captions']
                if captions:
                    return captions[0]['text']
            return "No description available"
        else:
            raise Exception(f"Azure API Error: {response.status_code} - {response.text}")


class OpenAIVisionClient(VisionAPIClient):
    """OpenAI GPT-4 Vision API Client"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    def describe_image(self, image_path: str) -> str:
        """Get image description from OpenAI GPT-4 Vision"""
        logger.info(f"OpenAI: Describing image {image_path}")

        try:
            # Read and encode image
            logger.debug(f"Reading image file: {image_path}")
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            logger.debug(f"Image encoded, size: {len(image_data)} bytes")

            # Determine image type
            ext = os.path.splitext(image_path)[1].lower()
            mime_type = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }.get(ext, 'image/jpeg')
            logger.debug(f"Image type: {mime_type}")

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this image in one concise sentence."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            logger.info("Sending request to OpenAI API...")
            response = requests.post(self.api_url, headers=headers, json=payload)
            logger.info(f"OpenAI API response status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                description = result['choices'][0]['message']['content'].strip()
                logger.info(f"OpenAI description received: {description[:100]}...")
                return description
            else:
                logger.error(f"OpenAI API Error: {response.status_code}")
                logger.error(f"Response: {response.text}")
                raise Exception(f"OpenAI API Error: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Exception in OpenAI describe_image: {str(e)}")
            logger.error(traceback.format_exc())
            raise


class SemanticComparator:
    """Compares descriptions semantically using sentence transformers"""

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize with a sentence transformer model
        Popular models:
        - 'all-MiniLM-L6-v2': Fast and efficient
        - 'all-mpnet-base-v2': Higher quality
        """
        logger.info(f"Initializing SemanticComparator with model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            logger.info("SemanticComparator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SentenceTransformer: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def compare(self, text1: str, text2: str) -> float:
        """
        Compare two texts semantically
        Returns similarity score between 0 and 1
        """
        logger.debug(f"Comparing texts: '{text1[:50]}...' vs '{text2[:50]}...'")
        try:
            embeddings = self.model.encode([text1, text2], convert_to_tensor=True)
            similarity = util.cos_sim(embeddings[0], embeddings[1])
            score = float(similarity.item())
            logger.debug(f"Similarity score: {score:.4f}")
            return score
        except Exception as e:
            logger.error(f"Error in semantic comparison: {str(e)}")
            logger.error(traceback.format_exc())
            raise


class ImageTestRunner:
    """Main test runner for automated image description testing"""

    def __init__(self, vision_client: VisionAPIClient, similarity_threshold: float = 0.7):
        logger.info("Initializing ImageTestRunner")
        logger.info(f"Vision client type: {type(vision_client).__name__}")
        logger.info(f"Similarity threshold: {similarity_threshold}")

        self.vision_client = vision_client
        try:
            self.comparator = SemanticComparator()
        except Exception as e:
            logger.error(f"Failed to initialize SemanticComparator: {str(e)}")
            raise
        self.similarity_threshold = similarity_threshold
        logger.info("ImageTestRunner initialized successfully")

    def run_test_case(self, test_case: TestCase) -> TestCase:
        """Run a single test case"""
        logger.info(f"Running test case #{test_case.id}: {test_case.image_path}")

        try:
            # Check if image file exists
            if not os.path.exists(test_case.image_path):
                raise FileNotFoundError(f"Image file not found: {test_case.image_path}")

            logger.info(f"Getting description from API for test #{test_case.id}")
            # Get actual description from API
            test_case.actual_description = self.vision_client.describe_image(test_case.image_path)
            logger.info(f"Got description for test #{test_case.id}: {test_case.actual_description[:100]}...")

            # Compare with expected description
            logger.info(f"Comparing descriptions for test #{test_case.id}")
            test_case.similarity_score = self.comparator.compare(
                test_case.expected_description,
                test_case.actual_description
            )
            logger.info(f"Similarity score for test #{test_case.id}: {test_case.similarity_score:.4f}")

            # Determine pass/fail
            test_case.passed = test_case.similarity_score >= self.similarity_threshold
            test_case.timestamp = datetime.now().isoformat()

            status = "PASSED" if test_case.passed else "FAILED"
            logger.info(f"Test #{test_case.id} {status}")

        except Exception as e:
            logger.error(f"Error in test case #{test_case.id}: {str(e)}")
            logger.error(traceback.format_exc())
            test_case.actual_description = f"Error: {str(e)}"
            test_case.passed = False
            test_case.timestamp = datetime.now().isoformat()

        return test_case

    def run_all_tests(self, test_cases: List[TestCase]) -> Dict:
        """Run all test cases and return results"""
        logger.info(f"Starting test run for {len(test_cases)} test cases")
        results = []
        passed_count = 0

        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"Processing test {i}/{len(test_cases)}")
            result = self.run_test_case(test_case)
            results.append(result)
            if result.passed:
                passed_count += 1

        success_rate = (passed_count / len(test_cases)) * 100 if test_cases else 0

        logger.info(f"Test run completed: {passed_count}/{len(test_cases)} passed ({success_rate:.2f}%)")

        return {
            'test_cases': [asdict(tc) for tc in results],
            'total_tests': len(test_cases),
            'passed': passed_count,
            'failed': len(test_cases) - passed_count,
            'success_rate': success_rate,
            'timestamp': datetime.now().isoformat()
        }


def load_test_cases_from_json(json_path: str) -> List[TestCase]:
    """Load test cases from a JSON file"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    return [
        TestCase(
            id=tc['id'],
            image_path=tc['image_path'],
            expected_description=tc['expected_description']
        )
        for tc in data['test_cases']
    ]


def save_results(results: Dict, output_path: str):
    """Save test results to JSON file"""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)


# Example usage
if __name__ == "__main__":
    # Configuration
    API_PROVIDER = "openai"  # or "azure"
    
    # For Azure Computer Vision
    AZURE_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT", "https://your-resource.cognitiveservices.azure.com/")
    AZURE_API_KEY = os.getenv("AZURE_VISION_KEY", "your-api-key")
    
    # For OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
    
    # Initialize the appropriate client
    if API_PROVIDER == "azure":
        vision_client = AzureComputerVisionClient(AZURE_ENDPOINT, AZURE_API_KEY)
    else:
        vision_client = OpenAIVisionClient(OPENAI_API_KEY)
    
    # Create test runner
    test_runner = ImageTestRunner(vision_client, similarity_threshold=0.7)
    
    # Load test cases
    test_cases = load_test_cases_from_json('test_cases.json')
    
    # Run tests
    print("Running automated image description tests...")
    results = test_runner.run_all_tests(test_cases)
    
    # Save results
    save_results(results, 'test_results.json')
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Test Results Summary")
    print(f"{'='*60}")
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Success Rate: {results['success_rate']:.2f}%")
    print(f"{'='*60}\n")
    
    # Print individual results
    for tc in results['test_cases']:
        status = "✓ PASS" if tc['passed'] else "✗ FAIL"
        print(f"{status} | Test {tc['id']}: {tc['similarity_score']:.2f}")
        print(f"  Expected: {tc['expected_description']}")
        print(f"  Actual:   {tc['actual_description']}\n")
