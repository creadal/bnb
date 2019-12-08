from pulp import *


MINIMIZE = LpMinimize
MAXIMIZE = LpMaximize


objective = [] # list of coefficients for objective function
constraints = [] # matrix m x (n+1) of constraints coefficients where n is number of variables, m - number of constraints
signs = [] # signs for our constraints


bound_max = -999999
bound_min = 999999


def solve_continious_problem(obj, coefs, signs, problem = MAXIMIZE):

    global bound_min
    global bound_max

    n = len(obj)

    prob = LpProblem('name', problem)

    vars = []
    for i in range(n):
        vars.append(LpVariable('{}'.format(i)))

    prob += lpSum([obj[i]*vars[i] for i in range(n)])

    m = len(coefs)

    for i in range(m):
        if signs[i] == '<=':
            prob += lpSum([coefs[i][j]*vars[j] for j in range(n)]) <= coefs[i][-1]
        elif signs[i] == '>=':
            prob += lpSum([coefs[i][j]*vars[j] for j in range(n)]) >= coefs[i][-1]

    prob.solve()

    if problem == MAXIMIZE: bound_max = max(value(prob.objective), bound_max)
    if problem == MINIMIZE: bound_min = min(value(prob.objective), bound_min)

    return [value(vars[i]) for i in range(n)], value(prob.objective), prob.status


#print(solve_continious_problem([1, 2], [[2, 2, 7], [4, -5, 9], [1, 0, 0], [0, 1, 0]], ['<=', '<=', '>=', '>=']))


variables = None
result = None


def branch(obj, coefs, signs, problem = MAXIMIZE):

    global result
    global variables

    values, solution, status = solve_continious_problem(obj, coefs, signs, problem)

    if status != 1:
        return 'stopped'

    n = len(obj)

    branched = False

    for i in range(n):

        if values[i] != int(values[i]):

            branched = True

            upper = int(values[i]+1)
            lower = int(values[i])

            coefs_u = coefs[:]

            constr_u = [0] * (n+1)
            constr_u[i] = 1
            constr_u[-1] = upper

            signs_u = signs[:]
            signs_u.append('>=')

            coefs_u.append(constr_u)

            branch(obj, coefs_u, signs_u, problem)


            coefs_l = coefs[:]

            constr_l = [0] * (n+1)
            constr_l[i] = 1
            constr_l[-1] = lower

            signs_l = signs[:]
            signs_l.append('<=')

            coefs_l.append(constr_l)

            branch(obj, coefs_l, signs_l, problem)

    if not branched:

        variables = values

        if result == None:
            result = solution
            
        else:
            if problem == MAXIMIZE:
                result = max(result, solution)
            elif problem == MINIMIZE:
                result = min(result, solution)
        
branch([1, 4], [[2, 4, 17], [10, 3, 15], [1, 0, 0], [0, 1, 0]], ['<=', '<=', '>=', '>='])

print(variables, result)



