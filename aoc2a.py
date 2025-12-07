#!/usr/bin/env python3
import sys

def is_exact_two_block_repeat(s: str) -> bool:
    """
    Return True if s is exactly two identical halves.
    Examples:
      "11"     -> True
      "1212"   -> True
      "123123" -> True (only if split exactly in middle -> here length 6 -> halves "123" and "123")
      "999"    -> False (odd length -> can't be two equal halves)
      "565656" -> False (three repeats of "56")
      "5555"   -> False (four repeats of "5")
    """
    if not s:
        return False
    if len(s) % 2 != 0:
        return False
    half = len(s) // 2
    return s[:half] == s[half:]


def expand_item(item: str):
    """Yield integers for a single item which may be a number or a range 'start-end'."""
    item = item.strip()
    if not item:
        return
    if "-" in item:
        try:
            start_str, end_str = item.split("-", 1)
            start, end = int(start_str), int(end_str)
            if start <= end:
                for v in range(start, end + 1):
                    yield v
            else:
                # If reversed range, treat as empty or you can swap; here we swap for robustness
                for v in range(end, start + 1):
                    yield v
        except ValueError:
            # ignore malformed ranges
            return
    else:
        try:
            yield int(item)
        except ValueError:
            return


def process_file(path: str):
    invalids = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # split by commas, allow items separated by whitespace too
            parts = [p.strip() for p in line.strip().split(",") if p.strip()]
            for p in parts:
                for num in expand_item(p):
                    s = str(num)
                    if is_exact_two_block_repeat(s):
                        invalids.append(num)

    # Output
    print("=== Invalid Numbers ===")
    if invalids:
        for n in invalids:
            print(n)
    else:
        print("(none)")

    print("\nTotal Invalid Count:", len(invalids))
    print("Sum of Invalid Numbers:", sum(invalids) if invalids else 0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_two_block.py input.txt")
        sys.exit(1)
    process_file(sys.argv[1])
