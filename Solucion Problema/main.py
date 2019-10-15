from gurobipy import GRB, Model, quicksum
from csv import reader, DictReader

# TODO tener cuidado con que las cosas empiezan desde el 1, por lo que es mejor

# TODO hacer A, agregar M, agregar F

modelo = Model()

'''Constantes '''
# M es M >> 0
# M = 21
# Tb es el límite superior de T
# Tb = 14
parametros = "Parametros_2"
URL_C = f"{parametros}/C.csv"
URL_B_U_M = f"{parametros}/B,U,M.csv"
URL_D_H_L = f"{parametros}/D,H,L.csv"
URL_F = f"{parametros}/F.csv"
URL_N = f"{parametros}/N.csv"
URL_Q = f"{parametros}/Q.csv"
URL_F = f"{parametros}/F.csv"

''' Conjuntos'''

# Piezas
Pb = 2
P = tuple(i for i in range(1, Pb + 1))
P2 = P
# Periodos
Tb = 4
T = tuple(i for i in range(0, Tb + 1))
T2 = T
# T0 = tuple(i for i in range(0, Tb + 1))

# Enfermedades
with open(URL_B_U_M, "r") as f:
    # E = dict()
    E = set()
    dict_reader = DictReader(f)
    for row in dict_reader:
        # E[row["e"]] = row["NAME"]
        E.add(int(row["e"]))
    largo_e = len(E)

''' Parámetros '''

# Cantidad de pacientes con la enfermedad e ∈ E a ser internados provenientes
# de urgencia turno t ∈ Γ.
with open(URL_D_H_L, "r") as f:
    d = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        d[(int(row["e"]), int(row["t"]))] = int(row["D"])
    for e in E:
        for t in range(0, Tb + 1):
            if (e,t) not in d.keys():
                d[(e, t)] = 0
# Cantidad de pacientes con enfermedad e ∈ E que ingresan por consulta
# (no urgencia) el turno t ∈ Γ.
with open(URL_D_H_L, "r") as f:
    h = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        h[(int(row["e"]), int(row["t"]))] = int(row["H"])
    for e in E:
        for t in range(0, Tb + 1):
            if (e,t) not in h.keys():
                h[(e, t)] = 0
# Costo monetario asociado a trasladar un paciente con enfermedad e ∈ E desde
# la pieza i ∈ P a la pieza j ∈ P.
with open(URL_C, "r") as f:
    c = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        c[(int(row["e"]), int(row["i"]), int(row["j"]))] = int(row["C"])
    for e in E:
        for i in P:
            for j in P:
                if (e, i, j) not in c.keys():
                    c[e, i, j] = 0
# Costo monetario de no internar un paciente de urgencia con la enfermedad e ∈ E
# el día t ∈ Γ.
with open(URL_D_H_L, "r") as f:
    l = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        l[(int(row["e"]), int(row["t"]))] = int(row["L"])
    for e in E:
        for t in range(0, Tb + 1):
            if (e,t) not in l.keys():
                l[(e, t)] = 0
# Número de días esperados de internación de un paciente con enfermedad e ∈ E.
# TODO ver si los keys de un elemento los dejo sueltos o como una tupla de un elemento
with open(URL_B_U_M, "r") as f:
    b = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        b[int(row["e"])] = int(row["B_2"])
    for e in E:
        if e not in b.keys():
                b[e] = 0
# Número máximo de días de espera para un paciente con enfermedad e ∈ E de
# consulta (no urgente) para ser internado.
with open(URL_B_U_M, "r") as f:
    m = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        m[int(row["e"])] = int(row["M_2"])
    for e in E:
        if e not in m.keys():
                m[e] = 0
# Capacidad de la pieza i ∈ P (camillas).
with open(URL_Q, "r") as f:
    q = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        q[int(row["i"])] = int(row["Q"])
    for i in P:
        if i not in q.keys():
                q[i] = 0
# Binario. 1 si y solo si la pieza i ∈ P es apta para recibir pacientes
# con la patología e ∈ E. 0 E.O.C.
with open(URL_F, "r") as f:
    a = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        i = int(row["i"])
        e = int(row["e"])
        a[(i, e)] = 1
    for i in P:
        for e in E:
            if (i, e) not in a.keys():
                a[(i, e)] = 0
# Costo monetario de habilitar la pieza i ∈ P el día t ∈ Γ.
with open(URL_N, "r") as f:
    n = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        n[int(row["i"]), int(row["t"])] = int(row["N"])
    for i in P:
        for t in range(0, Tb + 1):
            if (i,t) not in n.keys():
                n[(i, t)] = 0
# Cantidad de pacientes con enfermedad e ∈ E provenientes de consulta que
# esperan a ser internados antes de la implementación del sistema.
with open(URL_B_U_M, "r") as f:
    u = dict()
    dict_reader = DictReader(f)
    for row in dict_reader:
        u[int(row["e"])] = int(row["U"])
    for e in E:
        if e not in u.keys():
                u[e] = 0
# F
with open(URL_F, "r") as file:
    f = dict()
    dict_reader = DictReader(file)
    for row in dict_reader:
        f[int(row["e"]), int(row["i"])] = int(row["F"])
    for e in E:
        for i in P:
            if (e,i) not in f.keys():
                f[(e, i)] = 0

''' CONSTANTES '''
# Max({3*(8-i)}) donde i es el indice de la pieza
# 3*(8-i) es como calculamos la capacidad de la pieza i
# M = 21
M = 100




''' Variables '''

# Cantidad de pacientes con enfermedad e ∈ E internados que hay en el día
# t ∈ Γ que fueron ingresados el día d ∈ Γ en la pieza i ∈ P.
x = modelo.addVars(E, P, T, T2, vtype=GRB.INTEGER, name="x")
# Cantidad de pacientes con enfermedad e ∈ E internados en la pieza i ∈ P el
# día t ∈ Γ.
w = modelo.addVars(E, P, T, T2, vtype=GRB.INTEGER, name="w")
# Cantidad de pacientes con enfermedad e ∈ E internados en la pieza i ∈ P el día
# t ∈ Γ por urgencia.
k = modelo.addVars(E, P, T, vtype=GRB.INTEGER, name="k")
# Cantidad de pacientes con patología e ∈ E internados en la pieza i ∈ P el día
# t ∈ Γ por no urgencia que esperan a ser internados desde el día d ∈ Γ.
nu = modelo.addVars(E, P, T, T2, vtype=GRB.INTEGER, name="nu")
# Cantidad de pacientes ingresados el día d ∈ Γ con la enfermedad e ∈ E movidos
# desde la pieza i ∈ P a la pieza j ∈ P el día t ∈ Γ.
z = modelo.addVars(E, P, P2, T, T2, vtype=GRB.INTEGER, name="z")
# Cantidad de pacientes ingresados el día d ∈ Γ con enfermedad e ∈ E internados
# en la pieza i ∈ P que son dados de alta el día t ∈ Γ.
y = modelo.addVars(E, P, T, T2, vtype=GRB.INTEGER, name="y")
# Binario. 1 si y solo si la pieza i ∈ P está habilitada el día t ∈ E. 0 E.O.C.
v = modelo.addVars(P, T, vtype=GRB.BINARY, name="v")

modelo.update()




''' Restricciones '''

# Flujo común
modelo.addConstrs((x[e, i, t, d] == x[e, i , (t - 1), d] + quicksum(z[e, j, i, t, d] - z[e, i, j, t, d] for j in P2) + w[e, i, t, d] - y[e, i, t, d] for e in E for i in P for d in T for t in range(1, Tb) if (d < t)), name="c1")

# Todos se van el día que les corresponde
# TODO revisar si aqui hay un error, si no el constraint hay que hacerlo con addConstr
modelo.addConstrs((quicksum(w[e, i, t, d] for i in P) == quicksum(y[e, i, t + b[e], d] for i in P) for e in E for d in T2 for t in T if ((t <= (Tb - b[e])) and (d <= t))), name="c2")

# La gente que ingresa es la suma de los ingresados por urgencia con los de consulta
modelo.addConstrs((w[e, i, t, t] == k[e, i, t] + quicksum(nu[e, i, t, b] for b in T2 if b <= t) for e in E for i in P for t in T), name="c3")
# modelo.addConstrs((w[e, i, t, t] == k[e, i, t] for e in E for i in P for t in T), name="c3")

# Nunca se sobrepasa la capacidad de piezas
modelo.addConstrs((quicksum(x[e, i, t, d] for e in E for d in T) <= q[i] for i in P for t in T), name="c4")

# Las piezas deben ser aptas para recibir a los pacientes
# M >> 0, M = 14
modelo.addConstrs((quicksum(x[e, i, t, d] for d in T2) <= a[i,e] * M for e in E for t in T), name="c5")

# Relacionar variable v_{it}. M >> 0, M = 14
modelo.addConstrs((v[i, t] <= quicksum(x[e, i, t, d] for e in E for d in T) for i in P for t in T), name="c6.1")
modelo.addConstrs((quicksum(x[e, i, t, d] for e in E for d in T) <= M * v[i, t] for i in P for t in T), name="c6.2")

# Atender a todos los no urgentes(desde el día 2 en adelante)
# TODO revisar que la sumatoria funcione
# TODO revisar que el +1 de la sumatoria este bien, y que funcione el range
# modelo.addConstrs((quicksum(nu[e, i, t, b] for t in range(b, b + m[e] + 1)) == h[e, b] for e in E for b in T if ((2 <= b) and (b <= Tb - m[e]))), name= "c7")

# Atender a todos los pacientes no urgentes y a los que estaban esperando antes
# de la implementación del sistema
# TODO revisar el 1
# modelo.addConstrs((quicksum(nu[e, i, t, 1] for t in range(1, m[e] + 1 + 1) for i in P) == h[e, 1] + u[e] for e in E), name="c8")

# Nadie se va el día que no le corresponde
# TODO revisar el if y orden de fors
modelo.addConstrs((y[e, i, t, d] == 0 for e in E for i in P for t in T for d in T2 if t != (d + b[e])), name="c9")

# Restriccion trivial
modelo.addConstrs((w[e, i, t, d] == 0 for i in P for e in E for t in T for d in T2 if d > t), name= "c10")
#

# ''' NUEVO '''
# modelo.addConstrs((quicksum(nu[e, i, t, b] for t in range(b, b + m[e] + 1)) == h[e, b] + d[e, b] for e in E for b in T if ((2 <= b) and (b <= Tb - m[e]))), name= "c7")


# # Inicialización de las Variables
modelo.addConstrs((x[e, i, 0, d] == 0 for e in E for i in P for d in T), name="c11")

#


# Restriccion q se deberia cumplir pero no lo esta haceindo. ACEPTAR A TODA LA URGENCIA
# modelo.addConstrs(quicksum(k[e,i,t] for i in P) == d[e,t] for e in E for t in T)
''' Función Objetivo '''
# modelo.setObjective(quicksum(l[e, t] * (d[e, t] - k[e, i , t]) for e in E for t in T for i in P) + quicksum(v[i, t] * n[i, t] for i in P for t in T) + quicksum(c[e, i, j] * z[e, i, j, t, d] for e in E for i in P for j in P2 for t in T for d in T2) + quicksum(w[e, i, t] * f[e, i] for e in E for t in T for i in P), GRB.MINIMIZE)
# modelo.setObjective(quicksum(l[e, t] * (d[e, t] - k[e, i , t]) for e in E for t in T for i in P) + quicksum(x[e, i, t, d] * f[e, i] for i in P for e in E for t in range(1, len(T)) for d in T), GRB.MINIMIZE)
modelo.setObjective(quicksum(l[e, t] * (d[e, t] - k[e, i , t]) for e in E for t in T for i in P), GRB.MINIMIZE)

''' Solucion '''
modelo.optimize()

# Mostrar los valores de las soluciones
modelo.printAttr("X")
# print(maximo_dia)
