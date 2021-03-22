import gurobipy as g

d = [5, 5, 5, 5, 5, 10, 10, 15, 20, 20, 30, 30, 40, 50, 60, 60, 60, 50, 40, 30, 30, 20, 10, 5]
n_base = 3
e_base = 7
c_base = 2.0 / 24.0
n_peak = 40
e_peak = 2
c_peak = 12
s_max = 100
gamma = 0.75

#MODEL
m = g.Model()

# VARIABLES
base_plant = m.addVar(lb=0.0, ub=n_base, vtype=g.GRB.INTEGER, name="base_plant_count")
peak_plants = m.addVars(len(d), lb=0.0, ub=n_peak, vtype=g.GRB.INTEGER, name="peak_plant_count")

# CONSTRAINTS
for hour, demand in enumerate(d):
    m.addConstr(demand <= e_base * base_plant + e_peak * peak_plants[hour]) # pro kazdou hodinu musi byt demand vyplneny

# OBJECTIVE
m.setObjective(24 * c_base * base_plant + c_peak * g.quicksum(peak_plants), g.GRB.MINIMIZE)

m.optimize()

n_base_opt = base_plant.x
n_peak_opt = []
for peak in peak_plants:
    n_peak_opt.append(peak.x)

