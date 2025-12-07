with open('aoc7i.txt', 'r') as f:
    grid = [line.rstrip('\n') for line in f]

# grid now contains each line as a string
# Example check
print(len(grid), "rows loaded")
print("First row:", grid[0])

# Convert to list of lists
grid = [list(line) for line in grid]

rows = len(grid)
cols = len(grid[0])

# Find start
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 'S':
            start_r, start_c = r, c
            break

# DP table for timelines
dp = [[0] * cols for _ in range(rows)]
dp[start_r][start_c] = 1

for r in range(start_r, rows - 1):
    for c in range(cols):
        if dp[r][c] == 0:
            continue
        cell = grid[r][c]
        # go straight down if possible
        if cell in '|S.':
            dp[r + 1][c] += dp[r][c]
        # branch left/right at '^'
        if cell == '^':
            if c > 0:
                dp[r + 1][c - 1] += dp[r][c]
            if c < cols - 1:
                dp[r + 1][c + 1] += dp[r][c]

# Total timelines are all counts in the last row
total_timelines = sum(dp[rows - 1])
print(total_timelines)
