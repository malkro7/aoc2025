"""Day 3 merged runner.

Provides `parta(lines)`, `partb(lines, k=12)` and a `main()` that reads
an input file once and prints both results.
"""

from typing import Iterable, List
import argparse


def max_joltage(line: str) -> int:
    digits = list(map(int, line.strip()))
    best = -1

    for i in range(len(digits)):
        d1 = digits[i]
        if i == len(digits) - 1:
            continue

        d2 = max(digits[i + 1 :])
        joltage = d1 * 10 + d2

        if joltage > best:
            best = joltage

    return best


def max_k_subsequence(s: str, k: int) -> str:
    """Return lexicographically largest subsequence of length k."""
    stack: List[str] = []
    to_remove = len(s) - k  # how many digits we are allowed to drop

    for digit in s:
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    # If removals left, cut from end
    return "".join(stack[:k])


def parta(lines: Iterable[str]) -> int:
    """Compute the total 'joltage' as in the original `aoc3.py`.

    `lines` should be an iterable of raw input lines (may include newlines).
    Returns the integer total.
    """
    total = 0
    for line in lines:
        s = line.strip()
        if not s:
            continue
        total += max_joltage(s)
    return total


def partb(lines: Iterable[str], k: int = 12) -> int:
    """Compute the total using the largest k-digit subsequence per line.

    Returns the integer total (sum of int(max_k_subsequence(...))).
    """
    total = 0
    for line in lines:
        seq = line.strip()
        if not seq:
            continue
        best = int(max_k_subsequence(seq, k))
        total += best
    return total


def main():
    parser = argparse.ArgumentParser(description="Run part A and part B for day 3")
    parser.add_argument("input", nargs="?", default="day3input.txt", help="input file path")
    parser.add_argument("--k", type=int, default=12, help="subsequence length for part B")
    args = parser.parse_args()

    # Read file once
    with open(args.input, "r") as f:
        raw_lines = f.readlines()

    a = parta(raw_lines)
    b = partb(raw_lines, k=args.k)

    print("Part A Total Joltage:", a)
    print("Part B Total (k={}) :".format(args.k), b)


if __name__ == "__main__":
    main()
