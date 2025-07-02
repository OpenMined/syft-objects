#!/bin/bash
set -e

# SyftBox app entry point for syft-objects
# This script starts the syft objects UI service

echo "🔐 Syft Objects UI - Starting distributed object viewer..."

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
echo "📦 Installing dependencies..."
uv sync

# Check if frontend dependencies are installed, if not install them
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Build the frontend
echo "🏗️ Building frontend..."
cd frontend
npm run build
cd ..

# Verify frontend build exists
if [ ! -d "frontend/out" ]; then
    echo "❌ Frontend build failed - no 'out' directory found"
    exit 1
fi

echo "✅ Frontend built successfully"

# Start the backend API server
echo "🌐 Starting Syft Objects UI on port ${SYFTBOX_ASSIGNED_PORT:-8003}..."
SYFTBOX_ASSIGNED_PORT=${SYFTBOX_ASSIGNED_PORT:-8003}

# For development, serve the built frontend through FastAPI
echo "🚀 Starting combined backend and frontend server..."
uv run uvicorn backend.main:app --host 0.0.0.0 --port $SYFTBOX_ASSIGNED_PORT 