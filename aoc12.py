import sys
from functools import lru_cache

# ---------------------------------------------------------
# Parsing utilities
# ---------------------------------------------------------

def parse_shape_block(lines, idx):
    """Robust shape parser supporting arbitrary shape heights."""
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines):
        raise ValueError("Expected shape header but reached EOF.")

    header = lines[idx].strip()
    if not header.endswith(":"):
        raise ValueError(f"Malformed shape header: '{header}'")
    sid = int(header[:-1])
    idx += 1

    rows = []
    while idx < len(lines):
        line = lines[idx].rstrip("\n")

        # Stop if blank or next header
        if not line.strip():
            break
        if line.strip().endswith(":") and line.strip()[:-1].isdigit():
            break

        rows.append(line)
        idx += 1

    return sid, rows, idx


def parse_regions(lines, idx):
    """Read region lines: WxH: c0 c1 c2 c3 c4 c5"""
    regions = []

    while idx < len(lines):
        line = lines[idx].strip()
        idx += 1

        if not line:
            continue
        if ":" not in line:
            continue

        left, right = line.split(":")

        dims = left.strip()
        if "x" not in dims:
            continue

        try:
            W, H = map(int, dims.split("x"))
        except:
            continue

        counts = list(map(int, right.split()))
        if len(counts) != 6:
            continue

        need = {i: counts[i] for i in range(6)}
        regions.append((W, H, need))

    return regions


# ---------------------------------------------------------
# Shape normalization and transformations
# ---------------------------------------------------------

def normalize(shape):
    """Trim empty borders from a shape."""
    rows = shape
    # remove empty top
    while rows and all(c == "." for c in rows[0]):
        rows = rows[1:]
    # remove empty bottom
    while rows and all(c == "." for c in rows[-1]):
        rows = rows[:-1]

    if not rows:
        return [""]

    # remove empty left/right columns
    cols = list(zip(*rows))
    while cols and all(c == "." for c in cols[0]):
        cols = cols[1:]
    while cols and all(c == "." for c in cols[-1]):
        cols = cols[:-1]
    rows = ["".join(col) for col in zip(*cols)]
    return rows


def rotate(shape):
    """Rotate 90° clockwise."""
    return ["".join(row[i] for row in shape[::-1]) for i in range(len(shape[0]))]


def flip(shape):
    """Flip horizontally."""
    return [row[::-1] for row in shape]


def generate_variants(shape):
    """All unique rotations + flips."""
    variants = set()
    cur = normalize(shape)
    for _ in range(4):
        variants.add(tuple(cur))
        variants.add(tuple(flip(cur)))
        cur = rotate(cur)
    return [list(v) for v in variants]


# ---------------------------------------------------------
# Region solver
# ---------------------------------------------------------

class RegionSolver:
    def __init__(self, W, H, shapes, need):
        self.W = W
        self.H = H
        self.board = [[None]*W for _ in range(H)]
        self.need = dict(need)
        self.shape_variants = shapes
        self.remaining_ids = [i for i in range(6) for _ in range(self.need[i])]

    def fits(self, variant, x, y):
        for dy, row in enumerate(variant):
            for dx, ch in enumerate(row):
                if ch == "#":
                    if y+dy >= self.H or x+dx >= self.W:
                        return False
                    if self.board[y+dy][x+dx] is not None:
                        return False
        return True

    def place(self, variant, shape_id, x, y):
        for dy, row in enumerate(variant):
            for dx, ch in enumerate(row):
                if ch == "#":
                    self.board[y+dy][x+dx] = shape_id

    def remove(self, variant, x, y):
        for dy, row in enumerate(variant):
            for dx, ch in enumerate(row):
                if ch == "#":
                    self.board[y+dy][x+dx] = None

    def find_first_empty(self):
        for y in range(self.H):
            for x in range(self.W):
                if self.board[y][x] is None:
                    return x, y
        return None

    def backtrack(self):
        pos = self.find_first_empty()
        if pos is None:
            return True
        x, y = pos

        for sid in sorted(set(self.remaining_ids)):
            if self.remaining_ids.count(sid) == 0:
                continue

            for variant in self.shape_variants[sid]:
                if self.fits(variant, x, y):
                    self.place(variant, sid, x, y)
                    self.remaining_ids.remove(sid)

                    if self.backtrack():
                        return True

                    self.remaining_ids.append(sid)
                    self.remove(variant, x, y)

        return False


# ---------------------------------------------------------
# Main entry
# ---------------------------------------------------------

def main():
    fname = "aoc12i.txt"
    lines = [line.rstrip("\n") for line in open(fname)]

    idx = 0
    shapes = {}

    # Parse shapes 0..5
    for _ in range(6):
        sid, rows, idx = parse_shape_block(lines, idx)
        shapes[sid] = generate_variants(rows)

    # Parse remaining as regions
    regions = parse_regions(lines, idx)

    print(f"Loaded {len(shapes)} shapes and {len(regions)} regions.")

    can_fit = 0
    for (W, H, need) in regions:
        solver = RegionSolver(W, H, shapes, need)
        if solver.backtrack():
            can_fit += 1

    print("Part 1:", can_fit)


if __name__ == "__main__":
    main()
