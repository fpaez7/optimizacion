from Simplex import ModeloLineal
prueba_1  =ModeloLineal( costos = [-1,-1],
variables = ["x_1","x_2"],
columnas = [[-1,0],[1,1]],
igualdades = ["leq", "leq"],
b = [1,2],
naturaleza = ["geq","geq"])
print (prueba_1)
prueba_1.minimizar()
