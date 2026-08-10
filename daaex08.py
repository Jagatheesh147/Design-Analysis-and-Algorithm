import heapq

class Node:
    def __init__(self, level, path, reduced_matrix, cost, visited):
        self.level = level                  # depth in the search tree (number of cities fixed)
        self.path = path                    # path taken so far (list of city indices)
        self.reduced_matrix = reduced_matrix # reduced cost matrix at this node
        self.cost = cost                    # lower bound on cost from this node
        self.visited = visited              # set of visited cities

    def __lt__(self, other):
        # Needed for heapq to compare nodes by cost (min-heap = best-first search)
        return self.cost < other.cost


def reduce_matrix(matrix):
    """
    Reduces the matrix so every row and column has at least one zero,
    and returns the total reduction cost (lower bound contribution).
    """
    n = len(matrix)
    reduced = [row[:] for row in matrix]
    reduction_cost = 0

    # Row reduction
    for i in range(n):
        row_min = min(reduced[i])
        if row_min != float('inf') and row_min > 0:
            reduction_cost += row_min
            for j in range(n):
                if reduced[i][j] != float('inf'):
                    reduced[i][j] -= row_min

    # Column reduction
    for j in range(n):
        col_min = min(reduced[i][j] for i in range(n))
        if col_min != float('inf') and col_min > 0:
            reduction_cost += col_min
            for i in range(n):
                if reduced[i][j] != float('inf'):
                    reduced[i][j] -= col_min

    return reduced, reduction_cost


def copy_matrix_with_edge(matrix, from_city, to_city, n):
    """
    Creates a new matrix after choosing the edge (from_city -> to_city):
    - sets row `from_city` and column `to_city` to infinity
    - sets (to_city, from_city) to infinity to prevent going back immediately
    """
    new_matrix = [row[:] for row in matrix]
    for k in range(n):
        new_matrix[from_city][k] = float('inf')
        new_matrix[k][to_city] = float('inf')
    new_matrix[to_city][from_city] = float('inf')
    return new_matrix


def tsp_branch_and_bound(cost_matrix):
    """
    Solves TSP using Branch and Bound with matrix reduction.
    cost_matrix[i][j] = cost of traveling from city i to city j.
    Diagonal should be float('inf') (no self loops).
    Returns (optimal_path, optimal_cost).
    """
    n = len(cost_matrix)

    # Ensure diagonal is infinity
    matrix = [row[:] for row in cost_matrix]
    for i in range(n):
        matrix[i][i] = float('inf')

    # Initial reduction
    reduced, initial_cost = reduce_matrix(matrix)

    root = Node(level=0, path=[0], reduced_matrix=reduced,
                cost=initial_cost, visited={0})

    pq = []
    heapq.heappush(pq, root)

    best_cost = float('inf')
    best_path = None

    while pq:
        node = heapq.heappop(pq)

        # Prune: if this node's bound is already worse than best found, skip
        if node.cost >= best_cost:
            continue

        # If we've visited all cities, complete the tour back to start
        if node.level == n - 1:
            last_city = node.path[-1]
            return_cost = cost_matrix[last_city][0]
            total_cost = node.cost + return_cost
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = node.path + [0]
            continue

        current_city = node.path[-1]

        for next_city in range(n):
            if next_city not in node.visited and node.reduced_matrix[current_city][next_city] != float('inf'):
                edge_cost = node.reduced_matrix[current_city][next_city]

                # Build child matrix with chosen edge locked in
                child_matrix = copy_matrix_with_edge(
                    node.reduced_matrix, current_city, next_city, n
                )
                child_reduced, reduction_cost = reduce_matrix(child_matrix)

                child_cost = node.cost + edge_cost + reduction_cost
                child_path = node.path + [next_city]
                child_visited = node.visited | {next_city}

                child = Node(
                    level=node.level + 1,
                    path=child_path,
                    reduced_matrix=child_reduced,
                    cost=child_cost,
                    visited=child_visited
                )
                heapq.heappush(pq, child)

    return best_path, best_cost


if __name__ == "__main__":
    # Example: 4-city distance matrix (symmetric, but doesn't have to be)
    INF = float('inf')
    cost_matrix = [
        [INF, 10, 15, 20],
        [10, INF, 35, 25],
        [15, 35, INF, 30],
        [20, 25, 30, INF]
    ]

    path, cost = tsp_branch_and_bound(cost_matrix)

    print("Optimal path:", " -> ".join(map(str, path)))
    print("Optimal cost:", cost)