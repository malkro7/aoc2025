import re
import math

INF = float('inf')


class Part2Solver:
    """
    Given:
      - target joltage requirements (list[int])
      - button wirings (list[list[int]])

    Determine the minimum number of presses needed
    so that repeated application of the wirings exactly produces the target.
    """

    def __init__(self, targets, wirings):
        self.targets = targets[:]  # target remaining
        self.n = len(targets)
        self.wirings = [w[:] for w in wirings]
        self.num_wirings = len(wirings)

        # cnt_remaining[w][c] tells how many wirings from w onward affect counter c
        self.cnt_remaining = [[0]*self.n for _ in range(self.num_wirings + 1)]

        self.best = INF  # minimal presses found

    # --------------------------------------------
    # STEP 1: reorder wirings to reduce branching
    # --------------------------------------------
    def reorder_wirings(self):
        """
        Reorder wirings based on the heuristic:
        - Identify counters that appear in the fewest wirings
        - Prioritize wirings that satisfy those
        - If multiple wirings affect that counter, choose the wiring
          that affects the most counters overall (largest coverage)
        """
        remaining = self.wirings[:]
        ordered = []

        while remaining:
            # Count # of wirings affecting each counter among remaining
            counts = [0]*self.n
            for wiring in remaining:
                for c in wiring:
                    counts[c] += 1

            # find counter with smallest non-zero count
            rare_count = min(x for x in counts if x > 0)
            rare_id = counts.index(rare_count)

            # find a wiring matching rare_id that affects many counters
            best_choice = None
            for wiring in remaining:
                if rare_id in wiring:
                    if best_choice is None or len(wiring) > len(best_choice):
                        best_choice = wiring

            ordered.append(best_choice)
            remaining.remove(best_choice)

        self.wirings = ordered

    # --------------------------------------------
    # STEP 2: track how many remaining wirings can cover each counter
    # --------------------------------------------
    def compute_remaining_coverage(self):
        """
        cnt_remaining[w][c] means:
        how many of wirings [w..end] affect counter c
        """
        for idx in range(self.num_wirings - 1, -1, -1):
            # propagate from next row
            for c in range(self.n):
                self.cnt_remaining[idx][c] = self.cnt_remaining[idx+1][c]

            # count current wiring
            for c in self.wirings[idx]:
                self.cnt_remaining[idx][c] += 1

    # --------------------------------------------
    # STEP 3: the recursive optimization
    # --------------------------------------------
    def search(self, remaining, wiring_idx, presses_used):
        """
        remaining     = list[int] remaining joltage to satisfy
        wiring_idx    = index of current wiring to evaluate
        presses_used  = total presses so far
        """

        # prune based on known best
        if presses_used >= self.best:
            return

        # lower bound pruning:
        # since pressing reduces at most 1 unit total on any path
        # max target_remaining ensures a lower bound on future presses
        if presses_used + max(remaining) >= self.best:
            return

        # if no more wirings, check completion
        if wiring_idx == self.num_wirings:
            if all(x == 0 for x in remaining):
                self.best = presses_used
            return

        wiring = self.wirings[wiring_idx]

        # determine allowable range: minimum and maximum presses
        mn_presses = 0
        mx_presses = INF

        for c in wiring:
            # pressing too many times overshoots
            mx_presses = min(mx_presses, remaining[c])

            # if this is last wiring affecting index c,
            # then this wiring MUST satisfy all of that index
            if self.cnt_remaining[wiring_idx][c] == 1:
                mn_presses = max(mn_presses, remaining[c])

        # if infeasible, abort
        if mn_presses > mx_presses:
            return

        # try pressing from mn..mx
        for count in range(mn_presses, mx_presses + 1):
            new_remaining = remaining[:]
            for c in wiring:
                new_remaining[c] -= count
            self.search(new_remaining, wiring_idx + 1, presses_used + count)

    # --------------------------------------------
    # PUBLIC SOLVE METHOD
    # --------------------------------------------
    def solve(self):
        self.reorder_wirings()
        self.compute_remaining_coverage()
        self.best = INF
        self.search(self.targets[:], 0, 0)
        return self.best


def solve_file(filename):
    total = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # extract targets
            joltage_str = re.search(r"\{([^}]*)\}", line).group(1)
            targets = list(map(int, joltage_str.split(",")))

            # extract wirings
            wiring_strs = re.findall(r"\(([^)]*)\)", line)
            wirings = [list(map(int, w.split(","))) for w in wiring_strs if w]

            solver = Part2Solver(targets, wirings)
            total += solver.solve()

    return total


if __name__ == "__main__":
    result = solve_file("aoc10i.txt")
    print("Part 2:", result)
