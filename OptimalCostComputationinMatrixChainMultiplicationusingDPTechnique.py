def matrix_chain_order(p):
    """
    p: list of matrix dimensions such that matrix i has dimensions p[i-1] x p[i]
       for i = 1, 2, ..., n (so len(p) = n + 1 for n matrices)

    Returns:
        m: DP table where m[i][j] = minimum number of scalar multiplications
           needed to compute the product of matrices i through j
        s: table used to reconstruct the optimal parenthesization
    """
    n = len(p) - 1  # number of matrices

    # m[i][j] = min cost to multiply matrices i..j
    m = [[0] * (n + 1) for _ in range(n + 1)]
    # s[i][j] = index k where the optimal split occurs
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # chain_len is the length of the chain being considered
    for chain_len in range(2, n + 1):
        for i in range(1, n - chain_len + 2):
            j = i + chain_len - 1
            m[i][j] = float('inf')

            # Try every possible split point k
            for k in range(i, j):
                cost = (m[i][k] + m[k + 1][j] +
                        p[i - 1] * p[k] * p[j])

                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


def print_optimal_parens(s, i, j):
    """Reconstructs and prints the optimal parenthesization."""
    if i == j:
        print(f"A{i}", end="")
    else:
        print("(", end="")
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j] + 1, j)
        print(")", end="")


# Driver code
if __name__ == "__main__":
    # Example: dimensions for matrices A1, A2, A3, A4
    # A1: 10x30, A2: 30x5, A3: 5x60, A4: 60x10
    p = [10, 30, 5, 60, 10]

    n = len(p) - 1
    m, s = matrix_chain_order(p)

    print("Matrix dimensions:", p)
    print("Minimum number of multiplications:", m[1][n])

    print("Optimal Parenthesization: ", end="")
    print_optimal_parens(s, 1, n)
    print()

    print("\nCost Table (m):")
    for row in m[1:]:
        print(row[1:])