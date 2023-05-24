import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from sympy import *
import tkinter as tk

#Limpieza de datos termodinámicos. Extraidos de: https://www2.chem.wisc.edu/deptfiles/genchem/netorial/modules/thermodynamics/table.htm
#paso todo a un Dataframe

try:
    archivo = open('C:/Users/User/Documents/2023/inteligencia_artificial/cambio_enfoque_práctico/diagrama_Ellingham/archivo_modificado.txt', 'r')
except Exception as e:
    # handle the error and print the error message
    print("An error occurred: ", e)

archivo = archivo.readlines()
archivo = [lineas.strip() for lineas in archivo]
try:
    while True:
        archivo.remove("")
except ValueError:
    pass
titulo = ['Aluminum', 'Aqueous Solutions', 'Barium', 'Barium', 'Beryllium', 'Bromine', 
'Calcium', 'Carbon', 'Cesium', 'Chlorine', 'Chromium', 'Copper', 'Fluorine', 'Hydrogen', 'Iodine', 
'Iron', 'Lead', 'Lithium', 'Magnesium', 'Mercury', 'Nickel', 'Nitrogen', 'Oxygen', 'Phosphorus', 
'Potassium', 'Silicon', 'Silver', 'Sodium', 'Sulfur', 'Tin', 'Titanium', 'Zinc'] 
new_list = [e for e in archivo if e not in titulo]
lista_agrupada = [new_list[i:i+4] for i in range(0, len(new_list), 4)]
lista_nombres = [nombre_elemento[0] for nombre_elemento in lista_agrupada[:]]
lista_nombres =[e.replace('â€¢', '.') for e in lista_nombres]
sustancia_valores = {lista_nombres[i]:[x for x in lista_agrupada[i][1:]] for i in range(len(lista_agrupada))}
data = pd.DataFrame(sustancia_valores)
data = data.transpose()
data.columns = ["ΔHf", "S°", "DGf°"]
data = data[data.columns][:].replace('nulo', np.nan)
# print(data[25:80])


#clase Reacciones para manejar las reacciones, reactivos y productos. Aquí se incluyen 
#las funciones que operan reacciones.

class Sustancia():
    def __init__(self, formula):
        self.formula = formula
        self.sustancia =self.formula[:self.formula.index("(")]#nombre de la sustancia sin incluir estado de agregación  
        self.coeficiente = None
    def cambiar_coeficiente(self, coefieciente):
            self.coeficiente = coefieciente
    def termodinamica(self):
        if not self.__coeficiente:
            delta_H = data.loc[self.formula, "ΔHf"]
            delta_S = data.loc[self.formula, "S°"]
            delta_G = data.loc[self.formula, "DGf°"]
            return {'delta_H':delta_H, 'delta_S':delta_S, 'delta_G':delta_G}
        else:
            delta_H = data.loc[self.formula, "ΔHf"]
            delta_S = data.loc[self.formula, "S°"]
            delta_G = data.loc[self.formula, "DGf°"]
            return {'delta_H':delta_H*self.coeficiente, 'delta_S':delta_S*self.coeficiente, 'delta_G':delta_G*self.coeficiente}
    def __str__(self):
        try:
            if self.coeficiente >1:
                return(str(self.coeficiente) + self.formula)
            elif self.coeficiente == 1:
                return(self.formula)
            else:
                return(self.formula)
        except TypeError:
            return(self.formula)
    
    def contador_atomos(self):
        diccionario = {}
        lista_mayus = []
        lista_minus = []
        lista_nros = []

        for i in range(len(self.sustancia)):
            if (self.sustancia[i].isupper()):
                lista_mayus.append(i)
            elif (self.sustancia[i].isdigit()):
                lista_nros.append(i)
            else:
                lista_minus.append(i)
        for i in lista_mayus:
            if ((i+1) in lista_minus):
                diccionario[self.sustancia[i] + self.sustancia[i+1]] = i+1
            else:
                diccionario[self.sustancia[i]] = i
        lista_keys=[]
        for i in list(diccionario.values()):
            if (i+1) in lista_nros:
                key = ''.join([k for k, v in diccionario.items() if v == (i)])
                diccionario[key] = self.sustancia[i+1]
            else:
                for k, v in diccionario.items():
                    if v == (i):
                        lista_keys.append(k)
        for i in lista_keys:
            diccionario[i] = 1    
        return diccionario
        
class Reactante():
    contador = 0
    def __init__(self, sustancia_1, sustancia_2=None):
        self.sustancia_1 = sustancia_1
        self.sustancia_2 = sustancia_2

    def __str__(self):
        if self.sustancia_2:
            return (f"{self.sustancia_1} + {self.sustancia_2}")
        else:
            return (f"{self.sustancia_1}")
        
    def __len__(self):
        if self.sustancia_1 and self.sustancia_2:
            return 2
        else:
            return 1
    def contador_atomos(self):
        try:
            new_dic = {}
            i = 0
            if not self.sustancia_2:
                return (self.sustancia_1.contador_atomos())
            else:
                for key, value in self.sustancia_1.contador_atomos().items():
                    if key in self.sustancia_2.contador_atomos():
                        new_dic[key] = int(self.sustancia_1.contador_atomos()[key])+int(self.sustancia_2.contador_atomos()[key])
                    else:
                        new_dic[key] = self.sustancia_1.contador_atomos()[key]

                for key, value in self.sustancia_2.contador_atomos().items():
                    if (key not in list(new_dic.keys())):
                        new_dic[key] = self.sustancia_2.contador_atomos()[key]
            return new_dic
        except TypeError:
            return "algo fue mal"

    def sustancias(self):
        if self.sustancia_2:
            return([self.sustancia_1, self.sustancia_2])
        else:
            return [self.sustancia_1]
    def __iter__(self):
        if self.sustancia_2:
            return iter([self.sustancia_1, self.sustancia_2])
        else:
            return iter([self.sustancia_1])

class Reacciones():
    def __init__(self, reactivos, productos):
        self.reactivos = reactivos
        self.productos = productos
        self.nro_atomos = len(self.reactivos.contador_atomos())

    def __str__(self):
        return(f"la reacción es: {self.reactivos} → {self.productos}")
    def pre_balancear(self):
        lista_sustancias = self.reactivos.sustancias() + self.productos.sustancias()
        #validar reacciones notando que reactivos y productos tengan mismos atomos
        data_reaccion = pd.DataFrame(0, index = list(self.reactivos.contador_atomos().keys()), columns = lista_sustancias)        
        lista_sustancias_nombres = [i.__str__() for i in list(data.columns)]
        elementos_en_sustancia = []
        lista_elementos = list(self.reactivos.contador_atomos().keys())
        for sustancia in (lista_sustancias):
            elementos_en_sustancia.append(sustancia.contador_atomos())
        for elemento, j in zip(lista_elementos, range(len(lista_elementos))):
            for i in range(len(elementos_en_sustancia)):
                if elemento in list(elementos_en_sustancia[i].keys()):
                    data_reaccion.iloc[j, i] = elementos_en_sustancia[i][elemento]
        return {"data_reaccion":data_reaccion, "largo_reactivos":len(self.reactivos), "largo_productos":len(self.productos)}
    
    def balancear(self):
        assert (len(self.reactivos.contador_atomos())) == (len(self.productos.contador_atomos())), "reacción invalida"

        init_printing(use_unicode=True)
        # H2(g) N2(g) NH3(g)
        # H     2     0      3
        # N     0     2      1
        diccionario_pre_balancear = self.pre_balancear()
        nro_sustancias = diccionario_pre_balancear["largo_reactivos"] + diccionario_pre_balancear["largo_productos"]
        largo_reactivos = diccionario_pre_balancear["largo_reactivos"]
        largo_productos = diccionario_pre_balancear["largo_productos"]
        coefs_reaccion = diccionario_pre_balancear["data_reaccion"]
        
        while (nro_sustancias == 3):
            #nro de atomos tambien considerar ya que es nro de ecuaciones
            if (largo_reactivos == 2 and self.nro_atomos==2):
                #sé que reaccion es del tipo a+b > c
                x, y, z = symbols('x y z')
                coeficiente_1 = float(coefs_reaccion.iloc[0,0])
                coeficiente_2 = float(coefs_reaccion.iloc[0,1])
                coeficiente_3 = float(coefs_reaccion.iloc[0,2])
                coeficiente_4 = float(coefs_reaccion.iloc[1,0])
                coeficiente_5 = float(coefs_reaccion.iloc[1,1])
                coeficiente_6 = float(coefs_reaccion.iloc[1,2])
            
                ((a,b,c),) = linsolve([coeficiente_1*x+coeficiente_2*y-coeficiente_3*z, coeficiente_4*x+coeficiente_5*y-coeficiente_6*z], (x, y, z))
                break
            elif (largo_reactivos == 2 and self.nro_atomos==3):
                x, y, z = symbols('x y z')
                coeficiente_1 = float(coefs_reaccion.iloc[0,0])
                coeficiente_2 = float(coefs_reaccion.iloc[0,1])
                coeficiente_3 = float(coefs_reaccion.iloc[0,2])
                coeficiente_4 = float(coefs_reaccion.iloc[1,0])
                coeficiente_5 = float(coefs_reaccion.iloc[1,1])
                coeficiente_6 = float(coefs_reaccion.iloc[1,2])
                coeficiente_7 = float(coefs_reaccion.iloc[2,0])
                coeficiente_8 = float(coefs_reaccion.iloc[2,1])
                coeficiente_9 = float(coefs_reaccion.iloc[2,2])
                
            
                ((a,b,c),) = linsolve([coeficiente_1*x+coeficiente_2*y-coeficiente_3*z, coeficiente_4*x+coeficiente_5*y-coeficiente_6*z, coeficiente_7*x+coeficiente_8*y-coeficiente_9*z], (x, y, z))
                break
        
        try:
            a = a.as_two_terms()[0]
            b = b.as_two_terms()[0]
            c = c.as_two_terms()[0]
            lista_int = list(range(10))
            
            for i in range(100):
                z = i+1
                if ((z*a in lista_int) and (z*b in lista_int) and (z*c in lista_int)):
                    a = z*a
                    b = z*b
                    c = z*c
                    break
                elif i == 3:
                    return ("valores no encontrados", len(self.reactivos.contador_atomos()), len(self.productos.contador_atomos()))
                else:
                    pass
            coefs_reactivos = [int(a),int(b)]
            coefs_productos = [int(c)]
            lista_sustancias_reactivos = self.reactivos.sustancias()#devuelve lista de sustancias en reactivos
            lista_sustancias_productos = self.productos.sustancias()
            for i in range(len(lista_sustancias_reactivos)):
                lista_sustancias_reactivos[i].cambiar_coeficiente(coefs_reactivos[i])
            for i in range(len(lista_sustancias_productos)):
                lista_sustancias_productos[i].cambiar_coeficiente(coefs_productos[i])
            return ("ecuacion balanceada: \n " + self.__str__())
        
        except AttributeError:
            return(((a,b,c),))
        except TypeError:
            return (coefs_reactivos, coefs_productos)
            
data["species"] = "elementos"
data["species"][0:3] = "Aluminum"
data["species"][3:15] = "Aqueous Solutions"
data["species"][15:20] = "Barium"
data["species"][20:22] = "Beryllium"
data["species"][22:27] = "Bromine"
data["species"][27:40] = "Calcium"
data["species"][40:66] = "Carbon"
data["species"][66:69] = "Cesium"
data["species"][69:74] = "Chlorine"
data["species"][74:77] = "Chromium"
data["species"][77:80] = "Copper"
data["species"][80:86] = "Fluorine"
data["species"][86:92] = "Hydrogen"
data["species"][92:97] = "Iodine"
data["species"][97:105] = "Iron"
data["species"][105:109] = "Lead"
data["species"][109:114] = "Lithium"
data["species"][114:119] = "Magnesium"
data["species"][119:123] = "Mercury"
data["species"][123:126] = "Nickel"
data["species"][126:142] = "Nitrogen"
data["species"][142:145] = "Oxygen"
data["species"][145:152] = "Phosphorus"
data["species"][152:158] = "Potassium"
data["species"][158:165] = "Silicon"
data["species"][165:169] = "Silver"
data["species"][169:179] = "Sodium"
data["species"][179:189] = "Sulfur"
data["species"][189:194] = "Tin"
data["species"][194:198] = "Titanium"
data["species"][198:] = "Zinc"

indice = pd.MultiIndex.from_arrays([data["species"], data.index])
data.index = indice

#trabajar en reaccion del tipo a+b → c+d, también agregar más nro de átomos

def especies():
    global titulo
    return titulo

def sustancias_especies(especie):
    return data.loc[especie].index.tolist()


def definir_sustancia(sustancia):
    return Sustancia(sustancia)

def definir_reactante(*args):
    return Reactante(*args)

def definir_reaccion(*args):
    return Reacciones(*args)

#definir funcion que tome lo que envíe desde el front y lo procese

oxigeno =data.loc['Sodium'].index[-1]
carbono = data.loc['Sodium'].index[-2]
dioxido_c = data.loc['Sodium'].index[-3]

