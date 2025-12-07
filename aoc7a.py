from collections import deque

def load_grid_from_file(filename):
    with open(filename, "r") as f:
        grid = [line.rstrip("\n") for line in f]
    return grid

def count_splits(grid):
    H = len(grid)
    W = max(len(row) for row in grid)
    grid = [row.ljust(W, ".") for row in grid]  # normalize width

    # Locate S
    start = None
    for r in range(H):
        for c in range(W):
            if grid[r][c] == "S":
                start = (r, c)
                break
        if start:
            break

    if not start:
        raise ValueError("No starting point 'S' found in file.")

    # BFS over beams
    q = deque()
    q.append((start[0], start[1], "down"))
    seen = set()
    splits = 0

    while q:
        r, c, d = q.popleft()
        if (r, c, d) in seen:
            continue
        seen.add((r, c, d))

        if d == "down":
            nr = r + 1
            if nr >= H:
                continue
            cell = grid[nr][c]

            if cell == "^":
                # A splitter
                splits += 1

                # Emit beams left and right
                if c - 1 >= 0:
                    q.append((nr, c - 1, "left"))
                if c + 1 < W:
                    q.append((nr, c + 1, "right"))
            else:
                # Continue falling
                q.append((nr, c, "down"))

        elif d == "left":
            nc = c - 1
            if nc < 0:
                continue

            # May drop only if below is EMPTY '.'
            if r + 1 < H and grid[r + 1][c] == ".":
                q.append((r + 1, c, "down"))
            else:
                q.append((r, nc, "left"))

        elif d == "right":
            nc = c + 1
            if nc >= W:
                continue

            # Drop only on empty cell below
            if r + 1 < H and grid[r + 1][c] == ".":
                q.append((r + 1, c, "down"))
            else:
                q.append((r, nc, "right"))

    return splits


if __name__ == "__main__":
    grid = load_grid_from_file("aoc7i.txt")   # <= your puzzle file
    result = count_splits(grid)
    print(result)
