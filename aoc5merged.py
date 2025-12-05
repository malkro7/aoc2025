"""Day 5 merged runner.

Provides `parta(content)` which counts fresh IDs matching ranges and
`partb(content)` which counts unique fresh IDs by merging overlapping ranges.
`main()` reads the input file once and prints both results.
"""
from typing import List, Tuple
import argparse


def parse_ranges_and_ids(content: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    """Parse the input content into ranges and IDs."""
    sections = content.strip().split("\n\n")
    range_lines = sections[0].splitlines()
    id_lines = sections[1].splitlines()

    # Parse ranges
    ranges = []
    for line in range_lines:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    # Parse available IDs
    ids = [int(x) for x in id_lines]

    return ranges, ids


def parta(content: str) -> int:
    """Count fresh IDs that fall within at least one range."""
    ranges, ids = parse_ranges_and_ids(content)

    def is_fresh(id_val: int) -> bool:
        for start, end in ranges:
            if start <= id_val <= end:
                return True
        return False

    return sum(1 for id_val in ids if is_fresh(id_val))


def partb(content: str) -> int:
    """Count unique fresh IDs by merging overlapping ranges."""
    ranges, _ = parse_ranges_and_ids(content)

    if not ranges:
        return 0

    # Sort ranges by start
    ranges.sort()

    # Merge overlapping ranges
    merged: List[Tuple[int, int]] = []
    curr_start, curr_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= curr_end + 1:  # overlap or touching
            curr_end = max(curr_end, end)
        else:
            merged.append((curr_start, curr_end))
            curr_start, curr_end = start, end

    merged.append((curr_start, curr_end))

    # Count unique fresh IDs
    total_fresh = sum((end - start + 1) for start, end in merged)

    return total_fresh


def main():
    parser = argparse.ArgumentParser(description="Run part A and part B for day 5")
    parser.add_argument("input", nargs="?", default="day5input.txt", help="input file path")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    a = parta(content)
    b = partb(content)

    print("Part A - Count of fresh IDs:", a)
    print("Part B - Count of unique fresh IDs (merged ranges):", b)


if __name__ == "__main__":
    main()
