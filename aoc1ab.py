with open("aoc1i.txt") as f:
    input = f.read().splitlines()
pos = 50
max_pos = 99
ans_p1 = 0
ans_p2 = 0
steps_to_zero = 50
for line in input:
    direction = line[0]
    abs_steps = int(line[1:])
    if direction == "L":
        steps = -abs_steps
        steps_to_zero = pos
    else:
        steps = abs_steps
        if pos == 0:
            steps_to_zero = 0
        else:
            steps_to_zero = max_pos + 1 - pos
    tmp = pos + steps
    if abs_steps >= steps_to_zero:
        # Prevent double counting when pointer is already at 0
        if pos != 0:
            ans_p2 += 1
        ans_p2 += (abs_steps - steps_to_zero) // (max_pos + 1)
    pos = tmp % (max_pos + 1)
    if pos == 0:
        ans_p1 += 1
print(ans_p1)
print(ans_p2)
