from Simplex import ModeloLineal
prueba_1  =ModeloLineal( costos = [1,-2],
variables = ["x_1","x_2"],
columnas = [[1,-1,0],[1,1,1]],
igualdades = ["geq","geq", "leq"],
b = [3,1,3],
naturaleza = ["geq","geq"])
print (prueba_1)
prueba_1.minimizar()
