def count_fresh_ids_from_file(filename: str) -> int:
    with open(filename, "r") as f:
        content = f.read()

    # Split input into the two logical sections
    sections = content.strip().split("\n\n")
    range_lines = sections[0].splitlines()
    id_lines = sections[1].splitlines()

    # Parse ranges
    ranges = []
    for line in range_lines:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    # Parse available IDs
    ids = [int(x) for x in id_lines]

    # Membership check
    def is_fresh(id_val):
        for start, end in ranges:
            if start <= id_val <= end:
                return True
        return False

    # Aggregate fresh IDs
    return sum(1 for id_val in ids if is_fresh(id_val))


# Example usage:
print(count_fresh_ids_from_file("aoc5i.txt"))
