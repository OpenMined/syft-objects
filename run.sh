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

# Install dependencies using uv sync (which respects the virtual environment)
echo "📦 Installing Python dependencies..."
uv sync

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

# Pure Python FastAPI server startup with optimizations
uv run uvicorn backend.fast_main:app \
    --host 0.0.0.0 \
    --port $SYFTBOX_ASSIGNED_PORT \
    --workers 1 \
    --loop uvloop \
    --http httptools \
    --access-log \
    --use-colors \
    --server-header \
    --date-header 