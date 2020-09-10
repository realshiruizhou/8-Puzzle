from collections import deque
import random
goal = "012345678"
size = 3


class Node:
    def __init__(self, state, path_length):
        self.path_length = path_length
        self.state = state

    def get_path_length(self):
        return self.path_length

    def get_state(self):
        return self.state


def get_children(state):
    (x, y) = get_coordinate(state)
    move = []
    children = []
    if (x + 1) < size:
        move.append(get_index(x + 1, y))
    if (x - 1) >= 0:
        move.append(get_index(x - 1, y))
    if (y + 1) < size:
        move.append(get_index(x, y + 1))
    if (y - 1) >= 0:
        move.append(get_index(x, y - 1))
    for a in range(0, len(move)):
        children.append(swap(state, state.index("0"), move[a]))
    return children


def get_coordinate(state):
    index = state.index("0")
    x = index // size
    y = index % size
    return x, y


def get_index(x, y):
    index = 0
    index += size * x
    index += y
    return index


def swap(s, a, b):
    # swaps s[a] and s[b]
    n = list(s)
    temp = n[a]
    n[a] = n[b]
    n[b] = temp
    return ''.join(n)


def moves(moves_away):
    start = Node(goal, 0)
    fringe = deque()
    fringe.appendleft(start)
    visited = set()
    visited.add(start.get_state())
    count = set()
    while len(fringe) != 0:
        v = fringe.pop()
        if v.get_path_length() == moves_away:
            count.add(v.get_state())
        c = get_children(v.get_state())
        temp = []
        for e in c:
            add = Node(e, v.get_path_length() + 1)
            temp.append(add)
        for a in range(0, len(c)):
            if temp[a].get_state() not in visited:
                fringe.appendleft(temp[a])
                visited.add(temp[a].get_state())
    return count


for a in range(0, 32):
    print(random.sample(moves(a), 1)[0])
