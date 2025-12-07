def solve_worksheet(lines):
    # Normalize row length
    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]

    # Transpose: column-wise extraction
    columns = [''.join(grid[r][c] for r in range(len(grid))) for c in range(width)]

    # Segment columns into problems
    problems = []
    current = []

    for col in columns:
        if col.strip():
            current.append(col)
        else:
            if current:
                problems.append(current)
                current = []
    if current:
        problems.append(current)

    grand_total = 0

    for problem in problems:
        # Rebuild rows inside this problem block
        rows = [''.join(col[r] for col in problem) for r in range(len(lines))]

        # Last row is operator
        op = rows[-1].strip()

        # All above rows are numbers (if present)
        nums = [int(r.strip()) for r in rows[:-1] if r.strip()]

        # Execute the operation
        if op == '+':
            result = sum(nums)
        elif op == '*':
            result = 1
            for n in nums:
                result *= n
        else:
            raise ValueError(f"Unexpected operator found: {op}")

        grand_total += result

    return grand_total


if __name__ == "__main__":
    # Read file
    with open("aoc6i.txt", "r") as f:
        lines = [line.rstrip("\n") for line in f]

    # Compute and print result
    answer = solve_worksheet(lines)
    print(answer)
