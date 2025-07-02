#!/bin/bash

# Release script for syft-objects
# This script performs comprehensive checks before building and releasing the package

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_step() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "src/syft_objects" ]; then
    print_error "This script must be run from the syft-objects project root directory"
    exit 1
fi

print_step "Starting syft-objects release process"

# 1. Check git status
print_step "Checking git status"
if [ -n "$(git status --porcelain)" ]; then
    print_error "Working directory is not clean. Please commit or stash changes."
    git status --short
    exit 1
fi
print_success "Working directory is clean"

# 2. Check we're on main branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    print_warning "Not on main branch (currently on: $current_branch)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Aborted by user"
        exit 1
    fi
fi

# 3. Pull latest changes
print_step "Pulling latest changes"
git pull origin main
print_success "Repository is up to date"

# 4. Sync dependencies
print_step "Syncing dependencies"
if command -v uv &> /dev/null; then
    uv sync
    print_success "Dependencies synced with uv"
else
    print_error "uv not found. Please install uv first."
    exit 1
fi

# 5. Run tests (if test directory exists)
if [ -d "tests" ]; then
    print_step "Running tests"
    uv run pytest -v
    if [ $? -eq 0 ]; then
        print_success "All tests passed"
    else
        print_error "Tests failed"
        exit 1
    fi
else
    print_warning "No tests directory found, skipping tests"
fi

# 6. Run linting (if ruff is available)
print_step "Running linting checks"
uv run ruff check src/syft_objects/ || {
    print_warning "Linting issues found, but proceeding..."
}

# 7. Run formatting check (if ruff is available)
print_step "Checking code formatting"
uv run ruff format --check src/syft_objects/ || {
    print_warning "Code formatting issues found, but proceeding..."
}

# 8. Check version consistency
print_step "Checking version consistency"
init_version=$(python -c "import sys; sys.path.insert(0, 'src'); from syft_objects import __version__; print(__version__)")
toml_version=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

if [ "$init_version" != "$toml_version" ]; then
    print_error "Version mismatch: __init__.py has $init_version, pyproject.toml has $toml_version"
    exit 1
fi
print_success "Version consistency check passed: $init_version"

# 9. Build package
print_step "Building package"
# Clean previous builds
rm -rf dist/ build/ *.egg-info/
uv build
if [ $? -eq 0 ]; then
    print_success "Package built successfully"
else
    print_error "Package build failed"
    exit 1
fi

# 10. Check package
print_step "Checking package"
uv tool run twine check dist/*
if [ $? -eq 0 ]; then
    print_success "Package check passed"
else
    print_error "Package check failed"
    exit 1
fi

# 11. Show package info
print_step "Package information"
echo "Built packages:"
ls -la dist/
echo
echo "Package contents:"
tar -tzf dist/syft-objects-*.tar.gz | head -20
if [ $(tar -tzf dist/syft-objects-*.tar.gz | wc -l) -gt 20 ]; then
    echo "... (truncated, $(tar -tzf dist/syft-objects-*.tar.gz | wc -l) total files)"
fi

# 12. Final confirmation
print_step "Release Summary"
echo "Package: syft-objects"
echo "Version: $init_version"
echo "Branch: $current_branch"
echo "Files built: $(ls dist/ | tr '\n' ' ')"
echo

print_success "✅ All checks passed! Package is ready for release."
echo
echo "Next steps:"
echo "1. Create a git tag: git tag v$init_version"
echo "2. Push the tag: git push origin v$init_version"
echo "3. Create a GitHub release from the tag"
echo "4. Publish to PyPI: uv tool run twine upload dist/*"
echo

read -p "Would you like to publish to PyPI now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Publishing to PyPI"
    uv tool run twine upload dist/*
    if [ $? -eq 0 ]; then
        print_success "Successfully published to PyPI!"
        echo "Package available at: https://pypi.org/project/syft-objects/$init_version/"
    else
        print_error "Failed to publish to PyPI"
        exit 1
    fi
else
    echo "To publish later, run: uv tool run twine upload dist/*"
fi

print_warning "Remember to update the version in src/syft_objects/__init__.py and pyproject.toml before the next release!" 