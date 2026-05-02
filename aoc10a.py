from collections import deque
import re

def parse_machine_line(line):
    # Extract the indicator diagram inside []
    diag = re.search(r'\[([.#]+)\]', line).group(1)

    # Convert diagram to target bitmask
    target = 0
    for i, ch in enumerate(diag):
        if ch == '#':
            target |= (1 << i)

    # Extract button groups inside ()
    buttons = []
    button_groups = re.findall(r'\((.*?)\)', line)
    for bgrp in button_groups:
        if not bgrp.strip():  # handle empty "()"
            continue
        indices = list(map(int, bgrp.split(',')))
        mask = 0
        for idx in indices:
            mask |= (1 << idx)
        buttons.append(mask)

    return target, buttons


def min_presses_to_target(target, buttons):
    """
    Run BFS from state=0 until we reach target.
    Returns minimum number of presses required.
    """
    if target == 0:
        return 0

    max_state = 1 << max((target.bit_length(), *(b.bit_length() for b in buttons)))

    visited = [False] * max_state
    q = deque()
    q.append((0, 0))  # (state, depth)
    visited[0] = True

    while q:
        state, dist = q.popleft()
        for bmask in buttons:
            new_state = state ^ bmask
            if new_state == target:
                return dist + 1
            if new_state < max_state and not visited[new_state]:
                visited[new_state] = True
                q.append((new_state, dist + 1))

    # If unreachable, puzzle guarantees solvable, so should not occur
    return float('inf')


def main():
    total_presses = 0
    with open("aoc10i.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            target, buttons = parse_machine_line(line)
            presses = min_presses_to_target(target, buttons)
            total_presses += presses

    print(total_presses)


if __name__ == "__main__":
    main()
