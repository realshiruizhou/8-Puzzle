import sys
import random
from collections import deque


class Node:
    def __init__(self, state, parent, path_length, dir):
        self.parent = parent
        self.path_length = path_length
        self.state = state
        self.dir = dir

    def get_parent(self):
        return self.parent

    def get_path_length(self):
        return self.path_length

    def get_state(self):
        return self.state

    def get_dir(self):
        return self.dir


def print_puzzle(state):
    count = 1
    for a in state:
        if count % size == 0:
            print(a + " ")
        else:
            print(a + " ", end="", flush=True)
        count += 1


def goal_test(state):
    return goal == state


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


def get_child_dir(state):
    (x, y) = get_coordinate(state)
    move = {}
    children = {}
    if (x + 1) < size:
        move[get_index(x + 1, y)] = "DOWN"
    if (x - 1) >= 0:
        move[get_index(x - 1, y)] = "UP"
    if (y + 1) < size:
        move[get_index(x, y + 1)] = "RIGHT"
    if (y - 1) >= 0:
        move[get_index(x, y - 1)] = "LEFT"
    for key in move:
        children[swap(state, state.index("0"), key)] = move[key]
    return children


def get_coordinate(state):
    index = state.index("0")
    if index // size == 0:
        x = 0
    elif index // size == 1:
        x = 1
    elif index // size == 2:
        x = 2
    elif index // size == 3:
        x = 3
    else:
        x = 4
    if index % size == 0:
        y = 0
    elif index % size == 1:
        y = 1
    elif index % size == 2:
        y = 2
    elif index % size == 3:
        y = 3
    else:
        y = 4
    return x, y


def get_index(x, y):
    index = 0
    if x == 1:
        index += size
    elif x == 2:
        index += size * 2
    elif x == 3:
        index += size * 3
    elif x == 4:
        index += size * 4
    if y == 1:
        index += 1
    elif y == 2:
        index += 2
    elif y == 3:
        index += 3
    elif y == 4:
        index += 4
    return index


def swap(s, a, b):
    n = list(s)
    temp = n[a]
    n[a] = n[b]
    n[b] = temp
    return ''.join(n)


def bfs_winnable():
    children = [goal]
    fringe = deque()
    fringe.appendleft(goal)
    visited = set()
    visited.add(goal)
    while len(fringe) != 0:
        v = fringe.pop()
        c = get_children(v)
        for a in range(0, len(c)):
            if c[a] not in visited:
                fringe.appendleft(c[a])
                visited.add(c[a])
                children.append(c[a])
    return children


def bfs_winnable_set():
    children = set()
    children.add(goal)
    fringe = deque()
    fringe.appendleft(goal)
    visited = set()
    visited.add(goal)
    while len(fringe) != 0:
        v = fringe.pop()
        c = get_children(v)
        for a in range(0, len(c)):
            if c[a] not in visited:
                fringe.appendleft(c[a])
                visited.add(c[a])
                children.add(c[a])
    return children


def random_state():
    m = []
    for i in range(0, size * size):
        r = str(random.randint(0, 8))
        while r in m:
            r = str(random.randint(0, 8))
        m.append(str(r))
    return ''.join(m)


def random_solvable():
    rs = bfs_winnable()
    s = random.randint(0, len(rs) - 1)
    return rs[s]


def print_path(state):
    start = Node(state, None, 0, None)
    fringe = deque()
    fringe.appendleft(start)
    visited = set()
    visited.add(start.get_state())
    while len(fringe) != 0:
        v = fringe.pop()
        if goal_test(v.get_state()):
            print(v.get_path_length())
            parents = list()
            p = v
            while p is not None:
                parents.append(p)
                p = p.get_parent()
            if parents:
                print_puzzle(parents.pop().get_state())
                print()
            while parents:
                t = parents.pop()
                print_puzzle(t.get_state())
                print(t.get_dir())
                print()
            break
        c = get_child_dir(v.get_state())
        temp = []
        for e in c:
            add = Node(e, v, v.get_path_length() + 1, c[e])
            temp.append(add)
        for a in range(0, len(c)):
            if temp[a].get_state() not in visited:
                fringe.appendleft(temp[a])
                visited.add(temp[a].get_state())


def path(state):
    start = Node(state, None, 0, None)
    fringe = deque()
    fringe.appendleft(start)
    visited = set()
    visited.add(start.get_state())
    while len(fringe) != 0:
        v = fringe.pop()
        if goal_test(v.get_state()):
            return v.get_path_length()
        c = get_child_dir(v.get_state())
        temp = []
        for e in c:
            add = Node(e, v, v.get_path_length() + 1, c[e])
            temp.append(add)
        for a in range(0, len(c)):
            if temp[a].get_state() not in visited:
                fringe.appendleft(temp[a])
                visited.add(temp[a].get_state())


def random_gen():
    r = random.randint(100, 1000)
    solve = bfs_winnable_set()
    y = []
    for a in range(1, r):
        b = random_state()
        if b in solve:
            y.append(path(b))
    print("Longest Path Length:" + str(max(y)))
    print("Average Path Length:" + str(sum(y)/len(y)))
    print("Percent Solvable:" + str(len(y)/r * 100))


def longest_solvable():
    fringe = deque()
    fringe.appendleft(goal)
    visited = set()
    last = ""
    while len(fringe) != 0:
        v = fringe.pop()
        for a in get_children(v):
            if a not in visited:
                fringe.appendleft(a)
                visited.add(a)
                last = a
    return last


def print_path_dfs(state):
    start = Node(state, None, 0, None)
    fringe = list()
    fringe.append(start)
    visited = set()
    visited.add(start.get_state())
    while len(fringe) != 0:
        v = fringe.pop()
        visited.add(v)
        if goal_test(v.get_state()):
            print(v.get_path_length())
            parents = list()
            p = v
            while p is not None:
                parents.append(p)
                p = p.get_parent()
            if parents:
                print_puzzle(parents.pop().get_state())
                print()
            while parents:
                t = parents.pop()
                print_puzzle(t.get_state())
                print(t.get_dir())
                print()
            break
        c = get_child_dir(v.get_state())
        temp = []
        for e in c:
            add = Node(e, v, v.get_path_length() + 1, c[e])
            temp.append(add)
        for a in range(0, len(temp)):
            if temp[a].get_state() not in visited:
                fringe.append(temp[a])
                visited.add(temp[a].get_state())


def moves(moves_away):
    start = Node(goal, None, 0, None)
    fringe = deque()
    fringe.appendleft(start)
    visited = set()
    visited.add(start.get_state())
    count = 0
    while len(fringe) != 0:
        v = fringe.pop()
        if v.get_path_length() == moves_away:
            count += 1
        c = get_child_dir(v.get_state())
        temp = []
        for e in c:
            add = Node(e, v, v.get_path_length() + 1, c[e])
            temp.append(add)
        for a in range(0, len(c)):
            if temp[a].get_state() not in visited:
                fringe.appendleft(temp[a])
                visited.add(temp[a].get_state())
    return count


def parity_check(state):
    if state == goal:
        return 1
    out_of_order = 0
    temp = state[:state.index("0")] + state[state.index("0") + 1:]
    for a in range(0, len(temp)):
        for b in range(a, len(temp)):
            if temp[b] < temp[a]:
                out_of_order += 1
    if size % 2 == 1:
        if out_of_order % 2 == 0:
            return 1
        else:
            return 0
    else:
        (x, y) = get_coordinate(state)
        if x % 2 == 0:
            if out_of_order % 2 == 1:
                return 0
            else:
                return 1
        else:
            if out_of_order % 2 == 0:
                return 0
            else:
                return 1


size = 3
goal = "012345678"
print_path("806547231")
