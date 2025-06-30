#!/bin/bash

# Syft Objects Release Script
# This script builds the package and provides the upload command

set -e

echo "🔐 Building syft-objects v0.3.0..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/ 2>/dev/null || true

# Build the package
echo "📦 Building package..."
python3 -m build

# Check what was built
echo "📋 Built packages:"
ls -la dist/

echo ""
echo "✅ Build complete!"
echo ""
echo "🚀 To upload to PyPI, run:"
echo "   uv pip run twine upload dist/*"
echo ""
echo "📝 Or if you want to test first:"
echo "   uv pip run twine upload --repository testpypi dist/*"
echo "" 