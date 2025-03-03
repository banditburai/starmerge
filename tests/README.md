# TailwindMerge Python Test Suite

This directory contains tests for the Python implementation of TailwindMerge that maintain parity with the original JavaScript implementation.

## Methodology

Each Python test file in this directory corresponds directly to a JavaScript test file in the original codebase. We follow these principles:

1. **1:1 File Mapping**: Each JavaScript test file has exactly one corresponding Python test file with a similar name.
2. **Test Function Parity**: The Python test functions mirror the JavaScript test functions in functionality.
3. **Naming Convention**: JavaScript test names are converted to Python function names:
   - `test('handles arbitrary property conflicts correctly')` in JS becomes `test_handles_arbitrary_property_conflicts_correctly()` in Python.
   - Special characters are replaced with underscores.

## Maintaining Test Parity

When new tests are added to the JavaScript codebase:

1. Run the test analyzer: `python utils/test_coverage/test_analyzer.py`
2. Review the generated report in `new_python_tests/test_coverage_report.md`
3. Add any missing test functions to the appropriate Python test file
4. Re-run the analyzer to confirm 100% coverage

## Directory Structure

```
new_python_tests/
├── test_arbitrary_properties.py  # Maps to arbitrary-properties.test.ts
└── ... (more test files)
```

## Testing Guidelines

1. Python assertions should have the same inputs and expected outputs as their JavaScript counterparts.
2. Each test file should include a docstring referencing the original JavaScript file.
3. Each test function should include a docstring explaining its purpose.

## Coverage Analysis

The test coverage analyzer in `utils/test_coverage/test_analyzer.py` evaluates test parity based on function names rather than exact assertion matching. This makes it easier to maintain parity while allowing for Python-specific implementation details.

Run the analyzer to generate a coverage report that highlights:
- Missing Python tests that exist in JavaScript
- Extra Python tests that don't exist in JavaScript
- Overall test function coverage statistics 