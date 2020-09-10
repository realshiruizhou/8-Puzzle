import sys
import random
from collections import deque
import time


class Node:
    # Node class, which keeps track of the Nodes' string,
    # parent Node, length to get to that node from root,
    # and the direction the 0 moved to get to the Node.
    def __init__(self, state, parent, path_length, dir):
        # standard constructor to initialize all variables
        self.parent = parent
        self.path_length = path_length
        self.state = state
        self.dir = dir

    def get_parent(self):
        # returns the parent of the Node
        return self.parent

    def get_path_length(self):
        # returns the path length to the Node from root
        return self.path_length

    def get_state(self):
        # returns the string that represents the puzzle state
        return self.state

    def get_dir(self):
        # returns direction to get to Node from parent
        return self.dir


# question 1________________________________________________________
def goal_test(state):
    # determines if current state is the same as goal state
    return goal == state


def print_puzzle(state):
    # prints the puzzle
    count = 1
    for a in state:
        if count % size == 0:
            # if row is filled start a new row
            print(a + " ")
        else:
            # else continue on that row
            print(a + " ", end="", flush=True)
        count += 1


def get_children(state):
    # gives all children made by moving the blank space
    (x, y) = get_coordinate(state)  # (row, column) of 0
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
    # returns the (row, column) of 0 in state,
    index = state.index("0")
    x = index // size
    y = index % size
    return x, y


def get_index(x, y):
    # returns the index of a value in the string based on
    # the (row, column) representation.
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


# question 2________________________________________________________
def bfs_winnable():
    # starting from the goal state, finds all states
    # accessible from goal and puts them in a list (BFS)
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


# question 3________________________________________________________
def random_state():
    # makes a random game state
    m = []
    for i in range(0, size * size):
        r = str(random.randint(0, (size * size) - 1))
        while r in m:
            # replace r if already there (random non-repeating)
            r = str(random.randint(0, (size * size) - 1))
        m.append(str(r))
    return ''.join(m)


def random_solvable():
    # gives a solvable game state from the list of accessible
    # states randomly
    rs = bfs_winnable()
    s = random.randint(0, len(rs) - 1)
    return rs[s]


# question 4________________________________________________________
def get_child_dir(state):
    # modified get_children to include direction it took to
    # get to child and returns a dictionary with key being the
    # child and value being the direction
    (x, y) = get_coordinate(state)
    move = {}  # keeps track of direction with index as key
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


def path(state):
    # gives the shortest length to the goal state, using the
    # Node class to keep track of path length and parents
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
        temp = []  # storage for children (Nodes)
        for e in c:
            # change the dictionary to Nodes with direction
            add = Node(e, v, v.get_path_length() + 1, c[e])
            temp.append(add)
        for a in range(0, len(c)):
            if temp[a].get_state() not in visited:
                fringe.appendleft(temp[a])
                visited.add(temp[a].get_state())


def print_path(state):
    # same thing as path() but prints the path it takes to get
    # to the goal from the root
    start = Node(state, None, 0, None)
    fringe = deque()
    fringe.appendleft(start)
    visited = set()
    visited.add(start.get_state())
    while len(fringe) != 0:
        v = fringe.pop()
        if goal_test(v.get_state()):
            # stores parents with a stack to pop later
            print(v.get_path_length())
            parents = list()
            p = v
            while p is not None:
                # add to stack until no more parents
                parents.append(p)
                p = p.get_parent()
            if parents:
                # print the root without direction
                print_puzzle(parents.pop().get_state())
                print()
            while parents:
                # print the rest of the parents to goal with direction
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


# question 7________________________________________________________
def path_dfs(state):
    # same function as question 4 (find length of path to goal), but
    # with DFS
    start = Node(state, None, 0, None)
    fringe = list()
    fringe.append(start)
    visited = set()
    visited.add(start.get_state())
    while len(fringe) != 0:
        v = fringe.pop()
        visited.add(v)
        if goal_test(v.get_state()):
            return v.get_path_length()
        c = get_child_dir(v.get_state())
        temp = []
        for e in c:
            add = Node(e, v, v.get_path_length() + 1, c[e])
            temp.append(add)
        for a in range(0, len(temp)):
            if temp[a].get_state() not in visited:
                fringe.append(temp[a])
                visited.add(temp[a].get_state())


def print_path_dfs(state):
    # same function as question 4 (print path), but uses DFS
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


# question 9________________________________________________________
def moves(moves_away):
    # counts how many children are moves_away moves from the
    # start (goal)
    start = Node(goal, None, 0, None)
    fringe = deque()
    fringe.appendleft(start)
    visited = set()
    visited.add(start.get_state())
    count = 0
    while len(fringe) != 0:
        v = fringe.pop()
        if v.get_path_length() == moves_away:
            # increment if path length is equal to moves_away
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


# question 10_______________________________________________________
def parity_check(state):
    # check to see if the puzzle is solvable
    if goal_test(state):
        return 1
    out_of_order = pairs(state)
    ref = pairs(goal)
    if size % 2 == 1:
        # for odd size boards
        if out_of_order % 2 == ref % 2:
            return 1
        else:
            return 0
    else:
        # for even sized boards
        (x, y) = get_coordinate(state)
        (a, b) = get_coordinate(goal)
        if x % 2 == a % 2:
            if out_of_order % 2 == ref % 2:
                return 1
            else:
                return 0
        if x % 2 != a % 2:
            if out_of_order % 2 != ref % 2:
                return 1
            else:
                return 0


def pairs(state):
    # counts the number of out of order pairs
    out_pairs = 0
    temp = state[:state.index("0")] + state[state.index("0") + 1:]  # exclude blank
    for a in range(0, len(temp)):
        for b in range(a, len(temp)):
            if temp[b] < temp[a]:
                out_pairs += 1
    return out_pairs


# final question_____________________________________________________________
file = open(sys.argv[1], "r")
total_time = 0
for line in file:
    a = line.split()
    size = int(a[0])
    goal = a[2]
    state = a[1]
    start = time.process_time()
    solvable = parity_check(state)
    end = time.process_time()
    time1 = end - start
    time2 = 0
    if solvable == 0:
        print("No solution. It took %f seconds to find no solution" % time1)
    else:
        start2 = time.process_time()
        p = path(state)
        end2 = time.process_time()
        time2 = end2 - start2
        print(str(p) + " It took %f seconds to solve" % (time1 + time2))
    total_time += time1 + time2
print("Total number of seconds to process all input pairs: %f" % total_time)
