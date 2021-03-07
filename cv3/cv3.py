import gurobipy as g
import matplotlib.pyplot as plt

n = 5
params = {
0: {'r': 20, 'd': 45, 'p': 15},
1: {'r': 4, 'd': 30, 'p': 19},
2: {'r': 5, 'd': 80, 'p': 20},
3: {'r': 17, 'd': 70, 'p': 8},
4: {'r': 27, 'd': 66, 'p': 7}
}
#model
model = g.Model()

#ADD variables
r = [params[i]['r'] for i in range(n)]
d = [params[i]['d']-params[i]['p'] for i in range(n)]

s = model.addVars(n, vtype=g.GRB.CONTINUOUS, lb=r, ub=d)

x = model.addVars(n, n, vtype=g.GRB.BINARY)

#add constraints
#for i in range(n):
#    model.addConstr(s[i] >= params[i]['r'])
#    model.addConstr(s[i]) <= params[i]['d'] - params[i]['p']

M = max(params[i]['d'] for i in range(n))

for i in range(n):
    for j in range(n):
        if i != j:
            model.addConstr(s[i] + params[i]['p'] <= s[j] + M*x[i,j])
            model.addConstr(s[j] + params[j]['p'] <= s[i] + M*(1-x[i,j]))

#set objective

#call the solver
model.optimize()

#print solution
print("/n SOLUTION")

def plot_solution(s, p):
    """
    s: solution vector
    p: processing times
    """
    fig = plt.figure(figsize=(10,2))
    ax = plt.gca()
    ax.set_xlabel('time')
    ax.grid(True)
    ax.set_yticks([2.5])
    ax.set_yticklabels(["oven"])
    eps = 0.25 # just to show spaces between the dishes
    ax.broken_barh([(s[i], p[i]-eps) for i in range(len(s))], (0, 5),
    facecolors=('tab:orange', 'tab:green', 'tab:red', 'tab:,→blue', 'tab:gray'))
# TODO: plot your solution
plot_solution([23.0, 4.0, 53.0, 38.0, 46.0], [params[i]["p"] for i in range(n)])