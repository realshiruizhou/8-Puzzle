from collections import deque
import time


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
    children = set()
    if (x + 1) < size:
        move.append(get_index(x + 1, y))
    if (x - 1) >= 0:
        move.append(get_index(x - 1, y))
    if (y + 1) < size:
        move.append(get_index(x, y + 1))
    if (y - 1) >= 0:
        move.append(get_index(x, y - 1))
    for a in range(0, len(move)):
        children.add(swap(state, state.index("0"), move[a]))
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
    n = list(s)
    temp = n[a]
    n[a] = n[b]
    n[b] = temp
    return ''.join(n)


def path(state):
    start = Node(state, 0)
    end = Node(goal, 0)
    fringe = deque()
    fringe2 = deque()
    fringe2.appendleft(end)
    fringe.appendleft(start)
    visited = set()
    visited2 = set()
    visited2.add(goal)
    visited.add(state)
    while len(fringe) != 0:
        v = fringe.pop()
        v2 = fringe2.pop()
        c = get_children(v.get_state())
        c2 = get_children(v2.get_state())
        if v.get_state() == v2.get_state():
            return v.get_path_length() * 2
        for r in c2:
            if r in visited:
                return (v.get_path_length() + 1) * 2 - 1
        for a in c:
            if a not in visited:
                fringe.appendleft(Node(a, v.get_path_length() + 1))
                visited.add(a)
        for b in c2:
            if b not in visited2:
                fringe2.appendleft(Node(b, v2.get_path_length() + 1))
                visited2.add(b)

goal = "0ABCDEFGHIJKLMNO"
size = 4
file = open("ext.txt", "r")
for line in file:
    a = line.split()
    start2 = time.process_time()
    p = path(a[0])
    end2 = time.process_time()
    time2 = end2 - start2
    print(str(p) + " It took %f seconds to solve" % time2)
