# SyftBox Queue Implementations Context

## Overview
This directory contains two queue implementations for SyftBox:

### 1. syft_queue.py (New Implementation)
- **Location**: `/syft_queue.py`
- **Type**: Single-file implementation
- **Key Features**:
  - Uses syft-objects natively with `syo.syobj()`
  - Simple API with `q()` function for queue creation
  - No web UI - pure Python API
  - Automatic path detection for SyftBox datasites
  - Mock data generation for privacy

### 2. syft-code-queue/ (Original Implementation)
- **Location**: `/syft-code-queue/`
- **Type**: Full-stack application
- **Key Features**:
  - Web UI (Next.js/React frontend)
  - FastAPI backend (`backend/main.py`)
  - Python package in `src/syft_code_queue/`
  - More complex architecture

## Key Differences
| Feature | syft_queue.py | syft-code-queue |
|---------|---------------|-----------------|
| Architecture | Single file | Multi-module |
| UI | None | Full web interface |
| API | Simple `q()` function | REST API + Client |
| Dependencies | Minimal (syft-objects) | Many (FastAPI, Next.js) |
| Use Case | Programmatic queue management | Interactive web-based management |

## Common Concepts
Both implementations share:
- Job lifecycle: inbox → approved → running → completed/failed/rejected/timedout
- Cross-datasite job submission
- Permission management with syft.pub.yaml files
- Queue and job metadata tracking

## Quick Reference
```python
# syft_queue.py usage
from syft_queue import q
my_queue = q("analytics")  # Create/get queue
job = my_queue.create_job("analysis", "alice@example.com", "bob@example.com")

# syft-code-queue usage
from syft_code_queue.client import QueueClient
client = QueueClient()
# ... more complex setup
```

## Development Notes
- When comparing implementations, consider checking:
  - Job model differences
  - Queue management approaches
  - Permission handling
  - Status tracking mechanisms

# IMPORTANT DEVELOPMENT RULES

## Unit Testing Requirements
**MANDATORY**: For EVERY code change, modification, or new feature implementation, you MUST:

1. **Create or update unit tests** that cover the changes
2. **Place tests in the appropriate test file**:
   - For existing modules: Update tests in `tests/test_<module_name>.py`
   - For new modules: Create `tests/test_<module_name>.py`
   - For bug fixes: Add regression tests that would have caught the bug

3. **Test Coverage Requirements**:
   - All new functions/methods must have at least one test
   - All modified functions must have their tests updated
   - Edge cases and error conditions must be tested
   - Mock external dependencies appropriately

4. **Test Naming Convention**:
   - Test functions: `test_<function_name>_<scenario>`
   - Test classes: `Test<ClassName>`
   - Be descriptive: `test_create_job_with_invalid_email_raises_error`

5. **Run Tests Before Completion**:
   - Always run the relevant tests after implementation
   - Ensure all tests pass before considering the task complete
   - If test commands are unknown, ask the user for the correct command

## Example Test Pattern
```python
# When implementing a change to collections.py
# Also create/update tests/test_collections.py

def test_objects_search_with_so_nomenclature():
    """Test that generated code uses 'so' instead of 'syo'"""
    # Test implementation here
    assert "so.objects" in generated_code
    assert "syo.objects" not in generated_code
```

## Enforcement
- This is NON-NEGOTIABLE - every code change requires tests
- If unable to create tests due to project structure, explicitly inform the user
- Tests should be written DURING implementation, not as an afterthought

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.