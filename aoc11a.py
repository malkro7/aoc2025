from collections import defaultdict

def load_graph(path):
    graph = defaultdict(list)
    with open(path) as f:
        for line in f:
            if ":" not in line:
                continue
            src, targets = line.strip().split(":")
            src = src.strip()
            for t in targets.strip().split():
                graph[src].append(t.strip())
    return graph


def find_all_paths(graph, start="you", end="out"):
    stack = [(start, [start])]
    paths = []

    while stack:
        node, path = stack.pop()
        if node == end:
            paths.append(path)
            continue

        for nxt in graph.get(node, []):
            stack.append((nxt, path + [nxt]))

    return paths


if __name__ == "__main__":
    graph = load_graph("aoc11i.txt")
    paths = find_all_paths(graph)

    print("Total paths:", len(paths))
    print("Paths:")
    for p in paths:
        print(" -> ".join(p))
