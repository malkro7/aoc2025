from typing import List, Tuple
from bisect import bisect_left

Coord = Tuple[int, int]


# ------------------------------------------------------------
# STEP-1: Read input red tiles
# ------------------------------------------------------------
def read_input(filename: str) -> List[Coord]:
    coords = []
    with open(filename) as f:
        for line in f:
            line=line.strip()
            if line:
                x,y=line.split(",")
                coords.append((int(x),int(y)))
    return coords


# ------------------------------------------------------------
# STEP-2: Build border intersections per row
# Each row will have sorted X positions where polygon border passes
# ------------------------------------------------------------
def build_border_rows(red_tiles: List[Coord]):
    border_rows = {}
    n = len(red_tiles)

    for i in range(n):
        x1,y1 = red_tiles[i]
        x2,y2 = red_tiles[(i+1)%n]   # wrap

        if y1 == y2:
            # horizontal edge
            row = y1
            a,b = sorted((x1,x2))
            for x in range(a,b+1):
                border_rows.setdefault(row, []).append(x)

        elif x1 == x2:
            # vertical edge
            col = x1
            a,b = sorted((y1,y2))
            for y in range(a,b+1):
                border_rows.setdefault(y, []).append(col)

        else:
            raise ValueError("Red tile sequence must be axis aligned")

    # dedupe and sort
    for y in border_rows:
        border_rows[y] = sorted(set(border_rows[y]))

    return border_rows


# ------------------------------------------------------------
# STEP-3: Check if an entire X-range on given row is inside polygon
# Rule: interior OR boundary segments are valid
# The valid spans are between pairs (xs[0]..xs[1]), (xs[2]..xs[3]), etc.
# ------------------------------------------------------------
def row_is_inside_range(left: int, right: int, boundary_xs: List[int]) -> bool:
    xs = boundary_xs

    # Check each interior pair:
    # e.g. xs = [2,9,14,20]
    # inside bands = [2..9], [14..20]
    for i in range(0, len(xs)-1, 2):
        L = xs[i]
        R = xs[i+1]
        # rectangle may touch border (inclusive)
        if left >= L and right <= R:
            return True

    return False


# ------------------------------------------------------------
# STEP-4: Validate rectangle defined by two red corners
# Every row must be valid inside-or-boundary region
# ------------------------------------------------------------
def rectangle_valid(x1,y1,x2,y2, border_rows) -> bool:
    left, right = sorted((x1,x2))
    top, bottom = sorted((y1,y2))

    for y in range(top, bottom+1):
        if y not in border_rows:
            return False

        if not row_is_inside_range(left, right, border_rows[y]):
            return False

    return True


# ------------------------------------------------------------
# STEP-5: Main solver – only checks red-red diagonal pairs
# ------------------------------------------------------------
def largest_rectangle_area_part2(red_tiles: List[Coord]) -> int:
    border_rows = build_border_rows(red_tiles)
    best = 0
    n = len(red_tiles)

    for i in range(n):
        x1,y1 = red_tiles[i]
        for j in range(i+1, n):
            x2,y2 = red_tiles[j]

            # Must form diagonal
            if x1 == x2 or y1 == y2:
                continue

            if rectangle_valid(x1,y1,x2,y2, border_rows):
                area = (abs(x2-x1) + 1) * (abs(y2-y1) + 1)
                if area > best:
                    best = area

    return best


# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------
if __name__ == "__main__":
    red = read_input("aoc9t.txt")
    ans = largest_rectangle_area_part2(red)
    print("\nLargest rectangle area using only red/green tiles (Part 2):", ans)
