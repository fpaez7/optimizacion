
from Simplex import ModeloLineal
prueba_1  =ModeloLineal( costos = [2,1],
variables = ["x_1","x_2"],
columnas = [[-4,1,1],[3,3,-1]],
igualdades = ["leq","geq", "leq"],
b = [6,3,1],
naturaleza = ["geq","geq"])
print (prueba_1)
prueba_1.simplex (["h_1","t_1","h_3"],1,1)
