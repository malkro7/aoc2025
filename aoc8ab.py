#!/usr/bin/env python3

from itertools import combinations
from collections import deque
import sys


def squared_distance(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2


def solve(input_lines, k_pairs=1000):
    boxes = [tuple(map(int, line.split(","))) for line in input_lines]

    # STEP 1: Build all edges with squared distances
    edges = []
    for i, j in combinations(range(len(boxes)), 2):
        d2 = squared_distance(boxes[i], boxes[j])
        edges.append((d2, i, j))

    edges.sort()  # sort by shortest distance first

    # ----------------------------------------------------------------------
    # PART 1: Use exactly first k_pairs edges to form adjacency (even no-op)
    # ----------------------------------------------------------------------
    adj = [[] for _ in boxes]
    for idx in range(k_pairs):
        _, i, j = edges[idx]
        adj[i].append(j)
        adj[j].append(i)

    # Extract circuits using BFS
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

    part1 = len(comps[0]) * len(comps[1]) * len(comps[2])

    # ----------------------------------------------------------------------
    # PART 2: Use Union-Find until all collapse into a single circuit
    # ----------------------------------------------------------------------
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

    return part1, part2


def main():
    if len(sys.argv) < 2:
        print("Usage: python day8.py <inputfile>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    part1, part2 = solve(lines, k_pairs=1000)

    print("\n===== RESULT =====")
    print(f"Part 1 : {part1}")
    print(f"Part 2 : {part2}")
    print("==================\n")


if __name__ == "__main__":
    main()
