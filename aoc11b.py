#!/usr/bin/env python3
"""
part2_fixed.py

- Loads directed graph from input.txt (format: "node: out1 out2 ...")
- Counts all simple paths from START -> END that visit ALL REQUIRED_NODES (in any order).
- Optimized path-counting:
    * If the graph is a DAG -> use DP memoization on (node, visited_required_mask) (very fast).
    * If the graph has cycles -> fall back to safe DFS with visited-set (correct, may be expensive).
- Supports optional printing of qualified paths up to a user-configurable limit to avoid huge output.
"""
from collections import defaultdict, deque
from functools import lru_cache
import argparse
import sys

# ------------------ Configuration defaults ------------------
DEFAULT_INPUT = "aoc11i.txt"
DEFAULT_START = "svr"
DEFAULT_END = "out"
DEFAULT_REQUIRED = ["dac", "fft"]
DEFAULT_PRINT_PATHS = True
DEFAULT_PATH_PRINT_LIMIT = 1000  # cap to avoid huge outputs

# ------------------ Graph loader ------------------
def load_graph(path):
    graph = defaultdict(list)
    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line or ":" not in line:
                continue
            src, targets = line.split(":", 1)
            src = src.strip()
            for t in targets.strip().split():
                if t:
                    graph[src].append(t.strip())
    return graph

# ------------------ Cycle detection (directed) ------------------
def has_cycle(graph):
    """Return True if directed graph has a cycle (using colors DFS)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}
    for node in graph:
        color.setdefault(node, WHITE)
        for v in graph[node]:
            color.setdefault(v, WHITE)

    def dfs(u):
        color[u] = GRAY
        for v in graph.get(u, ()):
            if color[v] == GRAY:
                return True
            if color[v] == WHITE:
                if dfs(v):
                    return True
        color[u] = BLACK
        return False

    for n in list(color.keys()):
        if color[n] == WHITE:
            if dfs(n):
                return True
    return False

# ------------------ DAG-optimized DP (safe, fast) ------------------
def count_paths_dag(graph, start, end, required):
    """Count number of paths from start->end that visit all required nodes.
       Safe & fast for DAGs; memoizes on (node, mask)."""
    req_list = sorted(required)
    idx = {name: i for i, name in enumerate(req_list)}
    full_mask = (1 << len(req_list)) - 1

    @lru_cache(maxsize=None)
    def dp(node, mask):
        if node == end:
            return 1 if mask == full_mask else 0
        total = 0
        for nxt in graph.get(node, ()):
            next_mask = mask
            if nxt in idx:
                next_mask |= (1 << idx[nxt])
            total += dp(nxt, next_mask)
        return total

    start_mask = 0
    if start in idx:
        start_mask |= (1 << idx[start])
    return dp(start, start_mask)

# ------------------ Safe enumerator for graphs with cycles ------------------
def enumerate_and_count_safe(graph, start, end, required, path_print_limit=DEFAULT_PATH_PRINT_LIMIT, print_paths=True):
    """Enumerate simple paths (no vertex repeated on same path). Return (total_paths, qualified_paths_list).
       For memory/safety we limit the number of printed paths to path_print_limit."""
    total_paths = 0
    qualified_paths = []

    stack = [(start, [start], set([start]), (start in required) and {start} or set())]
    # stack items: (node, path_list, visited_set, required_seen_set)
    while stack:
        node, path, visited, req_seen = stack.pop()
        if node == end:
            total_paths += 1
            if req_seen.issuperset(required):
                if print_paths and len(qualified_paths) < path_print_limit:
                    qualified_paths.append(list(path))
            continue
        for nxt in graph.get(node, ()):
            if nxt in visited:
                continue
            new_visited = set(visited)
            new_visited.add(nxt)
            new_path = path + [nxt]
            new_req_seen = set(req_seen)
            if nxt in required:
                new_req_seen.add(nxt)
            stack.append((nxt, new_path, new_visited, new_req_seen))

    return total_paths, qualified_paths

# ------------------ Driver ------------------
def main():
    parser = argparse.ArgumentParser(description="Count paths from start->end that visit required nodes.")
    parser.add_argument("--input", "-i", default=DEFAULT_INPUT)
    parser.add_argument("--start", "-s", default=DEFAULT_START)
    parser.add_argument("--end", "-e", default=DEFAULT_END)
    parser.add_argument("--required", "-r", nargs="+", default=DEFAULT_REQUIRED)
    parser.add_argument("--no-print-paths", dest="print_paths", action="store_false")
    parser.add_argument("--path-limit", type=int, default=DEFAULT_PATH_PRINT_LIMIT,
                        help="Max number of qualified paths to print (to avoid massive output).")
    args = parser.parse_args()

    graph = load_graph(args.input)
    # Ensure nodes exist in graph keys so cycle detection & DP know about isolated nodes
    for node in list(graph.keys()):
        for v in graph[node]:
            if v not in graph:
                graph.setdefault(v, [])

    print(f"Loaded graph with {len(graph)} nodes (input={args.input})")
    cyc = has_cycle(graph)
    if cyc:
        print("Graph contains cycles. Using safe enumerator (guaranteed-correct but potentially slow).")
        total_paths, qualified_paths = enumerate_and_count_safe(
            graph, args.start, args.end, set(args.required),
            path_print_limit=args.path_limit, print_paths=args.print_paths
        )
        q_count = len(qualified_paths)
        print(f"\nTotal simple paths found from {args.start!r} to {args.end!r}: {total_paths}")
        print(f"Qualified (visit all required {sorted(args.required)}): {q_count}")
        if args.print_paths:
            print("\n--- Qualified paths (capped) ---")
            for p in qualified_paths:
                print(",".join(p))
            if q_count >= args.path_limit:
                print(f"...printed {args.path_limit} paths (limit).")
    else:
        print("Graph is a DAG. Using optimized DP memoization (very fast).")
        q_count = count_paths_dag(graph, args.start, args.end, set(args.required))
        # If you still want the list of paths when DAG, you can enumerate (safe) but may be large.
        print(f"\n(Optimized) Qualified paths count from {args.start!r} to {args.end!r} visiting {sorted(args.required)}: {q_count}")
        if args.print_paths and q_count > 0:
            # Optional: enumerate to print up to the path_limit (DAG => enumeration is safe, but may be many)
            total_paths, qualified_paths = enumerate_and_count_safe(
                graph, args.start, args.end, set(args.required),
                path_print_limit=args.path_limit, print_paths=args.print_paths
            )
            print("\n--- Qualified paths (capped) ---")
            for p in qualified_paths:
                print(",".join(p))
            if len(qualified_paths) >= args.path_limit:
                print(f"...printed {args.path_limit} paths (limit).")

if __name__ == "__main__":
    main()
