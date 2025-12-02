#!/usr/bin/env python3
"""
Diagnostic script to check application configuration and dependencies
"""

import os
import sys
from dotenv import load_dotenv

print("=" * 70)
print("Image Testing System - Diagnostic Tool")
print("=" * 70)
print()

# Load environment variables
load_dotenv()

# Check Python version
print(f"✓ Python version: {sys.version.split()[0]}")
print()

# Check dependencies
print("Checking dependencies...")
print("-" * 70)

dependencies = {
    'flask': 'Flask',
    'flask_cors': 'Flask-CORS',
    'requests': 'requests',
    'sentence_transformers': 'sentence-transformers',
    'torch': 'PyTorch',
    'numpy': 'NumPy',
    'PIL': 'Pillow',
    'dotenv': 'python-dotenv'
}

missing_deps = []
for module, name in dependencies.items():
    try:
        __import__(module)
        print(f"✓ {name}")
    except ImportError:
        print(f"✗ {name} - NOT INSTALLED")
        missing_deps.append(name)

if missing_deps:
    print()
    print(f"ERROR: Missing dependencies: {', '.join(missing_deps)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

print()

# Check environment configuration
print("Checking environment configuration...")
print("-" * 70)

api_provider = os.getenv("API_PROVIDER", "openai")
print(f"API Provider: {api_provider}")
print()

if api_provider == "azure":
    print("Azure Configuration:")
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    api_key = os.getenv("AZURE_VISION_KEY")

    if not endpoint or endpoint == "https://your-resource.cognitiveservices.azure.com/":
        print("✗ AZURE_VISION_ENDPOINT - NOT CONFIGURED (using placeholder)")
        print("  Please update .env with your actual Azure endpoint")
    else:
        print(f"✓ AZURE_VISION_ENDPOINT - {endpoint}")

    if not api_key or api_key.startswith("your-"):
        print("✗ AZURE_VISION_KEY - NOT CONFIGURED (using placeholder)")
        print("  Please update .env with your actual Azure API key")
    else:
        print(f"✓ AZURE_VISION_KEY - Set (length: {len(api_key)})")

elif api_provider == "openai":
    print("OpenAI Configuration:")
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your-openai-api-key-here":
        print("✗ OPENAI_API_KEY - NOT CONFIGURED (using placeholder)")
        print("  Please update .env with your actual OpenAI API key")
    else:
        print(f"✓ OPENAI_API_KEY - Set (length: {len(api_key)})")

else:
    print(f"✗ Unknown API provider: {api_provider}")
    print("  Valid options: 'openai' or 'azure'")

print()

# Check similarity threshold
threshold = os.getenv("SIMILARITY_THRESHOLD", "0.7")
try:
    threshold_val = float(threshold)
    if 0.0 <= threshold_val <= 1.0:
        print(f"✓ SIMILARITY_THRESHOLD - {threshold_val}")
    else:
        print(f"✗ SIMILARITY_THRESHOLD - {threshold_val} (should be between 0.0 and 1.0)")
except ValueError:
    print(f"✗ SIMILARITY_THRESHOLD - Invalid value: {threshold}")

print()

# Check directories
print("Checking directories...")
print("-" * 70)

directories = ['uploads', 'results', 'static']
for directory in directories:
    if os.path.exists(directory):
        print(f"✓ {directory}/ exists")
    else:
        print(f"✗ {directory}/ - Creating...")
        os.makedirs(directory, exist_ok=True)
        print(f"  Created {directory}/")

print()

# Summary
print("=" * 70)
print("Diagnostic Summary")
print("=" * 70)

issues = []

if api_provider == "azure":
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    api_key = os.getenv("AZURE_VISION_KEY")
    if not endpoint or endpoint == "https://your-resource.cognitiveservices.azure.com/":
        issues.append("Azure endpoint not configured")
    if not api_key or api_key.startswith("your-"):
        issues.append("Azure API key not configured")
elif api_provider == "openai":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-openai-api-key-here":
        issues.append("OpenAI API key not configured")

if issues:
    print()
    print("⚠️  CONFIGURATION ISSUES FOUND:")
    for issue in issues:
        print(f"   - {issue}")
    print()
    print("Please update your .env file with the correct API credentials.")
    print()
    print("If you're using Azure:")
    print("  1. Set API_PROVIDER=azure")
    print("  2. Set AZURE_VISION_ENDPOINT to your Azure resource endpoint")
    print("  3. Set AZURE_VISION_KEY to your Azure API key")
    print()
    print("If you're using OpenAI:")
    print("  1. Set API_PROVIDER=openai")
    print("  2. Set OPENAI_API_KEY to your OpenAI API key")
else:
    print()
    print("✓ All checks passed! Your application should be ready to run.")
    print()
    print("Start the server with: python app.py")

print("=" * 70)
