from gurobipy import GRB, Model

m = Model()

m.addVar()

x = m.addVar(vtype=GRB.BINARY, name="x")
y = m.addVar(vtype=GRB.BINARY, name="y")
z = m.addVar(vtype=GRB.BINARY, name="z")

m.update()

m.setObjective(x + y + 2*z, GRB.MAXIMIZE)

m.addConstr(x + 2*y + 3*z <= 6, name="c0")
m.addConstr(x + y >= 1, name="c1")

m.optimize()

m.printAttr("X")

for constr in m.getConstrs():
    print(constr, constr.getAttr("slack"))