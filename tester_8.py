from Simplex import ModeloLineal
prueba_1  =ModeloLineal( costos = [-1,-2,1,-4],
variables = ["x_1","x_2","x_3","x_4"],
columnas = [[1,1],[2,3],[-3,1],[1,2]],
igualdades = ["leq", "leq"],
b = [4,8],
naturaleza = ["geq","geq","geq","geq"])
print (prueba_1)
prueba_1.minimizar()
