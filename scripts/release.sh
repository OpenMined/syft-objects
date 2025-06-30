#!/bin/bash

# syft-objects release script
set -e

echo "🚀 Releasing syft-objects to PyPI..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Make sure you're in the syft-objects directory."
    exit 1
fi

# Get current version
CURRENT_VERSION=$(python3 -c "import sys; sys.path.insert(0, 'src'); from syft_objects import __version__; print(__version__)")
echo "📦 Current version: $CURRENT_VERSION"

# Check if version is in pyproject.toml
PYPROJECT_VERSION=$(python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")
echo "📦 PyProject version: $PYPROJECT_VERSION"

if [ "$CURRENT_VERSION" != "$PYPROJECT_VERSION" ]; then
    echo "❌ Error: Version mismatch between __init__.py ($CURRENT_VERSION) and pyproject.toml ($PYPROJECT_VERSION)"
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "🔨 Building package..."
python3 -m build

# Check if build was successful
if [ ! -f "dist/syft_objects-$CURRENT_VERSION.tar.gz" ]; then
    echo "❌ Error: Build failed - tar.gz not found"
    exit 1
fi

if [ ! -f "dist/syft_objects-$CURRENT_VERSION-py3-none-any.whl" ]; then
    echo "❌ Error: Build failed - wheel not found"
    exit 1
fi

echo "✅ Build successful!"

# Show what will be uploaded
echo "📋 Files to upload:"
ls -la dist/

# Ask for confirmation
read -p "🤔 Do you want to upload to PyPI? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Release cancelled"
    exit 1
fi

# Upload to PyPI
echo "🚀 Uploading to PyPI..."
python3 -m twine upload dist/*

echo "✅ Release successful!"
echo "🎉 syft-objects $CURRENT_VERSION is now available on PyPI!"
echo "📦 Install with: pip install syft-objects==$CURRENT_VERSION" 