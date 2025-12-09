def largest_rectangle_area(coords):
    max_area = 0

    for i in range(len(coords)):
        x1, y1 = coords[i]
        for j in range(i + 1, len(coords)):
            x2, y2 = coords[j]

            # Must be opposite corners (both axes differ)
            if x1 != x2 and y1 != y2:
                width = abs(x1 - x2) + 1   # inclusive width
                height = abs(y1 - y2) + 1  # inclusive height
                area = width * height
                max_area = max(max_area, area)

    return max_area


def read_input_file(filename):
    coords = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Expect format "x,y"
            parts = line.split(",")
            x = int(parts[0].strip())
            y = int(parts[1].strip())
            coords.append((x, y))

    return coords


if __name__ == "__main__":
    file_path = "aoc9i.txt"  # update as required
    coords = read_input_file(file_path)
    result = largest_rectangle_area(coords)
    print("Largest rectangle area:", result)
