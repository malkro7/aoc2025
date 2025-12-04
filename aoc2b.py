#!/usr/bin/env python3
import sys

def is_repeated_pattern(s: str) -> bool:
    """
    Returns True if s is composed of a smaller substring repeated
    at least twice. Example:
      '121212'   -> True (12 repeated 3 times)
      '1111111'  -> True (1 repeated 7 times)
      '12341234' -> True (1234 repeated 2 times)
      '999'      -> True (9 repeated 3 times)
      '12345'    -> False
    """
    n = len(s)

    # Try substring lengths from 1 up to half of the length
    for size in range(1, n // 2 + 1):
        if n % size == 0:  # only check sizes that divide the length
            block = s[:size]
            if block * (n // size) == s:
                return True

    return False


def expand_item(item: str):
    """Expand numbers or ranges like '100-105'."""
    item = item.strip()
    if not item:
        return

    if "-" in item:
        try:
            start_str, end_str = item.split("-", 1)
            start, end = int(start_str), int(end_str)
            if start <= end:
                for x in range(start, end + 1):
                    yield x
            else:
                for x in range(end, start + 1):
                    yield x
        except:
            return
    else:
        try:
            yield int(item)
        except:
            return


def process_file(path: str):
    invalids = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.split(",") if p.strip()]
            for p in parts:
                for num in expand_item(p):
                    if is_repeated_pattern(str(num)):
                        invalids.append(num)

    print("\n=== Invalid IDs ===")
    for n in invalids:
        print(n)

    print("\nTotal Invalid Count:", len(invalids))
    print("Sum of Invalid IDs:", sum(invalids) if invalids else 0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_invalid_ids.py input.txt")
        sys.exit(1)
    process_file(sys.argv[1])
