def count_accessible_rolls(grid):
    rows = len(grid)
    cols = len(grid[0])
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


def main():
    with open("aoc4i.txt") as f:
        grid = [line.rstrip("\n") for line in f]

    result = count_accessible_rolls(grid)
    print("Accessible rolls:", result)


if __name__ == "__main__":
    main()
