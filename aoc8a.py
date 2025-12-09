# Advent of Code 2025 - Day 8
# Final version: reads input from a file provided as a command-line argument.

import sys
from typing import List, Tuple


# -----------------------------
# Disjoint Set Union (Union-Find)
# -----------------------------
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, a: int) -> int:
        root = a
        while root != self.parent[root]:
            root = self.parent[root]
        while a != root:
            nxt = self.parent[a]
            self.parent[a] = root
            a = nxt
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


# -----------------------------
# Core Functions
# -----------------------------
def parse_points(lines: List[str]) -> List[Tuple[int, int, int]]:
    pts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        x, y, z = map(int, line.split(","))
        pts.append((x, y, z))
    return pts


def squared_distance(a, b) -> int:
    return ((a[0] - b[0]) ** 2 +
            (a[1] - b[1]) ** 2 +
            (a[2] - b[2]) ** 2)


def solve(lines: List[str], k: int = 1000) -> int:
    pts = parse_points(lines)
    n = len(pts)

    # Build all pair distances
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((squared_distance(pts[i], pts[j]), i, j))

    # Sort by distance (deterministic)
    pairs.sort(key=lambda x: (x[0], x[1], x[2]))

    # Take K closest pairs
    k = min(k, len(pairs))
    selected = pairs[:k]

    # Union the selected pairs
    dsu = DSU(n)
    for _, i, j in selected:
        dsu.union(i, j)

    # Count sizes
    comp = {}
    for i in range(n):
        r = dsu.find(i)
        comp[r] = comp.get(r, 0) + 1

    sizes = sorted(comp.values(), reverse=True)

    # Ensure at least 3 groups
    while len(sizes) < 3:
        sizes.append(1)

    return sizes[0] * sizes[1] * sizes[2]


# -----------------------------
# Main (file input)
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day8.py input.txt")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r") as f:
        lines = f.read().strip().splitlines()

    result = solve(lines, k=1000)
    print(result)
