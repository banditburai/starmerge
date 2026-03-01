"""Benchmarks for StarMerge core hot paths."""

import time
from starmerge import merge, tw_join, get_default_config
from starmerge.lib.lru_cache import create_lru_cache
from starmerge.lib.validators import (
    is_length, is_color, is_number, is_arbitrary_value,
    is_arbitrary_variable, is_tshirt_size, is_fraction,
)
from starmerge.lib.parse_class_name import create_parse_class_name


def bench(name: str, fn, iterations: int = 10_000):
    # Warmup
    for _ in range(100):
        fn()

    start = time.perf_counter_ns()
    for _ in range(iterations):
        fn()
    elapsed_ns = time.perf_counter_ns() - start

    per_call_ns = elapsed_ns / iterations
    per_call_us = per_call_ns / 1000
    total_ms = elapsed_ns / 1_000_000

    print(f"  {name:.<50} {per_call_us:>8.2f} us/call  ({total_ms:.1f}ms total, {iterations:,} iters)")
    return per_call_ns


def main():
    config = get_default_config()
    parse = create_parse_class_name(config)

    print("\n=== StarMerge Benchmarks ===\n")

    # --- tailwind_merge / merge ---
    print("[ merge / tailwind_merge ]")
    bench("merge: simple (2 classes)", lambda: merge("p-4 p-2"))
    bench("merge: medium (5 classes)", lambda: merge("p-4 px-2 text-red-500 bg-blue-200 font-bold"))
    bench("merge: conflict resolution", lambda: merge("p-4 px-2 pt-3"))
    bench("merge: modifiers", lambda: merge("hover:p-4 hover:p-2"))
    bench("merge: complex (10 classes)", lambda: merge(
        "p-4 px-2 pt-3 text-red-500 bg-blue-200 font-bold hover:text-green-300 "
        "focus:ring-2 sm:p-6 md:text-lg"
    ))
    bench("merge: long string (20 classes)", lambda: merge(
        "p-4 px-2 pt-3 text-red-500 bg-blue-200 font-bold hover:text-green-300 "
        "focus:ring-2 sm:p-6 md:text-lg w-full h-screen flex items-center "
        "justify-center gap-4 rounded-lg shadow-md border border-gray-200"
    ))
    bench("merge: no conflicts", lambda: merge("p-4 text-red-500 bg-blue-200 font-bold"))
    bench("merge: all conflicts", lambda: merge("p-1 p-2 p-3 p-4 p-5"))

    print()

    # --- tw_join ---
    print("[ tw_join ]")
    bench("tw_join: simple strings", lambda: tw_join("p-4", "text-red-500"))
    bench("tw_join: 5 strings", lambda: tw_join("p-4", "text-red-500", "bg-blue-200", "font-bold", "m-2"))
    bench("tw_join: nested lists", lambda: tw_join(["p-4", ["text-red-500", "bg-blue-200"]], "font-bold"))
    bench("tw_join: with falsy values", lambda: tw_join("p-4", None, False, "", "text-red-500", 0))

    print()

    # --- LRU Cache ---
    print("[ LRU Cache ]")
    cache = create_lru_cache(500)
    cache.set("test-key", "test-value")
    bench("cache: hit", lambda: cache.get("test-key"))
    bench("cache: miss", lambda: cache.get("nonexistent"))
    bench("cache: set", lambda: cache.set("bench-key", "bench-value"))

    print()

    # --- Validators ---
    print("[ Validators ]")
    bench("is_length: '10px'", lambda: is_length("10px"))
    bench("is_length: '1.5rem'", lambda: is_length("1.5rem"))
    bench("is_color: '#ff0000'", lambda: is_color("#ff0000"))
    bench("is_color: 'rgb(255,0,0)'", lambda: is_color("rgb(255,0,0)"))
    bench("is_number: '42'", lambda: is_number("42"))
    bench("is_number: '3.14'", lambda: is_number("3.14"))
    bench("is_arbitrary_value: '[10px]'", lambda: is_arbitrary_value("[10px]"))
    bench("is_arbitrary_variable: '(--my-var)'", lambda: is_arbitrary_variable("(--my-var)"))
    bench("is_tshirt_size: 'xl'", lambda: is_tshirt_size("xl"))
    bench("is_fraction: '1/2'", lambda: is_fraction("1/2"))

    print()

    # --- Parse class name ---
    print("[ Parse class name ]")
    bench("parse: simple 'p-4'", lambda: parse("p-4"))
    bench("parse: with modifier 'hover:p-4'", lambda: parse("hover:p-4"))
    bench("parse: complex 'sm:hover:focus:p-4!'", lambda: parse("sm:hover:focus:p-4!"))
    bench("parse: arbitrary '[color:red]'", lambda: parse("[color:red]"))
    bench("parse: postfix 'bg-red-500/50'", lambda: parse("bg-red-500/50"))

    print()

    # --- Config initialization ---
    print("[ Config initialization ]")
    bench("get_default_config", get_default_config, iterations=1_000)

    print()

    # --- End-to-end throughput ---
    print("[ Throughput ]")
    classes = "p-4 px-2 pt-3 text-red-500 bg-blue-200 font-bold hover:text-green-300 focus:ring-2"
    iters = 50_000
    start = time.perf_counter_ns()
    for _ in range(iters):
        merge(classes)
    elapsed = time.perf_counter_ns() - start
    ops_per_sec = iters / (elapsed / 1_000_000_000)
    print(f"  Throughput (8-class merge).................. {ops_per_sec:>10,.0f} ops/sec")

    # Uncached throughput (unique strings)
    unique_classes = [f"p-{i} px-{i} text-red-{i}" for i in range(1000)]
    start = time.perf_counter_ns()
    for cls in unique_classes:
        merge(cls)
    elapsed = time.perf_counter_ns() - start
    ops_per_sec = len(unique_classes) / (elapsed / 1_000_000_000)
    print(f"  Throughput (uncached, unique strings)....... {ops_per_sec:>10,.0f} ops/sec")

    print()


if __name__ == "__main__":
    main()
