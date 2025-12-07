"""Day 4 merged runner.

Provides `parta(lines)` which counts accessible rolls and
`partb(lines)` which simulates removals and returns total removed.
`main()` reads the input file once and prints both results.
"""
from typing import Iterable, List
import argparse
import copy


def count_accessible_rolls(grid: List[str]) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    accessible = 0

    # 8 neighbor directions
    dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue

            neighbor_count = 0

            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == '@':
                        neighbor_count += 1

            if neighbor_count < 4:
                accessible += 1

    return accessible


def count_neighbors(grid: List[List[str]], r: int, c: int) -> int:
    dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]
    rows, cols = len(grid), len(grid[0]) if grid else 0
    count = 0
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] == '@':
                count += 1
    return count


def simulate_removal(grid: List[List[str]]) -> int:
    rows, cols = len(grid), len(grid[0]) if grid else 0
    total_removed = 0

    while True:
        to_remove: List[tuple[int, int]] = []

        # Identify removable rolls
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    if count_neighbors(grid, r, c) < 4:
                        to_remove.append((r, c))

        # If nothing to remove, we're done
        if not to_remove:
            break

        # Remove simultaneously
        for r, c in to_remove:
            grid[r][c] = '.'

        total_removed += len(to_remove)

    return total_removed


def parta(lines: Iterable[str]) -> int:
    """Return the count of accessible rolls from the input lines."""
    grid = [line.rstrip("\n") for line in lines if line.strip() != ""]
    return count_accessible_rolls(grid)


def partb(lines: Iterable[str]) -> int:
    """Simulate removals and return total removed."""
    raw = [line.rstrip("\n") for line in lines if line.strip() != ""]
    grid = [list(row) for row in raw]
    # operate on a copy to avoid mutating input
    grid_copy = copy.deepcopy(grid)
    return simulate_removal(grid_copy)


def main():
    parser = argparse.ArgumentParser(description="Run part A and part B for day 4")
    parser.add_argument("input", nargs="?", default="aoc4i.txt", help="input file path")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    a = parta(raw_lines)
    b = partb(raw_lines)

    print("Part A Accessible rolls:", a)
    print("Part B Total rolls removed:", b)


if __name__ == "__main__":
    main()
