#!/bin/bash

# Variables
ZIP_FILE="deployment-package.zip"
PROJECT_DIR="."
VENV_DIR="$PROJECT_DIR/.venv"
PACKAGE_DIR="$PROJECT_DIR/package"

# Navigate to project directory
cd $PROJECT_DIR

# Remove old ZIP file
rm -f $ZIP_FILE

# Create a temporary directory for dependencies
mkdir -p $PACKAGE_DIR

# Install dependencies to package directory
poetry export --without-hashes --dev -o requirements.txt
pip install --target $PACKAGE_DIR -r requirements.txt

# Create the ZIP file with dependencies
cd $PACKAGE_DIR
zip -r ../$ZIP_FILE .

# Add the code to the ZIP file
cd ..
zip -r $ZIP_FILE reddit_news_bot

# Clean up
rm -rf $PACKAGE_DIR
rm requirements.txt

