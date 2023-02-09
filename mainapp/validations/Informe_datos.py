import fitz
from pathlib import Path
import os
import io
from PIL import Image 
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from .Funciones_datos import tablas_rango_variable,contador_de_codigo_colegio,contador_de_tramos_de_canalizacion,generar_tabla_resumen_cables_tramos,generar_tabla_resumen_cables_puntos,generar_tabla_resumen_cables_fibra,tramos_recursivos,revisar_total_de_metros

class DatosTextoInforme:#Es donde se encuentra toda la data importante del informe
    def __init__(self,file):
        self._PAGINAS = [
            13,43,44,
            45,46,47,
            48,49,50
        ]#el numero de la pagina dentro del informe que posee la información importante
        self._pathfile=file
        

    def __del__(self):
        return

    def ordenar_datos(self):
        self.informe = []
        doc = fitz.open(self._pathfile)
        for i in self._PAGINAS:
            numero = i-1  
            page = doc.load_page(numero) #pagina que se quiere revisar del informe
            text = page.get_text("text")
            contenido = ""#contenido dentro de la celda
            for i in range(len(text)):
                if text[i] == '\n':
                    self.informe.append(contenido)
                    contenido = ""
                else: 
                    contenido += text[i]

    def informacion_de_las_tablas(self):
        self.actividad_asesoria = self.informe[:9]#Pagina que tiene la información de asesoria
        self.elementos_red = self.informe[12:18]#Tabla resumen de elementos de red
        self.tramos_canalización = self.informe[25:46]#Tabla resumen de tramos de canalización
        self.cables = self.informe[49:53]#Tabla resumen de Cables
        self.enlaces_existentes = tablas_rango_variable(self.informe,56)#Tabla resumen de Enlaces Existentes
        self.rack_existentes = tablas_rango_variable(self.informe,self.enlaces_existentes[1]+3)#Tabla resumen de Racks Existentes
        self.rack_proyectados = tablas_rango_variable(self.informe,self.rack_existentes[1]+3)#Tabla resumen de Racks Proyectados
        self.puntos_proyectados = tablas_rango_variable(self.informe,self.rack_proyectados[1]+3)#Tabla resumen de Puntos Proyectados
        self.tramos_proyectados = tablas_rango_variable(self.informe,self.puntos_proyectados[1]+3)#Tabla resumen de Tramos Proyectados

    #Verifica si los datos de elementos de red en la tabla resumen estan correctos
    def verificar_elementos_de_red_existentes(self):
        #print("########Elementos de Red ############")
        self.codigo_colegio = self.informe[71]
        self.nombre_colegio = self.informe[55]
        #print(f"Codigo {self.nombre_colegio} es {self.codigo_colegio}")
        self.cantidad_enlaces = self.elementos_red[1]
        self.cantidad_racks_proyectados = self.elementos_red[3]
        self.cantidad_puntos_proyectados = self.elementos_red[5]
        cant_enlaces = contador_de_codigo_colegio(self.codigo_colegio,self.cantidad_enlaces,self.enlaces_existentes,"Enlaces")
        cant_racks = contador_de_codigo_colegio(self.codigo_colegio,self.cantidad_racks_proyectados,self.rack_proyectados,"Racks Proyectados")
        cant_puntos = contador_de_codigo_colegio(self.codigo_colegio,self.cantidad_puntos_proyectados,self.puntos_proyectados,"Puntos Proyectados")
        return (f"Nombre es <b>{self.nombre_colegio}</b> <br>Codigo <b>{self.codigo_colegio}</b>.<br>  {cant_enlaces} {cant_racks} {cant_puntos}")
    
    #Verifica si los datos de tramos de canalización en la tabla resumen estan correctos
    def verificar_tramos_de_canalizacion(self):
        cantidad_tramos_canalizacion = [
            self.tramos_canalización[1],self.tramos_canalización[4],
            self.tramos_canalización[7],self.tramos_canalización[10],
            self.tramos_canalización[13],self.tramos_canalización[16],
            self.tramos_canalización[19]
        ]
        nombre_canalizacion = [
            self.tramos_canalización[0],self.tramos_canalización[3],
            self.tramos_canalización[6],self.tramos_canalización[9],
            self.tramos_canalización[12],self.tramos_canalización[15],
            self.tramos_canalización[18]
        ]
        TIPO_CANALIZACION = [
            "3/4\"","1\"","1 1/4\"",
            "1 1/2\"","2\"","2 1/2\"",
            "Escalerilla "
        ]
        metros_canalizacion = [
            self.tramos_canalización[2],self.tramos_canalización[5],
            self.tramos_canalización[8],self.tramos_canalización[11],
            self.tramos_canalización[14],self.tramos_canalización[17],
            self.tramos_canalización[20]
        ]
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
        return (f"El total de fibra es <b>{total_metros_fibra[0]}</b> m.<br> Los puntos de fibra son : <br> &nbsp; &nbsp;{total_metros_fibra[1]}. <br> El total de UTP-6 es <b>{total_metros_puntos[0]}</b> m. <br>Los puntos UTP-6 son: <br> &nbsp; &nbsp;{total_metros_puntos[1]}")

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

