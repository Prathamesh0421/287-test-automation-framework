"""
Simple standalone example for testing a single image
Quick start script without needing the full web interface
"""

import os
from test_runner import OpenAIVisionClient, AzureComputerVisionClient, SemanticComparator

def test_single_image_example():
    """
    Example: Test a single image with OpenAI GPT-4 Vision
    """
    
    # Configuration
    OPENAI_API_KEY = "your-openai-api-key"  # Replace with your key
    IMAGE_PATH = "path/to/your/image.jpg"   # Replace with your image
    EXPECTED_DESCRIPTION = "A dog playing in a park"  # Expected result
    
    print("=" * 60)
    print("Single Image Testing Example")
    print("=" * 60)
    
    # Initialize client
    print("\n1. Initializing OpenAI Vision client...")
    client = OpenAIVisionClient(OPENAI_API_KEY)
    
    # Get image description
    print(f"\n2. Analyzing image: {IMAGE_PATH}")
    actual_description = client.describe_image(IMAGE_PATH)
    print(f"   Generated description: {actual_description}")
    
    # Compare descriptions
    print(f"\n3. Comparing with expected description...")
    print(f"   Expected: {EXPECTED_DESCRIPTION}")
    print(f"   Actual:   {actual_description}")
    
    comparator = SemanticComparator()
    similarity = comparator.compare(EXPECTED_DESCRIPTION, actual_description)
    
    print(f"\n4. Results:")
    print(f"   Similarity Score: {similarity:.2%}")
    print(f"   Status: {'✓ PASS' if similarity >= 0.7 else '✗ FAIL'}")
    print("=" * 60)


def test_multiple_images_example():
    """
    Example: Test multiple images in batch
    """
    
    # Configuration
    OPENAI_API_KEY = "your-openai-api-key"
    
    test_cases = [
        {
            "image": "images/dog.jpg",
            "expected": "A golden retriever playing outdoors"
        },
        {
            "image": "images/cat.jpg",
            "expected": "A cat sitting by a window"
        },
        {
            "image": "images/food.jpg",
            "expected": "A plate of pasta with tomato sauce"
        }
    ]
    
    print("=" * 60)
    print("Batch Testing Example")
    print("=" * 60)
    
    # Initialize
    client = OpenAIVisionClient(OPENAI_API_KEY)
    comparator = SemanticComparator()
    
    results = []
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}/{len(test_cases)}: {test['image']}")
        
        try:
            # Get description
            actual = client.describe_image(test['image'])
            
            # Compare
            similarity = comparator.compare(test['expected'], actual)
            passed = similarity >= 0.7
            
            result = {
                'test_id': i,
                'image': test['image'],
                'expected': test['expected'],
                'actual': actual,
                'similarity': similarity,
                'passed': passed
            }
            results.append(result)
            
            print(f"  Expected: {test['expected']}")
            print(f"  Actual:   {actual}")
            print(f"  Score:    {similarity:.2%}")
            print(f"  Status:   {'✓ PASS' if passed else '✗ FAIL'}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
    
    # Summary
    passed_count = sum(1 for r in results if r['passed'])
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total Tests:   {len(results)}")
    print(f"Passed:        {passed_count}")
    print(f"Failed:        {len(results) - passed_count}")
    print(f"Success Rate:  {(passed_count/len(results)*100):.1f}%")
    print("=" * 60)


def compare_apis_example():
    """
    Example: Compare OpenAI vs Azure results for same image
    """
    
    OPENAI_API_KEY = "your-openai-api-key"
    AZURE_ENDPOINT = "https://your-resource.cognitiveservices.azure.com/"
    AZURE_KEY = "your-azure-key"
    IMAGE_PATH = "path/to/image.jpg"
    
    print("=" * 60)
    print("API Comparison Example")
    print("=" * 60)
    
    # Test with OpenAI
    print("\n1. Testing with OpenAI GPT-4 Vision...")
    openai_client = OpenAIVisionClient(OPENAI_API_KEY)
    openai_result = openai_client.describe_image(IMAGE_PATH)
    print(f"   Result: {openai_result}")
    
    # Test with Azure
    print("\n2. Testing with Azure Computer Vision...")
    azure_client = AzureComputerVisionClient(AZURE_ENDPOINT, AZURE_KEY)
    azure_result = azure_client.describe_image(IMAGE_PATH)
    print(f"   Result: {azure_result}")
    
    # Compare results
    print("\n3. Comparing descriptions...")
    comparator = SemanticComparator()
    similarity = comparator.compare(openai_result, azure_result)
    
    print(f"   OpenAI:    {openai_result}")
    print(f"   Azure:     {azure_result}")
    print(f"   Similarity: {similarity:.2%}")
    print("=" * 60)


if __name__ == "__main__":
    print("\nChoose an example to run:")
    print("1. Test single image")
    print("2. Test multiple images (batch)")
    print("3. Compare OpenAI vs Azure")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == "1":
        test_single_image_example()
    elif choice == "2":
        test_multiple_images_example()
    elif choice == "3":
        compare_apis_example()
    else:
        print("Invalid choice!")
