"""
Setup and API Verification Script
Helps verify API credentials and test connections
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'results', 'templates', 'test_images']
    
    print("Creating directories...")
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✓ {directory}/")
    print()


def check_env_file():
    """Check if .env file exists"""
    print("Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("  ✗ .env file not found!")
        print("  Creating .env from template...")
        
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("  ✓ .env file created")
            print("  ⚠️  Please edit .env and add your API keys!")
            return False
        else:
            print("  ✗ .env.example not found!")
            return False
    else:
        print("  ✓ .env file exists")
        return True


def load_env_vars():
    """Load environment variables"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return True
    except ImportError:
        print("  ⚠️  python-dotenv not installed")
        print("  Run: pip install python-dotenv")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print("\nChecking dependencies...")
    
    required_packages = [
        ('flask', 'Flask'),
        ('flask_cors', 'flask-cors'),
        ('requests', 'requests'),
        ('sentence_transformers', 'sentence-transformers'),
        ('torch', 'torch'),
        ('numpy', 'numpy'),
        ('PIL', 'Pillow'),
        ('dotenv', 'python-dotenv')
    ]
    
    missing_packages = []
    
    for package_name, pip_name in required_packages:
        try:
            __import__(package_name)
            print(f"  ✓ {pip_name}")
        except ImportError:
            print(f"  ✗ {pip_name} (missing)")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n  Missing packages: {', '.join(missing_packages)}")
        print("  Run: pip install -r requirements.txt")
        return False
    
    return True


def test_openai_connection():
    """Test OpenAI API connection"""
    print("\nTesting OpenAI connection...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your-openai-api-key-here':
        print("  ✗ OpenAI API key not configured")
        print("  Set OPENAI_API_KEY in .env file")
        return False
    
    try:
        import requests
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        # Test with models endpoint (simpler than image)
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("  ✓ OpenAI API connection successful")
            return True
        elif response.status_code == 401:
            print("  ✗ Invalid API key")
            return False
        else:
            print(f"  ✗ Connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_azure_connection():
    """Test Azure Computer Vision connection"""
    print("\nTesting Azure connection...")
    
    endpoint = os.getenv('AZURE_VISION_ENDPOINT')
    api_key = os.getenv('AZURE_VISION_KEY')
    
    if not endpoint or endpoint == 'https://your-resource.cognitiveservices.azure.com/':
        print("  ✗ Azure endpoint not configured")
        return False
    
    if not api_key or api_key == 'your-azure-api-key-here':
        print("  ✗ Azure API key not configured")
        return False
    
    try:
        import requests
        
        headers = {
            'Ocp-Apim-Subscription-Key': api_key,
        }
        
        # Simple health check
        response = requests.get(
            f"{endpoint}/vision/v3.2/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("  ✓ Azure API connection successful")
            return True
        elif response.status_code == 401:
            print("  ✗ Invalid API key")
            return False
        else:
            print(f"  ✗ Connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def verify_api_provider():
    """Verify the configured API provider"""
    print("\nVerifying API configuration...")
    
    api_provider = os.getenv('API_PROVIDER', 'openai').lower()
    print(f"  Selected provider: {api_provider.upper()}")
    
    if api_provider == 'openai':
        return test_openai_connection()
    elif api_provider == 'azure':
        return test_azure_connection()
    else:
        print(f"  ✗ Invalid API provider: {api_provider}")
        print("  Must be 'openai' or 'azure'")
        return False


def main():
    """Run all setup and verification checks"""
    print("=" * 60)
    print("Image Description Testing System - Setup & Verification")
    print("=" * 60)
    print()
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Check .env file
    env_exists = check_env_file()
    
    if not env_exists:
        print("\n" + "=" * 60)
        print("Setup incomplete!")
        print("Please edit .env file with your API credentials")
        print("=" * 60)
        return
    
    # Step 3: Load environment variables
    if not load_env_vars():
        return
    
    # Step 4: Check dependencies
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n" + "=" * 60)
        print("Setup incomplete!")
        print("Please install missing dependencies")
        print("=" * 60)
        return
    
    # Step 5: Verify API connection
    api_ok = verify_api_provider()
    
    # Summary
    print("\n" + "=" * 60)
    if api_ok:
        print("✓ Setup complete! All checks passed.")
        print("\nYou can now:")
        print("  1. Run the web app: python app.py")
        print("  2. Run CLI tests: python test_runner.py")
        print("  3. Try examples: python example.py")
    else:
        print("✗ Setup incomplete!")
        print("Please fix the issues above and run this script again.")
    print("=" * 60)


if __name__ == "__main__":
    main()
