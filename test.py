from pulp import *

prob = LpProblem('h', -1)

x = LpVariable('x')
y = LpVariable('y')

prob += x+2*y

prob += 2*x+2*y<=7
prob += 4*x-5*y<=9
prob += x>=0
prob += y>=4

prob.solve()
print(LpStatus[prob.status])

print(value(x), value(y))