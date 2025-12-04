def max_k_subsequence(s: str, k: int) -> str:
    """Return lexicographically largest subsequence of length k."""
    stack = []
    to_remove = len(s) - k  # how many digits we are allowed to drop

    for digit in s:
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    # If removals left, cut from end
    return "".join(stack[:k])


def main():
    total = 0
    K = 12  # required subsequence length

    with open("day3input.txt") as f:
        for line in f:
            seq = line.strip()
            if not seq:
                continue
            best = int(max_k_subsequence(seq, K))
            total += best
            print(seq, "→", best)

    print("\nTotal Joltage:", total)


if __name__ == "__main__":
    main()
