def solve_worksheet(lines):
    # Normalize row length
    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]

    # Transpose into columns
    columns = [''.join(grid[r][c] for r in range(len(grid))) for c in range(width)]

    # Split columns into problem blocks
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

    for block in problems:
        # Last row is the operator
        op_row_index = len(lines) - 1
        operator = block[0][op_row_index]  # operator is same in all columns

        # Extract numbers column-by-column
        numbers = []

        # For each column, read digits top→bottom except last row
        # Then reverse the order: right→left processing
        for col in reversed(block):  # rightmost column first
            digits = col[:op_row_index]  # exclude operator row
            digits = ''.join(d for d in digits if d.isdigit())

            if digits:  # skip empty columns
                numbers.append(int(digits))

        # Compute result
        if operator == '+':
            result = sum(numbers)
        elif operator == '*':
            result = 1
            for n in numbers:
                result *= n
        else:
            raise ValueError(f"Unexpected operator: {operator}")

        grand_total += result

    return grand_total


if __name__ == "__main__":
    with open("day6test.txt", "r") as f:
        lines = [line.rstrip("\n") for line in f]

    print(solve_worksheet(lines))
