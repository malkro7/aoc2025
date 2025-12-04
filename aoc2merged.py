"""Day 2 merged runner.

Provides `parta(lines)` using the exact-two-block rule and
`partb(lines)` using the repeated-pattern rule. `main()` reads an
input file once and prints both parts' invalid numbers and totals.
"""
from typing import Iterable, List
import argparse


def is_exact_two_block_repeat(s: str) -> bool:
    if not s:
        return False
    if len(s) % 2 != 0:
        return False
    half = len(s) // 2
    return s[:half] == s[half:]


def is_repeated_pattern(s: str) -> bool:
    n = len(s)
    if n == 0:
        return False
    for size in range(1, n // 2 + 1):
        if n % size == 0:
            block = s[:size]
            if block * (n // size) == s:
                return True
    return False


def expand_item(item: str):
    """Yield integers for a single item which may be a number or a range 'start-end'."""
    item = item.strip()
    if not item:
        return
    if "-" in item:
        try:
            start_str, end_str = item.split("-", 1)
            start, end = int(start_str), int(end_str)
            if start <= end:
                for v in range(start, end + 1):
                    yield v
            else:
                for v in range(end, start + 1):
                    yield v
        except ValueError:
            return
    else:
        try:
            yield int(item)
        except ValueError:
            return


def parta(lines: Iterable[str]) -> List[int]:
    """Collect invalid numbers using the exact-two-block rule."""
    invalids: List[int] = []
    for line in lines:
        parts = [p.strip() for p in line.strip().split(",") if p.strip()]
        for p in parts:
            for num in expand_item(p):
                if is_exact_two_block_repeat(str(num)):
                    invalids.append(num)
    return invalids


def partb(lines: Iterable[str]) -> List[int]:
    """Collect invalid numbers using the repeated-pattern rule."""
    invalids: List[int] = []
    for line in lines:
        parts = [p.strip() for p in line.strip().split(",") if p.strip()]
        for p in parts:
            for num in expand_item(p):
                if is_repeated_pattern(str(num)):
                    invalids.append(num)
    return invalids


def _print_results(title: str, invalids: List[int]):
    print(f"\n=== {title} ===")
    if invalids:
        for n in invalids:
            print(n)
    else:
        print("(none)")
    print("\nTotal Invalid Count:", len(invalids))
    print("Sum of Invalid Numbers:", sum(invalids) if invalids else 0)


def main():
    parser = argparse.ArgumentParser(description="Run part A and part B for day 2")
    parser.add_argument("input", nargs="?", default="day2input.txt", help="input file path")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    invalids_a = parta(raw_lines)
    invalids_b = partb(raw_lines)

    _print_results("Part A - Exact Two-Block Repeats", invalids_a)
    _print_results("Part B - Repeated Pattern", invalids_b)


if __name__ == "__main__":
    main()
