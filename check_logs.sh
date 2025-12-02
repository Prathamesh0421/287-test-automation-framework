#!/bin/bash
# Script to check application logs

echo "==================================="
echo "Checking Application Logs"
echo "==================================="
echo ""

if [ -f "app.log" ]; then
    echo "Last 50 lines of app.log:"
    echo "-----------------------------------"
    tail -50 app.log
    echo ""
    echo "-----------------------------------"
    echo ""
    echo "Errors in app.log:"
    echo "-----------------------------------"
    grep -i "error\|exception\|failed" app.log | tail -20
else
    echo "app.log not found. Run the application first."
fi

echo ""
echo "==================================="
echo "Environment Variables Check"
echo "==================================="
echo ""

if [ -f ".env" ]; then
    echo "Checking .env file (sensitive info hidden):"
    echo "-----------------------------------"
    if grep -q "OPENAI_API_KEY" .env; then
        echo "✓ OPENAI_API_KEY is set"
    else
        echo "✗ OPENAI_API_KEY is NOT set"
    fi

    if grep -q "API_PROVIDER" .env; then
        echo "✓ API_PROVIDER is set to: $(grep API_PROVIDER .env | cut -d'=' -f2)"
    else
        echo "✗ API_PROVIDER is NOT set (defaults to openai)"
    fi

    if grep -q "SIMILARITY_THRESHOLD" .env; then
        echo "✓ SIMILARITY_THRESHOLD is set to: $(grep SIMILARITY_THRESHOLD .env | cut -d'=' -f2)"
    else
        echo "✗ SIMILARITY_THRESHOLD is NOT set (defaults to 0.7)"
    fi
else
    echo ".env file not found!"
fi

echo ""
echo "==================================="
