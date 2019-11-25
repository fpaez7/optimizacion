
from numpy import array,concatenate, amin, where,set_printoptions
from scipy import linalg
import copy
import fractions
from collections import OrderedDict



## Variables Gobales
global ITERACION
ITERACION = 1
FRACTIONS = True
VERBOSO = 1  # 0, Solo entrega resultados finale y
            # 1, Minimo de las iteraciones (Vb,Vr,Z,)
            # 2, Minimo para una prueba
            # 3, Te escribo el informe






if FRACTIONS:
    set_printoptions(formatter={'all':lambda x: str(fractions.Fraction(x).limit_denominator())})
class ModeloLineal:
    """docstring for ModeloLineal."""
    def __init__(self,costos, variables, columnas , igualdades , b , naturaleza):
        self.igualdades = igualdades
        self.naturaleza = naturaleza
        self.base_inicial = []
        if len(variables) != len(columnas):
            print("error")
        # asiganamos valor a b
        self.b = b
        #asignamos las variables
        self.variables = variables
        self.auxiliares = list()


        #asignamos columnas
        self.columnas = dict()
        for i in range (0,len(self.variables)):
            self.columnas[self.variables[i]]= columnas[i]

        c = 0
        for i in range (0, len(self.igualdades)):
            igualdad = False
            auxilar = False
            #creamos las variables auxiliares y sus columnas
            parcial =[]
            for e in range (0,i):
                parcial.append(0)

            if igualdades[i] == "leq":
                parcial.append(1)
            elif igualdades[i] == "geq":
                c += 1
                auxilar = True
                parcial.append(-1)
            elif igualdades[i] == "eq":
                igualdad = True
            else:
                print(f"NO CONOZCO EL simbolo {igualdades[i]}")

            for e in range (i+1,len(igualdades)):
                parcial.append(0)
            if not igualdad:
                self.variables.append(f"h_{i+1}")
                self.columnas[f"h_{i+1}"] = parcial

            if auxilar:
                self.base_inicial.append(f"t_{c}")
                self.auxiliares.append(f"t_{c}")
                self.columnas[f"t_{c}"] = [e * -1 for e in parcial]
            else:
                self.base_inicial.append(f"h_{i+1}")



            #asignamos costos a cada variable
        self.costos =  dict()
        i = 0
        while i < len (variables):
            if i < len(costos):
                self.costos[variables[i]] = costos[i]
            else:
                self.costos[variables[i]] = 0
            i+=1
    def obtener_costos (self,variables,fase):
        parcial = []
        for variable in variables:
            if fase == 1:
                if variable[0]=="t":
                    parcial.append(1)
                else:
                    parcial.append(0)
            elif fase == 2:
                if variable in self.variables:
                    parcial.append (self.costos [variable])
                else :
                    parcial.append(0)


        return array (parcial)
    def obtener_matris (self,variables):
        parcial = array ([self.columnas[variables[0]]])

        for i in range(1,len(variables)):
            b = array ([self.columnas[variables[i]]])
            parcial = concatenate((parcial,b), axis =0)
        return parcial.T


    def __str__(self):
        s = f"""costos:{self.costos}
variables:{self.variables}
columnas:{self.columnas}
b:{self.b}
auxiliares {self.auxiliares}
base inicial {self.base_inicial}"""
        return s
    def obtener_Vr (self,Vb,fase):
        Vr = []
        for variable in self.variables:
            if variable not in Vb:
                Vr.append (variable)
        if fase == 1:
            for auxiliar in self.auxiliares:
                if auxiliar not in Vb:
                    Vr.append (auxiliar)
        return Vr
    def minimizar (self):
        with open("resultado.txt","w") as file :
            #print(self.base_inicial)
            base1 = self.simplex(self.base_inicial,fase = 1, I =1)
            print(base1)
            base2 = self.simplex(base1,fase = 2, I =1)
            print(base2)
            file.close()


    def simplex (self, Vb,fase, I):
        VERBOSO = False

    #paso 0
        B = self.obtener_matris(Vb)
        Vr = self.obtener_Vr(Vb,fase)
        R = self.obtener_matris(Vr)

        Binv = linalg.inv(B)


        BinvxR= Binv @ R
        b_ = Binv  @ self.b

        # Costos reducidos:

        CR = list(self.obtener_costos(Vr,fase) - self.obtener_costos(Vb,fase)@BinvxR)
        Min = amin(CR)
        Z = self.obtener_costos(Vb,fase) @ b_
        resultados = dict()
        for i in range(0,len(Vb)):
            resultados[Vb[i]]= b_[i]
        for i in range(0,len(Vr)):
            resultados[Vr[i]]= 0

        resultados = dict(OrderedDict(sorted(resultados.items())))

        index = where(CR == amin(CR))[0][0]

        CEntrada = Vr[index]

        print(f"I {I} " +80*"*")
        print(f"Vb: {Vb}")
        print(f"Vr: {Vr}")

        if VERBOSO:
            print(f"B: {B}")
            print(f"B^-1: {Binv}")
            print(f"R: {R}")
            print(f"B^-1xR: {BinvxR}")
            print(f"b_: {b_}")
            print(f"Costos Reducidos:")
            print(f"calulo{self.obtener_costos(Vr,fase)} ― {self.obtener_costos(Vb,fase)} x {BinvxR}")
            print(f"Resultado:{CR}")
            print(f"Minimo: {Min}")
            print(f"Funcion Objetivo: {self.obtener_costos(Vb,fase)}x{b_}")
        print(f"Variables: {resultados}")
        print(f"FO: {Z}")


        if Min >= 0:
            if Min < 0.000001:

                respuesta = input(f"Diferencia Pequeña al ingresar {CEntrada}, desea continuar (Y/N): \n")
                if respuesta.upper() == "N":
                    print(80*"*")
                    return Vb
            else:
                ITERACION = 1
                print(80*"*")
                return Vb

        # nota1
        divisores = BinvxR [:,index]
        CS = []
        for i in range (0,len(b_)):
            if divisores[i] > 0:
                CS.append(b_[i]//divisores[i])
            else: CS.append (float("inf"))

        Min_2 = amin(CS)
        index_2 = where(CS == amin(CS))[0][0]
        CSalida = Vb[index_2]# nota1
        Vbfin = copy.deepcopy(Vb)
        Vbfin.pop(index_2)
        Vbfin.insert(index_2, CEntrada)
        Vrfin= self.obtener_Vr(Vbfin,fase)
        if VERBOSO:
            print(f"Criterio de Entrada: {CEntrada}")
            print(f"b_/columna: {CS}")
            print(f"Min_2: {Min_2}")

        # caso raro que no haya candidato de salida
        if Min_2 == float("inf"):
            print("PROBELMA EN EL CRITERIO DE SALIDA")
            for i in range (0,len(b_)):
                print (f"{b_[i]}/{divisores[i]}")
            return

        if VERBOSO:
            print(f"Criterio de Salida {CSalida}")
            print(f"Vb Final: {Vbfin}")
            print(f"Vr Final: {Vrfin}")
        self.simplex (Vbfin, fase ,I+1)





"""prueba =ModeloLineal( costos = [-1,-2,-1],
variables = ["x_1","x_2","x_3"],
columnas = [[3,1,1],[2,3,2],[1,2,3]],
igualdades = ["leq", "geq","leq"],
b = [21,10,15],
naturaleza = ["geq","geq","geq"])
print (prueba)
prueba.simplex (["x_1","x_3","h_2"],fase = 1, I =1)"""

"""prueba_2 = ModeloLineal( costos = [2,1],
variables = ["x_1","x_2"],
columnas = [[-4,1,1],[3,3,-1]],
igualdades = ["leq", "geq","leq"],
b = [6,3,4],
naturaleza = ["geq","geq"])
print (prueba_2)


prueba_2.simplex(["h_1","t_1","h_3"],fase = 1, I =1)"""






#NOTAS
#nota1 En caso de empate de criterio siempre elige el primero
