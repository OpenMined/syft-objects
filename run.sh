#!/bin/bash
set -e

# SyftBox app entry point for syft-objects (100% Pure Python Stack)
# This script starts the syft objects UI service with NO Node.js dependencies

echo "🚀 Syft Objects UI - Starting 100% Pure Python Stack (No Node.js)..."

# Disable interactive prompts and shell customizations for non-interactive environments
export ZSH_DISABLE_COMPFIX=true
export NONINTERACTIVE=1

# Create virtual environment with uv (remove old one if exists)
echo "📦 Setting up virtual environment with uv..."
rm -rf .venv

# Let uv handle Python version management - it will download if needed
echo "🐍 Creating virtual environment with Python 3.12..."
uv venv --python 3.12

# Set the virtual environment path for uv to use
export VIRTUAL_ENV="$(pwd)/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Install only core dependencies needed for the server and library
echo "📦 Installing minimal server dependencies..."
# Install syft-objects package without dependencies
uv pip uninstall syft-objects
uv pip install -e . --no-deps
# Install minimal dependencies for server + syft-objects core functionality
uv pip install \
      "fastapi>=0.104.0" \
      "uvicorn>=0.24.0" \
      "loguru>=0.7.0" \
      "pydantic>=2.0.0" \
      "pyyaml>=6.0" \
      "syft-perm>=0.1.0" \
      "syft-core>=0.2.5" \
      "requests>=2.32.4" \
      "python-multipart>=0.0.20" \
      "pandas>=2.0.0" \
      "openpyxl>=3.1.5" \
# Install optional performance enhancements if available (but don't fail if not)
echo "📦 Installing optional performance enhancements..."
# uv pip install "uvloop>=0.17.0" "httptools>=0.6.0" || echo "⚠️  Optional performance dependencies skipped"

# NO FRONTEND BUILD NEEDED - Pure Python serves HTML directly!
echo "✅ Pure Python implementation - No frontend build required!"

# Determine the port to use (FastAPI backend default)
SYFTBOX_ASSIGNED_PORT=${SYFTBOX_ASSIGNED_PORT:-8004}

# Create .syftbox directory if it doesn't exist
mkdir -p ~/.syftbox

# Save the port to a static config file for the Python API to discover
echo "💾 Saving port $SYFTBOX_ASSIGNED_PORT to ~/.syftbox/syft_objects.config..."
echo "$SYFTBOX_ASSIGNED_PORT" > ~/.syftbox/syft_objects.config

# Start the pure Python FastAPI server (no Node.js dependencies)
echo "🌐 Starting Pure Python Syft Objects UI on port $SYFTBOX_ASSIGNED_PORT..."
echo "🚀 Starting 100% Python FastAPI server with integrated HTML generation..."

# Pure Python FastAPI server startup with hot reload
# Check if optional performance dependencies are available
if python -c "import uvloop" 2>/dev/null && python -c "import httptools" 2>/dev/null; then
    echo "✅ Running with performance optimizations (uvloop + httptools)"
    uv run --no-sync uvicorn backend.fast_main:app \
        --host 0.0.0.0 \
        --port $SYFTBOX_ASSIGNED_PORT \
        --loop uvloop \
        --http httptools \
        --reload \
        --access-log \
        --use-colors \
        --server-header \
        --date-header
else
    echo "⚡ Running with standard event loop"
    uv run --no-sync uvicorn backend.fast_main:app \
        --host 0.0.0.0 \
        --port $SYFTBOX_ASSIGNED_PORT \
        --reload \
        --access-log \
        --use-colors \
        --server-header \
        --date-header
fi 
