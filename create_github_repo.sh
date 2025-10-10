#!/bin/bash

# GitHub Repository Creation Script
# Run these commands in sequence

echo "=== Creating New GitHub Repository for PID Digitization with Tesseract OCR ==="

# Step 1: Authenticate with GitHub CLI
echo "Step 1: Authenticate with GitHub..."
gh auth login -h github.com

# Step 2: Create a new repository
echo "Step 2: Creating new repository..."
REPO_NAME="pid-digitization-tesseract-ocr"
gh repo create $REPO_NAME --public --description "P&ID Digitization using open-source Tesseract OCR instead of Azure Form Recognizer" --clone=false

# Step 3: Set up git for the new repository
echo "Step 3: Setting up git for new repository..."
cd /Users/aalbaharnah/Projects/digitization-of-piping-and-instrument-diagrams

# Remove existing origin (points to Azure-Samples)
git remote remove origin

# Add new origin pointing to your repository
git remote add origin https://github.com/aalbaharnah/$REPO_NAME.git

# Step 4: Stage all your changes
echo "Step 4: Staging changes..."
git add .

# Step 5: Commit your changes
echo "Step 5: Committing changes..."
git commit -m "Convert from Azure Form Recognizer to Tesseract OCR

- Replaced azure-ai-formrecognizer with pytesseract
- Updated OCR client to use Tesseract instead of Azure services
- Maintained same interface for backward compatibility
- Updated dependencies and documentation
- Fixed Python 3.13 compatibility with Pydantic v2
- Added Tesseract installation to Dockerfile
- Updated tests to mock Tesseract instead of Azure services

Benefits:
- Open source solution
- No API costs
- Local processing for privacy
- Offline capability
- Self-contained deployment"

# Step 6: Push to new repository
echo "Step 6: Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "✅ Repository created successfully!"
echo "🔗 Your new repository: https://github.com/aalbaharnah/$REPO_NAME"
echo "📝 Don't forget to update the README.md with your specific details"