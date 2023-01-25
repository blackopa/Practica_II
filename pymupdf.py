import fitz
from pathlib import Path
import os


def Datos_pagina(file_name,paginas):
    datos_paginas=[]
    for i in paginas:
        numero=i-1
        doc= fitz.open(file_name)    
        page= doc.load_page(numero) #pagina que se quiere revisar del informe
        text = page.get_text("text")
        palabra=""
        for i in range(len(text)):
            if text[i]=='\n':
                datos_paginas.append(palabra)
                palabra=""
            else: 
                palabra+=text[i]
    return(datos_paginas)
#enlaces=text[50]
#print(enlaces)
f_list = os.listdir("./InformesPdf/Diciembre_adelante")
file_name="./InformesPdf/Diciembre_adelante/%s"%(f_list[0])
paginas=[13,43,44,45,46,47,48,49]
resultado=Datos_pagina(file_name, paginas)
#print(resultado[:9])
Actividad_asesoria=resultado[:9]
#print(Actividad_asesoria)
Elementos_red=resultado[12:18]
#print(Elementos_red)
Tramos_canalización=resultado[25:46]
#print(Tramos_canalización)
Cables=resultado[49:53]
#print(Cables)
def extraer_tabla_variable(resultado,limite):
    count=0
    a=[]
    for i in range(limite,len(resultado)):
        if resultado[i]==resultado[53]:
            count=i
            break
        else:   
            a.append(resultado[i])
    return(a,count)
Enlaces_existentes=extraer_tabla_variable(resultado,56)
#print(Enlaces_existentes[0])
#print(Enlaces_existentes[1])
Rack_existentes=extraer_tabla_variable(resultado,Enlaces_existentes[1]+3)
#print(Rack_existentes[0])
#print(Rack_existentes[1])
Rack_proyectados=extraer_tabla_variable(resultado,Rack_existentes[1]+3)
#print(Rack_proyectados[0])
#print(Rack_proyectados[1])
Puntos_Proyectados=extraer_tabla_variable(resultado,Rack_proyectados[1]+3)
#print(Puntos_Proyectados[0])
#print(Puntos_Proyectados[1])
Tramos_Proyectados=extraer_tabla_variable(resultado,Puntos_Proyectados[1]+3)
print(Tramos_Proyectados[0])
print(Tramos_Proyectados[1])
