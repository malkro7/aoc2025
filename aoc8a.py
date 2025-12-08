#!/usr/bin/env python3

from itertools import combinations
from collections import deque
import sys


def squared_distance(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2


def solve_part_a(input_lines, k_pairs=1000):
    """Part A: Use exactly the first k_pairs edges to form adjacency, then find
    the product of the three largest connected components."""
    boxes = [tuple(map(int, line.split(","))) for line in input_lines]

    # Build all edges with squared distances
    edges = []
    for i, j in combinations(range(len(boxes)), 2):
        d2 = squared_distance(boxes[i], boxes[j])
        edges.append((d2, i, j))

    edges.sort()  # sort by shortest distance first

    # Use exactly first k_pairs edges to form adjacency
    adj = [[] for _ in boxes]
    for idx in range(k_pairs):
        _, i, j = edges[idx]
        adj[i].append(j)
        adj[j].append(i)

    # Extract connected components using BFS
    visited = set()
    comps = []

    for i in range(len(boxes)):
        if i in visited:
            continue
        q = deque([i])
        visited.add(i)
        comp = []
        while q:
            cur = q.popleft()
            comp.append(cur)
            for nxt in adj[cur]:
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        comps.append(comp)

    comps.sort(key=len, reverse=True)

    # Product of the three largest components
    part1 = len(comps[0]) * len(comps[1]) * len(comps[2])

    return part1


def main():
    if len(sys.argv) < 2:
        print("Usage: python aoc8a.py <inputfile>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    result = solve_part_a(lines, k_pairs=1000)

    print("\n===== PART A RESULT =====")
    print(f"Part A : {result}")
    print("=========================\n")


if __name__ == "__main__":
    main()
