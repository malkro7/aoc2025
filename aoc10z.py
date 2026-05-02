def min_add_steps(target, increments):
    '''
    BFS search for smaller number of presses for Part 2
    target = final joltage configuration, as numpy array
    increments = collection of button presses, as numpy array
    It takes forever, despite attempt to prune the states...
    '''
    start = np.array([0]*len(target))
    queue = deque([(start, 0)]) # (value, steps)
    visited = {hash(start.tobytes())}

    while queue:
        value, steps = queue.popleft()
        if all(value == target):
            return steps

        for inc in increments:
            new_val = value + inc

            # Prune: skip if any counter exceeds target
            if any(new_val[i] > target[i] for i in range(len(target))):
                continue
            
            new_val_hash = hash(new_val.tobytes())
            if new_val_hash not in visited:
                visited.add(new_val_hash)
                queue.append((new_val, steps + 1))
    
    return None # unreachable
def part2bfs(filename):
    machines = read_input_10(filename)
    presses = 0 
    for i,machine in enumerate(machines):
        #print(f"{i+1} / {len(machines)} ...")
        _, buttons, joltage = machine
        # convert buttons values from Part 1 into presses numpy arrays
        increments = []
        for b in buttons:
            increments.append(np.array([int(n) for n in bin(b)[2:].zfill(len(joltage))])) 
        presses += min_add_steps(joltage, increments)
    return presses