
col_size = 16
starting_id = 511

stack = []
seen = set()
highest = 0

def get_nexts():
    left = stack[-1]
    left = left >> 1
    left = left & (511 - 4 - 32 - 256)
    if len(stack) < col_size:
        return [left | 32 | 256, left | 4 | 256, left | 4 | 32, left | 4, left | 32, left | 256, left | 4 | 32 | 256, left]
    up = stack[-col_size]
    up = up >> 3
    if len(stack) % col_size == 0:
        return [up | 128 | 256, up | 64 | 256, up | 64 | 128, up | 64, up | 128, up | 256, up | 64 | 128 | 256, up]
    return [left | up, left | up | 256]

def dfs(id):
    global highest

    stack.append(id)
    seen.add(id)
    if len(stack) == 512:
        print(stack)

    if len(stack) > highest:
        highest = len(stack)
        print(highest, stack)

    for next in get_nexts():
        if not next in seen:
            dfs(next)

    stack.pop()
    seen.remove(id)

dfs(starting_id)

# 0 1 0 0 0 0 1 0 0 0 0 1 1 0 1 0 0 0 1 0 
# 1 1 1 0 0 0 0 0 0 1 0 0 0 0 0 1 0 1 0 0
# 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 1 0

