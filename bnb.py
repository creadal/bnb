from pulp import *


MINIMIZE = LpMinimize
MAXIMIZE = LpMaximize


objective = [] # list of coefficients for objective function
constraints = [] # matrix m x (n+1) of constraints coefficients where n is number of variables, m - number of constraints
signs = [] # signs for our constraints


def solve_continious_problem(obj, coefs, signs, problem = MINIMIZE):

    n = len(obj)

    prob = LpProblem('name', problem)

    vars = []
    for i in range(n):
        vars.append(LpVariable('{}'.format(i)))

    prob += lpSum([obj[i]*vars[i] for i in range(n)])

    m = len(coefs)

    for i in range(m):
        if signs[i] == '<=':
            prob += lpSum([coefs[i][j]*vars[j] for j in range(n)]) <= coefs[-1]
        elif signs[i] == '>=':
            prob += lpSum([coefs[i][j]*vars[j] for j in range(n)]) >= coefs[-1]

    prob.solve()

    return [value(vars[i]) for i in range(n)]


print(solve_continious_problem([1, 4], [[2, 4, 7], [10, 3, 15], [1, 0, 0], [0, 1, 0]], ['<=', '<=', '>=', '>='])) 
