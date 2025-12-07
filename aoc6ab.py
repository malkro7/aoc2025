"""Day 6 merged runner.

Provides `parta(lines)` which solves the worksheet (left-to-right column processing)
and `partb(lines)` which solves the worksheet (right-to-left column processing).
`main()` reads the input file once and prints both results.
"""
from typing import List
import argparse


def solve_worksheet_parta(lines: List[str]) -> int:
    """Part A: Process columns left-to-right, extracting numbers in order."""
    # Normalize row length
    width = max(len(line) for line in lines) if lines else 0
    grid = [line.ljust(width) for line in lines]

    # Transpose: column-wise extraction
    columns = [''.join(grid[r][c] for r in range(len(grid))) for c in range(width)]

    # Segment columns into problems
    problems = []
    current = []

    for col in columns:
        if col.strip():
            current.append(col)
        else:
            if current:
                problems.append(current)
                current = []
    if current:
        problems.append(current)

    grand_total = 0

    for problem in problems:
        # Rebuild rows inside this problem block
        rows = [''.join(col[r] for col in problem) for r in range(len(lines))]

        # Last row is operator
        op = rows[-1].strip()

        # All above rows are numbers (if present)
        nums = [int(r.strip()) for r in rows[:-1] if r.strip()]

        # Execute the operation
        if op == '+':
            result = sum(nums)
        elif op == '*':
            result = 1
            for n in nums:
                result *= n
        else:
            raise ValueError(f"Unexpected operator found: {op}")

        grand_total += result

    return grand_total


def solve_worksheet_partb(lines: List[str]) -> int:
    """Part B: Process columns right-to-left, extracting digits from each column."""
    # Normalize row length
    width = max(len(line) for line in lines) if lines else 0
    grid = [line.ljust(width) for line in lines]

    # Transpose into columns
    columns = [''.join(grid[r][c] for r in range(len(grid))) for c in range(width)]

    # Split columns into problem blocks
    problems = []
    current = []

    for col in columns:
        if col.strip():
            current.append(col)
        else:
            if current:
                problems.append(current)
                current = []
    if current:
        problems.append(current)

    grand_total = 0

    for block in problems:
        # Last row is the operator
        op_row_index = len(lines) - 1
        operator = block[0][op_row_index]  # operator is same in all columns

        # Extract numbers column-by-column
        numbers = []

        # For each column, read digits top→bottom except last row
        # Then reverse the order: right→left processing
        for col in reversed(block):  # rightmost column first
            digits = col[:op_row_index]  # exclude operator row
            digits = ''.join(d for d in digits if d.isdigit())

            if digits:  # skip empty columns
                numbers.append(int(digits))

        # Compute result
        if operator == '+':
            result = sum(numbers)
        elif operator == '*':
            result = 1
            for n in numbers:
                result *= n
        else:
            raise ValueError(f"Unexpected operator: {operator}")

        grand_total += result

    return grand_total


def parta(lines: List[str]) -> int:
    """Part A: left-to-right processing."""
    return solve_worksheet_parta(lines)


def partb(lines: List[str]) -> int:
    """Part B: right-to-left processing."""
    return solve_worksheet_partb(lines)


def main():
    parser = argparse.ArgumentParser(description="Run part A and part B for day 6")
    parser.add_argument("input", nargs="?", default="aoc6i.txt", help="input file path")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    a = parta(lines)
    b = partb(lines)

    print("Part A (left-to-right):", a)
    print("Part B (right-to-left):", b)


if __name__ == "__main__":
    main()
