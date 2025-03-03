#!/usr/bin/env python3
"""
Test Coverage Analyzer for tailwind-merge-py

A simplified approach that focuses on test function/method parity rather than exact assertion matching.
This makes it easier to maintain and extend test coverage over time.
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict
import difflib

# Paths to the test directories
JS_TESTS_DIR = 'js-source/tests'
PY_TESTS_DIR = 'tests'  # Using the new clean directory

# Regular expressions to extract test functions/methods
JS_TEST_PATTERN = re.compile(r'test\([\'"]([^\'"]+)[\'"]')  # Matches test('test name')
PY_TEST_PATTERN = re.compile(r'def\s+test_([a-zA-Z0-9_]+)')  # Matches def test_function_name

# Mapping between JS test files and Python test files
# This maintains a direct 1:1 relationship between files
JS_TO_PY_FILE_MAPPING = {
    'arbitrary-properties.test.ts': 'test_arbitrary_properties.py',
    'arbitrary-values.test.ts': 'test_arbitrary_values.py',
    'arbitrary-variants.test.ts': 'test_arbitrary_variants.py',
    'class-group-conflicts.test.ts': 'test_class_group_conflicts.py',
    'class-map.test.ts': 'test_class_map.py',
    'class-utils.test.ts': 'test_class_utils.py',
    'colors.test.ts': 'test_colors.py',
    'conflicts-across-class-groups.test.ts': 'test_conflicts_across_class_groups.py',
    'content-utilities.test.ts': 'test_content_utilities.py',
    'core-concepts.test.ts': 'test_core_concepts.py',
    'create-tailwind-merge.test.ts': 'test_create_tailwind_merge.py',
    'default-config.test.ts': 'test_default_config.py',
    'docs-examples.test.ts': 'test_docs_examples.py',
    'experimental-parse-class-name.test.ts': 'test_experimental_parse_class_name.py',
    'extend-tailwind-merge.test.ts': 'test_extend_tailwind_merge.py',
    'extending-theme.test.ts': 'test_extending_theme.py',
    'important-modifier.test.ts': 'test_important_modifier.py',
    'lazy-initialization.test.ts': 'test_lazy_initialization.py',
    'merge-classlist.test.ts': 'test_merge_classlist.py',
    'merge-configs.test.ts': 'test_merge_configs.py',
    'modifiers.test.ts': 'test_modifiers.py',
    'negative-values.test.ts': 'test_negative_values.py',
    'non-conflicting-classes.test.ts': 'test_non_conflicting_classes.py',
    'non-tailwind-classes.test.ts': 'test_non_tailwind_classes.py',
    'per-side-border-colors.test.ts': 'test_per_side_border_colors.py',
    'prefixes.test.ts': 'test_prefixes.py',
    'pseudo-variants.test.ts': 'test_pseudo_variants.py',
    'public-api.test.ts': 'test_public_api.py',
    'standalone-classes.test.ts': 'test_standalone_classes.py',
    'tailwind-css-versions.test.ts': 'test_tailwind_css_versions.py',
    'theme.test.ts': 'test_theme.py',
    'tw-join.test.ts': 'test_tw_join.py',
    'tw-merge.test.ts': 'test_tw_merge.py',
    'type-generics.test.ts': 'test_type_generics.py',
    'validators.test.ts': 'test_validators.py',
    # Add more mappings as files are created
}


def js_name_to_py_name(js_name, js_file_path=None):
    """Convert a JavaScript test name to a Python test function name."""
    # Special case for validators.test.ts - convert isX to test_is_x
    if js_file_path and 'validators.test.ts' in js_file_path and js_name.startswith('is'):
        # Convert isArbitraryValue to test_is_arbitrary_value
        words = re.findall('[A-Z][a-z]*|[a-z]+', js_name)
        return 'test_' + '_'.join([word.lower() for word in words])
    
    # Regular case - standard conversion
    # Replace spaces and special chars with underscores
    py_name = re.sub(r'[^a-zA-Z0-9]+', '_', js_name.lower())
    # Remove leading/trailing underscores
    py_name = py_name.strip('_')
    # Prepend "test_" if not already there
    if not py_name.startswith('test_'):
        py_name = 'test_' + py_name
    return py_name


def extract_js_tests(js_file_path):
    """Extract test names from a JavaScript test file."""
    tests = []
    
    try:
        with open(js_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all test functions/methods
        matches = JS_TEST_PATTERN.finditer(content)
        
        for match in matches:
            test_name = match.group(1)
            expected_py_name = js_name_to_py_name(test_name, js_file_path)
            
            tests.append({
                'original_name': test_name,
                'expected_py_name': expected_py_name,
                'line': content[:match.start()].count('\n') + 1
            })
    except Exception as e:
        print(f"Error extracting tests from {js_file_path}: {e}")
    
    return tests


def extract_py_tests(py_file_path):
    """Extract test function names from a Python test file."""
    tests = []
    
    try:
        with open(py_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract all def test_* function definitions
        matches = PY_TEST_PATTERN.finditer(content)
        for match in matches:
            test_name = match.group(1)
            tests.append({
                'function_name': f'test_{test_name}',
                'line': content[:match.start()].count('\n') + 1
            })
    except Exception as e:
        print(f"Error extracting tests from {py_file_path}: {e}")
        
    return tests


def normalize_function_name(name):
    """Normalize function names to a common format for comparison."""
    # Remove prefixes and common testing words
    for prefix in ['test_', 'it_', 'describe_', 'isAny', 'is_any']:
        if name.startswith(prefix):
            name = name[len(prefix):]

    # Convert between snake_case and camelCase
    if '_' in name:
        # Convert snake_case to lowercase for comparison
        parts = name.split('_')
        normalized = parts[0].lower()
        for part in parts[1:]:
            normalized += part.capitalize()
        return normalized
    else:
        # Convert camelCase to lowercase for comparison
        result = ''
        for char in name:
            if char.isupper():
                result += '_' + char.lower()
            else:
                result += char
        return result.lower()


def similarity_score(str1, str2):
    """
    Calculate a similarity score between two strings.
    Returns a value between 0 and 1, where 1 is an exact match.
    """
    return difflib.SequenceMatcher(None, str1, str2).ratio()


def map_javascript_test_to_python_test(js_test, py_tests, js_file, py_file):
    """Map a JavaScript test name to its Python equivalent using smart matching."""
    normalized_js_test = normalize_function_name(js_test)
    
    # Special case for validators test - convert isX to test_is_x
    if 'validators.test.ts' in js_file and js_test.startswith('is'):
        # Convert isArbitraryValue to test_is_arbitrary_value
        py_test_name = 'test_' + '_'.join([word.lower() for word in re.findall('[A-Z][a-z]*|[a-z]+', js_test)])
        for py_test in py_tests:
            if py_test == py_test_name:
                return py_test
    
    for py_test in py_tests:
        normalized_py_test = normalize_function_name(py_test)
        if normalized_js_test == normalized_py_test:
            return py_test
        
        # Handle cases where test name might be slightly different
        if (normalized_js_test in normalized_py_test or 
            normalized_py_test in normalized_js_test or
            similarity_score(normalized_js_test, normalized_py_test) > 0.8):
            return py_test
    
    return None


def analyze_file_pair(js_file, py_file):
    """Analyze test coverage between a JavaScript and Python file pair."""
    js_file_path = os.path.join(JS_TESTS_DIR, js_file)
    py_file_path = os.path.join(PY_TESTS_DIR, py_file)
    
    # Check if both files exist
    if not os.path.isfile(js_file_path):
        return {
            'js_file': js_file,
            'py_file': py_file,
            'error': f"JavaScript file not found: {js_file_path}"
        }
    
    if not os.path.isfile(py_file_path):
        return {
            'js_file': js_file,
            'py_file': py_file,
            'error': f"Python file not found: {py_file_path}"
        }
    
    # Extract tests from both files
    js_tests = extract_js_tests(js_file_path)
    py_tests = extract_py_tests(py_file_path)
    
    # Find matches and mismatches
    py_test_names = [test['function_name'] for test in py_tests]
    
    matched_tests = []
    missing_tests = []
    
    for js_test in js_tests:
        expected_py_name = js_test['expected_py_name']
        if expected_py_name in py_test_names:
            matched_tests.append({
                'js_name': js_test['original_name'],
                'py_name': expected_py_name
            })
        else:
            missing_tests.append({
                'js_name': js_test['original_name'],
                'expected_py_name': expected_py_name,
                'js_line': js_test['line']
            })
    
    # Also identify extra Python tests not in JS
    js_expected_names = [test['expected_py_name'] for test in js_tests]
    extra_tests = [
        test for test in py_tests
        if test['function_name'] not in js_expected_names
    ]
    
    return {
        'js_file': js_file,
        'py_file': py_file,
        'js_tests': len(js_tests),
        'py_tests': len(py_tests),
        'matched_tests': len(matched_tests),
        'coverage': len(matched_tests) / len(js_tests) if js_tests else 1.0,
        'missing_tests': missing_tests,
        'extra_tests': extra_tests
    }


def analyze_coverage():
    """Analyze test coverage across all mapped files."""
    results = {
        'file_coverage': [],
        'summary': {
            'js_files': 0,
            'py_files': 0,
            'js_tests': 0,
            'py_tests': 0,
            'matched_tests': 0
        }
    }
    
    # Analyze each file pair
    for js_file, py_file in JS_TO_PY_FILE_MAPPING.items():
        if not py_file:
            continue
            
        file_result = analyze_file_pair(js_file, py_file)
        results['file_coverage'].append(file_result)
        
        # Update summary counts (if no error)
        if 'error' not in file_result:
            results['summary']['js_files'] += 1
            results['summary']['py_files'] += 1
            results['summary']['js_tests'] += file_result['js_tests']
            results['summary']['py_tests'] += file_result['py_tests']
            results['summary']['matched_tests'] += file_result['matched_tests']
    
    # Calculate overall coverage
    total_js_tests = results['summary']['js_tests']
    matched_tests = results['summary']['matched_tests']
    results['summary']['overall_coverage'] = matched_tests / total_js_tests if total_js_tests > 0 else 1.0
    
    return results


def format_results(results):
    """Format results for display in a readable report."""
    output = []
    
    # Summary
    output.append("# Test Function Coverage Analysis")
    output.append("")
    output.append(f"JavaScript Files: {results['summary']['js_files']}")
    output.append(f"Python Files: {results['summary']['py_files']}")
    output.append(f"JavaScript Tests: {results['summary']['js_tests']}")
    output.append(f"Python Tests: {results['summary']['py_tests']}")
    output.append(f"Matched Tests: {results['summary']['matched_tests']}")
    output.append(f"Overall Coverage: {results['summary']['overall_coverage']:.2%}")
    output.append("")
    
    # File coverage
    output.append("## File Coverage")
    output.append("")
    output.append("| JavaScript File | Python File | JS Tests | PY Tests | Matched | Coverage | Status |")
    output.append("|----------------|------------|----------|----------|---------|----------|--------|")
    
    for file_coverage in sorted(results['file_coverage'], key=lambda x: x.get('coverage', 0)):
        js_file = file_coverage['js_file']
        py_file = file_coverage['py_file']
        
        if 'error' in file_coverage:
            output.append(f"| {js_file} | {py_file} | - | - | - | - | Error: {file_coverage['error']} |")
            continue
            
        js_tests = file_coverage['js_tests']
        py_tests = file_coverage['py_tests']
        matched = file_coverage['matched_tests']
        coverage = f"{file_coverage['coverage']:.2%}"
        status = "Complete" if file_coverage['coverage'] == 1.0 else "Partial"
        
        output.append(f"| {js_file} | {py_file} | {js_tests} | {py_tests} | {matched} | {coverage} | {status} |")
    
    output.append("")
    
    # Missing tests
    missing_tests_exist = any(
        'missing_tests' in fc and fc['missing_tests'] 
        for fc in results['file_coverage'] 
        if 'error' not in fc
    )
    
    if missing_tests_exist:
        output.append("## Missing Tests")
        output.append("")
        
        for file_coverage in results['file_coverage']:
            if 'error' in file_coverage or not file_coverage.get('missing_tests'):
                continue
                
            js_file = file_coverage['js_file']
            py_file = file_coverage['py_file']
            missing_tests = file_coverage['missing_tests']
            
            output.append(f"### {js_file} -> {py_file}")
            output.append("")
            output.append("| Line | JavaScript Test | Expected Python Function |")
            output.append("|------|----------------|--------------------------|")
            
            for test in missing_tests:
                line = test['js_line']
                js_name = test['js_name']
                py_name = test['expected_py_name']
                
                output.append(f"| {line} | `{js_name}` | `{py_name}` |")
            
            output.append("")
    
    # Extra tests
    extra_tests_exist = any(
        'extra_tests' in fc and fc['extra_tests'] 
        for fc in results['file_coverage'] 
        if 'error' not in fc
    )
    
    if extra_tests_exist:
        output.append("## Extra Python Tests")
        output.append("")
        output.append("These Python tests don't have a direct JavaScript equivalent:")
        output.append("")
        
        for file_coverage in results['file_coverage']:
            if 'error' in file_coverage or not file_coverage.get('extra_tests'):
                continue
                
            py_file = file_coverage['py_file']
            extra_tests = file_coverage['extra_tests']
            
            output.append(f"### {py_file}")
            output.append("")
            output.append("| Line | Python Function |")
            output.append("|------|----------------|")
            
            for test in extra_tests:
                line = test['line']
                name = test['function_name']
                
                output.append(f"| {line} | `{name}` |")
            
            output.append("")
    
    return "\n".join(output)


def main():
    """Main function to run the analysis."""
    print("Analyzing test function coverage between JavaScript and Python implementations...")
    
    # Check if both directories exist
    if not os.path.isdir(JS_TESTS_DIR):
        print(f"Error: JavaScript tests directory not found: {JS_TESTS_DIR}")
        sys.exit(1)
    
    if not os.path.isdir(PY_TESTS_DIR):
        print(f"Error: Python tests directory not found: {PY_TESTS_DIR}")
        sys.exit(1)
    
    # Run analysis
    results = analyze_coverage()
    
    # Generate report
    report = format_results(results)
    
    # Write report to file
    report_file = os.path.join(PY_TESTS_DIR, 'test_coverage_report.md')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Test coverage report written to: {report_file}")
    
    # Write raw results as JSON for further processing
    json_file = os.path.join(PY_TESTS_DIR, 'test_coverage_data.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Raw coverage data written to: {json_file}")
    
    # Summary
    total_js_tests = results['summary']['js_tests']
    matched_tests = results['summary']['matched_tests']
    overall_coverage = matched_tests / total_js_tests if total_js_tests > 0 else 1.0
    
    print(f"\nOverall Test Function Coverage: {overall_coverage:.2%}")
    print(f"JavaScript Tests: {total_js_tests}")
    print(f"Matched Tests: {matched_tests}")
    print(f"Missing Tests: {total_js_tests - matched_tests}")


if __name__ == "__main__":
    main() 