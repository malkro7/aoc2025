#!/usr/bin/env python3
"""Day 9 merged runner.

Part A: Find the largest rectangle using any two coordinates as opposite corners.
Part B: Find the largest rectangle whose every tile is red or green (no interior
        edges of the red polygon pass through the rectangle interior).
"""
import itertools
import sys
from typing import List, Tuple

Coord = Tuple[int, int]


def read_input(filename: str) -> List[Coord]:
    """Read coordinates from file, format 'x,y' per line."""
    points: List[Coord] = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x_str, y_str = line.split(",")
            points.append((int(x_str), int(y_str)))
    return points


def solve_part_a(coords: List[Coord]) -> int:
    """Part A: Find largest rectangle using any two coordinates as opposite corners."""
    max_area = 0

    for i in range(len(coords)):
        x1, y1 = coords[i]
        for j in range(i + 1, len(coords)):
            x2, y2 = coords[j]

            # Must be opposite corners (both axes differ)
            if x1 != x2 and y1 != y2:
                width = abs(x1 - x2) + 1   # inclusive width
                height = abs(y1 - y2) + 1  # inclusive height
                area = width * height
                max_area = max(max_area, area)

    return max_area


def solve_part_b(points: List[Coord]) -> int:
    """Part B: Find largest rectangle whose every tile is red or green.

    The red tiles form a closed loop; consecutive points (and last->first)
    are joined by axis-aligned edges.
    A rectangle is valid if no edge of this loop passes through its interior.
    Touching the border is allowed.
    """

    # Close the loop: edges are between loop[k] and loop[k+1]
    loop = points + [points[0]]

    max_area = 0

    # Try all pairs of red tiles as opposite corners
    for (x1, y1), (x2, y2) in itertools.combinations(points, 2):
        # Compute inclusive bounding box of candidate rectangle
        bx1, bx2 = min(x1, x2), max(x1, x2)
        by1, by2 = min(y1, y2), max(y1, y2)

        # Check all polygon edges for intersection with the rectangle *interior*
        for (lx1, ly1), (lx2, ly2) in itertools.pairwise(loop):
            # Edge is axis-aligned per problem statement.
            #
            # This condition checks if the segment is completely:
            #   - to the left of the rectangle,
            #   - to the right of the rectangle,
            #   - above the rectangle, or
            #   - below the rectangle.
            #
            # If it is NOT completely outside in one of these ways,
            # then it intersects the rectangle.
            #
            # Note the use of <=, which ensures:
            #   - segments that lie exactly on the rectangle border
            #     are considered "outside" for this test, i.e. allowed.
            if not (
                max(lx1, lx2) <= bx1 or  # entirely left
                bx2 <= min(lx1, lx2) or  # entirely right
                max(ly1, ly2) <= by1 or  # entirely above
                by2 <= min(ly1, ly2)     # entirely below
            ):
                # This edge cuts through the rectangle interior -> invalid
                break

        else:
            # No edges cut the interior -> rectangle is fully red/green
            area = (bx2 - bx1 + 1) * (by2 - by1 + 1)
            if area > max_area:
                max_area = area

    return max_area


def main():
    if len(sys.argv) < 2:
        print("Usage: python aoc9ab.py <inputfile>")
        sys.exit(1)

    coords = read_input(sys.argv[1])

    part_a = solve_part_a(coords)
    part_b = solve_part_b(coords)

    print("\n===== DAY 9 RESULTS =====")
    print(f"Part A (largest rectangle - any two coords): {part_a}")
    print(f"Part B (largest rectangle - red/green only): {part_b}")
    print("==========================\n")


if __name__ == "__main__":
    main()
