from collections import deque


def _reconstruct_path(parents, start, goal):
    if goal != start and goal not in parents:
        return []

    path = [goal]
    current = goal
    while current != start:
        current = parents[current]
        path.append(current)

    path.reverse()
    return path


def _generic_search(maze, start, goal, pop_index):

    frontier = deque([start])

    reached = {start}
    parents = {}
    expanded_order = []

    while frontier:
        current = frontier[pop_index]
        del frontier[pop_index]

        expanded_order.append(current)

        if current == goal:
            break

        for neighbor in maze.safe_neighbors(current):
            if neighbor not in reached:
                reached.add(neighbor)
                parents[neighbor] = current
                frontier.append(neighbor)

    path = _reconstruct_path(parents, start, goal)
    return path, expanded_order


def bfs(maze, start: tuple[int, int], goal: tuple[int, int]):
    return _generic_search(maze, start, goal, pop_index=0)


def dfs(maze, start: tuple[int, int], goal: tuple[int, int]):
    return _generic_search(maze, start, goal, pop_index=-1)
