import fitz
from pathlib import Path
import os
import io
from PIL import Image 
import cv2
import insightface
import re
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from .Funciones_datos import string_to_int,tablas_rango_variable,contador_de_codigo_colegio,contador_de_tramos_de_canalizacion,generar_tabla_resumen_cables_tramos,generar_tabla_resumen_cables_puntos,generar_tabla_resumen_cables_fibra,tramos_recursivos,revisar_total_de_metros

class DatosTextoInforme:#Es donde se encuentra toda la data importante del informe
    def __init__(self,file):
        #el numero de la pagina dentro del informe que posee la información importante
        self._PAGINAS = [
            13,43,44,
            45,46,47,
            48,49,50,
            51,52,53
        ]
        self._pathfile=file
        

    def __del__(self):
        return

    def ordenar_datos(self):
        self.informe = []
        doc = fitz.open(self._pathfile)
        for i_pagina in self._PAGINAS:
            numero = i_pagina-1  
            #pagina que se quiere revisar del informe
            page = doc.load_page(numero) 
            text = page.get_text("text")
            contenido = ""
            #contenido dentro de la celda
            for j_linea in range(len(text)):
                if text[j_linea] == '\n':
                    self.informe.append(contenido)
                    contenido = ""
                else: 
                    contenido += text[j_linea]

    def informacion_de_las_tablas(self):
        #Pagina que tiene la información de asesoria
        self.actividad_asesoria = self.informe[:9]
        #Tabla resumen de elementos de red
        self.elementos_red = self.informe[12:18]
        #Tabla resumen de tramos de canalización
        self.tramos_canalizacion = self.informe[25:46]
        #Tabla resumen de Cables
        self.cables = self.informe[49:53]
        #Tabla resumen de Enlaces Existentes
        self.enlaces_existentes = tablas_rango_variable(self.informe,56)
        #Tabla resumen de Racks Existentes
        self.rack_existentes = tablas_rango_variable(self.informe,self.enlaces_existentes[1]+3)
        #Tabla resumen de Racks Proyectados
        self.rack_proyectados = tablas_rango_variable(self.informe,self.rack_existentes[1]+3)
        #Tabla resumen de Puntos Proyectados
        self.puntos_proyectados = tablas_rango_variable(self.informe,self.rack_proyectados[1]+3)
        #Tabla resumen de Tramos Proyectados
        self.tramos_proyectados = tablas_rango_variable(self.informe,self.puntos_proyectados[1]+3)

    #Verifica si los datos de elementos de red en la tabla resumen estan correctos
    def verificar_elementos_de_red_existentes(self):
        self.codigo_colegio = self.informe[71]
        self.nombre_colegio = self.informe[55]
        self.cantidad_enlaces = self.elementos_red[1]
        self.cantidad_racks_proyectados = self.elementos_red[3]
        self.cantidad_puntos_proyectados = self.elementos_red[5]
        cant_enlaces = contador_de_codigo_colegio(self.codigo_colegio,self.cantidad_enlaces,self.enlaces_existentes,"Enlaces")
        cant_racks = contador_de_codigo_colegio(self.codigo_colegio,self.cantidad_racks_proyectados,self.rack_proyectados,"Racks Proyectados")
        cant_puntos = contador_de_codigo_colegio(self.codigo_colegio,self.cantidad_puntos_proyectados,self.puntos_proyectados,"Puntos Proyectados")
        return (f"Nombre es <b>{self.nombre_colegio}</b> <br>RBD <b>{self.codigo_colegio}</b>.<br>  {cant_enlaces} {cant_racks} {cant_puntos}<hr>")
    
    #Verifica si los datos de tramos de canalización en la tabla resumen estan correctos
    def verificar_tramos_de_canalizacion(self):
        #Cuenta la cantidad de tramos que hay en la tabla tramos, esto incluye UTP y Fibra
        self.cantidad_tramos=0
        for i in self.tramos_proyectados[0]:
            if i == self.codigo_colegio:
                self.cantidad_tramos += 1
        #Cuenta la cantidad de los distintos tramos de canalizacion para UTP-6
        cantidad_tramos_canalizacion = [
            self.tramos_canalizacion[1],self.tramos_canalizacion[4],
            self.tramos_canalizacion[7],self.tramos_canalizacion[10],
            self.tramos_canalizacion[13],self.tramos_canalizacion[16],
            self.tramos_canalizacion[19]
        ]
        
        nombre_canalizacion = [
            self.tramos_canalizacion[0],self.tramos_canalizacion[3],
            self.tramos_canalizacion[6],self.tramos_canalizacion[9],
            self.tramos_canalizacion[12],self.tramos_canalizacion[15],
            self.tramos_canalizacion[18]
        ]
        TIPO_CANALIZACION = [
            "3/4\"","1\"","1 1/4\"",
            "1 1/2\"","2\"","2 1/2\"",
            "Escalerilla "
        ]
        metros_canalizacion = [
            self.tramos_canalizacion[2],self.tramos_canalizacion[5],
            self.tramos_canalizacion[8],self.tramos_canalizacion[11],
            self.tramos_canalizacion[14],self.tramos_canalizacion[17],
            self.tramos_canalizacion[20]
        ]
        #Verifica si la cantidad de tramos de canalizacion contados es igual a los de la tabla resumen, para cada tipo.
        verificar = []
        for i in range(len(TIPO_CANALIZACION)):
            verificar.append(
                contador_de_tramos_de_canalizacion(TIPO_CANALIZACION[i],
                cantidad_tramos_canalizacion[i],metros_canalizacion[i],
                self.tramos_proyectados,nombre_canalizacion[i])
            )
        return verificar
    
    #Verifica si los datos de los metros de cable UTP-6 y Fibra en la tabla resumen estan correctos
    def verificar_metros_de_cable(self):
        tabla_resumen_cables_tramos = generar_tabla_resumen_cables_tramos(self.tramos_proyectados,self.codigo_colegio)
        tabla_resumen_cables_puntos = generar_tabla_resumen_cables_puntos(self.puntos_proyectados,self.codigo_colegio)
        tabla_resumen_cables_fibra = generar_tabla_resumen_cables_fibra(self.rack_proyectados,self.codigo_colegio)
        total_metros_fibra = revisar_total_de_metros(tabla_resumen_cables_fibra,tabla_resumen_cables_tramos)
        total_metros_puntos = revisar_total_de_metros(tabla_resumen_cables_puntos,tabla_resumen_cables_tramos)
        return (f"El total de fibra es <b>{total_metros_fibra[0]}</b> m.<br> Los puntos de fibra son : <br> &nbsp; &nbsp;{total_metros_fibra[1]}. <br> El total de UTP-6 es <b>{total_metros_puntos[0]}</b> m. <br>Los puntos UTP-6 son: <br> &nbsp; &nbsp;{total_metros_puntos[1]}<hr>")

    #Detecta las caras que encuentra en las fotos que estan en el informe
    def detectar_caras(self,numero_pagina,file_name):#Numero de la pagina donde comienzan las fotos
        doc = fitz.open(self._pathfile)
        caras = []
        image_path = f"static/tmp/images{file_name}"
        try:
            os.mkdir(image_path)
        except:
            pass
        app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))
        for page_index in range(numero_pagina,len(doc)):
            # get the page itself
            page = doc.load_page(page_index)
            image_list = page.get_images()
            for image_index, img in enumerate(page.get_images(), start=1):
                # get the XREF of the image
                xref = img[0]
                # extract the image bytes
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                # get the image extension
                image_ext = base_image["ext"]
                # load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                image.save(open(f"{image_path}/image{page_index+1}_{image_index}.{image_ext}", "wb"))
                image = cv2.imread(f"{image_path}/image{page_index+1}_{image_index}.{image_ext}")
                image_name = f"image{page_index+1}_{image_index}"
                faces = app.get(image)
                if len(faces) > 0: 
                    caras.append(f"Encontrada cara en la pagina foto <b>{page_index+1}_{image_index}</b> <img src=\"/static/tmp/images{file_name}/image{page_index+1}_{image_index}.{image_ext}\"></img>")
        return caras
    
    def datos_colegio(self):
        #RBD del colegio y el nombre de el colegio
        datos = [self.informe[71],self.informe[55]]
        return datos

    #La función extrae de el informe el texto contenido en la sección de planos de red
    def ordenar_datos_planos(self):
        self.planos = []
        stop = 0
        #desde esta pagina en promedio parte la sección de los planos
        pagina_inicio = 50
        doc = fitz.open(self._pathfile)
        #se utiliza, ya que no se sabe cuantas paginas de planos habra
        while True:
            numero = pagina_inicio-1  
            #pagina que se quiere revisar del informe
            page = doc.load_page(numero) 
            text = page.get_text("text")
            contenido = ""
            #contenido dentro de la celda
            for i in range(len(text)):
                if text[i] == '\n':
                    #Esta linea representa el comienzo de la siguiente sección, osea fin de la sección de los planos
                    if contenido == "FOTOS RED PROYECTADA - AULAS CONECTADAS 2022":
                        stop = 1 
                        break
                    elif contenido == "DIAGRAMA LÓGICO":
                        self.planos.clear()
                    self.planos.append(contenido)
                    contenido = ""
                else: 
                    contenido += text[i]
            pagina_inicio += 1
            if stop == 1: break

    #Toma el contenido extraido y solo toma los numeros
    def separar_en_los_nuemros(self):
        numeros = []
        for i in self.planos:
            a = string_to_int(i)
            if a != 0:
                numeros.append(a)
        
        return numeros

    #Se revisan los numeros encontrados y se verfica si todos los puntos proyectados estan presentes en los planos
    def contar_puntos_en_plano(self,arreglo):
        count = 0
        n_puntos = int(self.elementos_red[5])
        size = len(arreglo)
        repite = [0] * (n_puntos+1)
        #Counting sort
        for i in range(0, size):
            repite[arreglo[i]] += 1
        
        for i in range(1,len(repite)):
            if repite[i] == 0:
                count += 1 
        #Revisa si falta algun punto
        if count == 0:
            return("Estan todos los <b><font color=green>Puntos Proyectados</font></b> presentes en los planos")
        else:
            return(f"Faltan <b><font color=red>{count} Punto o Puntos Proyectados</font></b> en los planos")
    
    #Toma el contenido extraido y solo toma los tramos
    def separar_los_tramos(self):
        tramos = []
        for i in self.planos:
            tramos += re.findall("^T[0-5][0-9]",i)
        return tramos

    def contar_tramos_en_planos(self,tramos):  
        try:
            n_tramos = self.cantidad_tramos
            numeros = []
            size = len(tramos)
            repite = [0] * (n_tramos+1)
            #Busca los tramos con el formato T01, T02..., TNN, dentro de los planos
            for i in tramos:
                numeros += re.findall("[0-5][0-9]",i)
            #Convierte los tramos en numeros T01 = 1
            for  i in range(len(numeros)):
                numeros[i] = string_to_int(numeros[i])
            #Counting sort
            for i in range(0, size):
                repite[numeros[i]] += 1
            count = 0
            for i in range(1,len(repite)):
                if repite[i] == 0:
                    count += 1 
            #Revisa si falta algun tramo
            if count == 0:
                return("Estan todos los <b><font color=green>Tramos proyectados</font></b> presentes en los planos")
            else:
                return(f"Faltan <b><font color=red>{count} Tramo o Tramos Proyectados</font></b> en los planos")
        except:
            return("No se pudo contar los tramos")

    def contar_puntos_cuadro_resumen(self):
        try:
            encontrado_puntos = 0
            encontrado_racks = 0
            for i in range(2,len(self.planos)):
                if (self.planos[i] == self.planos[1] 
                        or self.planos[i]==(f"{self.planos[1]} ANEXO")):
                    encontrado_puntos += string_to_int(self.planos[i-1])
                    encontrado_racks += string_to_int(self.planos[i-5])        
            if (round(encontrado_puntos/2) == int(self.elementos_red[5])
                    and round(encontrado_racks/2) == int(self.elementos_red[3])):
                return ("La cantidad de puntos y racks proyectados encontrados en los cuadros resumen de los planos <b><font color=green>coinciden</font></b><hr>")
            elif (int(self.elementos_red[5]) == round(encontrado_puntos/2) 
                    and round(encontrado_racks/2) != int(self.elementos_red[3])):
                return ("La cantidad de puntos proyectados encontrados en los cuadros resumen de los planos <b><font color=green>coinciden</font></b> y racks encontrados <b><font color=red>no coinciden</font></b><hr>")
            elif (int(self.elementos_red[5]) != round(encontrado_puntos/2) 
                    and round(encontrado_racks/2) == int(self.elementos_red[3])):
                return ("La cantidad de racks encontrados en los cuadros resumen de los planos <b><font color=green>coinciden</font></b> y los puntos encontrados <b><font color=red>no coinciden</font></b><hr>")
            else:
                return ("No coinciden la cantidad de puntos y racks proyectados encontrados en los cuadros resumen de los planos<hr>")
        except:
            return ("Error en la lectura de Cuadro Resumen<hr>")
        
        