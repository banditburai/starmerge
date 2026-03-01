"""Benchmarks for StarMerge internal hot path components (uncached)."""

import time
import statistics
from starmerge import get_default_config
from starmerge.lib.class_group_utils import _create_class_map, create_class_group_utils
from starmerge.lib.config_utils import create_config_utils
from starmerge.lib.create_tailwind_merge import _ConfigUtilsWrapper
from starmerge.lib.merge_classlist import merge_class_list
from starmerge.lib.parse_class_name import create_parse_class_name
from starmerge.lib.sort_modifiers import create_sort_modifiers


def bench(name: str, fn, iterations: int = 10_000):
    """Run benchmark with multiple trials, report median."""
    for _ in range(1000):
        fn()

    trials = []
    for _ in range(5):
        start = time.perf_counter_ns()
        for _ in range(iterations):
            fn()
        elapsed = time.perf_counter_ns() - start
        trials.append(elapsed / iterations)

    median = statistics.median(trials)
    print(f"  {name:.<55} {median / 1000:>7.2f} us/call")
    return median


def main():
    config = get_default_config()
    config_utils = _ConfigUtilsWrapper(create_config_utils(config))
    parse = create_parse_class_name(config)
    sort_mods = create_sort_modifiers(config)
    get_class_group_id, _ = create_class_group_utils(config)

    print("\n=== StarMerge Hot Path Benchmarks ===\n")

    # --- merge_class_list (uncached) ---
    print("[ merge_class_list ]")
    cases = [
        ("2 classes, no conflict", "p-4 text-red-500"),
        ("2 classes, conflict", "p-4 p-2"),
        ("5 classes, mixed", "p-4 px-2 pt-3 text-red-500 bg-blue-200"),
        ("8 classes, typical", (
            "p-4 px-2 pt-3 text-red-500 bg-blue-200 font-bold "
            "hover:text-green-300 focus:ring-2"
        )),
        ("10 classes", (
            "p-4 px-2 pt-3 text-red-500 bg-blue-200 font-bold "
            "hover:text-green-300 focus:ring-2 sm:p-6 md:text-lg"
        )),
        ("20 classes", (
            "p-4 px-2 pt-3 text-red-500 bg-blue-200 font-bold "
            "hover:text-green-300 focus:ring-2 sm:p-6 md:text-lg "
            "w-full h-screen flex items-center justify-center "
            "gap-4 rounded-lg shadow-md border border-gray-200"
        )),
        ("5 all conflicts", "p-1 p-2 p-3 p-4 p-5"),
        ("non-tailwind classes", "custom-class my-thing other-class foo bar"),
    ]
    for name, cls in cases:
        bench(name, lambda cls=cls: merge_class_list(cls, config_utils))

    print()

    # --- sort_modifiers ---
    print("[ sort_modifiers ]")
    bench("0 modifiers", lambda: sort_mods([]))
    bench("1 modifier", lambda: sort_mods(["hover"]))
    bench("3 modifiers", lambda: sort_mods(["sm", "hover", "focus"]))
    bench("5 modifiers", lambda: sort_mods(["sm", "md", "hover", "focus", "active"]))
    bench("3 with order-sensitive", lambda: sort_mods(["hover", "[&>*]", "focus"]))
    bench("5 with 2 order-sensitive", lambda: sort_mods(["sm", "[&>*]", "hover", "[&:nth-child(2)]", "focus"]))

    print()

    # --- get_class_group_id ---
    print("[ get_class_group_id ]")
    bench("simple: 'flex'", lambda: get_class_group_id("flex"))
    bench("simple: 'p-4'", lambda: get_class_group_id("p-4"))
    bench("compound: 'bg-red-500'", lambda: get_class_group_id("bg-red-500"))
    bench("compound: 'text-lg'", lambda: get_class_group_id("text-lg"))
    bench("arbitrary: '[color:red]'", lambda: get_class_group_id("[color:red]"))
    bench("arbitrary: '[padding:10px]'", lambda: get_class_group_id("[padding:10px]"))
    bench("miss: 'not-a-class'", lambda: get_class_group_id("not-a-class"))
    bench("negative: '-inset-1'", lambda: get_class_group_id("-inset-1"))

    print()

    # --- parse_class_name (sequential realistic parsing) ---
    print("[ parse_class_name ]")
    realistic_classes = [
        "p-4", "hover:text-red-500", "sm:flex", "md:hover:bg-blue-200",
        "focus:ring-2", "[color:red]", "bg-red-500/50", "text-lg!",
        "sm:hover:focus:p-4!", "dark:md:hover:text-white",
    ]
    bench("10 realistic classes (sequential)", lambda: [parse(c) for c in realistic_classes])
    bench("simple 'p-4'", lambda: parse("p-4"))
    bench("modifier 'hover:p-4'", lambda: parse("hover:p-4"))
    bench("deep 'sm:hover:focus:p-4!'", lambda: parse("sm:hover:focus:p-4!"))
    bench("arbitrary '[color:red]'", lambda: parse("[color:red]"))
    bench("postfix 'bg-red-500/50'", lambda: parse("bg-red-500/50"))

    print()

    # --- _create_class_map ---
    print("[ _create_class_map ]")
    bench("create_class_map", lambda: _create_class_map(config), iterations=100)

    print()

    # --- Real-world patterns ---
    print("[ Real-world patterns ]")
    bench("deeply nested modifiers", lambda: merge_class_list(
        "sm:hover:focus:active:p-4 sm:hover:focus:active:p-2 "
        "md:dark:hover:text-white md:dark:hover:text-black "
        "lg:focus-visible:ring-2 lg:focus-visible:ring-4",
        config_utils,
    ))
    bench("heavy conflict scenario", lambda: merge_class_list(
        "p-1 p-2 p-3 p-4 p-5 m-1 m-2 m-3 m-4 m-5 "
        "text-xs text-sm text-base text-lg text-xl "
        "font-thin font-light font-normal font-medium font-bold",
        config_utils,
    ))
    bench("responsive utility-heavy", lambda: merge_class_list(
        "w-full sm:w-1/2 md:w-1/3 lg:w-1/4 xl:w-1/5 "
        "p-2 sm:p-4 md:p-6 lg:p-8 xl:p-10 "
        "text-sm sm:text-base md:text-lg lg:text-xl xl:text-2xl "
        "flex sm:grid md:block lg:inline-flex xl:inline-grid",
        config_utils,
    ))
    bench("arbitrary values mix", lambda: merge_class_list(
        "p-[10px] m-[20px] text-[14px] bg-[#ff0000] w-[calc(100%-20px)] "
        "h-[var(--height)] border-[length:2px] [color:blue]",
        config_utils,
    ))

    print()


if __name__ == "__main__":
    main()
