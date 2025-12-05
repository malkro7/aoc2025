def count_unique_fresh_ids(filename: str) -> int:
    # Read and parse file
    with open(filename, "r") as f:
        content = f.read().strip()

    # Split into sections (ranges + irrelevant section)
    sections = content.split("\n\n")
    range_lines = sections[0].splitlines()

    # Parse ranges
    intervals = []
    for line in range_lines:
        start, end = map(int, line.split('-'))
        intervals.append((start, end))

    # Sort ranges by start
    intervals.sort()

    # Merge overlapping ranges
    merged = []
    curr_start, curr_end = intervals[0]

    for start, end in intervals[1:]:
        if start <= curr_end + 1:  # overlap or touching
            curr_end = max(curr_end, end)
        else:
            merged.append((curr_start, curr_end))
            curr_start, curr_end = start, end

    merged.append((curr_start, curr_end))

    # Count unique fresh IDs
    total_fresh = sum((end - start + 1) for start, end in merged)

    return total_fresh


# Example:
print(count_unique_fresh_ids("day5input.txt"))
