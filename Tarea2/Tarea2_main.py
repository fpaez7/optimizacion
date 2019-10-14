from gurobipy import Model, GRB

m = Model()

x = m.addVar(vtype=GRB.INTEGER, name="x")
y = m.addVar(vtype=GRB.INTEGER, name="y")
z = m.addVar(vtype=GRB.INTEGER, name="z")

m.update()

m.setObjective(x + z, GRB.MAXIMIZE)

m.addConstr(x + y + z <= 5, name="c0")
m.addConstr(x - z >= -3, name="c1")
m.addConstr(x - y - z <= 1, name="c2")

m.optimize()

m.printAttr("X")
