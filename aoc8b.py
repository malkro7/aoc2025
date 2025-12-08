#!/usr/bin/env python3

from itertools import combinations
import sys


def squared_distance(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2


def solve_part_b(input_lines):
    """Part B: Use Union-Find to merge boxes by shortest distances until all
    collapse into a single connected component. Return the product of the
    coordinates of the last two merged boxes."""
    boxes = [tuple(map(int, line.split(","))) for line in input_lines]

    # Build all edges with squared distances
    edges = []
    for i, j in combinations(range(len(boxes)), 2):
        d2 = squared_distance(boxes[i], boxes[j])
        edges.append((d2, i, j))

    edges.sort()  # sort by shortest distance first

    # Union-Find to merge until single component
    parent = list(range(len(boxes)))
    size = [1]*len(boxes)
    remaining_components = len(boxes)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        nonlocal remaining_components
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        remaining_components -= 1
        return True

    part2 = None
    for d2, i, j in edges:
        merged = union(i, j)
        if merged and remaining_components == 1:
            part2 = boxes[i][0] * boxes[j][0]
            break

    return part2


def main():
    if len(sys.argv) < 2:
        print("Usage: python aoc8b.py <inputfile>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    result = solve_part_b(lines)

    print("\n===== PART B RESULT =====")
    print(f"Part B : {result}")
    print("=========================\n")


if __name__ == "__main__":
    main()
