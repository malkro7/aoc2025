def count_neighbors(grid, r, c):
    dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] == '@':
                count += 1
    return count


def simulate_removal(grid):
    rows, cols = len(grid), len(grid[0])
    total_removed = 0
    
    while True:
        to_remove = []

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


def main():
    with open("day4input.txt") as f:
        grid = [list(line.strip()) for line in f]

    removed = simulate_removal(grid)
    print("Total rolls removed:", removed)


if __name__ == "__main__":
    main()
