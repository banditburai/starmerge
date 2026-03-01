#!/usr/bin/env python3
"""Run all StarMerge benchmarks, summarize results, and optionally compare with previous runs."""

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

BENCHMARKS_DIR = Path(__file__).parent
RESULTS_FILE = BENCHMARKS_DIR / ".results.json"

BENCH_FILES = [
    BENCHMARKS_DIR / "bench_core.py",
    BENCHMARKS_DIR / "bench_hot_path.py",
]

# Matches lines like:  merge: simple (2 classes)..................    1.23 us/call
RESULT_RE = re.compile(
    r"^\s{2}(.+?)\.\.*\s+([\d.]+)\s+us/call",
)
# Matches throughput lines like:  Throughput (8-class merge).................. 123,456 ops/sec
THROUGHPUT_RE = re.compile(
    r"^\s{2}(.+?)\.\.*\s+([\d,]+)\s+ops/sec",
)


def run_bench(path: Path) -> tuple[str, dict[str, float], set[str]]:
    """Run a benchmark file and parse its output. Returns (raw_output, parsed_results, throughput_names)."""
    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"FAILED: {path.name}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    output = result.stdout
    results: dict[str, float] = {}
    throughput_names: set[str] = set()
    for line in output.splitlines():
        m = RESULT_RE.match(line)
        if m:
            name = m.group(1).strip()
            results[name] = float(m.group(2))
            continue
        m = THROUGHPUT_RE.match(line)
        if m:
            name = m.group(1).strip()
            results[name] = float(m.group(2).replace(",", ""))
            throughput_names.add(name)

    return output, results, throughput_names


def print_summary(
    all_results: dict[str, float],
    throughput_names: set[str],
    previous: dict[str, float] | None = None,
):
    """Print a summary table with optional comparison."""
    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)

    if previous:
        print(f"  {'Benchmark':<45} {'Now':>10} {'Prev':>10} {'Delta':>10}")
        print(f"  {'-' * 45} {'-' * 10} {'-' * 10} {'-' * 10}")
    else:
        print(f"  {'Benchmark':<45} {'Result':>10}")
        print(f"  {'-' * 45} {'-' * 10}")

    for name, value in all_results.items():
        is_throughput = name in throughput_names

        if is_throughput:
            val_str = f"{value:>8,.0f} op/s"
        else:
            val_str = f"{value:>7.2f} us"

        if previous and name in previous:
            prev = previous[name]
            if is_throughput:
                prev_str = f"{prev:>8,.0f} op/s"
            else:
                prev_str = f"{prev:>7.2f} us"
            pct = ((value - prev) / prev) * 100 if prev else 0
            marker = "+" if pct > 0 else ""
            delta_str = f"{marker}{pct:.1f}%"
            print(f"  {name:<45} {val_str:>10} {prev_str:>10} {delta_str:>10}")
        else:
            print(f"  {name:<45} {val_str:>10}")

    print("=" * 78)


def main():
    parser = argparse.ArgumentParser(description="Run StarMerge benchmarks")
    parser.add_argument(
        "--compare", action="store_true", help="Compare with last saved results"
    )
    parser.add_argument(
        "--save", action="store_true", help="Save results to .results.json"
    )
    args = parser.parse_args()

    previous = None
    if args.compare and RESULTS_FILE.exists():
        previous = json.loads(RESULTS_FILE.read_text())
        print(f"Loaded previous results from {RESULTS_FILE.name}")

    all_results: dict[str, float] = {}
    all_throughput: set[str] = set()

    total_start = time.perf_counter()
    for bench_file in BENCH_FILES:
        print(f"\n>>> Running {bench_file.name} ...")
        output, results, throughput_names = run_bench(bench_file)
        print(output)
        all_results.update(results)
        all_throughput.update(throughput_names)
    total_elapsed = time.perf_counter() - total_start

    print_summary(all_results, all_throughput, previous)
    print(f"\nTotal time: {total_elapsed:.1f}s")

    if args.save:
        RESULTS_FILE.write_text(json.dumps(all_results, indent=2) + "\n")
        print(f"Results saved to {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
